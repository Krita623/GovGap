from __future__ import annotations

import json
import os
import re
import time
from typing import Any

import requests
from dotenv import load_dotenv
from pydantic import ValidationError

from src.models.proposal import Proposal
from src.models.semantics import ProposalSemantics, failed_semantics_fallback
from src.modules.llm.normalize_semantics import normalize_semantics


SYSTEM_PROMPT = """You extract only proposal text disclosures into strict JSON.

Rules:
- Use only the provided proposal title and description.
- Do not use trace data, ABI data, selectors, known addresses, chain knowledge, or external knowledge.
- Do not infer addresses that do not appear in the text.
- If uncertain, output "unknown".
- Do not output risk score, severity, dimensional scores, overall score, or security conclusions.
- Output pure JSON only. No markdown.
- The field llm_used_for_scoring must always be false.
"""

SCHEMA_INSTRUCTIONS = """Return exactly this JSON shape. No extra fields:
{
  "proposal_summary": "string",
  "disclosed_entities": [
    {
      "name": "string",
      "address": "0x... or null",
      "entity_type": "governor | timelock | treasury | token | bridge | multisig | proxy | implementation | external_contract | unknown",
      "disclosure_level": "explicit | implicit | not_disclosed",
      "textual_evidence": "string"
    }
  ],
  "disclosed_addresses": [
    {
      "address": "0x...",
      "textual_evidence": "string"
    }
  ],
  "claimed_actions": [
    {
      "raw_action": "string",
      "canonical_action": "parameter_update | upgrade | transfer | approval | contract_creation | governance_proposal_creation | role_change | bridge | treasury_operation | maintenance | unknown",
      "object": "string or null",
      "claimed_effect": "string",
      "textual_evidence": "string",
      "confidence": 0.0
    }
  ],
  "claimed_complexity": {
    "level": "simple | moderate | complex | unknown",
    "reason": "string",
    "textual_evidence": "string"
  },
  "disclosed_functions": [
    {
      "function_name": "string",
      "textual_evidence": "string"
    }
  ],
  "limitations": [
    "string"
  ],
  "llm_status": "success | repaired | failed",
  "llm_used_for_scoring": false
}
"""


def extract_proposal_semantics(proposal: Proposal) -> ProposalSemantics:
    """Extract proposal text claims.

    This is the only module boundary where LLM usage is allowed. It must not
    import or read trace facts.
    """

    load_dotenv()
    fallback_summary = _fallback_summary(proposal)

    try:
        raw_output = _call_llm(_build_extraction_prompt(proposal))
        parsed = _parse_json_object(raw_output)
        parsed["llm_status"] = "success"
        parsed["llm_used_for_scoring"] = False
        return normalize_semantics(ProposalSemantics.model_validate(parsed))
    except Exception as first_error:
        try:
            repaired_output = _call_llm(_build_repair_prompt(raw_output if "raw_output" in locals() else "", first_error))
            repaired = _parse_json_object(repaired_output)
            repaired["llm_status"] = "repaired"
            repaired["llm_used_for_scoring"] = False
            return normalize_semantics(ProposalSemantics.model_validate(repaired))
        except Exception as repair_error:
            return failed_semantics_fallback(
                fallback_summary,
                f"LLM semantics extraction failed: {type(repair_error).__name__}: {repair_error}",
            )


def _build_extraction_prompt(proposal: Proposal) -> str:
    return (
        f"{SCHEMA_INSTRUCTIONS}\n"
        "Extract disclosed information from this proposal text only.\n\n"
        f"TITLE:\n{proposal.title or 'unknown'}\n\n"
        f"DESCRIPTION:\n{proposal.body or 'unknown'}"
    )


def _build_repair_prompt(raw_output: str, error: Exception) -> str:
    if isinstance(error, ValidationError):
        error_text = error.json()
    else:
        error_text = str(error)
    return (
        f"{SCHEMA_INSTRUCTIONS}\n"
        "Repair the following invalid JSON output so it validates exactly against the schema. "
        "Remove all extra fields. Do not add scoring, severity, or conclusions.\n\n"
        f"VALIDATION_ERROR:\n{error_text}\n\n"
        f"INVALID_OUTPUT:\n{raw_output}"
    )


def _call_llm(prompt: str) -> str:
    base_url = os.getenv("LLM_BASE_URL", "").rstrip("/")
    api_key = os.getenv("LLM_API_KEY", "")
    model = os.getenv("LLM_MODEL", "")
    if not base_url or not api_key or not model:
        raise RuntimeError("LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL must be set")

    if base_url.endswith("/messages"):
        return _call_anthropic_messages(base_url, api_key, model, prompt)
    return _call_openai_compatible(base_url, api_key, model, prompt)


def _call_openai_compatible(base_url: str, api_key: str, model: str, prompt: str) -> str:
    endpoint = base_url
    if not endpoint.endswith("/chat/completions"):
        endpoint = f"{endpoint}/chat/completions"
    response = _post_with_retry(
        endpoint,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "Connection": "close"},
        json_payload={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        },
    )
    if not response.ok:
        raise RuntimeError(f"LLM request failed: {response.status_code} {response.text[:500]}")
    body = response.json()
    try:
        content = body["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError("LLM response did not contain choices[0].message.content") from exc
    if not isinstance(content, str):
        raise RuntimeError("LLM content is not a string")
    return content


def _call_anthropic_messages(base_url: str, api_key: str, model: str, prompt: str) -> str:
    response = _post_with_retry(
        base_url,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "Connection": "close",
        },
        json_payload={
            "model": model,
            "max_tokens": 4096,
            "temperature": 0,
            "system": SYSTEM_PROMPT,
            "messages": [{"role": "user", "content": prompt}],
        },
    )
    if not response.ok:
        raise RuntimeError(f"LLM request failed: {response.status_code} {response.text[:500]}")
    body = response.json()
    content = body.get("content")
    if not isinstance(content, list) or not content:
        raise RuntimeError("Anthropic response did not contain content")
    first = content[0]
    if not isinstance(first, dict) or not isinstance(first.get("text"), str):
        raise RuntimeError("Anthropic content[0].text is missing")
    return first["text"]


def _post_with_retry(endpoint: str, *, headers: dict[str, str], json_payload: dict[str, Any]) -> requests.Response:
    max_retries = max(1, int(os.getenv("LLM_MAX_RETRIES", "3")))
    retry_delay = max(0.0, float(os.getenv("LLM_RETRY_DELAY_SECONDS", "2")))
    last_error: requests.RequestException | None = None

    for attempt in range(1, max_retries + 1):
        try:
            return requests.post(endpoint, headers=headers, json=json_payload, timeout=120)
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_error = exc
            if attempt >= max_retries:
                break
            time.sleep(retry_delay * attempt)

    assert last_error is not None
    raise last_error


def _parse_json_object(raw_output: str) -> dict[str, Any]:
    text = raw_output.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    parsed = json.loads(text)
    if not isinstance(parsed, dict):
        raise ValueError("LLM output must be a JSON object")
    return parsed


def _fallback_summary(proposal: Proposal) -> str:
    if proposal.title:
        return proposal.title[:500]
    if proposal.body:
        return proposal.body[:500]
    return "unknown"

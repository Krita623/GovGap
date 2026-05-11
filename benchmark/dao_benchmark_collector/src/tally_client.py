"""Tally Governance GraphQL API client.

Responsible for reading the Tally API key, building GraphQL requests, and
returning normalized response payloads to higher-level collection modules.
"""

from __future__ import annotations

import os
import time
from typing import Any

import requests
from dotenv import load_dotenv


TALLY_ENDPOINT = "https://api.tally.xyz/query"


class TallyClientError(RuntimeError):
    """Base error raised by the Tally API client."""


class TallyGraphQLError(TallyClientError):
    """Raised when Tally returns GraphQL errors."""


class TallyClient:
    """Small wrapper around the Tally GraphQL endpoint."""

    def __init__(
        self,
        api_key: str | None = None,
        endpoint: str = TALLY_ENDPOINT,
        sleep_seconds: float = 0.5,
        max_retries: int = 3,
    ) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.sleep_seconds = sleep_seconds
        self.max_retries = max_retries

    @classmethod
    def from_env(
        cls,
        sleep_seconds: float = 0.5,
        max_retries: int = 3,
    ) -> "TallyClient":
        """Create a client using TALLY_API_KEY from the environment."""
        load_dotenv()
        api_key = os.getenv("TALLY_API_KEY")
        if not api_key:
            raise TallyClientError("Missing TALLY_API_KEY environment variable.")
        return cls(
            api_key=api_key,
            sleep_seconds=sleep_seconds,
            max_retries=max_retries,
        )

    def execute(self, query: str, variables: dict | None = None) -> dict:
        """Execute a GraphQL query against Tally."""
        if not self.api_key:
            raise TallyClientError("Tally API key is required.")

        body: dict[str, Any] = {
            "query": query,
            "variables": variables or {},
        }
        last_error: Exception | None = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.post(
                    self.endpoint,
                    json=body,
                    headers=self.headers(),
                    timeout=30,
                )
            except requests.RequestException as exc:
                last_error = exc
                if attempt == self.max_retries:
                    raise TallyClientError(
                        f"Tally request failed after {self.max_retries} attempts: {exc}"
                    ) from exc
                self._sleep_before_retry()
                continue

            if 400 <= response.status_code < 500:
                raise TallyClientError(
                    f"Tally request failed with HTTP {response.status_code}: {response.text}"
                )

            if response.status_code >= 500:
                last_error = TallyClientError(
                    f"Tally request failed with HTTP {response.status_code}: {response.text}"
                )
                if attempt == self.max_retries:
                    raise last_error
                self._sleep_before_retry()
                continue

            try:
                payload = response.json()
            except ValueError as exc:
                raise TallyClientError(f"Tally returned invalid JSON: {response.text}") from exc

            self._sleep_after_request()

            errors = payload.get("errors")
            if errors:
                raise TallyGraphQLError(f"Tally GraphQL errors: {errors}")

            data = payload.get("data")
            if data is None:
                raise TallyClientError(f"Tally response missing data field: {payload}")
            return data

        raise TallyClientError(f"Tally request failed: {last_error}")

    def headers(self) -> dict[str, str]:
        """Build request headers using the Api-Key header expected by Tally."""
        if not self.api_key:
            raise TallyClientError("Tally API key is required.")
        return {
            "Content-Type": "application/json",
            "Api-Key": self.api_key,
        }

    def _sleep_before_retry(self) -> None:
        """Sleep between retry attempts when configured."""
        if self.sleep_seconds > 0:
            time.sleep(self.sleep_seconds)

    def _sleep_after_request(self) -> None:
        """Sleep after completed API responses to avoid Tally rate limits."""
        if self.sleep_seconds > 0:
            time.sleep(self.sleep_seconds)

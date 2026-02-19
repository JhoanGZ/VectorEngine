from __future__ import annotations

import logging
import time
from typing import Any, Optional, Dict

from openai import OpenAI
from app.config import settings
from .base_llm import BaseLLM

logger = logging.getLogger(__name__)


class OpenAIAdapter(BaseLLM):
    supports_response_format = True

    # Conservative defaults for Phase 1 (first implementation)
    _DEFAULT_MODEL = "gpt-4o-mini"
    _DEFAULT_TIMEOUT_S = 20.0
    _MAX_RETRIES = 2  # total attempts = 1 + _MAX_RETRIES
    _BACKOFF_BASE_S = 0.6

    def __init__(self) -> None:
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.2,
        model: str = _DEFAULT_MODEL,
        response_format: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Production-aware behavior:
        - Explicit timeout per request
        - Retry with backoff on transient failures
        - Logs latency and high-level call metadata
        - Raises a bounded RuntimeError for the application layer
        """
        kwargs: Dict[str, Any] = {
            "model": model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            # OpenAI Python SDK supports request timeouts; keeping it explicit improves resiliency.
            "timeout": self._DEFAULT_TIMEOUT_S,
        }

        if response_format is not None:
            kwargs["response_format"] = response_format

        last_exc: Optional[Exception] = None

        for attempt in range(self._MAX_RETRIES + 1):
            start = time.perf_counter()
            try:
                response = self.client.chat.completions.create(**kwargs)

                content = response.choices[0].message.content
                if content is None:
                    # Defensive: content should exist; treat as provider failure
                    raise RuntimeError("OpenAI returned an empty message content.")

                elapsed = time.perf_counter() - start
                logger.info(
                    "llm_call_success provider=openai model=%s latency_s=%.3f attempt=%d",
                    model,
                    elapsed,
                    attempt + 1,
                )
                return content

            except Exception as exc:
                elapsed = time.perf_counter() - start
                last_exc = exc

                # Log with traceback for debugging; message remains stable for callers
                logger.warning(
                    "llm_call_failed provider=openai model=%s latency_s=%.3f attempt=%d/%d error=%s",
                    model,
                    elapsed,
                    attempt + 1,
                    self._MAX_RETRIES + 1,
                    str(exc),
                    exc_info=True,
                )

                # If no more retries, fail with a bounded exception
                if attempt >= self._MAX_RETRIES:
                    raise RuntimeError("OpenAI LLM invocation failed after retries.") from exc

                # Simple exponential-ish backoff (kept deterministic & lightweight)
                sleep_s = self._BACKOFF_BASE_S * (attempt + 1)
                time.sleep(sleep_s)

        # Should be unreachable, but keeps type checkers happy
        raise RuntimeError("OpenAI LLM invocation failed.") from last_exc

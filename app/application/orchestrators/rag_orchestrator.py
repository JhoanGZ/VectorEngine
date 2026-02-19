import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


class RAGOrchestrator:
    def __init__(self, repository, embedding_service, llm, fallback_llm=None):
        self.repository = repository
        self.embedding_service = embedding_service
        self.llm = llm
        self.fallback_llm = fallback_llm

    def execute(
        self,
        query: str,
        system_prompt: str,
        user_instruction_template: str,
        top_k: int = 5,
        temperature: float = 0.1,
        response_format: Optional[dict] = None,
    ) -> str:

        embedding = self.embedding_service.generate_embedding(query)
        results = self.repository.similarity_search(embedding, top_k)

        if not results:
            context = "No relevant documents retrieved from knowledge base."
        else:
            context = "\n\n".join(
                [r["content"] for r in results if r.get("content")]
            )

        user_prompt = user_instruction_template.format(
            context=context,
            query=query,
        )

        if response_format and not getattr(self.llm, "supports_response_format", False):
            response_format = None

        provider_name = type(self.llm).__name__

        logger.info(
            "llm_invocation provider=%s top_k=%d temperature=%.2f structured=%s",
            provider_name,
            top_k,
            temperature,
            bool(response_format),
        )

        start = time.perf_counter()

        try:
            response = self.llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                response_format=response_format,
            )

            duration = time.perf_counter() - start

            logger.info(
                "llm_completed provider=%s duration_s=%.3f",
                provider_name,
                duration,
            )

            return response

        except Exception:
            logger.warning(
                "primary_llm_failed provider=%s",
                provider_name,
                exc_info=True,
            )

        # Fallback strategy
        if not self.fallback_llm:
            logger.error("no_fallback_llm_configured")
            raise

        fallback_provider = type(self.fallback_llm).__name__
        logger.info("fallback_to_provider provider=%s", fallback_provider)

        start_fallback = time.perf_counter()

        try:
            response = self.fallback_llm.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                response_format=response_format,
            )

            duration_fallback = time.perf_counter() - start_fallback

            logger.info(
                "llm_completed provider=%s duration_s=%.3f",
                fallback_provider,
                duration_fallback,
            )

            return response

        except Exception:
            logger.error(
                "fallback_llm_failed provider=%s",
                fallback_provider,
                exc_info=True,
            )
            raise

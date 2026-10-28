"""Cliente HTTP resiliente com retries e backoff para a OpenF1 API."""

from __future__ import annotations

import time
from typing import Any, Callable

import httpx

from f1.utils.logger import get_logger

logger = get_logger(__name__)


class OpenF1ApiError(Exception):
    """Exceção levantada quando as chamadas à OpenF1 falham após retries."""


class HttpClient:
    """Cliente HTTP com timeout e retry exponencial."""

    def __init__(
        self,
        base_url: str,
        timeout: int = 10,
        max_retries: int = 3,
        sleep_fn: Callable[[float], None] = time.sleep,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        """Inicializa o cliente HTTP."""
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.sleep = sleep_fn
        self.transport = transport

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Executa uma requisição GET retornando JSON com retries em 429/5xx/timeout."""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        clean_params = {k: v for k, v in (params or {}).items() if v is not None}

        last_exc: Exception | None = None
        for attempt in range(1, self.max_retries + 1):
            try:
                with httpx.Client(
                    timeout=self.timeout, transport=self.transport
                ) as client:
                    logger.debug("GET %s (tentativa %d/%d)", url, attempt, self.max_retries)
                    resp = client.get(url, params=clean_params)

                    if resp.status_code == 429 or resp.status_code >= 500:
                        logger.warning(
                            "Status %d em %s. Tentativa %d/%d.",
                            resp.status_code,
                            url,
                            attempt,
                            self.max_retries,
                        )
                        if attempt < self.max_retries:
                            self.sleep(0.5 * (2 ** (attempt - 1)))
                            continue
                        resp.raise_for_status()

                    resp.raise_for_status()
                    data = resp.json()
                    return data if isinstance(data, list) else []

            except (httpx.TimeoutException, httpx.NetworkError) as exc:
                last_exc = exc
                logger.warning(
                    "Erro de rede/timeout em %s: %s (tentativa %d/%d)",
                    url,
                    exc,
                    attempt,
                    self.max_retries,
                )
                if attempt < self.max_retries:
                    self.sleep(0.5 * (2 ** (attempt - 1)))
                    continue
            except httpx.HTTPStatusError as exc:
                raise OpenF1ApiError(f"HTTP erro {exc.response.status_code} ao acessar {url}") from exc
            except Exception as exc:
                raise OpenF1ApiError(f"Erro inesperado ao acessar {url}: {exc}") from exc

        raise OpenF1ApiError(f"Falha após {self.max_retries} tentativas em {url}") from last_exc


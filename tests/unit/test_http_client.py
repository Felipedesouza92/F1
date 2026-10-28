"""Testes unitários para o cliente HTTP resiliente."""

import httpx
import pytest

from f1.ingestion.http_client import HttpClient, OpenF1ApiError


def test_http_client_success():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=[{"meeting_key": 1, "year": 2024}])

    transport = httpx.MockTransport(mock_handler)
    client = HttpClient(base_url="https://api.test", transport=transport)
    data = client.get("meetings")
    assert len(data) == 1
    assert data[0]["meeting_key"] == 1


def test_http_client_retry_on_500():
    calls = 0

    def mock_handler(request: httpx.Request) -> httpx.Response:
        nonlocal calls
        calls += 1
        if calls < 2:
            return httpx.Response(500)
        return httpx.Response(200, json=[{"ok": True}])

    transport = httpx.MockTransport(mock_handler)
    client = HttpClient(
        base_url="https://api.test",
        transport=transport,
        sleep_fn=lambda _: None,
    )
    data = client.get("test")
    assert calls == 2
    assert data == [{"ok": True}]


def test_http_client_4xx_no_retry():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(404)

    transport = httpx.MockTransport(mock_handler)
    client = HttpClient(base_url="https://api.test", transport=transport)
    with pytest.raises(OpenF1ApiError):
        client.get("not-found")

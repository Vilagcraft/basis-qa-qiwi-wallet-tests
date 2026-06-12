from __future__ import annotations

import os

import pytest
from dotenv import load_dotenv
from playwright.sync_api import APIRequestContext, Playwright

from tests.mock_qiwi_server import run_mock_server


@pytest.fixture(scope="session")
def settings():
    load_dotenv()
    return {
        "use_mock": os.getenv("USE_MOCK_SERVER", "true").lower() == "true",
        "base_url": os.getenv("BASE_URL", "https://edge.qiwi.com"),
        "wallet": os.getenv("WALLET", "79999999999"),
        "recipient_wallet": os.getenv("RECIPIENT_WALLET", "+79121112233"),
    }


@pytest.fixture(scope="session")
def mock_server(settings):
    if not settings["use_mock"]:
        yield None
        return
    server, base_url = run_mock_server()
    settings["base_url"] = base_url
    yield server
    server.shutdown()


@pytest.fixture
def api_context(playwright: Playwright, settings, mock_server) -> APIRequestContext:
    context = playwright.request.new_context(
        base_url=settings["base_url"],
        extra_http_headers={"Accept": "application/json", "Content-Type": "application/json"},
    )
    yield context
    context.dispose()

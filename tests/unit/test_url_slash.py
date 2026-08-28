"""Every server path ends in `/` — a slashless POST is rejected before it routes."""

from unittest.mock import MagicMock

import pytest

from indoxhub import Client
from indoxhub.client import _with_trailing_slash


@pytest.mark.unit
@pytest.mark.parametrize(
    "endpoint,expected",
    [
        ("api/v1/chat/completions", "api/v1/chat/completions/"),
        ("api/v1/models/openai/gpt-4o-mini", "api/v1/models/openai/gpt-4o-mini/"),
        ("api/v1/videos/jobs?limit=20&skip=0", "api/v1/videos/jobs/?limit=20&skip=0"),
        ("api/v1/user/usage/", "api/v1/user/usage/"),
    ],
)
def test_with_trailing_slash(endpoint, expected):
    assert _with_trailing_slash(endpoint) == expected


@pytest.mark.unit
def test_request_sends_slashed_url(monkeypatch, api_key):
    monkeypatch.setattr(Client, "_authenticate", lambda self: None)
    client = Client(api_key=api_key, base_url="https://api.example.com")

    response = MagicMock(status_code=200)
    response.json.return_value = {}
    sent = {}

    def fake_request(**kwargs):
        sent.update(kwargs)
        return response

    monkeypatch.setattr(client.session, "request", fake_request)
    client._request("GET", "videos/jobs?limit=20&skip=0")
    client.close()

    assert sent["url"] == "https://api.example.com/api/v1/videos/jobs/?limit=20&skip=0"

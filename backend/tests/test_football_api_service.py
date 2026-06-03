import requests

from app.services import football_api_service


class DummyResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def raise_for_status(self) -> None:
        return None

    def json(self) -> dict:
        return self.payload


def test_fetch_data_returns_json(monkeypatch) -> None:
    captured = {}

    def fake_get(url, headers, params, timeout):
        captured["url"] = url
        captured["headers"] = headers
        captured["params"] = params
        captured["timeout"] = timeout
        return DummyResponse({"ok": True})

    monkeypatch.setattr(football_api_service.requests, "get", fake_get)

    result = football_api_service.fetch_data("/teams/766", params={"season": 2026})

    assert result == {"ok": True}
    assert captured["url"].endswith("/teams/766")
    assert "X-Auth-Token" in captured["headers"]
    assert captured["params"] == {"season": 2026}
    assert captured["timeout"] == 10


def test_fetch_data_returns_none_on_request_error(monkeypatch) -> None:
    def fake_get(*args, **kwargs):
        raise requests.exceptions.RequestException("network error")

    monkeypatch.setattr(football_api_service.requests, "get", fake_get)

    assert football_api_service.fetch_data("/teams/766") is None


def test_get_competition_matches_filters_none_params(monkeypatch) -> None:
    captured = {}

    def fake_fetch_data(endpoint, params):
        captured["endpoint"] = endpoint
        captured["params"] = params
        return {"matches": []}

    monkeypatch.setattr(football_api_service, "fetch_data", fake_fetch_data)

    result = football_api_service.get_competition_matches(
        competition_code="WC",
        date_from="2026-06-11",
        date_to=None,
        matchday=1,
    )

    assert result == {"matches": []}
    assert captured["endpoint"] == "/competitions/WC/matches"
    assert captured["params"] == {
        "dateFrom": "2026-06-11",
        "matchday": 1,
    }


def test_get_team_and_person_detail_delegate_to_fetch_data(monkeypatch) -> None:
    endpoints = []

    def fake_fetch_data(endpoint, params=None):
        endpoints.append(endpoint)
        return {"id": 1}

    monkeypatch.setattr(football_api_service, "fetch_data", fake_fetch_data)

    football_api_service.get_team_detail(766)
    football_api_service.get_person_detail(100)

    assert endpoints == ["/teams/766", "/persons/100"]

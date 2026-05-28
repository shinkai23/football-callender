import requests

from app.core.config import FOOTBALL_API_BASE_URL, FOOTBALL_API_KEY


def fetch_data(endpoint: str, params: dict | None = None) -> dict | None:
    url = f"{FOOTBALL_API_BASE_URL}{endpoint}"
    headers = {
        "X-Auth-Token": FOOTBALL_API_KEY,
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"API呼び出し失敗: {url}: {e}")
        return None


def get_competition_matches(
    competition_code: str,
    date_from: str | None = None,
    date_to: str | None = None,
    stage: str | None = None,
    status: str | None = None,
    matchday: int | None = None,
    group: str | None = None,
    season: int | None = None,
) -> dict | None:
    params = {
        "dateFrom": date_from,
        "dateTo": date_to,
        "stage": stage,
        "status": status,
        "matchday": matchday,
        "group": group,
        "season": season,
    }
    params = {k: v for k, v in params.items() if v is not None}
    return fetch_data(
        endpoint=f"/competitions/{competition_code}/matches",
        params=params,
    )

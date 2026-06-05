from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_read_teams(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/teams")

    assert response.status_code == 200
    assert response.json()[0]["name"] == "Japan"


def test_read_clubs(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/clubs")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 86,
            "name": "Real Madrid CF",
            "country": "Spain",
            "league": "Primera Division",
        }
    ]


def test_read_club_returns_404(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/clubs/999")

    assert response.status_code == 404


def test_read_players(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/players?team_id=766")

    assert response.status_code == 200
    assert response.json()[0]["club"]["name"] == "Real Madrid CF"


def test_read_player_returns_404(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/players/999")

    assert response.status_code == 404


def test_read_matches(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/v1/matches")

    assert response.status_code == 200
    data = response.json()[0]
    assert data["home_team"]["name"] == "Mexico"
    assert data["kickoff_at"] == "2026-06-11T19:00:00"


def test_read_match_returns_404(client: TestClient, seeded_db: Session) -> None:
    response = client.get("/api/v1/matches/999")

    assert response.status_code == 404

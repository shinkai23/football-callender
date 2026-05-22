from fastapi import FastAPI

from app.routers import player_router, team_router


app = FastAPI() #FastAPIインスタンス作成

app.include_router(team_router.router) #インスタンスにteam_routerを追加
app.include_router(player_router.router) #player_routerを追加




"""
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Football Calendar API")

# フロントから呼べるようにする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発中はこれでOK。あとで絞る
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 仮データ
matches = [
    {
        "id": 1,
        "kickoff_at": "2026-06-14T19:00:00+09:00",
        "stage": "Group Stage",
        "venue": "Stadium A",
        "home_team": {
            "id": 1,
            "name": "Japan"
        },
        "away_team": {
            "id": 2,
            "name": "Germany"
        }
    },
    {
        "id": 2,
        "kickoff_at": "2026-06-15T21:00:00+09:00",
        "stage": "Group Stage",
        "venue": "Stadium B",
        "home_team": {
            "id": 3,
            "name": "Brazil"
        },
        "away_team": {
            "id": 4,
            "name": "Argentina"
        }
    }
]


@app.get("/api/v1/matches")
def get_matches():
    return matches


@app.get("/api/v1/matches/{match_id}")
def get_match_detail(match_id: int):
    for match in matches:
        if match["id"] == match_id:
            return match
    return {"message": "match not found"}

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import club_router, match_router, player_router, team_router


app = FastAPI() #FastAPIインスタンス作成

# フロントから呼べるようにする
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開発中はこれでOK。あとで絞る
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(club_router.router)
app.include_router(team_router.router) #インスタンスにteam_routerを追加
app.include_router(player_router.router) #player_routerを追加
app.include_router(match_router.router) #match_routerを追加

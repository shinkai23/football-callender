from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import SYNC_ON_STARTUP
from app.routers import club_router, match_router, player_router, team_router
from app.services.startup_sync_service import run_startup_sync


@asynccontextmanager
async def lifespan(app: FastAPI):
    if SYNC_ON_STARTUP:
        run_startup_sync()

    yield


app = FastAPI(lifespan=lifespan) #FastAPIインスタンス作成

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

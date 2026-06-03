from fastapi import FastAPI

from app.routers import club_router, match_router, player_router, team_router


app = FastAPI() #FastAPIインスタンス作成

app.include_router(club_router.router)
app.include_router(match_router.router)
app.include_router(team_router.router) #インスタンスにteam_routerを追加
app.include_router(player_router.router) #player_routerを追加

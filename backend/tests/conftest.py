from collections.abc import Generator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

import app.models
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.models.club import Club
from app.models.match import Match
from app.models.player import Player
from app.models.team import Team


@pytest.fixture()
def db() -> Generator[Session, None, None]:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db: Session) -> Generator[TestClient, None, None]:
    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def seeded_db(db: Session) -> Session:
    japan = Team(
        id=766,
        name="Japan",
        country="Japan",
        short_name="Japan",
        tla="JPN",
        crest="https://example.com/japan.svg",
    )
    mexico = Team(
        id=769,
        name="Mexico",
        country="Mexico",
        short_name="Mexico",
        tla="MEX",
        crest="https://example.com/mexico.svg",
    )
    club = Club(
        id=86,
        name="Real Madrid CF",
        country="Spain",
        league="Primera Division",
    )
    player = Player(
        id=100,
        name="Sample Player",
        position="Midfielder",
        team=japan,
        club=club,
    )
    match = Match(
        id=537327,
        kickoff_at=datetime(2026, 6, 11, 19, 0),
        stage="GROUP_STAGE",
        venue="Estadio Azteca",
        home_team=mexico,
        away_team=japan,
    )

    db.add_all([japan, mexico, club, player, match])
    db.commit()

    return db

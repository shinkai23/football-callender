# API 仕様書：Football Calendar

## 目的

REST API のエンドポイントとレスポンス形式をまとめる。データ投入は sync スクリプトのみ（POST / PUT なし）。

- 開発時ベース URL: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- `kickoff_at` は sync 時に JST へ変換済み

---

## エンドポイント一覧

| メソッド | path | v1 | 説明 |
|---|---|---|---|
| GET | `/api/teams` | 利用 | チーム一覧 |
| GET | `/api/v1/matches` | 利用 | 試合一覧 |
| GET | `/api/v1/matches/{match_id}` | 利用 | 試合詳細 |
| GET | `/api/players` | 実装のみ | 選手一覧（sync 未実施） |
| GET | `/api/players/{player_id}` | 実装のみ | 選手詳細 |
| GET | `/api/clubs` | 実装のみ | クラブ一覧 |
| GET | `/api/clubs/{club_id}` | 実装のみ | クラブ詳細 |

---

## GET /api/teams

W杯出場チームの一覧。

```json
[
  {
    "id": 769,
    "name": "Mexico",
    "country": "Mexico",
    "short_name": "Mexico",
    "tla": "MEX",
    "crest": "https://crests.football-data.org/769.svg"
  }
]
```

---

## GET /api/v1/matches

同期済み試合の一覧。フロントのカレンダー・リストで使用。

**v2 予定:** `?competition_code=WC` で大会絞り込み、レスポンスに `status`・スコア等を追加。

```json
[
  {
    "id": 500001,
    "kickoff_at": "2026-06-11T19:00:00",
    "stage": "GROUP_STAGE",
    "venue": "Estadio Azteca",
    "home_team": { "id": 769, "name": "Mexico", "...": "..." },
    "away_team": { "id": 770, "name": "South Africa", "...": "..." }
  }
]
```

---

## GET /api/v1/matches/{match_id}

試合 1 件。フィールドは一覧と同じ。

- 404: `{"detail": "Match not found"}`

---

## GET /api/players

| クエリ | 必須 | 説明 |
|---|---|---|
| team_id | 任意 | 指定チームの選手のみ |

- 該当なし: 空配列 `[]`
- 存在しない team_id: 404 `Team not found`

```json
[
  {
    "id": 1,
    "name": "Sample Player",
    "position": "MF",
    "team": { "id": 769, "name": "Mexico", "...": "..." },
    "club": { "id": 1, "name": "Sample Club", "country": "England", "league": "Premier League" }
  }
]
```

---

## GET /api/players/{player_id}

- 404: `{"detail": "Player not found"}`

---

## GET /api/clubs / GET /api/clubs/{club_id}

```json
{ "id": 86, "name": "Real Madrid CF", "country": "Spain", "league": "Primera Division" }
```

- 404: `{"detail": "Club not found"}`

---

## v2 で追加予定（MatchResponse）

| フィールド | 型 | 説明 |
|---|---|---|
| competition_code | str | 大会コード（`WC`, `PL` 等） |
| status | str | `SCHEDULED`, `FINISHED` 等 |
| home_score | int \| null | ホーム得点 |
| away_score | int \| null | アウェイ得点 |

詳細は `docs/モデル・スキーマ設計.md` を参照。

---

## エラー一覧

| 条件 | HTTP | detail |
|---|---|---|
| 試合が存在しない | 404 | Match not found |
| チームが存在しない（players?team_id=） | 404 | Team not found |
| 選手が存在しない | 404 | Player not found |
| クラブが存在しない | 404 | Club not found |

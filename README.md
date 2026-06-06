# football-callender

2026 FIFA ワールドカップの試合日程をカレンダー形式で表示する Web アプリ（**v1**）。

## v1 のスコープ

| 対象 | 内容 |
|------|------|
| ✅ 試合 | 日程・対戦カード・会場・スコアなど |
| ✅ チーム | 試合に登場するチーム一覧・絞り込み |
| ❌ 選手 | football-data.org Free プランでは取得不可のため **v1 対象外** |
| ❌ クラブ | 同上 |

バックエンドに `/api/players`・`/api/clubs` の API は残っていますが、同期・フロント表示は行いません。

## 環境構築

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 環境変数（`backend/.env`）

API キーは **`backend/.env`** に置きます（`app/core/config.py` が `backend/` 直下を読み込みます）。

```bash
cp .env.example .env   # backend ディレクトリ内で実行
# .env を編集
```

`backend/.env` の例:

```env
FOOTBALL_API_KEY=your_api_key_here
FOOTBALL_API_BASE_URL=https://api.football-data.org/v4
```

`FOOTBALL_API_KEY` は [football-data.org](https://www.football-data.org/) で取得してください。

## 起動手順

**順番: データ同期 → バックエンド → フロント**

### 1. 試合データを同期

```bash
cd backend
source .venv/bin/activate
python -m app.scripts.sync_world_cup_teams
```

### 2. バックエンド API を起動

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --reload-dir app
```

起動後:

- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs

### 3. フロントエンドを開く

1. バックエンドが起動していることを確認
2. `frontend/index.html` を Live Server などで開く（`file://` ではなくローカルサーバー推奨）
3. カレンダー・試合一覧・チーム絞り込み・試合詳細モーダルが使える

API のベース URL は `frontend/js/config.js` の `API_BASE_URL` で変更できます。

## テスト

```bash
cd backend
source .venv/bin/activate
pytest
```

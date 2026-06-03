# football-callender
サッカーの試合日程をカレンダー形式で表示する


## 環境構築手順

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

確認:
```bash
python --version
pip list
```

起動
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload --reload-dir app
```

起動後、以下にアクセスする。
```
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
```

## フロントエンド（試合カレンダー）

事前に試合データを同期しておく。

```bash
cd backend
source .venv/bin/activate
python -m app.scripts.sync_world_cup_teams
```

1. バックエンドを起動（上記 `uvicorn`）
2. `frontend/index.html` を Live Server などで開く（`file://` ではなくローカルサーバー推奨）
3. カレンダー・試合一覧・チーム絞り込み・試合詳細モーダルが使える

API のベース URL は `frontend/js/config.js` の `API_BASE_URL` で変更できる。
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
## 選手・クラブ機能のAPI仕様書

作成者: shinkai23

### 目的
本ドキュメントでは、選手・クラブ機能に関係するAPI仕様を整理する。
MVPでは、ライトユーザーが代表選手の所属クラブを理解できることを優先し、選手成績やクラブ詳細情報を扱わない。

### 対象範囲
- チーム一覧取得
- 選手一覧取得
- チーム別選手一覧取得
- 選手詳細取得
- 選手詳細情報に含めるクラブ情報

### API エンドポイント
|メソッド|path|目的|
|---|---|---|
| GET | `/api/teams` | チーム一覧を取得する |
| GET | `/api/players` | 選手一覧を取得する |
| GET | `/api/players?team_id={team_id}` | 指定チームの選手一覧を取得する |
| GET | `/api/players/{player_id}` | 選手詳細を取得する |

### GET /api/teams

#### 概要
W杯出場チームの一覧を取得する。

#### レスポンス例

```json
[
  {
    "id": 1,
    "name": "Japan",
    "country": "Japan"
  },
  {
    "id": 2,
    "name": "England",
    "country": "England"
  }
]
```

### GET /api/players

#### 概要
登録されている選手一覧を取得する。

#### クエリパラメータ
| 名前 | 型 | 必須 | 説明 |
|---|---|---|---|
| team_id | int | 任意 | 指定したチームの選手のみ取得する |

指定したチームが存在し、該当する選手がいない場合は空配列を返す。

#### レスポンス例

```json
[
  {
    "id": 1,
    "name": "Sample Player",
    "position": "MF",
    "team": {
      "id": 1,
      "name": "Japan",
      "country": "Japan"
    },
    "club": {
      "id": 1,
      "name": "Sample Club",
      "country": "England",
      "league": "Premier League"
    }
  }
]
```

### GET /api/players/{player_id}

#### 概要
指定した選手の詳細情報を取得する。

#### パスパラメータ
| 名前 | 型 | 説明 |
|---|---|---|
| player_id | int | 取得したい選手のID |

#### レスポンス例

```json
{
  "id": 1,
  "name": "Sample Player",
  "position": "MF",
  "team": {
    "id": 1,
    "name": "Japan",
    "country": "Japan"
  },
  "club": {
    "id": 1,
    "name": "Sample Club",
    "country": "England",
    "league": "Premier League"
  }
}
```

## エラーレスポンス方針
存在しない選手IDが指定された場合、HTTP 404 を返す

```json
{
    "detail": "Player not found"
}
```

存在しないチームIDが指定された場合、HTTP 404 を返す

```json
{
    "detail": "Team not found"
}
```

### MVPで扱わないAPI
- GET /api/clubs
- GET /api/clubs/{club_id}
- GET /api/players/{player_id}/stats

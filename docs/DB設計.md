## DB設計

作成者: shinkai23

### DBの概要
DBはSQLiteを使用し、Python側のDB操作にはSQLAlchemyを使用する。
試合は大会ごとに DB を分けず、`matches` テーブルに集約し、`competition_code` で区別する（v2）。

### データ関係図

```mermaid
---
title: "ER図"
---
erDiagram
    CLUB ||--o{ PLAYER :"has"
    TEAM ||--o{ PLAYER :"has"
    TEAM ||--o{ MATCH :"home_team"
    TEAM ||--o{ MATCH :"away_team"

    TEAM {
        int id PK
        string name
        string country
        string short_name
        string tla
        string crest
    }

    PLAYER {
        int id PK
        string name
        string position
        int team_id FK
        int club_id FK "null可"
    }

    CLUB {
        int id PK
        string name
        string country
        string league
    }

    MATCH {
        int id PK
        datetime kickoff_at
        string stage
        string venue
        int home_team_id FK
        int away_team_id FK
        string competition_code "v2"
        string status "v2"
        int home_score "v2 null可"
        int away_score "v2 null可"
    }
```

カラムの詳細・sync 方針は `docs/モデル・スキーマ設計.md` を参照する。

### MATCHについて
v1 では W杯の試合日程を中心に扱う。v2 で `competition_code`・`status`・スコアを追加する。
選手・クラブ機能では、Match が参照する Team を起点に Player / Club を表示する想定（v1 未実装）。

### Team ID の扱い
v1 では、football-data.org のチームIDを `teams.id` として利用する。
外部APIを football-data.org に固定することで、別途 `external_id` は持たず、同期処理を単純化する。
将来的に複数APIを扱う場合は、 `external_id` や `source` カラムの追加を検討する。

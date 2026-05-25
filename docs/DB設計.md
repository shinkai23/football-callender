## 選手・クラブ機能のDB設計

作成者: shinkai23

### DBの概要
DBはSQLiteを使用し、Python側のDB操作にはSQLAlchemyを使用する。

### データ関係図

```mermaid
---
title: "選手・クラブ機能のER図"
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
        int club_id FK
    }

    CLUB {
        int id PK
        string name
        string country
        string league
    }

    MATCH {
        int id PK
        int home_team_id FK
        int away_team_id FK
    }
```

### MATCHについて
Match は試合日程機能側の責務であるため、本設計では詳細なカラム定義は扱わない。
選手・クラブ機能では、Match が参照する Team を起点に Player / Club を表示する。

### Team ID の扱い
MVPでは、football-data.org のチームIDを `teams.id` として利用する。
外部APIを football-data.org に固定することで、別途 `external_id` は持たず、同期処理を単純化する。
将来的に複数APIを扱う場合は、 `external_id` や `source` カラムの追加を検討する。
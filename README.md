# asyncpgw
これはdiscord.pyとasyncpgを使用し、POSTTGRESQLにデータを保存する処理があるBOTを作ってる日本人向けに作成したものです。


# 使い方

### asyncpgwをインストール
```
python3 -m pip install asyncpg
```

### psqlに接続

```py
from asyncpgw import start
from asyncio import get_event_loop

async def postgresql_connect():
    pool = await start.connect('postgres://user_name:password@/db_name')

def main():
    loop = get_event_loop()
    loop.run_until_complete(postgresql_connect())

main()
```

###  データ取得
```py
from asyncpgw import general

psql = genetal.Pg()
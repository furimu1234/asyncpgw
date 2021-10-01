from discord.ext import commands as c
from discord import Intents
from asyncpgw import start

import asyncio

#discord.py-version: 1.5.0
intents = Intents.all()

cogs = [

]


class Main(c.Bot):
    """commands.Botを継承したBOTのメインクラス
    parms:
        command_prefix: BOTのPREFIX,
        description: BOTの説明,
        intents: まだ良くわかってない。discord apiの仕様変更で書く必要が出た
    """

    def __init__(self):
        super().__init__(
            command_prefix='!',
            description='asyncpgの説明用BOT',
            intents=intents
        )

        #作成するテーブルリスト
        self.tables = []


    async def psql_connect(self):
        "postgresqlに接続する関数"

        self.pool = await start.connect(url="postgres://user:password@/database_name")


    async def on_ready(self):
        "BOTが起動したときに呼ばれる関数"
        for cog in cogs:
            self.load_extension(cog)

        for table in self.tables:
            #self.tablesに格納されたテーブルを一つずつ取り出して作成する
            await start.create(self.pool, table)


    async def bot_start(self):
        await self.start('BOTTOKEN')


    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.psql_connect())
        loop.run_until_complete(self.bot_start())
        loop.close()


if __name__ == '__main__':
    bot = Main()
    bot.main()
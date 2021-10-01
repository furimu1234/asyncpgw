from discord.ext import commands as c
from asyncpgw import general

#テーブル構造
#server: メッセージが送信されたサーバーのID
#user_id: メッセージを送信したユーザーのID,
#lvl: ユーザーのレベル デフォルト値0
#xp: ユーザーの経験値=発言数 デフォルト値1
lvl_table = """lvl(
    server bigint,
    user_id bigint,
    lvl smallint DEFAULT 0,
    xp smallint DEFAULT 1
)"""

class Lvl(c.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.lvl = general.Pg(bot, 'lvl')


    @c.Cog.listener()
    async def on_message(self, message):
        #メッセージ送信者がBOTだったら何もしない
        if message.author.bot:
            return

        #メッセージが発言されたサーバーでメッセージ送信者のデータがない場合
        #見つかったらデータを変数user_dataに格納する
        if not (user_data := await self.lvl.fetch(server=message.guild.id, user_id=message.author.id)):
            #サーバーIDとユーザーIDを保存。xpとlvlはデフォルト値で保存される。
            return await self.lvl.insert(server=message.guild.id, user_id=message.author.id)

        #user_data[xp]を+1してxpを上書き
        await self.lvl.update(xp= user_data['xp'] + 1, server=message.guild.id, user_id=message.author.id)

        #user_data['xp]は上書きする前のデータなので+1する
        #ユーザーのxpが3だったら
        if user_data['xp'] + 1 % 3 == 0:
            #レベルを+1する
            await self.lvl.update(lvl=user_data['lvl'] + 1, server=message.guild.id, user_id=message.author.id)


def setup(bot):
    #cogとして登録する
    bot.add_cog(Lvl(bot))
    #作成するテーブルを登録する
    bot.add_table(lvl_table)
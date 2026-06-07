import discord
from discord.ext import commands, tasks

GUILD_ID = 1497430589413003274
VOICE_CHANNEL_ID = 1510225108793557033

class Voice24h(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.keep_connected.start()

    def cog_unload(self):
        self.keep_connected.cancel()

    @tasks.loop(seconds=30)
    async def keep_connected(self):
        guild = self.bot.get_guild(1497430589413003274)
        if not guild:
            return

        channel = guild.get_channel(1510225108793557033)
        if not channel:
            return

        vc = guild.voice_client

        if vc is None or not vc.is_connected():
            try:
                await channel.connect(reconnect=True)
                print("Conectado na call.")
            except Exception as e:
                print(f"Erro ao conectar: {e}")

        elif vc.channel.id != 1510225108793557033:
            try:
                await vc.move_to(channel)
                print("Movido para a call correta.")
            except Exception as e:
                print(f"Erro ao mover: {e}")

    @keep_connected.before_loop
    async def before_keep_connected(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Voice24h(bot))
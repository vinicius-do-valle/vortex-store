import discord
from discord.ext import commands, tasks

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=5)
    async def update_stats(self):
        guild = self.bot.get_guild(1497430589413003274)

        if not guild:
            return

        members_channel = guild.get_channel(1512560078740263143)
        boosts_channel = guild.get_channel(1512560316070756422)

        if not members_channel or not boosts_channel:
            return

        member_count = guild.member_count
        boost_count = guild.premium_subscription_count

        try:
            await members_channel.edit(
                name=f"👥┃Membros: {member_count}"
            )

            await boosts_channel.edit(
                name=f"🚀┃Boosts: {boost_count}"
            )

        except discord.Forbidden:
            print("Sem permissão para editar os canais.")
        except Exception as e:
            print(f"Erro ao atualizar estatísticas: {e}")

    @update_stats.before_loop
    async def before_update_stats(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(ServerStats(bot))
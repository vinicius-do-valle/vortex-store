from dotenv import load_dotenv
import os
import asyncio

import discord
from discord.ext import commands

# =========================
# CONFIG DIRETA (SEM ENV)
# =========================
TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX", "!")

# =========================
# INTENTS
# =========================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# =========================
# BOT SETUP
# =========================
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    await self.load_extension(f"cogs.{filename[:-3]}")
                    print(f"[COG] Carregado: {filename}")
                except Exception as e:
                    print(f"[ERRO] Falha ao carregar {filename}: {e}")

        try:
            synced = await self.tree.sync()
            print(f"[SYNC] {len(synced)} comandos slash sincronizados")
        except Exception as e:
            print(f"[ERRO] Sync falhou: {e}")

    async def on_ready(self):
        print(f"\n[ONLINE] Logado como {self.user} (ID: {self.user.id})")
        print("------")

# =========================
# START BOT
# =========================
async def main():
    bot = MyBot()

    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
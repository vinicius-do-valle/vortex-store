import discord
from discord.ext import commands
import re

IMAGEM_URL = "https://media.discordapp.net/attachments/1505653227293769798/1507861034373746808/Vortex_Store_2026_Banner.png?ex=6a1ff6c5&is=6a1ea545&hm=708d78c429cf003e83d4047d4a7d0ede0d83720498f791f1d522cb8aa6588699&=&format=webp&quality=lossless&width=1768&height=707"


def brl(valor: float):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class CalculadoraView(discord.ui.LayoutView):
    def __init__(self, robux: int = None, reais: float = None):
        super().__init__()

        container = discord.ui.Container(
            accent_color=discord.Color.from_rgb(170, 0, 255)
        )

        container.add_item(discord.ui.TextDisplay(
            "# <:VortexStore2026:1502511529545826416> Vortex Store - Calculadora"
        ))

        container.add_item(discord.ui.Separator())

        if robux is not None:
            preco_taxado = robux * 0.036
            preco_sem_taxa = robux * 0.04

            recebido_com_taxa = int(robux * 0.7)
            bruto_sem_taxa = int(robux / 0.7)
            preco_grupo = preco_sem_taxa + (robux * 0.002)

            container.add_item(discord.ui.TextDisplay(
                f"## Simulação para {robux} Robux"
            ))

            container.add_item(discord.ui.Separator())

            container.add_item(discord.ui.TextDisplay(
                f"### Robux Com Taxa:\n"
                f"└ Você coloca: **{robux} Robux**\n"
                f"└ Você recebe: **{recebido_com_taxa} Robux**\n"
                f"└ Preço: **R$ {brl(preco_taxado)}**\n"
                f"└ Tempo: **7 Dias**"
            ))

            container.add_item(discord.ui.Separator())

            container.add_item(discord.ui.TextDisplay(
                f"### Robux Sem Taxa:\n"
                f"└ Você coloca: **{bruto_sem_taxa} Robux**\n"
                f"└ Você recebe: **{robux} Robux**\n"
                f"└ Preço: **R$ {brl(preco_sem_taxa)}**\n"
                f"└ Tempo: **7 Dias**"
            ))

            container.add_item(discord.ui.Separator())

            container.add_item(discord.ui.TextDisplay(
                f"### Grupo (Indisponível):\n"
                f"└ Você coloca: **{robux} Robux**\n"
                f"└ Você recebe: **{robux} Robux**\n"
                f"└ Preço: **R$ {brl(preco_grupo)}**\n"
                f"└ Tempo: **Instantâneo (15 dias no grupo)**"
            ))


        elif reais is not None:
            robux_com_taxa = int(reais / 0.036)
            robux_sem_taxa = int(reais / 0.04)

            recebido_com_taxa = int(robux_com_taxa * 0.7)

            container.add_item(discord.ui.TextDisplay(
                f"## Simulação para R$ {brl(reais)}"
            ))

            container.add_item(discord.ui.Separator())

            container.add_item(discord.ui.TextDisplay(
                f"### Com Taxa:\n"
                f"└ Total comprado: **{robux_com_taxa} Robux**\n"
                f"└ Você recebe: **{recebido_com_taxa} Robux**\n"
                f"└ Tempo: **7 Dias**"
            ))

            container.add_item(discord.ui.Separator())

            container.add_item(discord.ui.TextDisplay(
                f"### Sem Taxa:\n"
                f"└ Você recebe: **{robux_sem_taxa} Robux**\n"
                f"└ Tempo: **7 Dias**"
            ))

        container.add_item(discord.ui.Separator())

        container.add_item(discord.ui.MediaGallery(
            discord.MediaGalleryItem(
                IMAGEM_URL,
                description="VORTEX STORE - Todos os direitos reservados."
            )
        ))

        self.add_item(container)


class CalculadoraCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        if message.channel.id != 1507823015847657673:
            return

        content = message.content.lower().strip()

        match_reais = re.search(r"(r\$|\breais?\b|\brs\b)", content)

        numero = re.search(r"\d+([.,]\d+)?", content)

        if not numero:
            return

        valor = float(numero.group().replace(",", "."))


        if match_reais:
            await message.channel.send(
                view=CalculadoraView(reais=valor)
            )

        else:
            await message.channel.send(
                view=CalculadoraView(robux=int(valor))
            )


async def setup(bot):
    await bot.add_cog(CalculadoraCog(bot))
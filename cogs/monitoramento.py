import discord
from discord.ext import commands

MOD_ROLE_ID = 1497638542317453442


class NotificarView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.usuarios_notificados = set()
        self.add_item(
            discord.ui.Button(
                label="Entrar no Servidor Privado!",
                style=discord.ButtonStyle.link,
                url="https://www.roblox.com/games/77747658251236/Sailor-Piece?privateServerLinkCode=36747001832486053534720217573752",
                emoji="🙌",
                row=0
            )
        )

    @discord.ui.button(
        label="Notificar Moderadores",
        style=discord.ButtonStyle.danger,
        emoji="🔔",
        custom_id="notify_mods",
        row=1
    )
    async def notificar_mods(self, interaction: discord.Interaction, button: discord.ui.Button):
        key = (interaction.user.id, interaction.channel.id)

        if key in self.usuarios_notificados:
            await interaction.response.send_message(
                "Você já notificou os moderadores nesta compra.",
                ephemeral=True
            )
            return

        self.usuarios_notificados.add(key)

        role = interaction.guild.get_role(MOD_ROLE_ID)

        if role:
            await interaction.channel.send(f"{role.mention} 🔔 Um cliente solicitou suporte!")

        await interaction.response.send_message(
            "Moderadores foram notificados com sucesso.",
            ephemeral=True
        )


class MonitorThreads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.canais_permitidos = {
            1505674427831029892,
            1497438803986612325,
            1505674481698345010
        }

        self.threads_processadas = set()

    def criar_embed(self):
        return discord.Embed(
            title="COMPRA REALIZADA COM SUCESSO! ✅",
            description="## Agradecemos pela confiança em nosso serviço\n"
                        "### Para darmos continuidade, envie:\n"
                        "<:status_streaming:1508676088719605941> Seu nome de usuário (nick) do Roblox\n"
                        "<:status_streaming:1508676088719605941> Seu nome de usuário (display) do Roblox)\n"
                        "### Acesso ao servidor\n"
                        "<:status_streaming:1508676088719605941> Acesse o servidor privado pelo link do botão abaixo\n"
                        "<:status_streaming:1508676088719605941> Envie solicitação para A_EoLuccaServerPv e avise.\n"
                        "### Suporte\n"
                        "<:status_streaming:1508676088719605941> Em caso de dúvidas ou necessidade de assistência:\n"
                        "<:status_streaming:1508676088719605941> Moderadores\n"
                        "### Orientação importante\n"
                        "<:status_streaming:1508676088719605941> Mantenha-se atento(a) às notificações de trade dentro do jogo para garantir uma entrega rápida e evitar atrasos.\n"
                        "### Avaliação\n"
                        "<:status_streaming:1508676088719605941> Após a finalização do pedido, deixe sua avaliação em: <#1497645477758500966>",
            color=0xA855F7
        ).set_image(
            url="https://cdn.discordapp.com/attachments/1500967050514923773/1502541415727628308/Vortex_Store_2026_Banner.png"
        ).set_footer(
            text="Vortex Store 2026 - Todos os Direitos Reservados ©"
        )

    async def processar_thread(self, thread: discord.Thread):
        try:
            if thread.parent_id not in self.canais_permitidos:
                return

            if thread.id in self.threads_processadas:
                return

            if "🕔" not in thread.name:
                return

            self.threads_processadas.add(thread.id)

            await thread.send(
                content="# COMPRA REALIZADA COM SUCESSO! ✅",
                embed=self.criar_embed(),
                view=NotificarView()
            )

            print(f"[OK] Thread processada: {thread.name}")

        except Exception as e:
            print("[ERRO THREAD]:", e)

    @commands.command(name="preview")
    async def preview(self, ctx):
        try:
            await ctx.send(
                content="# COMPRA REALIZADA COM SUCESSO! ✅",
                embed=self.criar_embed(),
                view=NotificarView()
            )
        except Exception as e:
            await ctx.send(f"Erro: `{e}`")

    @commands.Cog.listener()
    async def on_thread_create(self, thread: discord.Thread):
        await self.processar_thread(thread)

    @commands.Cog.listener()
    async def on_thread_update(self, before: discord.Thread, after: discord.Thread):
        if before.name != after.name:
            await self.processar_thread(after)


async def setup(bot):
    await bot.add_cog(MonitorThreads(bot))
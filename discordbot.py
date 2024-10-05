import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Synchronisierung der Slash-Commands
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Bot {bot.user.name} ist online und die Slash-Commands sind synchronisiert!')

# Klasse, um die Buttons und den Fortschritt zu verwalten
class ProgressView(View):
    def __init__(self, kunde, gegenstand, menge):
        super().__init__(timeout=None)
        self.kunde = kunde
        self.gegenstand = gegenstand
        self.menge = menge
        self.hergestellt = 0

    # Button, um den Fortschritt zu erhöhen
    @discord.ui.button(label="Fortschritt +1", style=discord.ButtonStyle.green)
    async def fortschritt_button(self, interaction: discord.Interaction, button: Button):
        if self.hergestellt < self.menge:
            self.hergestellt += 1
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)
        else:
            button.disabled = True
            embed = self.create_embed()
            await interaction.response.edit_message(embed=embed, view=self)

    # Funktion, um das Embed zu aktualisieren
    def create_embed(self):
        embed = discord.Embed(title="Herstellungsfortschritt", color=discord.Color.blue())
        embed.add_field(name="Kunde", value=self.kunde, inline=True)
        embed.add_field(name="Gegenstand", value=self.gegenstand, inline=True)
        embed.add_field(name="Menge", value=self.menge, inline=True)
        embed.add_field(name="Hergestellt", value=self.hergestellt, inline=True)
        embed.set_footer(text="Fortschritt wird mit jedem Klick aktualisiert.")
        return embed

# Slash-Command, um den Prozess zu starten
@bot.tree.command(name="start", description="Beginnt den Herstellungsprozess")
async def start(interaction: discord.Interaction, kunde: str, gegenstand: str, menge: int):
    view = ProgressView(kunde, gegenstand, menge)
    embed = view.create_embed()
    await interaction.response.send_message(embed=embed, view=view)

# Starte den Bot
bot.run("DEIN_BOT_TOKEN_HIER")

import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
from discord import AllowedMentions

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= STORAGE =================
ticket_category_id = None
ticket_mod_role_id = None
ticket_count = 0

# ================= COMMANDS =================
@bot.event
async def on_ready():
    print(f"✅ Bot online als {bot.user}")

    # Persistent Views registrieren
    bot.add_view(TicketOpenPersistentView())    # Ticket erstellen Button
    bot.add_view(TicketClosePersistentView())   # Ticket schließen Buttons

    await bot.tree.sync()
    print(f"Slash Commands synchronisiert")

# /create-ticket-in
@bot.tree.command(name="create-ticket-in", description="Setze die Kategorie für Tickets")
async def create_ticket_in(interaction: discord.Interaction, category_id: str):
    global ticket_category_id
    ticket_category_id = int(category_id)
    await interaction.response.send_message(f"✅ Ticket Kategorie gesetzt: <#{ticket_category_id}>", ephemeral=True)

# /set-ticket-mod
@bot.tree.command(name="set-ticket-mod", description="Setze die Ticket-Mod Rolle")
async def set_ticket_mod(interaction: discord.Interaction, role_id: str):
    global ticket_mod_role_id
    ticket_mod_role_id = int(role_id)
    await interaction.response.send_message(f"✅ Ticket Mod Rolle gesetzt: <@&{ticket_mod_role_id}>", ephemeral=True)

# /ticket-starten
@bot.tree.command(name="ticket-starten", description="Erstellt den Ticket Button")
async def ticket_starten(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📨 Support Ticket",
        description="Bitte erstelle ein Ticket um deine Angelegenheiten mit dem Support zu besprechen.",
        color=discord.Color.orange()
    )
    view = TicketOpenPersistentView()

    # Normale Nachricht im Kanal, kein Antwortsymbol
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Ticket-Nachricht wurde gesendet.", ephemeral=True)

# ================= BUTTON VIEWS =================
class TicketOpenPersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📨 Ticket erstellen", style=discord.ButtonStyle.primary, custom_id="ticket_open")
    async def ticket_open_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        global ticket_count, ticket_category_id, ticket_mod_role_id
        if ticket_category_id is None:
            await interaction.response.send_message("❌ Es wurde keine Ticket-Kategorie gesetzt!", ephemeral=True)
            return

        ticket_count += 1
        guild = interaction.guild
        category = guild.get_channel(ticket_category_id)
        if category is None:
            await interaction.response.send_message("❌ Die angegebene Kategorie existiert nicht oder ist ungültig.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
        }

        if ticket_mod_role_id:
            mod_role = guild.get_role(ticket_mod_role_id)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        # Ticket-Kanal erstellen
        channel = await guild.create_text_channel(
            name=f"ticardo-ticket-{ticket_count}",
            category=category,
            overwrites=overwrites
        )

        # Embeds im Ticket
        embed1 = discord.Embed(
            description=f"<@&{ticket_mod_role_id}>" if ticket_mod_role_id else "",
            color=discord.Color.orange()
        )
        embed2 = discord.Embed(
            description=f"<@{interaction.user.id}> Bitte haben Sie ein wenig Geduld, der Support wird sich um Sie kümmern.",
            color=discord.Color.orange()
        )

        view = TicketClosePersistentView()
        allowed = discord.AllowedMentions(users=True, roles=True)
        
        await channel.send(
            embeds=[embed1, embed2],
            view=view,
            allowed_mentions=allowed
        )

        await interaction.response.send_message(f"✅ Ticket erstellt: {channel.mention}", ephemeral=True)

class TicketClosePersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❌ Ticket schließen", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def ticket_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmCloseView(interaction.channel)
        await interaction.response.send_message("Möchten Sie das Ticket wirklich schließen?", view=view, ephemeral=True)

class ConfirmCloseView(discord.ui.View):
    def __init__(self, channel):
        super().__init__(timeout=30)
        self.channel = channel
        self.add_item(ConfirmYesButton(channel))
        self.add_item(ConfirmNoButton())

class ConfirmYesButton(discord.ui.Button):
    def __init__(self, channel):
        super().__init__(label="Ja", style=discord.ButtonStyle.success, custom_id="confirm_yes")
        self.channel = channel

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("✅ Ticket wird geschlossen...", ephemeral=True)
        await asyncio.sleep(2)
        await self.channel.delete()

class ConfirmNoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(label="Nein", style=discord.ButtonStyle.secondary, custom_id="confirm_no")

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("❌ Ticket bleibt geöffnet.", ephemeral=True)

# ================= START BOT =================
bot.run(os.getenv("DISCORD_TOKEN"))

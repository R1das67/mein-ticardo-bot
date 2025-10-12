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

# ================= STORAGE PANEL 1 =================
ticket_category_id = None
ticket_mod_role_id = None
ticket_count = 0

# ================= STORAGE PANEL 2 =================
ticket_category_id_2 = None
ticket_mod_role_id_2 = None
ticket_count_2 = 0
embed_title_2 = "📨 Support Ticket"
embed_text_2 = "Bitte erstelle ein Ticket, um deine Angelegenheiten mit dem Support zu besprechen."

# ================= STORAGE PANEL 3 =================
ticket_category_id_3 = None
ticket_mod_role_id_3 = None
ticket_count_3 = 0
embed_title_3 = "📨 Support Ticket (Panel 3)"
embed_text_3 = "Bitte erstelle ein Ticket, um deine Angelegenheiten mit dem Support zu besprechen."

# ================= ADMIN CHECK =================
def is_admin(interaction: discord.Interaction) -> bool:
    """Prüft, ob der Benutzer Administratorrechte hat."""
    return interaction.user.guild_permissions.administrator

# ================= EMBED FARBE =================
LAVENDER_PURPLE = discord.Color.from_rgb(150, 123, 182)

# ================= COMMANDS =================
@bot.event
async def on_ready():
    print(f"✅ Bot online als {bot.user}")

    # Persistent Views registrieren
    bot.add_view(TicketOpenPersistentView())      # Panel 1: Ticket erstellen Button
    bot.add_view(TicketClosePersistentView())     # Panel 1: Ticket schließen Buttons
    bot.add_view(TicketOpenPersistentView2())     # Panel 2: Ticket erstellen Button
    bot.add_view(TicketClosePersistentView2())    # Panel 2: Ticket schließen Buttons
    bot.add_view(TicketOpenPersistentView3())     # Panel 3: Ticket erstellen Button
    bot.add_view(TicketClosePersistentView3())    # Panel 3: Ticket schließen Buttons

    await bot.tree.sync()
    print(f"Slash Commands synchronisiert")

# ================= PANEL 1 =================
@bot.tree.command(name="create-ticket-in", description="Setze die Kategorie für Tickets")
@app_commands.check(is_admin)
async def create_ticket_in(interaction: discord.Interaction, category_id: str):
    global ticket_category_id
    ticket_category_id = int(category_id)
    await interaction.response.send_message(f"✅ Ticket Kategorie gesetzt: <#{ticket_category_id}>", ephemeral=True)

@bot.tree.command(name="set-ticket-mod", description="Setze die Ticket-Mod Rolle")
@app_commands.check(is_admin)
async def set_ticket_mod(interaction: discord.Interaction, role_id: str):
    global ticket_mod_role_id
    ticket_mod_role_id = int(role_id)
    await interaction.response.send_message(f"✅ Ticket Mod Rolle gesetzt: <@&{ticket_mod_role_id}>", ephemeral=True)

@bot.tree.command(name="ticket-starten", description="Erstellt den Ticket Button")
@app_commands.check(is_admin)
async def ticket_starten(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📨 Support Ticket",
        description="Bitte erstelle ein Ticket, um deine Angelegenheiten mit dem Support zu besprechen.",
        color=LAVENDER_PURPLE
    )
    view = TicketOpenPersistentView()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Ticket-Nachricht wurde gesendet.", ephemeral=True)

# ================= PANEL 2 =================
@bot.tree.command(name="create-ticket-in-2", description="Setze die Kategorie für Tickets (Panel 2)")
@app_commands.check(is_admin)
async def create_ticket_in_2(interaction: discord.Interaction, category_id: str):
    global ticket_category_id_2
    ticket_category_id_2 = int(category_id)
    await interaction.response.send_message(f"✅ Ticket Kategorie (Panel 2) gesetzt: <#{ticket_category_id_2}>", ephemeral=True)

@bot.tree.command(name="set-ticket-mod-2", description="Setze die Ticket-Mod Rolle (Panel 2)")
@app_commands.check(is_admin)
async def set_ticket_mod_2(interaction: discord.Interaction, role_id: str):
    global ticket_mod_role_id_2
    ticket_mod_role_id_2 = int(role_id)
    await interaction.response.send_message(f"✅ Ticket Mod Rolle (Panel 2) gesetzt: <@&{ticket_mod_role_id_2}>", ephemeral=True)

@bot.tree.command(name="set-embed-überschrift-2", description="Setze die Embed Überschrift für Panel 2")
@app_commands.check(is_admin)
async def set_embed_überschrift_2(interaction: discord.Interaction, title: str):
    global embed_title_2
    embed_title_2 = title
    await interaction.response.send_message(f"✅ Embed Überschrift (Panel 2) gesetzt: **{embed_title_2}**", ephemeral=True)

@bot.tree.command(name="set-embed-text-2", description="Setze den Embed Text für Panel 2")
@app_commands.check(is_admin)
async def set_embed_text_2(interaction: discord.Interaction, text: str):
    global embed_text_2
    embed_text_2 = text
    await interaction.response.send_message(f"✅ Embed Text (Panel 2) gesetzt.", ephemeral=True)

@bot.tree.command(name="ticket-starten-2", description="Erstellt den Ticket Button für Panel 2")
@app_commands.check(is_admin)
async def ticket_starten_2(interaction: discord.Interaction):
    embed = discord.Embed(
        title=embed_title_2,
        description=embed_text_2,
        color=LAVENDER_PURPLE
    )
    view = TicketOpenPersistentView2()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Ticket-Nachricht (Panel 2) wurde gesendet.", ephemeral=True)

# ================= PANEL 3 =================
@bot.tree.command(name="create-ticket-in-3", description="Setze die Kategorie für Tickets (Panel 3)")
@app_commands.check(is_admin)
async def create_ticket_in_3(interaction: discord.Interaction, category_id: str):
    global ticket_category_id_3
    ticket_category_id_3 = int(category_id)
    await interaction.response.send_message(f"✅ Ticket Kategorie (Panel 3) gesetzt: <#{ticket_category_id_3}>", ephemeral=True)

@bot.tree.command(name="set-ticket-mod-3", description="Setze die Ticket-Mod Rolle (Panel 3)")
@app_commands.check(is_admin)
async def set_ticket_mod_3(interaction: discord.Interaction, role_id: str):
    global ticket_mod_role_id_3
    ticket_mod_role_id_3 = int(role_id)
    await interaction.response.send_message(f"✅ Ticket Mod Rolle (Panel 3) gesetzt: <@&{ticket_mod_role_id_3}>", ephemeral=True)

@bot.tree.command(name="set-embed-überschrift-3", description="Setze die Embed Überschrift für Panel 3")
@app_commands.check(is_admin)
async def set_embed_überschrift_3(interaction: discord.Interaction, title: str):
    global embed_title_3
    embed_title_3 = title
    await interaction.response.send_message(f"✅ Embed Überschrift (Panel 3) gesetzt: **{embed_title_3}**", ephemeral=True)

@bot.tree.command(name="set-embed-text-3", description="Setze den Embed Text für Panel 3")
@app_commands.check(is_admin)
async def set_embed_text_3(interaction: discord.Interaction, text: str):
    global embed_text_3
    embed_text_3 = text
    await interaction.response.send_message(f"✅ Embed Text (Panel 3) gesetzt.", ephemeral=True)

@bot.tree.command(name="ticket-starten-3", description="Erstellt den Ticket Button für Panel 3")
@app_commands.check(is_admin)
async def ticket_starten_3(interaction: discord.Interaction):
    embed = discord.Embed(
        title=embed_title_3,
        description=embed_text_3,
        color=LAVENDER_PURPLE
    )
    view = TicketOpenPersistentView3()
    await interaction.channel.send(embed=embed, view=view)
    await interaction.response.send_message("✅ Ticket-Nachricht (Panel 3) wurde gesendet.", ephemeral=True)

# ================= ERROR HANDLER =================
@create_ticket_in.error
@set_ticket_mod.error
@ticket_starten.error
@create_ticket_in_2.error
@set_ticket_mod_2.error
@set_embed_überschrift_2.error
@set_embed_text_2.error
@ticket_starten_2.error
@create_ticket_in_3.error
@set_ticket_mod_3.error
@set_embed_überschrift_3.error
@set_embed_text_3.error
@ticket_starten_3.error
async def admin_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Du hast keine Administratorrechte, um diesen Befehl zu nutzen.", ephemeral=True)

# ================= BUTTON VIEWS =================
# PANEL 1
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

        channel = await guild.create_text_channel(
            name=f"ticardo-ticket-{ticket_count}",
            category=category,
            overwrites=overwrites
        )

        ping_text = ""
        if ticket_mod_role_id:
            ping_text += f"<@&{ticket_mod_role_id}> "
        ping_text += f"<@{interaction.user.id}>"

        await channel.send(ping_text)

        embed = discord.Embed(
            description="Bitte haben Sie ein wenig Geduld, der Support wird sich um Sie kümmern.",
            color=LAVENDER_PURPLE
        )
        view = TicketClosePersistentView()
        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"✅ Ticket erstellt: {channel.mention}", ephemeral=True)

class TicketClosePersistentView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❌ Ticket schließen", style=discord.ButtonStyle.danger, custom_id="ticket_close")
    async def ticket_close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmCloseView(interaction.channel)
        await interaction.response.send_message("Möchten Sie das Ticket wirklich schließen?", view=view, ephemeral=True)

# PANEL 2
class TicketOpenPersistentView2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📨 Ticket erstellen (Panel 2)", style=discord.ButtonStyle.primary, custom_id="ticket_open_2")
    async def ticket_open_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        global ticket_count_2, ticket_category_id_2, ticket_mod_role_id_2
        if ticket_category_id_2 is None:
            await interaction.response.send_message("❌ Es wurde keine Ticket-Kategorie (Panel 2) gesetzt!", ephemeral=True)
            return

        ticket_count_2 += 1
        guild = interaction.guild
        category = guild.get_channel(ticket_category_id_2)
        if category is None:
            await interaction.response.send_message("❌ Die angegebene Kategorie (Panel 2) existiert nicht oder ist ungültig.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
        }

        if ticket_mod_role_id_2:
            mod_role = guild.get_role(ticket_mod_role_id_2)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticardo2-ticket-{ticket_count_2}",
            category=category,
            overwrites=overwrites
        )

        ping_text = ""
        if ticket_mod_role_id_2:
            ping_text += f"<@&{ticket_mod_role_id_2}> "
        ping_text += f"<@{interaction.user.id}>"

        await channel.send(ping_text)

        embed = discord.Embed(
            description="Bitte haben Sie ein wenig Geduld, der Support wird sich um Sie kümmern.",
            color=LAVENDER_PURPLE
        )
        view = TicketClosePersistentView2()
        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"✅ Ticket erstellt (Panel 2): {channel.mention}", ephemeral=True)

class TicketClosePersistentView2(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❌ Ticket schließen (Panel 2)", style=discord.ButtonStyle.danger, custom_id="ticket_close_2")
    async def ticket_close_button_2(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmCloseView(interaction.channel)
        await interaction.response.send_message("Möchten Sie das Ticket wirklich schließen?", view=view, ephemeral=True)

# PANEL 3
class TicketOpenPersistentView3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📨 Ticket erstellen (Panel 3)", style=discord.ButtonStyle.primary, custom_id="ticket_open_3")
    async def ticket_open_button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        global ticket_count_3, ticket_category_id_3, ticket_mod_role_id_3
        if ticket_category_id_3 is None:
            await interaction.response.send_message("❌ Es wurde keine Ticket-Kategorie (Panel 3) gesetzt!", ephemeral=True)
            return

        ticket_count_3 += 1
        guild = interaction.guild
        category = guild.get_channel(ticket_category_id_3)
        if category is None:
            await interaction.response.send_message("❌ Die angegebene Kategorie (Panel 3) existiert nicht oder ist ungültig.", ephemeral=True)
            return

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
        }

        if ticket_mod_role_id_3:
            mod_role = guild.get_role(ticket_mod_role_id_3)
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticardo3-ticket-{ticket_count_3}",
            category=category,
            overwrites=overwrites
        )

        ping_text = ""
        if ticket_mod_role_id_3:
            ping_text += f"<@&{ticket_mod_role_id_3}> "
        ping_text += f"<@{interaction.user.id}>"

        await channel.send(ping_text)

        embed = discord.Embed(
            description="Bitte haben Sie ein wenig Geduld, der Support wird sich um Sie kümmern.",
            color=LAVENDER_PURPLE
        )
        view = TicketClosePersistentView3()
        await channel.send(embed=embed, view=view)

        await interaction.response.send_message(f"✅ Ticket erstellt (Panel 3): {channel.mention}", ephemeral=True)

class TicketClosePersistentView3(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="❌ Ticket schließen (Panel 3)", style=discord.ButtonStyle.danger, custom_id="ticket_close_3")
    async def ticket_close_button_3(self, interaction: discord.Interaction, button: discord.ui.Button):
        view = ConfirmCloseView(interaction.channel)
        await interaction.response.send_message("Möchten Sie das Ticket wirklich schließen?", view=view, ephemeral=True)

# ================= CONFIRM CLOSE (beide Panels) =================
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

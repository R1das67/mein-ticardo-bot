import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

# ================= BOT SETUP =================
intents = discord.Intents.default()
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ================= PANEL STORAGE =================
panels = {
    "panel1": {"name": None, "embed_text": None, "mod_role_id": None, "category_id": None, "ticket_count": 0},
    "panel2": {"name": None, "embed_text": None, "mod_role_id": None, "category_id": None, "ticket_count": 0},
    "panel3": {"name": None, "embed_text": None, "mod_role_id": None, "category_id": None, "ticket_count": 0},
}

# ================= ADMIN CHECK =================
def is_admin(interaction: discord.Interaction) -> bool:
    """Prüft, ob der Benutzer Administratorrechte hat."""
    return interaction.user.guild_permissions.administrator

# ================= COMMANDS =================
GUILD_ID = 1424384847169847338

@bot.event
async def on_ready():
    print(f"✅ Bot online als {bot.user}")

    # Persistent Views registrieren
    bot.add_view(TicketOpenPersistentView())    # Ticket erstellen Button
    bot.add_view(TicketClosePersistentView())   # Ticket schließen Buttons
    bot.add_view(WizardFinishView())            # Wizard Finish Buttons
    bot.add_view(GoBackButtonView())            # Go Back Button

    # Nur für deinen Server synchronisieren (Guild Commands)
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print(f"Slash Commands für Server {GUILD_ID} synchronisiert")

# ================= PANEL EDIT COMMANDS =================
@bot.tree.command(name="edit-panel-1", description="Wizard für Panel 1")
@app_commands.check(is_admin)
async def edit_panel_1(interaction: discord.Interaction):
    await start_panel_wizard(interaction, "panel1")

@bot.tree.command(name="edit-panel-2", description="Wizard für Panel 2")
@app_commands.check(is_admin)
async def edit_panel_2(interaction: discord.Interaction):
    await start_panel_wizard(interaction, "panel2")

@bot.tree.command(name="edit-panel-3", description="Wizard für Panel 3")
@app_commands.check(is_admin)
async def edit_panel_3(interaction: discord.Interaction):
    await start_panel_wizard(interaction, "panel3")

# ================= WIZARD FUNCTION =================
async def start_panel_wizard(interaction: discord.Interaction, panel_key: str):
    await interaction.response.send_message(f"**Wizard für {panel_key} gestartet!**\nBitte gib den **Panel-Namen** ein:", ephemeral=True)

    def check_name(m):
        return m.author == interaction.user and m.channel == interaction.channel

    try:
        name_msg = await bot.wait_for("message", check=check_name, timeout=120)
        panels[panel_key]["name"] = name_msg.content

        await interaction.followup.send("✅ Name gesetzt! Bitte gib nun den **Embed Text** ein (Paragraph):", ephemeral=True)
        text_msg = await bot.wait_for("message", check=check_name, timeout=300)
        panels[panel_key]["embed_text"] = text_msg.content

        await interaction.followup.send("✅ Embed Text gesetzt! Bitte gib nun die **Mod-Rolle ID** ein:", ephemeral=True)
        role_msg = await bot.wait_for("message", check=check_name, timeout=120)
        panels[panel_key]["mod_role_id"] = int(role_msg.content)

        await interaction.followup.send("✅ Mod-Rolle gesetzt! Bitte gib nun die **Kategorie ID** ein:", ephemeral=True)
        cat_msg = await bot.wait_for("message", check=check_name, timeout=120)
        panels[panel_key]["category_id"] = int(cat_msg.content)

        # Wizard Finish Buttons
        await interaction.followup.send(
            "Alles gesetzt! Panel fertigstellen?", 
            view=WizardFinishView(panel_key=panel_key), ephemeral=True
        )
    except asyncio.TimeoutError:
        await interaction.followup.send("⏰ Wizard abgebrochen, Zeit überschritten.", ephemeral=True)

# ================= WIZARD FINISH BUTTONS =================
class WizardFinishView(discord.ui.View):
    def __init__(self, panel_key=None):
        super().__init__(timeout=None)
        self.panel_key = panel_key

    @discord.ui.button(label="✅ Yes", style=discord.ButtonStyle.success, custom_id="wizard_yes")
    async def yes_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        panel = panels[self.panel_key]
        embed = discord.Embed(
            title=f"📨 {panel['name']}",
            description=panel["embed_text"],
            color=discord.Color(0x3EB489)
        )
        view = TicketOpenPersistentView(panel_name=self.panel_key)
        channel = interaction.channel
        await channel.send(embed=embed, view=view)
        await interaction.response.send_message(f"✅ Panel {self.panel_key} erstellt!", ephemeral=True)

    @discord.ui.button(label="❌ No", style=discord.ButtonStyle.danger, custom_id="wizard_no")
    async def no_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Wizard wird neu gestartet...", view=GoBackButtonView(panel_key=self.panel_key), ephemeral=True)

# ================= GO BACK BUTTON =================
class GoBackButtonView(discord.ui.View):
    def __init__(self, panel_key=None):
        super().__init__(timeout=None)
        self.panel_key = panel_key

    @discord.ui.button(label="🔄 Go Back", style=discord.ButtonStyle.secondary, custom_id="wizard_goback")
    async def go_back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await start_panel_wizard(interaction, self.panel_key)

# ================= BUTTON VIEWS =================
class TicketOpenPersistentView(discord.ui.View):
    def __init__(self, panel_name=None):
        super().__init__(timeout=None)
        self.panel_name = panel_name

    @discord.ui.button(label="📨 Ticket erstellen", style=discord.ButtonStyle.primary, custom_id="ticket_open")
    async def ticket_open_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        panel = panels.get(self.panel_name)
        if not panel or not panel["category_id"]:
            await interaction.response.send_message("❌ Panel ist nicht richtig eingerichtet!", ephemeral=True)
            return

        panel["ticket_count"] += 1
        guild = interaction.guild
        category = guild.get_channel(panel["category_id"])

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True),
        }

        if panel["mod_role_id"]:
            mod_role = guild.get_role(panel["mod_role_id"])
            if mod_role:
                overwrites[mod_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"{self.panel_name}-ticket-{panel['ticket_count']}",
            category=category,
            overwrites=overwrites
        )

        ping_text = f"<@{interaction.user.id}>"
        if panel["mod_role_id"]:
            ping_text = f"<@&{panel['mod_role_id']}> {ping_text}"
        await channel.send(ping_text)

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

# ================= ERROR HANDLER =================
@edit_panel_1.error
@edit_panel_2.error
@edit_panel_3.error
async def admin_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Du hast keine Administratorrechte, um diesen Befehl zu nutzen.", ephemeral=True)

# ================= START BOT =================
bot.run(os.getenv("DISCORD_TOKEN"))

import json
import os
import random
from pathlib import Path

import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = 1484219249852678266
DATA_FILE = Path("roles.json")

DEFAULT_ROLE_IDS = [
    1490387734341226748,
    1490387671233855568,
    1490387602757517352,
    1490387456590086376,
    1490387372368593066,
    1490387161885704372,
    1490386863394001128,
    1492127181956976681,
    1490387904751472771,
    1484256136449232958,
    1484255958619259062,
    1484255350268891287,
    1484254931643928686,
    1484254573622460587,
    1484254475790188584,
    1484254403413151925,
    1484252401136308317,
    1491882522714308728,
    1484254659270021230,
    1490386195916656822,
    1484251974395367517,
    1484256010326507802,
    1492552564473069660,
    1490732262755536989,
    1493213834884681828,
    1489757293913575454,
    1484255091224739920,
    1484256312786157588,
    1489337541533634631,
    1491365093269831801,
    1490385552308961411,
    1484254977198129192,
    1492552444142682153,
    1484255657950449784,
    1489335874364768437,
    1484251276605784157,
    1484254736457924669,
    1484255623620067469,
    1484255763311493201,
    1484254476058497144,
    1489696171726209075,
    1484251126739108003,
    1489695724043243641,
    1485334113589395646,
    1490732382473682954,
    1491014916436394085,
    1484254036344574014,
    1489336461294571541,
    1490731777072042148,
    1485333759627624610,
    1489695986795155507,
]

if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN is not set. Add it to your .env file.")


def ensure_data_file() -> None:
    if not DATA_FILE.exists():
        save_role_ids(DEFAULT_ROLE_IDS)


def load_role_ids() -> list[int]:
    ensure_data_file()
    try:
        data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        role_ids = data.get("role_ids", [])
        return [int(role_id) for role_id in role_ids]
    except (json.JSONDecodeError, ValueError, TypeError):
        save_role_ids(DEFAULT_ROLE_IDS)
        return DEFAULT_ROLE_IDS.copy()


def save_role_ids(role_ids: list[int]) -> None:
    unique_role_ids = list(dict.fromkeys(int(role_id) for role_id in role_ids))
    DATA_FILE.write_text(
        json.dumps({"role_ids": unique_role_ids}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)
GUILD_OBJECT = discord.Object(id=GUILD_ID)


async def is_allowed_guild(interaction: discord.Interaction) -> bool:
    return interaction.guild is not None and interaction.guild.id == GUILD_ID


async def admin_only(interaction: discord.Interaction) -> bool:
    if not await is_allowed_guild(interaction):
        await interaction.response.send_message(
            "Эта команда работает только на нужном сервере.", ephemeral=True
        )
        return False

    user = interaction.user
    if isinstance(user, discord.Member) and user.guild_permissions.manage_roles:
        return True

    await interaction.response.send_message(
        "У тебя нет права **Manage Roles** для этой команды.", ephemeral=True
    )
    return False


@bot.event
async def on_ready():
    ensure_data_file()
    try:
        synced = await bot.tree.sync(guild=GUILD_OBJECT)
        print(f"Synced {len(synced)} slash command(s) for guild {GUILD_ID}.")
    except Exception as error:
        print(f"Command sync error: {error}")

    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready.")


@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id != GUILD_ID:
        return

    role_ids = load_role_ids()
    roles = [member.guild.get_role(role_id) for role_id in role_ids]
    roles = [role for role in roles if role is not None]

    if not roles:
        print("No valid roles found in the auto-role list.")
        return

    selected_role = random.choice(roles)

    try:
        await member.add_roles(selected_role, reason="Random auto-role on join")
        print(f"Gave role '{selected_role.name}' ({selected_role.id}) to {member}")
    except discord.Forbidden:
        print("Missing permissions to assign roles.")
    except discord.HTTPException as error:
        print(f"Discord API error: {error}")


@bot.tree.command(name="addrole", description="Добавить роль в список авто-выдачи", guild=GUILD_OBJECT)
@app_commands.describe(role_id="ID роли, которую нужно добавить")
async def addrole(interaction: discord.Interaction, role_id: str):
    if not await admin_only(interaction):
        return

    try:
        parsed_role_id = int(role_id.strip())
    except ValueError:
        await interaction.response.send_message(
            "Укажи корректный ID роли числом.", ephemeral=True
        )
        return

    role = interaction.guild.get_role(parsed_role_id)
    if role is None:
        await interaction.response.send_message(
            "Я не вижу роль с таким ID на этом сервере.", ephemeral=True
        )
        return

    role_ids = load_role_ids()
    if parsed_role_id in role_ids:
        await interaction.response.send_message(
            f"Роль **{role.name}** уже есть в списке авто-выдачи.", ephemeral=True
        )
        return

    role_ids.append(parsed_role_id)
    save_role_ids(role_ids)
    await interaction.response.send_message(
        f"Готово =3\nРоль **{role.name}** (`{role.id}`) добавлена в список авто-выдачи.",
        ephemeral=True,
    )


@bot.tree.command(name="delrole", description="Удалить роль из списка авто-выдачи", guild=GUILD_OBJECT)
@app_commands.describe(role_id="ID роли, которую нужно удалить")
async def delrole(interaction: discord.Interaction, role_id: str):
    if not await admin_only(interaction):
        return

    try:
        parsed_role_id = int(role_id.strip())
    except ValueError:
        await interaction.response.send_message(
            "Укажи корректный ID роли числом.", ephemeral=True
        )
        return

    role_ids = load_role_ids()
    if parsed_role_id not in role_ids:
        await interaction.response.send_message(
            "Этой роли нет в списке авто-выдачи.", ephemeral=True
        )
        return

    role_ids.remove(parsed_role_id)
    save_role_ids(role_ids)

    role = interaction.guild.get_role(parsed_role_id)
    role_name = role.name if role else "Удаленная/невидимая роль"
    await interaction.response.send_message(
        f"Готово =3\nРоль **{role_name}** (`{parsed_role_id}`) удалена из списка авто-выдачи.",
        ephemeral=True,
    )


@bot.tree.command(name="checkid", description="Показать ID выбранной роли", guild=GUILD_OBJECT)
@app_commands.describe(role="Роль, ID которой нужно посмотреть")
async def checkid(interaction: discord.Interaction, role: discord.Role):
    if not await is_allowed_guild(interaction):
        await interaction.response.send_message(
            "Эта команда работает только на нужном сервере.", ephemeral=True
        )
        return

    await interaction.response.send_message(
        f"Роль **{role.name}** имеет ID: `{role.id}`", ephemeral=True
    )


@bot.tree.command(name="allrole", description="Показать все роли из списка авто-выдачи", guild=GUILD_OBJECT)
async def allrole(interaction: discord.Interaction):
    if not await is_allowed_guild(interaction):
        await interaction.response.send_message(
            "Эта команда работает только на нужном сервере.", ephemeral=True
        )
        return

    role_ids = load_role_ids()
    if not role_ids:
        await interaction.response.send_message(
            "```Вот список ролей и их айди, которые выдаются при входе на дс сервер:\nПока список пуст.```"
        )
        return

    lines = ["Вот список ролей и их айди, которые выдаются при входе на дс сервер:"]
    for index, role_id in enumerate(role_ids, start=1):
        role = interaction.guild.get_role(role_id)
        role_name = role.name if role else "Не найдена на сервере"
        lines.append(f"{index}) {role_name} - {role_id}")

    await interaction.response.send_message(f"```\n" + "\n".join(lines) + "\n```")


bot.run(TOKEN)

import discord
from discord import app_commands
from bot.list import weapon_choices
from func.auctions import weapons

weapon_check = {v.lower(): k for k, v in weapon_choices.items()}

async def add_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=display_name, value=api_name) for display_name, api_name in weapon_choices.items() if current.lower() in display_name.lower()][:25]

async def remove_autocomplete(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=weapon_check[weapon], value=weapon) for weapon in weapons if current.lower() in weapon.lower()][:25]

import discord
from discord.ext import commands
from func.auctions import *
from discord import app_commands
from bot.list import weapon_choices
from bot.autocomplete import *

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.tree.command(name="add", description="Add a weapon to the list")
@app_commands.describe(weapon="The weapon you want to add")
@app_commands.autocomplete(weapon=add_autocomplete)
async def add(interaction: discord.Interaction, weapon: str):
    weapon_format = weapon_check[weapon.lower()]
    if weapon.lower() not in weapon_check:
        await interaction.response.send_message(f"{weapon_format} doesn't exist stupid!", ephemeral=True)
    elif weapon.lower() in weapons:
        await interaction.response.send_message(f"{weapon_format} is already in the list!", ephemeral=True)
    else:
        weapons.append(weapon.lower())
        await interaction.response.send_message(f"Added {weapon_format} to the list!")
        await check_auctions(interaction.channel)

@bot.tree.command(name="remove", description="Remove a weapon from the list")
@app_commands.describe(weapon="The weapon you want to remove")
@app_commands.autocomplete(weapon=remove_autocomplete)
async def remove(interaction: discord.Interaction, weapon: str):
    weapon_format = weapon_check[weapon.lower()]
    if weapon.lower() not in weapon_check:
        await interaction.response.send_message(f"{weapon_format} doesn't exist stupid!", ephemeral=True)
    elif weapon.lower() not in weapons:
        await interaction.response.send_message(f"{weapon_format} is already not in the list!", ephemeral=True)
    else:
        weapons.remove(weapon.lower())
        await interaction.response.send_message(f"Removed {weapon_format} from the list!")

@bot.tree.command(name="disp", description="Display weapons in the list")
async def disp(interaction: discord.Interaction):
    if len(weapons) == 0:
        await interaction.response.send_message("You have no weapons in the list!")
        return
    weapon_list = "\n".join(f"- {weapon}" for weapon in weapons)
    await interaction.response.send_message(f"**You have:**\n{weapon_list}")

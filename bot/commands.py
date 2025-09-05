import discord
from discord.ext import commands
from func.auctions import *
from discord import app_commands
from bot.weapon_list import weapon_choices
from bot.autocomplete import *
from include.data import cache_dir
from func.is_attribute_pos import is_attribute_pos

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
        await interaction.response.send_message(f"Added {weapon_format} to the list!", ephemeral=True)
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
        save_cache(f"{cache_dir}/weapons.json", weapons)
        await interaction.response.send_message(f"Removed {weapon_format} from the list!", ephemeral=True)

@bot.tree.command(name="disp", description="Display weapons in the list")
async def disp(interaction: discord.Interaction):
    if len(weapons) == 0:
        await interaction.response.send_message("You have no weapons in the list!", ephemeral=True)
        return
    weapon_list = "\n".join(f"- {weapon}" for weapon in weapons)
    await interaction.response.send_message(f"**You have:**\n{weapon_list}", ephemeral=True)

@bot.tree.command(name="search", description="Search for riven in the list")
@app_commands.describe(user_weapon="The riven you want")
@app_commands.autocomplete(
              user_weapon=search_weapon_autocomplete,
              atr1=positive_attribute_autocomplete,
              atr2=positive_attribute_autocomplete,
              atr3=positive_attribute_autocomplete,
              neg=negative_attribute_autocomplete)
async def search(interaction: discord.Interaction, user_weapon: str, atr1: str, atr2: str, atr3: str, neg: str):
    valid = {}
    for item in previous_ids:
        weapon = item["weapon"]
        id_ = item["id"]
        attributes = item["attributes"]
        price = item["price"]
        invalid_atr = False
        if user_weapon != "None" and user_weapon != weapon:
            continue
        for atr in (atr1, atr2, atr3):
            if atr == "None":
                continue
            if (atr not in attributes) or (not is_attribute_pos(atr, attributes)):
                invalid_atr = True
                break
        if (neg not in attributes) or (is_attribute_pos(neg, attributes)):
            continue
        if (invalid_atr):
            continue
        valid[item[id]] = item
        valid.update(item)
        await interaction.response.send_message(f"{item}", ephemeral=True)

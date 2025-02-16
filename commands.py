from auctions import *
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def add(ctx, weapon: str):
    if weapon.lower() in weapons:
        await ctx.send(f"{weapon} is already in the list!")
    else:
        weapons.append(weapon.lower())
        await ctx.send(f"Added {weapon} to the list!")
        await check_auctions(ctx.channel)

@bot.command()
async def remove(ctx, weapon: str):
    if weapon.lower() not in weapons:
        await ctx.send(f"{weapon} is already not in the list!")
    else:
        weapons.remove(weapon.lower())
        await ctx.send(f"Removed {weapon} from the list!")

@bot.command()
async def disp(ctx):
    if len(weapons) == 0:
        await ctx.send("You have no weapons in the list!")
        return
    await ctx.send("**You have :**")
    for weapon in weapons:
        await ctx.send(f"- {weapon}")

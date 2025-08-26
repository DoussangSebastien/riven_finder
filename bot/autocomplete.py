from bisect import bisect_left
from discord import app_commands
from bot.list import weapon_choices
from func.auctions import weapons

sorted_weapon_choices = sorted((display_name.lower(), display_name, api_name) for display_name, api_name in weapon_choices.items())
sorted_weapons = sorted((weapon.lower(), weapon) for weapon in weapons)
weapon_check = {api_name.lower(): display_name for display_name, api_name in weapon_choices.items()}

def dichotomic_autocomplete(sorted_list, prefix, limit=25):
    prefix_lower = prefix.lower()
    start_index = bisect_left(sorted_list, (prefix_lower,))
    results = []
    while start_index < len(sorted_list) and sorted_list[start_index][0].startswith(prefix_lower) and len(results) < limit:
        results.append(sorted_list[start_index])
        start_index += 1
    return results

async def add_autocomplete(interaction, current: str):
    matches = dichotomic_autocomplete(sorted_weapon_choices, current)
    return [app_commands.Choice(name=display_name, value=api_name) for _, display_name, api_name in matches]

async def remove_autocomplete(interaction, current: str):
    matches = dichotomic_autocomplete(sorted_weapons, current)
    return [app_commands.Choice(name=weapon_check[api_name_lower], value=weapon_name) for api_name_lower, weapon_name in matches]

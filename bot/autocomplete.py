from bisect import bisect_left
from discord import app_commands
from bot.weapon_list import weapon_choices
from bot.riven_attribute_list import riven_positive_attributes, riven_negative_attributes
from func.auctions import weapons

sorted_weapon_choices = sorted((display_name.lower(), display_name, api_name) for display_name, api_name in weapon_choices.items())
sorted_positive_riven_attributes = sorted((display_name.lower(), display_name, api_name) for display_name, api_name in riven_positive_attributes.items())
sorted_negative_riven_attributes = sorted((display_name.lower(), display_name, api_name) for display_name, api_name in riven_negative_attributes.items())
weapon_check = {api_name.lower(): display_name for display_name, api_name in weapon_choices.items()}

def dichotomic_autocomplete(sorted_list, prefix, limit=25):
    prefix_lower = prefix.lower()
    start_index = bisect_left(sorted_list, (prefix_lower,))
    results = []
    while start_index < len(sorted_list) and sorted_list[start_index][0].startswith(prefix_lower) and len(results) < limit:
        results.append(sorted_list[start_index])
        start_index += 1
    return results

def make_weapon_autocomplete(choice_list):
    async def inner(interaction, current: str):
        matches = dichotomic_autocomplete(choice_list, current)
        return [app_commands.Choice(name=display_name, value=api_name) for _, display_name, api_name in matches]
    return inner

add_autocomplete = make_weapon_autocomplete(sorted_weapon_choices)

async def remove_autocomplete(interaction, current: str):
    sorted_weapons = sorted((weapon.lower(), weapon) for weapon in weapons)
    matches = dichotomic_autocomplete(sorted_weapons, current)
    return [app_commands.Choice(name=weapon_check[display_name], value=api_name) for display_name, api_name in matches]

# search autocomplete
search_weapon_autocomplete = make_weapon_autocomplete(sorted_weapon_choices)
positive_attribute_autocomplete = make_weapon_autocomplete(sorted_positive_riven_attributes)
negative_attribute_autocomplete = make_weapon_autocomplete(sorted_negative_riven_attributes)

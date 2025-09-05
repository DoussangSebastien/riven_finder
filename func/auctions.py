import requests
from bot.weapon_list import weapon_choices
from func.cache import load_cache, save_cache
from include.data import baseurl, url, cache_dir

previous_ids = load_cache(f"{cache_dir}/previous_ids.json", [])
weapons = load_cache(f"{cache_dir}/weapons.json", [])

async def send_discord_message(channel, auction_url, price_info, attributes, name):
    content = (
        f"**New {name} Riven Mod Found!**\n"
        f"{price_info}\n"
        f"**Attributes:**\n{attributes}\n"
        f"[View Auction]({auction_url})"
    )
    await channel.send(content)

def get_attributes(item):
    return "\n".join(f"{stat['url_name']}: {stat['value']}" for stat in item['item']['attributes'])

def get_price(item):
    if item['buyout_price'] != item['starting_price']:
        return f"Starting price: {item['starting_price']} -> Auction, Buyout price: {item['buyout_price'] or '∞'}"
    return f"Price: {item['starting_price']}"

def normalize_weapon_name(name):
    suffixes = ["_prime", "_prisma"]
    for s in suffixes:
        if name.endswith(s):
            return name[: -len(s)]
    return name

def is_same_weapon(current_weapon, list_weapon):
    return normalize_weapon_name(current_weapon) == normalize_weapon_name(list_weapon)

async def check_auctions(channel):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch auctions. Status code: {response.status_code}")
        return
    try:
        items = response.json()
    except:
        print("Failed to parse JSON.")
        return
    for item in items.get('payload', {}).get('auctions', []):
        if 'item' not in item or 'weapon_url_name' not in item['item']:
            continue
        auction_id = item['id']
        if any(is_same_weapon(item['item']['weapon_url_name'], w) for w in weapons) and all(auction_id != previous['id'] for previous in previous_ids):
            print("new")
            price_info = get_price(item)
            auction_url = f"https://warframe.market/auction/{auction_id}"
            name = item['item']['weapon_url_name']
            attributes = get_attributes(item)
            previous_ids.append({"weapon": name, "id" : auction_id, "attributes": attributes, "price": price_info})
            save_cache(f"{cache_dir}/previous_ids.json", previous_ids)
            save_cache(f"{cache_dir}/weapons.json", weapons)
            await send_discord_message(channel, auction_url, price_info, attributes, [key for key, val in weapon_choices.items() if name == val][0])

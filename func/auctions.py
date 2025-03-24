import requests
from bot.list import weapon_choices

url = "https://api.warframe.market/v1/auctions"
previous_ids = []
weapons = []

async def send_discord_message(channel, auction_url, price_info, attributes, name):
    content = (
        f"**New {name} Riven Mod Found!**\n"
        f"{price_info}\n"
        f"**Attributes:**\n{attributes}\n"
        f"[View Auction]({auction_url})"
    )
    await channel.send(content)

def get_attributes(item):
    return "\n".join(f"- {stat['url_name']}: {stat['value']}" for stat in item['item']['attributes'])

def get_price(item):
    if item['buyout_price'] != item['starting_price']:
        return f"Starting price: {item['starting_price']} -> Auction, Buyout price: {item['buyout_price'] or '∞'}"
    return f"Price: {item['starting_price']}"

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
        if item['item']['weapon_url_name'] in weapons:
            auction_id = item['id']
            if auction_id not in previous_ids:
                previous_ids.append(auction_id)
                price_info = get_price(item)
                auction_url = f"https://warframe.market/auction/{auction_id}"
                name = item['item']['weapon_url_name']
                attributes = get_attributes(item)
                await send_discord_message(channel, auction_url, price_info, attributes, [key for key, val in weapon_choices.items() if name == val][0])

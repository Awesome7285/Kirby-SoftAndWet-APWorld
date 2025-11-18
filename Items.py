from BaseClasses import Item

BASE_ID = 1

class KSAWItem(Item):
    game: str = "Kirby ~ Soft & Wet"

# ITEM_IDS = {
#     "coins": 1,
#     "baits": 100,
#     "bobbers": 200,
#     "sprays": 300
# }

coin_items = [
    "1 Coin",
    "2 Coins",
    "3 Coins",
    "4 Coins",
    "100 Coins",
]

bait_items = {
    "Glod Berry": "0rarity_IsUnlocked",
    "Rare Cookie": "1rarity_IsUnlocked",
    "Big Bun": "2rarity_IsUnlocked",
    "Starfruit": "3rarity_IsUnlocked"
}

all_items = coin_items + list(bait_items.keys())

item_table = {name: id for id, name in enumerate(all_items, BASE_ID)}
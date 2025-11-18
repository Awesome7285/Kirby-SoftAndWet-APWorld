from BaseClasses import Item

BASE_ID = 1

class KSAWItem(Item):
    game: str = "Kirby ~ Soft & Wet"

all_items = [
    "1 Coin",
    "2 Coins",
    "3 Coins",
    "4 Coins",
    "100 Coins",
    "Glod Berry"
]

item_table = {name: id for id, name in enumerate(all_items, BASE_ID)}
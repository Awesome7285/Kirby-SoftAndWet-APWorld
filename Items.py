from BaseClasses import Item

BASE_ID = 1

class KSAWItem(Item):
    game: str = "Kirby ~ Soft & Wet"

all_items = [
    "fish",
]

item_table = {name: id for id, name in enumerate(all_items, BASE_ID)}
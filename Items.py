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
    "Starfruit": "3rarity_IsUnlocked",
    "Sundae": "extraDay_IsUnlocked",
    "Love Egg": "extraAfternoon_IsUnlocked",
    "Mooncake": "extraNight_IsUnlocked",
    "Ruffpaste": "easyInputs_IsUnlocked",
    "Rush Pepper": "fasterFinds_IsUnlocked",
    "Lifelight": "moreShinies_IsUnlocked",
    "Stone Chum": "moreGrams_IsUnlocked",
    "Baggie Candy": "moreCoins_IsUnlocked"
}

bobber_items = {
    "Red Bobber": "red_IsUnlocked",
    "Blue Bobber": "blue_IsUnlocked",
    "Green Bobber": "green_IsUnlocked",
    "Yellow Bobber": "yellow_IsUnlocked",
    "Purple Bobber": "purple_IsUnlocked",
    "Red Peg Bobber": "redPeg_IsUnlocked",
    "Anchor Bobber": "anchor_IsUnlocked",
    "Wormiller Bobber": "worm_IsUnlocked",
    "Dynamite Bobber": "dynamite_IsUnlocked",
    "Rocket Slime Bobber": "rocketSlime_IsUnlocked",
    "Dedede Bobber": "dedede_IsUnlocked",
    "Hayuto Bobber": "hayuto_IsUnlocked",
    "Deirdre Bobber": "deirdre_IsUnlocked",
    "Super Mushroom Bobber": "superMushroom_IsUnlocked",
    "Zebra Bloon Bobber": "zebraBloon_IsUnlocked",
    "Astro Bot Bobber": "astroBot_IsUnlocked",
    "Bad Piggie Bobber": "badPiggie_IsUnlocked",
    "Dream Peace Bobber": "dreamPeace_IsUnlocked",
    "Bejewel Bobber": "bejewel_IsUnlocked",
    "Master Ball Bobber": "masterBall_IsUnlocked",
    "Blinky Bobber": "blinky_IsUnlocked",
    "Inky Bobber": "inky_IsUnlocked",
    "Pinky Bobber": "pinky_IsUnlocked",
    "Clyde Bobber": "clyde_IsUnlocked",
    "Pac-Man Bobber": "pacman_IsUnlocked",
    "Smash Bobber": "smash_IsUnlocked",
    "Rainbow Drop Bobber": "rainbowDrop_IsUnlocked",
    "Kirby Bobber": "kirby_IsUnlocked",
    "Star Bobber": "star_IsUnlocked",
    "Dark Matter Bobber": "darkMatter_IsUnlocked",
    "Starry Bobber": "starry_IsUnlocked",
    "Nightmare Orb Bobber": "nightmareOrb_IsUnlocked",
    "Master Crown Bobber": "masterCrown_IsUnlocked",
    "Legend Bobber": "legend_IsUnlocked",
    "Rogue Matter Bobber": "rogueMatter_IsUnlocked",
    "Daremo Bobber": "daremo_IsUnlocked",
    "Rosemarie Bobber": "rosemarie_IsUnlocked"
}

hat_items = {
    "No Hat": "kirby_None_IsUnlocked",
    "Shades": "kirby_Shades_IsUnlocked",
    "Straw Hat": "kirby_StrawHat_IsUnlocked",
    "Goggles": "kirby_Goggles_IsUnlocked"
}

spray_items = {
    "Pink Spray Can": "kirby_Pink_IsUnlocked",
    "Yellow Spray Can": "kirby_Yellow_IsUnlocked",
    "Red Spray Can": "kirby_Red_IsUnlocked",
    "Green Spray Can": "kirby_Green_IsUnlocked",
    "Snow Spray Can": "kirby_Snow_IsUnlocked",
    "Carbon Spray Can": "kirby_Carbon_IsUnlocked",
    "Ocean Spray Can": "kirby_Ocean_IsUnlocked",
    "Sapphire Spray Can": "kirby_Sapphire_IsUnlocked",
    "Grape Spray Can": "kirby_Grape_IsUnlocked",
    "Emerald Spray Can": "kirby_Emerald_IsUnlocked",
    "Orange Spray Can": "kirby_Orange_IsUnlocked",
    "Chocolate Spray Can": "kirby_Chocolate_IsUnlocked",
    "Cherry Spray Can": "kirby_Cherry_IsUnlocked",
    "Chalk Spray Can": "kirby_Chalk_IsUnlocked",
    "Mirror Spray Can": "kirby_Mirror_IsUnlocked",
    "Shadow Spray Can": "kirby_Shadow_IsUnlocked",
    "Ivory Spray Can": "kirby_Ivory_IsUnlocked",
    "Citrus Spray Can": "kirby_Citrus_IsUnlocked",
    "Lavender Spray Can": "kirby_Lavender_IsUnlocked",
    "Smash Yellow Spray Can": "kirby_SmashYellow_IsUnlocked",
    "Smash Red Spray Can": "kirby_SmashRed_IsUnlocked",
    "Smash Green Spray Can": "kirby_SmashGreen_IsUnlocked",
    "Smash White Spray Can": "kirby_SmashWhite_IsUnlocked",
    "Superstar Pink Spray Can": "kirby_SuperstarPink_IsUnlocked",
    "Superstar Ice Spray Can": "kirby_SuperstarIce_IsUnlocked",
    "Pastel Pink Spray Can": "kirby_PastelPink_IsUnlocked",
    "Advance Ice Spray Can": "kirby_AdvanceIce_IsUnlocked",
    "Advance Stone Spray Can": "kirby_AdvanceStone_IsUnlocked",
    "Superstar Meta Spray Can": "kirby_SuperstarMeta_IsUnlocked",
    "Advance Meta Spray Can": "kirby_AdvanceMeta_IsUnlocked",
    "Waddle Spray Can": "kirby_Waddle_IsUnlocked",
    "Lololo Spray Can": "kirby_Lololo_IsUnlocked",
    "Lalala Spray Can": "kirby_Lalala_IsUnlocked",
    "Original Spray Can": "kirby_Original_IsUnlocked",
    "Elfilin Peacock Spray Can": "kirby_ElfilinPeacock_IsUnlocked",
    "Baggie Spray Can": "kirby_Baggie_IsUnlocked",
    "Galacta Spray Can": "kirby_Galacta_IsUnlocked",
    "Unpleasant Spray Can": "kirby_Unpleasant_IsUnlocked",
    "Mango Spray Can": "kirby_Mango_IsUnlocked",
    "Air Ride L Blue Spray Can": "kirby_AirRideLBlue_IsUnlocked",
    "Laser Bird Spray Can": "kirby_LaserBird_IsUnlocked",
    "Strawberry Spray Can": "kirby_Strawberry_IsUnlocked",
    "Seashell Spray Can": "kirby_Seashell_IsUnlocked",
    "Lando Spray Can": "kirby_Lando_IsUnlocked",
    "Golden Hour Spray Can": "kirby_GoldenHour_IsUnlocked",
    "Dawn Spray Can": "kirby_Dawn_IsUnlocked",
    "Super Star Spray Can": "kirby_SuperStar_IsUnlocked",
    "Lornus Spray Can": "kirby_Lornus_IsUnlocked",
    "ChuChu Spray Can": "kirby_ChuChu_IsUnlocked"
}

area_items = {
    "Grass Beach Unlock": "grassBeach_IsUnlocked",
    "Cream Crevasse Unlock": "creamCrevasse_IsUnlocked",
    "Hallow Reen Unlock": "hallowReen_IsUnlocked"
}

all_items = coin_items + list(bait_items.keys()) + list(bobber_items.keys()) + list(hat_items.keys()) + list(spray_items.keys())

item_table = {name: id for id, name in enumerate(all_items, BASE_ID)}
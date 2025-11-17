from BaseClasses import MultiWorld, Region, Entrance
from .Locations import KSAWLocation, all_locations, location_table

def create_regions(world: MultiWorld, player: int):
    # Menu region
    menu = Region("Menu", player, world)
    world.regions.append(menu)

    # Store all entrances from Menu for use in Rules.py
    world.menu_entrances = {}

    for loc in all_locations:
        menu.locations.append(KSAWLocation(player, loc, location_table[loc], menu))

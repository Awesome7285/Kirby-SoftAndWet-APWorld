import typing
from worlds.generic.Rules import add_rule, set_rule
from .Locations import all_locations

def set_rules(world, options, player):
    pass


def debug_reachability(world, player):
    print("\n--- Reachability Debug ---")
    state = world.get_all_state(False)  # initial state, no items collected
    for entrance_name, entrance in world.menu_entrances.items():
        print(f"{entrance_name}: {'reachable' if entrance.can_reach(state) else 'locked'}")
    print("--------------------------\n")

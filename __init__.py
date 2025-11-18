from typing import List, Dict, Tuple
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from .Items import KSAWItem, all_items, coin_items, bait_items, bobber_items, hat_items, spray_items, item_table as item_name_to_id
from .Locations import KSAWLocation, all_locations, location_table as location_name_to_id
from .Regions import create_regions
from .Rules import set_rules
from .Options import KSAWOptions

from BaseClasses import Item, ItemClassification, Tutorial
from ..AutoWorld import World, WebWorld


def run_client():
    from .Client import main as client_main
    launch_subprocess(client_main)

components.append(Component("KSAW Client", func=run_client, component_type=Type.CLIENT))


class KSAWWorld(World):
    """ 
    Kirby ~ Soft & Wet game description.
    """

    game: str = "Kirby ~ Soft & Wet"
    topology_present = False

    item_name_to_id = item_name_to_id
    location_name_to_id = location_name_to_id

    required_client_version: Tuple[int, int, int] = (0, 0, 1)

    options_dataclass = KSAWOptions

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

    def create_item(self, name: str) -> Item:
        classification = ItemClassification.progression
        # elif name in stage_items:
        #     classification = ItemClassification.progression_skip_balancing
        return KSAWItem(name, classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        item_pool: List[KSAWItem] = []
        #print([i.name for i in self.multiworld.get_locations()])

        # Choose random starting items
        starting_items = []
        starting_items.append(self.random.choice(list(bait_items.keys())))
        starting_items.append(self.random.choice(list(bobber_items.keys())))
        starting_items.append(self.random.choice(list(hat_items.keys())))
        starting_items.append(self.random.choice(list(spray_items.keys())))
        for item in starting_items:
            self.multiworld.push_precollected(self.create_item(item))
        

        # Add all items
        item_pool += [self.create_item(item) for item in all_items if item not in starting_items]

        # # Fill any empty locations with filler items.
        while len(item_pool) < len(self.multiworld.get_unfilled_locations(player=self.player)):
            item_pool.append(self.create_item(self.random.choice(coin_items))) # self.get_filler_item_name()

        self.multiworld.itempool += item_pool

    def generate_basic(self):
        pass

    def generate_early(self):
        pass

    def fill_slot_data(self):
        slot_data: Dict[str, object] = {
            "goal": self.options.goal.value,
            #"DeathLink": self.options.death_link.value == True,
        }

        return slot_data
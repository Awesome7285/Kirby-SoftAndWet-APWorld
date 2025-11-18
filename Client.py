import os, sys, Utils, asyncio, configparser, multiprocessing, time
import colorama
from collections import Counter

from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser, logger, ClientStatus, ClientCommandProcessor
from .Items import item_table, BASE_ID, coin_items, bait_items
from .Locations import location_table, all_locations, fish_count_locations, fish_locations


### INI OPENING STUFF

MAX_RETRIES = 3
RETRY_DELAY = 0.05  # 50 ms between tries

def clear_ini(ini_dir):
    for attempt in range(MAX_RETRIES):
        try:
            if os.path.exists(ini_dir):
                os.remove(ini_dir)
            config = configparser.ConfigParser()
            config.optionxform = str
            config.add_section("Items")
            config.add_section("Locations")
            with open(ini_dir, "w") as f:
                config.write(f)
            break
        except PermissionError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"WARNING: Failed to remove {ini_dir} after {MAX_RETRIES} attempts.")


def read_ini_section(ini_dir, section):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini_dir)
    return dict(config[section]) if section in config else {}

def write_ini(ini_dir, section, key, value):
    config = configparser.ConfigParser()
    config.optionxform = str
    if os.path.exists(ini_dir):
        config.read(ini_dir)
    if section not in config:
        config[section] = {}
    config[section][key] = str(value).lower()

    tmp = ini_dir + ".tmp"
    with open(tmp, "w") as f:
        config.write(f)
    
    for attempt in range(MAX_RETRIES):
        try:
            os.replace(tmp, ini_dir)
            break
        except PermissionError:
            if attempt < MAX_RETRIES - 1:
                time.sleep(RETRY_DELAY)
            else:
                print(f"WARNING: Failed to replace {ini_dir} after {MAX_RETRIES} attempts.")
        
### ARCHIPELAGO STUFF

class TomTom4ClientCommand(ClientCommandProcessor):
    def _cmd_refresh(self):
        """Manually refresh all items from the server and rewrite them to the INI."""
        items = sorted(self.ctx.items_received)
        clear_ini(self.ctx.ini_dir)
        asyncio.create_task(self.ctx.update_received_items(items))
        asyncio.create_task(self.ctx.update_checked_locations(self.ctx.previous_location_checked))
        logger.info("Refreshed Items and Locations.")
        return None

class KSAWContext(CommonContext):
    game = "Kirby ~ Soft & Wet"
    items_handling = 0b111
    locations_dir = os.path.join(os.path.expanduser("~"), "AppData/Local/Kirby ~ Soft & Wet/data1.ini")
    items_dir = os.path.join(os.path.expanduser("~"), "AppData/Local/Kirby ~ Soft & Wet/apdata1.ini")

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.checked_locations = set()
        self.is_connected = False
        self.options = None
        self.command_processor = TomTom4ClientCommand

        self.all_location_ids = None
        self.location_name_to_ap_id = None
        self.location_ap_id_to_name = None
        self.item_name_to_ap_id = None
        self.item_ap_id_to_name = None
        self.previous_location_checked = None
        self.location_mapping = None

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"KSAW Client"
        return ui

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        """
        Manage the package received from the server
        """
        
        if cmd == "Connected":
            self.previous_location_checked = args['checked_locations']
            self.all_location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.options = args["slot_data"] # Yaml Options
            self.is_connected = True

            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Kirby ~ Soft & Wet"]}]))
            #clear_ini(self.ini_dir)
            asyncio.create_task(self.update_checked_locations(self.previous_location_checked))

        if cmd == "ReceivedItems":
            print("got:", args["items"])
            asyncio.create_task(self.update_received_items(args["items"]))

        elif cmd == "DataPackage":
            if not self.all_location_ids:
                # Connected package not received yet, wait for datapackage request after connected package
                return
            self.location_name_to_ap_id = args["data"]["games"]["Kirby ~ Soft & Wet"]["location_name_to_id"]
            self.location_name_to_ap_id = {
                name: loc_id for name, loc_id in
                self.location_name_to_ap_id.items() if loc_id in self.all_location_ids
            }
            self.location_ap_id_to_name = {v: k for k, v in self.location_name_to_ap_id.items()}
            self.item_name_to_ap_id = args["data"]["games"]["Kirby ~ Soft & Wet"]["item_name_to_id"]
            self.item_ap_id_to_name = {v: k for k, v in self.item_name_to_ap_id.items()}

            print(self.location_name_to_ap_id)
            print(self.location_ap_id_to_name)
            print(self.item_name_to_ap_id)
            print(self.item_ap_id_to_name)

            asyncio.create_task(self.check_for_locations_loop())

    async def update_checked_locations(self, locations):
        """Updates the locations already completed from initial datapackage"""
        print(locations)
        for loc in locations:
            write_ini(self.locations_dir, "Locations", str(loc-BASE_ID+1), 1)
    
    async def update_received_items(self, items):
        """Updates items received to the INI"""
        

        new_items = [self.item_ap_id_to_name[item.item] for item in items]
        received = dict(Counter(new_items))
        for item_name, amount in received.items():
            if item_name in bait_items.keys():
                write_ini(self.items_dir, "baitStatus", bait_items[item_name], 1)
            # elif item_name in coin_items:
            #     write_ini(self.items_dir, "gameplay", "coins", item_name)
    
    async def check_for_locations_loop(self):
        """Permanent Loop that checks the users ini file for new locations to send"""
        while True:
            await asyncio.sleep(1.3)
            new_locations = []
            game_data = read_ini_section(self.locations_dir, "gameplay")
            try:
                fish = int(float(game_data["caughtTotalFishCount"].replace('"', "")))
            except KeyError:
                fish = 0
            for f in range(1, fish+1):
                new_locations.append(self.location_name_to_ap_id[f"Obtained Fish #{f}"])

            
            # written_locations = read_ini_section(self.ini_dir, "Locations")
            # for loc_id, obtained in written_locations.items():
            #     actual_id = int(loc_id)+BASE_ID-1
            #     if obtained == "1" and actual_id not in self.previous_location_checked:
            #         new_locations.append(actual_id)

            if new_locations:
                self.previous_location_checked = self.previous_location_checked + new_locations
                await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])


def main():
    Utils.init_logging("KSAW Client")
    parser = get_base_parser()
    args = sys.argv[1:]
    if "KSAW Client" in args:
        args.remove("KSAW Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()
        ctx = KSAWContext(args.connect, args.password)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()
        await ctx.exit_event.wait()
        ctx.server_address = None
        await ctx.shutdown()

    colorama.init()
    asyncio.run(_main())
    colorama.deinit()

    

if __name__ == "__main__":
    main()
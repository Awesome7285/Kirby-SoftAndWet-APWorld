import os, sys, Utils, asyncio, configparser, multiprocessing, time
import colorama
from collections import Counter

from CommonClient import CommonContext, server_loop, gui_enabled, get_base_parser, logger, ClientStatus, ClientCommandProcessor
from .Items import item_table, BASE_ID, coin_items, bait_items, bobber_items, hat_items, spray_items
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
    config[section][key] = str(value)

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
        self.received_datapackage = False
        self.first_items = []
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
        # print(cmd, args)

        if cmd == "Connected":
            self.previous_location_checked = args['checked_locations']
            self.all_location_ids = set(args["missing_locations"] + args["checked_locations"])
            self.options = args["slot_data"] # Yaml Options
            self.is_connected = True

            asyncio.create_task(self.send_msgs([{"cmd": "GetDataPackage", "games": ["Kirby ~ Soft & Wet"]}]))
            #clear_ini(self.ini_dir)

        if cmd == "ReceivedItems":
            if self.received_datapackage == False:
                self.first_items.extend(args["items"])
                print(self.first_items)
            else:
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

            # print(self.location_name_to_ap_id)
            # print(self.location_ap_id_to_name)
            # print(self.item_name_to_ap_id)
            # print(self.item_ap_id_to_name)

            self.received_datapackage = True

            asyncio.create_task(self.refresh_loaded_ini(self.previous_location_checked, self.first_items))

            asyncio.create_task(self.update_received_items(self.first_items))

            asyncio.create_task(self.check_for_locations_loop())

    async def refresh_loaded_ini(self, locations, items):
        """Updates the locations already completed from initial datapackage"""
        clear_ini(self.items_dir)
        write_ini(self.items_dir, "NotifStatus", "welcome_Obtained", 1)
        write_ini(self.items_dir, "baitStatus", "none_IsUnlocked", 1)
        write_ini(self.items_dir, "gameplay", "timePlayed_Seconds", 1)

        completed = 0
        for item in items:
            if self.item_ap_id_to_name[item.item] in bait_items.keys():
                starting_bait = self.item_ap_id_to_name[item.item]
                completed += 1
            if self.item_ap_id_to_name[item.item] in bobber_items.keys():
                starting_bobber = self.item_ap_id_to_name[item.item]
                completed += 1
            if self.item_ap_id_to_name[item.item] in hat_items.keys():
                starting_hat = self.item_ap_id_to_name[item.item]
                completed += 1
            if self.item_ap_id_to_name[item.item] in spray_items.keys():
                starting_spray = self.item_ap_id_to_name[item.item]
                completed += 1
            if completed == 4:
                break


        write_ini(self.items_dir, "playerStatus", "equippedBait_0", bait_items[starting_bait].replace("_IsUnlocked", ""))
        write_ini(self.items_dir, "playerStatus", "equippedBobberShuffle_0", 0)
        write_ini(self.items_dir, "playerStatus", "equippedBobber_0", bobber_items[starting_bobber].replace("_IsUnlocked", ""))
        write_ini(self.items_dir, "playerStatus", "playerEquippedSprayPaint_0_kirby", spray_items[starting_spray].replace("_IsUnlocked", ""))
        write_ini(self.items_dir, "playerStatus", "playerEquippedHat_0_kirby", hat_items[starting_hat].replace("_IsUnlocked", ""))

    
    async def update_received_items(self, items):
        """Updates items received to the INI"""
        
        print(items)
        print(items[0].item)
        new_items = [self.item_ap_id_to_name[item.item] for item in items]
        for item_name in new_items:
            if item_name in bait_items.keys():
                write_ini(self.items_dir, "baitStatus", bait_items[item_name], 1)
            if item_name in bobber_items.keys():
                write_ini(self.items_dir, "bobberStatus", bobber_items[item_name], 1)
            if item_name in hat_items.keys():
                write_ini(self.items_dir, "hatStatus", hat_items[item_name], 1)
            if item_name in spray_items.keys():
                write_ini(self.items_dir, "sprayPaintStatus", spray_items[item_name], 1)
            # elif item_name in coin_items:
            #     write_ini(self.items_dir, "gameplay", "coins", item_name)

        self.first_items = []
    
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
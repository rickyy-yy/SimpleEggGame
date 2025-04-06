from datetime import *
import random
import os
import json
import time

COMMON_SPIRITS = ["Wood", "Grass", "Fire"]
UNCOMMON_SPIRITS = ["Water", "Wind", "Clover"]
RARE_SPIRITS = ["Gold", "Metal", "Oil"]
LEGENDARY_SPIRITS = ["Human", "Monster", "Evil"]
EGG_STORAGE_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\egg_storage.json"
SPIRIT_STORAGE_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\spirit_storage.json"

money = 100


class Egg:
    def __init__(self, rarity, egg_id=None, hatch_datetime=None):
        self.rarity: str
        self.hatch_time: timedelta
        self.hatch_datetime: datetime
        self.remaining_hatch_time: timedelta
        self.egg_id: int
        self.worth: int
        self.hatched: bool

        self.hatched = False

        self.rarity = rarity

        if self.rarity == "Common":
            self.hatch_time = timedelta(hours=1)
            self.worth = 5
        elif self.rarity == "Uncommon":
            self.hatch_time = timedelta(days=1, hours=12)
            self.worth = 10
        elif self.rarity == "Rare":
            self.hatch_time = timedelta(hours=12)
            self.worth = 30
        elif self.rarity == "Legendary":
            self.hatch_time = timedelta(hours=3)
            self.worth = 80

        if hatch_datetime is None:
            self.hatch_datetime = datetime.now() + self.hatch_time
        else:
            self.hatch_datetime = hatch_datetime

        if egg_id is None:
            self.egg_id = get_next_egg_id()
        else:
            self.egg_id = egg_id

        self.remaining_hatch_time = self.hatch_datetime - datetime.now()

        self.info_summary = {
            "Rarity": self.rarity,
            "Hatch Datetime": self.hatch_datetime.strftime('%d-%m-%Y, %H:%M:%S'),
            "Worth": self.worth,
            "Hatched": self.hatched
        }

        print("Ding! An egg has arrived in your inventory.")

        self.check_hatch_status()

    def get_rarity(self):
        return self.rarity

    def get_remaining_hatch_time(self):
        self.remaining_hatch_time = self.hatch_datetime - datetime.now()
        return self.remaining_hatch_time

    def update_remaining_hatch_time(self):
        self.remaining_hatch_time = self.hatch_datetime - datetime.now()

    def get_hatch_time(self):
        return self.hatch_time

    def get_hatch_datetime(self):
        return self.hatch_datetime

    def store_egg(self):
        temp_dict = {self.egg_id: self.info_summary}
        json_summary = json.dumps(temp_dict)
        if os.stat(EGG_STORAGE_PATH).st_size == 0:
            with open(EGG_STORAGE_PATH, "w") as file:
                file.write(json_summary)
        else:
            with open(EGG_STORAGE_PATH, "r") as file:
                eggs = file.readlines()
                loaded_summary = json.loads(eggs[0])
                loaded_summary[self.egg_id] = self.info_summary
            json_summary = json.dumps(loaded_summary)
            with open(EGG_STORAGE_PATH, "w") as file:
                file.write(json_summary)

    def check_hatch_status(self):
        if self.hatch_datetime - datetime.now() < timedelta(seconds=0):
            self.update_egg_hatched_status()
            hatched_spirit = Spirit(self.rarity, self.worth)
            hatched_spirit.store_spirit()

    def update_egg_hatched_status(self):
        self.info_summary["Hatched"] = True
        print("updated!")
        with open(EGG_STORAGE_PATH, "r") as file:
            lines = file.readlines()[0]
            loaded_eggs = json.loads(lines)
            loaded_eggs[self.egg_id] = self.info_summary
            loaded_eggs.pop(self.egg_id)
        with open(EGG_STORAGE_PATH, "w") as file:
            file.write(json.dumps(loaded_eggs))


class Spirit:
    def __init__(self, rarity, worth):
        self.rarity = rarity
        self.variant_name: str
        self.gold_production: float
        self.spirit_id: int
        self.worth: float

        if rarity == "Common":
            self.gold_production = 1
            self.variant_name = random.choice(COMMON_SPIRITS)
        elif rarity == "Uncommon":
            self.gold_production = 2.5
            self.variant_name = random.choice(UNCOMMON_SPIRITS)
        elif rarity == "Rare":
            self.gold_production = 10
            self.variant_name = random.choice(RARE_SPIRITS)
        else:
            self.gold_production = 50
            self.variant_name = random.choice(LEGENDARY_SPIRITS)

        self.spirit_id = get_next_spirit_id()
        self.worth = worth * 1.5

        self.info_summary = {
            "Rarity": self.rarity,
            "Variant Name": self.variant_name,
            "Worth": self.worth,
            "Gold per Minute": self.gold_production
        }

        print(f"Crack! A new {self.rarity} spirit emerges from an egg. Check it out in your spirit pouch!")

    def get_rarity(self):
        return self.rarity

    def get_variant_name(self):
        return self.variant_name

    def get_gold_per_minute(self):
        return self.gold_production

    def get_worth(self):
        return self.worth

    def store_spirit(self):
        temp_dict = {self.spirit_id: self.info_summary}
        json_summary = json.dumps(temp_dict)
        if os.stat(SPIRIT_STORAGE_PATH).st_size == 0:
            with open(SPIRIT_STORAGE_PATH, "w") as file:
                file.write(json_summary)
        else:
            with open(SPIRIT_STORAGE_PATH, "r") as file:
                spirits = file.readlines()
                loaded_summary = json.loads(spirits[0])
                loaded_summary[self.spirit_id] = self.info_summary
            json_summary = json.dumps(loaded_summary)
            with open(SPIRIT_STORAGE_PATH, "w") as file:
                file.write(json_summary)

    def delete_stored_spirit(self):
        with open(SPIRIT_STORAGE_PATH, "r") as file:
            spirits = file.readlines()
        loaded_summary = json.loads(spirits[0])
        del loaded_summary[self.spirit_id]
        with open(SPIRIT_STORAGE_PATH, "w") as file:
            json_summary = json.dumps(loaded_summary)
            file.write(json_summary)


def check_egg_storage():
    if not os.path.exists(EGG_STORAGE_PATH):
        with open(EGG_STORAGE_PATH, "x") as file:
            pass
        initiate_beginner()
    else:
        check_for_hatched_eggs()
        menu()


def check_spirit_storage():
    if not os.path.exists(SPIRIT_STORAGE_PATH):
        with open(SPIRIT_STORAGE_PATH, "x") as file:
            pass


def get_next_egg_id():
    with open(EGG_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        if lines:
            lines = json.loads(lines[0])
            next_egg_id = int(list(lines.keys())[len(lines.keys()) - 1]) + 1
            return next_egg_id
        else:
            return 0


def get_next_spirit_id():
    with open(SPIRIT_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        if lines:
            lines = json.loads(lines[0])
            next_spirit_id = int(list(lines.keys())[len(lines.keys()) - 1]) + 1
            return next_spirit_id
        else:
            return 0


def retrieve_egg_info(egg_id):
    with open(EGG_STORAGE_PATH, "r") as file:
        eggs = file.readlines()
        target_egg = eggs[egg_id - 1]
        loaded_info_summary = json.loads(target_egg)
        return loaded_info_summary


def egg_shop():
    print("===========Egg Shop===========")
    print("")
    print("{}|{}                 {}".format("1", "Common Egg", "$10"))
    print("{}|{}               {}".format("2", "Uncommon Egg", "$25"))
    print("{}|{}                   {}".format("3", "Rare Egg", "$50"))
    print("{}|{}             {}".format("4", "Legendary Egg", "$100"))
    print("")
    while True:
        try:
            choice = int(input(
                "Enter the item number of the egg you wish to purchase (1/2/3/4), enter anything else to return to menu: "))
            match choice:
                case 1:
                    if can_afford(10):
                        purchase_common_egg()
                        break
                    else:
                        not_enough_money()
                case 2:
                    if can_afford(25):
                        purchase_uncommon_egg()
                        break
                    else:
                        not_enough_money()
                case 3:
                    if can_afford(50):
                        purchase_rare_egg()
                        break
                    else:
                        not_enough_money()
                case 4:
                    if can_afford(100):
                        purchase_legendary_egg()
                        break
                    else:
                        not_enough_money()
                case _:
                    break
        except ValueError:
            pass


def can_afford(price):
    global money
    if money < price:
        return False
    return True


def purchase_common_egg():
    global money
    money -= 10
    give_common_egg()


def purchase_uncommon_egg():
    global money
    money -= 25
    give_uncommon_egg()


def purchase_rare_egg():
    global money
    money -= 50
    give_rare_egg()


def purchase_legendary_egg():
    global money
    money -= 100
    give_legendary_egg()


def initiate_beginner():
    print("Welcome to my Egg Game!")
    time.sleep(0.5)
    print("The game is simple. Hatch eggs and earn money!")
    time.sleep(0.5)
    print("To start you off, here's a Common Egg.")
    time.sleep(0.5)
    give_common_egg()
    time.sleep(0.5)
    print("Taking you to the main menu now...")
    menu()


def give_common_egg():
    common_egg = Egg("Common")
    common_egg.store_egg()


def give_uncommon_egg():
    uncommon_egg = Egg("Uncommon")
    uncommon_egg.store_egg()


def give_rare_egg():
    rare_egg = Egg("Rare")
    rare_egg.store_egg()


def give_legendary_egg():
    legendary_egg = Egg("Legendary")
    legendary_egg.store_egg()


def menu():
    print("==========Main Menu==========")
    print("")
    print("1| Egg Shop")
    print("")
    while True:
        try:
            choice = int(input("Enter the list number (1) of the page you wish to go to: "))
            match choice:
                case 1:
                    egg_shop()
                case _:
                    pass
        except ValueError:
            pass


def not_enough_money():
    print("Oops! You don't have enough money to purchase this!")


def check_for_hatched_eggs():
    with open(EGG_STORAGE_PATH, "r") as file:
        eggs = file.readlines()
        loaded_eggs = json.loads(eggs[0])

    for egg_id, egg_data in loaded_eggs.items():
        rarity = egg_data["Rarity"]
        hatch_datetime = datetime.strptime(egg_data["Hatch Datetime"], '%d-%m-%Y, %H:%M:%S')
        worth = float(egg_data["Worth"])
        hatched = egg_data["Hatched"]

        if bool(hatched):
            new_spirit = Spirit(rarity, worth)
            new_spirit.store_spirit()

check_spirit_storage()
check_egg_storage()

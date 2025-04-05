from contextlib import nullcontext
from datetime import *
import random
import os
import json
import time

COMMON_EGGS = ["Wood", "Grass", "Fire"]
UNCOMMON_EGGS = ["Water", "Wind", "Clover"]
RARE_EGGS = ["Gold", "Metal", "Oil"]
LEGENDARY_EGGS = ["Human", "Monster", "Evil"]
EGG_STORAGE_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\egg_storage.json"

money = 0


class Egg:
    def __init__(self, is_starter):
        self.rarity: str
        self.variant_name: str
        self.hatch_time: timedelta
        self.hatch_datetime: datetime
        self.remaining_hatch_time: timedelta
        self.rarity_chance: int
        self.egg_id: int

        self.rarity_chance = random.randint(1, 100)

        if is_starter:
            self.rarity = "Common"
            self.variant_name = random.choice(COMMON_EGGS)
            self.hatch_time = timedelta(hours=1)
            self.hatch_datetime = datetime.now() + self.hatch_time
        else:
            if self.rarity_chance <= 5:
                self.rarity = "Legendary"
                self.variant_name = random.choice(LEGENDARY_EGGS)
                self.hatch_time = timedelta(days=1, hours=12)
                self.hatch_datetime = datetime.now() + self.hatch_time
            elif self.rarity_chance <= 25:
                self.rarity = "Rare"
                self.variant_name = random.choice(RARE_EGGS)
                self.hatch_time = timedelta(hours=12)
                self.hatch_datetime = datetime.now() + self.hatch_time
            elif self.rarity_chance <= 50:
                self.rarity = "Uncommon"
                self.variant_name = random.choice(UNCOMMON_EGGS)
                self.hatch_time = timedelta(hours=3)
                self.hatch_datetime = datetime.now() + self.hatch_time
            else:
                self.rarity = "Common"
                self.variant_name = random.choice(COMMON_EGGS)
                self.hatch_time = timedelta(hours=1)
                self.hatch_datetime = datetime.now() + self.hatch_time

        self.egg_id = get_number_of_eggs_stored()
        self.remaining_hatch_time = self.hatch_datetime - datetime.now()

        self.info_summary = {"Egg ID": self.egg_id,
                             "Rarity": self.rarity,
                             "Variant Name": self.variant_name,
                             "Hatch DateTime": self.hatch_datetime.strftime('%d-%m-%Y')
                             }

        print("Ding! An egg has arrived in your inventory.")


    def get_rarity(self):
        return self.rarity


    def get_remaining_hatch_time(self):
        self.remaining_hatch_time = self.hatch_datetime - datetime.now()
        return self.remaining_hatch_time


    def update_remaining_hatch_time(self):
        self.remaining_hatch_time = self.hatch_datetime - datetime.now()


    def get_egg_variant(self):
        return self.variant_name


    def get_hatch_time(self):
        return self.hatch_time


    def get_hatch_datetime(self):
        return self.hatch_datetime


    def store_egg(self):
        json_summary = json.dumps(self.info_summary)
        if os.stat(EGG_STORAGE_PATH).st_size != 0:
            with open(EGG_STORAGE_PATH, "a") as file:
                file.write(json_summary)
        else:
            with open(EGG_STORAGE_PATH, "w") as file:
                file.write(json_summary)


def check_egg_storage():
    if not os.path.exists(EGG_STORAGE_PATH):
        with open(EGG_STORAGE_PATH, "x") as file:
            pass
        initiate_beginner()
    else:
        pass


def get_number_of_eggs_stored():
    with open(EGG_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        number_of_eggs = len(lines)
        return number_of_eggs


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
            choice = int(input("If you wish to purchase an egg, enter its item number (1/2/3/4), otherwise, enter anything else to cancel."))
            match choice:
                case 1:
                    if can_afford(10):
                        purchase_common_egg()
                        break
                case 2:
                    if can_afford(25):
                        purchase_uncommon_egg()
                        break
                case 3:
                    if can_afford(50):
                        purchase_rare_egg()
                        break
                case 4:
                    if can_afford(100):
                        purchase_legendary_egg()
                        break
                case _:
                    break
        except ValueError:
            pass


def can_afford(price):
    if money < price:
        return False
    return True


def purchase_common_egg():
    pass


def purchase_uncommon_egg():
    pass


def purchase_rare_egg():
    pass


def purchase_legendary_egg():
    pass


def initiate_beginner():
    print("Welcome to my Egg Game!")
    time.sleep(0.5)
    print("The game is simple. Hatch eggs and earn money!")
    time.sleep(0.5)
    print("To start you off, here's a Common Egg.")
    time.sleep(0.5)
    give_starter_egg()
    time.sleep(0.5)
    print("Taking you to the main menu now...")
    menu()


def give_starter_egg():
    starter_egg = Egg(True)
    starter_egg.store_egg()


def menu():
    pass


check_egg_storage()

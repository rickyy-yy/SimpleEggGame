import json
import os
import random
import time as tm
import multiprocessing
import atexit
import sys
from datetime import *

COMMON_SPIRITS = ["Wood", "Grass", "Fire"]
UNCOMMON_SPIRITS = ["Water", "Wind", "Clover"]
RARE_SPIRITS = ["Gold", "Metal", "Oil"]
LEGENDARY_SPIRITS = ["Human", "Monster", "Evil"]
EGG_STORAGE_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\egg_storage.json"
SPIRIT_STORAGE_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\spirit_storage.json"
MONEY_PATH = r"C:\Users\Richie\Documents\Python\SimpleEggGame\money.txt"

money: int
alive = True


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
            file.write("{}")


def check_money():
    if not os.path.exists(MONEY_PATH):
        with open(MONEY_PATH, "x") as file:
            file.write("100")

    get_money()


def get_money():
    global money
    with open(MONEY_PATH, "r") as file:
        money = int(file.readline())


def update_money():
    global money
    with open(MONEY_PATH, "w") as file:
        file.write(str(money))


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
        lines = json.loads(lines[0])
        if len(lines) != 0:
            next_spirit_id = int(list(lines.keys())[len(lines.keys()) - 1])
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
                        if not is_incubator_full():
                            purchase_common_egg()
                            break
                        else:
                            incubator_full()
                    else:
                        not_enough_money()
                case 2:
                    if can_afford(25):
                        if not is_incubator_full():
                            purchase_uncommon_egg()
                            break
                        else:
                            incubator_full()
                    else:
                        not_enough_money()
                case 3:
                    if can_afford(50):
                        if not is_incubator_full():
                            purchase_rare_egg()
                            break
                        else:
                            incubator_full()
                    else:
                        not_enough_money()
                case 4:
                    if can_afford(100):
                        if not is_incubator_full():
                            purchase_legendary_egg()
                            break
                        else:
                            incubator_full()
                    else:
                        not_enough_money()
                case _:
                    menu()
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
    print("Ding! A Common egg arrived in your inventory.")


def give_uncommon_egg():
    uncommon_egg = Egg("Uncommon")
    uncommon_egg.store_egg()
    print("Ding! A Uncommon egg arrived in your inventory.")


def give_rare_egg():
    rare_egg = Egg("Rare")
    rare_egg.store_egg()
    print("Ding! A Rare egg arrived in your inventory.")


def give_legendary_egg():
    legendary_egg = Egg("Legendary")
    legendary_egg.store_egg()
    print("Ding! A Legendary egg arrived in your inventory.")


def menu():
    print(f"=====Eggs: {check_number_of_eggs()}===== Main Menu =====Money: ${money}=====")
    print("")
    print("1| Egg Shop")
    print("2| Egg Incubators")
    print("3| Spirit Pouch")
    print("4| Exit Game")
    print("")
    while True:
        try:
            choice = int(input("Enter the list number (1/2/3/4) of the page you wish to go to: "))
            match choice:
                case 1:
                    egg_shop()
                case 2:
                    view_eggs()
                case 3:
                    view_spirits()
                case 4:
                    exit_game(process)
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

    for egg_id in loaded_eggs.copy():
        egg_data = loaded_eggs[egg_id]
        rarity = egg_data["Rarity"]
        hatch_datetime = datetime.strptime(egg_data["Hatch Datetime"], '%d-%m-%Y, %H:%M:%S')
        worth = float(egg_data["Worth"])
        hatched = egg_data["Hatched"]

        if bool(hatched):
            new_spirit = Spirit(rarity, worth)
            new_spirit.store_spirit()
            loaded_eggs.pop(egg_id)

        if hatch_datetime - datetime.now() < timedelta(seconds=0):
            new_spirit = Spirit(rarity, worth)
            new_spirit.store_spirit()
            loaded_eggs.pop(egg_id)


    with open(EGG_STORAGE_PATH, "w") as file:
        eggs = json.dumps(loaded_eggs)
        file.write(eggs)


def view_eggs():
    loaded_eggs = []
    index = 0
    with open(EGG_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        eggs = json.loads(lines[0])
        for egg in eggs:
            current_egg = eggs[egg]
            rarity = current_egg["Rarity"]
            hatch_datetime = datetime.strptime(current_egg["Hatch Datetime"], '%d-%m-%Y, %H:%M:%S')
            worth = current_egg["Worth"]
            time_to_hatch = str(hatch_datetime - datetime.now()).split('.')[0]

            loaded_eggs.append({"Rarity": rarity,
                                "Worth": f"{worth}",
                                "Time to Hatch": time_to_hatch})

        print("")
        print("=============Egg Inventory=============")
        print("No  |  Rarity   | Worth | Time to Hatch")
        for egg in loaded_eggs:
            index += 1
            print("{0:<2}  |  {1:<9}| ${2:<4} | {3}".format(index, egg['Rarity'], egg['Worth'], egg['Time to Hatch']))
        print("")


def view_spirits():
    loaded_spirits = []
    index = 0
    with open(SPIRIT_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        spirits = json.loads(lines[0])
        for spirit in spirits:
            current_spirit = spirits[spirit]
            rarity = current_spirit["Rarity"]
            variant_name = current_spirit["Variant Name"]
            worth = current_spirit["Worth"]
            gold_production = current_spirit["Gold per Minute"]

            loaded_spirits.append({"Rarity": rarity,
                                   "Variant Name": variant_name,
                                   "Worth": f"{worth}",
                                   "Gold per Minute": gold_production})

        print("")
        print("=================Spirit Inventory=================")
        print("No |  Rarity   |  Variant  |  Worth  | Gold/Minute")
        for spirit in loaded_spirits:
            index += 1
            print("{0}  |  {1:<9}|  {2:<6}   |  ${3:<4}  | {4:<5}".format(index, spirit['Rarity'], spirit['Variant Name'], spirit['Worth'], spirit['Gold per Minute']))
        print("")


def check_number_of_eggs():
    with open(EGG_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        if lines:
            lines = json.loads(lines[0])
            number_of_eggs = len(lines)
            return number_of_eggs
        else:
            return 0


def check_number_of_spirits():
    with open(SPIRIT_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        if lines:
            lines = json.loads(lines[0])
            number_of_spirits = len(lines)
            return number_of_spirits
        else:
            return 0


def is_incubator_full():
    if check_number_of_eggs() < 10:
        return False
    return True


def incubator_full():
    print("Oops! You do not have enough space in your incubator. Sell or hatch an egg first.")


def give_gold():
    global money
    total_gold_per_minute = 0
    with open(SPIRIT_STORAGE_PATH, "r") as file:
        lines = file.readlines()
        spirits = json.loads(lines[0])

    for spirit_id, spirit_data in spirits.items():
        total_gold_per_minute += spirit_data["Gold per Minute"]

    money += total_gold_per_minute


def start_money_giver():
    while alive:
        tm.sleep(60)
        give_gold()


process = multiprocessing.Process(target=start_money_giver)

def main():
    if __name__ == '__main__':
        check_money()
        check_spirit_storage()

        atexit.register(update_money)

        process.start()

        check_egg_storage()


def exit_game(process):
    update_money()
    process.terminate()
    exit(0)


main()

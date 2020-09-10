""" A Choose Your Own Adventure Story """
from time import sleep
from cyoa.cyoa_lib import *
from Fortuna import *


class Adventure:
    def __init__(self, question, answers, funcs):
        self.question = f"\n{question}"
        self.answers = answers
        self.funcs = funcs
        self.delay = 0.25

    def __call__(self):
        print(self.question)
        for key, val in enumerate(self.answers):
            print(f"  {key}. {val}")
        answer = input("\n")

        for key, val in enumerate(self.answers):
            if answer.lower() == self.answers[key].lower():
                sleep(self.delay)
                self.funcs[key]()
                break
            else:
                try:
                    if int(answer) == key:
                        sleep(self.delay)
                        self.funcs[key]()
                        break
                except ValueError:
                    pass
        else:
            print(f"Sorry, I do not understand ({answer}). Please try again.")
            self()


class ChapterOne:
    def __init__(self):
        self.name = ""
        self.char_class = Fighter
        self.weapon = "fists"
        self.vial = False

    def __call__(self, *args, **kwargs):
        self.zero_quest()

    def success(self):
        if self.weapon != "fists":
            if not self.vial:
                print("\nSuccess! You have found the dungeon, and you're equipped for battle.")
                ChapterTwo(self.name, self.char_class, self.weapon, self.vial)()
            else:
                print("\nSuccess! You have found the dungeon, and you're very well equipped for battle.")
                ChapterTwo(self.name, self.char_class, self.weapon, self.vial)()
        else:
            print("\nFailure! You have found the dungeon, but you're not prepared for battle.")
            self.goodbye()
        print("")

    def exit(self):
        pass

    def goodbye(self):
        print(f"\nSorry {self.name}... Game Over.")
        print("")
        Adventure(
            f"Would you like to play again?",
            ("no", "yes", "maybe"),
            (self.exit, self.second_quest, self.maybe)
        )()

    def maybe(self):
        print("I don't have all day, make up your mind.")
        self.first_quest()

    def set_class(self, char_class):
        classes = {
            "Wizard": Wizard,
            "Fighter": Fighter,
            "Rogue": Rogue,
        }
        self.char_class = classes[char_class]

    def zero_quest(self):
        print("\nWhat's your name?")
        self.name = input()
        print(f"Hello {self.name}!")
        # choose class
        Adventure(
            f"What class?",
            ("Wizard", "Fighter", "Rogue"),
            (lambda: self.set_class("Wizard"), lambda: self.set_class("Fighter"), lambda: self.set_class("Rogue"))
        )()
        self.second_quest()

    def first_quest(self):
        Adventure(
            f"Would you like to play a game?",
            ("no", "yes", "maybe"),
            (self.goodbye, self.second_quest, self.maybe)
        )()

    def caught(self):
        print("Your sister catches you!")
        self.goodbye()

    def second_quest(self):
        Adventure(
            f"Your adventure begins in the small village of Alphea. \n"
            "It’s late and all of the villagers are fast asleep, including your family. \n"
            "Choose one...",
            ("go back to bed", "sneak outside", "spy on my sister"),
            (self.goodbye, self.third_quest, self.caught)
        )()

    def third_quest(self):
        Adventure(
            "You manage to sneak out of your house without being noticed. \n"
            "The village streets are quiet, shops are locked for the night. \n"
            "But across the way you can see one of the shops has an open window, \n"
            "Would you like to investigate?",
            ("no", "yes"),
            (self.goodbye, self.forth_quest)
        )()

    def take_shovel(self):
        if self.weapon != "fists" and self.weapon != "shovel":
            print(f"\nYou drop the {self.weapon}.")
            print("You now have the shovel.")
        else:
            if self.weapon != "shovel":
                print("\nYou take the shovel.")
            else:
                print("you already have the shovel.")
        self.weapon = "shovel"
        self.fifth_quest()

    def take_rake(self):
        if self.weapon != "fists" and self.weapon != "rake":
            print(f"\nYou drop the {self.weapon}.")
            print("You now have the rake.")
        else:
            if self.weapon != "rake":
                print("\nYou take the rake.")
            else:
                print("You already have the rake.")
        self.weapon = "rake"
        self.fifth_quest()

    def forth_quest(self):
        Adventure(
            "Inside you find a rake and a shovel, but you can only carry one or the other at this time. \n"
            "Either will make a better weapon than your bare fists.",
            ("take shovel", "take rake", "neither"),
            (self.take_shovel, self.take_rake, self.fifth_quest)
        )()

    def go_home(self):
        Adventure(
            "It’s late and all of the villagers are fast asleep, including your family. \n"
            "Choose one...",
            ("go back to bed", "sneak back outside", "spy on my sister"),
            (self.goodbye, self.third_quest, self.caught)
        )()

    def go_store(self):
        self.forth_quest()

    def go_temple(self):
        Adventure(
            "As you approach the temple you hear the faint sound of someone crying. \n"
            "Would you like to investigate the sound coming from the graveyard or go inside the temple?",
            ("investigate graveyard", "enter temple"),
            (self.find_dungeon, self.goodbye)
        )()

    def find_dungeon(self):
        Adventure(
            "It sounds like someone crying behind the temple. \n"
            "When you go around the temple you can see a graveyard. \n"
            "In the center of the graveyard there is a large stone mausoleum. \n"
            "The rusty iron gate creaks open as if to invite you in. Do you enter?",
            ("no", "yes"),
            (self.goodbye, self.success)
        )()

    def go_alchemy(self):
        Adventure(
            "The merchandise is locked up for the night, \n"
            "except for a corked glass vial containing red fluid laying on the counter. Take vial?",
            ("no", "yes"),
            (self.fifth_quest, self.take_vial)
        )()

    def take_vial(self):
        self.vial = True
        self.fifth_quest()

    def fifth_quest(self):
        Adventure(
            "Where would you like to go?",
            ("home", "store", "temple", "alchemy shop"),
            (self.go_home, self.go_store, self.go_temple, self.go_alchemy)
        )()


class ChapterTwo:
    def __init__(self, name, char_class, weapon, vial):
        self.name = name
        self.char_class = char_class
        self.weapon = weapon
        self.vial = vial
        self.damage = (1, 4)
        self.troll_dead = False

        if self.weapon == "rake":
            self.damage = (1, 8)
        elif self.weapon == "shovel":
            self.damage = (1, 6)

    def __call__(self, *args, **kwargs):
        self.first_quest()

    def goodbye(self):
        print(f"\nSorry {self.name}... Game Over.")
        print("")

    def first_quest(self):
        Adventure(
            "The dungeon is dark and dank. Would what direction would you like to go?",
            ("go north", "go south", "go east", "go west", "go back to town"),
            (self.go_north, self.go_south, self.go_east, self.go_west, self.go_up)
        )()

    def troll(self):
        print("You encounter a Troll!")
        Adventure(
            "The Troll sees you. Would you like to attack or run away?",
            ("attack", "run"),
            (self.attack_troll, self.run_away)
        )()

    def attack_troll(self):
        player = Player(self.name, self.char_class, 1)
        troll = Player("The Troll", Troll, 2)
        print("")
        print(player)
        combat(player, troll)
        if troll.is_dead:
            self.troll_dead = True
            self.go_up()
        else:
            self.goodbye()

    def run_away(self):
        print("The Troll kills you as you try to run a way, coward!")
        self.goodbye()

    def cross_roads(self):
        Adventure(
            "The dungeon is dark and dank. Would what direction would you like to go?",
            ("go north", "go south", "go east", "go west"),
            (self.go_north, self.go_south, self.go_east, self.go_west)
        )()

    def go_north(self):
        print("Going north...")
        if not self.troll_dead and percent_true(25):
            self.troll()
        else:
            if not self.troll_dead:
                self.cross_roads()
            else:
                self.first_quest()

    def go_south(self):
        print("Going south...")
        if not self.troll_dead and percent_true(25):
            self.troll()
        else:
            if not self.troll_dead:
                self.cross_roads()
            else:
                self.first_quest()

    def go_east(self):
        print("Going east...")
        if not self.troll_dead and percent_true(25):
            self.troll()
        else:
            if not self.troll_dead:
                self.cross_roads()
            else:
                self.first_quest()

    def go_west(self):
        print("Going west...")
        if not self.troll_dead and percent_true(25):
            self.troll()
        else:
            if not self.troll_dead:
                self.cross_roads()
            else:
                self.first_quest()

    def go_up(self):
        print("Going up...")
        if not self.troll_dead:
            print("Failure!")
            print("Game Over.")
        else:
            print(f"Congrats {self.name}, You Win!")


if __name__ == "__main__":
    lets_play = ChapterOne()
    lets_play()

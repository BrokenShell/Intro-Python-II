from Fortuna import *
from cyoa.utils import *


class Fighter:
    hd = 10
    name = 'Fighter'
    fav_stat = 'STR'
    primary_att = 'Weapon'
    armor_ac = 18
    max_ac_dex = 2
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Wizard:
    hd = 6
    name = 'Wizard'
    fav_stat = 'INT'
    primary_att = 'Arcane Spell'
    armor_ac = 10
    max_ac_dex = 4
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Paladin:
    hd = 10
    name = 'Paladin'
    fav_stat = 'STR'
    primary_att = 'Melee Weapon'
    armor_ac = 18
    max_ac_dex = 0
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Barbarian:
    hd = 12
    name = 'Barbarian'
    fav_stat = 'STR'
    primary_att = 'Melee Weapon'
    armor_ac = 10
    max_ac_dex = 4
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Sorcerer:
    hd = 6
    name = 'Sorcerer'
    fav_stat = 'CHA'
    primary_att = 'Elemental Spell'
    armor_ac = 10
    max_ac_dex = 4
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Warlock:
    hd = 8
    name = 'Warlock'
    fav_stat = 'CHA'
    primary_att = 'Demonic Spell'
    armor_ac = 12
    max_ac_dex = 4
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Cleric:
    hd = 8
    name = 'Cleric'
    fav_stat = 'WIS'
    primary_att = 'Holy Spell'
    armor_ac = 15
    max_ac_dex = 2
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Bard:
    hd = 8
    name = 'Bard'
    fav_stat = 'CHA'
    primary_att = 'Charm'
    armor_ac = 12
    max_ac_dex = 4
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Druid:
    hd = 8
    name = 'Druid'
    fav_stat = 'WIS'
    primary_att = 'Nature Spell'
    armor_ac = 15
    max_ac_dex = 2
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Rogue:
    hd = 8
    name = 'Rogue'
    fav_stat = 'DEX'
    primary_att = 'Light Weapon'
    armor_ac = 12
    max_ac_dex = 10
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Ranger:
    hd = 8
    name = 'Ranger'
    fav_stat = 'DEX'
    primary_att = 'Ranged Weapon'
    armor_ac = 12
    max_ac_dex = 10
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Monk:
    hd = 8
    name = 'Monk'
    fav_stat = 'DEX'
    primary_att = 'Unarmed Combat'
    armor_ac = 10
    max_ac_dex = 10
    xp_award = 0

    @staticmethod
    def damage(level, bonus):
        return dice(level, 8) + bonus


class Troll:
    hd = 12
    name = 'Troll'
    fav_stat = 'STR'
    primary_att = 'Weapon'
    armor_ac = 15
    max_ac_dex = 2
    xp_award = 1000

    @staticmethod
    def damage(level, bonus):
        return dice(level, 6) + bonus


class Player:
    def __init__(self, name, cls, level):
        self.name = name
        self.cls = cls()
        self.level = smart_clamp(level, 1, 20)
        self.current_hp = 1
        self.total_hp = 1
        self.xp = 0
        self.ac = 10
        self.prof_bonus = 0
        self.magic_bonus = smart_clamp(self.prof_bonus - 2, 0, 3)
        self.save_dc = 0
        self.att_bonus = 0
        self.stats = {}
        self.stat_mod = {}
        self._set_stats()
        self._set_stat_mods()
        self._set_ac()
        self._set_xp()
        self._set_health()
        self._set_prof()
        self._set_save_dc()
        self._set_att_bonus()
        self.damage = self.set_damage()
        self.is_dead = False

    def take_damage(self, num_damage):
        self.current_hp -= num_damage
        if self.current_hp <= 0:
            # print(f"{self.name} has died.")
            self.is_dead = True

    def __repr__(self):
        output = (
            f"Name: {self.name}",
            f"Class: {self.cls.name}, Level: {self.level}",
            f"XP: {self.xp}",
            f"Proficiency Bonus: {self.prof_bonus}",
            f"Armor Class: {self.ac}",
            f"Save DC: {self.save_dc}",
            f"Health: {self.current_hp} / {self.total_hp}",
            f"Attack Bonus: {self.att_bonus}",
            "Ability Scores:",
            f" STR: {self.stats['STR']}, {self.stat_mod['STR']}",
            f" INT: {self.stats['INT']}, {self.stat_mod['INT']}",
            f" DEX: {self.stats['DEX']}, {self.stat_mod['DEX']}",
            f" WIS: {self.stats['WIS']}, {self.stat_mod['WIS']}",
            f" CON: {self.stats['CON']}, {self.stat_mod['CON']}",
            f" CHA: {self.stats['CHA']}, {self.stat_mod['CHA']}",
            ""
        )
        return '\n'.join(output)

    def set_damage(self):
        amount = self.cls.damage(self.level, self.stat_mod[self.cls.fav_stat] + self.magic_bonus)
        return amount

    def set_damage_str(self):
        amount = self.cls.damage(self.level, self.stat_mod[self.cls.fav_stat] + self.magic_bonus)
        kind = self.cls.damage_type
        return f"{amount} {kind}"

    def att_roll(self, target_ac, advantage='none'):
        return attack_roll(target_ac, self.att_bonus, advantage)

    def long_rest(self):
        self.current_hp = self.total_hp

    def _set_stats(self):
        # needed for init and leveling
        stats = ('STR', 'INT', 'DEX', 'WIS', 'CON', 'CHA')
        for ability in stats:
            if ability == self.cls.fav_stat:
                self.stats[ability] = ability_dice(6)
            elif ability == 'CON':
                self.stats[ability] = ability_dice(5)
            else:
                self.stats[ability] = ability_dice(4)

    def _set_ac(self):
        self.ac = self.cls.armor_ac + min(self.stat_mod['DEX'], self.cls.max_ac_dex) + self.magic_bonus

    def _set_stat_mods(self):
        # needed for init and leveling
        mod_by_stat = (
            -5, -5, -4, -4, -3, -3, -2, -2, -1, -1, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7
        )
        for ability in self.stats:
            self.stat_mod[ability] = mod_by_stat[smart_clamp(self.stats[ability], 0, 24)]

    def _set_health(self):
        # only run at init!
        bonus = self.stat_mod['CON'] * self.level
        if self.level > 1:
            hp_gain_by_level = dice(self.level - 1, self.cls.hd)
        else:
            hp_gain_by_level = 0
        self.total_hp = self.cls.hd + hp_gain_by_level + bonus
        self.long_rest()

    def _set_prof(self):
        # needed for init and leveling
        prof_by_level = (0, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6)
        self.prof_bonus = prof_by_level[self.level]

    def _set_save_dc(self):
        # used for init and leveling
        self.save_dc = 8 + self.prof_bonus + self.stat_mod[self.cls.fav_stat]

    def _set_att_bonus(self):
        # used for init and leveling
        self.att_bonus = self.stat_mod[self.cls.fav_stat] + self.prof_bonus + self.magic_bonus

    def _set_xp(self):
        # only run at init!
        xp_by_level = (
            0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000,
            100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000, 400000
        )
        if self.level == 1:
            self.xp = xp_by_level[0]
        else:
            self.xp = random_range(xp_by_level[self.level - 1], xp_by_level[self.level])
            for _ in range(self.level // 4):
                self._boost_stats()

    def _boost_stats(self):
        # used to level up and init
        if self.stats[self.cls.fav_stat] <= 22:
            self.stats[self.cls.fav_stat] += 2
        elif self.stats[self.cls.fav_stat] == 23:
            self.stats[self.cls.fav_stat] += 1
            self.stats['CON'] += 1
        else:
            self.stats['CON'] += 2
        self._set_stat_mods()

    def level_up(self, levels=1):
        # used to level up, max level: 20
        for _ in range(levels):
            # print("{} --> leveling up...".format(self.name))
            self.level += 1
            if self.level > 1 and self.level % 4 == 0:
                self._boost_stats()
            self.total_hp += max(dice(1, self.cls.hd) + self.stat_mod['CON'], 0)
            self._set_prof()
            self._set_save_dc()
            self._set_att_bonus()
        self.long_rest()
        self._set_ac()
        new_damage = self.set_damage()
        old_damage = self.damage
        self.damage = new_damage if new_damage > old_damage else old_damage
        # print(self)

    def xp_gain(self, xp):
        self.xp += xp
        xp_by_level = (
            0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000, 85000,
            100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000
        )
        print(f"{self.name} gained {xp} xp")
        if self.level <= 20:
            if self.level < 18 and self.xp >= xp_by_level[self.level + 2]:
                self.level_up(3)
            elif self.level < 19 and self.xp >= xp_by_level[self.level + 1]:
                self.level_up(2)
            elif self.level < 20 and self.xp >= xp_by_level[self.level]:
                self.level_up(1)
            # print(self)

    def opp_kill(self, num_opp, party_size, difficulty):
        xp_by_level = (
            0, 10, 25, 100, 200, 450, 700, 1100, 1800, 2300, 2900, 3900, 5000, 5900, 7200, 8400,
            10000, 11500, 13000, 15000, 18000, 20000, 22000, 25000, 33000, 41000, 50000,
            62000, 72000, 82000, 92000, 102000, 122000, 142000, 155000
        )
        xp_gained = sum(xp_by_level[self.level + difficulty + 3] // party_size for _ in range(num_opp))
        self.xp_gain(xp_gained)


def combat(player_1, player_2, reroll=False):
    if not reroll:
        print("Roll Initiative!")
    else:
        print("Tie, please roll inititive again")
    p1, p2 = initiative(player_1), initiative(player_2)
    if p1 > p2:
        print(f"{player_1.name} goes first.\n")
        return combat_turns(player_1, player_2)
    elif p1 < p2:
        print(f"{player_2.name} goes first.\n")
        return combat_turns(player_2, player_1)
    else:
        return combat(player_1, player_2, reroll=True)


def initiative(player):
    player_roll = dice(1, 20)
    player_bonus = player.stat_mod["DEX"]
    total = player_roll + player_bonus
    string_bonus = f"+ {player_bonus}" if player_bonus >= 0 else f"- {abs(player_bonus)}"
    print(f"{player.name} rolled: {player_roll} {string_bonus} = {total}")
    return total


def party_initiative(party):
    return sorted([(initiative(member), member) for member in party], key=lambda x: x[0], reverse=True)


def combat_turns(player_1, player_2):
    round_number = 0
    while True:
        if not player_1.is_dead:
            round_number += 1
            combat_turn(player_1, player_2, round_number)
        else:
            player_2.xp_gain(player_1.cls.xp_award)
            winner = player_2
            # player_2.long_rest()
            break

        if not player_2.is_dead:
            combat_turn(player_2, player_1, round_number)
        else:
            player_1.xp_gain(player_2.cls.xp_award)
            winner = player_1
            # player_1.long_rest()
            break
    print("")
    print(f"Winner, after {round_number} rounds: {winner.name}\n")
    return winner


def combat_turn(attacker, defender, round_number):
    success, att_roll, damage_multiplier, target_ac = attack_roll(defender.ac, attacker.att_bonus)
    damage = attacker.damage * damage_multiplier
    defender.take_damage(damage)
    string_bonus = f"+ {attacker.att_bonus}" if attacker.att_bonus >= 0 else f"- {abs(attacker.att_bonus)}"
    output = (
        f"Round {round_number}: ",
        f"{attacker.name} rolls {att_roll - attacker.att_bonus} {string_bonus} = {att_roll}, ",
        f"{success}: {damage} damage"
    )
    print("".join(output))


if __name__ == "__main__":
    my_player = Player("Raven", Barbarian, 10)
    my_troll = Player("The Troll", Troll, 10)
    print()
    print(my_player)
    print(my_troll)
    combat(my_player, my_troll)

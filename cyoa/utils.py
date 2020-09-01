from Fortuna import dice


def advantage_roll(advantage=None):
    """ True = Advantage: max(d20, d20)
        False = Disadvantage: min(d20, d20)
        None = No Advantage: d20 """
    if not advantage and advantage is not False:
        my_roll = dice(1, 20)
    elif advantage:
        arr = (dice(1, 20) for _ in range(2))
        my_roll = max(arr)
    else:
        arr = (dice(1, 20) for _ in range(2))
        my_roll = min(arr)
    return my_roll


def ability_check(dc, bonus=0, advantage="none"):
    ability_roll = advantage_roll(advantage) + bonus
    if ability_roll >= dc:
        check = "Success"
    else:
        check = "Fail"
    return check, ability_roll


def attack_roll(target_ac, bonus=0, advantage="none"):
    att_roll = advantage_roll(advantage)
    if att_roll == 20:
        success = 'Critical Hit'
        damage_multiplier = 2
    elif att_roll == 1:
        success = 'Critical Miss'
        damage_multiplier = 0
    elif att_roll + bonus >= target_ac:
        success = 'Hit'
        damage_multiplier = 1
    else:
        success = 'Miss'
        damage_multiplier = 0
    return success, att_roll + bonus, damage_multiplier, target_ac

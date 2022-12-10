#!/usr/bin/python3
import os
import math
import random

"""
todo list:
format numbers to 2 decimal places
go back to menu after results are displayed
"""


def lockingTime(scan_res, sig_rad):
    """
    calculates ship->ship locking time bases on below variables:
    scan_res = scan resolution of your ship
    sig_rad = signature radius of target ship
    """
    return (40000/scan_res) / (pow(math.asinh(sig_rad), 2))


def missileDamage(s, vt, d, e, ve, drf):
    """
    calculates missile damage based on the below variables:
    s     signature radius of target
    vt    velocity of target
    d     base damage of missile
    e     explosion radius of missile
    ve    explosion velocity of missile
    drf   damage reduction factor (use CCP data)
    damage created = base damage * min[1, S/E, (S/E*Ve/Vt)^drf
    """
    return d * min(1, min(s/e, pow((s/e)*(ve/vt), drf)))
    # NEED CODE TO STOP DRF CAUSING ERROR IF TOO HIGH (WHAT IS TOO HIGH? 1?)


def turretHit(v_angular, was, sig_target, distance, opt_turret, fall_turret, base_damage, shots_fired):
    """
    calculates turret hit quality and damage based on the below variables:
    v_angular = angular velocity
    was = weapon accuracy score
    sig_target = target signature radius
    distance = target distance
    opt_turret = turret optimal range
    fall_turret = turret falloff range
    base_damage = weapon base damage stat
    shots_fired = number of shots you want to test against
    """
    modified_tracking = pow(((v_angular * 40000) / (was * sig_target)), 2)
    modified_range = pow((max(0, distance - opt_turret) / fall_turret), 2)
    chance_to_hit = pow(0.5, (modified_tracking + modified_range))

    damage_list = []

    for i in range(shots_fired):
        rand = random.random()
        damage_modifier = 3 if rand < 0.01 else rand + 0.5

        if rand < chance_to_hit:  # calculate damage value per shot
            damage = damage_modifier * base_damage
        else:
            damage = 0.00
            damage_modifier = 0.00

        if damage_modifier == 3:  # assign damage type string to values <- SIMPLIFY THIS!
            damage_type = "(Wrecks)"
        elif damage_modifier > 1.25 and damage_modifier <= 1.49:
            damage_type = "(Smashes)"
        elif damage_modifier > 1.00 and damage_modifier <= 1.25:
            damage_type = "(Penetrates)"
        elif damage_modifier > 0.75 and damage_modifier <= 1.00:
            damage_type = "(Hits)"
        elif damage_modifier > 0.625 and damage_modifier <= 0.75:
            damage_type = "(Glances off)"
        elif damage_modifier > 0.5 and damage_modifier <= 0.625:
            damage_type = "(Grazes)"
        elif damage_modifier == 0.00:
            damage_type = "(Misses)"

        damage_list.append(damage)
        print(f'Shot {str(i+1)}: Damage = {str(damage)} {str(damage_type)}')
    return sum(damage_list)


# calculate effective weapon dps, without reload time
def dpsCalc(damage, cycle_time, shots=1):
    return (damage / shots) / cycle_time


# MAIN PROGRAM
# clear terminal on program start
os.system('cls' if os.name == 'nt' else 'clear')

# title
print("EVE PvP TOOLS")
print("-------------\n")

# list of main menu options
options = ["Locking Time", "Missile Damage", "Turret Hit Quality", "Quit Program"]

# loop program while waiting for user input
while True:
    try:
        print("\nPlease choose an option:\n------------------------")
        for index, value in enumerate(options):
            print(f'{index+1}) {value}')
        print("------------------------")
        chosen_option = int(input("Enter choice: "))
        # OPTION 1 - Locking Time
        if chosen_option == 1:
            scan_res = int(input("\nScan resolution of attacker: "))
            sig_rad = int(input("Signature radius of defender: "))
            print(f'\nLocking time: {lockingTime(scan_res, sig_rad)}s')
        # OPTION 2 - Missile Damage
        if chosen_option == 2:
            s = int(input("Signature radius of target: "))
            vt = int(input("Velocity of target: "))
            d = int(input("Base damage of missile: "))
            e = int(input("Explosion radius of missile: "))
            ve = int(input("Explosion velocity of missile: "))
            drf = float(input("Damage reduction factor: "))
            damage = missileDamage(s, vt, d, e, ve, drf)
            print(f'Damage per hit: {damage}')
            cycle_time = int(input("Enter cycle time for guns to fire for DPS number (enter to ignore): "))
            print(f'DPS: {dpsCalc(damage, cycle_time)}\n')
        # OPTION 3 - Turret Hit Quality
        if chosen_option == 3:
            v_angular = float(input("Angular velocity: "))
            was = float(input("Weapon accuracy score: "))
            sig_target = int(input("Target's signature radius: "))
            distance = int(input("Target distance: "))
            opt_turret = int(input("Turret optimal range: "))
            fall_turret = int(input("Turret falloff: "))
            base_damage = int(input("Weapon base damage stat: "))
            shots_fired = int(input("Number of shots: "))
            total_damage = turretHit(v_angular, was, sig_target, distance, opt_turret, fall_turret, base_damage, shots_fired)
            print(f'Total Damage: {total_damage}\n')
            cycle_time = int(input("Enter cycle time for guns to fire for DPS number (enter to ignore): "))
            print(f'DPS: {dpsCalc(total_damage, cycle_time, shots_fired)}\n')
        if chosen_option == 4:
            break
    except ValueError:
        continue

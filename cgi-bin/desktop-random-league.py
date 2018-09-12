#!/usr/bin/env python
import json
import random
import urllib

def random_lanes():
    lanes = random.sample(json.load(open("lanes.json", "r"))["lanes"], 2)
    return {"lane1": lanes[0], "lane2": lanes[1]}

def random_champ():
    champs = json.load(open("champs.json", "r"))
    return {"champ": champs[random.choice(list(champs.keys()))][0]}

def random_runepage():
    runes = json.load(open("runes.json", "r"))
    first_path = random.choice(runes["paths"])
    secondary_path = random.choice(runes["paths"])
    while first_path == secondary_path:
        secondary_path = random.choice(runes["paths"])
    keystone = random.choice(runes["keystone"][first_path])
    slot1 = random.choice(runes["slot1"][first_path])
    slot2 = random.choice(runes["slot2"][first_path])
    slot3 = random.choice(runes["slot3"][first_path])
    slots = random.sample(["slot1", "slot2", "slot3"], 2)
    secondary_slot1 = random.choice(runes[slots[0]][secondary_path])
    secondary_slot2 = random.choice(runes[slots[1]][secondary_path])
    return {"keystone": keystone, "first_path": {"slot1": slot1, "slot2": slot2, "slot3": slot3}, "secondary_path": {"slot1": secondary_slot1, "slot2": secondary_slot2}}

lanes = random_lanes()
champ = random_champ()
runes = random_runepage()

print()
print(lanes["lane1"] + ', ' + lanes["lane2"])
print()
print(champ["champ"])
print()
print(runes["keystone"])
print(runes["first_path"]["slot1"].ljust(25) + runes["secondary_path"]["slot1"])
print(runes["first_path"]["slot2"].ljust(25) + runes["secondary_path"]["slot2"])
print(runes["first_path"]["slot3"])
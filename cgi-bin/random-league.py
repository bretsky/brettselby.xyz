#!/usr/bin/env python
import cgi, cgitb
import json
import random
import urllib

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

def random_lanes():
    lanes = random.sample(json.load(open("lanes.json", "r"))["lanes"], 2)
    return {"lane1": lanes[0], "lane2": lanes[1]}

def random_champ():
	return {"champ": random.choice(json.load(open("champs.json", "r")).keys())}

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

data = random_lanes()
data.update(random_champ())
data.update(random_runepage())
print data
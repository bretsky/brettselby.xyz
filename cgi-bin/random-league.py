#!/usr/bin/env python
import cgi, cgitb
import json
import random
import urllib

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

def random_lanes():
    return random.choice(json.load(open("lanes.json", "r"))["lanes"])

def random_champ():
	return random.choice(json.load(open("champs.json", "r")).keys())

print random_champ()
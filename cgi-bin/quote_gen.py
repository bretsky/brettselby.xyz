#!/usr/bin/env python
import cgi, cgitb
import json
import random

cgitb.enable()

print("Content-Type: text/plain;charset=utf-8\n")

def choose_quote():
	quotes = json.load(open("quotes.json", encoding="utf-8"))
	return json[random.choice(list(json.keys()))]

def generate_hmtl(quote):
	
#!/usr/bin/env python
import cgi, cgitb
cgitb.enable()
print("Content-Type: text/plain;charset=utf-8\n")
import urllib2
from re import findall
import random
from decimal import Decimal

form = cgi.FieldStorage() 

try:
    i = int(form.getvalue('i'))
except (TypeError, ValueError):
    i = 1
if i == None:
    i = 1

def weighted_choice(n, p):
	r = random.uniform(0,sum(p))
	cur = 0
	for i in range(len(n)):
		if cur + p[i] >= r:
			return n[i]
		cur += p[i]
		
ideas = open('skinchoice-allwords.txt','r').read().splitlines()
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = { 'User-Agent' : user_agent }
link = "https://csgostash.com/weapon/"
weapon_count = []
weapons = ["Glock-18",
		   "P250",
		   "Desert Eagle",
		   "Dual Berettas",
		   "Tec-9",
		   "CZ75-Auto",
		   "R8 Revolver",
		   "P2000",
		   "USP-S",
		   "Five-SeveN",
		   "Nova",
		   "XM1014",
		   "Sawed-Off",
		   "MAG-7",
		   "MAC-10",
		   "MP7",
		   "UMP-45",
		   "PP-Bizon",
		   "P90",
		   "MP9",
		   "Galil AR",
		   "AK-47",
		   "SSG 08",
		   "SG 553",
		   "AWP",
		   "FAMAS",
		   "M4A4",
		   "M4A1-S",
		   "AUG",
		   "SCAR-20",
		   "M249",
		   "Negev",
		   "Bayonet",
		   "Bowie Knife",
		   "Butterfly Knife",
		   "Falchion Knife",
		   "Flip Knife",
		   "Gut Knife",
		   "Huntsman Knife",
		   "Karambit",
		   "M9 Bayonet",
		   "Shadow Daggers"]
for weapon in weapons:
	request = urllib2.Request("".join((link,weapon.replace(' ', '+'))))
	request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)')
	html = urllib2.urlopen(request).read().decode('utf-8')
	skins = set([name[name.find('=') + 2:len(name) - 1] for name in findall('data-gaevent="' + weapon + '.*?"', html) if not "(Vanilla)" in name])
	length = len(skins)
	if False:
		if length >= weapon_count[len(weapon_count)-1][1]:
			weapon_count.insert(len(weapon_count), (weapon, length))
		else:
			for i in range(len(weapon_count)):
				if length <= weapon_count[i][1]:
					weapon_count.insert(i, (weapon, length))
					break
	else:
		weapon_count.append((weapon, length))

p = [1/x[1]**1.5 for x in weapon_count]
n = [x[0] for x in weapon_count]
user_input = ''
for x in range(min(i, 2000)):
	print('\n' + weighted_choice(n, p))
	print(random.choice(ideas))

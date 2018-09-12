#!/usr/bin/env python
import cgi, cgitb
import json
import random
import urllib2

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

patch = open("patch.txt", "r").read()

req = urllib2.Request('https://ddragon.leagueoflegends.com/cdn/{0}/data/en_US/champion.json'.format(patch))
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
resp = urllib2.urlopen(req)
content = resp.read()

data_dict = json.loads(content)["data"]
champ_info = {}

print(len(data_dict))
for key in list(data_dict.keys()):
    champ_info[key] = {}
    champ_info[key]["name"] = data_dict[key]["name"]
    champ_info[key]["img"] = "https://ddragon.leagueoflegends.com/cdn/{0}/img/champion/{1}".format(patch, data_dict[key]["image"]["full"])

with open('champs.json', 'w') as outfile:
    json.dump(champ_info, outfile)

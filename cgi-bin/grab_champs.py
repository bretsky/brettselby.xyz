#!/usr/bin/env python
import cgi, cgitb
import json
import random
import urllib2
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"


class LeagueChampParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.names = []
        self.urlnames = []
        self.img_base_url = ""
        self.next_data_is_champ = False

    def handle_starttag(self, tag, attrs):
        get_img_url = False
        for attr in attrs:
            if attr[0] == "class" and attr[1] == "champ-name":
                self.next_data_is_champ = True
            elif self.next_data_is_champ and tag == "a" and attr[0] == "href":
                self.urlnames.append(attr[1][:-1])
            elif not self.img_base_url and not get_img_url and tag == "img" and attr[0] == "class" and attr[1] == "img":
                get_img_url = True
        if get_img_url:
            for attr in attrs:
                if attr[0] == "src":
                    self.img_base_url = attr[1][:attr[1].rfind("/") + 1]
           
    def handle_data(self, data):
        if self.next_data_is_champ:
            self.next_data_is_champ = False
            self.names.append(data)




parser = LeagueChampParser()
req = urllib2.Request('https://na.leagueoflegends.com/en/game-info/champions/')
req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36')
resp = urllib2.urlopen(req)
content = resp.read()
print content
parser.feed(content)

img_names = []
for name in parser.urlnames:
    img_names.append(parser.img_base_url + name + ".png")

data_dict = {}

for i in range(len(parser.urlnames)):
    data_dict[parser.urlnames[i]] = [parser.names[i], img_names[i]]

print(len(data_dict.keys()))

with open('champs.json', 'w') as outfile:
    json.dump(data_dict, outfile)

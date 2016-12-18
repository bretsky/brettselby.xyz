#!/usr/bin/env python
import cgi, cgitb
import random

cgitb.enable()

print("Content-Type: text/plain;charset=utf-8\n")

form = cgi.FieldStorage()

try:
    chirps = int(form.getvalue('i'))
except (TypeError, ValueError):
    chirps = 1
if chirps == None:
    chirps = 1
    
chirps = min(chirps, 2000)
words = open('allwords.txt')
wordlist = words.read().splitlines()
nouns = open('nouns.txt', 'r')
nounlist = nouns.read().splitlines()
adj = open('adjectives.txt', 'r')
adjlist = adj.read().splitlines()

def nounpick():
    return random.choice(nounlist)

def chirper():
    for x in range(chirps):
        random.shuffle(wordlist)
        exclam = random.choice(wordlist)
        exclam_gram = exclam.upper() + '! '
        adj = random.choice(adjlist)
        vowels = 'aeiou'
        if adj[0] in vowels:
            adj_gram = "You're an " + adj + ' '
        else:
            adj_gram = "You're a " + adj + ' '
        noun = nounpick()
        print(exclam_gram + adj_gram + noun+ '!')
    return 0
                
chirper()
exit()

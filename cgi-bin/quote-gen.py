#!/usr/bin/env python
import cgi, cgitb
import json
import random

cgitb.enable()

print "Content-Type: text/html;charset=utf-8\n"

def choose_quote():
	quotes = json.load(open("quotes.json", "r"))["quotes"]
	return random.choice(quotes)

def generate_hmtl(quote):
		return """<span>&quot;{}&quot;</span><br><span class="quoteauthor">-{}</span>""".format(quote[0], quote[1])

print generate_hmtl(choose_quote())
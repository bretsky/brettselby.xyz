#!/usr/bin/env python
import cgi, cgitb
import json
import random

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

def choose_quote():
	quotes = json.load(open("quotes.json", "r"))["quotes"]
	return random.choice(quotes)

def generate_html(quote):
	return unicode("""<span id="quotetext">&quot;{}&quot;</span><br><span class="quoteauthor" id="author" style="float:right">&mdash;{}</span>""").format(quote[0], quote[1])

print generate_html(choose_quote()).encode("utf-8")
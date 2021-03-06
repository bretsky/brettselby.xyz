#!/usr/bin/env python
import cgi, cgitb
import json
import random
from xml.etree import ElementTree as ET

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

form = cgi.FieldStorage()

user_input = form.getvalue('s')

etree = ET.parse('dayna-sms.xml')
root = etree.getroot()

def input_reverse_search(s):
	if s:
		user_input = s.lower().split()
	else:
		user_input = ""
	sms_list = root.getchildren()
	indexes = []
	scores = []
	for sms in root.findall('./*[@type="1"]'):
		word_score = 0
		run_score = 0
		match_count = 0
		body = sms.attrib['body'].lower().split()
		indexes.append(sms_list.index(sms))
		if any(strip_non_alphanum(word) in [strip_non_alphanum(w) for w in body] for word in user_input):			
			if user_input[-1] == body[-1]:
				run_score += 2
				for i in range(min(len(user_input)-1, len(body)-1)):
					index = -2 - i
					if user_input[index] == body[index]:
						run_score += 2
			word_score += len(set([word for word in user_input if strip_non_alphanum(word) in [strip_non_alphanum(w) for w in body]]))
			scores.append((word_score + 4*run_score**2)**2)
		else:
			scores.append(0.25)
	if not indexes:
		return None
	return (indexes, scores)

def strip_non_alphanum(s):
	return ''.join([c for c in s if c.lower() in 'abcdefghijklmnopqrstuvwxyz'])

def find_reply(index):
	while index < len(root.getchildren())-1:
		index += 1
		if root[index].attrib['type'] == '2':
			return index
	return None

def get_reply(s):
	indexes, scores = input_reverse_search(s)
	best_indexes = [indexes[index] for index in [index for index, val in enumerate(scores) if val == max(scores)]]
	choice = random.choice(best_indexes)
	reply = find_reply(choice)
	return root[reply].attrib['body']

print get_reply(user_input)

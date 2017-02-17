#!/usr/bin/env python
import cgi, cgitb
from xml.etree import ElementTree as ET
import random

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

def weighted_choice(choices):
	total = sum(w for c, w in choices)
	r = random.uniform(0, total)
	upto = 0
	for c, w in choices:
		if upto + w >= r:
			return c
		upto += w
	assert False

def find_reply(index):
	while index < len(root.getchildren())-1:
		index += 1
		if root[index].attrib['type'] == '2':
			return index
	return None

def get_first_word(s):
	indexes, scores = input_reverse_search(s)
	choice = weighted_choice(list(zip(indexes, scores)))
	reply = find_reply(choice)
	return root[reply].attrib['body'].split()[0]

def get_next_word(sentence):
	sentence_list = [word.lower() for word in sentence.split()]
	sms_list = root.getchildren()
	indexes = []
	scores = []
	for sms in root.findall('./*[@type="2"]'):		
		body = sms.attrib['body'].lower().split()
		if sentence_list[-1] in body:
			word_score = 0
			sms_index = sms_list.index(sms)
			word_indexes = [i for i, x in enumerate(body) if x == sentence_list[-1]]
			indexes += [(sms_index, word_index) for word_index in word_indexes]
			for word_index in word_indexes:
				run_score = 2
				for i in range(min(len(sentence_list)-1, word_index)):
					index = -2-i
					if sentence_list[index] == body[index]:
						run_score += 2
			word_score += len(set([word for word in sentence_list if word in body]))
			scores.append((word_score + 4*run_score**2)**2)
	next_index = weighted_choice(list(zip(indexes, scores)))
	if next_index[1]+1 >= len(root[next_index[0]].attrib['body'].split()):
		return [' '.join([sentence]), False]
	else:
		next_word = root[next_index[0]].attrib['body'].split()[next_index[1]+1]
	return [' '.join((sentence, next_word)), True]

def create_message(s):
	first_word = get_first_word(s)
	message = first_word
	not_at_end = True
	while not_at_end:
		next_word = get_next_word(message)
		message = next_word[0]
		not_at_end = next_word[1]
	return message
	
print create_message(user_input)

#!/usr/bin/env python
import cgi, cgitb
import random

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8\n"

form = cgi.FieldStorage()

user_input = form.getvalue('s')

class Conversation():
	def __init__(self, src):
		src = src.splitlines()
		self.intro = src[0].replace("bretsky: ", "")
		self.convo = {}
		for i in range(1, len(self.convo)//2):
			self.convo[src[2*i - 1].replace("cleverbot: ", "").split()] = src[2*i].replace("bretsky: ", "").split()

	def get_scores(s):
		scores = {}
		for key in list(self.convo.keys()):
			word_score = 0
			run_score = 0


def convert_src(src):
	src = src.lower().split("<conversation>\n")[1:]
	convos = [Conversation(convo) for convo in src]
	return convos

def input_reverse_search(s, convos):
	user_input = s.lower().split()
	indexes = []
	scores = []
	for convo in convos:
		for msg in convo:
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


convos = open("brett-src.txt", "r").read()
convos = convert_src(convos)
print len(convos)
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
		self.original = {}
		for i in range(1, len(src)//2):
			clever_msg = tuple(strip_non_alphanum(src[2*i - 1].replace("cleverbot: ", "").lower()).split())
			brett_msg = tuple(strip_non_alphanum(src[2*i].replace("bretsky: ", "").lower()).split())
			self.convo[clever_msg] = brett_msg
			self.original[brett_msg] = src[2*i].replace("bretsky: ", "")
			self.original[clever_msg] = src[2*i - 1].replace("cleverbot: ", "")

	def get_scores(self, s):
		scores = []
		for msg in list(self.convo.keys()):
			reply = self.original[self.convo[msg]]
			word_score = 0
			run_score = 0
			for i in range(min(len(s), len(msg))):
				index = -1 - i
				if s[index] == msg[index]:
					run_score += 2
				else:
					break
			word_score += len(set([word for word in s if word in msg]))
			score = (word_score + 4*run_score**2)**2 + 1
			scores.append((score, self.original[msg], reply))
		return scores

def convert_src(src):
	src = src.split("<conversation>\n")[1:]
	convos = [Conversation(convo) for convo in src]
	return convos

def input_lookup(s, convos):
	user_input = strip_non_alphanum(s.lower()).split()
	scores = []
	for convo in convos:
		scores.extend(convo.get_scores(user_input))
	return scores

def strip_non_alphanum(s):
	return ''.join([c for c in s if c.lower() in 'abcdefghijklmnopqrstuvwxyz '])

def get_reply(s, convos):
	scores = input_lookup(s, convos)
	max_score = max(scores, key=lambda x: x[0])[0]
	# print max_score
	best_indexes = [msg[2] for msg in scores if msg[0] >= 0.9*max_score]
	# print len(best_indexes)
	choice = random.choice(best_indexes)
	return choice


convos = open("brett-src.txt", "r").read()
convos = convert_src(convos)
print get_reply(user_input, convos)
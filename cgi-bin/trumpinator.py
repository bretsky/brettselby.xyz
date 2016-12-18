#! /bin/python
import cgi, cgitb
cgitb.enable()
print "Content-type: text/plain;charset=utf-8\n"
form = cgi.FieldStorage() 

contexts = 3
try:
	contexts = int(form.getvalue('i'))
except (TypeError, ValueError):
	contexts = 3
if contexts == None:
	contexts = 3
if contexts == -1:
	contexts = 1000
    
contexts = min(contexts, 1000)
import random
import time
import codecs
start = time.clock()

def weighted_random(c, p):
	average = sum(p)/len(p)
        c = [c[i] for i in range(len(c)) if p[i] >= 0.5*average]
        p = [p[i] for i in range(len(p)) if p[i] >= 0.5*average]
	target = random.uniform(0, sum(p))
	total = 0
	choice = random.randrange(len(c))
	while total < target:
		choice = random.randrange(len(c))
		total += p[choice]
	if sum(p) > 0:
		pass
	else:
		pass
	return c[choice]

class Corpus():
	def __init__(self, src):
		self.text = codecs.open(src, mode='r', encoding='utf-8').read()
		self.nested_pairs =  [(u'\u2014', u'\u2014'), ('(', ')')]
		self.nested_start_tokens = [nested_pair[0] for nested_pair in self.nested_pairs]
		self.linear_pairs = [('', '.'), ('', '!'), ('', '?'), ('.', '.'), ('.', '!'), ('.', '?'), ('!', '.'), ('!', '?'), ('!', '!'), ('?', '.'), ('?', '!'), ('?', '?')]
		self.linear_start_tokens = [linear_pair[0] for linear_pair in self.linear_pairs]
		self.tokens = self.parse(self.text)
		self.contexts = self.separate(self.tokens)

	def parse(self, text):
		tokens = []
		token = ''
		for c in text:
			if c == ' ':
				if token:
					tokens.append(token)
					token = ''
			elif c in [',', '.', ';', ':', '(', ')', '"', u'\u2014', '!', '?']:
				if token:
					tokens.append(token)
					token = ''
				tokens.append(c)
			else:
				token += c
		return tokens

	def separate(self, tokens):
		contexts = Contexts()
		start = ''
		end = ''
		split = False
		# Make contexts class to handle context nesting, identifying contexts and moving between them
		# When split found, set split value, move to next context, when end found (token pair) move to previous, until original context end.
		# Use reverse process to generate nested contexts for speeches
		index = contexts.insert(Context([], ''), 0)
		for t in range(len(tokens)):
			token = tokens[t]
			if token in ['.', '(', ')', u'\u2014', '!', '?']:
				if (contexts.contexts[index].start, token) in self.nested_pairs:
					contexts.contexts[index].end = token
					index = contexts.structure[index]
				elif (contexts.contexts[index].start, token) in self.linear_pairs:
					contexts.contexts[index].end = token
					if index != 1:
						index = contexts.insert(Context([], token), contexts.structure[index])
				elif token in self.nested_start_tokens:
					new_index = contexts.insert(Context([], token), index)
					contexts.contexts[index].splits.append((len(contexts.contexts[index].tokens), new_index))
					index = new_index				
			else:
				contexts.contexts[index].tokens.append(token)
		return contexts
				

class Context():
	def __init__(self, tokens, start=None, end=None):
		self.tokens = tokens
		self.start = start
		self.end = end
		self.splits = []

	def search(self, token):
		indices = []
		for t in range(len(self.tokens)):
			if self.tokens[t].lower() == token.lower():
				indices.append(t)
		return indices

class Contexts():
	def __init__(self):
		self.contexts = [0]
		self.structure = {}

	def insert(self, context, insert):
		index = len(self.contexts)
		self.contexts.append(context)
		self.structure[index] = insert
		return index

	def add(self, context):
		self.contexts.append(context)
		return len(self.contexts) - 1

class Speech():
	def __init__(self, src, limit=3):
		self.corpus = Corpus(src)
		self.contexts = Contexts()
		self.tokens = []
		self.limit = limit

	def start(self, index):
		random_context = random.choice(self.corpus.contexts.contexts[1:])
		self.tokens.append(random_context.tokens[0].capitalize())
		self.contexts.contexts[index].tokens.append(random_context.tokens[0].capitalize())
		
	def get_random_word(self):
		random_context = random.choice(self.corpus.contexts.contexts[1:])
		return random_context.tokens[0]


	def search(self, token):
		indices = []
		for c in range(1, len(self.corpus.contexts.contexts)):
			s = self.corpus.contexts.contexts[c].search(token)
			indices.extend([(c, s[i]) for i in range(len(s))])
		return indices

	def backtrack(self, current, target):
		backtrack = 0
		for i in range(-1, -min(len(current), len(target)) - 1, -1):
			if current[i].lower() == self.corpus.contexts.contexts[target[0]].tokens[target[1] + i + 1].lower():
				backtrack += 1
			else:
				break
		return backtrack

	def similar(self, current, target):
		similar = 0
		for token in current[-1:-8:-1]:
			for match in self.corpus.contexts.contexts[target[0]].tokens[-1:-8:-1]:
				if token.lower() == match.lower():
					similar += 1
		return similar

	def score(self, current, target):
		backtrack = self.backtrack(current, target)
		similar = self.similar(current, target)
		return max((backtrack-1), 0)**4 + (similar)/3

	def find_next(self, context, split=False):
		#if random.randrange(0, 140) == 0:
		#	return "[APPLAUSE]"
		targets = self.search(context.tokens[-1])
		
		if split:
			targets = [targets[i] for i in range(len(targets)) if len(self.corpus.contexts.contexts[targets[i][0]].tokens) != targets[i][1] + 1]
		if len(targets) == 0:
			return self.get_random_word()
		scores = [self.score(context.tokens, targets[i]) for i in range(len(targets))]
		target = weighted_random(targets, scores)
		target_context = self.corpus.contexts.contexts[target[0]]
		if target[1] + 1 == len(target_context.tokens):
			return target_context.end
		else:
			return target_context.tokens[target[1] + 1]

	def add(self, index, split=False):
		if index >= self.limit:
			return None, False
		next_token = self.find_next(self.contexts.contexts[index], split)
		self.tokens.append(next_token)
		if next_token in ['.', '(', ')', u'\u2014', '!', '?']:
			if (self.contexts.contexts[index].start, next_token) in self.corpus.nested_pairs:
				self.contexts.contexts[index].end = next_token
				return self.contexts.structure[index], True
			elif (self.contexts.contexts[index].start, next_token) in self.corpus.linear_pairs:
				self.contexts.contexts[index].end = next_token
				if not self.contexts.structure[index] == 0:
					index = self.contexts.insert(Context([], next_token), self.contexts.structure[index])
					self.start(index)
					return index, False
				else:
					return (None, False)
			elif next_token in self.corpus.nested_start_tokens:
				new_index = self.contexts.insert(Context([], next_token), index)
				if new_index >= self.limit:
					return None, False
				self.contexts.contexts[index].splits.append((len(self.contexts.contexts[index].tokens), new_index))			
				self.start(new_index)
				return new_index, False
			else:
				return self.add(index, split=split) 
		else:
			self.contexts.contexts[index].tokens.append(next_token)
			return index, False



	def write(self):
		self.contexts.insert(Context([], ''), 0)
		index = 1, False
		self.start(index[0])
		while index[0] != None and index[0] <= self.limit:
			if index[1]:
				index = self.add(index[0], split=True)
			else:
				index = self.add(index[0])
				# print(self.__str__())

	def __str__(self):
		string = unicode(' '.join(self.tokens[:-1]).replace(' .', '.').replace(' ,', ',').replace(' ;', ';').replace(u'\u2014,', u'\u2014').replace(u'\u2014', '--').replace(' " ', ' ').lower() + '!')
		return string
				
speech = Speech("corpus.txt", limit=contexts)

speech.write()


print 'Imported and configured modules\n'
print str(speech) 
print '\n-------- Execution took ' + str(time.clock() - start) + 's --------'

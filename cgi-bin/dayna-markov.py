from xml.etree import ElementTree as ET
import random
etree = ET.parse('dayna-sms.xml')
root = etree.getroot()
# for sms in root.findall('./*[@type="1"]'):
# 	print(sms.attrib['body'])

def input_reverse_search(s):
	user_input = s.lower().split()
	sms_list = root.getchildren()
	indexes = []
	scores = []
	for sms in root.findall('./*[@type="2"]'):
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
			# print(' '.join(body), word_score, run_score)
			scores.append((word_score + 4*run_score**2)**2)
		else:
			scores.append(0.25)
	if not indexes:
		return None
	return (indexes, scores)

def strip_non_alphanum(s):
	# print(''.join([c for c in s if c.lower() in 'abcdefghijklmnopqrstuvwxyz']))
	return ''.join([c for c in s if c.lower() in 'abcdefghijklmnopqrstuvwxyz'])

def weighted_choice(choices):
	total = sum(w for c, w in choices)

	r = random.uniform(0, total)
	upto = 0
	for c, w in choices:
		if upto + w >= r:
			# print(w, '/', total, '=', str(w/total*100) + '% chance')
			return c
		upto += w
	assert False

def find_reply(index):
	while index < len(root.getchildren())-1:
		index += 1
		if root[index].attrib['type'] == '1':
			return index
	return None

def get_first_word(s):
	indexes, scores = input_reverse_search(s)
	# print(indexes, scores)
	# [print(root[index].attrib['body'] + '\t ' + str(score)) for index, score in zip(indexes, scores)]
	choice = weighted_choice(list(zip(indexes, scores)))
	# print('Sent text:', root[choice].attrib['body'])
	# print('Score:', scores[indexes.index(choice)])
	reply = find_reply(choice)
	# print([root[reply].attrib['body'] for reply in replies])
	# print('Reply:', root[reply].attrib['body'])
	# print('Chosen word:', root[reply].attrib['body'].split()[0], '\n')
	return root[reply].attrib['body'].split()[0]

def get_next_word(sentence):
	sentence_list = [word.lower() for word in sentence.split()]
	sms_list = root.getchildren()
	indexes = []
	scores = []
	for sms in root.findall('./*[@type="1"]'):		
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
			# print(' '.join(body) + '\t', word_score, run_score, (word_score + 4*run_score**2)**2)
	next_index = weighted_choice(list(zip(indexes, scores)))
	# print(next_index)
	# print('Next message:', root[next_index[0]].attrib['body'])
	# print("Score:", scores[indexes.index(next_index)])
	if next_index[1]+1 >= len(root[next_index[0]].attrib['body'].split()):
		return [' '.join([sentence]), False]
	else:
		next_word = root[next_index[0]].attrib['body'].split()[next_index[1]+1]
		# print('Next word:', next_word)
		# print(indexes)
		# print(scores)
	# print('Current sentence:', ' '.join((sentence, next_word)), '\n')
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

print('Brett:')
user_input = input()
while user_input != "*ABORT":
	print('Dayna:')
	print(create_message(user_input))
	print('Brett:')
	user_input = input()
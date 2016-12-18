#!/usr/bin/env python
import cgi, cgitb
cgitb.enable()
print("Content-Type: text/plain;charset=utf-8\n")
print('Imported and configured CGI')
import random
print('Imported random module')
import time
print('Imported time module')
start = time.clock()
print('Initialized clock, time: %i' %start)
swift_lyrics = open('swift_lyrics.txt', 'r')
print('Opened lyrics source file')
swift_songs = swift_lyrics.read().split('%new_song%')
print('Assembled song library')
for song_index in range(len(swift_songs)):
	# print('Beginning organisation of song %i' %(song_index+1))
	song = swift_songs[song_index].split('\n\n')
	swift_songs[song_index] = song
	for verse_index in range(len(song)):
		verse = song[verse_index].split('\n')
		swift_songs[song_index][verse_index] = verse
		for line_index in range(len(verse)):
			line = verse[line_index].split()
			swift_songs[song_index][verse_index][line_index] = line
	# print('Finished organisation of song %i' %(song_index+1))
print 'All', len(swift_songs), 'songs loaded successfully'
end = time.clock()
print('Setup complete; time taken: ' + str(end-start))

def first_word():
	song = random.choice(swift_songs)
	verse = random.choice(song)
	line = random.choice(verse)
	# print(verse)
	# print(' '.join(line) + ': is the starting line')
	return line[0]

def word_count(a):
	start = time.clock()
	word_counter = 0
	for song in swift_songs:
		for verse in song:
			for line in verse:
				word_counter += line.count(a)
	end = time.clock()
	# print('Finding %i instances of "%s" took ' %(word_counter, a) + str(end-start) + ' seconds')
	return word_counter

def double_word_count(word1, word2):
	start = time.clock()
	word_counter = 0
	for song in swift_songs:
		for verse in song:
			for line in verse:
				for word_index in range(len(line)):
					if line[word_index] == word1:
						if word_index+1 != len(line):
							if line[word_index+1] == word2:
								word_counter += 1
	end = time.clock()
	# print('Finding %i instances of "%s" took ' %(word_counter, a) + str(end-start) + ' seconds')
	return word_counter

def find_double_word(word1, word2, index):
	counter = 0
	for song in swift_songs:
		for verse in song:
			for line in verse:
				for word_index in range(len(line)):
					if line[word_index] == word1:
						if word_index+1 != len(line):
							if line[word_index+1] == word2:
								if counter >= index:
									if word_index+2 != len(line):
										# print(line[word_index+1] + ' is the next word')
										return line[word_index+2]
									else:
										return False
								counter += 1


def find_word(word, index):
	counter = 0
	for song in swift_songs:
		for verse in song:
			for line in verse:
				for word_index in range(len(line)):
					if line[word_index] == word:
						if counter >= index:
							if word_index+1 != len(line):
								# print(line[word_index+1] + ' is the next word')
								return line[word_index+1]
							else:
								return False
						counter += 1

def find_next_line(word, index):
	counter = 0
	for song in swift_songs:
		for verse in song:
			for line_index in range(len(verse)):
				line = verse[line_index]
				for word_index in range(len(line)):
					if line[word_index] == word:
						if counter >= index:
							if line_index+1 != len(verse):
								# print(verse[line_index+1][0] + ' is the start of the next line')
								return verse[line_index+1][0]
							else:
								# print('No next line found')
								return first_word()
						counter += 1

def make_line(first, start_song):
	start = time.clock()
	# print('Beginning creation of a line')
	line = []
	# print('"' + first + '" is the root')
	if start_song:
		line.append(first)
	if not start_song:
		# print('not start_song')
		index = random.randrange(0, word_count(first))
		next_word = find_next_line(first, index)
		line.append(next_word)
	x = 0
	while x < 12:
		if x >= 1:
			index = random.randrange(0, double_word_count(line[x-1], line[x]))
			next_word = find_double_word(line[x-1], line[x], index)
		else:
			index = random.randrange(0, word_count(line[x]))
			next_word = find_word(line[x], index)
		if next_word:
			line.append(next_word)
			x += 1
			# print('Word #%i has been created, it is %s' %(x+1, next_word))
		else:
			end = time.clock()
			# print('Line creation successful, found end word; process took ' + str(end-start) + ' seconds')
			return line
	end = time.clock()
	# print('Line creation successful, max line length reached; process took ' + str(end-start) + ' seconds')
	return line

def make_verse():
	lines = random.randrange(2,9)
	verse = []
	verse.append(make_line(first_word(), True))
	for x in range(lines-1):
		verse.append(make_line(verse[x][::-1][0], False))
	return verse

def make_song():
	song = []
	intro = make_verse()
	verse1 = make_verse()
	verse2 = make_verse()
	chorus = make_verse()
	verse3 = make_verse()
	verse4 = make_verse()
	bridge = make_verse()
	verse5 = make_verse()
	verse6 = make_verse()
	outro  = [intro[0]]
	song.append(intro)
	song.append(verse1)
	song.append(verse2)
	song.append(chorus)
	song.append(verse3)
	song.append(verse4)
	song.append(chorus)
	song.append(bridge)
	song.append(verse5)
	song.append(verse6)
	song.append(chorus)
	song.append(outro)
	return song

def make_title(song):
	title_length = random.randrange(1,3)
	title = []
	verse = random.choice(song)
	line = random.choice(verse)
	if len(line) >= title_length:
		start = random.randrange(0,len(line)-title_length+1)
		title = line[start:start+3]
		return title
	else:
		return make_title(song)


def write_song(song):
	print('\n\n\n\n\n\n')
	title = ' '.join(make_title(song))
	print(title)
	print('-'*len(title))
	print('\n\n')
	for verse in song:
		for line in verse:
			print(' '.join(line))
		print('\n')
	return 0

start = time.clock()
write_song(make_song())
end = time.clock()
print('\n\n\n\n')
print('Program terminated in ' + str(end-start) + ' seconds')

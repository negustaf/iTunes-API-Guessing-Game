# No code will be printable without the imported files form Jupiter Notebook. This file is purely for record of code. Sorry you can't play the game. It was a fun one :/

import requests, json, sys, random, time # imported all at once, random and time will be used later

# Part 1.1: Search for music on the iTunes API
# Fetches a list of songs from the iTunes API (https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/). iTunesSearch returns a list of results from the iTunes API. It is limited to only include music tracks.

def iTunesSearch(searchTerm):
	urlRequest = 'https://itunes.apple.com/search'; params = {'term': searchTerm, 'media': 'music', 'entity': 'musicTrack'}
	response = requests.get(urlRequest, params)
	results = response.json()
	return results

iTunesSearch('Mesa')

# Part 1.2: Get a list of songs
# Indefinitely asks user for search terms (e.g., artist names, track names, etc.). For every search term the user enters, the results from the iTunes API (part 1.1) are added to a list that tracks all the results. The program asks the user for search terms until they enter 'stop'.

roundNumber = 1

while True:
	print('== ROUND ' + str(roundNumber) + ' ==')
	
	calledSongs = []
	trackedSongs = {}
	
	whileLoopRunCount = 0

	while True:
		userInput = input('''Enter a search term (song name, artist, album, etc.) to find a song (enter "done calling terms" to stop the program): ''')
		if userInput == '==exit==': # added this for ability to stop the game at any point
			sys.exit('''You successfully broke the game.''')
		if userInput != 'done calling terms':
			whileLoopRunCount += 1
			for item in iTunesSearch(userInput)['results']:
				calledSongs.append(item['trackName'])
			referenceCount = 0
			for item in iTunesSearch(userInput)['results']:
				trackedSongs[item['trackName']] = 0
				referenceCount += 1
			songs_entered = len(calledSongs)
			print('{} songs so far'.format(songs_entered))
		if userInput == 'done calling terms':
			if whileLoopRunCount != 0:
				print('{} songs total'.format(songs_entered))
				break
			if whileLoopRunCount == 0:
				print('Zero terms entered. Please enter a valid song term.')
				continue
			#print(calledSongs)

# Part 2.1: Pick a random song
# After creating a list of songs (part 1), the program picks a song at random from that list.

	randomSong = random.choice(calledSongs)
	#print(randomSong)

# Part 2.2: Play a song preview
# After picking a random song (2.1), the program plays an audio preview of the song by importing a few features from the IPython.display module. The program then generates a URL for an audio file.

	from IPython.display import display, Audio, clear_output
	audio_url = iTunesSearch(randomSong)['results']['trackName'==randomSong]['previewUrl']
	display(Audio(audio_url, autoplay=True))

# Part 2.3: Print a "blanked out" version of the song
# After picking a random song (2.1) and playing a song preview (2.2), the code replaces every alphanumeric character (a-z, 0-9) in the track name with an underscore ('_').

	blankedSong = ''
	for ch in randomSong:
		if ch.isalnum() == True:
			blankedSong += '_'
		elif ch == " ":
			blankedSong += ' '
		else: 
			blankedSong += ch
	print(blankedSong)
	failedAttemptsCount = 0

# Part 2.4: Allow the user to guess the track name (or pass)
# After the program picks a random song (2.1), plays the song preview (2.2), and prints a "blanked out" version of the song (2.3), it repeatedly asks the user to guess the song. Each time, it does the following:
# - Asks the user to enter a guess (using input()).
# - If the user guesses the correct track name, print "You got it!".
# - If the user guesses incorrectly, print "It's not '<what the user entered>'".
# - If the user enters 'pass' then the correct answer is displayed ("The song was '<track name>'") and stops asking for guesses.
# This is not run to be case sensitive.

	while True:
		user_guess = input('''Enter your guess here for what song you are listening to (enter 'pass' if you don't know): ''')
		if user_guess.upper() == '==exit=='.upper():
			sys.exit('''You successfully broke the game.''')
		if user_guess.upper() == randomSong.upper():
			print('You got it!')
			time.sleep(3)
			break
		elif user_guess.upper() == 'pass'.upper():
			print('The song was {}'.format(randomSong))
			time.sleep(3)
			break
		else: 
			print("It's not {}".format(user_guess))
# Part 2.5: Indefinite rounds¶
# The program repeats parts 2.1-2.4 indefinitely (until the user types 'exit'). 

# Part 3: (Lines 77-108 and marked extraneous lines): Hints and counting runs
#  If the user doesn't answer correctly in three tries, they will be prompted with a hint. If they accept the hint, they will see it and continue back to guessing. If they deny the hint, they will be forced to keep guessing and will be prompted after another three guesses. This process will repeat for a second hint. The first hint is to reveal album artwork. The second hint is to reveal the name of the artist. I also included termination commands by typing '==exit==' in all the input prompts for the admin to terminate the game if necessary (without using 'interupt the kernel' in the code window). I also wrote whileLoopRunCount to track whether the user is inputing 'done calling terms' when there are no terms desired, preventing the script from erroring with terms counted for 'done calling terms'.
			failedAttemptsCount += 1 
			if failedAttemptsCount == 3: 
				user_hint_request1 = input('''Do you want a hint? Answer with 'yes' or 'no'.''')
				if user_hint_request1 == '==exit==':
					sys.exit('''You successfully broke the game.''')
				if user_hint_request1 == 'yes':
					print('''Let's see if this helps.''')
					from IPython.display import Image
					album_art_url = iTunesSearch(randomSong)['results']['trackName'==randomSong]['artworkUrl100']
					display(Image(album_art_url))
					time.sleep(3)
					continue
				else:
					failedAttemptsCount = 0
					continue
			if failedAttemptsCount == 6:
				user_hint_request2 = input('''Do you want another hint? This is your last one! Answer with 'yes' or 'no'.''')
				if user_hint_request2 == '==exit==':
					sys.exit('''You successfully broke the game.''')
				if user_hint_request2 == 'yes':
					print('''Let's see if this helps.''')
					time.sleep(3)
					artistName = iTunesSearch(randomSong)['results']['trackName'==randomSong]['artistName']
					print('''The artist's name is: {}'''.format(artistName))
					time.sleep(3)
					continue
				else: # 'no' or other
					failedAttemptsCount = 3
					continue
			else:
				continue
		time.sleep(3)
	clear_output()
	end_game = input('''Do you want to exit the game? Enter 'yes' or 'exit' to leave the game. To stay in the game, enter 'no' or anything.''')
	if end_game == 'exit' or end_game == 'yes':
		print('Hope you liked my game! Come back soon!')
		time.sleep(3)
		break
	else:
		roundNumber += 1
		continue
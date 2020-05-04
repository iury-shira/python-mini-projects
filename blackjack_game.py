import random

try:
	import tkinter
except ImportError:
	import Tkinter as tkinter		# if running in Python 2


# function to "retrieve" the cards image files from the directory "cards" in a list variable
def load_cards(cards_list: list):
	suits = ['heart', 'club', 'diamond', 'spade']
	face_cards = ['jack', 'queen', 'king']

	if tkinter.TkVersion >= 8.6:
		extension = 'png'
	else:
		extension = 'ppm'

	# for each suit, retrieve the card image files for numbers and faces
	for suit in suits:
		for number in range(1, 11):
			file_path = 'cards/{}_{}.{}'.format(str(number), suit, extension)
			image_object = tkinter.PhotoImage(file=file_path)
			cards_list.append((number, image_object,))

		for face in face_cards:
			file_path = 'cards/{}_{}.{}'.format(str(face), suit, extension)
			image_object = tkinter.PhotoImage(file=file_path)
			cards_list.append((10, image_object))


def deal_card(frame, deck_game: list):
	# pop the next card off the top of the deck
	next_card = deck_game.pop(0)
	# add the image to a Label and then display the Label
	tkinter.Label(frame, image=next_card[1], relief='raised').pack(side='left')
	return next_card


def score_hand(hand: list):
	# Calculates the total score of the hand. Only one ace can have the value 11, and this will be reduced to if the
	# hand would bust
	score = 0
	ace = False

	for card in hand:
		card_value = card[0]
		# ace
		if card_value == 1 and not ace:
			card_value += 10
			ace = True
		score += card_value
		# if the hand bust
		if score > 21 and ace:
			score -= 10
			ace = False
	return score


# deal cards to dealer and also gives the game result
def deal_dealer():
	global end_game
	if not end_game:
		dealer_score = score_hand(dealer_hand)
		while 0 < dealer_score < 17:
			dealer_hand.append(deal_card(dealer_card_frame, deck))
			dealer_score = score_hand(dealer_hand)
			dealer_score_label.set(dealer_score)						# updating the dealer tkinter frame

		# here the order of the tests is very important
		player_score = score_hand(player_hand)
		if player_score > 21:
			result_text.set("Dealer wins!")
			end_game = True
			enable_restart()
		elif dealer_score > 21 or dealer_score < player_score:
			result_text.set("Player wins!")
			end_game = True
			enable_restart()
		elif dealer_score > player_score:
			result_text.set("Dealer wins!")
			end_game = True
			enable_restart()
		else:
			result_text.set("Draw!")
			end_game = True
			enable_restart()


def deal_player():
	global end_game
	if not end_game:
		player_hand.append(deal_card(player_card_frame, deck))
		player_score = score_hand(player_hand)
		player_score_label.set(player_score)

		if player_score > 21:
			result_text.set("Dealer wins!")
			end_game = True
			enable_restart()


def shuffle():
	random.shuffle(deck)


def new_game():
	global end_game
	global dealer_card_frame
	global player_card_frame
	global deck
	global dealer_hand
	global player_hand

	end_game = False
	result_text.set("New Game")

	if restart_button:
		restart_button.destroy()

	if dealer_card_frame:
		dealer_card_frame.destroy()
	dealer_card_frame = tkinter.Frame(card_frame, background='green')
	dealer_card_frame.grid(row=0, column=1, sticky='ew', rowspan=2)

	if player_card_frame:
		player_card_frame.destroy()
	player_card_frame = tkinter.Frame(card_frame, background='green')
	player_card_frame.grid(row=2, column=1, sticky='ew', rowspan=2)

	new_cards = []
	load_cards(new_cards)
	deck = list(new_cards)
	shuffle()

	dealer_hand = []
	player_hand = []

	deal_player()
	dealer_hand.append(deal_card(dealer_card_frame, deck))
	dealer_score_label.set(score_hand(dealer_hand))
	deal_player()
	player_score_label.set(score_hand(player_hand))


def enable_restart():
	global restart_button
	restart_button = tkinter.Button(button_frame, text="Restart", command=new_game)
	restart_button.grid(row=0, column=3)


# setting up the screen and frames for the game with tkinter module
mainWindow = tkinter.Tk()
mainWindow.title("Blackjack Game")
mainWindow.geometry('640x480')
mainWindow.configure(background='green')

result_text = tkinter.StringVar()								# a variable string
result_text.set("New Game")
result = tkinter.Label(mainWindow, textvariable=result_text)
result.grid(row=0, column=0, columnspan=3)

card_frame = tkinter.Frame(mainWindow, relief='sunken', borderwidth=1, background='green')
card_frame.grid(row=1, column=0, sticky='ew', rowspan=2, columnspan=3)

dealer_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Dealer", background='green', fg='white').grid(row=0, column=0)
tkinter.Label(card_frame, textvariable=dealer_score_label, background='green', fg='white').grid(row=1, column=0)

player_score_label = tkinter.IntVar()
tkinter.Label(card_frame, text="Player", background='green', fg='white').grid(row=2, column=0)
tkinter.Label(card_frame, textvariable=player_score_label, background='green', fg='white').grid(row=3, column=0)

button_frame = tkinter.Frame(mainWindow)
button_frame.grid(row=3, column=0, sticky='w', columnspan=3)

dealer_button = tkinter.Button(button_frame, text="Deal Dealer", command=deal_dealer)
dealer_button.grid(row=0, column=0)
player_button = tkinter.Button(button_frame, text="Deal Player", command=deal_player)
player_button.grid(row=0, column=1)
shuffle_button = tkinter.Button(button_frame, text="Shuffle", command=shuffle)
shuffle_button.grid(row=0, column=2)
quit_button = tkinter.Button(button_frame, text="Quit", command=mainWindow.destroy)
quit_button.grid(row=0, column=4)

dealer_card_frame = False
player_card_frame = False
end_game = False
restart_button = False

new_game()
mainWindow.mainloop()

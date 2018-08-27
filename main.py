#-------GLOBAL VARIABLES---------
players = []
found_dealer = False
no_of_players = 0
card_pack = ('A',2,3,4,5,6,7,8,9,10,'J','Q','K','A',2,3,4,5,6,7,8,9,10,'J','Q','K'\
			,'A',2,3,4,5,6,7,8,9,10,'J','Q','K','A',2,3,4,5,6,7,8,9,10,'J','Q','K')
cp = list(card_pack)
budget_of_game = 0
from display import display_board
import random
from calls import take_a_call
from pc_checks import checks_prior_taking_calls

class player(object):
	def __init__(self):
		self.isdealer = False
		self.name = "None "
		self.budget = 0
		self.bet_amount = 0
		self.main_hand = [None,None,None,None,None]
		self.split_hand = [None,None,None,None,None]
		self.split_opted = False
		self.insurance = 0
		self.hand_total = 0
		self.no_of_cards = 0
		self.bj_exist = False
		self.ttu = False

dealer = player()

def get_player_details(arg):
	global players
	global found_dealer
	print("Player-{x} : Please enter your name in less than 10 chars".format(x=arg+1))
	players[arg].name = input().upper()
	while True:
		if (len(players[arg].name)<20) and (len(players[arg].name)>0):
			if players[arg].name.isalpha() or players[arg].name.isalnum():
				break
			else:
				print('Incorrect input ! Name should not contain special chars! It can be either alphabetic or alphanumeric only.')			
				players[arg].name = input().upper()
		else:
			print("Length of name outside permissible limits!")
			print("Player-{x} : Please enter your name in less than 10 and more than 0 chars".format(x=arg+1))
			players[arg].name = input().upper()
	if (arg==no_of_players-1) and not found_dealer:
		print("You are the DEALER for the game!")
		players[arg].isdealer = True
	elif not found_dealer:
		print("You wanna play as dealer? Say 'yes' or 'no'")
		resp = input()
		while True:
			if resp.isalpha() and resp.lower().startswith('y') and (resp.lower().count('n')==0):
				players[arg].isdealer = True
				found_dealer = True
				break
			elif resp.isalpha() and resp.lower().startswith('n') and (resp.lower().count('y')==0):
				players[arg].isdealer = False
				break
			else:
				print("Either your input contains numbers OR the input is ambiguous!!")
				resp = input()
	players[arg].is_active = True

def decide_budget():
	global players
	global budget_of_game
	print("Please decide the budget for the game. It can be between 1 to 1000.")
	budget_of_game = input()
	while True:
		if budget_of_game.isnumeric() and int(budget_of_game) in range(1,1001):
			budget_of_game = int(budget_of_game)
			break
		else:
			print("Please provide a budget from 1 to 1000")
			budget_of_game = input()
	for i in range(0,no_of_players):
		players[i].budget = budget_of_game

def distribute_cards():
	global cp
	global players
	global dealer
	global no_of_players
	card_left = cp.__len__()
	print('Cards left in deck : {x}'.format(x=card_left))
	for player in players:
		if (player.budget>0) or (player.bet_amount>0):
			for j in [0,1]:
				try:
					rand_card = random.choice(cp)
				except:
					cp = list(card_pack)
					rand_card = random.choice(cp)
					print("Card Deck is recreated")
				finally:
					player.main_hand[j] = str(rand_card)
					cp.remove(rand_card)
					player.no_of_cards = 2
	for j in [0,1]:
		try:
			rand_card = random.choice(cp)
		except:
			cp = list(card_pack)
			rand_card = random.choice(cp)
			print("Card Deck is recreated")
		finally:
			dealer.main_hand[j] = str(rand_card)
			cp.remove(rand_card)
			dealer.no_of_cards = 2

def place_bet():
	for player in players:
		if (player.budget>0):
			print("{Name}: How much you want to bet?".format(Name=player.name))
			player.bet_amount = input()
			while True:
				if player.bet_amount.isnumeric() and int(player.bet_amount) in range(1,int(player.budget+1)):
					player.bet_amount = int(player.bet_amount)
					player.budget -= player.bet_amount
					break
				else:
					print("Incorrect bet amount!")
					player.bet_amount = input()

def results():
	global dealer
	global players
	if (dealer.hand_total>21):
		for player in players:
			if (player.no_of_cards!=5):
				if (player.hand_total<=21):
					if (not player.bj_exist):
						print('Dealer is busted!! {pl}: You Won the bet. Congratulations !!!!'.format(pl=player.name))
						player.budget += (player.bet_amount * 2)
						dealer.budget -= (player.bet_amount)
				else:
					print('{pl} : You both busted !! But since you busted first, You Lost the bet. Alas!!!!'.format(pl=player.name))
		prepare_for_next_round()
	else:
		if not dealer.bj_exist:
			for player in players:
				if (player.no_of_cards!=5):
					if (player.hand_total<=21) and (player.no_of_cards!=5):
						if not player.bj_exist:
							if (dealer.hand_total < player.hand_total):
								print('{pl}: You Won the bet. Congratulations !!!!'.format(pl=player.name))
								player.budget += (player.bet_amount * 2)
								dealer.budget -= (player.bet_amount)
							elif (dealer.hand_total == player.hand_total):
								print("{pl}: It's a push for you. Nobody wins.".format(pl=player.name))
								player.budget += (player.bet_amount)
							else:
								print("{pl}: Dealer won the bet".format(pl = player.name))
								dealer.budget += (player.bet_amount)
					else:
						print("{pl}: Dealer won the bet".format(pl = player.name))
						dealer.budget += (player.bet_amount)
		prepare_for_next_round()
	display_board(dealer, players, no_of_players)

def prepare_for_next_round():
	global players
	global no_of_players
	global dealer
	for player in players:
		player.bet_amount = 0
		player.main_hand = [None,None,None,None,None]
		player.split_hand = [None,None,None,None,None]
		player.split_opted = False
		player.insurance = 0
		player.hand_total = 0
		player.no_of_cards = 0
		player.bj_exist = False
		dealer.main_hand = [None,None,None,None,None]
		dealer.hand_total = 0
		dealer.no_of_cards = 0
		dealer.bj_exist = False
		dealer.ttu = False
	display_board(dealer, players, no_of_players)
	
def filter_the_dealer():
	global dealer
	global players
	global no_of_players
	for player in players:
		if player.isdealer:
			dealer = player
			players.remove(player)

print("Lets play the game of Blackjack!!")
print("Min 2 and Max 5 players can play the game. Please provide your count :")
# DECIDE HOW MANY PLAYERS WANT TO PLAY THE GAME
no_of_players = input()

while True:
        if no_of_players.isnumeric() and int(no_of_players) in range(2,6):
                no_of_players = int(no_of_players)
                break
        else:
                print("Please provide a count from 2 to 5")
                no_of_players = input()


# CREATE PLAYERS - KNOW THEIR NAMES
for i in range(0,no_of_players):
	players.append(player())
	get_player_details(i)

# DECIDE BUDGET FOR EACH PLAYER
decide_budget()
# LET US TAKE OUT THE DEALER FROM PLAYERS
filter_the_dealer()

print("GAME BEGINS !!!")
while (dealer.budget in range(1,(no_of_players*budget_of_game))):
	# TAKE THE BET AMOUNT
	place_bet()
	# DISTRIBUTE FIRST ROUND OF 2 CARDS TO EACH PLAYER
	distribute_cards()
	display_board(dealer, players, no_of_players)
	# PERFORM CHECKS PRIOR TAKING CALLS FROM PLAYERS
	dealer, players, no_of_players = checks_prior_taking_calls(dealer, players, no_of_players)
	
	# TIME TO TAKE A CALL FROM EACH PLAYER
	if not dealer.bj_exist:
		for player in players:
			if (not player.isdealer and not player.bj_exist and ((player.budget>0) or (player.bet_amount>0))):
				call,cp,player = take_a_call(player, cp, dealer, players, no_of_players)
				display_board(dealer, players, no_of_players)
				while ((player.hand_total <= 21) and (call is not 'STAND') and (call is not 'DOUBLE') and (player.no_of_cards<5)):
					call,cp,player = take_a_call(player, cp, dealer, players, no_of_players)
					display_board(dealer, players, no_of_players)
					# ensure that at the time of 2nd call 'split' and 'double' calls are disabled
				if (player.hand_total > 21):
					dealer.budget += (player.bet_amount)
					player.bet_amount = 0
					display_board(dealer, players, no_of_players)
					print('Wrong choice !! You busted !!')
				elif (player.no_of_cards==5):
					player.budget += (player.bet_amount*2)
					dealer.budget -= (player.bet_amount)
					player.bet_amount = 0
					display_board(dealer, players, no_of_players)
					print('{name} : CONGRATS!! You win!! You survived 5 hits without bursting.'.format(name=player.name))
				else:
					pass # Player chooses to stand

		dealer.ttu = True #time to uncover 2nd card of dealer
		display_board(dealer, players, no_of_players)
		# reduce no_of_player , make a new players array which has 1 less num of players. if no of players is zero. dealer wins
		call,cp,dealer = take_a_call(dealer, cp, dealer, players, no_of_players)
		display_board(dealer, players, no_of_players)
		while ((dealer.hand_total <= 21) and call is not 'STAND'):
			#instead of 21 above, keeping max of any players hand_total would be good.
			call,cp,dealer = take_a_call(dealer, cp, dealer, players, no_of_players)
			display_board(dealer, players, no_of_players)
	
	# AFTER ALL HAVE PLACED THEIR CALLS. IT'S TIME FOR RESULTS
	results()


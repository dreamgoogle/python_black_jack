import random
from tkinter import messagebox
from display import display_board

card_pack = ('A',2,3,4,5,6,7,8,9,10,'J','Q','K','A',2,3,4,5,6,7,8,9,10,'J','Q','K'\
			,'A',2,3,4,5,6,7,8,9,10,'J','Q','K','A',2,3,4,5,6,7,8,9,10,'J','Q','K')

def min_hand_total(player, call, dealer, players, no_of_players):
	sum = 0
	a_present = False
	for i in range(0,5):
		if player.main_hand[i] is not None:
			if player.main_hand[i] is not 'A':
				if (player.main_hand[i] is 'J') or (player.main_hand[i] is 'Q') or (player.main_hand[i] is 'K'):
					sum = sum + 10
				else:
					sum = sum + int(player.main_hand[i])
			else:
				a_present = True
	if a_present:
		if (player.no_of_cards!=2):
			for i in range(0,5):
				if player.main_hand[i] is 'A':
					if ((sum+11)>21):
						sum += 1
					else:
						print('{name} : Check the pop-up message box!'.format(name=player.name))
						is_eleven = messagebox.askyesno('Value of A', 'Is it 11 ?')
						if is_eleven:
							sum += 11
						else:
							sum += 1
		else:
			if (call == 'STAND'):
				sum += 11
			else:
				sum += 1
	player.hand_total = sum
	return player
					
def hit(player, cp, call, dealer, players, no_of_players):
	global card_pack
	try:
		new_card = random.choice(cp)
	except:
		cp = list(card_pack)
		new_card = random.choice(cp)
		print("Card Deck is recreated")
	finally:
		player.main_hand[player.no_of_cards] = str(new_card)
		player.no_of_cards += 1
		display_board(dealer, players, no_of_players)
		min_hand_total(player, call, dealer, players, no_of_players)
		cp.remove(new_card)
	return player,cp
	
def stand(player, cp, call, dealer, players, no_of_players):
	player = min_hand_total(player, call, dealer, players, no_of_players)
	return player,cp
	
def split(player, cp, call):
	return player,cp
	
def double(player, cp, call, dealer, players, no_of_players):
	print('You can again bet any amount not exceeding your previous bet amount within your budget.')
	print('Bet amount : ')
	while True:
		bet_amt = input()
		if (bet_amt.isnumeric() and (int(bet_amt)<=player.budget)):
			player.bet_amount += int(bet_amt)
			player.budget -= int(bet_amt)
			player,cp = hit(player, cp, call, dealer, players, no_of_players)
			break
		else:
			print('Invalid amount! Please check your budget!')
	return player,cp

def take_a_call(player, cp, dealer, players, no_of_players):
	call = 'dummy'
	player = min_hand_total(player, call, dealer, players, no_of_players)
	if (player.no_of_cards==2):
		print("{name}: Please make a call: HIT(H)   or   STAND(S)   or   SPLIT(SP)   or   DOUBLE(D)".format(name=player.name))
	else:
		print("{name}: Please make a call: HIT(H)   or   STAND(S)".format(name=player.name))
	while True:
		call = input()
		if call.isalpha() and (len(call)<10):
			if call.upper().startswith('H'):
				print('You chose HIT')
				call = 'HIT'
				player, cp = hit(player, cp, call, dealer, players, no_of_players)
				break
			elif call.upper().startswith('SP'):
				print('You chose SPLIT')
				call = 'SPLIT'
				is_valid = validate_the_call(player, call)
				if is_valid:
					player, cp = split(player, cp, call)
					break
			elif call.upper().startswith('S'):
				print('You chose STAND')
				call = 'STAND'
				player, cp = stand(player, cp, call, dealer, players, no_of_players)
				break
			elif call.upper().startswith('D'):
				print('You chose DOUBLE')
				call = 'DOUBLE'
				is_valid = validate_the_call(player, call)
				if is_valid:
					player, cp = double(player, cp, call, dealer, players, no_of_players)
					break
			else:
				print('Incorrect/Ambiguous Input.')
		else:
			print('Incorrect Input')
	return call,cp,player
	
def validate_the_call(player, call):
	ret = True
	if player.isdealer:
		print('HaHaHaHa !! Dealer does not have option to choose DOUBLE or SPLIT')
		ret = False
	else:
		if (player.no_of_cards!=2):
			print('You are not allowed to make this choice at this stage. Make a different call!')
			print("{name}: Please make a call: HIT(H)   or   STAND(S)".format(name=player.name))
			ret = False
		elif (call is 'DOUBLE' and (player.hand_total not in range(9,12))):
			print('You are not eligible to choose DOUBLE. Hand total not in range 9-11!')
			ret = False
		elif (call is 'SPLIT' and (player.main_hand[0] != player.main_hand[1])):
			print('You are not eligible to choose SPLIT. Both cards should be identical!')
			ret = False
		else:
			pass
	return ret


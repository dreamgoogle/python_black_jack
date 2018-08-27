def print_dealer_board(dealer, no_of_players):
	c = []
	for j in dealer.main_hand:
		if j is None:
			c.append("   ")
		elif (j == '10'):
			c.append(' 10')
		else:
			c.append(' '+j+' ')
	if not dealer.ttu:
		c[1] = "   "
	empty_space = "            "
	print(empty_space*(no_of_players-2)+"-------------------------")
	print(empty_space*(no_of_players-2)+"| DEALER BOARD          |")
	print(empty_space*(no_of_players-2)+"|  ___ ___ ___ ___ ___  |")
	print(empty_space*(no_of_players-2)+"| |   |   |   |   |   | |")
	print(empty_space*(no_of_players-2)+"| |{x}|{y}|{z}|{w}|{v}| |".format(x=c[0],y=c[1],z=c[2],w=c[3],v=c[4]))
	print(empty_space*(no_of_players-2)+"| |___|___|___|___|___| |")
	final1,final2 = '',''
	print(empty_space*(no_of_players-2)+'| '+ (dealer.name.upper().ljust(21)) + ' | ')
	print(empty_space*(no_of_players-2)+'| '+ 'Budget = {ba}'.format(ba = dealer.budget).ljust(21) + ' | ')
	print(empty_space*(no_of_players-2)+"|                       |")
	print(empty_space*(no_of_players-2)+"-------------------------")

def print_insurance_panel(players, no_of_players):
	final = ""
	print('-'*24*(no_of_players-1))
	for player in players:
		if not player.isdealer:
			final = final + 'Insurance = {x}'.format(x=player.insurance).ljust(21) + ' | '
	print('| '+ final)
	print('-'*24*(no_of_players-1))

def print_player_box(players, no_of_players):
	a = '------------------------'
	b = '                       |'
	c = '  ___ ___ ___ ___ ___  |'
	d = ' |   |   |   |   |   | |'
	e = ' |___|___|___|___|___| |'
	final = ""
	print("-"+a*(no_of_players-1))
	print("|"+b*(no_of_players-1))
	print("|"+c*(no_of_players-1))
	print("|"+d*(no_of_players-1))
	final = ""
	for player in players:
		ca = []
		for j in player.main_hand:
			if j is None:
				ca.append("   ")
			elif (j == '10'):
				ca.append(' 10')
			else:
				ca.append(' '+j+' ')
		final = final + "|{x}|{y}|{z}|{w}|{v}| | ".format(x=ca[0],y=ca[1],z=ca[2],w=ca[3],v=ca[4])
	print('| '+ final)
	print("|"+e*(no_of_players-1))
	final1,final2,final3,final4 = "",'','',''
	for player in players:
		final1 = final1 + (player.name.upper().ljust(21)) + ' | '
		final2 = final2 + 'Bet amount = {ba}'.format(ba = player.bet_amount).ljust(21) + ' | '
		final3 = final3 + 'Budget = {ba}'.format(ba = player.budget).ljust(21) + ' | '
		final4 = final4 + 'Hand Total = {ba}'.format(ba = player.hand_total).ljust(21) + ' | '
	print('| '+ final1)
	print('| '+ final2)
	print('| '+ final3)
	print('| '+ final4)
	print("|"+b*(no_of_players-1))
	print("-"+a*(no_of_players-1))

def display_board(dealer, players, no_of_players):
	print_dealer_board(dealer, no_of_players)
	print_insurance_panel(players, no_of_players)
	print_player_box(players, no_of_players)

qipans = {}

def init_qipans(player1,player2):
	qipan = {'black':player1,'white':player2,'record':{'black':[],'white':[]},'now':'black'}
	qipans[(player1,player2)] = qipan

def try_play(player1,player2,player,xy):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	print(pair)
	print(pair in qipans)
	if pair not in qipans:
		return "-1"

	color = 'white'
	if qipans[pair]['black'] == player:
		color = 'black'

	if qipans[pair]['now'] == color:
		qipans[pair]['record'][color].append(xy)
		if color == 'white':
			qipans[pair]['now'] = 'black'
		else:
			qipans[pair]['now'] = 'white'
		return "1"
	else:
		return "0"

def end_play(player1,player2):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	if pair in qipans:
		qipans.pop(pair)
	return "1"

def get_color(player1,player2,p):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	if pair not in qipans:
		return ''
	else:
		if qipans[pair]['black'] == p:
			return 'black'
		else:
			return 'white'

def get_players(s):
	u = ''
	p = ''
	try:
		u = s['username']
		p = s['play']
	except:
		pass
	return u,p
def get_new_play(player1,player2,player):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	if pair not in qipans:
		return "-2"

	color = 'white'
	anti_color = 'black'
	if qipans[pair]['black'] == player:
		color = 'black'
		anti_color = 'white'

	if qipans[pair]['now'] == anti_color:
		return "-1"
	elif len(qipans[pair]['record'][anti_color]) == 0:
		return ""
	else:
		return str(qipans[pair]['record'][anti_color][-1])

def get_all_play(player1,player2,c):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	if pair not in qipans:
		return "-2"

	return str(qipans[pair]['record'][c]).replace('[','').replace(']','')



def get_now_color(player1,player2,p):
	pair = (player1,player2)
	if pair not in qipans:
		pair = (player2,player1)
	if pair not in qipans:
		return ''
	else:
		return qipans[pair]['now']
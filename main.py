from flask import Flask,request,render_template,session,redirect,url_for
from sqldb import *
from wuziqi import *
# from datetime import timedelta

now_user = []
player_user = []
now_play = []

app=Flask("__name__")
app.config['SECRET_KEY'] = '123456'
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)



# 注册
@app.route("/signin")
def signin_index():
	return app.send_static_file("signin.html")

@app.route("/CheckUserID",methods = ("POST",))
def checkPrime():
	netname = request.form['username'].strip()
	check_rst = search_user(netname)
	if len(check_rst) == 0:
		return "1"
	else:
		return "0"

@app.route("/Register",methods = ("POST",))
def webRegister():
	netname = request.form['username'].strip()
	pwd1 = request.form['pwd1']
	pwd2 = request.form['pwd2']
	if pwd1 != pwd2:
		statusMsg = "两次密码不一致<br><a href='/signin'>重新注册</a>"
	elif len(search_user(netname)) != 0:
		statusMsg = "用户名已注册<br><a href='/signin'>重新注册</a><br><a href='/login'>登录</a>"
	else:
		create_user(str(netname),str(pwd1))
		statusMsg = "注册成功<br><a href='/signin'>重新注册</a><br><a href='/login'>登录</a><br>"
		# statusMsg += str(showalldata())

	return render_template("msg.html",registerMsg = statusMsg)

# 登录
@app.route("/login")
def login_index():
	return app.send_static_file("login.html")

@app.route("/Login",methods = ("POST",))
def webLogin():
	netname = request.form['username'].strip()
	pwd1 = request.form['pwd1']
	login_rst = login_user(netname,pwd1)
	if login_rst[0]:
		session['username'] = login_rst[1]
		if session['username'] not in now_user:
			now_user.append(session['username'])
		else:
			statusMsg = "用户已登陆<br><a href='/signin'>注册</a><br><a href='/login'>重新登录</a><br>"
			session.pop('username', None)
			return render_template("msg.html",registerMsg = statusMsg)
		return redirect("/play")
	elif login_rst[1] == None:
		statusMsg = "用户不存在<br><a href='/signin'>注册</a><br><a href='/login'>重新登录</a><br>"
	else:
		statusMsg = "密码错误<br><a href='/signin'>注册</a><br><a href='/login'>重新登录</a><br>"

	return render_template("msg.html",registerMsg = statusMsg)


@app.route("/play")
def play_index():
	user = ''
	if 'username' in session:
		user = session['username']
	else:
		user = '游客'
		statusMsg = "尚未登录<br><a href='/signin'>注册</a><br><a href='/login'>登录</a><br>"
		return render_template("msg.html",registerMsg = statusMsg)

	statusMsg = "登陆成功<br>欢迎回来，" + str(user) +"<br>"

	playMsg = '''
	<a href="/findPlayer">开始匹配<a>
	'''
	if 'play' in session:
		statusMsg += ("对手:" + session['play'])
		playMsg = ''



	print(session)

	return render_template("play.html",registerMsg = statusMsg,pendingjs = '',startFindPlayer = playMsg)

@app.route('/logout')
def logout():
	if session['username'] in now_user:
		now_user.remove(session['username'])
	if session['username'] in player_user:
		player_user.remove(session['username'])
	plays = [e for e in now_play if e[1] == session['username']] + [e for e in now_play if e[0] == session['username']]
	for e in plays:
		try:
			end_play(e[0],e[1])
			now_play.remove(e)
		except:
			pass
	# session.pop('username', None)
	session.clear()


	return redirect(url_for("play_index"))#此处修改

@app.route('/getNowUser')
def getNowUser():
	return str(len(now_user))


@app.route('/getPair')
def getPair():
	if session['username'] not in player_user:
		plays = [e[0] for e in now_play if e[1] == session['username']] + [e[1] for e in now_play if e[0] == session['username']]
		other = plays[0]
		session['play'] = other
		return other
	else:
		return ""



@app.route('/findPlayer')
def findPlayer():
	if len(player_user) == 0:
		player_user.append(session['username'])
		statusMsg = statusMsg = "登陆成功<br>欢迎回来，" + session['username'] +"<br>"
		pendingjs = '''
		<script type="text/javascript">

		function getPlayer(){
			$.get("/getPair",function(rtnFromSvr){
				if (rtnFromSvr.length == 0)
					$("#pending").html("正在匹配...");
				else
					window.location.replace("/chessPlay")
				// $("#nowUser").html("当前在线人数：" + rtnFromSvr);
				console.log(rtnFromSvr);
			});
		}
		setInterval("getPlayer()",1000);
		</script>
		'''
		return render_template("play.html",registerMsg = statusMsg,pendingjs = pendingjs)
	else:
		player = player_user.pop()
		now_play.append((player,session['username']))
		session['play'] = player
		init_qipans(player,session['username'])

		return redirect(url_for("chessPlay"))


@app.route('/chessPlay')
def chessPlay():
	u,p = get_players(session)
	color = get_color(u,p,u)
	if color == 'black':
		color_msg = '执黑先下'
	elif color == 'white':
		color_msg = '执白后下'
	else:
		color_msg = '网络故障'
	return render_template("wuzi.html",msg = "对手：" + p + "<br>" + color_msg)

@app.route('/getColor')
def getColor():
	u,p =get_players(session)
	return get_color(u,p,u)

@app.route('/play_chess')
def play_chess():
	xy = request.args['xy']
	print(xy)
	print(qipans)
	u,p =get_players(session)
	rst = try_play(u,p,u,xy)
	return rst

@app.route('/get_chess')
def get_chess():
	u,p =get_players(session)
	return get_new_play(u,p,u)

@app.route('/get_all_black_chess')
def get_all_black_chess():
	u,p = get_players(session)
	return get_all_play(u,p,'black')

@app.route('/get_all_white_chess')
def get_all_white_chess():
	u,p = get_players(session)
	return get_all_play(u,p,'white')


@app.route('/end_chess')
def end_chess():
	# u,p = get_players(session)
	plays = [e for e in now_play if e[1] == session['username']] + [e for e in now_play if e[0] == session['username']]
	for e in plays:
		try:
			end_play(e[0],e[1])
			now_play.remove(e)
		except:
			pass
	if 'play' in session:
		session.pop('play', None)
	return '1'


@app.route('/')
def root_web():
	return redirect('/login')

@app.route('/CheckTurn')
def CheckTurn():
	print("debug")
	u,p =get_players(session)
	color = get_now_color(u,p,u)
	msg = ''
	if color == '':
		return ''
	elif color == 'black':
		msg += '当前：黑色'

	else:
		msg += '当前：白色'

	if color == get_color(u,p,u):
		msg += '<br>轮到你了'
	else:
		msg += '<br>请等待对手'

	return msg



if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.run(debug=True)



#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver
To run locally
    python server.py
Go to http://localhost:8111 in your browser
A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
from sqlalchemy import *
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response, url_for, flash
import terms
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PlayerCompForm, TeamCompForm, FavPlayerCompForm, FavTeamCompForm, PlayerInfoForm, TeamInfoForm, MatchForm
from flask_login import LoginManager, login_user, UserMixin, current_user, logout_user, login_required

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

login_manager = LoginManager(app)

# Set up for the class database

DB_USER = "yk2805"
DB_PASSWORD = "j25CnkRB8F"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"



# This line creates a database engine that knows how to connect to the URI above

engine = create_engine(DATABASEURI)


# Here we create a test table and insert some values in it
engine.execute("""DROP TABLE IF EXISTS test;""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
engine.execute("""INSERT INTO test(name) VALUES ('grace hopper'), ('alan turing'), ('ada lovelace');""")


@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request
  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

app.config['SECRET_KEY'] = 'df46583764fe4ce75e0ea7cc58dd2cc7'

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():

  # DEBUG: this is debugging code to see what request looks like
  print request.args



  cursor = g.conn.execute("""SELECT fullname, ppg 
                             FROM player 
                             ORDER BY ppg DESC
                             LIMIT 5;""")
  
  p_ppg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT fullname, rpg 
                             FROM player 
                             ORDER BY rpg DESC
                             LIMIT 5;""")
  
  p_rpg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT fullname, apg 
                             FROM player 
                             ORDER BY apg DESC
                             LIMIT 5;""")
  
  p_apg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT fullname, bpg 
                             FROM player 
                             ORDER BY bpg DESC
                             LIMIT 5;""")
  
  p_bpg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT fullname, spg 
                             FROM player 
                             ORDER BY spg DESC
                             LIMIT 5;""")
  
  p_spg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT fullname, topg 
                             FROM player 
                             ORDER BY topg DESC
                             LIMIT 5;""")
  
  p_tpg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, ptsgm 
                             FROM team 
                             ORDER BY ptsgm DESC
                             LIMIT 5;""")
  
  t_ppg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, aptsgm 
                             FROM team 
                             ORDER BY aptsgm DESC
                             LIMIT 5;""")
  
  t_appg = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, ptsdiff 
                             FROM team 
                             ORDER BY ptsdiff DESC
                             LIMIT 5;""")
  
  t_ptsdiff = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, oeff 
                             FROM team 
                             ORDER BY oeff DESC
                             LIMIT 5;""")
  
  t_oeff = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, deff 
                             FROM team 
                             ORDER BY deff DESC
                             LIMIT 5;""")
  
  t_deff = [(res[0], res[1]) for res in cursor]

  cursor = g.conn.execute("""SELECT team, pace 
                             FROM team 
                             ORDER BY pace DESC
                             LIMIT 5;""")
  
  t_pace = [(res[0], res[1]) for res in cursor]


  cursor.close()

  context = dict(p_ppg = p_ppg,
                 p_rpg = p_rpg,
                 p_apg = p_apg,
                 p_bpg = p_bpg,
                 p_spg = p_spg,
                 p_tpg = p_tpg,
                 t_ppg = t_ppg,
                 t_appg = t_appg,
                 t_ptsdiff = t_ptsdiff,
                 t_oeff = t_oeff,
                 t_deff = t_deff,
                 t_pace = t_pace,)

  return render_template("index.html", **context)

def player_info_request(pid, attr_show=None):
  # attributes to select in database query
  attr_select = ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', 'team']

  attr_select_str = ", ".join(["P."+x for x in attr_select[:-1]])

  attr_show_default = ['gp', 'mpg', 'ppg', 'rpg', 'apg', 'topg', 'usg', 'p2', 'pa2', 'p3', 'pa3', 'ft', 'fta', 'spg', 'bpg', 'ortg', 'drtg', 'trb', 'vi', 'tor']

  if attr_show is None:
    attr_show = attr_show_default

  cmd = """
        SELECT P.pid, P.fullname, P.pos, P.age, P.gp, P.mpg, P.min, P.usg, P.tor, P.fta, P.ft, P.pa2, P.p2, P.pa3, P.p3, P.efg, P.ts, P.ppg, P.rpg, P.trb, P.apg, P.ast, P.spg, P.bpg, P.topg, P.vi, P.ortg, P.drtg, T.team
        FROM player as P, team as T 
        WHERE P.tid = T.tid AND P.pid = %s
        LIMIT 1;
        """

  cursor = g.conn.execute(cmd, pid)

  result_dict = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor.close()

  # general_attr = ['team', 'fullname', 'age', 'pos']
  
  data_show = [result_dict[x] for x in attr_show]
  data_show_des = [terms.attr_des[x].title() for x in attr_show]

  
  data = zip(attr_show, data_show_des, data_show)
  p_team = result_dict['team']
  p_fullname = result_dict['fullname'].title()
  p_pos = result_dict['pos'].upper()
  p_age = str(result_dict['age']) + ' Year Old'
  title = "Player Stats"

  context = dict(data=data, p_team=p_team, p_fullname=p_fullname, p_pos=p_pos, p_age=p_age, title=title)
  
  return context

@app.route('/players', methods=['POST', 'GET'])
def player_info():

  form = PlayerInfoForm()

  if form.validate_on_submit():
    pid = form.player.data
    context = player_info_request(pid)
    return render_template("players.html", **context)

  return render_template("player_request.html", form=form)

def team_info_request(tid, attr_show=None):
  # attributes to select in database query
  attr_select = ['tid', 'team', 'conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

  attr_select_str = ", ".join(attr_select)

  attr_show_default = ['gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

  if attr_show is None:
    attr_show = attr_show_default

  cmd = """
          SELECT tid, team, conf, division, gp, ptsgm, aptsgm, ptsdiff, pace, oeff, deff, ediff, sos, rsos, sar, cons, a4f, w, l, win, ewin, pwin, ach, strk 
          FROM team
          WHERE tid = %s
          LIMIT 1;
          """

  cursor = g.conn.execute(cmd, tid)
  result = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor.close()

  
  data = zip([terms.attr_des[x] for x in attr_show], attr_show, [result[x] for x in attr_show])
    
  t_team = result['team']
  t_conf = result['conf']
  t_division = result['division']
  title = "Team Stats"

  context = dict(data=data, t_team=t_team, t_conf=t_conf, t_division=t_division, title=title)
  
  return context

@app.route('/teams', methods=['POST', 'GET'])
def team_info():
  form = TeamInfoForm()
  if form.validate_on_submit():
    tid = form.team.data
    context = team_info_request(tid)

    return render_template("teams.html", **context)

  return render_template("teams_request.html", form=form)


def player_comp(pid1, pid2, attr_show=None):
  # attributes to select in the query
  attr_select = ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', 'team']
  attr_select_str = ", ".join(['P.' + x for x in attr_select[:-1]])

  attr_show_default = ['team', 'pos', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', ]

  if attr_show is None:
    attr_show = attr_show_default

  cmd = """
        SELECT P.pid, P.fullname, P.pos, P.age, P.gp, P.mpg, P.min, P.usg, P.tor, P.fta, P.ft, P.pa2, P.p2, P.pa3, P.p3, P.efg, P.ts, P.ppg, P.rpg, P.trb, P.apg, P.ast, P.spg, P.bpg, P.topg, P.vi, P.ortg, P.drtg, T.team
        FROM player as P, team as T 
        WHERE P.tid = T.tid AND P.pid = %s
        LIMIT 1;
        """
  
  cursor = g.conn.execute(cmd, pid1)
  result_dict1 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor = g.conn.execute(cmd, pid2)
  result_dict2 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor.close()

  player_name_1 = result_dict1['fullname']
  player_name_2 = result_dict2['fullname']

  attr_show_des = [terms.attr_des[x] for x in attr_show]
  data = zip([result_dict1[x] for x in attr_show], attr_show_des, attr_show, [result_dict2[x] for x in attr_show])

  return data, player_name_1, player_name_2

@app.route("/comparing_players", methods=['POST', 'GET'])
def comparing_players():
  form = PlayerCompForm()
  if form.validate_on_submit():
    pid1 = form.player1.data
    pid2 = form.player2.data

    data, player_name_1, player_name_2 = player_comp(pid1, pid2)
    return render_template("players_comp.html", data=data, player_name_1=player_name_1, player_name_2=player_name_2)

  return render_template("player_comp_request.html", form=form)

def team_comp(tid1, tid2, attr_show=None):
  # attributes to select in database query
  attr_select = ['tid', 'team', 'conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

  attr_select_str = ", ".join(attr_select)

  attr_show_default = ['conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

  if attr_show is None:
    attr_show = attr_show_default

  cmd = """
        SELECT tid, team, conf, division, gp, ptsgm, aptsgm, ptsdiff, pace, oeff, deff, ediff, sos, rsos, sar, cons, a4f, w, l, win, ewin, pwin, ach, strk 
        FROM team
        WHERE tid = %s
        LIMIT 1;
        """
  cursor = g.conn.execute(cmd, tid1)

  result1 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}

  cursor = g.conn.execute(cmd, tid2)

  result2 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor.close()

  attr_des = [terms.attr_des[x] for x in attr_show]
  data = zip([result1[x] for x in attr_show], attr_des, attr_show, [result2[x] for x in attr_show])

  team_name_1 = result1['team']
  team_name_2 = result2['team']

  return data, team_name_1, team_name_2

@app.route("/comparing_teams", methods=['POST', 'GET'])
def comparing_teams():
  form = TeamCompForm()

  if form.validate_on_submit():
    tid1 = form.team1.data
    tid2 = form.team2.data

    data, team_name_1, team_name_2 = team_comp(tid1, tid2)
    return render_template("teams_comp.html", data=data, team_name_1 = team_name_1, team_name_2=team_name_2)

  return render_template("team_comp_request.html", form=form, title="Comparing Teams")

def match_request(tid1, tid2):

  cursor = g.conn.execute("SELECT team FROM team WHERE tid = %s;", tid1)
  tname1 = cursor.fetchone()[0]
  cursor = g.conn.execute("SELECT team FROM team WHERE tid = %s;", tid2)
  tname2 = cursor.fetchone()[0]

  res1, res2 = [], []
  # team 1 as the home team
  cmd = """
         SELECT match_date, match_time, visitor_name, visitor_pts, home_pts, home_name, attend 
         FROM match 
         WHERE home_tid = %s AND visitor_tid = %s;
  """
  cursor = g.conn.execute(cmd, (tid1, tid2))

  if cursor:
    for res in cursor:
      res1.append((n for n in res))

  # team 2 as the home team
  
  cursor = g.conn.execute(cmd, (tid2, tid1))
  if cursor:
    for res in cursor:
      res2.append((n for n in res))

  cursor.close()
  
  if not res1:
    res1 = None
  if not res2:
    res2 = None
  return tname1, tname2, res1, res2


@app.route("/matches", methods=['POST', 'GET'])
def matches():
  form = MatchForm()
  if form.validate_on_submit():
    tid1 = form.team1.data
    tid2 = form.team2.data
    print "2"
    tname1, tname2, data1, data2 = match_request(tid1, tid2)

    return render_template("match_stat.html", data1=data1, data2=data2, tname1 = tname1, tname2 = tname2)

  return render_template("matches.html", form=form)

# =============================================================================
# Registration and Login
# 

@login_manager.user_loader
def load_user(user_id):
  '''1. fetch user information through query the database
     2. return a User object with user data '''

  cursor = g.conn.execute("SELECT uid, username, password, tid, pid FROM users WHERE uid = %s;", user_id)
  result = cursor.fetchone()

  return User(result[0], result[1], result[2], result[3], result[4])
    
class User(UserMixin):
  """Creating a representation of each user"""
  def __init__(self, id, username, password, tid, pid, active=True):
    self.id = id
    self.username = username
    self.password = password 
    self.tid = tid
    self.pid = pid 
    self.active = active
    self.fav_team = self.get_fav_team()
    self.fav_player = self.get_fav_player()

  def __repr__(self):
    return "User('{}', '{}', '{}', '{}', '{}'".format(self.id, self.username, self.password, self.tid, self.pid)
  
  def get_fav_team(self):

    cmd = """
          SELECT team FROM team WHERE tid = %s;
    """
    cursor = g.conn.execute(cmd, self.tid)
    res = cursor.fetchone()
    cursor.close()
    if res:
      return res[0]

    return "No Favorite Team information"

  def get_fav_player(self):

    cmd = """
          SELECT fullname FROM player WHERE pid = %s;
    """
    cursor = g.conn.execute(cmd, self.pid)
    res = cursor.fetchone()
    cursor.close()
    print res
    print res[0]
    if res:
      return res[0]

    return "No Favorite Player Information"


@app.route('/register', methods=['POST', 'GET'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data
    
    tid = form.fav_team.data
    pid = form.fav_player.data

    cursor = g.conn.execute("SELECT MAX(uid) FROM users;")
    uid = cursor.fetchone()[0] + 1

    cursor = g.conn.execute("INSERT INTO users VALUES (%s, %s, %s, %s, %s);", (uid, username, password, tid, pid))

    cursor.close()

    flash('Account created for {}!'.format(form.username.data), 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():

    cmd = """
          SELECT uid, username, password, tid, pid
          FROM users
          WHERE username = %s;
          """

    cursor = g.conn.execute(cmd, form.username.data)
    result = cursor.fetchone()
    cursor.close()

    user = User(result[0], result[1], result[2], result[3], result[4])
    if form.password.data == result[2]:
      flash('You have been logged in!', 'success')
      login_user(user, remember=form.remember.data)
      return redirect(url_for('account'))
    else:
      flash('Login Unsuccesful. Username or Password is incorrect.', 'danger')

  return render_template('login.html', title='Login', form=form)
    
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
  
  form = UpdateAccountForm()
  if form.validate_on_submit():
    new_username = form.username.data
    new_tid = form.fav_team.data
    new_pid = form.fav_player.data

    cmd = """
          UPDATE users
          SET username = %s, tid = %s, pid = %s
          WHERE uid = %s;
    """
    
    cursor = g.conn.execute(cmd, (new_username, 
                                  new_tid, new_pid, current_user.id))
    cursor.close()

    flash('your account has been updated!', 'success')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.fav_team.data = current_user.tid
    form.fav_player.data = current_user.pid
  return render_template("account.html", 
                          title='Account', form=form)


@app.route('/account/fav_player_comp', methods=['POST', 'GET'])
@login_required
def fav_player_comp():

  fav_player = current_user.fav_player
  fav_player_id = current_user.pid
  form = FavPlayerCompForm()

  if form.validate_on_submit():
    pid2 = form.comp_player.data
    data, player_name_1, player_name_2 = player_comp(fav_player_id, pid2)
    return render_template("players_comp.html", data=data, player_name_1=player_name_1, player_name_2=player_name_2)

  return render_template("fav_player_comp_request.html", fav_player=fav_player, form=form)

@app.route('/account/fav_team_comp', methods=['POST', 'GET'])
@login_required
def fav_team_comp():

  fav_team = current_user.fav_team
  fav_team_id = current_user.tid
  form = FavTeamCompForm()

  if form.validate_on_submit():
    tid2 = form.comp_team.data
    data, team_name_1, team_name_2 = team_comp(fav_team_id, tid2)
    return render_template("teams_comp.html", data=data, team_name_1=team_name_1, team_name_2=team_name_2)

  return render_template("fav_team_comp_request.html", fav_team=fav_team, form=form)

@app.route('/account/fav_player_info', methods=['POST', 'GET'])
@login_required
def fav_player_info():
  
  pid = current_user.pid
  context = player_info_request(pid)
  return render_template("players.html", **context)
  

@app.route('/account/fav_team_info', methods=['POST', 'GET'])
@login_required
def fav_team_info():
  
  tid = current_user.tid
  context = team_info_request(tid)

  return render_template("teams.html", **context)



if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using
        python server.py
    Show the help text using
        python server.py --help
    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    
    app.run(host=HOST, port=PORT, debug=debug, threaded=threaded)



  run()
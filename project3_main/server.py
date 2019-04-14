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
from forms import RegistrationForm, LoginForm, UpdateAccountForm, PlayerCompForm, FavPlayerCompForm, FavTeamCompForm
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
def index():

  # DEBUG: this is debugging code to see what request looks like
  print request.args

  # cursor = g.conn.execute("SELECT name FROM test")
  # names = []
  # for result in cursor:
  #   names.append(result['name'])  # can also be accessed using result[0]
  # cursor.close()
  cursor = g.conn.execute("SELECT fullname FROM player WHERE pid <> 0 ORDER BY pid;")
  names = []
  for result in cursor:
    names.append(result[0])
  cursor.close()

  context = dict(data = names)

  return render_template("index.html", **context)


@app.route('/players', methods=['POST', 'GET'])
def player_info():

  # DEBUG: this is debugging code to see what request looks like
  # print request.args

  if request.method == 'POST':
    pid = request.form.get('player_id')

    attr_select_cat = {'player': ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg'], 'team': ['team']}
    
    attr_select_flat = ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', 'team']
    
    cmd = """
          SELECT {0}, T.team
          FROM player as P, team as T 
          WHERE P.tid = T.tid AND P.pid = {1}
          LIMIT 1;
          """.format(", ".join(['P.' + x for x in attr_select_cat['player']]), pid)

    cursor = g.conn.execute(cmd)
    result_dict = {attr: data for attr, data in zip(attr_select_flat, cursor.fetchone())}
    cursor.close()

    general_attr = ['team', 'fullname', 'age', 'pos']
    attr_show = ['gp', 'mpg', 'ppg', 'rpg', 'apg', 'topg']
    data_show = [result_dict[x] for x in attr_show]
    data_show_des = [terms.attr_des[x].title() for x in attr_show]

    data = zip(data_show_des, data_show)
    p_team = result_dict['team']
    p_fullname = result_dict['fullname'].title()
    p_pos = result_dict['pos'].upper()
    p_age = str(result_dict['age']) + ' Year Old'
    title = "Player Stats"

    return render_template("players.html", data=data, p_team=p_team, p_fullname=p_fullname, p_pos = p_pos, p_age=p_age, title=title, teams=zip(range(1, 31), terms.teams))


  cmd = "SELECT pid, fullname FROM player ORDER BY pid;"
  cursor = g.conn.execute(cmd)


  names = []
  for res in cursor:
    names.append((res[0], res[1]))
  cursor.close()

  undup_names = []
  for ind in range(len(names)-1):
    if names[ind + 1][1] != names[ind][1]:
      undup_names.append(names[ind])

  return render_template("player_request.html", player_names = undup_names)

@app.route('/teams', methods=['POST', 'GET'])
def team_info():
  
  if request.method == 'POST':
    attr_select = ['tid', 'team', 'conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

    tid = request.form.get('team_name')
    cmd = """
          SELECT {0} 
          FROM team
          WHERE tid = {1}
          LIMIT 1;
          """.format(", ".join(attr_select), tid)

    cursor = g.conn.execute(cmd)

    result = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
    cursor.close()

    attr_show = ['gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']
    data = zip([terms.attr_des[x] for x in attr_show], [result[x] for x in attr_show])
    
    t_team = result['team']
    t_conf = result['conf']
    t_division = result['division']

    return render_template("teams.html", data=data, t_team=t_team, t_conf=t_conf, t_division=t_division, teams=zip(range(1, 31), terms.teams))

  return render_template("teams_request.html", teams=zip(range(1, 31), terms.teams))


def player_comp(pid1, pid2, attr_show=None):
  # attributes to select in the query
  attr_select = ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', 'team']
  attr_select_str = ", ".join(['P.' + x for x in attr_select[:-1]])

  attr_show_default = ['team', 'pos', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', ]

  if attr_show is None:
    attr_show = attr_show_default

  cmd = """
        SELECT {attr_select}, T.team
        FROM player as P, team as T 
        WHERE P.tid = T.tid AND P.pid = {pid}
        LIMIT 1;
        """
  
  cursor = g.conn.execute(cmd.format(attr_select=attr_select_str, pid=pid1))
  result_dict1 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor = g.conn.execute(cmd.format(attr_select=attr_select_str, pid=pid2))
  result_dict2 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
  cursor.close()

  player_name_1 = result_dict1['fullname']
  player_name_2 = result_dict2['fullname']

  attr_show_des = [terms.attr_des[x] for x in attr_show]
  data = zip([result_dict1[x] for x in attr_show], attr_show_des, [result_dict2[x] for x in attr_show])

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

@app.route("/comparing_teams", methods=['POST', 'GET'])
def comparing_teams():
  if request.method == 'POST':
    tid1 = request.form.get('team_name1')
    tid2 = request.form.get('team_name2')

    # attr_select = ['tid', 'team', 'conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

    cmd1 = """
          SELECT {0} 
          FROM team
          WHERE tid = {1}
          LIMIT 1;
          """.format(", ".join(attr_select), tid1)

    cmd2 = """
          SELECT {0} 
          FROM team
          WHERE tid = {1}
          LIMIT 1;
          """.format(", ".join(attr_select), tid2)    

    cursor = g.conn.execute(cmd1)

    result1 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
    cursor = g.conn.execute(cmd2)
    result2 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
    cursor.close()

    attr_show = ['conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']
    attr_des = [terms.attr_des[x] for x in attr_show]
    data = zip([result1[x] for x in attr_show], attr_des, [result2[x] for x in attr_show])

    team_name_1 = result1['team']
    team_name_2 = result2['team']
    return render_template("teams_comp.html", data=data, team_name_1 = team_name_1, team_name_2=team_name_2)


  return render_template("teams_comp_request.html", teams=zip(range(1, 31), terms.teams))


# =============================================================================
# Registration and Login
# 

@login_manager.user_loader
def load_user(user_id):
  '''1. fetch user information through query the database
     2. return a User object with user data '''

  cursor = g.conn.execute("SELECT uid, username, password, tid, pid FROM users WHERE uid = {};".format(user_id))
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
          SELECT team FROM team WHERE tid = {};
    """.format(self.tid)
    cursor = g.conn.execute(cmd)
    res = cursor.fetchone()
    cursor.close()
    if res:
      return res[0]

    return "No Favorite Team information"

  def get_fav_player(self):

    cmd = """
          SELECT fullname FROM player WHERE pid = {};
    """.format(self.pid)
    cursor = g.conn.execute(cmd)
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
    cursor = g.conn.execute("INSERT INTO users VALUES ({}, '{}', '{}', {}, {});".format(uid, username, password, tid, pid))
    cursor.close()

    flash('Account created for {}!'.format(form.username.data), 'success')
    return redirect('/')
  return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
  form = LoginForm()
  if form.validate_on_submit():

    cmd = """
          SELECT uid, username, password, tid, pid
          FROM users
          WHERE username = '{}';
          """.format(form.username.data)

    cursor = g.conn.execute(cmd)
    result = cursor.fetchone()
    cursor.close()

    user = User(result[0], result[1], result[2], result[3], result[4])
    if form.password.data == result[2]:
      # flash('You have been logged in!', 'success')
      login_user(user, remember=form.remember.data)
      return redirect('/')
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
          SET username = '{username}', tid = {tid}, pid = {pid}
          WHERE uid = {uid};
    """.format(username = new_username,
              tid = new_tid,
              pid = new_pid,
              uid = current_user.id)
    
    cursor = g.conn.execute(cmd)
    cursor.close()

    flash('your account has been updated!', 'success')
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.fav_team.data = current_user.tid
    form.fav_player.data = current_user.pid
  return render_template("account.html", 
                          title='Account', form=form)


@app.route('/fav_player_comp', methods=['POST', 'GET'])
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
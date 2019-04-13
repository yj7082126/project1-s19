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
from flask import Flask, request, render_template, g, redirect, Response, url_for
import terms

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

# Set up for the class database

DB_USER = "yk2805"
DB_PASSWORD = "j25CnkRB8F"

DB_SERVER = "w4111.cisxo09blonu.us-east-1.rds.amazonaws.com"

DATABASEURI = "postgresql://"+DB_USER+":"+DB_PASSWORD+"@"+DB_SERVER+"/w4111"


#
# This line creates a database engine that knows how to connect to the URI above
#
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

team_names = []
#
# @app.route is a decorator around index() that means:
#   run index() whenever the user tries to access the "/" path using a GET request
#
# If you wanted the user to go to e.g., localhost:8111/foobar/ with POST or GET then you could use
#
#       @app.route("/foobar/", methods=["POST", "GET"])
#
# PROTIP: (the trailing / in the path is important)
# 
# see for routing: http://flask.pocoo.org/docs/0.10/quickstart/#routing
# see for decorators: http://simeonfranklin.com/blog/2012/jul/1/python-decorators-in-12-steps/
#
@app.route('/')
@app.route('/index')
def index():
  """
  request is a special object that Flask provides to access web request information:
  request.method:   "GET" or "POST"
  request.form:     if the browser submitted a form, this contains the data in the form
  request.args:     dictionary of URL arguments e.g., {a:1, b:2} for http://localhost?a=1&b=2
  See its API: http://flask.pocoo.org/docs/0.10/api/#incoming-request-data
  """

  # DEBUG: this is debugging code to see what request looks like
  print request.args


  #
  # example of a database query
  #
  cursor = g.conn.execute("SELECT name FROM test")
  names = []
  for result in cursor:
    names.append(result['name'])  # can also be accessed using result[0]
  cursor.close()

  #
  # Flask uses Jinja templates, which is an extension to HTML where you can
  # pass data to a template and dynamically generate HTML based on the data
  # (you can think of it as simple PHP)
  # documentation: https://realpython.com/blog/python/primer-on-jinja-templating/
  #
  # You can see an example template in templates/index.html
  #
  # context are the variables that are passed to the template.
  # for example, "data" key in the context variable defined below will be 
  # accessible as a variable in index.html:
  #
  #     # will print: [u'grace hopper', u'alan turing', u'ada lovelace']
  #     <div>{{data}}</div>
  #     
  #     # creates a <div> tag for each element in data
  #     # will print: 
  #     #
  #     #   <div>grace hopper</div>
  #     #   <div>alan turing</div>
  #     #   <div>ada lovelace</div>
  #     #
  #     {% for n in data %}
  #     <div>{{n}}</div>
  #     {% endfor %}
  #
  context = dict(data = names)


  #
  # render_template looks in the templates/ folder for files.
  # for example, the below file reads template/index.html
  #
  return render_template("index.html", **context)

#
# This is an example of a different path.  You can see it at
# 
#     localhost:8111/another
#
# notice that the functio name is another() rather than index()
# the functions for each app.route needs to have different names
#



# Example of adding new data to the database
@app.route('/add', methods=['POST'])
def add():
  name = request.form['name']
  print name
  cmd = 'INSERT INTO test(name) VALUES (:name1), (:name2)';
  g.conn.execute(text(cmd), name1 = name, name2 = name);
  return redirect('/')


@app.route('/login')
def login():
    abort(401)
    this_is_never_executed()


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


@app.route("/comparing_players", methods=['POST', 'GET'])
def comparing_players():
  

  if request.method == 'POST':
    pid1 = request.form.get('player_name1')
    pid2 = request.form.get('player_name2')

    attr_select = ['pid', 'fullname', 'pos', 'age', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', 'team']
    
    cmd1 = """
          SELECT {0}, T.team
          FROM player as P, team as T 
          WHERE P.tid = T.tid AND P.pid = {1}
          LIMIT 1;
          """.format(", ".join(['P.' + x for x in attr_select[:-1]]), pid1)

    cmd2 = """
          SELECT {0}, T.team
          FROM player as P, team as T 
          WHERE P.tid = T.tid AND P.pid = {1}
          LIMIT 1;
          """.format(", ".join(['P.' + x for x in attr_select[:-1]]), pid2)

    cursor = g.conn.execute(cmd1)
    result_dict1 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
    cursor = g.conn.execute(cmd2)
    result_dict2 = {attr: data for attr, data in zip(attr_select, cursor.fetchone())}
    cursor.close()

    player_name_1 = result_dict1['fullname']
    player_name_2 = result_dict2['fullname']


    attr_show = attr_select = ['team', 'pos', 'gp', 'mpg', 'min', 'usg', 'tor', 'fta', 'ft', 'pa2', 'p2', 'pa3', 'p3', 'efg', 'ts', 'ppg', 'rpg', 'trb', 'apg', 'ast', 'spg', 'bpg', 'topg', 'vi', 'ortg', 'drtg', ]

    attr_show_des = [terms.attr_des[x] for x in attr_show]
    data = zip([result_dict1[x] for x in attr_show], attr_show_des, [result_dict2[x] for x in attr_show])

    return render_template("players_comp.html", data=data, player_name_1=player_name_1, player_name_2=player_name_2)

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

  return render_template("players_comp_request.html", player_names = undup_names)

@app.route("/comparing_teams", methods=['POST', 'GET'])
def comparing_teams():
  if request.method == 'POST':
    tid1 = request.form.get('team_name1')
    tid2 = request.form.get('team_name2')

    attr_select = ['tid', 'team', 'conf', 'division', 'gp', 'ptsgm', 'aptsgm', 'ptsdiff', 'pace', 'oeff', 'deff', 'ediff', 'sos', 'rsos', 'sar', 'cons', 'a4f', 'w', 'l', 'win', 'ewin', 'pwin', 'ach', 'strk']

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
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask import g
from flask_login import current_user

team_list = [u'Atlanta Hawks', u'Boston Celtics', u'Brooklyn Nets', u'Charlotte Hornets', u'Chicago Bulls', u'Cleveland Cavaliers', u'Dallas Mavericks', u'Denver Nuggets', u'Detroit Pistons', u'Golden State Warriors', u'Houston Rockets', u'Indiana Pacers', u'Los Angeles Clippers', u'Los Angeles Lakers', u'Memphis Grizzlies', u'Miami Heat', u'Milwaukee Bucks', u'Minnesota Timberwolves', u'New Orleans Pelicans', u'New York Knicks', u'Oklahoma City Thunder', u'Orlando Magic', u'Philadelphia 76ers', u'Phoenix Suns', u'Portland Trail Blazers', u'Sacramento Kings', u'San Antonio Spurs', u'Toronto Raptors', u'Utah Jazz', u'Washington Wizards']


player_list = [u'Alex Abrines', u'Quincy Acy', u'Jaylen Adams', u'Steven Adams', u'Bam Adebayo', u'Deng Adel', u'DeVaughn Akoon-Purcell', u'LaMarcus Aldridge', u'Rawle Alkins', u'Grayson Allen', u'Jarrett Allen', u'Kadeem Allen', u'Al-Farouq Aminu', u'Justin Anderson', u'Kyle Anderson', u'Ryan Anderson', u'Ryan Anderson', u'Ike Anigbogu', u'Giannis Antetokounmpo', u'Carmelo Anthony', u'OG Anunoby', u'Ryan Arcidiacono', u'Trevor Ariza', u'Trevor Ariza', u'D.J. Augustin', u'Deandre Ayton', u'Dwayne Bacon', u'Marvin Bagley III', u'Ron Baker', u'Ron Baker', u'Wade Baldwin IV', u'Lonzo Ball', u'Mo Bamba', u'J.J. Barea', u'Harrison Barnes', u'Harrison Barnes', u'Will Barton', u'Keita Bates-Diop', u'Nicolas Batum', u'Jerryd Bayless', u'Aron Baynes', u'Kent Bazemore', u'Bradley Beal', u'Malik Beasley', u'Michael Beasley', u'Marco Belinelli', u'Jordan Bell', u"DeAndre' Bembry", u'Dragan Bender', u'Davis Bertans', u'Patrick Beverley', u'Khem Birch', u'Bismack Biyombo', u'Nemanja Bjelica', u'Antonio Blakeney', u'Eric Bledsoe', u'Jaron Blossomgame', u'Bojan Bogdanovic', u'Bogdan Bogdanovic', u'Jonah Bolden', u'Isaac Bonga', u'Devin Booker', u'Chris Boucher', u'Avery Bradley', u'Avery Bradley', u'Tony Bradley', u'Corey Brewer', u'Corey Brewer', u'Miles Bridges', u'Mikal Bridges', u'Isaiah Briscoe', u'Ryan Broekhoff', u'Malcolm Brogdon', u'Dillon Brooks', u'MarShon Brooks', u'Troy Brown Jr.', u'Bruce Brown', u'Jaylen Brown', u'Lorenzo Brown', u'Sterling Brown', u'Jalen Brunson', u'Thomas Bryant', u'Reggie Bullock', u'Reggie Bullock', u'Trey Burke', u'Trey Burke', u'Alec Burks', u'Alec Burks', u'Alec Burks', u'Deonte Burton', u'Jimmy Butler', u'Jimmy Butler', u'Bruno Caboclo', u'Jose Calderon', u'Kentavious Caldwell-Pope', u'Isaiah Canaan', u'Isaiah Canaan', u'Isaiah Canaan', u'Clint Capela', u'DeMarre Carroll', u'Wendell Carter Jr.', u'Jevon Carter', u'Vince Carter', u'Michael Carter-Williams', u'Alex Caruso', u'Omri Casspi', u'Willie Cauley-Stein', u'Troy Caupain', u'Tyler Cavanaugh', u'Tyson Chandler', u'Tyson Chandler', u'Wilson Chandler', u'Joe Chealey', u'Marquese Chriss', u'Marquese Chriss', u'Gary Clark', u'Ian Clark', u'Jordan Clarkson', u'John Collins', u'Zach Collins', u'Darren Collison', u'Bonzie Colson', u'Mike Conley', u'Pat Connaughton', u'Quinn Cook', u'DeMarcus Cousins', u'Robert Covington', u'Robert Covington', u'Allen Crabbe', u'Torrey Craig', u'Jamal Crawford', u'Mitchell Creek', u'Jae Crowder', u'Dante Cunningham', u'Seth Curry', u'Stephen Curry', u'Troy Daniels', u'Anthony Davis', u'Ed Davis', u'Tyler Davis', u'Dewayne Dedmon', u'Sam Dekker', u'Sam Dekker', u'Angel Delgado', u'Matthew Dellavedova', u'Matthew Dellavedova', u'Luol Deng', u'DeMar DeRozan', u'Marcus Derrickson', u'Cheick Diallo', u'Hamidou Diallo', u'Gorgui Dieng', u'Spencer Dinwiddie', u'Donte DiVincenzo', u'Luka Doncic', u'Tyler Dorsey', u'Tyler Dorsey', u'Damyean Dotson', u'PJ Dozier', u'Goran Dragic', u'Andre Drummond', u'Jared Dudley', u'Kris Dunn', u'Kevin Durant', u'Trevon Duval', u'Vincent Edwards', u'Henry Ellenson', u'Henry Ellenson', u'Wayne Ellington', u'Wayne Ellington', u'Joel Embiid', u'James Ennis III', u'James Ennis III', u'Drew Eubanks', u'Jacob Evans', u'Jawun Evans', u'Tyreke Evans', u'Dante Exum', u'Kenneth Faried', u'Kenneth Faried', u'Derrick Favors', u'Cristiano Felicio', u'Raymond Felton', u'Terrance Ferguson', u'Yogi Ferrell', u'Dorian Finney-Smith', u'Bryn Forbes', u'Evan Fournier', u"De'Aaron Fox", u'Melvin Frazier Jr.', u'Tim Frazier', u'Channing Frye', u'Markelle Fultz', u'Danilo Gallinari', u'Langston Galloway', u'Marc Gasol', u'Marc Gasol', u'Pau Gasol', u'Rudy Gay', u'Paul George', u'Taj Gibson', u'Harry Giles III', u'Shai Gilgeous-Alexander', u'Rudy Gobert', u'Brandon Goodwin', u'Aaron Gordon', u'Eric Gordon', u'Marcin Gortat', u"Devonte' Graham", u'Treveon Graham', u'Donte Grantham', u'Jerami Grant', u'Jerian Grant', u'Danny Green', u'Draymond Green', u'Gerald Green', u'JaMychal Green', u'JaMychal Green', u'Jeff Green', u'Blake Griffin', u'Daniel Hamilton', u'Tim Hardaway Jr.', u'Tim Hardaway Jr.', u'James Harden', u'Maurice Harkless', u'Montrezl Harrell', u'Devin Harris', u'Gary Harris', u'Joe Harris', u'Andrew Harrison', u'Andrew Harrison', u'Andrew Harrison', u'Shaquille Harrison', u'Tobias Harris', u'Tobias Harris', u'Isaiah Hartenstein', u'Josh Hart', u'Udonis Haslem', u'Gordon Hayward', u'John Henson', u'Juancho Hernangomez', u'Willy Hernangomez', u'Mario Hezonja', u'Isaiah Hicks', u'Buddy Hield', u'Haywood Highsmith', u'George Hill', u'George Hill', u'Solomon Hill', u'Aaron Holiday', u'Jrue Holiday', u'Justin Holiday', u'Justin Holiday', u'John Holland', u'Rondae Hollis-Jefferson', u'Richaun Holmes', u'Rodney Hood', u'Rodney Hood', u'Al Horford', u'Danuel House Jr.', u'Dwight Howard', u'Kevin Huerter', u'Chandler Hutchison', u'Serge Ibaka', u'Andre Iguodala', u'Ersan Ilyasova', u'Joe Ingles', u'Brandon Ingram', u'Kyrie Irving', u'Jonathan Isaac', u'Wes Iwundu', u'Jaren Jackson Jr.', u'Demetrius Jackson', u'Frank Jackson', u'Josh Jackson', u'Justin Jackson', u'Justin Jackson', u'Reggie Jackson', u'LeBron James', u'Amile Jefferson', u'John Jenkins', u'John Jenkins', u'Jonas Jerebko', u'Alize Johnson', u'Amir Johnson', u'James Johnson', u'Stanley Johnson', u'Stanley Johnson', u'Tyler Johnson', u'Tyler Johnson', u'Wesley Johnson', u'Wesley Johnson', u'Nikola Jokic', u'Derrick Jones Jr.', u'Da16n Jones', u'Jalen Jones', u'Tyus Jones', u'DeAndre Jordan', u'DeAndre Jordan', u'Cory Joseph', u'Frank Kaminsky', u'Enes Kanter', u'Enes Kanter', u'Luke Kennard', u'Michael Kidd-Gilchrist', u'George King', u'Maxi Kleber', u'Brandon Knight', u'Brandon Knight', u'Kevin Knox', u'Furkan Korkmaz', u'Luke Kornet', u'Kyle Korver', u'Kyle Korver', u'Kosta Koufos', u'Rodions Kurucs', u'Kyle Kuzma', u'Skal Labissiere', u'Skal Labissiere', u'Jeremy Lamb', u'Zach LaVine', u'Jake Layman', u'TJ Leaf', u'Courtney Lee', u'Courtney Lee', u'Damion Lee', u'Alex Len', u'Kawhi Leonard', u'Meyers Leonard', u'Jon Leuer', u'Caris LeVert', u'Da16n Lillard', u'Jeremy Lin', u'Jeremy Lin', u'Shaun Livingston', u'Zach Lofton', u'Kevon Looney', u'Brook Lopez', u'Robin Lopez', u'Kevin Love', u'Kyle Lowry', u'Jordan Loyd', u'Kalin Lucas', u'Timothe Luwawu-Cabarrot', u'Timothe Luwawu-Cabarrot', u'Tyler Lydon', u'Trey Lyles', u'Shelvin Mack', u'Shelvin Mack', u'Daryl Macon', u'J.P. Macura', u'Ian Mahinmi', u'Thon Maker', u'Thon Maker', u'Boban Marjanovic', u'Boban Marjanovic', u'Lauri Markkanen', u'Jarell Martin', u'Frank Mason', u'Wesley Matthews', u'Wesley Matthews', u'Wesley Matthews', u'Luc Mbah a Moute', u'Patrick McCaw', u'Patrick McCaw', u'CJ McCollum', u'T.J. McConnell', u'Doug McDermott', u'JaVale McGee', u'Rodney McGruder', u'Alfonzo McKinnie', u'Ben M6more', u'Jordan McRae', u'Jodie Meeks', u'Salah Mejri', u"De'Anthony Melton", u'Chimezie Metu', u'Khris Middleton', u'CJ Miles', u'CJ Miles', u'Darius Miller', u'Paul Millsap', u'Patty Mills', u'Shake Milton', u'Nikola Mirotic', u'Nikola Mirotic', u'Donovan Mitchell', u'Naz Mitrou-Long', u'Malik Monk', u'Greg Monroe', u"E'Twaun Moore", u'Eric Moreland', u'Jaylen Morris', u'Marcus Morris', u'Markieff Morris', u'Markieff Morris', u'Monte Morris', u'Johnathan Motley', u'Emmanuel Mudiay', u'Jamal Murray', u'Dzanan Musa', u'Mike Muscala', u'Mike Muscala', u'Svi Mykhailiuk', u'Svi Mykhailiuk', u'Abdel Nader', u'Larry Nance Jr.', u'Shabazz Napier', u'Nene', u'Raul Neto', u'Georges Niang', u'Joakim Noah', u'Nerlens Noel', u'Dirk Nowitzki', u'Frank Ntilikina', u'James Nunnally', u'James Nunnally', u'Jusuf Nurkic', u'David Nwaba', u'Semi Ojeleye', u'Jahlil Okafor', u'Elie Okobo', u'Josh Okogie', u'Victor Oladipo', u'Kelly Olynyk', u"Royce O'Neale", u"Kyle O'Quinn", u'Cedi Osman', u'Kelly Oubre Jr.', u'Kelly Oubre Jr.', u'Zaza Pachulia', u'Jabari Parker', u'Jabari Parker', u'Tony Parker', u'Chandler Parsons', u'Patrick Patterson', u'Chris Paul', u'Cameron Payne', u'Cameron Payne', u'Gary Payton II', u'Elfrid Payton', u'Theo Pinson', u'Mason Plumlee', u'Miles Plumlee', u'Jakob Poeltl', u'Quincy Pondexter', u'Otto Porter Jr.', u'Otto Porter Jr.', u'Bobby Portis', u'Bobby Portis', u'Dwight Powell', u'Norman Powell', u'Alex Poythress', u'Taurean Prince', u'Zhou Qi', u'Ivan Rabb', u'Chasson Randle', u'Julius Randle', u'JJ Redick', u'Davon Reed', u'Josh Richardson', u'Malachi Richardson', u'Austin Rivers', u'Austin Rivers', u'Glenn Robinson III', u'Devin Robinson', u'Duncan Robinson', u'Jerome Robinson', u'Mitchell Robinson', u'Rajon Rondo', u'Derrick Rose', u'Terrence Ross', u'Terry Rozier', u'Ricky Rubio', u"D'Angelo Russell", u'Domantas Sabonis', u'Brandon Sampson', u'Dario Saric', u'Dario Saric', u'Tomas Satoransky', u'Dennis Schroder', u'Mike Scott', u'Mike Scott', u'Thabo Sefolosha', u'Wayne Selden', u'Wayne Selden', u'Collin Sexton', u'Landry Shamet', u'Landry Shamet', u'Iman Shumpert', u'Iman Shumpert', u'Pascal Siakam', u'Ben Simmons', u'Jonathon Simmons', u'Jonathon Simmons', u'Kobi Simmons', u'Anfernee Simons', u'Marcus Smart', u'Dennis Smith Jr.', u'Dennis Smith Jr.', u'Ish Smith', u'Jason Smith', u'Jason Smith', u'JR Smith', u'Tony Snell', u'Ray Spalding', u'Omari Spellman', u'Nik Stauskas', u'Nik Stauskas', u'DJ Stephens', u'Lance Stephenson', u'Edmond Sumner', u'Caleb Swanigan', u'Jayson Tatum', u'Jeff Teague', u'Garrett Temple', u'Garrett Temple', u'Milos Teodosic', u'Jared Terrell', u'Emanuel Terry', u'Emanuel Terry', u'Daniel Theis', u'Isaiah Thomas', u'Khyri Thomas', u'Lance Thomas', u'Klay Thompson', u'Tristan Thompson', u'Sindarius Thornwell', u'Anthony Tolliver', u'Karl-Anthony Towns', u'Gary Trent Jr.', u'Allonzo Trier', u'PJ Tucker', u'Evan Turner', u'Myles Turner', u'Ekpe Udoh', u'Tyler Ulis', u'Jonas Valanciunas', u'Jonas Valanciunas', u'Jarred Vanderbilt', u'Fred VanVleet', u'Noah Vonleh', u'Nikola Vucevic', u'Dwyane Wade', u'Moritz Wagner', u'Dion Waiters', u'Lonnie Walker IV', u'Kemba Walker', u'Tyrone Wallace', u'John Wall', u'Brad Wanamaker', u'T.J. Warren', u'Julian Washburn', u'Yuta Watanabe', u'Thomas Welsh', u'Russell Westbrook', u'Derrick White', u'Okaro White', u'Hassan Whiteside', u'Andrew Wiggins', u'Robert Williams III', u'Alan Williams', u'C.J. Williams', u'Johnathan Williams', u'Kenrich Williams', u'Lou Williams', u'Marvin Williams', u'Troy Williams', u'D.J. Wilson', u'Justise Winslow', u'Christian Wood', u'Delon Wright', u'Delon Wright', u'Guerschon Yabusele', u'Nick Young', u'Thaddeus Young', u'Trae Young', u'Cody Zeller', u'Ante Zizic', u'Ivica Zubac', u'Ivica Zubac']

team_choices = [(ind, team_name) for ind, team_name in enumerate(team_list, start=1)]

player_choices = [(ind, player_name) for ind, player_name in enumerate(player_list, start=1)]

class RegistrationForm(FlaskForm):
	"""Creating Forms for Registration"""

	username = StringField('Username', 
						validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired(), 
													Length(min=10)])
	confirm_password = PasswordField('Confirm Password', 
								validators=[DataRequired(), EqualTo('password')])

	fav_player = SelectField('Favorite Player', choices=player_choices, coerce=int)

	fav_team = SelectField('Favorite Team', choices=team_choices, coerce=int)

	submit = SubmitField('Sign Up')

	def validate_username(self, username):

		cursor = g.conn.execute("SELECT uid FROM users WHERE username = %s", username.data)
		result = cursor.fetchone()
		if result:
			raise ValidationError('That username is taken. Please choose a different one.')
	

class LoginForm(FlaskForm):
	"""Creating Forms for login"""

	username = StringField('Username', 
						validators=[DataRequired(), Length(min=2, max=20)])
	password = PasswordField('Password', validators=[DataRequired(), 
													Length(min=10)])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
	"""Creating Forms for Registration"""

	username = StringField('Username', 
						validators=[DataRequired(), Length(min=2, max=20)])
	
	fav_player = SelectField('Favorite Player', choices=player_choices, coerce=int)

	fav_team = SelectField('Favorite Team', choices=team_choices, coerce=int)
	
	submit = SubmitField('Update')

	def validate_username(self, username):
		if username.data != current_user.username:

			cursor = g.conn.execute("SELECT uid FROM users WHERE username = %s", username.data)
			result = cursor.fetchone()
			if result:
				raise ValidationError('That username is taken. Please choose a different one.')

class PlayerInfoForm(FlaskForm):
	player = SelectField('Player', choices=player_choices, coerce=int)
	submit = SubmitField('Get Stat!')

class TeamInfoForm(FlaskForm):

	team = SelectField('Team', choices=team_choices, coerce=int)
	submit = SubmitField('Get Stat!')

class PlayerCompForm(FlaskForm):

	player1 = SelectField('First Player', choices=player_choices, coerce=int)
	player2 = SelectField('Second Player', choices=player_choices, coerce=int)

	submit = SubmitField('Compare!')


class TeamCompForm(FlaskForm):

	team1 = SelectField('First Team', choices=team_choices, coerce=int)
	team2 = SelectField('Second Team', choices=team_choices, coerce=int)

	submit = SubmitField('Compare!')


class FavPlayerCompForm(FlaskForm):
	"""docstring for FavPlayerCompForm"""

	comp_player = SelectField('Second Player', choices=player_choices, coerce=int)
	submit = SubmitField('Compare!')


class FavTeamCompForm(FlaskForm):
	"""docstring for FavPlayerCompForm"""
	
	comp_team = SelectField('Second Team', choices=team_choices, coerce=int)
	submit = SubmitField('Compare!')
		

class MatchForm(FlaskForm):

	team1 = SelectField('First Team', choices=team_choices, coerce=int)
	team2 = SelectField('Second Team', choices=team_choices, coerce=int)

	submit = SubmitField('Search!')

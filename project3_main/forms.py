from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask import g
from flask_login import current_user
from terms import teams as team_list, players as player_list



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

		cursor = g.conn.execute("SELECT uid FROM users WHERE username = '{}'".format(username.data))
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

			cursor = g.conn.execute("SELECT uid FROM users WHERE username = '{}'".format(username.data))
			result = cursor.fetchone()
			if result:
				raise ValidationError('That username is taken. Please choose a different one.')


class FavPlayerCompForm(FlaskForm):
	"""docstring for FavPlayerCompForm"""

	comp_player = SelectField('Second Player', choices=player_choices, coerce=int)
	submit = SubmitField('Compare!')


class FavTeamCompForm(FlaskForm):
	"""docstring for FavPlayerCompForm"""
	
	comp_team = SelectField('Second Team', choices=team_choices, coerce=int)
	submit = SubmitField('Compare!')
		


from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class RegistrationForm(FlaskForm):
	"""docstring for RegistrationForm"""
	def __init__(self, arg):
		super(RegistrationForm, self).__init__()
		self.arg = arg

	username = StringField('Username', validators=[])
		
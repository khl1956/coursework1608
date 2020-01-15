from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, SelectField
from wtforms.validators import DataRequired, Length, Email, Regexp, regexp


class SignUpFrom(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min = 2, max = 20), Regexp(r'^[\w.@+-]+$')])
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	button = SubmitField('Submit!')


class LogInFrom(FlaskForm):
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	button = SubmitField('Submit!')


class CreateUserFrom(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min = 2, max = 20), Regexp(r'^[\w.@+-]+$')])
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	make_admin = BooleanField('Make this new user admin?')
	button = SubmitField('Create!')

class EditForm(FlaskForm):
	name = StringField('Name', validators = [DataRequired(), Length(min = 2, max = 20), Regexp(r'^[\w.@+-]+$')])
	email = StringField('E-mail', validators = [DataRequired(), Email()])
	password = PasswordField('Password', validators = [DataRequired()])
	button = SubmitField('Save!')

class CreateMigrationFrom(FlaskForm):
	file = FileField(u'File', [Regexp(r'^[^/\\]\.sql$')])
	databaseFrom = SelectField(u'Database to migrate from', choices=[('postgresql', 'PostgreSQL')])
	databaseTo = SelectField(u'Database to migrate from', choices=[('cassandra', 'Cassandra')])
	button = SubmitField('Create!')


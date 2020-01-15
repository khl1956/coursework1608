from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime

app = Flask(__name__)
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__ = 'user_'

	id = db.Column(db.String(36), primary_key = True)
	password = db.Column(db.Text)
	name = db.Column(db.Text)
	email = db.Column(db.Text, unique=True)
	isadmin = db.Column(db.Boolean, default = False)

	session = db.relationship('Session', backref = 'user')
	databasemigration = db.relationship('Migration', backref = 'user')

	def get_id(self):
		return self.id

	def __init__(self, name, email, password, isAdmin):
		self.id = str(uuid.uuid1())
		self.name = name
		self.password = password
		self.email = email
		self.isadmin = isAdmin


class Session(db.Model):
	__tablename__ = 'session'

	id = db.Column(db.String(36), primary_key = True)
	userid = db.Column(db.String(36), db.ForeignKey('user_.id'))
	browser = db.Column(db.Text)
	os = db.Column(db.Text)

	def __init__(self, browser, os, user):
		self.id = str(uuid.uuid1())
		self.browser = browser
		self.os = os
		self.user = user


class DataType(db.Model):
	__tablename__ = 'datatype'
	id = db.Column(db.String(50), primary_key = True)
	database = db.Column(db.String(50))
	name = db.Column(db.String(50))
	datatype = db.Column(db.String(50))
	__table_args__ = (db.UniqueConstraint('database', 'datatype', name='dtdbu'),)
	def __init__(self, database, name, datatype):
		self.id = str(uuid.uuid1())
		self.database = database
		self.name = name
		self.datatype = datatype


class DatabaseEntity(db.Model):
	__tablename__ = 'databaseentity'
	id = db.Column(db.String(36), primary_key = True, nullable = False)
	database = db.Column(db.String(50), nullable = False)
	entityname = db.Column(db.String(50), nullable = False)
	__table_args__ = (db.UniqueConstraint('database', 'entityname', name='endbU'),)
	def __init__(self, database, entityname):
		self.id = str(uuid.uuid1())
		self.database = database
		self.entityname = entityname

class Operation(db.Model):
	__tablename__ = 'operation'
	id = db.Column(db.String(36), primary_key = True)
	database = db.Column(db.String(50), nullable = False)
	name = db.Column(db.String(50), nullable = False)
	__table_args__ = (db.UniqueConstraint('database', 'name', name='opdbU'),)
	def __init__(self, database, name):
		self.id = str(uuid.uuid1())
		self.name = name
		self.database = database


class OperationContainsOperation(db.Model):
	__tablename__ = 'operationcontainsoperation'
	id = db.Column(db.String(36), primary_key = True)
	operation1id = db.Column(db.String(36), db.ForeignKey('operation.id'), primary_key = True, nullable = False)
	operation2id = db.Column(db.String(36), db.ForeignKey('operation.id'), primary_key = True, nullable = False)
	def __init__(self, operation1id, operation2id):
		self.id = str(uuid.uuid1())
		self.operation1id = operation1id
		self.operation2id = operation2id


class OperationUseDatabaseEntity(db.Model):
	__tablename__ = 'operationusedatabaseentity'
	id = db.Column(db.String(36), primary_key = True)
	operationid = db.Column(db.String(36), db.ForeignKey('operation.id'), primary_key = True, nullable = False)
	databaseentityid = db.Column(db.String(36), db.ForeignKey('databaseentity.id'), primary_key = True, nullable = False)
	def __init__(self, operationid, databaseentityid):
		self.id = str(uuid.uuid1())
		self.operationid = operationid
		self.databaseentityid = databaseentityid

class Syntax(db.Model):
	__tablename__ = 'syntax'
	id = db.Column(db.String(36), primary_key = True)
	database = db.Column(db.String(50), nullable = False)
	regex = db.Column(db.Text, nullable = False)
	operationid = db.Column(db.String(36), db.ForeignKey('operation.id'), nullable = False)
	__table_args__ = (db.UniqueConstraint('database', 'regex', name='redbU'),)
	def __init__(self, database, regex, operationid):
		self.id = str(uuid.uuid1())
		self.regex = regex
		self.database = database
		self.operationid = operationid

class Migration(db.Model):
	__tablename__ = 'databasemigration'

	databaseTo = db.Column(db.String(50), nullable = False)
	databaseFrom = db.Column(db.String(50), nullable = False)
	input_file = db.Column(db.String(100), nullable = False)
	log = db.Column(db.String(100), nullable = False)
	result = db.Column(db.String(100), nullable = True)
	date = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)
	id = db.Column(db.String(36), primary_key = True)
	userid = db.Column(db.String(36), db.ForeignKey('user_.id'))

	def __init__(self, databaseTo, databaseFrom, input_file, log, result, userid):
		self.id = str(uuid.uuid1())
		self.databaseTo = databaseTo
		self.databaseFrom = databaseFrom
		self.input_file = input_file
		self.log = log
		self.result = result
		self.userid = userid
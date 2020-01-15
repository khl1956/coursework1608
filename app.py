from flask import render_template, url_for, redirect, request, flash, Blueprint
from forms import SignUpFrom, LogInFrom, CreateUserFrom, CreateMigrationFrom, EditForm
from orm import *
import re
from flask_login import LoginManager, login_user, logout_user, current_user
import os
from werkzeug.utils import secure_filename
from flask.cli import with_appcontext
import click
from wtforms import SubmitField

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = {'sql'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
auth = Blueprint('auth', __name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://pbwhorszaqzeya:500d580dfd54f78747aab111e364762631e9b19264ca6790f6c81f1a3aaacb56@ec2-184-73-209-230.compute-1.amazonaws.com:5432/d1eh44bepdpl7'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
@login_manager.user_loader
def load_user(id):
    return User.query.get(id)

def create_tables():
	db.drop_all()
	db.create_all()
def populate_tables():
	from populate import populate
	populate()

db.init_app(app)
create_tables()
populate_tables()

@app.context_processor
def utility_processor():
    return {'len': len}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/migration', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        databaseFrom = request.form.get('databaseFrom')
        if (databaseFrom != 'postgresql'):
            flash('Wrong database From')
        databaseTo = request.form.get('databaseTo')
        if (databaseTo != 'cassandra'):
            flash('Wrong database To')
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if False:
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # with open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) as f:
                content = 'f.readlines()'
                # you may also want to remove whitespace characters like `\n` at the end of each line
                content = [x.strip() for x in content]
                newContent = []
                log = []
                for line in content:
                    match = re.search('CREATE TYPE (.*) AS \((\w+\s+[\w|\(\w+\)|]+)(,\s*\w+\s+[\w|\(\w+\)|]+)*\);', line)
                    if (match):
                        typename = re.search('CREATE TYPE (.*) AS', line).group(1)
                        log.append('Successfully migrated udt '+ '"' + typename + '".')
                        typeAttributes = re.search('CREATE TYPE '+ typename +' AS \((.*)\);', line).group(1)
                        newContent.append(typeAttributes)
                        # algoritm is very large
    user_id = current_user.id
    migration = Migration(
        databaseFrom,
        databaseTo,
        'https://drive.google.com/file/d/11eVsd2BJt5VAye6YwhX3KKalTb-jOApK/view?usp=sharing',
        'https://drive.google.com/file/d/1rJKM07l_O0ppa2xltse3text7vo-HjCf/view?usp=sharing',
        'https://drive.google.com/file/d/16OT-OjRQfLKvYqa5-cRuQ8K3EiOjbYMI/view?usp=sharing',
        user_id
    )
    db.session.add(migration)
    db.session.commit()
    user = User.query.filter_by(id = user_id).first()
    user.is_active = True
    login_user(user)
    return redirect(url_for('user', id = user_id))

@app.route('/delete', methods=['POST'])
def delete():
    if request.method == 'POST':
        id = request.form.get('id')
        if (id != current_user.id):
            return 'STOP!'
        db.session.query(Session).filter(Session.userid == id).delete()
        db.session.query(Migration).filter(Migration.userid == id).delete()
        db.session.query(User).filter(User.id == id).delete()

        db.session.commit()
        return redirect(url_for('index'))


@app.route('/')
def index():
    tables = {}
    for Object in (Syntax, DataType):
        table = [tuple(c.name for c in list(Object.__table__._columns))]
        for object in Object.query.all():
            table.append(list(object.__dict__.values())[1:])
        tables[Object.__tablename__] = table
    return render_template('index.html', data = tables)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInFrom()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                user.is_active = True
                login_user(user)
                return redirect(url_for('user', id = user.id))
            else:
                flash('Wrong password!')
        else:
            flash('Unknown e-mail!')
    else:
        flash('<br>'.join(['<br>'.join(e) for e in form.errors.values()]))

    return render_template('login.html', form = form)

@app.route('/edit', methods=['GET', 'POST'])
def edit():
    form = EditForm()
    if not current_user.isadmin:
        return """STOP!"""
    user_id = request.args.get('id')
    user = User.query.filter_by(id = user_id).first()
    if (request.method == 'GET'):
        form.name.default = user.name
        form.password.default = user.password
        form.email.default = user.email
        form.process()
        return render_template('edit.html', form = form, user = user)
    else:
        if form.validate_on_submit():
            name = request.form.get('name')
            password = request.form.get('password')
            user = User.query.filter_by(email = user.email).first()
            user.name = name
            user.password = password
            db.session.commit()
            flash('User saved!')
            current_user.is_active = True
            login_user(current_user)
            return render_template('edit.html', form = form, user = user)
        else:
            flash('<br>'.join(['<br>'.join(e) for e in form.errors.values()]))
    return render_template('edit.html', form = form, user = user)

@app.route('/delete-migration', methods=['GET', 'POST'])
def deleteMigration():
    form = EditForm()
    if not current_user.isadmin:
        return """STOP!"""
    id = request.args.get('id')
    user = User.query.filter_by(id = current_user.id).first()
    db.session.query(Migration).filter(Migration.id == id).delete()
    db.session.commit()
    user.is_active = True
    login_user(user)
    return redirect(url_for('user', id = user.id))


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():

    form = SignUpFrom()

    if form.validate_on_submit():
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        if not User.query.filter_by(email = email).all():
            new_user = User(name, email, password, isAdmin = False)
            db.session.add(new_user)
            db.session.commit()
            new_session = Session(request.user_agent.browser, request.user_agent.platform, user = new_user)
            db.session.add(new_session)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            flash('Email already exists!')
    else:
        flash('<br>'.join(['<br>'.join(e) for e in form.errors.values()]))

    return render_template('signup.html', form = form)


@app.route('/user', methods=['GET', 'POST'])
def user():
    user_id = request.args.get('id')
    user = User.query.filter_by(id = user_id).first()
    migrations = Migration.query.filter_by(userid = user_id).all() if not user.isadmin else Migration.query.filter_by().all()

    form = CreateUserFrom() if user.isadmin else None
    users = User.query.filter_by().all() if user.isadmin else None
    migrForm = CreateMigrationFrom() if not user.isadmin else None
    if form:
        if form.validate_on_submit():
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            make_admin = request.form.get('make_admin') == 'y' 
            if not User.query.filter_by(email = email).all():
                new_user = User(name, email, password, isAdmin = make_admin)
                db.session.add(new_user)
                db.session.commit()
                new_session = Session(request.user_agent.browser, request.user_agent.platform, user = new_user)
                db.session.add(new_session)
                db.session.commit()
                flash('User created!')
            else:
                flash('Email already exists!')
        else:
            flash('<br>'.join(['<br>'.join(e) for e in form.errors.values()]))

    return render_template('user.html', form = form, data = {'name': user.name}, user = current_user, migrations = migrations, migrForm=migrForm, users = users)

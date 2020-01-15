from flask import Blueprint, request, flash, url_for, redirect
from app import db
from flask_login import login_user, logout_user
from models import Student


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST'])
def login():
    form = LogInFrom()
    if form.validate_on_submit():
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('user', id = user.id))
            else:
                flash('Wrong password!')
        else:
            flash('Unknown e-mail!')
    else:
        flash('<br>'.join(['<br>'.join(e) for e in form.errors.values()]))

    return render_template('login.html', form = form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
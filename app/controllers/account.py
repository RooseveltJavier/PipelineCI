import random
from flask import (
    Blueprint, flash, render_template, 
    redirect, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from app.database import db_session
from app.models import User

bp = Blueprint('account', __name__, template_folder='templates')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        pwd = request.form['password']

        user = User.query.filter(User.login == login).first()

        if user is None or not check_password_hash(user.password, pwd):
            flash('Usuario o contraseña incorrectos', 'error')
        else:
            signin(user)
            return redirect(url_for('index'))

    return render_template('account/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    

def signin(user):
    session.clear()
    session['user_id'] = user.id
    session['user_login'] = user.login

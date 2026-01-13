from flask import Blueprint, current_app, flash, \
    redirect, render_template, request, session, url_for
from app import authorize
from app.models import Client, User
from app.database import db_session
from sqlalchemy.orm import joinedload

bp = Blueprint('clients', __name__, template_folder='templates')


@bp.route('/clients')
@authorize()
def index():
    list = Client.query.all()

    return render_template('clients/index.html', list=list)


@bp.route('/clients/create', methods=['GET', 'POST'])
@authorize()
def create():
    if request.method == 'POST':
        client = Client()     

        client.name = request.form['name']
        client.address = request.form['address']
        client.cedula = request.form['cedula']

        db_session.add(client)
        db_session.commit()

        return redirect(url_for('clients.index'))

    return render_template('clients/form.html')


@bp.route('/clients/delete/<int:id>', methods=['POST'])
@authorize()
def delete(id):
    client = Client.query.filter(Client.id == id).first()

    db_session.delete(client)
    db_session.commit()

    return redirect(url_for('clients.index'))

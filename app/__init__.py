import logging
import os
from flask import flash, Flask, redirect, render_template, session, url_for
from functools import wraps


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_object('config')

        handler = logging.FileHandler(os.path.join(app.instance_path, 'app.log'))
        handler.setLevel(logging.WARNING)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
        app.logger.addHandler(handler)
    else:
        app.config.from_mapping(test_config)

    if not os.path.isdir(app.instance_path):
        os.makedirs(app.instance_path)

    with app.app_context():
        from . import database
        
        database.init_app(app)

    from app.controllers import account, clients
    app.register_blueprint(account.bp)
    app.register_blueprint(clients.bp)


    @app.route('/')
    def index():   
        return render_template('home.html')


    return app


def authorize():
    def decorator(view):
        @wraps(view)
        def decorated_view(*args, **kwargs):
            if not session.get('user_id'):
                return redirect(url_for('account.login'))
            return view(*args, **kwargs)        
        return decorated_view
    return decorator
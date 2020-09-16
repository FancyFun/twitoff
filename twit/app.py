from flask import Flask, render_template
from .model import DB, User
from .twitter import insert_example_users
from os import getenv


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())

    @app.route('/update')
    def update():
        insert_example_users()
        return render_template('base.html', title="users updated!", users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')
    return app
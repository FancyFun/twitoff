from flask import Flask, render_template, request
from .model import DB, User
from .twitter import insert_example_users
from os import getenv
from .predict import predict_user


def create_app():

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title="Home", users=User.query.all())
    
    @app.route('/compare', methods=['POST'])
    def compare():
        user0, user1 = sorted([request.values['user0'], request.values['user1']])

        if user0 == user1:
            message = 'Cannot compare a user to themselves'
        else:
            prediction = predict_user(user0, user1, request.values['tweet_text'])
            message = "{} is more likely to be said by {} than {}".format(
                request.values['tweet_text'], user1 if prediction else user0, user0 if prediction else user1)

        return render_template('predictions.html', title='prediction', message=message)


    @app.route('/update')
    def update():
        insert_example_users()
        return render_template('base.html', title="users updated!", users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='Reset Database')
    
    @app.route('/user', methods=['POST'])
    @app.route('/user.<name>', methods=['GET'])
    def update2(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = 'User {} successfully added!'.format(name)

            tweets = Usesr.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name, e)

            tweets = []


        return render_template('base.html', title="Compare the two", users=User.query.all())

    
    return app
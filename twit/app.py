from flask import Flask, render_template
from model import DB, User, insert_example_users, Tweet


#def create_app():
#    app = Flask(__name__)

#    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
#    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#    DB.init_app(app)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

DB.init_app(app)


@app.route('/')
def root():
    DB.drop_all()
    DB.create_all()
    insert_example_users()


    users = User.query.all()

    return render_template('base.html', title="Home", users=User.query.all())

    return app

if __name__ == "__main__":
    app.run()
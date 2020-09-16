from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class User(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key= True)
    name = DB.Column(DB.String, nullable=False)
    newest_tweet_id = DB.Column(DB.BigInteger)

    def __repr__(self):
        return '-User {}-'.format(self.name)
    

class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True)
    text = DB.Column(DB.Unicode(300))

    embedding = DB.Column(DB.PickleType, nullable = False) 


    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    user = DB.relationship('User', backref=DB.backref('tweets', lazy=True))

    def __repr__(self):
        return '-Tweet {}-'.format(self.text)
    
def insert_example_users():
    nick = User(id=1, name='Nick')
    elon = User(id=2, name='Elon')
    DB.session.add(nick)
    DB.session.add(elon)
    DB.session.commit()

def tweetTest():
    tweet1 = Tweet(id=3, text="yayayaya", user_id=1)
    DB.session.add(tweet1)
    DB.session.commit()

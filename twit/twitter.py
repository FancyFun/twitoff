import tweepy
import basilica
from .model import DB, Tweet, User
from os import getenv

######requests - JSON - flask

TWITTER_USERS = ['calebhicks','elonmusk','rrherr','SteveMartinToGo', 'alyankovic','nasa', 'sadserver', 'jkhowland', 'austen', 'common_squirrel', 'KenJennings', 'conanobrien', 'big_ben_clock', 'IAM_SHAKESPEARE']

TWITTER_AUTH = tweepy.OAuthHandler(getenv('TWITTER_API_KEY'), getenv('TWITTER_API_KEY_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(getenv('BASILICA_KEY'))

def add_or_update_user(username):
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = (User.query.get(twitter_user.id)) or User(id=twitter_user.id, name=username)
        DB.session.add(db_user)

        tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended', since_id = db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id

        for tweet in tweets:
            embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.full_text, embedding=embedding)
            db_user.tweets.append(db_tweet)

    except Exception as e:
        print('PROCESSING {}: {}'.format(username, e))
        raise e 

    else:
        DB.session.commit()

def insert_example_users():
    DB.drop_all()
    DB.create_all()
    for users in TWITTER_USERS:
        add_or_update_user(users)
    #add_or_update_user('elonmusk')
    #add_or_update_user('jackblack')
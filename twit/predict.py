import numpy as np
from sklearn.linear_model import LogisticRegression
from .model import User
from .twitter import BASILICA

def predict_user(user0_name, user1_name, tweet_text):
  user0 = User.query.filter(User.name == user0_name).one()
  user1 = User.query.filter(User.name == user1_name).one()
  user0_embeddings = np.array([tweet.embedding for tweet in user0.tweets])
  user1_embeddings = np.array([tweet.embedding for tweet in user1.tweets])

  embeddings = np.vstack([user0_embeddings, user1_embeddings])
  labels = np.concatenate([np.zeros(len(user0.tweets)), np.ones(len(user1.tweets))])

  log_reg = LogisticRegression().fit(embeddings, labels)
  tweet_embedding = BASILICA.embed_sentence(tweet_text, model='twitter')
  return log_reg.predict(np.array(tweet_embedding).reshape(1,-1))

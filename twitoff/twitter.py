import os
import tweepy
import spacy
from .models import db, User, Tweet

# Authenticates us and allows us to user the Twitter API
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_KEY_SECRET = os.getenv("TWITTER_API_KEY_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_KEY_SECRET)
api = tweepy.API(auth)

#nlp = spacy.load("my_model")

#def vectorize_tweet(tweet_text):
#    return nlp(tweet_text).vector

def add_or_update_user(username):

    twitter_user = api.get_user(username)

    db_user = User.query.get(twitter_user.id) or User(id=twitter_user.id, username=username)
    db.session.add(db_user)

    tweets = twitter_user.timeline(
            count=100,
            exclude_replies=True,
            include_rts=False,
            tweet_mode="extended",
            since_id=db_user.newest_tweet_id
        )

    if tweets:
        db_user.newest_tweet_id = tweets[0].id

    for tweet in tweets:
        db_tweet = Tweet(id=tweet.id, text=tweet.full_text)
        db_user.tweets.append(db_tweet)
        db.session.add(db_tweet)

    db.session.commit()

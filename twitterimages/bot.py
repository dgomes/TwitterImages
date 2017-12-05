import logging
import tweepy
from config import p as Config

class Bot:
    def __init__(self):
    
        consumer_key = Config.get("twitter", "consumer_key")
        consumer_secret = Config.get("twitter", "consumer_secret")

        access_token = Config.get("twitter", "access_token")
        access_token_secret = Config.get("twitter", "access_token_secret")

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self.api = tweepy.API(auth)


    def publish(self, filename, status=None, in_reply_to_status_id=None):
        status = self.api.update_with_media(filename, status, in_reply_to_status_id)
        logging.debug(status)


import logging
logging.getLogger('tweepy').setLevel(logging.WARN)
logging.getLogger('urllib3').setLevel(logging.WARN)
logging.getLogger('requests_oauthlib').setLevel(logging.WARN)
logging.getLogger('oauthlib').setLevel(logging.WARN)
import tweepy
from config import p as Config
from db import Status 

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
        logging.debug("Published new status: {}".format(status.id_str))
        return status.id_str

    def get_favs(self, status_id):
        s = self.api.get_status(status_id)
        return s.favorite_count

    def replies(self, min_fav=1):
        user_timeline = self.api.user_timeline()
        if len(user_timeline) == 0:
            return dict()
        last = min([status.id_str for status in user_timeline])
        me = self.api.me()

        replies = dict()

        for t in self.api.search(q="@{}".format(me.screen_name), since_id=last):
            if t.favorite_count >= min_fav:
                if not t.in_reply_to_status_id_str in replies:
                    replies[t.in_reply_to_status_id_str] = []

                replies[t.in_reply_to_status_id_str].append(Status(twitter_status_id=t.id_str, twitter_status_text=t.text))
      
        return replies

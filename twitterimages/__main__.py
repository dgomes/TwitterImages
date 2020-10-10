import magic
import coloredlogs, logging
import sys
import argparse
import os
from bot import Bot 
from db import DB,Status
from config import p as Config

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.DEBUG)
coloredlogs.install(level='DEBUG')

def post(bot, db):
    try: 
        img = db.get_image()
        logging.info("Posting: {}".format(img))
        if False: #len(img.statuses):
            new_caption = (0,img.caption)
            for s in img.statuses:
                try:
                    favs = bot.get_favs(s.twitter_status_id)
                    if favs > new_caption[0]:
                        new_caption = (favs, s.twitter_status_text)
                except Exception as e:
                    logging.error("%s ignoring", e)
            img.caption = new_caption[1].replace(Config.get("twitter", "screen_name"), '')
        
        if img.caption != None: 
            status = img.caption
        else:
            status = Config.get("messages", "missing_caption")
        status_id = bot.publish(os.path.join(Config.get("main", "images_dir"),img.filename), status)
        img.times_published+=1
        img.statuses.append(Status(twitter_status_id=status_id, twitter_status_text=status))
        logging.info("Updating image to {}".format(img))
        db.update(img)
    except Exception as e:
        logging.error("Error while posting: %s", e)

def sync(db):
    db.sync_dir(Config.get("main", "images_dir"))

def process_replies(bot, db):
    replies = bot.replies(min_fav=1)
    logging.debug("Replies: {}".format(replies))
    for image_status_id,replies in replies.items():
        img = db.get_image(image_status_id)
        if img==None:
            logging.error("No img for {}".format(image_status_id))
            continue
        logging.info("Replies for {}".format(img))
        for reply in replies:
            if db.get_status(reply.twitter_status_id) != False: #don't process replies we alread processed
                logging.debug("Ignoring reply: {}".format(reply))
                continue
            logging.info("Reply: {}".format(reply))
            if not reply.twitter_status_id in [s.twitter_status_id for s in img.statuses]:
                img.statuses.append(reply)
                db.update(img)

def main(args):
    logging.info("TwitterImage v0") 
 
    b = Bot()
    db = DB(Config.get("main","db_url"))
    if args.sync:
        sync(db)
    if args.post:
        post(b, db)
    if args.replies:
        process_replies(b, db)

    if args.follow_search or args.follow_location:
        users = b.search_users(args.follow_search, args.follow_location)
        for u in users:
            if not u.following:
                logging.info("Following {}".format(u.screen_name))
                b.follow(u.id_str)

    if args.follow:
        u = b.follow(args.follow)
        logging.info("Following {}".format(u.screen_name))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter Image Bot")
    parser.add_argument('--sync', help='syncronize imagedir with database', action='store_true')
    parser.add_argument('--replies', help='syncronize replies', action='store_true')
    parser.add_argument('--post', help='post an image', action='store_true')
    parser.add_argument('--follow_search', help='follow users talking about', action='store')
    parser.add_argument('--follow_location', help='follow users with provided location', action='store')
    parser.add_argument('--follow', help='follow user', action='store')

    args = parser.parse_args()
    sys.exit(main(args))

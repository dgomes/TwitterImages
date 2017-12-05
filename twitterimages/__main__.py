import logging
import sys
import argparse
import os
from bot import Bot 
from images import DB
from config import p as Config

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

def main(args):
    logging.info("TwitterImage v0") 
    images_dir = Config.get("main", "images_dir") 
 
    db = DB(Config.get("main","db_url"))
    if args.sync:
        db.sync_dir(images_dir)
    img = db.get_image()
    logging.info(img)
    b = Bot()
    if img.status != None: 
        status = img.status
    else:
        status = Config.get("messages", "missing_status")
    b.publish(os.path.join(images_dir,img.filename), status)
    db.update_image(img)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Twitter Image Bot")
    parser.add_argument('--sync', help='syncronize imagedir with database', default=False)

    args = parser.parse_args()
    sys.exit(main(args))

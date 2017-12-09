import magic 
import sys
import logging
import os
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy import create_engine
from sqlalchemy_utils.functions import database_exists
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
logging.getLogger('sqlalchemy').setLevel(logging.WARN)
from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    filename = Column(String(280))
    caption = Column(String(280))
    author = Column(String(80))
    times_published = Column(Integer, default=0)

    def __repr__(self):
        return "<Image [{}] {} : {}>".format(self.filename, self.caption, self.statuses)

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    twitter_status_id = Column(String, unique=True)
    twitter_status_text = Column(String(280))
    image_id = Column(Integer, ForeignKey('images.id'))

    image = relationship("Image", back_populates="statuses")
    

    def __repr__(self):
        return "<Status [{}] {}>".format(self.twitter_status_id, self.twitter_status_text)

class DB():
    def __init__(self,db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        Image.statuses = relationship("Status", order_by=Status.id, back_populates="image")
        if not database_exists(db_url): 
            Base.metadata.create_all(self.engine)
        self.session = self.Session()

    def sync_dir(self,dirname="images"):
        logging.info("Syncing directory <{}>".format(dirname))
        for f in os.listdir(dirname):
            if os.path.isfile(os.path.join(dirname,f)) and "image" in magic.from_file(os.path.join(dirname,f), mime=True):
                if self.session.query(exists().where(Image.filename==str(f))).scalar() == 0:
                    i = Image(filename=str(f))    
                    self.session.add(i)
                    logging.info("Adding {}".format(f)) 
                else:
                    logging.info("Skipping {}".format(f)) 
            else:
                logging.debug("ignoring {}".format(f))
        self.session.commit()

    def get_image(self, status_id=None):
        try:
            if status_id != None:
                s = self.session.query(Status).filter_by(twitter_status_id=status_id).one()
                i = self.session.query(Image).filter_by(id=s.image_id).one()
            else:
                i = self.session.query(Image).order_by(Image.times_published)[0]
            return i
        except Exception as e:
            logging.error(e)
            logging.error("No Images available")
            sys.exit(2)

    def update(self, image):
        self.session.add(image)
        self.session.commit()
 
if __name__ == '__main__':
    db = DB("images.sqlite3")
    db.sync_dir()

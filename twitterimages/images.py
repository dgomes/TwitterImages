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
from sqlalchemy.orm import sessionmaker

class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    filename = Column(String(280))
    status = Column(String(280))
    author = Column(String(80))
    times_published = Column(Integer, default=0)

    def __repr__(self):
        return "{} - {}".format(self.filename, self.status)


class DB():
    def __init__(self,db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)
        if not database_exists(db_url): 
            Base.metadata.create_all(self.engine)
        

    def sync_dir(self,dirname="images"):
        session = self.Session()
        logging.info("Syncing directory <{}>".format(dirname))
        for f in os.listdir(dirname):
            if session.query(exists().where(Image.filename==str(f))).scalar() == 0:
                i = Image(filename=str(f))    
                session.add(i)
                logging.info("Adding {}".format(f)) 
            else:
                logging.info("Skipping {}".format(f)) 

        session.commit()

    def get_image(self):
        session = self.Session()
        i = session.query(Image).order_by(Image.times_published)[0]
        return i

    def update_image(self, image):
        session = self.Session()
        i = session.query(Image).filter_by(filename=image.filename).one()
        i.times_published+=1  
        session.commit()
 
if __name__ == '__main__':
    db = DB("images.sqlite3")
    db.sync_dir()

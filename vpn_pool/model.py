from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,Column,Integer,String,Float,DateTime
import datetime


Base = declarative_base()

class Vpn(Base):
    def __init__(self,ip,port,protocol,anony,country,region,city,available,respeed,trspeed):
        self.ip = ip
        self.port = port
        self.protocol = protocol
        self.anony = anony
        self.country = country
        self.region = region
        self.city = city
        self.available = available
        self.respeed = respeed
        self.trspeed = trspeed

    __tablename__ = 'vpns'
    id = Column(Integer, primary_key=True)
    ip = Column(String(32))
    port = Column(Integer)
    protocol = Column(String(10))
    anony = Column(String(10))
    country = Column(String(20))
    region = Column(String(30))
    city = Column(String(30))
    available = Column(Float)
    respeed = Column(Float)
    trspeed = Column(Float)
    createTime = Column(DateTime,default=datetime.datetime.utcnow())

    def __repr__(self):
        return auto_repr(self)

engine = create_engine('mysql+pymysql://root:123456@localhost:3307/vpns?charset=utf8mb4',pool_recycle=3600)
# Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()

def auto_repr(obj):
    try:
        items = ('{} = {}'.format(k,v) for k,v in obj.__dict__.items())
        return '<{}:{}>'.format(obj.__class__.__name__, ', '.join(items))
    except AttributeError:
        return repr(obj)
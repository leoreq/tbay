#Setting up conection from python file to SQL Alchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

#Setting up the Model -> This will create relevant tables
from datetime import datetime
from sqlalchemy import Table,Column, Integer, String, DateTime, Float,ForeignKey,desc
from sqlalchemy.orm import relationship

class User(Base):
    """User model represented by User class. Base subclass will register the model with a declarative base"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items=relationship("Item",backref="owner")
    bids=relationship("Bid",backref="bidder")
    

    
class Item(Base):
    """Item model represented by Item class. Base subclass will register the model with a declarative base"""
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime,nullable=False, default=datetime.utcnow)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    bids=relationship("Bid",backref="item")

class Bid(Base):
    """Bid model represented by Bid class. Base subclass will register the model with a declarative base"""
    __tablename__ = "bids"

    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    item_id=Column(Integer,ForeignKey('items.id'),nullable=False)
    #user_name=Column(Integer,ForeignKey('users.username'))
    #item_name=Column(Integer,ForeignKey('items.name'))




#Create all the tables from the declarative base: all the subclasses of the declarative base will be created
Base.metadata.create_all(engine)

leo=User(username="leonardo",password="requena")
baseball=Item(name="baseball", description="wilson baseball",owner=leo)
ale=User(username="alejandro",password="villavicencio")
alebuyball1=Bid(price=5,item=baseball,bidder=ale)
alebuyball2=Bid(price=6,item=baseball,bidder=ale)
andres=User(username="andres",password="zarecht")
andresbuyball2=Bid(price=8,item=baseball,bidder=andres)
andresbuyball1=Bid(price=4,item=baseball,bidder=andres)
session.add_all([leo,baseball,ale,alebuyball1,alebuyball2,andres,andresbuyball2,andresbuyball1])
session.commit()

print "show all the baseballs"
print session.query(Item.id,Item.name,Item.user_id).filter(Item.name=="baseball").all()
print"owners"
print session.query(User.id,User.username).all()
print "bids"
print session.query(Bid.user_id,Bid.price).order_by(desc(Bid.price)).first()


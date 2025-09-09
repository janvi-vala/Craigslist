from sqlalchemy import Column,Integer,String,ForeignKey,Float,JSON
from .database import Base
from typing import List

class Sale_item(Base):
    __tablename__="sale-items"
    id=Column(String,primary_key=True)
    loc=Column(JSON)
    userId = Column(String)
    description = Column(String, nullable=True)
    price = Column(Float)
    status = Column(String)
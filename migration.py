from app.database import SessionLocal
from sqlalchemy.orm import Session
from app import Models
from app.database import engine,Base

from app.logger import logger
import json


Models.Base.metadata.create_all(engine)

def firstTimeData():
    with open("json/item.json","r")as f:
        data=json.load(f)
    db:Session=SessionLocal()
    try:
        for item in data:
            sale_item=Models.Sale_item(
                id=item["id"],
                loc=item["loc"], 
                userId=item.get("userId"),
                description=item.get("description"),
                price=item.get("price"),
                status=item.get("status"))
            db.add(sale_item)
        db.commit()
        logger.info("Data inserted successfully from json/item.json")
    except Exception as e:
        db.rollback()
        logger.error(f"Error inserting JSON data into table: {e}") 
    finally :
        db.close()
        logger.info("Database session closed") 


if __name__=="__main__":
    firstTimeData()
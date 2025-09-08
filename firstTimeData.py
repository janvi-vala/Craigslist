from Data.database import SessionLocal
from sqlalchemy.orm import Session
from Data import Models
import json
def firstTimeData():
    with open("data/item.json","r")as f:
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
    except Exception as e:
        db.rollback()
        print("error in the json data add in the table")
    finally :
        db.close()


if __name__=="__main__":
    firstTimeData()
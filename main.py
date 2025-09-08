from fastapi import FastAPI,Query,HTTPException,status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pathlib import Path
import json
import math
from Data.schemas import sort,getSingle,getFilterDataS,getDataByRange,getItemsByFilter
from typing import Annotated


app=FastAPI()  

# DATABASE_URL = "sqlite:///./app.db"


   
    

# engine=create_engine(DATABASE_URL)
# session=sessionmaker(autocommit=False,autoflush=False ,bind=engine)
# def get_db():
#     db=session()
#     try:
#         yield db
#     finally:
#         db.close()

    
Data_File = Path("data/item.json")
def loadData ():
    if Data_File.exists():
        with open(Data_File,"r") as f:
            return json.load(f)
    return[]


def saveData (data):
    with open(Data_File ,"w") as f:
        json.dump(data,f,indent=4)
def haveSine(lat1,log1,lat2,log2):
    ER=6371.0
    lat1=math.radians(lat1)
    lat2=math.radians(lat2)
    log1=math.radians(log1)
    log2=math.radians(log2)


    dlat=lat2-lat1
    dlog=log2-log1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlog / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = ER* c
    return distance
@app.get("/sales")
def getSortedPrice(Q:Annotated[sort,Query()]):
    try:
        data=loadData()
    except Exception as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND,detail="data is not found")
    for items in data:
        if items.get("price") is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item price is not found")
    sorted_data=sorted(data,key=lambda x: x.get(Q.criteria,0),reverse=Q.reverse)
     
    return sorted_data


@app.get("/sales/getsingle")
def getSingleItem(Q:Annotated[getSingle,Query()]):
    try:
        data=loadData()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='load data is throw the error : {e}')
     
    if Q.id :
        for item in data:
            if item.get("id") is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="id is undefind in  your list of data")
            else:
                if item.get('id')==Q.id:
               
                    return item
    if Q.location:
        for item in data:
            if(item.get("loc") is None):
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="loc is is undefind in your list of the data")

            else:
                if item["loc"][0]==Q.location[0] and item["loc"][1]==Q.location[1]:
                    return item
 

@app.get("/sales/getFilterData")
def getFilterData(Q:Annotated[getFilterDataS,Query()]):
    try:
        data=loadData()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='load data is throw the error : {e}')
    if Q.Status:
        filter_item=[]
        for item in data:
            if item.get("status") is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="status is undefind in  your list of data")
            else:
                if item.get('status')==Q.Status:
                    filter_item.append(item)
        return filter_item      
    if Q.userId:
        filter_item=[]
        for item in data:
            if item.get("userId") is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="userId is undefind in  your list of data")
            else:
                if item.get('userId')==Q.userId:
                    filter_item.append(item)
        return filter_item
    

@app.get("/sales/getDataBasedOnRadius")
def getDataBasedOnRange(Q:Annotated[getDataByRange,Query()]):
    try:
        data=loadData()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='load data is throw the error like : {e}')
    if not (Q.radius or Q.lang or Q.lati):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="latitude, longitude, and radius are required"
        )
     
    
    filter_item_by_radius=[]
    for item in data:
            item_let,item_log=item.get('loc')
            distance = haveSine(Q.lati, Q.lang, item_let, item_log)
            if distance <= Q.radius:
                filter_item_by_radius.append(item)
    return filter_item_by_radius

@app.get("/sales/getItemByFilter")
def getItemByFilter(Q:Annotated[getItemsByFilter,Query()]):
    try:
        data = loadData()  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading data: {e}")

    filtered_items = data  

    result1=[]
    if Q.filterby == "price":
        if Q.lower is None or Q.upper is None:
            raise HTTPException(status_code=400, detail="Price filter requires 'lower' and 'upper'")
        
        for item in filtered_items:
            if item.get("price"):
                if item.get("price")>=Q.lower and item.get("price") <= Q.upper:
                    result1.append(item)
        filtered_items=result1
 
    elif Q.filterby == "radius":
        if Q.radius is None or Q.latitude is None or Q.longitude is None:
            raise HTTPException(status_code=400, detail="Radius filter requires 'radius', 'latitude' and 'longitude'")
        result2=[]
    
        for item in filtered_items:
            item_lat, item_lon = item["loc"]
            distance = haveSine(Q.latitude, Q.longitude, item_lat, item_lon)
            if distance <= Q.radius:
                item["distance_km"] = round(distance, 2)
                result2.append(item)
        filtered_items=result2

   
    elif Q.filterby == "description":
        
        if not Q.words:
            raise HTTPException(status_code=400, detail="Description filter requires 'words'")
        result3=[]
        
        search_words = [w.lower() for w in Q.words]

        for item in filtered_items:
            if item.get('description') and any(word in item.get('description').lower() for word in search_words):
                result3.append(item)
        filtered_items=result3
      

    else:
        raise HTTPException(status_code=400, detail="Invalid filterby value. Use 'price', 'radius', or 'desc'.")

   
    if not filtered_items:
        raise HTTPException(status_code=404, detail="No items found for given filter")

    return filtered_items

    
    
    


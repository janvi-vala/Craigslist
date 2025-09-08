from fastapi import APIRouter, Depends, HTTPException, status,Query
from sqlalchemy.orm import Session
from sqlalchemy import Float, and_,or_

from Data import Models
from Data.database import get_db
from Data.schemas import sort,getSingle,getDataByRange,getFilterDataS,getItemsByFilter
from typing import Annotated
import math


# all api end point are here
router = APIRouter(
    prefix="/sales",
    tags=["Sales"]
)
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
@router.get("/")
def get_all_sales(q:Annotated[sort,Query()],db: Session = Depends(get_db)):
    query = db.query(Models.Sale_item)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data is not found")
     
    if not hasattr(Models.Sale_item,q.criteria):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="criteria is not found ")
    
    sort_column = getattr(Models.Sale_item, q.criteria)
    if q.reverse:
        query = query.order_by(sort_column.desc()).all()
    else:
        query = query.order_by(sort_column.asc()).all()
     
    return query




@router.get("/getsingle")
def getSingleItem(Q:Annotated[getSingle,Query()],db: Session = Depends(get_db)):
    query = db.query(Models.Sale_item)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data is not found")
        
            
    if Q.id :
        sale=query.filter(Models.Sale_item.id==Q.id).all()
    if Q.location:
        location_str = str(Q.location)   
        sale = query.filter(Models.Sale_item.loc == location_str).first()
    return sale 


@router.get("/getDataBasedOnRadius")
def getDataBasedOnRange(Q:Annotated[getDataByRange,Query()],db: Session = Depends(get_db)):
    if not (Q.radius or Q.lang or Q.lati):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="latitude, longitude, and radius are required"
        )
    query = db.query(Models.Sale_item)
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data is not found")
    filter_item_by_radius=[]
    for item in query :
    
        loc_value = item.loc

        item_lat, item_lng = loc_value
        distance = haveSine(Q.lati, Q.lang, item_lat, item_lng)
        if distance <= Q.radius:
            filter_item_by_radius.append(item)
    return filter_item_by_radius
    
@router.get("/getFilterData")
def getFilterData(Q:Annotated[getFilterDataS,Query()],db: Session = Depends(get_db)):
    query = db.query(Models.Sale_item)
    if Q.Status:
          sale=query.filter(Models.Sale_item.status==Q.Status).all()
    if Q.userId:
          sale=query.filter(Models.Sale_item.userId==Q.userId).all()
    if not sale:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="data is not found")
    return sale


@router.get("/getMultipleFilterData")
def getMultipleFilterData(Q:Annotated[getItemsByFilter,Query()],db: Session = Depends(get_db)):
    query=db.query(Models.Sale_item)
    if Q.filterby == "price":
       
        if Q.lower is None or Q.upper is None:
            raise HTTPException(status_code=400, detail="Price filter requires 'lower' and 'upper'")
        result = query.filter(
        Models.Sale_item.price >= Q.lower,
        Models.Sale_item.price <= Q.upper).all()
        return result
    elif Q.filterby == "radius":
        filter_item_by_radius=[]
        if Q.radius is None or Q.latitude is None or Q.longitude is None:
            raise HTTPException(status_code=400, detail="Radius filter requires 'radius', 'latitude' and 'longitude'")
        for item in query.all():
    
            loc_value = item.loc

            item_lat, item_lng = loc_value
            distance = haveSine(Q.lati, Q.lang, item_lat, item_lng)
            if distance <= Q.radius:
                    filter_item_by_radius.append(item)
        return filter_item_by_radius
    

    elif Q.filterby == "description":
        # query=db.query(Models.Sale_item)
        if not Q.words:
            raise HTTPException(status_code=400, detail="Description filter requires 'words'")
      
        
        search_words = [w.lower() for w in Q.words]
        filters = [Models.Sale_item.description.ilike(f"%{word}%") for word in search_words]
        query = query.filter(or_(*filters))
        results = query.all()
        return results

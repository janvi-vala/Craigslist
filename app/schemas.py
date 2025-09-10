from pydantic import BaseModel
from typing import List,Optional


# //all the model which are attached with the post api are definded here 
class sort(BaseModel):
    criteria:str='price'
    reverse:bool=True
# above is for query schema of json and and sort the item by then price 
class getSingle(BaseModel):
    id:str|None=None
    location:list[float]|None=None

class getFilterDataS(BaseModel):
    Status:str|None=None
    userId:str|None=None
class getDataByRange(BaseModel):
    radius:float
    lang:float
    lati:float
class getItemsByFilter(BaseModel):
    filterby: str="price"
   
    lower: Optional[float] = -1
    upper: Optional[float] = 1000
    
  
    radius: Optional[float] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
  
    words: Optional[List[str]] = "iphon"

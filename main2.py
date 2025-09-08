from fastapi import FastAPI
from Data import Models
from Data.database import engine,Base
from Data.router import sale 

app=FastAPI()
# verify that table is 
Models.Base.metadata.create_all(engine)
app.include_router(sale.router)

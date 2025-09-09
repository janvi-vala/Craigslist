from fastapi import FastAPI
from app import Models
from app.router import sale,sale_json

app=FastAPI()
app.include_router(sale.router)
app.include_router(sale_json.router)

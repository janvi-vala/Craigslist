from fastapi import FastAPI
from app import Models
from app.router import sale,sale_json
import uvicorn

app=FastAPI()
app.include_router(sale.router)
app.include_router(sale_json.router)


if __name__=="__main__":
    uvicorn.run(app,host="127.0.0.1",port="10001")
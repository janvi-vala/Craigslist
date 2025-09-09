from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base
# from sqlalchemy.ext.declarative import 


DataBaseURL="sqlite:///./item.db"
engine=create_engine(DataBaseURL,echo=True,future=True)
SessionLocal=sessionmaker(bind=engine,autoflush=False,autocommit=False,future=True)
Base=declarative_base()




def get_db():
    db=SessionLocal()
    try:

      yield db
    finally:
      db.close()

      
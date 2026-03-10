from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os
load_dotenv()



# create engine
engine = create_engine(os.getenv("DB_URL"))

# create session
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# create your Base
Base = declarative_base()

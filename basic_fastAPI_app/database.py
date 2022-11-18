from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

psql_db = "fastapi"
psql_url = f"postgresql://postgres:mypass@127.0.0.1:5432/{psql_db}"

engine = create_engine(psql_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


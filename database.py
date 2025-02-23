# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cria o banco de dados SQLite
engine = create_engine('sqlite:///academia.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://lin:G7jG7bnDn2VTxZjbAARNThnrCmFAGXnG@dpg-d3i3htbe5dus738psntg-a/tlce_db")

engine = create_engine(DATABASE_URL, connect_args={'options': '-csearch_path=public'})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:

        db.close()

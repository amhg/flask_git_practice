from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

DB_URL = "mysql+mysqlconnector://flaskuser:flaskpass@localhost/flaskdb"

engine = create_engine(DB_URL)

db_session = scoped_session(
    sessionmaker(autocommit=False,
                autoflush=False,
                bind=engine))

Base = declarative_base()

def init_db():
    import app.model.db
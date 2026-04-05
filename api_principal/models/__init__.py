import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models.base import Base
from models.endereco import Endereco

db_path = "database/"
if not os.path.exists(db_path):
    os.makedirs(db_path)

db_url = f"sqlite:///{db_path}db.sqlite3"

engine = create_engine(db_url, echo=False)

Session = sessionmaker(bind=engine)

if not database_exists(engine.url):
    create_database(engine.url)

Base.metadata.create_all(engine)
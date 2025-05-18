
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost/employee_catalog"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

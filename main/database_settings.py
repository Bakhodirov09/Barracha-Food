import databases
import sqlalchemy
from sqlalchemy.orm import declarative_base
from data.config import env
from .config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
# Database configuration
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize the database
database = databases.Database(DATABASE_URL)
Base = declarative_base()
metadata = sqlalchemy.MetaData()
# Create the engine
engine = sqlalchemy.create_engine(DATABASE_URL)

# Ensure that Base.metadata uses the correct engine to create all tables
Base.metadata.create_all(engine)
from sqlalchemy import create_engine
DATABASE_URI = "postgresql://postgres:9782157241@localhost:5455/movies"
engine = create_engine(DATABASE_URI)
from sqlalchemy import create_engine, Column, String, Float, Integer
from sqlalchemy.orm import declarative_base, sessionmaker

SQLITE_DATABASE_URL = "sqlite:///./sqlite3.db"

engine = create_engine(SQLITE_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer(), primary_key=True, unique=True, autoincrement=True)
    description = Column(String(500))
    amount = Column(Float())

    def __repr__(self):
        return self.description


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

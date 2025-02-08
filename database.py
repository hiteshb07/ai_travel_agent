# database.py
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True)
    event_date = Column(Date, nullable=False)
    event_name = Column(String, nullable=True)
    holiday_flag = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Event(date={self.event_date}, name={self.event_name}, holiday={self.holiday_flag})>"

# Create a SQLite engine and session
engine = create_engine('sqlite:///calendar_events.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)

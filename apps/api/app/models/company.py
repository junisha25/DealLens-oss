from sqlalchemy import Column, Integer, String

from app.db.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    ticker = Column(String(20), unique=True, nullable=False)

    cik = Column(String(20))

    name = Column(String(255), nullable=False)

    sector = Column(String(255))

    industry = Column(String(255))

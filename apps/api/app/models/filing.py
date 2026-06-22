from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base


class Filing(Base):
    __tablename__ = "filings"

    id = Column(Integer, primary_key=True, index=True)

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False
    )

    form_type = Column(String(20), nullable=False)

    filing_date = Column(String(20))

    accession_number = Column(String(50))

    filing_url = Column(String(500))

    company = relationship(
        "Company",
        back_populates="filings"
    )

from pydantic import BaseModel


class FilingCreate(BaseModel):
    company_id: int
    form_type: str
    filing_date: str | None = None
    accession_number: str | None = None
    filing_url: str | None = None


class FilingResponse(BaseModel):
    id: int
    company_id: int
    form_type: str
    filing_date: str | None = None
    accession_number: str | None = None
    filing_url: str | None = None

    class Config:
        from_attributes = True

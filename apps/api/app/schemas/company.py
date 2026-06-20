from pydantic import BaseModel


class CompanyCreate(BaseModel):
    ticker: str
    name: str
    cik: str | None = None
    sector: str | None = None
    industry: str | None = None


class CompanyResponse(BaseModel):
    id: int
    ticker: str
    name: str
    cik: str | None = None
    sector: str | None = None
    industry: str | None = None

    class Config:
        from_attributes = True

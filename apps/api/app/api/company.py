from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyResponse

from app.models.filing import Filing
from app.services.sec_service import get_recent_filings

router = APIRouter(prefix="/companies", tags=["Companies"])


@router.post("/", response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    db_company = Company(
        ticker=company.ticker,
        name=company.name,
        cik=company.cik,
        sector=company.sector,
        industry=company.industry
    )

    db.add(db_company)
    db.commit()
    db.refresh(db_company)

    return db_company


@router.get("/", response_model=list[CompanyResponse])
def get_companies(
    db: Session = Depends(get_db)
):
    return db.query(Company).all()


@router.post("/{company_id}/sync")
def sync_company_filings(
    company_id: int,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        return {"error": "Company not found"}

    filings = get_recent_filings(company.cik)

    added = 0

    for filing in filings[:20]:

        existing = db.query(Filing).filter(
            Filing.accession_number ==
            filing["accession_number"]
        ).first()

        if existing:
            continue

        db_filing = Filing(
            company_id=company.id,
            form_type=filing["form_type"],
            filing_date=filing["filing_date"],
            accession_number=filing["accession_number"]
        )

        db.add(db_filing)
        added += 1

    db.commit()

    return {
        "message": "Sync completed",
        "filings_added": added
    }

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.company import Company
from app.models.filing import Filing
from app.schemas.company import CompanyCreate, CompanyResponse
from app.services.sec_service import get_recent_filings
from app.schemas.filing import FilingResponse

router = APIRouter(prefix="/companies", tags=["Companies"])


def sync_filings_for_company(
    db: Session,
    company: Company
):
    filings = get_recent_filings(company.cik)

    added = 0

    for filing in filings[:20]:
        existing = db.query(Filing).filter(
            Filing.accession_number ==
            filing["accession_number"]
        ).first()

        if existing:
            continue

        filing_url = (
            f"https://www.sec.gov/Archives/edgar/data/"
            f"{company.cik}/"
            f"{filing['accession_number'].replace('-', '')}/"
            f"index.html"
        )

        db_filing = Filing(
            company_id=company.id,
            form_type=filing["form_type"],
            filing_date=filing["filing_date"],
            accession_number=filing["accession_number"],
            filing_url=filing_url
        )

        db.add(db_filing)
        added += 1

    db.commit()

    return added


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
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    added = sync_filings_for_company(
        db,
        company
    )

    return {
        "message": "Sync completed",
        "filings_added": added
    }


@router.post("/sync/{ticker}")
def sync_company_by_ticker(
    ticker: str,
    db: Session = Depends(get_db)
):
    company = (
        db.query(Company)
        .filter(
            Company.ticker == ticker.upper()
        )
        .first()
    )
    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    if not company.cik:
        raise HTTPException(
            status_code=400,
            detail="Company does not have a CIK"
        )

    added = sync_filings_for_company(
        db,
        company
    )

    return {
        "message": "Sync completed",
        "ticker": company.ticker,
        "filings_added": added
    }


@router.get(
    "/{company_id}/filings",
    response_model=list[FilingResponse]
)
def get_company_filings(
    company_id: int,
    form_type: str | None = None,
    db: Session = Depends(get_db)
):
    company = db.query(Company).filter(
        Company.id == company_id
    ).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )

    query = db.query(Filing).filter(
        Filing.company_id == company_id
    )

    if form_type:
        query = query.filter(
            Filing.form_type == form_type
        )

    return query.all()

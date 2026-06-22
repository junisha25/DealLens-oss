from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.filing import Filing
from app.schemas.filing import FilingCreate, FilingResponse

router = APIRouter(
    prefix="/filings",
    tags=["Filings"]
)


@router.post("/", response_model=FilingResponse)
def create_filing(
    filing: FilingCreate,
    db: Session = Depends(get_db)
):
    db_filing = Filing(**filing.model_dump())

    db.add(db_filing)
    db.commit()
    db.refresh(db_filing)

    return db_filing


@router.get("/", response_model=list[FilingResponse])
def get_filings(
    db: Session = Depends(get_db)
):
    return db.query(Filing).all()

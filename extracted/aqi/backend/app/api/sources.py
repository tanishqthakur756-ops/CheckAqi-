"""
Sources API endpoint — returns metadata about data providers.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db import get_db_session
from ..models import Source
from ..schemas import SourceInfo

router = APIRouter(prefix="/api/sources", tags=["sources"])


@router.get("/", response_model=list[SourceInfo])
def list_sources(db: Session = Depends(get_db_session)):
    """
    List all data sources with metadata.
    """
    sources = db.query(Source).all()
    return [
        SourceInfo(
            source_name=s.source_name,
            source_url=s.source_url,
            license_note=s.license_note,
            last_synced_at=s.last_synced_at.isoformat() if s.last_synced_at else None,
        )
        for s in sources
    ]

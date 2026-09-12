from fastapi import APIRouter, File, HTTPException, UploadFile, Depends

from sqlalchemy import func, select, and_, or_
from sqlalchemy.orm import Session


from src.db.session import get_db
from src.models import Record, RecordStatus, Document, ExtractField

from src.core.constants import CONFIDENCE_THRESHOLD

import filetype
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _records_with_status(db: Session, status: RecordStatus) -> list[dict]:
    """Review-list rows for one status: record number, source file, page."""
    rows = db.execute(
        select(
            Record.id,
            Record.record_number,
            Record.page_number,
            Document.original_filename,
        )
        .join(Document)
        .where(Record.status == status)
    ).all()

    return [
        {
            "record_id": r.id,
            "record_number": r.record_number,
            "page_number": r.page_number,
            "filename": r.original_filename,
        }
        for r in rows
    ]


@router.get("")
def get_dashboard(db: Session = Depends(get_db)):
    rows = db.execute(
        select(Record.status, func.count()).group_by(Record.status)
    ).all()

    return {
        "status_counts": {status.value: count for status, count in rows},
        "needs_review": _records_with_status(db, RecordStatus.needs_review),
        "verified": _records_with_status(db, RecordStatus.verified),
    }
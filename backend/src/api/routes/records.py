from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models import ExtractField, Record, RecordStatus
from src.schemas.record import VerifyRequest

router = APIRouter(prefix="/records", tags=["records"])

@router.get("/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):

    record = db.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    fields = db.scalars(
    select(ExtractField).where(ExtractField.record_id == record_id)
    ).all()

    return {
    "record_id": record.id,
    "record_number": record.record_number,
    "page_number": record.page_number,
    "status": record.status.value,
    "filename": record.document.original_filename,
    "fields": [
    {
        "field_id": f.id,
        "name": f.attribute_name,
        "value": f.attribute_value,
        "corrected_value": f.corrected_value,
        "display_value": f.corrected_value or f.attribute_value,
        "confidence": f.confidence,
        }for f in fields
    ]
    }


@router.post("/{record_id}/verify")
def verify_record(
    record_id: int,
    body: VerifyRequest,
    db: Session = Depends(get_db),
    ):
    """
    Save a reviewer's corrections for one record and mark it verified.

    Corrections go into corrected_value; attribute_value is never overwritten.
    An empty corrections list is valid — it means the reviewer read the record
    and accepted it as extracted.

    Raises:
        HTTPException: 404 if the record does not exist, 400 if a field_id
        does not belong to this record.
    """

    record = db.get(Record, record_id)

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    fields = db.scalars(
        select(ExtractField).where(ExtractField.record_id == record_id)
    ).all()

    by_id = {f.id: f for f in fields}

    for item in body.corrections:
        field = by_id.get(item.field_id)

        # stops a correction being written onto another record's field
        if field is None:
            raise HTTPException(
                status_code=400,
                detail=f"field {item.field_id} does not belong to record {record_id}",
            )

        field.corrected_value = item.corrected_value

    record.status = RecordStatus.verified

    # nothing above touched the database until this line, so a bad field_id
    # leaves the record completely unchanged
    db.commit()

    return {
        "record_id": record.id,
        "status": record.status.value,
        "corrected_count": len(body.corrections),
    }

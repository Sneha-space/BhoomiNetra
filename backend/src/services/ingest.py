"""Turns extraction results into database rows.

The only place records and fields are written. Extraction code returns
plain data; this file stores it.
"""

import logging

from sqlalchemy.orm import Session

from src.core.constants import CRITICAL_FIELDS, EXPECTED_FIELDS, CONFIDENCE_THRESHOLD
from src.db.session import SessionLocal
from src.models import DocStatus, Document, ExtractField, Record, RecordStatus

logger = logging.getLogger(__name__)

def _clean(value) -> str | None:
    """
    Clean a string value by stripping whitespace and converting empty strings to None.
    """
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _needs_review(values: dict, confidences: dict) -> bool:
    """
    The flag rule. A record goes to a human if either:
      - a critical field (CRITICAL_FIELDS) has no value, or
      - any field scored below CONFIDENCE_THRESHOLD.

    A confidence of None means "no score given" and never flags on its own.
    """
    missing_critical = any(values[name] is None for name in CRITICAL_FIELDS)
    low_confidence = any(
        c is not None and c < CONFIDENCE_THRESHOLD for c in confidences.values()
    )
    return missing_critical or low_confidence


def add_record(
        db : Session,
        document_id : int,
        record_number : int,
        page_number : int,
        result : dict
    ) -> Record:
    """
    Add one new record and it's fields to the session. Does not commit.
    """

    unknown = set(result) - set(EXPECTED_FIELDS)
    if unknown:
        logger.warning("ignored unknown field names : %s", sorted(unknown))

    values = {}
    confidences = {}
    for name in EXPECTED_FIELDS:
        item = result.get(name) or {}
        values[name] = _clean(item.get("value"))
        confidences[name] = item.get("confidence")

    if _needs_review(values, confidences):
        status = RecordStatus.needs_review
    else:
        status = RecordStatus.auto_approved

    record = Record(
        document_id=document_id,
        record_number=record_number,
        page_number=page_number,
        status=status,
    )
    db.add(record)
    db.flush()  # gives record.id now; still undone by a rollback

    for name in EXPECTED_FIELDS:
        db.add(
            ExtractField(
                record_id=record.id,
                attribute_name=name,
                attribute_value=values[name],
                confidence=confidences[name],
            )
        )

    return record


def save_document_results(document_id : int, pages : list[list[dict]]) -> None:
    """
    Store every record found in one document, all or nothing.

    pages[0] is the list of records found on page 1, pages[1] on page 2, ...
    On any error nothing is saved, the document is marked failed, and the
    error is raised again.
    """
    db = SessionLocal()
    try:
        doc = db.get(Document, document_id)
        if doc is None:
            raise ValueError(f"document {document_id} does not exist")

        record_number = 0
        for page_number, records in enumerate(pages, start=1):
            for result in records:
                record_number += 1
                add_record(db, document_id, record_number, page_number, result)

        doc.page_count = len(pages)
        doc.status = DocStatus.done
        db.commit()

    except Exception:
        db.rollback()
        doc = db.get(Document, document_id)
        if doc is not None:
            doc.status = DocStatus.failed
            db.commit()
        raise

    finally:
        db.close()

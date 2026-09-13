"""Document routes: upload and (later) retrieval."""
import threading

from fastapi import APIRouter, File, HTTPException, UploadFile, Depends
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.models import Document

import filetype
from fastapi import APIRouter, File, HTTPException, UploadFile

from src.core.config import ALLOWED_EXTENSIONS, MAX_UPLOAD_BYTES
from src.services.storage import save_bytes
from src.core.session_maker import create_session
from src.ml.pipeline import MlPipeline
router = APIRouter(prefix="/documents", tags=["documents"])
pipeline = MlPipeline()
@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    db : Session = Depends(get_db),
    ):

    """
    Accept a land record file, validate it, and store it.

    Raises:
        HTTPException: 413 if too large, 415 if not PDF/JPG/PNG.
    """

    data = await file.read()

    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File too large")

    kind = filetype.guess(data)
    if kind is None or kind.extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=415, detail="Only PDF, JPG, PNG allowed")

    key = save_bytes(data, kind.extension)
    session = create_session(key)
    worker = threading.Thread(target=pipeline.process,args=(key,))
    worker.start()
    session["thread"] = worker


    doc = Document(
        original_filename=file.filename,
        storage_key=key,
    )

    db.add(doc)
    db.commit()
    db.refresh(doc)
    session["doc_id"] = doc.id
    return {
        "document_id": doc.id,
        "original_filename": doc.original_filename,
        "storage_key": doc.storage_key,
        "status": doc.status.value,
    }
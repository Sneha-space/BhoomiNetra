import enum
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base



class DocStatus(enum.Enum):
    """
    State of a document in the processing pipeline. A document is created with status "processing", and then either transitions to "done" or "failed" after processing.
    """

    processing = "processing"
    done = "done"
    failed = "failed"



class Document(Base):
    """
    One file gets uploaded which may hold more than one records
    """

    __tablename__ = "documents"

    id : Mapped[int] = mapped_column(primary_key=True)
    original_filename : Mapped[str]
    storage_key : Mapped[str]
    page_count : Mapped[int | None]
    status : Mapped[DocStatus] = mapped_column(default=DocStatus.processing)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

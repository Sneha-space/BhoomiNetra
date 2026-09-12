from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base

class ExtractField(Base):
    """
    One extracted value belongs to a record
    """

    __tablename__ = "fields"

    id : Mapped[int] = mapped_column(primary_key=True)
    record_id : Mapped[int] = mapped_column(ForeignKey("records.id"), index=True)
    attribute_name : Mapped[str]
    attribute_value : Mapped[str | None]
    corrected_value : Mapped[str | None]
    confidence : Mapped[float | None]
from uuid import UUID
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.db.models.base import TimeStampedModel
from pgvector.sqlalchemy import Vector

from src.db.models.document import Document


class Chunk(TimeStampedModel):
    __tablename__ = "chunks"

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id"),
        nullable=False,
        index=True,
    )

    document: Mapped["Document"] = relationship(
        "Document",
        back_populates="chunks",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    chunk_index: Mapped[int] = mapped_column(
        nullable=False,
    )

    embedding: Mapped[list[float]] = mapped_column(
        Vector(1024),
        nullable=False,
    )

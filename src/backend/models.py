"""
ETEx - Database Models

SQLAlchemy 2.0 declarative models for ETEx terminology management system.
Implements database schema from docs/REQUIREMENTS.md Section 13.

Adapted from Glossary APP (2025-10-31)
Original: vendor/glossary-app/src/backend/base_models.py
Modifications:
- Redesigned for multi-source authoritative terminology system
- Added authoritative_sources table for source management
- Added term_synonyms for thesaurus functionality
- Added translations table for cross-language mappings
- Simplified terms table for multi-language support
- Updated to SQLAlchemy 2.0 syntax (Mapped, mapped_column)
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class AuthoritativeSource(Base):
    """
    Authoritative terminology sources (IATE, NAMUR, DIN, IEC, etc.)

    Represents external and internal sources of terminology with configuration
    for different source types (API, PDF, database, manual entry).
    """
    __tablename__ = "authoritative_sources"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Core Fields
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        doc="Unique identifier: 'IATE', 'NAMUR', 'DIN', 'IEC'"
    )
    display_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        doc="Human-readable name: 'IATE - EU Terminology Database'"
    )
    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        doc="Source type: 'api', 'pdf', 'database', 'manual'"
    )

    # Tier System
    tier: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        doc="1=Authoritative (IATE, IEC), 2=Translators (DeepL), 3=Internal"
    )

    # Status
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        doc="Whether this source is currently active"
    )

    # Configuration
    config_json: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="JSON configuration for source-specific settings (API keys, endpoints, etc.)"
    )

    # Timestamps
    last_updated: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        doc="Last time this source was updated/synced"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        doc="When this source was added"
    )

    # Relationships
    terms: Mapped[list["Term"]] = relationship(
        "Term",
        back_populates="source",
        cascade="all, delete-orphan"
    )
    uploaded_documents: Mapped[list["UploadedDocument"]] = relationship(
        "UploadedDocument",
        back_populates="source",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "source_type IN ('api', 'pdf', 'database', 'manual')",
            name="ck_source_type"
        ),
        CheckConstraint(
            "tier IN (1, 2, 3)",
            name="ck_tier"
        ),
        Index("idx_authoritative_source_tier", "tier"),
        Index("idx_authoritative_source_active", "is_active"),
    )

    def __repr__(self) -> str:
        return f"<AuthoritativeSource(id={self.id}, name='{self.name}', tier={self.tier})>"


class Term(Base):
    """
    Core terminology table supporting multiple languages and sources.

    Stores individual terms with definitions, metadata, and source references.
    Supports thesaurus functionality via preferred_term_id.
    """
    __tablename__ = "terms"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Core Fields
    term: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="The actual term text"
    )
    language_code: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="ISO 639-1 language code: 'en', 'de', 'es', etc."
    )
    definition: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Definition in the same language as the term"
    )

    # Source References
    source_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("authoritative_sources.id", ondelete="SET NULL"),
        nullable=True,
        doc="Reference to authoritative source"
    )
    document_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("uploaded_documents.id", ondelete="SET NULL"),
        nullable=True,
        doc="Reference to uploaded document (if extracted from PDF)"
    )
    page_reference: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="Page number or section reference in source document"
    )

    # Linguistic Metadata
    gender: Mapped[Optional[str]] = mapped_column(
        String(1),
        nullable=True,
        doc="Grammatical gender: 'm', 'f', 'n' (for German nouns)"
    )
    part_of_speech: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        doc="Part of speech: 'noun', 'verb', 'adjective', etc."
    )
    context: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Domain/discipline context or usage notes"
    )

    # Thesaurus Support
    preferred_term_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("terms.id", ondelete="SET NULL"),
        nullable=True,
        doc="Reference to preferred term (for synonym relationships)"
    )

    # Confidence Score
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        doc="Confidence score (0.0-1.0) for auto-extracted terms"
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        onupdate=func.now()
    )

    # Relationships
    source: Mapped[Optional["AuthoritativeSource"]] = relationship(
        "AuthoritativeSource",
        back_populates="terms"
    )
    document: Mapped[Optional["UploadedDocument"]] = relationship(
        "UploadedDocument",
        back_populates="terms",
        foreign_keys=[document_id]
    )
    preferred_term: Mapped[Optional["Term"]] = relationship(
        "Term",
        remote_side=[id],
        foreign_keys=[preferred_term_id]
    )

    # Synonym relationships (bidirectional)
    synonyms_as_term1: Mapped[list["TermSynonym"]] = relationship(
        "TermSynonym",
        foreign_keys="[TermSynonym.term_id_1]",
        back_populates="term_1",
        cascade="all, delete-orphan"
    )
    synonyms_as_term2: Mapped[list["TermSynonym"]] = relationship(
        "TermSynonym",
        foreign_keys="[TermSynonym.term_id_2]",
        back_populates="term_2",
        cascade="all, delete-orphan"
    )

    # Translation relationships
    translations_as_source: Mapped[list["Translation"]] = relationship(
        "Translation",
        foreign_keys="[Translation.source_term_id]",
        back_populates="source_term",
        cascade="all, delete-orphan"
    )
    translations_as_target: Mapped[list["Translation"]] = relationship(
        "Translation",
        foreign_keys="[Translation.target_term_id]",
        back_populates="target_term",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "gender IS NULL OR gender IN ('m', 'f', 'n')",
            name="ck_gender"
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_confidence"
        ),
        Index("idx_term_language", "term", "language_code"),
        Index("idx_term_source", "source_id"),
        Index("idx_term_language_code", "language_code"),
        Index("idx_term_document", "document_id"),
    )

    def __repr__(self) -> str:
        return f"<Term(id={self.id}, term='{self.term}', lang='{self.language_code}')>"


class TermSynonym(Base):
    """
    Bidirectional synonym relationships between terms.

    Links terms that are synonyms within the same language.
    Used for thesaurus functionality and synonym detection.
    """
    __tablename__ = "term_synonyms"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Term References (bidirectional)
    term_id_1: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("terms.id", ondelete="CASCADE"),
        nullable=False,
        doc="First term in synonym pair"
    )
    term_id_2: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("terms.id", ondelete="CASCADE"),
        nullable=False,
        doc="Second term in synonym pair"
    )

    # Relationship Metadata
    relationship_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="synonym",
        doc="Type: 'synonym', 'broader', 'narrower', 'related'"
    )
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        doc="Confidence score for auto-detected synonyms (0.0-1.0)"
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    # Relationships
    term_1: Mapped["Term"] = relationship(
        "Term",
        foreign_keys=[term_id_1],
        back_populates="synonyms_as_term1"
    )
    term_2: Mapped["Term"] = relationship(
        "Term",
        foreign_keys=[term_id_2],
        back_populates="synonyms_as_term2"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("term_id_1", "term_id_2", name="uq_term_synonym_pair"),
        CheckConstraint(
            "relationship_type IN ('synonym', 'broader', 'narrower', 'related')",
            name="ck_relationship_type"
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_synonym_confidence"
        ),
        CheckConstraint(
            "term_id_1 != term_id_2",
            name="ck_different_terms"
        ),
        Index("idx_synonym_term1", "term_id_1"),
        Index("idx_synonym_term2", "term_id_2"),
    )

    def __repr__(self) -> str:
        return f"<TermSynonym(id={self.id}, term1={self.term_id_1}, term2={self.term_id_2}, type='{self.relationship_type}')>"


class Translation(Base):
    """
    Cross-language translation mappings between terms.

    Links terms in different languages with confidence scoring
    and validation tracking.
    """
    __tablename__ = "translations"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # Term References
    source_term_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("terms.id", ondelete="CASCADE"),
        nullable=False,
        doc="Source term ID"
    )
    target_term_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("terms.id", ondelete="CASCADE"),
        nullable=False,
        doc="Target term ID"
    )

    # Language Codes
    source_language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="Source language code (ISO 639-1)"
    )
    target_language: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        doc="Target language code (ISO 639-1)"
    )

    # Quality Metadata
    confidence: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=1.0,
        doc="Confidence score for translation (0.0-1.0)"
    )
    validated_by_human: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
        doc="Whether translation has been validated by human"
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now()
    )

    # Relationships
    source_term: Mapped["Term"] = relationship(
        "Term",
        foreign_keys=[source_term_id],
        back_populates="translations_as_source"
    )
    target_term: Mapped["Term"] = relationship(
        "Term",
        foreign_keys=[target_term_id],
        back_populates="translations_as_target"
    )

    # Constraints
    __table_args__ = (
        UniqueConstraint("source_term_id", "target_term_id", name="uq_translation_pair"),
        CheckConstraint(
            "source_language != target_language",
            name="ck_different_languages"
        ),
        CheckConstraint(
            "confidence >= 0.0 AND confidence <= 1.0",
            name="ck_translation_confidence"
        ),
        Index("idx_translation_source", "source_term_id"),
        Index("idx_translation_target", "target_term_id"),
        Index("idx_translation_languages", "source_language", "target_language"),
    )

    def __repr__(self) -> str:
        return f"<Translation(id={self.id}, {self.source_language}→{self.target_language}, confidence={self.confidence})>"


class UploadedDocument(Base):
    """
    Metadata for uploaded PDF/CSV/TBX documents.

    Tracks document processing status, file information, and
    links to extracted terms.
    """
    __tablename__ = "uploaded_documents"

    # Primary Key
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # File Information
    filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Storage filename (with timestamp/hash)"
    )
    original_filename: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        doc="Original uploaded filename"
    )
    file_size: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        doc="File size in bytes"
    )
    mime_type: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        doc="MIME type: 'application/pdf', 'text/csv', etc."
    )

    # Source Reference
    source_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("authoritative_sources.id", ondelete="SET NULL"),
        nullable=True,
        doc="Associated authoritative source"
    )

    # Processing Status
    processing_status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="pending",
        doc="Status: 'pending', 'processing', 'completed', 'failed'"
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        doc="Error message if processing failed"
    )

    # User Information
    uploaded_by: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        doc="User who uploaded document (for future multi-user support)"
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=func.now(),
        doc="Upload timestamp"
    )
    processed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
        doc="When processing completed (success or failure)"
    )

    # Relationships
    source: Mapped[Optional["AuthoritativeSource"]] = relationship(
        "AuthoritativeSource",
        back_populates="uploaded_documents"
    )
    terms: Mapped[list["Term"]] = relationship(
        "Term",
        back_populates="document",
        cascade="all, delete-orphan"
    )

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "processing_status IN ('pending', 'processing', 'completed', 'failed')",
            name="ck_processing_status"
        ),
        Index("idx_document_status", "processing_status"),
        Index("idx_document_source", "source_id"),
        Index("idx_document_created", "created_at"),
    )

    def __repr__(self) -> str:
        return f"<UploadedDocument(id={self.id}, filename='{self.original_filename}', status='{self.processing_status}')>"

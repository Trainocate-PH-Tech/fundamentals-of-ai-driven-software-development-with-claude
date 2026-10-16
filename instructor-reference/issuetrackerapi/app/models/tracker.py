from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base
from app.models.user import User, utcnow
from uuid import uuid4
from datetime import datetime


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    __table_args__ = (
        Index("uq_categories_name_lower", func.lower(name), unique=True),
        CheckConstraint("length(trim(name)) > 0", name="ck_category_nonblank"),
    )


class Issue(Base):
    __tablename__ = "issues"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="open")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="medium")
    category_id: Mapped[str] = mapped_column(ForeignKey("categories.id", ondelete="RESTRICT"), index=True)
    assigned_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)
    category: Mapped[Category] = relationship(lazy="selectin")
    assigned_user: Mapped[User | None] = relationship(lazy="selectin")
    __table_args__ = (
        CheckConstraint("status IN ('open','in_progress','resolved','closed')", name="ck_issue_status"),
        CheckConstraint("priority IN ('low','medium','high','critical')", name="ck_issue_priority"),
        CheckConstraint("length(trim(title)) > 0", name="ck_issue_nonblank"),
    )

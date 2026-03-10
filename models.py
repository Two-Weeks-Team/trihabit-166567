import os
from datetime import datetime
from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    Boolean,
    Text,
    Date,
    Float,
    JSON,
    ForeignKey,
    create_engine,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import uuid

# Resolve DATABASE URL with auto‑fixes
_db_url = os.getenv("DATABASE_URL", os.getenv("POSTGRES_URL", "sqlite:///./app.db"))
if _db_url.startswith("postgresql+asyncpg://"):
    _db_url = _db_url.replace("postgresql+asyncpg://", "postgresql+psycopg://")
elif _db_url.startswith("postgres://"):
    _db_url = _db_url.replace("postgres://", "postgresql+psycopg://")

# Add SSL mode for non‑localhost connections (except sqlite)
if not _db_url.startswith("sqlite") and "localhost" not in _db_url and "127.0.0.1" not in _db_url:
    if "?" in _db_url:
        _db_url += "&sslmode=require"
    else:
        _db_url += "?sslmode=require"

engine = create_engine(_db_url, echo=False, future=True, connect_args={"sslmode": "require"} if not _db_url.startswith("sqlite") else {})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
Base = declarative_base()

# Table name prefix to avoid collisions
TABLE_PREFIX = "trihabit_166567_"

def _prefixed(name: str) -> str:
    return f"{TABLE_PREFIX}{name}"

class User(Base):
    __tablename__ = _prefixed("users")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    habits = relationship("Habit", back_populates="user")
    coaching_suggestions = relationship("CoachingSuggestion", back_populates="user")
    milestones = relationship("HabitMilestone", back_populates="user")
    integrations = relationship("Integration", back_populates="user")

class Habit(Base):
    __tablename__ = _prefixed("habits")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("users") + ".id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    goal = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="habits")
    checks = relationship("HabitCheck", back_populates="habit")
    coaching_suggestions = relationship("CoachingSuggestion", back_populates="habit")
    milestones = relationship("HabitMilestone", back_populates="habit")

class HabitCheck(Base):
    __tablename__ = _prefixed("habit_checks")
    user_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("users") + ".id"), primary_key=True)
    habit_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("habits") + ".id"), primary_key=True)
    date = Column(Date, primary_key=True)
    checked_in = Column(Boolean, default=False, nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    habit = relationship("Habit", back_populates="checks")
    user = relationship("User")

class CoachingSuggestion(Base):
    __tablename__ = _prefixed("coaching_suggestions")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("users") + ".id"), nullable=False)
    habit_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("habits") + ".id"), nullable=True)
    suggestion = Column(Text, nullable=False)
    reason = Column(Text, nullable=True)
    confidence_score = Column(Float, nullable=True)
    generated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="coaching_suggestions")
    habit = relationship("Habit", back_populates="coaching_suggestions")

class HabitMilestone(Base):
    __tablename__ = _prefixed("habit_milestones")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("users") + ".id"), nullable=False)
    habit_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("habits") + ".id"), nullable=False)
    type = Column(String(50), nullable=False)
    value = Column(Integer, nullable=False)
    achieved_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="milestones")
    habit = relationship("Habit", back_populates="milestones")

class Integration(Base):
    __tablename__ = _prefixed("integrations")
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey(_prefixed("users") + ".id"), nullable=False)
    type = Column(String(50), nullable=False)
    connected_at = Column(DateTime, nullable=True)
    last_synced_at = Column(DateTime, nullable=True)
    settings = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="integrations")

# Indexes for performance (optional but useful)
Index("ix_habits_user_id", Habit.user_id)
Index("ix_habit_checks_habit_id", HabitCheck.habit_id)
Index("ix_coaching_suggestions_user_id", CoachingSuggestion.user_id)
Index("ix_habit_milestones_user_id", HabitMilestone.user_id)

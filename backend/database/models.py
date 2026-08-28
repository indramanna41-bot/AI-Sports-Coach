from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text
)

from backend.database.database import Base


class PerformanceRecord(Base):
    __tablename__ = "performance_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        String,
        index=True,
        nullable=False
    )

    sport = Column(
        String,
        index=True,
        nullable=False
    )

    overall_score = Column(
        Float,
        nullable=False
    )

    components_json = Column(
        Text,
        nullable=False
    )

    strengths_json = Column(
        Text,
        nullable=False
    )

    weaknesses_json = Column(
        Text,
        nullable=False
    )

    recommendations_json = Column(
        Text,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
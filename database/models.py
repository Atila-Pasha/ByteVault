from datetime import UTC, datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy import func


from database.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=True)

    bio = Column(String(500), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class Snippet(Base):
    __tablename__ = "snippets"

    id = Column(Integer, primary_key=True, autoincrement=True)

    title = Column(String(150), nullable=False)

    description = Column(
        String(1000),
        nullable=True,
    )

    language = Column(
        String(50),
        nullable=False,
    )

    code = Column(
        Text,
        nullable=False,
    )
    
    is_favorite = Column(Boolean, default=False, nullable=False)
    
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    view_count = Column(Integer, default=0)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
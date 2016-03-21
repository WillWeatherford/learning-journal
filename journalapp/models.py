# -*- coding: utf-8 -*-
"""Define models for learning journalapp."""
from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    String,
)

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from zope.sqlalchemy import ZopeTransactionExtension
import datetime

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    """Model Entry."""

    __tablename__ = "entries"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), unique=True)
    text = Column(Text)
    created = Column(DateTime, default=datetime.datetime.utcnow)

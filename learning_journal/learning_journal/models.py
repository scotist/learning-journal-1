import datetime
from sqlalchemy import (
    Column,
    Index,
    Integer,
    Unicode,
    UnicodeText,
    DateTime,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
)
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, unique=True, primary_key=True)
    title = Column(Unicode(128), unique=True, nullable=False)
    text = Column(UnicodeText)
    created = Column(DateTime, default=datetime.datetime.utcnow)

Index('my_index', Entry.title, unique=True, mysql_length=255)

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BlockedTag(Base):
    __tablename__ = 'blocked_tags'
    id = Column(Integer, primary_key=True)
    tag = Column(String, unique=True, nullable=False)

class PostedFic(Base):
    __tablename__ = 'posted_fics'
    id = Column(Integer, primary_key=True)
    fic_id = Column(String, unique=True, nullable=False)

class DeniedFic(Base):
    __tablename__ = 'denied_fics'
    id = Column(Integer, primary_key=True)
    fic_id = Column(String, unique=True, nullable=False)

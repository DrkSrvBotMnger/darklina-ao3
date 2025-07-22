from models import BlockedTag, PostedFic, DeniedFic
from database import SessionLocal

# --- Blocked Tags ---

def get_blocked_tags():
    session = SessionLocal()
    tags = session.query(BlockedTag).all()
    session.close()
    return [tag.tag for tag in tags]

def add_blocked_tag(tag):
    session = SessionLocal()
    if not session.query(BlockedTag).filter_by(tag=tag).first():
        session.add(BlockedTag(tag=tag))
        session.commit()
    session.close()

def remove_blocked_tag(tag):
    session = SessionLocal()
    session.query(BlockedTag).filter_by(tag=tag).delete()
    session.commit()
    session.close()

# --- Posted Fics ---

def fic_already_posted(fic_id):
    session = SessionLocal()
    exists = session.query(PostedFic).filter_by(fic_id=fic_id).first() is not None
    session.close()
    return exists

def log_posted_fic(fic_id):
    session = SessionLocal()
    session.add(PostedFic(fic_id=fic_id))
    session.commit()
    session.close()

# --- Denied Fics ---

def fic_already_denied(fic_id):
    session = SessionLocal()
    exists = session.query(DeniedFic).filter_by(fic_id=fic_id).first() is not None
    session.close()
    return exists

def log_denied_fic(fic_id):
    session = SessionLocal()
    session.add(DeniedFic(fic_id=fic_id))
    session.commit()
    session.close()

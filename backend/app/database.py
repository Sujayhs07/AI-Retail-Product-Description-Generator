import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)
    if "sqlite" in settings.DATABASE_URL:
        db_path = settings.DATABASE_URL.replace("sqlite:///", "")
        if os.path.exists(db_path):
            try:
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                cols = [r[1] for r in cursor.execute("PRAGMA table_info(generated_contents)").fetchall()]
                if cols and "candidates_data" not in cols:
                    cursor.execute("ALTER TABLE generated_contents ADD COLUMN candidates_data TEXT")
                if cols and "decision_rationale" not in cols:
                    cursor.execute("ALTER TABLE generated_contents ADD COLUMN decision_rationale TEXT")
                conn.commit()
                conn.close()
            except Exception:
                pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


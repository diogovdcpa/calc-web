from datetime import datetime

from ..db import db


class Company(db.Model):
    __tablename__ = "companies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", back_populates="company", cascade="all, delete")
    sizings = db.relationship("Sizing", back_populates="company", cascade="all, delete")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Company {self.name}>"

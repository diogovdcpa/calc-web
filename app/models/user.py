from datetime import datetime

from ..db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    company = db.relationship("Company", back_populates="users")
    sizings = db.relationship("Sizing", back_populates="owner", cascade="all, delete")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<User {self.email}>"

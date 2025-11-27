from datetime import datetime

from ..db import db


class Sizing(db.Model):
    __tablename__ = "sizings"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey("companies.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = db.relationship("Company", back_populates="sizings")
    owner = db.relationship("User", back_populates="sizings")
    assets = db.relationship(
        "Asset", back_populates="sizing", cascade="all, delete-orphan", lazy="joined"
    )

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Sizing {self.title}>"

from ..db import db


def round_to_thousands(value: int) -> int:
    """
    Arredonda sempre para cima em múltiplos de 1000.
    """
    if value <= 0:
        return 0
    remainder = value % 1000
    if remainder == 0:
        return value
    return value + (1000 - remainder)


class Asset(db.Model):
    __tablename__ = "assets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    description = db.Column(db.Text, nullable=True)
    sizing_id = db.Column(db.Integer, db.ForeignKey("sizings.id"), nullable=False)

    sizing = db.relationship("Sizing", back_populates="assets")

    def __repr__(self) -> str:  # pragma: no cover - debug helper
        return f"<Asset {self.name} x{self.quantity}>"

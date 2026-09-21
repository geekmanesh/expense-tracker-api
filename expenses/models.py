from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(100), nullable=False)
    amount = Column(Float, nullable=False)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    user = relationship(
        "User",
        back_populates="expenses",
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, description='{self.description}')>"

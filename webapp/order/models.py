from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from webapp.db import db


class OrderStatus(db.Model):
    __tablename__ = 'ED'

    id = Column(Integer, primary_key=True)
    From = Column(Date, index=True, unique=True, nullable=False)
    To = Column(Date, index=True, unique=True)
    Rate = Column(Numeric)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'ED from {self.From} is {self.Rate} Rub per Tonne'
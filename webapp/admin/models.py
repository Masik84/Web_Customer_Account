from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from webapp.db import db


class FX_rate(db.Model):
    __tablename__ = 'FX_rate'

    id = Column(Integer, primary_key=True)
    FX_date = Column(Date, index=True)
    FX_id = Column(String)
    Curr_Name = Column(String, index=True)
    Nominal = Column(Integer)
    Rate = Column(Numeric)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'FX rate {self.Rate}'
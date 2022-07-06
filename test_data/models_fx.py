from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from db import Base


class CurrencyName(Base):
    __tablename__ = 'Currency'

    id = Column(Integer, primary_key=True)
    Curr_code = Column(String, index=True, unique=True, nullable=False)
    Curr_name = Column(String)


class FX_rate(Base):
    __tablename__ = 'FX_rate'

    id = Column(Integer, primary_key=True)
    FX_date = Column(Date, index=True)
    Curr_id = Column(Integer, ForeignKey(CurrencyName.id) , index=True)
    Nominal = Column(Integer)
    Rate = Column(Numeric)

    Curr_table = relationship('CurrencyName')

    def __repr__(self):
        return f'FX rate {self.Rate}'
from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from webapp.db import db
from webapp.customer.models import Customers, PriceHierarchy, ShipTos
from webapp.product.models import Materials


class  PriceType(db.Model):
    __tablename__ = 'PriceType'

    id = Column(Integer, primary_key=True)
    Type = Column(String, unique=True, nullable=False)
    Type_desc = Column(String)

    def __repr__(self):
        return f'Price type {self.Type_desc}'



class PriceTable(db.Model):
    __tablename__ = 'PriceTable'

    id = Column(Integer, primary_key=True)
    TabN = Column(Integer, unique=True, nullable=False)
    Tab_desc = Column(String)

    def __repr__(self):
        return f'Price type {self.Tab_desc}'


class Prices(db.Model):
    __tablename__ = 'Prices'

    id = Column(Integer, primary_key=True)
    Table_id = Column(Integer, ForeignKey(PriceTable.id), nullable=False)
    PriceType_id = Column(Integer, ForeignKey(PriceType.id), nullable=False)
    ValidFrom = Column(Date, nullable=False)
    ValidTo = Column(Date, nullable=False)
    Hier_id = Column(Integer, ForeignKey(PriceHierarchy.id))
    Soldto_id = Column(Integer, ForeignKey(Customers.id))
    Shipto_id = Column(Integer, ForeignKey(ShipTos.id))
    Material_id = Column(Integer, ForeignKey(Materials.id))
    Price = Column(Numeric)
    PriceCurr = Column(String, nullable=False)
    PricingUnit = Column(Integer)
    UoM = Column(String)


    PriceType_table = relationship('PriceType')
    Hier_table = relationship('PriceHierarchy')
    Soldto_table = relationship('Customers')
    Shipto_table = relationship('ShipTos')
    Material_table = relationship('Materials')
    
    def __repr__(self):
        return f'Price {self.Price}'

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from ..db import Base, engine

#     company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=False)
db = SQLAlchemy()

class Managers(db.Model, Base):
    __tablename__ = 'Managers'
    id = Column(Integer, primary_key=True)
    Sales_Grp = Column(String, index=True, unique=True)
    AM = Column(String)
    SO_code = Column(String)
    STL = relationship('STLs')
    LoB = relationship('LoB')

    def __repr__(self):
        return f'AM id: {self.id}, AM name: {self.AM}'


class STLs(db.Model, Base):
    __tablename__ = 'STLs'
    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True)

    def __repr__(self):
        return f'STL id: {self.id}, STL name: {self.STL}'


class LoB(db.Model, Base):
    __tablename__ = 'LoB'
    id = Column(Integer, primary_key=True)
    LoB = Column(String, index=True, unique=True)    


class Customers(db.Model, Base):
    __tablename__ = 'Customers'
    id = Column(Integer, primary_key=True)
    AM_id = Column(Integer, ForeignKey(Managers), null = True)
    SoldTo = Column(Integer, index=True, unique=True)
    SoldTo_Name = Column(String)
    INN = Column(Integer)
    KPP = Column(Integer)
    ShipTo = Column(Integer, index=True)
    POD = Column(String)
    YFRP = Column(Integer)
    Payment_term = relationship("Pay_Terms")
    Sales_Grp = relationship('Managers')
    Address = relationship('Addresses')

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.SoldTo_Name}'


class Addresses(db.Model, Base):
    __tablename__ = 'Delivery_Addresses'
    id = Column(Integer, primary_key=True)
    Address_Code = Column(Integer, index=True, unique=True)
    Region = Column(String)
    City = Column(String)
    Postal_Code = Column(Integer)
    Street = Column(String)
    House = Column(String)

    def __repr__(self):
        return f'Address id: {self.id}, address: {self.Postal_Code}, {self.Region}, {self.City}, {self.Street}, {self.House}'


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
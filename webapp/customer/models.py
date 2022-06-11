from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from webapp.db import Base, engine

#     company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=False)
class LoB(Base):
    __tablename__ = 'LoB'

    id = Column(Integer, primary_key=True)
    LoB = Column(String, index=True, unique=True)

    def __repr__(self):
        return f'LoB id: {self.id}, name: {self.LoB}'


class PaymentTerms(Base):
    __tablename__ = 'PaymentTerms'

    id = Column(Integer, primary_key=True)
    Pay_term = Column(String, index=True, unique=True)
    PT_description = Column(String)

    def __repr__(self):
        return f'PaymentTerms id: {self.id}, name: {self.PT_description}'


class STLs(Base):
    __tablename__ = 'STLs'

    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True, nullable=False)

    def __repr__(self):
        return f'STL id: {self.id}, STL name: {self.STL}'


class Managers(Base):
    __tablename__ = 'Managers'
    
    id = Column(Integer, primary_key=True)
    Sales_Grp = Column(String, index=True, unique=True)
    AM_name = Column(String)
    SO_code = Column(String)
    STL_id = Column(Integer, ForeignKey(STLs.id), index=True, nullable=False)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True, nullable=False)
    STL = relationship('STLs')
    LoB = relationship('LoB')

    def __repr__(self):
        return f'AM id: {self.id}, name: {self.AM_name}'


class Customers(Base):
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True)
    AM_id = Column(Integer, ForeignKey(Managers.id), nullable=False)
    SoldTo = Column(Integer, index=True, unique=True, nullable=False)
    SoldTo_Name = Column(String)
    INN = Column(Integer, nullable=False)
    KPP = Column(Integer)
    ShipTo = Column(Integer, index=True)
    POD = Column(String)
    YFRP = Column(Integer)

    PayTerm_id = Column(Integer, ForeignKey(PaymentTerms.id), index=True, nullable=False)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True, nullable=False)
    STL_id = Column(Integer, ForeignKey(STLs.id), index=True, nullable=False)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True, nullable=False)
    STL = relationship('STLs')
    LoB = relationship('LoB')
    Payment_term = relationship("Pay_Terms")
    Sales_Grp = relationship('Managers')

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.SoldTo_Name}'


class YFRP(Base):
    __tablename__ = 'Shipto'

    id = Column(Integer, primary_key=True)
    YFRP = Column(Integer, index=True, unique=True, nullable=False)
    YFRP_Name = Column(String)

    def __repr__(self):
        return f'ShipTo id: {self.id}, name: {self.ShipTo_Name}'


class ShipTos(Base):
    __tablename__ = 'Shipto'

    id = Column(Integer, primary_key=True)
    ShipTo = Column(Integer, index=True, unique=True, nullable=False)
    ShipTo_Name = Column(String)
    SoldTo_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    YFRP_id = Column(Integer, ForeignKey(YFRP.id), nullable=False)

    def __repr__(self):
        return f'ShipTo id: {self.id}, name: {self.ShipTo_Name}'


class Addresses(Base):
    __tablename__ = 'Delivery_Addresses'

    id = Column(Integer, primary_key=True)
    Address_Code = Column(Integer, index=True, unique=True)
    Region = Column(String)
    City = Column(String)
    Postal_Code = Column(Integer)
    Street = Column(String)
    House = Column(String)
    SoldTo_id = Column(Integer, ForeignKey(Customers.id), index=True, nullable=False)
    SoldTo = relationship('Customers')

    def __repr__(self):
        return f'Address id: {self.id}, address: {self.Postal_Code}, {self.Region}, {self.City}, {self.Street}, {self.House}'



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
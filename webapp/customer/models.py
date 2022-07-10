from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from webapp.db import db


class LoB(db.Model):
    __tablename__ = 'LoB'

    id = Column(Integer, primary_key=True)
    LoB = Column(String, index=True, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.LoB


class PaymentTerms(db.Model):
    __tablename__ = 'PaymentTerms'

    id = Column(Integer, primary_key=True)
    Pay_term = Column(String, index=True, unique=True, nullable=False)
    PT_description = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.PT_description


class PriceHierarchy(db.Model):
    __tablename__ = 'PriceHierarchy'

    id = Column(Integer, primary_key=True)
    Code = Column(Integer, unique=True, nullable=False)
    Name = Column(String)

    def __repr__(self):
        return f'PriceHierarchy Name {self.Name}'


class STLs(db.Model):
    __tablename__ = 'STLs'

    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.STL


class Managers(db.Model):
    __tablename__ = 'Managers'

    id = Column(Integer, primary_key=True)
    Sales_Grp = Column(String, index=True, unique=True, nullable=False)
    AM_name = Column(String, nullable=False)
    SO_code = Column(String)

    STL_id = Column(Integer, ForeignKey(STLs.id), index=True)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True)
    is_deleted = Column(Boolean, default=False)

    STL_Table = relationship('STLs')
    LoB_Table = relationship('LoB')

    def __repr__(self):
        return self.AM_name


class Addresses(db.Model):
    __tablename__ = 'Addresses'

    id = Column(Integer, primary_key=True)
    Address_Code = Column(Integer, index=True, unique=True, nullable=False)
    Region = Column(String)
    City = Column(String)
    Postal_Code = Column(Integer)
    Street = Column(String)
    House = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"{self.Postal_Code}, {self.Region}, {self.City}, {self.Street}, {self.House}"


class YFRP(db.Model):
    __tablename__ = 'YFRP'

    id = Column(Integer, primary_key=True)
    YFRP = Column(Integer, index=True, unique=True, nullable=False)
    YFRP_Name = Column(String)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True)
    is_deleted = Column(Boolean, default=False)

    Addr_Table = relationship('Addresses')

    def __repr__(self):
        return f'YFRP id: {self.id}, name: {self.ShipTo_Name}'


class Customers(db.Model):
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True)
    SoldTo = Column(Integer, index=True, unique=True, nullable=False)
    SoldTo_Name = Column(String)
    INN = Column(String)
    KPP = Column(String, nullable=True)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True)
    PayTerm_id = Column(Integer, ForeignKey(PaymentTerms.id), index=True)
    PriceHier_id = Column(Integer, ForeignKey(PriceHierarchy.id), index=True)
    is_deleted = Column(Boolean, default=False)

    AM_Table = relationship('Managers')
    Addr_Table = relationship('Addresses')
    PayTerm_Table = relationship("PaymentTerms")
    PriceHier_Table = relationship('PriceHierarchy')

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.SoldTo_Name}'


class ShipTos(db.Model):
    __tablename__ = 'Shipto'

    id = Column(Integer, primary_key=True)
    ShipTo = Column(Integer, index=True, unique=True, nullable=False)
    ShipTo_Name = Column(String)
    POD = Column(String, nullable=True)

    SoldTo_id = Column(Integer, ForeignKey(Customers.id), index=True)
    YFRP_id = Column(Integer, ForeignKey(YFRP.id), index=True, nullable=True)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True)
    is_deleted = Column(Boolean, default=False)

    SoldTo_Table = relationship('Customers')
    YFRP_Table = relationship('YFRP')
    AM_Table = relationship('Managers')
    Addr_Table = relationship('Addresses')

    def __repr__(self):
        return f'ShipTo id: {self.id}, name: {self.ShipTo_Name}'

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


#sys.path.append(os.path.join( os.dirname(__file__), '..' ) )
from db import Base

class LoB(Base):
    __tablename__ = 'LoB'

    id = Column(Integer, primary_key=True)
    LoB = Column(String, index=True, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.LoB


class PaymentTerms(Base):
    __tablename__ = 'PaymentTerms'

    id = Column(Integer, primary_key=True)
    Pay_term = Column(String, index=True, unique=True, nullable=False)
    PT_description = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.PT_description


class STLs(Base):
    __tablename__ = 'STLs'

    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return self.STL


class Managers(Base):
    __tablename__ = 'Managers'
    
    id = Column(Integer, primary_key=True)
    Sales_Grp = Column(String, index=True, unique=True, nullable=False)
    AM_name = Column(String)
    SO_code = Column(String)

    STL_id = Column(Integer, ForeignKey(STLs.id), index=True, nullable=False)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    STL_Table = relationship('STLs')
    LoB_Table = relationship('LoB')

    def __repr__(self):
        return self.AM_name


class Addresses(Base):
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


class YFRP(Base):
    __tablename__ = 'YFRP'

    id = Column(Integer, primary_key=True)
    YFRP = Column(Integer, index=True, unique=True, nullable=False)
    YFRP_Name = Column(String)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True)
    is_deleted = Column(Boolean, default=False)

    Addr_Table = relationship('Addresses')

    def __repr__(self):
        return f'YFRP id: {self.id}, name: {self.ShipTo_Name}'

class Customers(Base):
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True)
    SoldTo = Column(Integer, index=True, unique=True, nullable=False)
    SoldTo_Name = Column(String)
    INN = Column(String, nullable=False)
    KPP = Column(String)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True, nullable=False)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True, nullable=False)
    PayTerm_id = Column(Integer, ForeignKey(PaymentTerms.id), index=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    AM_Table = relationship('Managers')
    Addr_Table = relationship('Addresses')
    PayTerm_Table = relationship("PaymentTerms")

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.SoldTo_Name}'


class ShipTos(Base):
    __tablename__ = 'Shipto'

    id = Column(Integer, primary_key=True)
    ShipTo = Column(Integer, index=True, unique=True, nullable=False)
    ShipTo_Name = Column(String)
    POD = Column(String)
    
    SoldTo_id = Column(Integer, ForeignKey(Customers.id), index=True, nullable=False)
    YFRP_id = Column(Integer, ForeignKey(YFRP.id), index=True)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True, nullable=False)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True, nullable=False)
    is_deleted = Column(Boolean, default=False)

    SoldTo_Table = relationship('Customers')
    YFRP_Table = relationship('YFRP')
    AM_Table = relationship('Managers')
    Addr_Table = relationship('Addresses')

    def __repr__(self):
        return f'ShipTo id: {self.id}, name: {self.ShipTo_Name}'
        


from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


#sys.path.append(os.path.join( os.dirname(__file__), '..' ) )
import webapp.db as db

#     company_id = Column(Integer, ForeignKey(Company.id), index=True, nullable=False)
class LoB(db.Model):
    __tablename__ = 'LoB'

    id = Column(Integer, primary_key=True)
    LoB = Column(String, index=True, unique=True)

    def __repr__(self):
        return self.LoB


class PaymentTerms(db.Model):
    __tablename__ = 'PaymentTerms'

    id = Column(Integer, primary_key=True)
    Pay_term = Column(String, index=True, unique=True)
    PT_description = Column(String)

    def __repr__(self):
        return self.PT_description


class STLs(db.Model):
    __tablename__ = 'STLs'

    id = Column(Integer, primary_key=True)
    STL = Column(String, index=True, unique=True)

    def __repr__(self):
        return self.STL


class Managers(db.Model):
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
        return self.AM_name


class Addresses(db.Model):
    __tablename__ = 'Addresses'

    id = Column(Integer, primary_key=True)
    Address_Code = Column(Integer, index=True, unique=True)
    Region = Column(String)
    City = Column(String)
    Postal_Code = Column(Integer)
    Street = Column(String)
    House = Column(String)

    def __repr__(self):
        return f"{self.Postal_Code}, {self.Region}, {self.City}, {self.Street}, {self.House}"


class YFRP(db.Model):
    __tablename__ = 'YFRP'

    id = Column(Integer, primary_key=True)
    YFRP = Column(Integer, index=True, unique=True, nullable=False)
    YFRP_Name = Column(String)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True, nullable=False)
    Addr = relationship('Addresses')

    def __repr__(self):
        return f'YFRP id: {self.id}, name: {self.ShipTo_Name}'

class Customers(db.Model):
    __tablename__ = 'Customers'

    id = Column(Integer, primary_key=True)
    SoldTo = Column(Integer, index=True, unique=True, nullable=False)
    SoldTo_Name = Column(String)
    INN = Column(String, nullable=False)
    KPP = Column(String)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True, nullable=False)
    STL_id = Column(Integer, ForeignKey(STLs.id), index=True, nullable=False)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True, nullable=False)
    PayTerm_id = Column(Integer, ForeignKey(PaymentTerms.id), index=True, nullable=False)

    AM = relationship('Managers')
    STL = relationship('STLs')
    Addr = relationship('Addresses')
    Payment_term = relationship("PaymentTerms")



    def __repr__(self):
        return f'Company id: {self.id}, name: {self.SoldTo_Name}'


class ShipTos(db.Model):
    __tablename__ = 'Shipto'

    id = Column(Integer, primary_key=True)
    ShipTo = Column(Integer, index=True, unique=True, nullable=False)
    ShipTo_Name = Column(String)
    POD = Column(String)

    SoldTo_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    YFRP_id = Column(Integer, ForeignKey(YFRP.id), nullable=False)
    AM_id = Column(Integer, ForeignKey(Managers.id), index=True, nullable=False)
    STL_id = Column(Integer, ForeignKey(STLs.id), index=True, nullable=False)
    LoB_id = Column(Integer, ForeignKey(LoB.id), index=True, nullable=False)
    Addr_id = Column(Integer, ForeignKey(Addresses.id), index=True, nullable=False)

    SoldTo = relationship('Customers')
    YFRP = relationship('YFRP')
    AM = relationship('Managers')
    STL = relationship('STLs')
    LoB = relationship('LoB')
    Addr = relationship('Addresses')

    def __repr__(self):
        return f'ShipTo id: {self.id}, name: {self.ShipTo_Name}'
        


from sqlalchemy import Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from webapp.db import db
from webapp.customer.models import Customers, ShipTos
from webapp.product.models import Materials, Plants



class OrderStatus(db.Model):
    __tablename__ = 'OrderStatus'

    id = Column(Integer, primary_key=True)
    Ord_Status = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f'Status {self.Ord_Status}'



class OrderType(db.Model):
    __tablename__ = 'OrderType'

    id = Column(Integer, primary_key=True)
    Type_code = Column(String, index=True, unique=True, nullable=False)
    Type_Name = Column(String)

    def __repr__(self):
        return f'Order type {self.Type_Name}'



class InvoiceType(db.Model):
    __tablename__ = 'InvoiceType'

    id = Column(Integer, primary_key=True)
    OrderType = Column(String, index=True, unique=True, nullable=False)
    Type_Name = Column(String)

    def __repr__(self):
        return f'Invoice type {self.Type_Name}'



class Orders(db.Model):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    OrderN = Column(String, index=True, unique=True, nullable=False)
    OrderItem = Column(Integer)
    LineItem = Column(Integer)
    Ord_type_id = Column(Integer, ForeignKey(OrderType.id), nullable=False)
    Order_date = Column(Date, nullable=False)
    Price_date = Column(Date, nullable=False)
    GI_date = Column(Date)
    Act_GI_date = Column(Date)
    Material_id = Column(Integer, ForeignKey(Materials.id), nullable=False)
    Soldto_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    Shipto_id = Column(Integer, ForeignKey(ShipTos.id), nullable=False)
    Plant_id = Column(Integer, ForeignKey(Plants.id), nullable=False)
    Ord_Status_id = Column(Integer, ForeignKey(OrderStatus.id))
    DelivryN = Column(String)
    LineQty = Column(Numeric)

    Order_type_table = relationship('OrderType')
    SoldTo_table = relationship('Customers')
    ShipTo_table = relationship('ShipTos')
    Plant_table = relationship('Plants')
    Material_table = relationship('Materials')
    Status_table = relationship('OrderStatus')

    def __repr__(self):
        return f'Order Number {self.OrderN}'



class Invoices(db.Model):
    __tablename__ = 'Invoices'

    id = Column(Integer, primary_key=True)
    InvoiceN = Column(String, index=True, unique=True)
    Item = Column(Integer)
    Inv_type_id = Column(Integer, ForeignKey(InvoiceType.id), index=True)
    Order_date = Column(Date)
    Price_date = Column(Date)
    Act_GI_date = Column(Date)
    Invoice_date = Column(Date, nullable=False)
    Material_id = Column(Integer, ForeignKey(Materials.id), nullable=False)
    Soldto_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    Shipto_id = Column(Integer, ForeignKey(ShipTos.id), nullable=False)
    Plant_id = Column(Integer, ForeignKey(Plants.id), nullable=False)
    OrderN = Column(String)
    Order_type_id = Column(Integer, ForeignKey(OrderType.id))
    DeliveryN = Column(String)
    Proceeds = Column(Numeric)
    Qty = Column(Numeric)

    Inv_type_table = relationship('InvoiceType')
    Material_table = relationship('Materials')
    SoldTo_table = relationship('Customers')
    ShipTo_table = relationship('ShipTos')
    Plant_table = relationship('Plants')
    Order_type_table = relationship('OrderType')

    def __repr__(self):
        return f'Invoice No: {self.InvoiceN}' 



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
    Type_code = Column(String, index=True, unique=True, nullable=False)
    Type_Name = Column(String)

    def __repr__(self):
        return f'Invoice type {self.Type_Name}'



class Orders(db.Model):
    __tablename__ = 'Orders'

    id = Column(Integer, primary_key=True)
    OrderN = Column(String, index=True, unique=True, nullable=False)
    Ord_type_id = Column(Integer, ForeignKey(OrderType.id), nullable=False)
    Order_date = Column(Date, nullable=False)
    Soldto_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    Shipto_id = Column(Integer, ForeignKey(ShipTos.id), nullable=False)
    Plant_id = Column(Integer, ForeignKey(Plants.id), nullable=False)

    Order_type_table = relationship('OrderType')
    SoldTo_table = relationship('Customers')
    ShipTo_table = relationship('ShipTos')
    Plant_table = relationship('Plants')

    def __repr__(self):
        return f'Order Number {self.OrderN}'



class Deliveries(db.Model):
    __tablename__ = 'Deliveries'

    id = Column(Integer, primary_key=True)
    DeliveryN = Column(String, unique=True, index=True, nullable=False)

    def __repr__(self):
        return f'Delivery id: {self.id}'   



class OpenOrderLines(db.Model):
    id = Column(Integer, primary_key=True)
    Order_id = Column(Integer, ForeignKey(Orders.id), index=True, nullable=False)
    LineItem = Column(Integer)
    Pricing_date = Column(Date, nullable=False)
    GI_date = Column(Date, nullable=False)
    Act_GI_date = Column(Date)
    Material_id = Column(Integer, ForeignKey(Materials.id), nullable=False)
    Ord_Status_id = Column(Integer, ForeignKey(OrderStatus.id))
    OrderQty = Column(Numeric)
    LineQty = Column(Numeric)

    Order_table = relationship('Orders')
    Material_table = relationship('Materials')
    Status_table = relationship('OrderStatus')

    def __repr__(self):
        return f'Order line id: {self.id}'


class Invoices(db.Model):
    __tablename__ = 'Invoices'

    id = Column(Integer, primary_key=True)
    InvoiceN = Column(String, index=True, unique=True)
    Invoice_date = Column(Date, nullable=False)
    Inv_type_id = Column(Integer, ForeignKey(InvoiceType.id), index=True)
    Order_id = Column(Integer, ForeignKey(Orders.id), index=True, nullable=False)
    Delivery_id = Column(Integer, ForeignKey(Deliveries.id))
    SoldTo_id = Column(Integer, ForeignKey(Customers.id), nullable=False)
    ShipTo_id = Column(Integer, ForeignKey(ShipTos.id), nullable=False)
    Plant_id = Column(Integer, ForeignKey(Plants.id), nullable=False)

    Inv_type_table = relationship('InvoiceType')
    Order_table = relationship('Orders')
    Delivery_table = relationship('Deliveries')
    SoldTo_table = relationship('Customers')
    ShipTo_table = relationship('ShipTos')
    Plant_table = relationship('Plants')


class InvoiceLines(db.Model):
    __tablename__ = 'InvoiceLines'

    id = Column(Integer, primary_key=True)
    Invoice_id = Column(Integer, ForeignKey(Invoices.id), index=True, nullable=False)
    Pricing_date = Column(Date, nullable=False)
    GI_date = Column(Date, nullable=False)
    Act_GI_date = Column(Date)
    Material_id = Column(Integer, ForeignKey(Materials.id), nullable=False)
    Ord_Status_id = Column(Integer, ForeignKey(OrderStatus.id))
    Qty = Column(Numeric)

    Invoice_table = relationship('Invoices')
    Material_table = relationship('Materials')
    Status_table = relationship('OrderStatus')

    def __repr__(self):
        return f'Invoice line id: {self.id}'



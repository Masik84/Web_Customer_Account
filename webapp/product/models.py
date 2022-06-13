from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from webapp.db import db


class BOs(db.Model):
    __tablename__ = 'BOs'
    id = Column(Integer, primary_key=True)
    BO_type = Column(String)


class MaterialStatus(db.Model):
    __tablename__ = 'Status'
    id = Column(Integer, primary_key=True)
    Status_code = Column(Integer, index=True, unique=True)
    Status_descr = Column(String)


class ProdSubClass(db.Model):
    __tablename__ = 'ProdSubClass'
    id = Column(Integer, primary_key=True)
    Sub_Class = Column(Integer, index=True, unique=True)
    Sub_Class_Name = Column(String)


class ProdFamily(db.Model):
    __tablename__ = 'ProdFamily'
    id = Column(Integer, primary_key=True)
    Family_Code = Column(Integer, index=True, unique=True)
    Family_Name = Column(String)
    SubClass_id = Column(Integer, ForeignKey(ProdSubClass.id), index=True, nullable=False)
    Sub_Class = relationship('ProdSubClass')


class SalProducts(db.Model):
    __tablename__ = 'SalProducts'
    id = Column(Integer, primary_key=True)
    Sal_Prod_Code = Column(Integer, index=True, unique=True)
    Sal_Prod_Name = Column(String)
    Family_id = Column(Integer, ForeignKey(ProdFamily.id), index=True, nullable=False)
    SubClass_id = Column(Integer, ForeignKey(ProdSubClass.id), index=True, nullable=False)
    Family_Code = relationship('ProdFamily')
    Sub_Class = relationship('ProdSubClass')



class Materials(db.Model):
    __tablename__ = 'Materials'
    id = Column(Integer, primary_key=True)
    Material_code = Column(String, index=True, unique=True)
    Material_Name = Column(String)
    LoB = Column(String)
    Pack_Vol = Column(Integer)
    UoM = Column(String)
    Plant = Column(String)
    Producer = Column(String)
    Comment = Column(String)
    BO_Location = Column(String)
    Production = Column(String)
    Density = Column(Integer)
    Net_Weight = Column(Integer)
    ED_type = Column(String)
    Pack_type = Column(String)
    SalProduct_id = Column(Integer, ForeignKey(SalProducts.id), index=True, nullable=False)
    Family_id = Column(Integer, ForeignKey(ProdFamily.id), index=True, nullable=False)
    SubClass_id = Column(Integer, ForeignKey(ProdSubClass.id), index=True, nullable=False)
    BO_id = Column(Integer, ForeignKey(BOs.id), index=True, nullable=False)
    Status_id = Column(Integer, ForeignKey(MaterialStatus.id), index=True, nullable=False)
    
    Sal_Prod_Code = relationship('SalProducts')
    Family_Code = relationship('ProdFamily')
    Sub_Class = relationship('ProdSubClass')
    BO_type = relationship('BOs')
    Status_code = relationship('MaterialStatus')

    def __repr__(self):
        return f'Material id: {self.id}, Material name: {self.Material_Name}'





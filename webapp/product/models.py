from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy

from webapp.db import Base, engine

db = SQLAlchemy()

class Materials(db.Model, Base):
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

    Sal_Prod_Code = relationship('SalProducts')
    Family_Code = relationship('ProdFamily')
    Sub_Class = relationship('ProdSubClass')
    BO_type = relationship('BOs')
    Status_code = relationship('Status')

    def __repr__(self):
        return f'Material id: {self.id}, Material name: {self.Material_Name}'


class SalProducts(db.Model, Base):
    __tablename__ = 'SalProducts'
    id = Column(Integer, primary_key=True)
    Sal_Prod_Code = Column(Integer, index=True, unique=True)
    Sal_Prod_Name = Column(String)
    Family_Code = relationship('ProdFamily')
    Sub_Class = relationship('ProdSubClass')


class ProdFam(db.Model, Base):
    __tablename__ = 'ProdFamily'
    id = Column(Integer, primary_key=True)
    Family_Code = Column(Integer, index=True, unique=True)
    Family_Name = Column(String)
    Sub_Class = relationship('ProdSubClass')


class ProdSubClass(db.Model, Base):
    __tablename__ = 'ProdSubClass'
    id = Column(Integer, primary_key=True)
    Sub_Class = Column(Integer, index=True, unique=True)
    Sub_Class_Name = Column(String)


class BOs(db.Model, Base):
    __tablename__ = 'BOs'
    id = Column(Integer, primary_key=True)
    BO_type = Column(String)


class MaterialStatus(db.Model, Base):
    __tablename__ = 'Status'
    id = Column(Integer, primary_key=True)
    Status_code = Column(Integer, index=True, unique=True)
    Status_descr = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
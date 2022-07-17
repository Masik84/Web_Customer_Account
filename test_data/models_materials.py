from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from db import Base


class ED(Base):
    __tablename__ = 'ED'

    id = Column(Integer, primary_key=True)
    From = Column(Date, index=True, unique=True, nullable=False)
    To = Column(Date, index=True, unique=True)
    Rate = Column(Numeric)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'ED from {self.From} is {self.Rate} Rub per Tonne'


class BOs(Base):
    __tablename__ = 'BOs'

    id = Column(Integer, primary_key=True)
    BO_type = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.BO_type}'


class Plants(Base):
    __tablename__ = 'Plant'

    id = Column(Integer, primary_key=True)
    Plant_Code = Column(String, unique=True, nullable=False)
    Plant_Name = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.Plant_Code}'


class Producers(Base):
    __tablename__ = 'Producer'

    id = Column(Integer, primary_key=True)
    Producer_Code = Column(String, unique=True, nullable=False)
    Producer_Name = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.Plant_Code}'


class MaterialStatus(Base):
    __tablename__ = 'Status'

    id = Column(Integer, primary_key=True)
    Status_code = Column(Integer, index=True, unique=True, nullable=False)
    Status_descr = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.Status_descr}'


class ProdSubClass(Base):
    __tablename__ = 'ProdSubClass'

    id = Column(Integer, primary_key=True)
    Sub_Class = Column(Integer, index=True, unique=True, nullable=False)
    Sub_Class_Name = Column(String)
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f'{self.Sub_Class_Name}'

    def to_dict(self):
        return {
            'Sub_Class': self.Sub_Class,
            'Sub_Class_Name': self.Sub_Class_Name
        }


class ProdFamily(Base):
    __tablename__ = 'ProdFamily'

    id = Column(Integer, primary_key=True)
    Family_Code = Column(String, index=True, unique=True, nullable=False)
    Family_Name = Column(String)
    SubClass_id = Column(Integer, ForeignKey(ProdSubClass.id), index=True)
    is_deleted = Column(Boolean, default=False)

    Sub_Class_table = relationship('ProdSubClass')

    def __repr__(self):
        return f'{self.Family_Name}'


class SalProducts(Base):
    __tablename__ = 'SalProducts'

    id = Column(Integer, primary_key=True)
    Sal_Prod_Code = Column(String, index=True, unique=True, nullable=False)
    Sal_Prod_Name = Column(String)
    Family_id = Column(Integer, ForeignKey(ProdFamily.id), index=True)
    is_deleted = Column(Boolean, default=False)
    
    Family_Table = relationship('ProdFamily')

    def __repr__(self):
        return f'{self.Sal_Prod_Name}'


class Materials(Base):
    __tablename__ = 'Materials'

    id = Column(Integer, primary_key=True)
    Material_code = Column(String, index=True, unique=True, nullable=False)
    Material_Name = Column(String)
    LoB = Column(String)
    Pack_Vol = Column(Numeric)
    UoM = Column(String)
    Comment = Column(String, nullable=True)
    BO_Location = Column(String)
    Production = Column(String)
    Density = Column(Numeric)
    Net_Weight = Column(Numeric)
    ED_type = Column(String)
    Pack_type = Column(String)
    is_deleted = Column(Boolean, default=False)
    
    SalProduct_id = Column(Integer, ForeignKey(SalProducts.id), index=True)
    BO_id = Column(Integer, ForeignKey(BOs.id), index=True)
    Status_id = Column(Integer, ForeignKey(MaterialStatus.id), index=True)
    Plant_id = Column(Integer, ForeignKey(Plants.id), index=True)
    Producer_id = Column(Integer, ForeignKey(Producers.id), index=True)
    
    Sal_Prod_Table = relationship('SalProducts')
    BO_Table = relationship('BOs')
    Status_Table = relationship('MaterialStatus')
    Plant_Table = relationship('Plants')
    Producer_Table = relationship('Producers')

    def __repr__(self):
        return f'Material id: {self.id}, Material name: {self.Material_Name}'





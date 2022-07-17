from numpy import s_
from db import db_session

from models_materials import Materials, ProdFamily, ProdSubClass, SalProducts


search = 'Bimula'

search_salprod = SalProducts.query.filter(SalProducts.Sal_Prod_Name.contains(search)).all()

material=Materials.query.order_by(Materials.Material_Name).filter(SalProducts.Sal_Prod_Name == search_salprod).all()
print(material)
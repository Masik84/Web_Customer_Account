
from db import db_session

from models_materials import Materials, ProdFamily, ProdSubClass, SalProducts


search = 'Bimula'

search_salprod = SalProducts.query.filter(SalProducts.Sal_Prod_Name.contains(search)).all()

# q = db_session.query(Materials, SalProducts).filter(Materials.SalProduct_id == SalProducts.id).filter(SalProducts.Sal_Prod_Name.contains(search)).all()
# print(q)

material_data = Materials.query.filter(Materials.SalProduct_id == SalProducts.id
                                                                        ).filter(SalProducts.Sal_Prod_Name.contains(search)
                                                                        ).all()

print(material_data)
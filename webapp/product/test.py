from models import SalProducts



def find_salprod_byName(search):
    find = SalProducts.query.filter(SalProducts.Sal_Prod_Name.contains(search))

    return find



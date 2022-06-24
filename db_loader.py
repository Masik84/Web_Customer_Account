from webapp import create_app
from webapp.db import db
from webapp.customer.models import Addresses
import pandas as pd


app = create_app()
data_file = 'DB_data.xlsx'

with app.app_context():
    addr_data = pd.read_excel(data_file, sheet_name='Addresses')

    data_in_db = Addresses.query.all()
    print(data_in_db)


    addr_exists = Addresses.query.filter(Addresses.Address_Code == addr_data.Address_Code).count()
    print(addr_exists)
    # if not addr_exists:
    #     addr_data.to_sql('Addresses', con=db, 
    #             if_exists='append', 
    #             index=False)
    #     addr_to_create = Addresses(
    #         Address_Code=addr_data.Address_Code, 
    #         Region=addr_data.Region, 
    #         City=addr_data.City,
    #         Postal_Code=addr_data.Postal_Code,
    #         Street=addr_data.Street,
    #         House=addr_data.House
    #         )
    #     db.session.add(addr_to_create)
    #     db.session.commit()

    # print('User with id {} added'.format(addr_to_create.id))


#############################################################################
# def read_xlsx(filename):
#     with open(filename, 'r') as f:
#         fields = ['Address_Code', 'Region', 'City', 'Postal_Code', 'Street', 'House']
#         reader = pd.read_excel(f,sheet_name='Addresses', usecols=fields)
#         addr_data = []
#         for row in reader:
#             addr_data.append(row)
#         save_addr(addr_data)

# def save_addr():
# #     db.session.bulk_insert_mappings(Addresses, addr_data)
# #     db.session.commit()

#     addr_data = pd.read_excel(data_file,sheet_name='Addresses')
#     addr_data.to_sql('Addresses', db)

# if __name__ == '__main__':
#     save_addr(data_file)
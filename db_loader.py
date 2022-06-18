from webapp import create_app
from webapp.db import db
from webapp.customer.models import Addresses
import pandas as pd


app = create_app()
data_file = 'DB_data.xlsx'

with app.app_context():
    addr_data = pd.read_excel(data_file,sheet_name='Addresses')

    addr_exists = Addresses.query.filter(Addresses.Address_Code == addr_data).count()
    if not addr_exists:
        addr_data.to_sql('Addresses', db)
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
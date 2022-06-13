from flask import Blueprint
import pandas as pd

from webapp.db import db
from webapp.customer.models import Customers, Addresses, YFRP, LoB, ShipTos, Managers, STLs, PaymentTerms

blueprint = Blueprint('сustomer', __name__, url_prefix='/customers')

data_file = '../DB_data.xlsx'

def read_xlsx(filename):
    with open(filename, 'r') as f:
        fields = ['Address_Code', 'Region', 'City', 'Postal_Code', 'Street', 'House']
        reader = pd.read_excel(f,sheet_name='Addresses', usecols=fields)
        addr_data = []
        for row in reader:
            addr_data.append(row)
        save_addr(addr_data)

def save_addr(addr_data):
    db.session.bulk_insert_mappings(Addresses, addr_data)
    db.session.commit()


if __name__ == '__main__':
    read_xlsx(data_file)
import csv
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from models_customer import Addresses, Customers, PaymentTerms, Managers, YFRP, ShipTos
from db import db_session

xls_file = 'Customer_data.xlsx'
addr_file = 'Addresses_2022-06-26.csv'
cust_file = 'Cust_Data_2022-06-26.csv'

def convert_file(filename):
    xls = pd.ExcelFile(filename)
    sheets = xls.sheet_names
    now = datetime.today().strftime('%Y-%m-%d')
    file_saved =[]
    for sheet in sheets:
        xls_data = pd.read_excel(filename, sheet_name=sheet)
        csv_filename = sheet + '_' + now + '.csv'
        np.savetxt(csv_filename, xls_data, encoding='utf-8', fmt='%s', delimiter=';')
        file_saved.append(csv_filename)

    return file_saved


def read_csv_addresses(addr_file):
    with open(addr_file, 'r', encoding='utf-8') as f:
        fields = ['Address_Code', 'Region', 'City', 'Postal_Code', 'Street', 'House']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            addr_exists = Addresses.query.filter(Addresses.Address_Code == row['Address_Code']).count()
            if addr_exists == 0:
                save_address_data(row)


def save_address_data(row):
    address = Addresses(
            Address_Code=row['Address_Code'], 
            Region=row['Region'],
            City=row['City'],
            Postal_Code=row['Postal_Code'],
            Street=row['Street'],
            House=row['House'])
    db_session.add(address)
    db_session.commit()


def get_id_Address(Address_Code):
    db_data = Addresses.query.filter(Addresses.Address_Code == Address_Code).first()
    addr_id = db_data.id
    return addr_id


def read_csv_customers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['SoldTo', 'SoldTo_Name', 'Soldto_SalesGr', 'INN', 'KPP', 'Pay_term', 'PT_description', 'ShipTo', 'Shipto_SalesGr', 'POD', 'YFRP']
        reader = csv.DictReader(f, fields, delimiter=';')
        customer_data = []
        for row in reader:
            customer_data.append(row)
        return customer_data


def save_PayTerm(data):
    processed = []
    pt_unique = []

    for row in data:
        if row['Pay_term'] not in processed:
            pt = {'Pay_term': row['Pay_term'], 'PT_description': row['PT_description']}
            pt_unique.append(pt)
            print(pt_unique)
            processed.append(pt['Pay_term'])

    for mylist in pt_unique:
        pt_exists = PaymentTerms.query.filter(PaymentTerms.Pay_term == mylist['Pay_term']).count()
        if pt_exists == 0:
            new_pay_term = PaymentTerms(Pay_term = mylist['Pay_term'], PT_description = mylist['PT_description']) 
            db_session.add(new_pay_term)
            db_session.commit()

    return pt_unique

def get_id_PT(Pay_term):
    db_data = PaymentTerms.query.filter(PaymentTerms.Pay_term == Pay_term).first()
    pt_id = db_data.id

    return pt_id


def get_id_AM(SalesGr):
    db_data = Managers.query.filter(Managers.Sales_Grp == SalesGr).first()
    am_id = db_data.id

    return am_id


def save_YFRP(data):
    processed = []
    YFRP_unique = []

    for row in data:
        if row['YFRP'] != 'nan':
            if row['YFRP'] not in processed:
                yfrp = {'YFRP': int(float(row['YFRP'])),
                            'YFRP_Name': row['SoldTo_Name']}
                YFRP_unique.append(yfrp)
                processed.append(row['YFRP'])

    for mylist in YFRP_unique:
        YFRP_exists = YFRP.query.filter(YFRP.YFRP == mylist['YFRP']).count()
        if YFRP_exists == 0:
            new_YFRP = YFRP(YFRP = mylist['YFRP'], 
                                        YFRP_Name = mylist['YFRP_Name'],
                                        Addr_id = get_id_Address(mylist['YFRP']),
                                        is_deleted = False) 
            db_session.add(new_YFRP)
            db_session.commit()

    return YFRP_unique    


def get_id_YFRP(YFRP):
    db_data = YFRP.query.filter(YFRP.YFRP == YFRP).first()
    Yfrp_id = db_data.id

    return Yfrp_id


def save_Soldto(data):
    processed = []
    soldto_unique = []

    for row in data:
        if row['SoldTo'] not in processed:
            soldto = {
                'SoldTo': int(float(row['SoldTo'])),
                'SoldTo_Name': row['SoldTo_Name'],
                'INN': int(float(row['INN'])),
                'KPP': int(float(row['KPP'])),
                'PT': row['Pay_term'],
                'AM': row['Soldto_SalesGr']}
            soldto_unique.append(soldto)
            processed.append(row['SoldTo'])
    
    for mylist in soldto_unique:
        soldto_exists = Customers.query.filter(Customers.SoldTo == mylist['SoldTo']).count()
        if soldto_exists == 0:
            new_soldto = Customers(
                SoldTo = mylist['SoldTo'],
                SoldTo_Name = mylist['SoldTo_Name'],
                INN = mylist['INN'],
                KPP = mylist['KPP'],
                AM_id = get_id_AM(mylist['AM']),
                Addr_id = get_id_Address(mylist['SoldTo']),
                PayTerm_id = get_id_PT(mylist['PT']),
                is_deleted = False)

            db_session.add(new_soldto)
            db_session.commit()
    
    return soldto_unique


def get_id_Soldto(SoldTo):
    db_data = Customers.query.filter(Customers.SoldTo == SoldTo).first()
    soldto_id = db_data.id

    return soldto_id


def save_Shipto(data):
    processed = []
    shipto_unique = []

    for row in data:
        if row['ShipTo'] not in processed:
            shipto = {
                'ShipTo': int(float(row['ShipTo'])),
                'ShipTo_Name': row['SoldTo_Name'],
                'POD': row['POD'],
                'SoldTo': int(float(row['SoldTo'])),
                'YFRP': row['YFRP'],
                'AM': row['Shipto_SalesGr']}
            shipto_unique.append(shipto)
            processed.append(row['ShipTo'])
    
    for mylist in shipto_unique:
        shipto_exists = ShipTos.query.filter(ShipTos.ShipTo == mylist['ShipTo']).count()
        if shipto_exists == 0:
            new_shipto = Customers(
                ShipTo = mylist['ShipTo'],
                ShipTo_Name = mylist['ShipTo_Name'],
                POD = mylist['POD'],
                SoldTo_id = get_id_Soldto(mylist['SoldTo']),
                YFRP_id = get_id_YFRP(mylist['YFRP']),
                AM_id = get_id_AM(mylist['AM']),
                Addr_id = get_id_Address(mylist['ShipTo']),
                is_deleted = False)

            db_session.add(new_shipto)
            db_session.commit()
    
    return shipto_unique


def det_id_Shipto(ShipTo):
    db_data = ShipTos.query.filter(ShipTos.ShipTo == ShipTo).first()
    shipto_id = db_data.id

    return shipto_id








if __name__ == "__main__":
    # files = convert_file(xls_file)
    # print('Файлы сохранены')

    # data = read_csv_addresses(addr_file)
    # print(data)

    data = read_csv_customers(cust_file)

    x = save_Shipto(data)
    # print(payterm)

    # AMs = get_AM_id(data)
    # print(AMs)


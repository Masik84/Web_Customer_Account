import csv
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy.exc import SQLAlchemyError

from models_customer import Customers, PaymentTerms, Managers, LoB, STLs
from db import db_session

xls_file = 'Managers.xlsx'
filename = 'AM_STL_2022-06-26.csv'

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
        print(f'Файл {csv_filename} сохранен')



def read_csv_managers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Sales_Grp', 'AM_name', 'SO_code', 'STL', 'LoB']
        reader = csv.DictReader(f, fields, delimiter=';')
        manager_data = []
        for row in reader:
            manager_data.append(row)
        return manager_data


def save_LOB(data):
    processed = []
    lob_unique = []
    for row in data:
        if row['LoB'] not in processed:
            lob = {'LoB_name': row['LoB']}
            lob_unique.append(lob)
            processed.append(lob['LoB_name'])

    for mylist in lob_unique:
        lob_exists = LoB.query.filter(LoB.LoB == mylist['LoB_name']).count()
        if lob_exists == 0:
            new_lob = LoB(LoB = mylist['LoB_name'], is_deleted = False)
            db_session.add(new_lob)
            db_session.commit()

    return lob_unique


def get_id_LoB(LoB_name):
    db_data = LoB.query.filter(LoB.LoB == LoB_name).first()
    lob_id = db_data.id

    return lob_id


def save_STL(data):
    processed = []
    stl_unique = []
    for row in data:
        if row['STL'] not in processed:
            stl = {'STL_name': row['STL']}
            stl_unique.append(stl)
            processed.append(stl['STL_name'])

    for mylist in stl_unique:
        stl_exists = STLs.query.filter(STLs.STL == mylist['STL_name']).count()
        if stl_exists == 0:
            new_stl = STLs(STL = mylist['STL_name'], is_deleted = False)
            db_session.add(new_stl)
            db_session.commit()

    return stl_unique


def get_id_STL(STL_name):
    db_data = STLs.query.filter(STLs.STL == STL_name).first()
    stl_id = db_data.id

    return stl_id


def save_AM(data):
    processed = []
    am_unique = []
    for row in data:
        if row['Sales_Grp'] not in processed:
            am = {'Sales_Grp': row['Sales_Grp'], 
                    'AM_name': row['AM_name'], 
                    'SO_code': row['SO_code'], 
                    'STL_id': get_id_STL(row['STL']),
                    'LoB_id': get_id_LoB(row['LoB'])
                    }
            am_unique.append(am)
            processed.append(am['Sales_Grp'])

    for mylist in am_unique:
        print(mylist)
        am_exists = Managers.query.filter(Managers.Sales_Grp == mylist['Sales_Grp']).count()
        if am_exists == 0:
            new_am = Managers(
                Sales_Grp = mylist['Sales_Grp'],
                AM_name = mylist['AM_name'],
                SO_code = mylist['SO_code'],
                STL_id = mylist['STL_id'],
                LoB_id = mylist['LoB_id'],
                is_deleted = False)
            db_session.add(new_am)
            db_session.commit()

    return am_unique


def get_id_AM(data):
    am_unique = save_AM(data)
    am_id_list = []
    for mylist in am_unique:
        db_data = Managers.query.filter(Managers.Sales_Grp == mylist['Sales_Grp']).first()
        combine = {'am_id': db_data.id, 'Sales_Grp': db_data.Sales_Grp}
        am_id_list.append(combine)

    return am_id_list







if __name__ == "__main__":
    convert_file(xls_file)
    data = read_csv_managers(filename)
    lob = save_LOB(data)
    print(lob)
    stl = save_STL(data)
    print(stl)
    am = save_AM(data)
    print(am)



import csv, os
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import numpy as np

from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.db import db
from webapp.customer.models import Customers, Addresses, YFRP, LoB, ShipTos, Managers, STLs, PaymentTerms
from webapp.user.decorators import admin_required


blueprint = Blueprint('сustomer', __name__)

path = os.getcwd()
now = datetime.today().strftime('%Y-%m-%d')
am_file = os.path.join(UPLOAD_FOLDER, 'AM_STL' + '_' + now + '.csv')
addr_file = os.path.join(UPLOAD_FOLDER, 'Addresses' + '_' + now + '.csv')
cust_file = os.path.join(UPLOAD_FOLDER, 'Cust_Data' + '_' + now + '.csv')


################################################################################
@blueprint.route("/customers")
@admin_required
def customers_page():
    cust_data = Customers.query.order_by(Customers.SoldTo_Name).limit(20).all()
    return render_template("customer/customer_list.html", cust_data=cust_data)


@blueprint.route("/address")
@admin_required
def deladdress_page():
    del_addr_data = ShipTos.query.order_by(ShipTos.ShipTo_Name).limit(20).all()
    return render_template('customer/delivery_addr.html', del_addr_data=del_addr_data)


@blueprint.route("/managers")
@admin_required
def managers_page():
    am_data = Managers.query.order_by(Managers.AM_name).all()
    return render_template("admin/managers.html", am_data=am_data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@blueprint.route('/update_customers', methods=['GET', 'POST'])
@admin_required
def update_customers():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='alert-warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filename)
            convert_file(filename)
            run_customer_func()
            flash("Customer's Data Uploaded Successfully!", category='alert-success')
            return redirect(url_for('сustomer.customers_page'))
    return redirect(url_for('admin.admin_index'))


@blueprint.route('/update_managers', methods=['GET', 'POST'])
@admin_required
def update_managers():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='alert-warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filename = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filename)
            convert_file(filename)
            am_data = read_csv_managers(am_file)
            save_LOB(am_data)
            save_STL(am_data)
            save_AM(am_data)
            flash("Manager's Data Uploaded Successfully!", category='alert-success')
            return redirect(url_for('сustomer.managers_page'))
    return redirect(url_for('admin.admin_index'))


def run_customer_func():
    read_csv_addresses(addr_file)
    cust_data = read_csv_customers(cust_file)
    save_PayTerm(cust_data)
    save_YFRP(cust_data)
    save_Soldto(cust_data)
    save_Shipto(cust_data)


def convert_file(filename):
    xls = pd.ExcelFile(filename)
    sheets = xls.sheet_names
    now = datetime.today().strftime('%Y-%m-%d')
    file_saved = []
    for sheet in sheets:
        xls_data = pd.read_excel(filename, sheet_name=sheet)
        csv_filename = sheet + '_' + now + '.csv'
        csv_filename = os.path.join(UPLOAD_FOLDER, csv_filename)
        np.savetxt(csv_filename, xls_data, encoding='utf-8', fmt='%s', delimiter=';')
        file_saved.append(csv_filename)

    return file_saved


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

    lob_for_upload = []
    for mylist in lob_unique:
        lob_exists = LoB.query.filter(LoB.LoB == mylist['LoB_name']).count()
        if lob_exists == 0:
            new_lob = {'LoB': mylist['LoB_name'], 'is_deleted': False}
            lob_for_upload.append(new_lob)

    db.session.bulk_insert_mappings(LoB, lob_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise
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

    stl_for_upload = []
    for mylist in stl_unique:
        stl_exists = STLs.query.filter(STLs.STL == mylist['STL_name']).count()
        if stl_exists == 0:
            new_stl = {'STL': mylist['STL_name'], 'is_deleted': False}
            stl_for_upload.append(new_stl)

    db.session.bulk_insert_mappings(STLs, stl_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

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

    am_for_upload = []
    for mylist in am_unique:
        print(mylist)
        am_exists = Managers.query.filter(Managers.Sales_Grp == mylist['Sales_Grp']).count()
        if am_exists == 0:
            new_am = {'Sales_Grp': mylist['Sales_Grp'],
                                'AM_name': mylist['AM_name'],
                                'SO_code': mylist['SO_code'],
                                'STL_id': mylist['STL_id'],
                                'LoB_id': mylist['LoB_id'],
                                'is_deleted': False}
            am_for_upload.append(new_am)

    db.session.bulk_insert_mappings(Managers, am_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

    return am_unique


def get_id_AM(SalesGr):
    db_data = Managers.query.filter(Managers.Sales_Grp == SalesGr).first()
    am_id = db_data.id

    return am_id


def read_csv_addresses(addr_file):
    with open(addr_file, 'r', encoding='utf-8') as f:
        fields = ['Address_Code', 'Region', 'City', 'Postal_Code', 'Street', 'House']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        addr_for_upload = []
        for row in reader:
            addr_exists = Addresses.query.filter(Addresses.Address_Code == row['Address_Code']).count()
            if addr_exists == 0:
                address = {'Address_Code': row['Address_Code'], 
                                    'Region': row['Region'],
                                    'City': row['City'],
                                    'Postal_Code': int(float(row['Postal_Code'])),
                                    'Street': row['Street'],
                                    'House': row['House']}
                addr_for_upload.append(address)

        db.session.bulk_insert_mappings(Addresses, addr_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(address, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(address, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_Address(Address_Code):
    db_data = Addresses.query.filter(Addresses.Address_Code == Address_Code).first()
    addr_id = db_data.id
    return addr_id


def read_csv_customers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['SoldTo', 'SoldTo_Name', 'Soldto_SalesGr', 'INN', 'KPP', 'Pay_term', 'PT_description', 'ShipTo',
                  'Shipto_SalesGr', 'POD', 'YFRP']
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
            pt = {'Pay_term': row['Pay_term'], 
                    'PT_description': row['PT_description']}
            pt_unique.append(pt)
            processed.append(pt['Pay_term'])

    pt_for_upload = []
    for mylist in pt_unique:
        pt_exists = PaymentTerms.query.filter(PaymentTerms.Pay_term == mylist['Pay_term']).count()
        if pt_exists == 0:
            new_pay_term = {'Pay_term': mylist['Pay_term'], 
                                        'PT_description': mylist['PT_description']}
            pt_for_upload.append(new_pay_term)

    db.session.bulk_insert_mappings(PaymentTerms, pt_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

    return pt_unique


def get_id_PT(Pay_term):
    db_data = PaymentTerms.query.filter(PaymentTerms.Pay_term == Pay_term).first()
    pt_id = db_data.id

    return pt_id


def save_YFRP(data):
    processed = []
    YFRP_unique = []

    for row in data:
        if row['YFRP'] != 'nan':
            if row['YFRP'] not in processed:
                yfrp = {'YFRP': int(float(row['YFRP'])),
                            'YFRP_Name': row['SoldTo_Name']
                            }
                YFRP_unique.append(yfrp)
                processed.append(row['YFRP'])

    YFRP_for_upload = []
    for mylist in YFRP_unique:
        YFRP_exists = YFRP.query.filter(YFRP.YFRP == mylist['YFRP']).count()
        if YFRP_exists == 0:
            new_YFRP = {'YFRP': mylist['YFRP'],
                                    'YFRP_Name': mylist['YFRP_Name'],
                                    'Addr_id': get_id_Address(mylist['YFRP']),
                                    'is_deleted': False}
            YFRP_for_upload.append(new_YFRP)

    db.session.bulk_insert_mappings(YFRP, YFRP_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

    return YFRP_unique


def get_id_YFRP(YFRP_find):
    if YFRP_find != 'nan':
        YFRP_find = int(float(YFRP_find))
        db_data = YFRP.query.filter(YFRP.YFRP == YFRP_find).first()
        Yfrp_id = db_data.id

    else:
        Yfrp_id = None

    return Yfrp_id


def check_POD(POD_field):
    if POD_field != 'nan':
        POD_checked = POD_field
    else:
        POD_checked = None

    return POD_checked


def check_KPP(KPP_field):
    if KPP_field != 'nan':
        KPP_checked = str(int(float(KPP_field)))
    else:
        KPP_checked = None
    
    return KPP_checked


def save_Soldto(data):
    processed = []
    soldto_unique = []

    for row in data:
        if row['SoldTo'] not in processed:
            soldto = {'SoldTo': int(float(row['SoldTo'])),
                            'SoldTo_Name': row['SoldTo_Name'],
                            'INN': row['INN'],
                            'KPP': row['KPP'],
                            'PT': row['Pay_term'],
                            'AM': row['Soldto_SalesGr']}
            soldto_unique.append(soldto)
            processed.append(row['SoldTo'])

    soldto_for_upload = []
    for mylist in soldto_unique:
        soldto_exists = Customers.query.filter(Customers.SoldTo == mylist['SoldTo']).count()
        if soldto_exists == 0:
            new_soldto = {'SoldTo': mylist['SoldTo'],
                                    'SoldTo_Name': mylist['SoldTo_Name'],
                                    'INN': mylist['INN'],
                                    'KPP': check_KPP(mylist['KPP']),
                                    'AM_id': get_id_AM(mylist['AM']),
                                    'Addr_id': get_id_Address(mylist['SoldTo']),
                                    'PayTerm_id': get_id_PT(mylist['PT']),
                                    'is_deleted': False}
            soldto_for_upload.append(new_soldto)

    db.session.bulk_insert_mappings(Customers, soldto_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

    return soldto_unique


def get_id_Soldto_bySoldto(SoldTo):
    db_data = Customers.query.filter(Customers.SoldTo == SoldTo).first()
    soldto_id = db_data.id

    return soldto_id


def get_id_Soldto_byINN(Cust_Inn):
    db_data = Customers.query.filter(Customers.INN == Cust_Inn).first()
    soldto_id = db_data.id

    return soldto_id



def save_Shipto(data):
    processed = []
    shipto_unique = []

    for row in data:
        if row['ShipTo'] not in processed:
            shipto = {'ShipTo': int(float(row['ShipTo'])),
                            'ShipTo_Name': row['SoldTo_Name'],
                            'POD': row['POD'],
                            'SoldTo': int(float(row['SoldTo'])),
                            'YFRP': row['YFRP'],
                            'AM': row['Shipto_SalesGr']
                            }
            shipto_unique.append(shipto)
            processed.append(row['ShipTo'])

    shipto_for_upload = []
    for mylist in shipto_unique:
        shipto_exists = ShipTos.query.filter(ShipTos.ShipTo == mylist['ShipTo']).count()
        if shipto_exists == 0:
            new_shipto = {'ShipTo': mylist['ShipTo'],
                                    'ShipTo_Name': mylist['ShipTo_Name'],
                                    'POD': check_POD(mylist['POD']),
                                    'SoldTo_id': get_id_Soldto_bySoldto(mylist['SoldTo']),
                                    'YFRP_id': get_id_YFRP(mylist['YFRP']),
                                    'AM_id': get_id_AM(mylist['AM']),
                                    'Addr_id': get_id_Address(mylist['ShipTo']),
                                    'is_deleted': False}
            shipto_for_upload.append(new_shipto)                              

    db.session.bulk_insert_mappings(ShipTos, shipto_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(mylist, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(mylist, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise

    return shipto_unique


def det_id_Shipto(ShipTo):
    db_data = ShipTos.query.filter(ShipTos.ShipTo == ShipTo).first()
    shipto_id = db_data.id

    return shipto_id


def print_error(row_number, error_text, exception):
    print(f"Ошибка на строке {row_number}")
    print(error_text.format(exception))
    print('-' * 80)

from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import csv, os
import numpy as np
import pandas as pd

from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.customer.models import Customers
from webapp.customer.views import get_id_Shipto, get_id_Soldto_bySoldto
from webapp.db import db
from webapp.price.models import PriceHierarchy, PriceTable, PriceType, Prices
from webapp.product.views import get_id_Material
from webapp.user.decorators import admin_required


blueprint = Blueprint('prices', __name__)

path = os.getcwd()
now = datetime.today().strftime('%Y-%m-%d')
price_hier_file = os.path.join(UPLOAD_FOLDER, 'PriceHier' + '_' + now + '.csv')
cust_hier_file = os.path.join(UPLOAD_FOLDER, 'CustHier' + '_' + now + '.csv')
price_table_file = os.path.join(UPLOAD_FOLDER, 'PriceTable' + '_' + now + '.csv')
price_type_file = os.path.join(UPLOAD_FOLDER, 'PriceType' + '_' + now + '.csv')
price_file = os.path.join(UPLOAD_FOLDER, 'Prices' + '_' + now + '.csv')


################################################################################
@blueprint.route("/prices")
@admin_required
def prices_page():
    price_data = Prices.query.order_by(Prices.ValidFrom.desc()).limit(20).all()
    return render_template("price/price_list.html", price_data=price_data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@blueprint.route('/update_prices', methods=['GET', 'POST'])
@admin_required
def update_prices_master_data():
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
            run_price_masterdata_func()
            flash("Prices Master Data Uploaded Successfully!", category='alert-success')
            return redirect(url_for('prices.prices_page'))
    return redirect(url_for('admin.admin_index'))


def run_price_masterdata_func():
    read_csv_pricetables(price_table_file)
    read_csv_pricetype(price_type_file)
    read_csv_pricehier(price_hier_file)
    read_csv_cust_hier(cust_hier_file)
    read_csv_prices(price_file)


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


def read_csv_pricetables(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['TabN', 'Tab_desc']
        reader = csv.DictReader(f, fields, delimiter=';')

        processed = []
        pr_table_unique = []
        for row in reader:
            if row['TabN'] not in processed:
                pr_table = {'TabN': int(float(row['TabN'])), 
                                    'Tab_desc': row['Tab_desc']}
                pr_table_unique.append(pr_table)
                processed.append(row['TabN'])

        pr_table_for_upload = []
        for mylist in pr_table_unique:
            table_exists = PriceTable.query.filter(PriceTable.TabN == mylist['TabN']).count()
            if table_exists == 0:
                new_pr_table = {'TabN': mylist['TabN'], 
                                            'Tab_desc': mylist['Tab_desc']}
                pr_table_for_upload.append(new_pr_table)
                processed.append(new_pr_table['TabN'])

        db.session.bulk_insert_mappings(PriceTable, pr_table_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_pr_table, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_pr_table, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_PriceTable(pr_tab_n):
    db_data = PriceTable.query.filter(PriceTable.TabN == pr_tab_n).first()
    price_table_id = db_data.id

    return price_table_id


def read_csv_pricetype(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Type', 'Type_desc']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        processed = []
        pr_type_unique = []
        for row in reader:
            if row['Type'] not in processed:
                pr_type = {'Type': row['Type'], 
                                    'Type_desc': row['Type_desc']}
                pr_type_unique.append(pr_type)
                processed.append(row['Type'])
        print(pr_type_unique)

        pr_type_for_upload = []
        for mylist in pr_type_unique:
            type_exists = PriceType.query.filter(PriceType.Type == mylist['Type']).count()
            if type_exists == 0:
                new_pr_type = {'Type': mylist['Type'], 
                                            'Type_desc': mylist['Type_desc']}
                pr_type_for_upload.append(new_pr_type)

        db.session.bulk_insert_mappings(PriceType, pr_type_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_pr_type, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_pr_type, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_PriceType(pr_type_code):
    db_data = PriceType.query.filter(PriceType.Type == pr_type_code).first()
    price_type_id = db_data.id

    return price_type_id


def read_csv_pricehier(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Code', 'Name']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        processed = []
        pr_hier_unique = []
        for row in reader:
            if row['Code'] not in processed:
                pr_hier = {'Code': int(float(row['Code'])), 
                                    'Name': row['Name']}
                pr_hier_unique.append(pr_hier)
                processed.append(row['Code'])

        pr_hier_for_upload = []
        for mylist in pr_hier_unique:
            hier_exists = PriceHierarchy.query.filter(PriceHierarchy.Code == mylist['Code']).count()
            if hier_exists == 0:
                new_pr_hier = {'Code': mylist['Code'], 
                                            'Name': mylist['Name']}
                pr_hier_for_upload.append(new_pr_hier)

        db.session.bulk_insert_mappings(PriceHierarchy, pr_hier_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_pr_hier, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_pr_hier, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_PriceHier(pr_hier_code):
    if pr_hier_code != 'nan':
        pr_hier_code = int(float(pr_hier_code))
        db_data = PriceHierarchy.query.filter(PriceHierarchy.Code == pr_hier_code).first()
        price_hier_id = db_data.id
    else:
        price_hier_id = None
    return price_hier_id


def read_csv_cust_hier(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['SoldTo', 'SoldTo_Name', 'Heir_code', 'Hier_Name']
        reader = csv.DictReader(f, fields, delimiter=';')

        for row in reader:
            cust_id = get_id_Soldto_bySoldto(int(float(row['SoldTo'])))
            hierarchy_id = get_id_PriceHier(int(float(row['Heir_code'])))
            print(f'customer - {cust_id}')
            print(f'hierarchy - {hierarchy_id}')
            if cust_id is None:
                flash(f'No such Soldto - ' + row['SoldTo'], category='alert-danger')
            else:
                cust = Customers.query.filter(Customers.id == cust_id).first()
                cust.id = cust_id
                cust.PriceHier_id = hierarchy_id
                db.session.commit()



def read_csv_prices(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Table', 'PriceType', 'ValidFrom', 'ValidTo', 'Hierarchy', 'SoldTo', 'ShipTo', 
                        'Material', 'Price', 'PriceCurr', 'PricingUnit', 'UoM']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        price_for_upload = []
        for row in reader:
            price_new = {'Table_id': get_id_PriceTable(int(float(row['Table']))),
                                'PriceType_id': get_id_PriceType(row['PriceType']),
                                'ValidFrom': row['ValidFrom'],
                                'ValidTo': row['ValidTo'],
                                'Hier_id': get_id_PriceHier(row['Hierarchy']),
                                'Soldto_id': get_id_Soldto_bySoldto(row['SoldTo']),
                                'Shipto_id': get_id_Shipto(row['ShipTo']),
                                'Material_id': get_id_Material(str(int(float(row['Material'])))),
                                'Price': row['Price'],
                                'PriceCurr': row['PriceCurr'],
                                'PricingUnit': row['PricingUnit'],
                                'UoM': row['UoM']}
            print(price_new)
            price_for_upload.append(price_new)

        db.session.bulk_insert_mappings(Prices, price_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(price_new, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(price_new, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise



def print_error(row_number, error_text, exception):
    print(f"Ошибка на строке {row_number}")
    print(error_text.format(exception))
    print('-' * 80)
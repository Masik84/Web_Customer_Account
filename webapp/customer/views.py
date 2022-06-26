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

################################################################################
@blueprint.route("/customers")
@admin_required
def customers_page():
    cust_data = Customers.query.order_by(Customers.SoldTo_Name).all()
    return render_template("customer/customer_list.html", cust_data=cust_data)


@blueprint.route("/address")
@admin_required
def deladdress_page():
    return render_template('customer/del_addr.html')


@blueprint.route("/managers")
@admin_required
def managers_page():
    am_data = Managers.query.order_by(Managers.AM_name).all()
    return render_template("admin/managers.html", am_data=am_data)


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/update_customers', methods=['GET', 'POST'])
def update_customers():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', category='alert-warning')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            convert_file(filename)
            addr_file = 'Addresses' + '_' + now + '.csv'
            cust_file = 'Cust_Data' + '_' + now + '.csv'
            read_csv_addresses(addr_file)
            #flash('File saved Successfully!', category='alert-success')
            return redirect(url_for('сustomer.customers_page'))
    return redirect(url_for('admin.admin_index'))


def convert_file(addr_file):
    xls = pd.ExcelFile(addr_file)
    sheets = xls.sheet_names
    now = datetime.today().strftime('%Y-%m-%d')
    file_saved =[]
    for sheet in sheets:
        xls_data = pd.read_excel(addr_file, sheet_name=sheet)
        csv_filename = sheet + '_' + now + '.csv'
        np.savetxt(csv_filename, xls_data, encoding='utf-8', fmt='%s', delimiter=';')
        file_saved.append(csv_filename)
        print(f'Файл {csv_filename} сохранен')
        return file_saved


def read_csv_addresses(addr_file):
    with open(addr_file, 'r', encoding='utf-8') as f:
        fields = ['Address_Code', 'Region', 'City', 'Postal_Code', 'Street', 'House']
        reader = csv.DictReader(f, fields, delimiter=';')
        for row in reader:
            addr_exists = Addresses.query.filter(Addresses.Address_Code == row['Address_Code']).count()
            if addr_exists == 0:
                save_address_data(row)
            else:
                pass
    flash("Данные обновлены", category='alert-success')


def save_address_data(row):
    address = Addresses(
            Address_Code=row['Address_Code'], 
            Region=row['Region'],
            City=row['City'],
            Postal_Code=row['Postal_Code'],
            Street=row['Street'],
            House=row['House'])
    db.session.add(address)
    db.session.commit()

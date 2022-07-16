from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.utils import secure_filename
import csv, os
import numpy as np
import pandas as pd

from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.customer.views import get_id_Shipto, get_id_Soldto_bySoldto
from webapp.db import db
from webapp.order.models import Deliveries, InvoiceType, OrderStatus, OrderType, Orders
from webapp.price.models import PriceHierarchy, PriceTable, PriceType, Prices
from webapp.product.views import get_id_Material, get_id_Plant
from webapp.user.decorators import admin_required


blueprint = Blueprint('orders', __name__)


path = os.getcwd()
now = datetime.today().strftime('%Y-%m-%d')
ord_type_file = os.path.join(UPLOAD_FOLDER, 'OrderType' + '_' + now + '.csv')
inv_type_file = os.path.join(UPLOAD_FOLDER, 'InvoiceType' + '_' + now + '.csv')
ord_status = os.path.join(UPLOAD_FOLDER, 'OrderStatus' + '_' + now + '.csv')
orders_file = os.path.join(UPLOAD_FOLDER, 'OpenOrders' + '_' + now + '.csv')
invoices_file = os.path.join(UPLOAD_FOLDER, 'Invoices' + '_' + now + '.csv')


################################################################################
@blueprint.route("/orders")
@login_required
def orders_page():
    return render_template("order/order_list.html")


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/update_sales', methods=['GET', 'POST'])
@admin_required
def update_sales_data():
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
            run_sales_func()
            flash("Sales Uploaded Successfully!", category='alert-success')
            return redirect(url_for('prices.prices_page'))
    return redirect(url_for('admin.admin_index'))


def run_sales_func():
    read_csv_ordertyper(ord_type_file)
    read_csv_invoicetype(inv_type_file)
    read_csv_orderstatus(ord_status)
    
    order_data = read_csv_orders(orders_file)
    update_delivery(order_data)
    update_orders(order_data)

    # read_csv_deliv_inv(invoices_file)
    # read_csv_orders(orders_file)
    # read_csv_invoices(invoices_file)


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


def read_csv_ordertyper(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Type_code', 'Type_Name']
        reader = csv.DictReader(f, fields, delimiter=';')

        processed = []
        ord_type_unique = []
        for row in reader:
            if row['Type_code'] not in processed:
                ord_type = {'Type_code': row['Type_code'],
                                    'Type_Name': row['Type_Name']}
                ord_type_unique.append(ord_type)
                processed.append(row['Type_code'])

        ord_type_for_upload = []
        for mylist in ord_type_unique:
            table_exists = OrderType.query.filter(OrderType.Type_code == mylist['Type_code']).count()
            if table_exists == 0:
                new_ord_type = {'Type_code': mylist['Type_code'], 
                                            'Type_Name': mylist['Type_Name']}
                ord_type_for_upload.append(new_ord_type)
                processed.append(mylist['Type_code'])

        db.session.bulk_insert_mappings(OrderType, ord_type_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_ord_type, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_ord_type, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_OrderType(ord_to_find):
    db_data = OrderType.query.filter(OrderType.Type_code == ord_to_find).first()
    order_type_id = db_data.id

    return order_type_id


def read_csv_invoicetype(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Type_code', 'Type_Name']
        reader = csv.DictReader(f, fields, delimiter=';')

        processed = []
        inv_type_unique = []
        for row in reader:
            if row['Type_code'] not in processed:
                inv_type = {'Type_code': row['Type_code'],
                                    'Type_Name': row['Type_Name']}
                inv_type_unique.append(inv_type)
                processed.append(row['Type_code'])

        inv_type_for_upload = []
        for mylist in inv_type_unique:
            table_exists = InvoiceType.query.filter(InvoiceType.Type_code == mylist['Type_code']).count()
            if table_exists == 0:
                new_inv_type = {'Type_code': mylist['Type_code'], 
                                            'Type_Name': mylist['Type_Name']}
                inv_type_for_upload.append(new_inv_type)
                processed.append(mylist['Type_code'])

        db.session.bulk_insert_mappings(InvoiceType, inv_type_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_inv_type, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_inv_type, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_InvoiceType(inv_to_find):
    db_data = InvoiceType.query.filter(InvoiceType.Type_code == inv_to_find).first()
    invoice_type_id = db_data.id

    return invoice_type_id


def read_csv_orderstatus(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Status']
        reader = csv.DictReader(f, fields, delimiter=';')

        ord_status_for_upload = []
        for row in reader:
            table_exists = OrderStatus.query.filter(OrderStatus.Status == row['Status']).count()
            if table_exists == 0:
                new_ord_status = {'Status': row['Status']}
                ord_status_for_upload.append(new_ord_status)

        db.session.bulk_insert_mappings(OrderStatus, ord_status_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(new_ord_status, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(new_ord_status, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_OrderStatus(status_to_find):
    db_data = OrderStatus.query.filter(OrderStatus.Status == status_to_find).first()
    order_status_id = db_data.id

    return order_status_id


def read_csv_orders(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['OrderN', 'Type_code', 'Order_date', 'Pricing_date', 'GI_date', 'Act_GI_date', 'Material',
                        'SoldTo', 'ShipTo', 'Plant', 'Status', 'DeliveryN', 'Qty']
        reader = csv.DictReader(f, fields, delimiter=';')

        order_list = []
        for row in reader:
            order_list.append(row)
        return order_list


def update_delivery(data):
    processed = []
    deliv_unique = []
    for row in data:
        if row['DeliveryN'] not in processed:
            deliv = {'DeliveryN': row['DeliveryN']}
            deliv_unique.append(deliv)
            processed.append(row['DeliveryN'])

    delivery_for_upload = []
    for mylist in deliv_unique:
        table_exists = Deliveries.query.filter(Deliveries.DeliveryN == mylist['Type_code']).count()
        if table_exists == 0:
            new_delivery = {'DeliveryN': mylist['DeliveryN']}
            delivery_for_upload.append(new_delivery)
            processed.append(mylist['Type_code'])

    db.session.bulk_insert_mappings(Deliveries, delivery_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(new_delivery, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(new_delivery, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise


def get_id_Delivery(del_to_find):
    if del_to_find != 'nan':
        db_data = Deliveries.query.filter(Deliveries.DeliveryN == del_to_find).first()
        delivery_id = db_data.id
    else:
        delivery_id = None

    return delivery_id


def update_orders(data):
    processed = []
    orders_unique = []
    for row in data:
        if row['OrderN'] not in processed:
            orders = {'OrderN': row['OrderN'],
                            'Type_code': row['Type_code'],
                            'Order_date': row['Order_date'],
                            'SoldTo': row['SoldTo'],
                            'ShipTo': row['ShipTo'],
                            'Plant': row['Plant']}
            orders_unique.append(orders)
            processed.append(row['OrderN'])

    orders_for_upload = []
    for mylist in orders_unique:
        table_exists = Orders.query.filter(Orders.OrderN == mylist['OrderN']).count()
        if table_exists == 0:
            new_order = {'OrderN': row['OrderN'],
                                    'Ord_type_id': get_id_OrderType(row['Type_code']),
                                    'Order_date': row['Order_date'],
                                    'Soldto_id': get_id_Soldto_bySoldto(row['SoldTo']),
                                    'Shipto_id': get_id_Shipto(row['ShipTo']),
                                    'Plant_id': get_id_Plant(row['Plant'])}
            orders_for_upload.append(new_order)
            processed.append(mylist['OrderN'])

    db.session.bulk_insert_mappings(Orders, orders_for_upload)
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        print_error(new_order, "Ошибка целостности данных: {}", e)
        db.session.rollback()
        raise
    except ValueError as e:
        print_error(new_order, "Неправильный формат данных: {}", e)
        db.session.rollback()
        raise


def get_id_Order(ord_to_find):
    if ord_to_find != 'nan':
        db_data = Orders.query.filter(Orders.OrderN == ord_to_find).first()
        order_id = db_data.id
    else:
        order_id = None

    return order_id








def print_error(row_number, error_text, exception):
    print(f"Ошибка на строке {row_number}")
    print(error_text.format(exception))
    print('-' * 80)
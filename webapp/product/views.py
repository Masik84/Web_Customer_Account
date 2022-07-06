import csv, os
from datetime import datetime
from flask import Blueprint, abort, render_template, request, flash, redirect, url_for
from flask_login import current_user
from werkzeug.utils import secure_filename
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
import numpy as np

from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.db import db
from webapp.product.models import ED, Materials, SalProducts, ProdFamily, ProdSubClass, MaterialStatus, BOs, Plants, Producers
from webapp.user.decorators import admin_required


blueprint = Blueprint('products', __name__)

path = os.getcwd()
now = datetime.today().strftime('%Y-%m-%d')
ed_file = os.path.join(UPLOAD_FOLDER, 'ED' + '_' + now + '.csv')
prod_file = os.path.join(UPLOAD_FOLDER, 'Product_Data' + '_' + now + '.csv')
plant_file = os.path.join(UPLOAD_FOLDER, 'Plant' + '_' + now + '.csv')

################################################################################
@blueprint.route("/products")
def products_page():
    if current_user.is_anonymous or not current_user.is_admin:
        abort(404, "Page not found")
    return render_template("product/products.html")


@blueprint.route('/materials')
def materials_page():
    material_data = Materials.query.order_by(Materials.Material_Name).all()
    return render_template("product/material_list.html", material_data=material_data)


@blueprint.route('/sal_product')
def sal_prod_page():
    sal_prod_data = SalProducts.query.order_by(SalProducts.Sal_Prod_Name).all()
    return render_template("product/salproduct_list.html", sal_prod_data=sal_prod_data)


@blueprint.route('/product_family')
def family_page():
    family_data = ProdFamily.query.order_by(ProdFamily.Family_Name).all()
    return render_template("product/prodfamily_list.html", family_data=family_data)


@blueprint.route('/product_subclass')
def subclass_page():
    subclass_data = ProdSubClass.query.order_by(ProdSubClass.Sub_Class_Name).all()
    return render_template("product/prodsubclass_list.html", subclass_data=subclass_data)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    

@blueprint.route('/update_products', methods=['GET', 'POST'])
@admin_required
def update_products():
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
            run_product_func()
            flash("Product's Data Uploaded Successfully!", category='alert-success')
            return redirect(url_for('products.products_page'))
    return redirect(url_for('admin.admin_index'))



def run_product_func():
    prod_data = read_csv_product(prod_file)
    read_csv_plant(plant_file)
    read_csv_producers(plant_file)
    read_csv_ed(ed_file)

    save_BO(prod_data)
    save_Status(prod_data)
    save_ProdSubClass(prod_data)
    save_Family(prod_data)
    save_SalProducts(prod_data)
    save_Materials(prod_data)


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


def read_csv_plant(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Plant_Code', 'Plant_Name']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        plant_for_upload = []
        for row in reader:
            plant_exists = Plants.query.filter(Plants.Plant_Code == row['Plant_Code']).count()
            if plant_exists == 0:
                plant_new = {'Plant_Code': row['Plant_Code'], 
                                    'Plant_Name': row['Plant_Name'],
                                    'is_deleted': False}
                plant_for_upload.append(plant_new)

        db.session.bulk_insert_mappings(Plants, plant_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(row, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(row, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_Plant(Plant_code):
    db_data = Plants.query.filter(Plants.Plant_Code == Plant_code).first()
    plant_id = db_data.id

    return plant_id


def read_csv_producers(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Producer_Code', 'Producer_Name']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        producer_for_upload = []
        for row in reader:
            producer_exists = Producers.query.filter(Producers.Producer_Code == row['Producer_Code']).count()
            if producer_exists == 0:
                producer_new = {'Producer_Code': row['Producer_Code'], 
                                    'Producer_Name': row['Producer_Name'],
                                    'is_deleted': False}
                producer_for_upload.append(producer_new)

        db.session.bulk_insert_mappings(Producers, producer_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(row, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(row, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_id_Producer(Producer_code):
    db_data = Producers.query.filter(Producers.Producer_Code == Producer_code).first()
    producer_id = db_data.id

    return producer_id


def read_csv_ed(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['From', 'To', 'Rate']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        ed_for_upload = []
        for row in reader:
            ed_exists = ED.query.filter(ED.From == row['From']).count()
            if ed_exists == 0:
                ed_new = {'From': row['From'], 
                                    'To': row['To'],
                                    'Rate': float(row['Rate']),
                                    'is_deleted': False}
                ed_for_upload.append(ed_new)

        db.session.bulk_insert_mappings(ED, ed_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(row, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(row, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def read_csv_product(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Material_code', 'Material_Name', 'Sal_Prod_Code', 
                        'Sal_Prod_Name', 'Family_Code', 'Family_Name', 
                        'Sub_Class', 'Sub_Class_Name', 'LoB', 'BO_type', 'Pack_Vol', 
                        'UoM', 'Plant', 'Producer', 'Status_code', 'Status_descr', 
                        'Comment', 'BO_Location', 'Production', 'Density', 
                        'Net_Weight', 'ED_type', 'Pack_type']
        reader = csv.DictReader(f, fields, delimiter=';')
        product_data = []
        for row in reader:
            product_data.append(row)
        return product_data


def save_BO(data):
    processed = []
    bo_unique = []
    for row in data:
        if row['BO_type'] not in processed:
            bo_list = {'BO_type': row['BO_type']}
            bo_unique.append(bo_list)
            processed.append(bo_list['BO_type'])

    bo_for_upload = []
    for mylist in bo_unique:
        bo_exists = BOs.query.filter(BOs.BO_type == mylist['BO_type']).count()
        if bo_exists == 0:
            new_bo = {'BO_type': mylist['BO_type'], 'is_deleted': False}
            bo_for_upload.append(new_bo)

    db.session.bulk_insert_mappings(BOs, bo_for_upload)
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
    return bo_unique


def get_id_BO(BO_name):
    db_data = BOs.query.filter(BOs.BO_type == BO_name).first()
    bo_id = db_data.id

    return bo_id


def save_Status(data):
    processed = []
    status_unique = []
    for row in data:
        if int(row['Status_code']) not in processed:
            status_list = {'Status_code': int(row['Status_code']),
                                    'Status_descr': row['Status_descr']}
            status_unique.append(status_list)
            processed.append(status_list['Status_code'])

    status_for_upload = []
    for mylist in status_unique:
        status_exists = MaterialStatus.query.filter(MaterialStatus.Status_code == mylist['Status_code']).count()
        if status_exists == 0:
            new_status = {'Status_code': mylist['Status_code'], 
                                    'Status_descr': mylist['Status_descr'],
                                    'is_deleted': False}
            status_for_upload.append(new_status)

    db.session.bulk_insert_mappings(MaterialStatus, status_for_upload)
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
    return status_unique


def get_id_Status(Status_code):
    db_data = MaterialStatus.query.filter(MaterialStatus.Status_code == Status_code).first()
    status_id = db_data.id

    return status_id


def save_ProdSubClass(data):
    processed = []
    subclass_unique = []
    for row in data:
        if int(row['Sub_Class']) not in processed:
            subclass_list = {'Sub_Class': int(row['Sub_Class']),
                                        'Sub_Class_Name': row['Sub_Class_Name']}
            subclass_unique.append(subclass_list)
            processed.append(subclass_list['Sub_Class'])

    subclass_for_upload = []
    for mylist in subclass_unique:
        subclass_exists = ProdSubClass.query.filter(ProdSubClass.Sub_Class == mylist['Sub_Class']).count()
        if subclass_exists == 0:
            new_subclass = {'Sub_Class': mylist['Sub_Class'],
                                        'Sub_Class_Name': mylist['Sub_Class_Name'],
                                        'is_deleted': False}
            subclass_for_upload.append(new_subclass)

    db.session.bulk_insert_mappings(ProdSubClass, subclass_for_upload)
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
    return subclass_unique


def get_id_ProdSubClass(SubClass_code):
    db_data = ProdSubClass.query.filter(ProdSubClass.Sub_Class == SubClass_code).first()
    subclass_id = db_data.id

    return subclass_id


def save_Family(data):
    processed = []
    family_unique = []
    for row in data:
        if row['Family_Code'] not in processed:
            family_list = {'Family_Code': row['Family_Code'],
                                    'Family_Name': row['Family_Name'],
                                    'Sub_Class': row['Sub_Class']}
            family_unique.append(family_list)
            processed.append(family_list['Family_Code'])

    family_for_upload = []
    for mylist in family_unique:
        family_exists = ProdFamily.query.filter(ProdFamily.Family_Code == mylist['Family_Code']).count()
        if family_exists == 0:
            new_family = {'Family_Code': mylist['Family_Code'],
                                    'Family_Name': mylist['Family_Name'],
                                    'SubClass_id': get_id_ProdSubClass(mylist['Sub_Class']),
                                    'is_deleted': False}
            family_for_upload.append(new_family)

    db.session.bulk_insert_mappings(ProdFamily, family_for_upload)
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
    return family_unique


def get_id_Family(Family_code):
    db_data = ProdFamily.query.filter(ProdFamily.Family_Code == Family_code).first()
    family_id = db_data.id

    return family_id


def save_SalProducts(data):
    processed = []
    salprod_unique = []
    for row in data:
        if row['Sal_Prod_Code'] not in processed:
            salprod_list = {'Sal_Prod_Code': row['Sal_Prod_Code'],
                                    'Sal_Prod_Name': row['Sal_Prod_Name'],
                                    'Family_Code': row['Family_Code'],}
            salprod_unique.append(salprod_list)
            processed.append(salprod_list['Sal_Prod_Code'])

    salprod_for_upload = []
    for mylist in salprod_unique:
        salprod_exists = SalProducts.query.filter(SalProducts.Sal_Prod_Code == mylist['Sal_Prod_Code']).count()
        if salprod_exists == 0:
            new_salprod = {'Sal_Prod_Code': mylist['Sal_Prod_Code'],
                                    'Sal_Prod_Name': mylist['Sal_Prod_Name'],
                                    'Family_id': get_id_Family(mylist['Family_Code']),
                                    'is_deleted': False}
            salprod_for_upload.append(new_salprod)

    db.session.bulk_insert_mappings(SalProducts, salprod_for_upload)
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
    return salprod_unique


def get_id_SalProduct(SalProd_code):
    db_data = SalProducts.query.filter(SalProducts.Sal_Prod_Code == SalProd_code).first()
    salprod_id = db_data.id

    return salprod_id


def save_Materials(data):
    processed = []
    material_unique = []
    for row in data:
        if row['Material_code'] not in processed:
            material_list = {'Material_code': row['Material_code'],
                                        'Material_Name': row['Material_Name'],
                                        'LoB': row['LoB'],
                                        'Pack_Vol': float(row['Pack_Vol']),
                                        'UoM': row['UoM'],
                                        'Comment': row['Comment'],
                                        'BO_Location': row['BO_Location'],
                                        'Production': row['Production'],
                                        'Density': float(row['Density']),
                                        'Net_Weight': float(row['Net_Weight']),
                                        'ED_type': row['ED_type'],
                                        'Pack_type': row['Pack_type'],
                                        'Sal_Prod_Code': row['Sal_Prod_Code'],
                                        'BO_type': row['BO_type'],
                                        'Status_code': row['Status_code'],
                                        'Plant': row['Plant'],
                                        'Producer': row['Producer']}
            material_unique.append(material_list)
            processed.append(material_list['Sal_Prod_Code'])

    material_for_upload = []
    for mylist in material_unique:
        material_exists = Materials.query.filter(Materials.Material_code == mylist['Material_code']).count()
        if material_exists == 0:
            new_material = {'Material_code': mylist['Material_code'],
                                        'Material_Name': mylist['Material_Name'],
                                        'LoB': mylist['LoB'],
                                        'Pack_Vol': mylist['Pack_Vol'],
                                        'UoM': mylist['UoM'],
                                        'Comment': mylist['Comment'],
                                        'BO_Location': mylist['BO_Location'],
                                        'Production': mylist['Production'],
                                        'Density': mylist['Density'],
                                        'Net_Weight': mylist['Net_Weight'],
                                        'ED_type': mylist['ED_type'],
                                        'Pack_type': mylist['Pack_type'],
                                        'SalProduct_id': get_id_SalProduct(mylist['Sal_Prod_Code']),
                                        'BO_id': get_id_BO(mylist['BO_type']),
                                        'Status_id': get_id_Status(mylist['Status_code']),
                                        'Plant_id': get_id_Plant(mylist['Plant']),
                                        'Producer_id': get_id_Plant(mylist['Producer']),
                                        'is_deleted': False}
            print(new_material)
            material_for_upload.append(new_material)

    db.session.bulk_insert_mappings(Materials, material_for_upload)
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
    return material_unique


def get_id_Material(Mater_code):
    db_data = Materials.query.filter(Materials.Material_code == Mater_code).first()
    material_id = db_data.id

    return material_id




def print_error(row_number, error_text, exception):
    print(f"Ошибка на строке {row_number}")
    print(error_text.format(exception))
    print('-' * 80)
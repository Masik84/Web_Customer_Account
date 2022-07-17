import csv, os
from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
import pandas as pd
import requests
from sqlalchemy.exc import SQLAlchemyError

from webapp.config import UPLOAD_FOLDER
from webapp.customer.models import Customers
from webapp.customer.views import get_id_Soldto_byINN, get_id_Soldto_bySoldto, print_error
from webapp.db import db
from webapp.admin.forms import AdminRegistrationForm, AdminUserUpdateForm
from webapp.admin.models import CurrencyName, FX_rate
from webapp.user.models import User
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__)



now = datetime.today().strftime('%Y-%m-%d')
fx_usd_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_USD' + '_' + now + '.csv')
fx_eur_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_EUR' + '_' + now + '.csv')

usd_id = 'R01235'
eur_id = 'R01239'

@blueprint.route('/admin/')
@admin_required
def admin_index():
    return render_template('admin/index.html')


################################################################################
@blueprint.route("/user_list")
@admin_required
def users_page():
    user_data = User.query.order_by(User.username).all()
    return render_template("user/user_list.html", user_data=user_data)


@blueprint.route('/add_user')
@admin_required
def register():
    title = "Регистрация"
    form = AdminRegistrationForm()
    return render_template('admin/registration.html', page_title=title, form=form)


@blueprint.route('/user-reg', methods=['POST'])
@admin_required
def process_reg():
    form = AdminRegistrationForm()

    if form.validate_on_submit():
        user_name = form.username.data
        user_email = form.email.data
        user_role = form.role.data
        user_cust_inn = form.cust_inn.data

        if user_role == 1:
            new_user = User(username=user_name, 
                                            email=user_email, 
                                            role='admin')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировали админа!', category='alert-success')
            return redirect(url_for('admin.users_page'))
        else:
            cust_id = get_id_Soldto_byINN(user_cust_inn)
            if cust_id:
                new_user = User(username=user_name, 
                                            email=user_email, 
                                            role='user', 
                                            comp_id=cust_id)
                new_user.set_password(form.password.data)
                db.session.add(new_user)
                db.session.commit()
                flash('Вы успешно зарегистрировали пользователя!', category='alert-success')
                return redirect(url_for('admin.users_page'))
            else:
                flash('Такая компания не найдена, попробуйте снова!', category='alert-danger')
                return redirect(url_for('admin.users_page'))
            
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text,
                    error
                ), category='alert-danger')
        return redirect(url_for('admin.users_page'))


@blueprint.route('/user/<int:user_id>')
@admin_required
def single_user(user_id):
    form = AdminUserUpdateForm()
    this_user = User.query.filter(User.id == user_id).first()
    if not this_user:
        abort(404)
    return render_template("user/user_admin_page.html", user=this_user, form=form)


@blueprint.route('/user_update/<int:user_id>', methods=['POST'])
@admin_required
def user_update(user_id):
    form = AdminUserUpdateForm()

    if form.validate_on_submit():
        user_to_update = User.query.filter(User.id == user_id).first()

        user_to_update.id = request.form["user_id"]
        user_to_update.username = request.form["username"]
        user_to_update.role = request.form["userrole"]
        user_to_update.email = request.form["useremail"]
        user_to_update.comp_id = get_id_Soldto_bySoldto(request.form['cust_soldto'])
        if request.form['del_flag'] == 2:
            user_to_update.is_deleted = True
        else:
            user_to_update.is_deleted = False
        db.session.commit()

        flash('User updated successfully', category='alert-success')
        return redirect(url_for('admin.users_page'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in field "{}": - {}'.format(
                    getattr(form, field).label.text, 
                    error
                ), category='alert-danger')
    return redirect(url_for('admin.admin_index'))

@blueprint.route('/user_delete', methods=['POST'])
@admin_required
def user_delete():
    form = AdminUserUpdateForm()

    user_to_delete = User.query.filter(User.id == request.form["user_id"]).first()
    user_to_delete.id = request.form['user_id']
    user_to_delete.is_deleted = True
    
    db.session.commit()
    flash('User updated successfully', category='alert-success')
    return redirect(url_for('admin.users_page'))


################################################################################

@blueprint.route("/fx_list")
@admin_required
def fx_page():
    fx_data = FX_rate.query.order_by(FX_rate.FX_date.desc(), FX_rate.Curr_id).limit(10)
    return render_template("admin/fx_rate.html", fx_data=fx_data)


@blueprint.route("/fx_update")
@admin_required
def exchange_update():
    get_fx_from_cbr()
    read_csv_currency(fx_usd_file)
    read_csv_currency(fx_eur_file)
    flash('Exchange Rates updated successfully!', category='alert-success')
    return redirect(url_for('admin.fx_page'))


def get_usd_last_date():
    last_date = FX_rate.query.order_by(FX_rate.FX_date.desc()).filter(FX_rate.Curr_id == get_curr_id(usd_id)).first()

    if last_date is None:
        last_date = '01/01/2020'
    else:
        last_date = last_date.FX_date
        last_date = datetime.strftime(last_date, '%d/%m/%Y')

    return last_date

def get_eur_last_date():
    last_date = FX_rate.query.order_by(FX_rate.FX_date.desc()).filter(FX_rate.Curr_id == get_curr_id(eur_id)).first()

    if last_date is None:
        last_date = '01/01/2020'
    else:
        last_date = last_date.FX_date
        last_date = datetime.strftime(last_date, '%d/%m/%Y')

    return last_date


def get_html(url):
    headers = {
        'User_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36 OPR/87.0.4390.36 (Edition Yx 05) Firefox/102.0'
    }
    try:
        result = requests.get(url, headers = headers)
        result.raise_for_status()          # обязательно вносить строку, чтобы исключить ошибки сервера
        return result.text
    except(requests.RequestException, ValueError):
        print('Сетевая ошибка')
        return False


def get_fx_from_cbr():
    usd_date_from = get_usd_last_date()
    eur_date_from = get_eur_last_date()
    date_to = datetime.today().strftime('%d/%m/%Y')

    url_usd = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={usd_date_from}&date_req2={date_to}&VAL_NM_RQ={usd_id}"
    url_eur = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={eur_date_from}&date_req2={date_to}&VAL_NM_RQ={eur_id}"

    usd_r = get_html(url_usd)
    eur_r = get_html(url_eur)

    fx_usd_df = pd.read_xml(usd_r)
    fx_usd_df['Value'] = [x.replace(',', '.') for x in fx_usd_df['Value']]
    fx_usd_df.to_csv(fx_usd_file, sep=';', encoding='utf-8', index=False, header=False)

    fx_eur_df = pd.read_xml(eur_r)
    fx_eur_df['Value'] = [x.replace(',', '.') for x in fx_eur_df['Value']]
    fx_eur_df.to_csv(fx_eur_file, sep=';', encoding='utf-8', index=False, header=False)


def read_csv_currency(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        fields = ['Date', 'Curr_code', 'Nominal', 'Rate']
        reader = csv.DictReader(f, fields, delimiter=';')
        
        data_for_upload = []
        for row in reader:
            row['Date'] = datetime.strptime(row['Date'], '%d.%m.%Y')
            data_exists = FX_rate.query.filter(FX_rate.FX_date == row['Date'], FX_rate.Curr_id == get_curr_id(row['Curr_code'])).count()
            if data_exists == 0:
                data = {'FX_date': row['Date'], 
                                'Curr_id': get_curr_id(row['Curr_code']),
                                'Nominal': row['Nominal'],
                                'Rate': float(row['Rate']),}
                data_for_upload.append(data)
        db.session.bulk_insert_mappings(FX_rate, data_for_upload)
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            print_error(data, "Ошибка целостности данных: {}", e)
            db.session.rollback()
            raise
        except ValueError as e:
            print_error(data, "Неправильный формат данных: {}", e)
            db.session.rollback()
            raise


def get_curr_id(curr_code):
    db_data = CurrencyName.query.filter(CurrencyName.Curr_code == curr_code).first()
    curr_id = db_data.id

    return curr_id
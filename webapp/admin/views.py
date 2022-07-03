import csv, os
from datetime import datetime
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import pandas as pd
import numpy as np
import urllib.request
from xml.dom import minidom

from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.customer.views import get_id_Soldto_byINN, get_id_Soldto_bySoldto
from webapp.db import db
from webapp.admin.forms import AdminRegistrationForm, AdminUserUpdateForm
from webapp.admin.models import FX_rate
from webapp.user.models import User
from webapp.user.decorators import admin_required


blueprint = Blueprint('admin', __name__)


date_from = '01/01/2020'
date_to = datetime.today().strftime('%d/%m/%Y')
usd_id = 'R01235'
eur_id = 'R01239'

url_usd = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_from}&date_req2={date_to}&VAL_NM_RQ={usd_id}"
url_eur = f"http://www.cbr.ru/scripts/XML_dynamic.asp?date_req1={date_from}&date_req2={date_to}&VAL_NM_RQ={eur_id}"

path = os.getcwd()
now = datetime.today().strftime('%Y-%m-%d')
xml_usd_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_USD' + '_' + now + '.xml')
fx_usd_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_USD' + '_' + now + '.csv')
xml_eur_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_EUR' + '_' + now + '.xml')
fx_eur_file = os.path.join(UPLOAD_FOLDER, 'Exchange_rate_EUR' + '_' + now + '.csv')


@blueprint.route('/admin/')
@admin_required
def admin_index():
    title = 'Control Panel'
    return render_template('admin/index.html', page_title=title)


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
            new_user = User(username=user_name, email=user_email, role='admin')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировали пользователя!', category='alert-success')
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
    return render_template("user/user_admin_page.html", user=this_user, form=form, action_link=f"/user_update/{user_id}" )


@blueprint.route('/user_update/<int:user_id>', methods=['POST'])
@admin_required
def user_update(user_id):
    form = AdminUserUpdateForm()

    if form.validate_on_submit():
        user_to_update = User.query.filter(User.id == user_id).first()
        if request.form.get("Active"):

            user_to_update.id = request.form["user_id"]
            user_to_update.username = request.form["username"]
            user_to_update.role = request.form["userrole"]
            user_to_update.email = request.form["useremail"]
            user_to_update.comp_id = get_id_Soldto_bySoldto(request.form['cust_soldto'])
            user_to_update.is_deleted = False
        else:
            user_to_update.id = request.form["user_id"]
            user_to_update.username = request.form["username"]
            user_to_update.role = request.form["userrole"]
            user_to_update.email = request.form["useremail"]
            user_to_update.comp_id = get_id_Soldto_bySoldto(request.form['cust_soldto'])
            user_to_update.is_deleted = True

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
    fx_data = FX_rate.query.order_by(FX_rate.FX_date).all()
    return render_template("admin/fx_rate.html", fx_data=fx_data)


@blueprint.route("/update_fx")
@admin_required
def update_fx_usd():
    webFile = urllib.request.urlopen(url_usd)
    data = webFile.read()
    with open(xml_usd_file, "wb") as localFile:
        localFile.write(data)
        webFile.close()

    doc = minidom.parse(xml_usd_file)
    root = doc.getElementsByTagName("ValCurs")[0]

    currency = doc.getElementsByTagName("ValCurs")

    with open(fx_usd_file,"w") as out:
        for rate in currency:
            item = rate.getElementsByTagName('Record')
            sid = item[0].attributes['Id'].value
            date = item[0].attributes['Date'].value
            nominal = rate.getElementsByTagName("Nominal")[0]
            value = rate.getElementsByTagName("Value")[0]

            str = "{0}; {1}; {2}; {3}; {4} \n".format(
                date, sid, 'USD', 
                nominal.firstChild.data,
                value.firstChild.data, False)

            out.write(str)
    return redirect(url_for('admin.fx_page'))
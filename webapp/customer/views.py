from flask import Blueprint, render_template
import pandas as pd

from webapp.db import db
from webapp.customer.models import Customers, Addresses, YFRP, LoB, ShipTos, Managers, STLs, PaymentTerms
from webapp.user.decorators import admin_required


blueprint = Blueprint('сustomer', __name__)

data_file = '../DB_data.xlsx'


################################################################################
@blueprint.route("/customers")
@admin_required
def customers_page():
    cust_data = Customers.query.order_by(Customers.SoldTo_Name).all()
    return render_template("customer/customer_list.html", cust_data=cust_data)


@blueprint.route("/address")
@admin_required
def deladdress_page():
    return render_template('admin/del_addr.html')


@blueprint.route("/managers")
@admin_required
def managers_page():
    am_data = Managers.query.order_by(Managers.AM_name).all()
    return render_template("admin/managers.html", am_data=am_data)


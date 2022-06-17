import imp
from flask import Blueprint, redirect, render_template, url_for
from flask_login import logout_user
from webapp.user.views import logout

from webapp.db import db
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')


@blueprint.route('/')
@admin_required
def admin_index():
    title = 'Control Panel'
    return render_template('admin/index.html', page_title=title)


@blueprint.route("/users")
@admin_required
def users_page():
    return render_template("admin/users.html")


@blueprint.route("/customers")
def customers_page():
    return render_template("admin/customers.html")


@blueprint.route("/managers")
def managers_page():
    return render_template("admin/managers.html")


@blueprint.route("/products")
def products_page():
    return render_template("admin/products.html")
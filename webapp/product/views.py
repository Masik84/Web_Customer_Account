from flask import Blueprint, render_template, flash, redirect, url_for, abort
from flask_login import current_user

from webapp.db import db
from webapp.product.models import Materials, SalProducts, ProdFamily, ProdSubClass, MaterialStatus, BOs

blueprint = Blueprint('products', __name__, url_prefix='/products')


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

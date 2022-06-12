from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.db import db_session
from webapp.product.models import Materials, SalProducts, ProdFam, ProdSubClass, MaterialStatus, BOs

blueprint = Blueprint('products', __name__, url_prefix='/products')
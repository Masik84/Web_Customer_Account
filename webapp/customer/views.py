from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.db import db_session
from webapp.customer.models import Customers, Addresses, YFRP, LoB, ShipTos, Managers, STLs, PaymentTerms

blueprint = Blueprint('сustomer', __name__, url_prefix='/customers')
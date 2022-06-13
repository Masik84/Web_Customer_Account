from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from webapp.db import db
from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')
#@admin_required
def admin_index():
    title = 'Панель управления'
    return render_template('admin/index.html', page_title=title)


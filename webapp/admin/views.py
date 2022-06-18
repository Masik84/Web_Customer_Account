import os
from flask import Blueprint, abort, flash, redirect, render_template, request, send_from_directory, url_for
from werkzeug.utils import secure_filename

#from webapp.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from webapp.db import db
from webapp.user.models import User
from webapp.user.decorators import admin_required
from webapp.user.forms import UserDataForm

from webapp.customer.models import STLs, Managers, LoB, Customers

blueprint = Blueprint('admin', __name__)


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


@blueprint.route('/user/<int:user_id>')
def single_user(user_id):
    form = UserDataForm()
    this_user = User.query.filter(User.id == user_id).first()
    if not this_user:
        abort(404)
    return render_template("user/user_single.html", user=this_user, form=form, action_link=f"/user_update/{user_id}" )


@blueprint.route('/user_update/<int:user_id>', methods=['POST'])
def user_update(user_id):
    form = UserDataForm()

    #if form.validate_on_submit():
    user_to_update = User.query.filter(User.id == user_id).first()

    if request.form['update']:
        user_to_update.id = request.form["user_id"]
        user_to_update.username = request.form["username"]
        user_to_update.role = request.form["userrole"]
        user_to_update.email = request.form["useremail"]

        db.session.commit()

        flash('User updated successfully')
        return redirect(url_for('admin.users_page'))

    elif request.form['delete']:
        user_to_delete = User.query.filter(User.id == user_id).first()
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect(url_for('admin.users_page'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in field "{}": - {}'.format(
                    getattr(form, field).label.text, 
                    error
                ))
    return redirect(url_for('admin.admin_index'))


################################################################################
@blueprint.route("/customers")
def customers_page():
    cust_data = Customers.query.order_by(Customers.SoldTo_Name).all()
    return render_template("customer/customer_list.html", cust_data=cust_data)


@blueprint.route("/address")
def deladdress_page():
    return render_template('admin/del_addr.html')


@blueprint.route("/managers")
def managers_page():
    am_data = Managers.query.order_by(Managers.AM_name).all()
    return render_template("admin/managers.html", am_data=am_data)


################################################################################
@blueprint.route("/products")
def products_page():
    return render_template("admin/products.html")



################################################################################
path = os.getcwd()
UPLOAD_FOLDER = 'test_data'
ALLOWED_EXTENSIONS = {'xls', 'xlsx'}


def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('uploaded_file', filename=filename))
    return redirect(url_for('admin.admin_index'))

@blueprint.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import current_user, login_required, login_user, logout_user, LoginManager

from datetime import datetime

# from webapp import user_id
from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm, UserDataUpdateForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


@blueprint.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы вошли на сайт')
            return redirect(url_for('index'))

    flash('Неправильное имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле "{}": - {}'.format(
                    getattr(form, field).label.text, 
                    error
                ))
        return redirect(url_for('user.register'))


@blueprint.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@blueprint.route('/me')
@login_required
def single_user():
    if current_user.is_authenticated:
        form = UserDataUpdateForm()
        return render_template("user/user_own_page.html", user=current_user, form=form)


@blueprint.route('/', methods=['POST'])
@login_required
def user_self_update():
    form = UserDataUpdateForm()
    if form.validate_on_submit():
        user_to_update = User.query.filter(User.id == current_user.id).first()

        user_to_update.username = request.form["username"]
        user_to_update.email = request.form["useremail"]

        db.session.commit()

        flash('Info updated successfully')
        return redirect(url_for('index'))

    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Error in field "{}": - {}'.format(
                    getattr(form, field).label.text, 
                    error
                ))
    return redirect(url_for('index'))


@blueprint.route('/delete_me', methods=['POST'])
@login_required
def user_self_delete():
    pass
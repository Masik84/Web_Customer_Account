from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, ValidationError

from webapp.user.models import User


class AdminRegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    role = SelectField('Role', validators=[DataRequired()], choices=[("", "Please Choose"), ("1", "admin"), ("2", "user")], render_kw={"class": "form-control"})
    cust_inn = StringField('Company Tax Code (INN)', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Submit!',render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')
    
    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')


class AdminUserUpdateForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()], render_kw={"class": "form-control"})
    username = StringField("User Name", validators=[DataRequired()], render_kw={"class": "form-control"})
    useremail = StringField("User Email", validators=[DataRequired()], render_kw={"class": "form-control"})
    userrole = StringField("User Role", validators=[DataRequired()], render_kw={"class": "form-control"})
    cust_soldto = StringField('Company Code', validators=[DataRequired()], render_kw={"class": "form-control"})
    del_flag = BooleanField('Deletion Flag', validators=[DataRequired()], render_kw={"class": "form-control"})
    update = SubmitField('Update', render_kw={"class": "btn btn-primary"})
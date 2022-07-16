from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField, HiddenField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length

from webapp.user.models import User



class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=4, max=100)], render_kw={"class": "form-control"},  )
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Отправить', render_kw={"class":"btn btn-primary"})

    def get_id(self):
        return str(self.__user['id'])

        

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    cust_inn = StringField('Company Tax Code (INN)', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль', validators=[DataRequired(), EqualTo('password')], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить!',render_kw={"class": "btn btn-primary"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с таким именем уже зарегистрирован')
    
    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError('Пользователь с такой электронной почтой уже зарегистрирован')


class UserDataUpdateForm(FlaskForm):
    user_id = HiddenField('User ID', validators=[DataRequired()], render_kw={"class": "form-control"})
    username = StringField("User Name", validators=[DataRequired()], render_kw={"class": "form-control"})
    useremail = StringField("User Email", validators=[DataRequired()], render_kw={"class": "form-control"})
    update = SubmitField('Save', render_kw={"class": "btn btn-primary"})
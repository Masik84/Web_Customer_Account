from getpass import getpass
import sys

from webapp import create_app
from webapp.db import db_session
from webapp.user.models import User

app = create_app()

with app.app_context():
    username = input('Введите имя пользователя: ')
    admin_email = input('Введите email: ')

    if User.query.filter(User.username == username).count():
        print('Такой пользователь уже есть')
        sys.exit(0)

    password = getpass('Введите пароль: ')
    password2 = getpass('Повторите пароль: ')
    if not password == password2:
        sys.exit(0)

    new_user = User(username=username, role='admin', email = admin_email)
    new_user.set_password(password)

    db_session.add(new_user)
    db_session.commit()
    print('User with id {} added'.format(new_user.id))
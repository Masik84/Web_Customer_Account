import logging
from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate

from logging.handlers import RotatingFileHandler, SMTPHandler

from webapp.db import db

from webapp.admin.views import blueprint as admin_blueprint
from webapp.customer.views import blueprint as customer_blueprint
from webapp.price.views import blueprint as price_blueprint
from webapp.product.views import blueprint as product_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.order.views import blueprint as oder_blueprint


def create_app():

    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    migrate = Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    app.register_blueprint(admin_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(price_blueprint)
    app.register_blueprint(oder_blueprint)

    # if not app.debug:
    #     if not os.path.exists('logs'):
    #             os.mkdir('logs')
    #     file_handler = RotatingFileHandler('logs/mylog.log', maxBytes=10240, backupCount=10)
    #     file_handler.setFormatter(logging.Formatter(
    #         '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    #     file_handler.setLevel(logging.INFO)

    #     app.logger.addHandler(file_handler)

    #     app.logger.setLevel(logging.INFO)
    #     app.logger.info('Microblog startup')


    @app.route("/")
    def index():
        title = 'First site'
        return render_template('main_win/index.html', page_title = title)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    return app




from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import db
from webapp.customer.models import Customers


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    role = Column(String(10), index=True)
    email = Column(String(50))
    comp_id = Column(Integer, ForeignKey(Customers.id), index=True, nullable = True)
    created_on = Column(db.DateTime, default=datetime.utcnow)
    last_visit = Column(db.DateTime, default=datetime.utcnow)
    is_deleted = Column(db.Boolean, default=False)

    customer_table = relationship("Customers")

    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_anonymous(self):
        return False


    def __repr__(self):
        return '<User {}>'.format(self.username)
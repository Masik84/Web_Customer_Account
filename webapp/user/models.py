
from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash

from webapp.db import Base, engine

db = SQLAlchemy()

class User(Base, db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    password = Column(String(128))
    role = Column(String(10), index=True)
    email = Column(String(50))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    #customer = relationship("Customers")

    def __repr__(self):
        return f'Company id: {self.id}, name: {self.name}'


    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin'


    def __repr__(self):
        return '<User {}>'.format(self.username)



if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
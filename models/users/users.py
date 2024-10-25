from connectors.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from bcrypt import hashpw, gensalt, checkpw
from flask_login import UserMixin

class UserModel(Base, UserMixin):
    __tablename__ ='users'

    user_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default='user')
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<User {self.user_id}>'

    def get_id(self):
        return (self.user_id)

    def set_password(self, password):
        self.password = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password):
        return checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
from connectors.db import Base
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from bcrypt import hashpw, gensalt, checkpw
from flask_login import UserMixin

class ReviewModel(Base, UserMixin):
    __tablename__ = 'reviews'
    
    review_id = Column(Integer, primary_key=True)
    description = Column(String(300), nullable=False)
    user_email = Column(String(120), ForeignKey('users.email'), nullable=False)
    rating = Column(Integer, nullable=False)
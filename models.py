from app import sqlalchemy, session, Base
from datetime import datetime


class Advertisement(Base):
    __tablename__ = 'Advertisement'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String(128), nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    created_at = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.utcnow)
    owner = sqlalchemy.Column(sqlalchemy.String(30), nullable=False)
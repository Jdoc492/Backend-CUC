from app import db
from sqlalchemy.dialects.mysql import JSON

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(120), nullable=False)



class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="Pendiente")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resources = db.Column(db.String, nullable=True)  # Almacena los IDs de recursos como JSON

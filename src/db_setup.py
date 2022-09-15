from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import quiz_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = quiz_config.db_connection_string
db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    id: int
    username: str
    email: str
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

@dataclass
class Quiz(db.Model):
    id: int
    user_id: int
    answer: str
    
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.JSON, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
@dataclass
class Distance(db.Model):
    user1_id: int
    user2_id: int
    distance: float

    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    distance = db.Column(db.Float, nullable=False)
    
db.create_all()
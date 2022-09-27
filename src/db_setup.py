from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import quiz_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = quiz_config.db_connection_string
db = SQLAlchemy(app)

# Info utente
@dataclass
class User(db.Model):
    id: int
    username: str
    email: str
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

# Pesi categorie
class Category(db.Model):
    id: int
    description: str
    weight: float
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))
    weight = db.Column(db.Float, nullable=False)

# Schema quiz
@dataclass
class Quiz(db.Model):
    id: int
    question: str
    question_id: str
    category_id: int
    
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(250), nullable=False)
    question_id = db.Column(db.String(10), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

# Risposte degli utenti al quiz
@dataclass
class UserQuiz(db.Model):
    id: int
    user_id: int
    question_id: str
    answer: str
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.String(10), db.ForeignKey('quiz.question_id'), nullable=False)
    answer = db.Column(db.String(10), nullable=False)

# Distanze calcolate fra utenti
@dataclass
class Distance(db.Model):
    user1_id: int
    user2_id: int
    distance: float

    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    distance = db.Column(db.Float, nullable=False)
    
db.create_all()
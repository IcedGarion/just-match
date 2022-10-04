from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import quiz_config

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = quiz_config.db_connection_string
db = SQLAlchemy(app)


''' Tabelle schema '''
# Tipi di attivita' 
@dataclass
class Activity(db.Model):
    id: int
    description: str
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))

# N:M activity-category: per ogni attivita' (gruppo/singolo/viaggi...) elenco di pesi da dare a tutte le categorie
# TODO: per ogni attivita' devono essere elencati i pesi per TUTTE le categorie presenti in tab categorie: Left join con default isnull(weigth, 0)
@dataclass
class WeightCategory(db.Model):
    id: int
    activity_id: int
    category_id: int
    weight: float
    
    id = db.Column(db.Integer, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    weight = db.Column(db.Float, nullable=False)

# Categorie di domande
@dataclass
class Category(db.Model):
    id: int
    description: str
    
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(250))

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

# Valori costanti (es, max e min answer value)
@dataclass
class Constant(db.Model):
    id: int
    name: str
    value: str
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    value = db.Column(db.String(250), nullable=False)

@dataclass
class Normalization(db.Model):
    id: int
    category_id: str
    value: float
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)


''' Tabelle dati '''
# Info utente
@dataclass
class User(db.Model):
    id: int
    username: str
    email: str
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), nullable=False)

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

# Distanze calcolate fra utenti, all'interno di ogni categoria
@dataclass
class Distance(db.Model):
    user1_id: int
    user2_id: int
    category_id: int
    distance: float

    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), primary_key = True)
    distance = db.Column(db.Float, nullable=False)

# Distanze calcolate fra utenti, risultato di media fra le distanze per categoria, pesi dati dal tipo di attivita
@dataclass
class ActivityDistance(db.Model):
    user1_id: int
    user2_id: int
    activity_id: int
    distance: float
    
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    activity_id = db.Column(db.Integer, db.ForeignKey('activity.id'), primary_key = True)
    distance = db.Column(db.Float, nullable=False)

# Hobby + immagini
@dataclass
class Hobby(db.Model):
    id: int
    name: str
    description: str
    img_url: str

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(250))
    img_url = db.Column(db.Text(100))


db.create_all()
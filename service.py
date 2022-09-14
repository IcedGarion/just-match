from db_setup import db, app, User, Quiz, Distance
from quiz_distance import calc_distance
import numpy as np


def get_all_users():
    return User.query.all()
    
def get_user(user_id: str):
    return User.query.filter_by(id=user_id).first()
    
def create_user(user):
    new_user = User(username=user["username"], email=user["email"])
    
    # TODO: check se esiste gia username/password
    db.session.add(new_user)
    db.session.commit()
    return new_user
    
def create_quiz(user_id: str, quiz):
    # TODO: check se user_id passato esiste effettivamente
    user = User.query.filter_by(id=user_id).first()
    new_quiz = Quiz(answer=quiz, user_id=user.id)
    db.session.add(new_quiz)
    db.session.commit()
    
    
    # nuovo quiz: calcola le distanze fra quiz utente e tutti gli altri
    
    # TODO
    # Da ottimizzare: calcolare distanze solo per il nuovo utente verso tutti gli altri + tutti gli altri solo verso il nuovo utente
    # Qua per ora calcola tutte le distanze di tutti tutti
    # da spostare in quiz_distance
    all_quiz = Quiz.query.all()
    for quiz in all_quiz:
        risposte = [[int(risposta['risposta'])] for risposta in quiz.answer ]
        
        altri_quiz = Quiz.query.all()
        for altro_quiz in altri_quiz:
            altre_risposte = [[int(risposta['risposta'])] for risposta in altro_quiz.answer ]
            distanza = np.linalg.norm(np.array(risposte) - np.array(altre_risposte))
            print(user_id, altro_quiz.user_id, distanza)
            
            # salva su db distanze appena calcolate
            new_distance = Distance(user1_id=quiz.user_id, user2_id=altro_quiz.user_id, distance=distanza)
            db.session.add(new_distance)
            db.session.commit()

    return new_quiz
    

# da fare in thread parallelo
def _calc_user_distance(user_id, quizzes):
    pass

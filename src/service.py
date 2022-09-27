from db_setup import db, app, User, UserQuiz, Distance
from quiz_distance import calc_distance
from threading import Thread
from time import sleep
import numpy as np


def get_all_users():
    return User.query.all()
    
def get_user(user_id: str):
    return User.query.filter(User.id == user_id).first()
    
def create_user(user):
    new_user = User(username=user["username"], email=user["email"])
    
    # check se esiste gia' username
    existing_user = User.query.filter(User.username == new_user.username).all()
    if len(existing_user) != 0:
        raise AssertionError("Username already exists: '{}'".format(new_user.username))
    
    db.session.add(new_user)
    db.session.commit()
    return new_user

def get_nearest_users(user_id: str, top: int):
    # check se user_id passato esiste effettivamente
    existing_user = User.query.filter(User.id == user_id).all()
    if len(existing_user) == 0:
        raise AssertionError("User_id does not exists: {}".format(user_id))
        
    nearest_users = Distance.query.filter(Distance.user1_id == user_id).order_by(Distance.distance.asc()).limit(top).all()
    
    return nearest_users

    
def create_quiz(user_id: str, quiz_json):
    # check se user_id passato esiste effettivamente
    existing_user = User.query.filter(User.id == user_id).all()
    if len(existing_user) == 0:
        raise AssertionError("User_id does not exists: {}".format(user_id))

    # recupera evantuale quiz gia' esistente per quel user
    user_quiz = UserQuiz.query.filter(UserQuiz.user_id == user_id).order_by(UserQuiz.question_id.asc()).all()
    
    # Aggiorna quiz gia esistente rimpiazzando tutto
    if len(user_quiz) != 0:
        # per ciascuna nuova risposta, modifica la vecchia risposta
        for answer in quiz_json:
            old_user_quiz =  UserQuiz.query.filter(UserQuiz.user_id == user_id).filter(UserQuiz.question_id == answer["id"]).first()
            old_user_quiz.answer = answer["risposta"]
        db.session.commit()
    
    # Aggiunge nuovo quiz
    # TODO: mancano le category in json quiz
    else:
        new_quiz = [ UserQuiz(answer=answer["question"], question_id=answer["id"], user_id=user_id) for answer in quiz_json ]
        db.session.add_all(new_quiz)
        db.session.commit()
    
    # nuovo quiz: calcola le distanze fra quiz utente e tutti gli altri
    Thread(target = _calc_user_distance, args = (user_quiz, )).start()
    
    return user_quiz



def _calc_user_distance(user_quiz):
    # TODO: fare in modo che parta solo quando ha finito di inserire il nuovo quiz qua sopra ?
    sleep(2)

    # prendere a gruppi di users il quiz e poi darlo in pasto al for qua sotto
    # (serve calcolare la distinct sui user_id prima (escludendo il mio user_id), e poi fare ogni volta la query su userquiz prendendo solo un user_id alla volta
    
    # prende tutti gli altri user_id
    user_id = user_quiz[0].user_id
    users_ids = [ result[0] for result in UserQuiz.query.filter(UserQuiz.user_id != user_id).with_entities(UserQuiz.user_id).distinct().all() ]
    if len(users_ids) == 0:
        raise AssertionError("Not enough user quiz (1) to calculate distance")

    # per ciascun altro user legge tutto il suo quiz e calcola distanza
    distances_from_me = []
    for other_user_id in users_ids:
        other_user_quiz = UserQuiz.query.filter(UserQuiz.user_id == other_user_id).order_by(UserQuiz.question_id.asc()).all()
        distances_from_me.extend(calc_distance(user_quiz, other_user_quiz))

    # se userid1 sono io, aggiungi tutti quelli che trovi
    # se userid1 non sono io, aggiungi solo quelli che hanno come userid2 = io    
    for new_dist in distances_from_me:
        print(new_dist)
        if new_dist.user1_id == user_id or (new_dist.user1_id != user_id and new_dist.user2_id == user_id):
            # se esisteva gia' una distanza fra i due user (caso in cui si inserisce un nuovo quiz), aggiorna quello esistente
            existing_distance = Distance.query.filter(Distance.user1_id == new_dist.user1_id and Distance.user2_id == new_dist.user2_id).all()
            if len(existing_distance) == 0:
                db.session.add(new_dist)            

    db.session.commit()
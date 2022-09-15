from db_setup import db, app, User, Quiz, Distance
from quiz_distance import calc_distance
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
    
def create_quiz(user_id: str, quiz_json):
    # check se user_id passato esiste effettivamente
    existing_user = User.query.filter(User.id == user_id).all()
    if len(existing_user) == 0:
        # TODO GESTIONE ERRORI
        raise AssertionError("User_id does not exists: '{}'".format(user_id))

    # recupera evantuale quiz gia' esistente per quel user
    user_quiz = Quiz.query.filter(Quiz.user_id == user_id).all()
    
    # Aggiorna quiz gia esistente
    if len(user_quiz) != 0:
        user_quiz = user_quiz[0]
        user_quiz.answer = quiz_json
        db.session.commit()
    
    # Aggiunge nuovo quiz
    else:
        user_quiz = Quiz(answer=quiz_json, user_id=existing_user[0].id)
        db.session.add(user_quiz)
        db.session.commit()
    
    
    # _calc_user_distance
    # nuovo quiz: calcola le distanze fra quiz utente e tutti gli altri
    all_other_quiz = Quiz.query.filter(Quiz.user_id != user_id).all()
    
    _calc_user_distance(user_quiz, all_other_quiz)
    
    return user_quiz


# da fare in thread parallelo
def _calc_user_distance(user_quiz, all_other_quiz):
    distances_from_me = calc_distance(user_quiz, all_other_quiz)

    # se userid1 sono io, aggiungi tutti quelli che trovi
    # se userid1 non sono io, aggiungi solo quelli che hanno come userid2 = io    
    for new_dist in distances_from_me:
        if new_dist.user1_id == user_quiz.user_id or (new_dist.user1_id != user_quiz.user_id and new_dist.user2_id == user_quiz.user_id):
            # se esisteva gia' una distanza fra i due user (caso in cui si inserisce un nuovo quiz), aggiorna quello esistente
            existing_distance = Distance.query.filter(Distance.user1_id == new_dist.user1_id and Distance.user2_id == new_dist.user2_id).all()
            if len(existing_distance) == 0:
                db.session.add(new_dist)            

    db.session.commit()

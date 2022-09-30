from db_setup import db, app, User, UserQuiz, Quiz, Distance, Category, WeightCategory, Activity, ActivityDistance
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

def get_nearest_users(user_id: str, activity_id: int, top: int):
    # check se user_id passato esiste effettivamente
    existing_user = User.query.filter(User.id == user_id).all()
    if len(existing_user) == 0:
        raise AssertionError("User_id does not exists: {}".format(user_id))
        
    # check se l'attivita' passata esiste
    existing_activity = Activity.query.filter(Activity.id == activity_id).all()
    if len(existing_activity) == 0:
        raise AssertionError("Activity_id does not exists: {}".format(activity_id))

    # calcola distanza globale in base all'attivita' scelta
    _calc_global_distance(existing_user[0], existing_activity[0])
    
    # calcolate le distanze e salvate su db, le rilegge, ordina per piu vicino e prende i primi <top> user_id
    nearest_users_id = [ x.user2_id for x in sorted(ActivityDistance.query.filter(ActivityDistance.user1_id == existing_user[0].id).filter(ActivityDistance.activity_id == existing_activity[0].id).all(),
                key=lambda x: x.distance)[0:top] ]
    
    # Ritorna gli utenti associati
    return User.query.filter(User.id.in_(nearest_users_id)).all()


# TODO: caso in cui si aggiungono soltanto 1+ risposte NUOVE? 
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
    else:
        user_quiz = sorted([ UserQuiz(answer=answer["risposta"], question_id=answer["id"], user_id=user_id) for answer in quiz_json ], key=lambda x: x.question_id)
        db.session.add_all(user_quiz)
        db.session.commit()
    
    # nuovo quiz: calcola le distanze fra quiz utente e tutti gli altri
    Thread(target = _calc_category_distance, args = (user_quiz, )).start()
    
    return user_quiz


''' Calcola distanze all'interno di ciascuna categoria'''
def _calc_category_distance(user_quiz):
    # TODO: fare in modo che parta solo quando ha finito di inserire il nuovo quiz qua sopra ?
    sleep(2)
  
    # prende tutti gli altri user_id
    user_id = user_quiz[0].user_id
    users_ids = [ result[0] for result in UserQuiz.query.filter(UserQuiz.user_id != user_id).with_entities(UserQuiz.user_id).distinct().all() ]
    if len(users_ids) == 0:
        raise AssertionError("Not enough user quiz (1) to calculate distance")

    # prende tutte le categorie
    categories = [ x[0] for x in Category.query.with_entities(Category.id).distinct().all() ]
    distances_from_me = []
    
    # per ciascuna categoria calcola le distanze
    for category in categories:
        # per ciascuna categoria estrae solo i quiz di quella categoria
        question_ids_per_category = [ x[0] for x in Quiz.query.filter(Quiz.category_id == category).with_entities(Quiz.question_id).all() ]
        user_category_quiz = [ quiz for quiz in user_quiz if quiz.question_id in question_ids_per_category ]
        
        # TODO1: calcolo distanze esegue solo se utente ha compilato tutte le domande di una categoria 
        # TODO2: (question_ids_per_category) == 0 vuol dire che non hai ancora inserito le domande per le altre categorie id>0
        if len(user_category_quiz) != len(question_ids_per_category) or len(question_ids_per_category) == 0:
            continue
    
        # per ciascun altro user legge tutto il suo quiz (cambiando ogni volta la categoria) e calcola distanza
        for other_user_id in users_ids:
            other_user_category_quiz = [ x for x in UserQuiz.query.filter(UserQuiz.user_id == other_user_id).order_by(UserQuiz.question_id.asc()).all() if x.question_id in question_ids_per_category]
            distances_from_me.extend(calc_distance(user_category_quiz, other_user_category_quiz, category))

    # se userid1 sono io, aggiungi tutti quelli che trovi
    # se userid1 non sono io, aggiungi solo quelli che hanno come userid2 = io    
    for new_dist in distances_from_me:
        if new_dist.user1_id == user_id or (new_dist.user1_id != user_id and new_dist.user2_id == user_id):
            # se esisteva gia' una distanza fra i due user (caso in cui si inserisce un nuovo quiz), aggiorna quello esistente
            existing_distance = Distance.query.filter(Distance.user1_id == new_dist.user1_id and Distance.user2_id == new_dist.user2_id).all()
            if len(existing_distance) == 0:
                db.session.add(new_dist)            

    db.session.commit()
    # TODO: spostare in file separato e qua ritornare gli oggetti da salvare


''' Calcola media delle distanze globali per ciascuna categoria usando i pesi a seconda dell'attivita' '''
def _calc_global_distance(user: User, activity: Activity):
    # recupera elenco categorie + pesi delle categorie in base all'attivita
    category_weights = { weight_category.category_id: weight_category.weight for weight_category in WeightCategory.query.filter(WeightCategory.activity_id == activity.id).all() }
    
    # prende tutti gli altri user che hanno delle distanze gia' calcolate
    users_ids = [ result[0] for result in Distance.query.filter(Distance.user1_id != user.id).with_entities(Distance.user1_id).distinct().all() ]
    
    users_distance = []
    for other_user_id in users_ids:
        # controlla subito se la distanza globale fra i 2 utenti era gia stata calcolata; se c'e' gia allora skippa il calcolo
        existing_distance = ActivityDistance.query.filter(ActivityDistance.user1_id == user.id).filter(ActivityDistance.user2_id == other_user_id).filter(ActivityDistance.activity_id == activity.id).all()
        if len(existing_distance) != 0:
            continue
    
        # recupera le distanze fra utente e un altro utente
        category_distances = Distance.query.filter(Distance.user1_id == user.id).filter(Distance.user2_id == other_user_id).all()
        
        # array distanze e pesi per ognuna delle distanze di categoria
        distances = []
        weights = []
        for distance in category_distances:
            # TODO1: sta usando soltanto le distanze che ha, quindi se mancano risposte ai quiz (se una categoria di risposte e' incompleta o manca completamente non la usa)
            distances.append(distance.distance)
            weights.append(category_weights[distance.category_id])

        # fa la media usando i pesi delle categorie e crea oggetto ActivityDistance + reverse
        weighted_avg = np.average(distances, weights=weights)
        users_distance.append(ActivityDistance(user1_id=user.id, user2_id=other_user_id, activity_id=activity.id, distance=weighted_avg))
        users_distance.append(ActivityDistance(user2_id=user.id, user1_id=other_user_id, activity_id=activity.id, distance=weighted_avg))
    
    if len(users_distance) != 0:
        db.session.add_all(users_distance)
        db.session.commit()    
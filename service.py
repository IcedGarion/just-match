from db_setup import db, app, User, Quiz, Distance
from quiz_distance import calc_distance


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
    user = User.query.filter_by(id=user_id).first()
    new_quiz = Quiz(answer=str(quiz), user_id=user.id)
    db.session.add(new_quiz)
    db.session.commit()
    
    calc_distance(user.id)
    
    return new_quiz
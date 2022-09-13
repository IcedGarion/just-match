from flask import jsonify, request
from db_setup import db, app, User, Quiz, Distance
import quiz_config
from quiz_distance import calc_distance


@app.route("/users", methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify(users)

@app.route("/users/<user_id>", methods=['GET'])
def list_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return jsonify(user)

@app.route("/users", methods=['POST'])
def add_user():
    new_user = User(username=request.json["username"], email=request.json["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user)

@app.route("/quiz/<user_id>", methods=['POST'])
def add_quiz(user_id):
    user = User.query.filter_by(id=user_id).first()
    new_quiz = Quiz(answer=str(request.json), user_id=user.id)
    db.session.add(new_quiz)
    db.session.commit()
    calc_distance(user.id)
    return jsonify(new_quiz)
    
@app.route("/distance/<user_id>", methods=['GET'])
def get_nearest(user_id):
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)
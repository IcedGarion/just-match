from flask import jsonify, request
from db_setup import db, app, User, Quiz, Distance
import quiz_config
import service


@app.route("/users", methods=['GET'])
def list_users():
    users = service.get_all_users()
    return jsonify(users)

@app.route("/users/<user_id>", methods=['GET'])
def list_user(user_id):
    user = service.get_user(user_id)
    return jsonify(user)

@app.route("/users", methods=['POST'])
def add_user():
    new_user = service.create_user(request.json)
    return jsonify(new_user)

@app.route("/quiz/<user_id>", methods=['POST'])
def add_quiz(user_id):
    new_quiz = service.create_quiz(user_id, request.json)
    return jsonify(new_quiz)
    
@app.route("/distance/<user_id>", methods=['GET'])
def get_nearest(user_id):
    pass

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)
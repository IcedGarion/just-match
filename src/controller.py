from flask import jsonify, request, abort, Response
from db_setup import db, app, User, Quiz, Distance
from quiz_config import app_host
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
    try:
        new_user = service.create_user(request.json)
        return jsonify(new_user)
    except AssertionError as e:
        return { "error":  "{}".format(str(e)) }, 409

@app.route("/quiz/<user_id>", methods=['POST'])
def add_quiz(user_id):
    try:
        new_quiz = service.create_quiz(user_id, request.json)
        return jsonify(new_quiz)
    except AssertionError as e:
        return { "error":  "{}".format(str(e)) }, 404
    
@app.route("/distance/<user_id>/<top>", methods=['GET'])
def get_nearest(user_id, top):
    try:
        nearest = service.get_nearest_users(user_id, top)
        return jsonify(nearest)
    except AssertionError as e:
        return { "error":  "{}".format(str(e)) }, 404

# solo per debug
@app.route("/distance", methods=['GET'])
def list_distances():
    from db_setup import Distance
    return Distance.query.all()

@app.route("/quiz", methods=['GET'])
def list_quizzes():
    return Quiz.query.all()



if __name__ == '__main__':
    app.run(host=app_host, threaded=True)
from flask import jsonify, request, abort, Response
from werkzeug.exceptions import HTTPException
from db_setup import db, app, User, Quiz, Distance, ActivityDistance
from quiz_config import app_host
import service

# USER
@app.route("/users", methods=['GET'])
def list_users():
    users = service.get_all_users()
    return jsonify(users)

@app.route("/users/<int:user_id>", methods=['GET'])
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

# ACTIVITY
@app.route("/activity", methods=['GET'])
def list_activities():
    activities = service.get_all_activities()
    return jsonify(activities)

# CATEGORY
@app.route("/category", methods=['GET'])
def list_categories():
    categories = service.get_all_categories()
    return jsonify(categories)

# QUIZ
@app.route("/quiz", methods=['GET'])
def list_quizzes():
    return Quiz.query.all()

@app.route("/quiz/<int:user_id>", methods=['POST'])
def add_quiz(user_id):
    try:
        new_quiz = service.create_quiz(user_id, request.json)
        return jsonify(new_quiz)
    except AssertionError as e:
        return { "error":  "{}".format(str(e)) }, 404

# DISTANCE
@app.route("/distance/<int:user_id>/<int:activity_id>/<int:top>", methods=['GET'])
def get_nearest(user_id, activity_id, top):
    try:
        nearest = service.get_nearest_users(user_id, activity_id, top)
        return jsonify(nearest)
    except AssertionError as e:
        return { "error":  "{}".format(str(e)) }, 404


# HOBBY
@app.route("/hobby", methods=['GET'])
def list_hobbies():
    return


# solo per debug
@app.route("/distance", methods=['GET'])
def list_distances():
    from db_setup import Distance
    return Distance.query.all()
    
@app.route("/activity_distance", methods=['GET'])
def list_global_distances():
    from db_setup import Distance
    return ActivityDistance.query.all()


# error handling
@app.errorhandler(HTTPException)
def handle_exception(e):
    return jsonify({"error": e.description, "code": e.code}), e.code


if __name__ == '__main__':
    app.run(host=app_host, threaded=True)
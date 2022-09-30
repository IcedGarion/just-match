from db_setup import db, Quiz, Category, Activity, WeightCategory
import json


schema_quiz_json = "data/schema_quiz.json"
schema_category_json = "data/schema_category.json"
schema_activity_json = "data/schema_activity.json"
schema_pesi_json = "data/schema_pesi.json"

if __name__ == "__main__":
    # category
    schema = json.load(open(schema_category_json))
    data = [ Category(id=category["id"],description=category["description"]) for category in schema ]
    db.session.add_all(data)
    db.session.commit()
    
    # activity
    schema = json.load(open(schema_activity_json))
    data = [ Activity(id=activity["id"],description=activity["description"]) for activity in schema ]
    db.session.add_all(data)
    db.session.commit()
    
    # pesi activity-category
    schema = json.load(open(schema_pesi_json))
    for activity in schema:
        data = [ WeightCategory(category_id=pesi["id"],activity_id=activity["activity_id"],weight=pesi["weight"]) for pesi in activity["categories"] ]
        db.session.add_all(data)
    db.session.commit()
    
    # quiz
    schema = json.load(open(schema_quiz_json))
    for category in schema:
        data = [ Quiz(question=question["question"], question_id=question["id"], category_id=int(category["category"])) for question in category["quiz"] ]
        db.session.add_all(data)
    db.session.commit()

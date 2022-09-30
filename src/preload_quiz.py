from db_setup import db, Quiz, Category
import json


schema_quiz_json = "data/schema_quiz.json"
schema_category_json = "data/schema_category.json"

if __name__ == "__main__":
    schema_category = json.load(open(schema_category_json))
    cat = [ Category(id=category["category"],description=category["description"]) for category in schema_category ]
    
    db.session.add_all(cat)
    db.session.commit()
    
    schema_quiz = json.load(open(schema_quiz_json))
    for category in schema_quiz:
        quiz = [ Quiz(question=question["question"], question_id=question["id"], category_id=int(category["category"])) for question in category["quiz"] ]
    
    db.session.add_all(quiz)
    db.session.commit()

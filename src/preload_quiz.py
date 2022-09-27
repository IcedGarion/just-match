from db_setup import db, Quiz
import json


schema_json = "data/schema_quiz.json"

if __name__ == "__main__":
    # TODO creare file schema.json
    schema = json.load(open(schema_json))
    for category in schema:
        quiz = [ Quiz(question=question["question"], question_id=question["id"], category=category["category"]) for question in category["quiz"] ]
    
    db.session.add_all(quiz)
    db.session.commit()
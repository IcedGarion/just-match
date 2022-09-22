from db_setup import db, Quiz
import json


schema_json = "data/risposte_elias.json"
# TODO: aggiungere categorie
category = "1"

if __name__ == "__main__":
    # TODO creare file schema.json
    schema = json.load(open(schema_json))
    quiz = [ Quiz(question=question["question"], question_id=question["id"], category=category) for question in schema ]
    
    db.session.add_all(quiz)
    db.session.commit()
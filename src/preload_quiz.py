from db_setup import db, Quiz, Category, Activity, WeightCategory, Constant, Normalization
import json
import numpy as np

schema_quiz_json = "data/schema_quiz.json"
schema_category_json = "data/schema_category.json"
schema_activity_json = "data/schema_activity.json"
schema_pesi_json = "data/schema_pesi.json"
schema_constants_json = "data/schema_constants.json"

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
    
    # costanti
    schema = json.load(open(schema_constants_json))
    data = [ Constant(id=constant["id"],name=constant["name"],value=constant["value"]) for constant in schema ]
    db.session.add_all(data)
    db.session.commit()
    
    # normalization
    ''' calcola fattore di normalizzazione per ciascuna categoria '''
    normalizations = []
    # recupera max/min value risposta
    max_val = Constant.query.filter(Constant.name == "max_answer_value").one()
    min_val = Constant.query.filter(Constant.name == "min_answer_value").one()

    categories = [ x[0] for x in Category.query.with_entities(Category.id).distinct().all() ]
    for category in categories:
        # per ogni categoria recupera il NUMERO tot di domande
        tot_questions = int(Quiz.query.filter(Quiz.category_id == category).count())
    
        # crea array lungo quanto il numero di domande, uno tutto a 0 e l'altro tutto a max value
        max_ansers = np.full((tot_questions,1), int(max_val.value))
        min_ansers = np.full((tot_questions,1), int(min_val.value))
         
        # calcola fattore norm
        norm_factor = np.linalg.norm(np.array(max_ansers) - np.array(min_ansers))
        normalizations.append(Normalization(category_id=category, value=norm_factor))
    
    db.session.add_all(normalizations)
    db.session.commit()
import numpy as np
from db_setup import Quiz, Distance

def calc_distance(my_quiz: Quiz, other_quizzes):
    risposte = [[int(risposta['risposta'])] for risposta in my_quiz.answer ]
    distanze = []

    for altro_quiz in other_quizzes:
        altre_risposte = [[int(risposta['risposta'])] for risposta in altro_quiz.answer ]
        distanza = np.linalg.norm(np.array(risposte) - np.array(altre_risposte))
        
        # crea oggetti distanze da salvare poi su db
        new_distance = Distance(user1_id=my_quiz.user_id, user2_id=altro_quiz.user_id, distance=distanza)
        reverse_new_distance = Distance(user2_id=my_quiz.user_id, user1_id=altro_quiz.user_id, distance=distanza)
        distanze.append(new_distance)
        distanze.append(reverse_new_distance)

    return distanze

'''
# { persona0: {domanda0: punteggio, domanda1: punteggio } }
f1 = open("risposte_elias.json")
f2 = open("risposte_andrea.json")

risposte_raw = { 'elias': json.load(f1),
             'andrea': json.load(f2) }

# Converte json risposte in formato numpy
risposte = dict()
for nome, questionario in risposte_raw.items():
    risposte.update({nome: [[int(risp['risposta'])] for risp in questionario]})

# calcola distanza max da usare come denominatore per normalizzare le distanze
num_risp = len(list(risposte.values())[0])
max_risp_val, min_risp_val = 4,0
norm = { "min": np.full((num_risp,1), max_risp_val),
         "max": np.full((num_risp,1), min_risp_val) }
max_distanza_possibile = np.linalg.norm(np.array(norm["max"]) - np.array(norm["min"]))
    
# calcola le distanze
distanze = dict()
for persona,risp in risposte.items():
    distanze.update({persona: dict()})
    for altra_persona,altre_risp in risposte.items():
        if(persona != altra_persona):
            distanza = (np.linalg.norm(np.array(risp) - np.array(altre_risp)) / max_distanza_possibile)
            distanze[persona].update({ altra_persona: distanza })
'''

'''

    for quiz in all_quiz:
        risposte = [[int(risposta['risposta'])] for risposta in quiz.answer ]
        
        altri_quiz = Quiz.query.all()
        for altro_quiz in altri_quiz:
            altre_risposte = [[int(risposta['risposta'])] for risposta in altro_quiz.answer ]
            distanza = np.linalg.norm(np.array(risposte) - np.array(altre_risposte))
            print(user_id, altro_quiz.user_id, distanza)
            
            # salva su db distanze appena calcolate
            new_distance = Distance(user1_id=quiz.user_id, user2_id=altro_quiz.user_id, distance=distanza)
            db.session.add(new_distance)
            db.session.commit()

    return new_quiz
    
'''
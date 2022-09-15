import numpy as np
from db_setup import Quiz, Distance

# TODO: normalizzazione (serve calcolare il denominatore, come costante)
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
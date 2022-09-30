import numpy as np
from db_setup import UserQuiz, Distance, Normalization

# TODO: normalizzazione (serve calcolare il denominatore, come costante)
def calc_distance(my_quiz, another_users_quiz, category):
    mie_risposte = [[int(risposta.answer)] for risposta in my_quiz ]
    sue_risposte = [[int(risposta.answer)] for risposta in another_users_quiz ]
    distanze = []

    # legge fattore di normalizzazione per questa categoria
    normalization_factor = Normalization.query.filter(Normalization.category_id == category).one()
    
    # calcola distanza vettoriale
    distanza = np.linalg.norm(np.array(mie_risposte) - np.array(sue_risposte)) / normalization_factor.value
   
    # crea oggetti distanze da salvare poi su db
    new_distance = Distance(user1_id=my_quiz[0].user_id, user2_id=another_users_quiz[0].user_id, distance=distanza, category_id=category)
    reverse_new_distance = Distance(user2_id=my_quiz[0].user_id, user1_id=another_users_quiz[0].user_id, distance=distanza, category_id=category)
    distanze.append(new_distance)
    distanze.append(reverse_new_distance)

    return distanze
import numpy as np
import json

def calc_distance(user_id: str):
    print("Calc distance")

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
## Install

### Python
apt install python3

### Flask / SQLAlchemy
pip3 install Flask Flask-SQLAlchemy SQLAlchemy

### numpy
pip3 install numpy

## Run
python3 controller.py

## Test
(data/test.sh)
<br>
curl -X POST localhost:5000/users -H 'Content-Type: application/json' -d '{"username": "andrea", "email": "andrea"}'
<br>
curl -X POST localhost:5000/users -H 'Content-Type: application/json' -d '{"username": "elias", "email": "elias"}'
<br>
curl -X POST localhost:5000/quiz/1 -H 'Content-Type: application/json' -d @risposte_andrea.json
<br>
curl -X POST localhost:5000/quiz/2 -H 'Content-Type: application/json' -d @risposte_elias.json
<br>
curl localhost:5000/distance

## API
### List users
Lists all users.<br><br>
`GET /users`


### List user
Lists single user specified by "id".<br><br>
`GET /users/<id>`

### Create user
Create new user with payload json data.<br><br>
`POST /users`<br><br>
Example json:<br>
`{ "username": "andrea", "email": "andrea"}`

### Create User Quiz
Create a new quiz answer for user specified by "id" with payload json data.<br><br>
`POST /quiz/<user_id>`<br><br>
Example json:<br>
`[
    {
        "question": "Sono in grado di chiudere gli occhi e raffigurarmi oggetti, luoghi o  avvenimenti",
        "risposta": "4",
        "id": "0"
    },
    {
        "question": "Leggo più facilmente cartine, tabelle e diagrammi piuttosto che  indicazioni scritte",
        "risposta": "4",
        "id": "1"
    }
]`

### Get nearest user
Return the top x "top" users nearest to the user specified by "id".<br><br>
`GET /distance/<user_id>/<top>`


# TODO
## Feature
### TODO2: Finire di inserire domande per le altre categorie
### E poi inserire dati quiz vero per almeno 10 utenti e testare se le distanze per activity funzionano

## Codice
### Caso in cui si aggiungono soltanto 1+ risposte NUOVE? 
### Fare in modo che calcolo distanza per nuovo quiz parta solo quando ha finito di inserire il nuovo quiz
### Spostare i calcoli in file a parte (non nel service)

## Errori
### TODO1: Se user compila solo parte del quiz, quando calcola le distanze cerca comunque tutte le categorie. Fare in modo che i calcoli distanza per categoria e distanza globale usino solo le categorie compilate
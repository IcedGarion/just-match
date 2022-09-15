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

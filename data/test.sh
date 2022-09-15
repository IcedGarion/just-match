
# inserisce user 1
curl -X POST localhost:5000/users -H 'Content-Type: application/json' -d '{"username": "andrea", "email": "andrea"}'
# inserisce user 2
curl -X POST localhost:5000/users -H 'Content-Type: application/json' -d '{"username": "elias", "email": "elias"}'

# inserisce quiz user1 (serve file risposte_andrea.json)
curl -X POST localhost:5000/quiz/1 -H 'Content-Type: application/json' -d @risposte_andrea.json
# inserisce quiz user2 (serve file risposte_elias.json)
curl -X POST localhost:5000/quiz/2 -H 'Content-Type: application/json' -d @risposte_elias.json

# mostra tutte le distanze appena calcolate
curl localhost:5000/distance
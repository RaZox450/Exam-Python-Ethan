# Réponses

## Exercice 1

__Question 1__ : Une route GET /stations crée une station. Quel verbe et quel code HTTP faut-il utiliser pour cette création ?

> Réponse 1 : POST, 201 Créé

__Question 2__ : GET /stations/999 demande une station inexistante. Quel code HTTP et quel type de réponse faut-il
renvoyer ?

> Réponse 2 : GET, 404 Non trouvé

__Question 3__ : Quelle est la différence entre les codes 401 et 403 ? Donnez un exemple de chaque cas.

> Réponse 3 : Le code 401 signifie "Non autorisé" et c'est utilisé lorsque l'utilisateur n'est pas authentifié. Le code 403 signifie "Accès refusé" et c'est utilisé lorsque l'utilisateur est authentifié mais n'a pas la permission d'accéder à la ressource. Exemple de 401 : tentative d'accès à une ressource protégée sans s'authentifier. Exemple de 403 : utilisateur authentifié mais sans droits d'accès à la ressource.

## Exercice 3 - Persistance

Test de redémarrage : j'ai créé la station `P1` via `POST /stations` (réponse 201, id 1), puis arrêté et relancé `uvicorn`. `GET /stations/1` renvoie toujours 200 avec `{"id":1,"code":"P1","name":"Persist","capacity":4,"status":"open"}`. Les données sont donc bien conservées dans le fichier SQLite après redémarrage.

## Exercice 4 - Tests

Deux exécutions successives de `python -m pytest -q` :

- 1re exécution : `8 passed` (succès)
- 2e exécution : `8 passed` (succès)

Les tests sont indépendants de l'ordre et de l'état de la base de l'application, car chaque test démarre avec une base SQLite en mémoire vide.

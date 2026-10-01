# Dock Control - Exam Python Ethan

## Installation

```bash
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## Lancer l'API

```bash
uvicorn app.main:app --reload
```

La base SQLite (`stations.db`) est créée automatiquement au lancement.
Documentation interactive : http://127.0.0.1:8000/docs

## Lancer les tests

```bash
python -m pytest -q
```

Les tests utilisent une base SQLite en mémoire, distincte de celle de l'application.

## Routes

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | `{"status": "ok"}` |
| POST | `/stations` | Crée une station (201, 409 si code existant, 422 si invalide) |
| GET | `/stations?status=open` | Liste, filtre optionnel |
| GET | `/stations/{id}` | Lecture (404 si inconnue) |
| PATCH | `/stations/{id}` | Modifie `name` et/ou `status` uniquement |

> PS : L'exercice 4 a été fait à l'IA car beaucoup trop dur, on n'a jamais vu ça.
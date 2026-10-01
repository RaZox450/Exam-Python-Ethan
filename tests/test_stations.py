import pytest


def make(code="ST01", name="Gare", capacity=10, status=None):
    data = {"code": code, "name": name, "capacity": capacity}
    if status is not None:
        data["status"] = status
    return data


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_create_then_read(client):
    r = client.post("/stations", json=make())
    assert r.status_code == 201
    created = r.json()
    assert created["status"] == "open"

    r = client.get(f"/stations/{created['id']}")
    assert r.status_code == 200
    assert r.json() == created
    assert r.json()["code"] == "ST01"
    assert r.json()["name"] == "Gare"
    assert r.json()["capacity"] == 10


def test_filter_by_status(client):
    client.post("/stations", json=make("A", "A", 5, "open"))
    client.post("/stations", json=make("B", "B", 5, "closed"))
    client.post("/stations", json=make("C", "C", 5, "maintenance"))
    client.post("/stations", json=make("D", "D", 5, "open"))

    r = client.get("/stations", params={"status": "open"})
    assert r.status_code == 200
    stations = r.json()
    assert {s["code"] for s in stations} == {"A", "D"}
    assert all(s["status"] == "open" for s in stations)


def test_patch_name_only(client):
    created = client.post("/stations", json=make("ST9", "Ancien", 7, "maintenance")).json()

    r = client.patch(f"/stations/{created['id']}", json={"name": "Nouveau"})
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "Nouveau"
    assert body["code"] == "ST9"
    assert body["capacity"] == 7
    assert body["status"] == "maintenance"

    assert client.get(f"/stations/{created['id']}").json()["name"] == "Nouveau"


def test_get_unknown_id(client):
    r = client.get("/stations/999")
    assert r.status_code == 404
    assert isinstance(r.json(), dict)
    assert "detail" in r.json()


@pytest.mark.parametrize(
    "payload",
    [
        make(capacity=0),
        make(status="flying"),
    ],
    ids=["capacity=0", "status=flying"],
)
def test_invalid_input_returns_422(client, payload):
    r = client.post("/stations", json=payload)
    assert r.status_code == 422
    assert client.get("/stations").json() == []


def test_duplicate_code_returns_409(client):
    assert client.post("/stations", json=make("DUP", "Une")).status_code == 201
    r = client.post("/stations", json=make("DUP", "Deux"))
    assert r.status_code == 409

    stations = client.get("/stations").json()
    assert len(stations) == 1
    assert stations[0]["name"] == "Une"

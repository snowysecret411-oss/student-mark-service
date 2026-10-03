from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Student Mark Service (SMS)"}


def test_create_student():
    response = client.post("/students", json={"id": 1, "name": "Alice", "maths": 90, "physics": 85, "chemistry": 80})
    assert response.status_code == 200
    assert response.json()["name"] == "Alice"


def test_get_all_students():
    response = client.get("/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student():
    client.post("/students", json={"id": 2, "name": "Bob", "maths": 70, "physics": 75, "chemistry": 65})
    response = client.get("/students/2")
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"


def test_get_student_not_found():
    response = client.get("/students/9999")
    assert response.status_code == 404


def test_update_student():
    client.post("/students", json={"id": 3, "name": "Carol", "maths": 60, "physics": 55, "chemistry": 50})
    response = client.put("/students/3", json={"id": 3, "name": "Carol", "maths": 95, "physics": 90, "chemistry": 88})
    assert response.status_code == 200
    assert response.json()["maths"] == 95


def test_update_student_not_found():
    response = client.put("/students/9999", json={"id": 9999, "name": "X", "maths": 50, "physics": 50, "chemistry": 50})
    assert response.status_code == 404


def test_delete_student():
    client.post("/students", json={"id": 4, "name": "Dave", "maths": 80, "physics": 80, "chemistry": 80})
    response = client.delete("/students/4")
    assert response.status_code == 200
    assert response.json()["student_id"] == 4


def test_delete_student_not_found():
    response = client.delete("/students/9999")
    assert response.status_code == 404


def test_create_duplicate_student():
    client.post("/students", json={"id": 5, "name": "Eve", "maths": 70, "physics": 70, "chemistry": 70})
    response = client.post("/students", json={"id": 5, "name": "Eve", "maths": 70, "physics": 70, "chemistry": 70})
    assert response.status_code == 400


def test_filter_students_by_name():
    client.post("/students", json={"id": 6, "name": "Frank", "maths": 88, "physics": 82, "chemistry": 79})
    response = client.get("/students?name=Frank")
    assert response.status_code == 200
    results = response.json()
    assert all(s["name"] == "Frank" for s in results)

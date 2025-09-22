from fastapi.testclient import TestClient
import sys
import os

# Ensure the source folder is in sys.path so Python can find main.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "source")))

from main import api  # import FastAPI instance

client = TestClient(api)


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Message": "Welcome to the Ticket Booking System"}


def test_add_ticket():
    ticket_data = {
        "id": 1,
        "flight_name": "AirTest",
        "flight_date": "2025-10-15",
        "flight_time": "14:30",
        "destination": "New York"
    }
    response = client.post("/ticket", json=ticket_data)
    assert response.status_code == 200
    assert response.json() == ticket_data


def test_get_tickets():
    response = client.get("/ticket")
    assert response.status_code == 200
    tickets = response.json()
    assert isinstance(tickets, list)
    assert len(tickets) > 0
    assert tickets[0]["flight_name"] == "AirTest"


def test_update_ticket():
    updated_ticket_data = {
        "id": 1,
        "flight_name": "AirTest Updated",
        "flight_date": "2025-10-16",
        "flight_time": "15:00",
        "destination": "Los Angeles"
    }
    response = client.put("/ticket/1", json=updated_ticket_data)
    assert response.status_code == 200
    assert response.json() == updated_ticket_data


def test_delete_ticket():
    response = client.delete("/ticket/1")
    assert response.status_code == 200
    deleted_ticket = response.json()
    assert deleted_ticket["id"] == 1

    # Check deletion actually worked
    response = client.get("/ticket")
    tickets = response.json()
    assert all(ticket["id"] != 1 for ticket in tickets)

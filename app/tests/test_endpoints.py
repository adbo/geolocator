# tests/test_endpoints.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from main import app
from core.exceptions import IPStackAPIError
from db.database import get_db
from unittest.mock import patch

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def override_get_db():
        yield session
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_db, None)

mock_ipstack_response = {
    "ip": "8.8.8.8",
    "type": "ipv4",
    "continent_code": "NA",
    "continent_name": "North America",
    "country_code": "US",
    "country_name": "United States",
    "region_code": "CA",
    "region_name": "California",
    "city": "Mountain View",
    "zip": "94035",
    "latitude": 37.386051177978516,
    "longitude": -122.08385467529297,
    "location": {"geoname_id": 5375481, "capital": "Washington D.C.", "languages": [{"code": "en", "name": "English", "native": "English"}]},
    "is_eu": False
}

def test_create_geolocation(client: TestClient):
    with patch("app.utils.ipstack_client.get_geolocation_data", return_value=mock_ipstack_response):
        response = client.post("/api/v1/geolocations", json={"ip_or_url": "8.8.8.8"})
        assert response.status_code == 201

def test_read_geolocation(client: TestClient):
    with patch("app.utils.ipstack_client.get_geolocation_data", return_value=mock_ipstack_response):
        client.post("/api/v1/geolocations", json={"ip_or_url": "8.8.8.8"})
    response = client.get("/api/v1/geolocations/8.8.8.8")
    assert response.status_code == 200

def test_read_geolocation_not_found(client: TestClient):
    response = client.get("/api/v1/geolocations/1.1.1.1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Geolocation for '1.1.1.1' not found"

def test_delete_geolocation(client: TestClient):
    with patch("app.utils.ipstack_client.get_geolocation_data", return_value=mock_ipstack_response):
        client.post("/api/v1/geolocations", json={"ip_or_url": "8.8.8.8"})
    response = client.delete("/api/v1/geolocations/8.8.8.8")
    assert response.status_code == 204

def test_delete_geolocation_not_found(client: TestClient):
    response = client.delete("/api/v1/geolocations/1.1.1.1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Geolocation for '1.1.1.1' not found"

def test_create_geolocation_existing(client: TestClient):
    with patch("app.utils.ipstack_client.get_geolocation_data", return_value=mock_ipstack_response):
        response_create = client.post("/api/v1/geolocations", json={"ip_or_url": "8.8.8.8"})
        assert response_create.status_code == 201

        response_second_create = client.post("/api/v1/geolocations", json={"ip_or_url": "8.8.8.8"})
        assert response_second_create.status_code == 200

def test_create_geolocation_invalid_input(client: TestClient):
    response = client.post("/api/v1/geolocations", json={"invalid_field": "value"})
    assert response.status_code == 422

def test_create_geolocation_ipstack_error(client: TestClient):
    with patch("core.crud.get_geolocation_data", side_effect=IPStackAPIError(detail="API Error")):
        response = client.post("/api/v1/geolocations", json={"ip_or_url": "9.9.9.9"})
        assert response.status_code == 503
        assert response.json()["detail"] == "503: API Error"
import pytest
import pytest_asyncio
from httpx import AsyncClient
from my_authentication_app.main import app
import uuid

@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio
async def test_register_user(client):
    unique_email = f"jane.smith+{uuid.uuid4()}@example.com"
    response = await client.post(
        "/auth/register",
        json={
            "firstName": "Jane",
            "lastName": "Smith",
            "email": unique_email,
            "password": "password123",
            "phone": "0987654321"
        }
    )
    assert response.status_code in [200, 201]
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["data"]["user"]["email"] == unique_email
    assert "access_token" in response_data["data"]

@pytest.mark.asyncio
async def test_login_user(client):
    unique_email = f"jane.smith+{uuid.uuid4()}@example.com"
    response = await client.post(
        "/auth/register",
        json={
            "firstName": "Jane",
            "lastName": "Smith",
            "email": unique_email,
            "password": "password123",
            "phone": "0987654321"
        }
    )
    assert response.status_code in [200, 201]

    response = await client.post(
        "/auth/login",
        data={
            "username": unique_email,
            "password": "password123"
        }
    )
    assert response.status_code == 200
    response_data = response.json()
    assert response_data["status"] == "success"
    assert response_data["user"]["email"] == unique_email
    assert "access_token" in response_data

@pytest.mark.asyncio
async def test_get_user(client):
    unique_email = f"jane.smith+{uuid.uuid4()}@example.com"
    register_response = await client.post(
        "/auth/register",
        json={
            "firstName": "Jane",
            "lastName": "Smith",
            "email": unique_email,
            "password": "password123",
            "phone": "0987654321"
        }
    )
    assert register_response.status_code in [200, 201]

    # Login to get the access token
    login_response = await client.post(
        "/auth/login",
        data={
            "username": unique_email,
            "password": "password123"
        }
    )
    assert login_response.status_code == 200
    access_token = login_response.json()["access_token"]

    user_id = register_response.json()["data"]["user"]["userId"]

    # Get the user with the access token
    response = await client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200
    user_data = response.json()
    assert user_data["status"] == "success"
    assert user_data["data"]["email"] == unique_email

@pytest.mark.asyncio
async def test_register_user_missing_fields(client):
    required_fields = ["firstName", "lastName", "email", "password"]
    for field in required_fields:
        user_data = {
            "firstName": "Jane",
            "lastName": "Smith",
            "email": f"jane.smith+{uuid.uuid4()}@example.com",
            "password": "password123",
            "phone": "0987654321"
        }
        del user_data[field]
        response = await client.post("/auth/register", json=user_data)
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_register_user_duplicate_email(client):
    unique_email = f"jane.smith+{uuid.uuid4()}@example.com"
    response = await client.post(
        "/auth/register",
        json={
            "firstName": "Jane",
            "lastName": "Smith",
            "email": unique_email,
            "password": "password123",
            "phone": "0987654321"
        }
    )
    assert response.status_code in [200, 201]

    response = await client.post(
        "/auth/register",
        json={
            "firstName": "Jane",
            "lastName": "Smith",
            "email": unique_email,
            "password": "password123",
            "phone": "0987654321"
        }
    )
    assert response.status_code == 400
    assert response.json()["detail"] == f"Email {unique_email} already registered."

import uuid


def test_login_demo_user(client):
    """Test successful JSON login with demo credentials."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "alex.morgan@ai-learning.io", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_id"] == "usr_98741"


def test_login_invalid_credentials(client):
    """Test login failure with invalid password."""
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "alex.morgan@ai-learning.io", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_register_new_user(client):
    """Test new user registration."""
    unique_email = f"test.learner_{uuid.uuid4().hex[:6]}@ai-learning.io"
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": unique_email,
            "password": "securepassword123",
            "full_name": "Test Learner",
            "learning_goal": "Machine Learning Engineer",
            "preferred_learning_style": "practical",
            "skill_level": "beginner",
        },
    )
    assert response.status_code in [200, 201]
    data = response.json()
    assert data["email"] == unique_email
    assert "user_id" in data


def test_authenticated_me_endpoint(client):
    """Test /me endpoint using JWT token."""
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "alex.morgan@ai-learning.io", "password": "password123"},
    )
    token = login_res.json()["access_token"]

    me_res = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert me_res.status_code == 200
    user_data = me_res.json()
    assert user_data["email"] == "alex.morgan@ai-learning.io"

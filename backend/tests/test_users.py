def test_get_user_profile(client):
    """Test user profile retrieval by ID."""
    response = client.get("/api/v1/users/usr_98741")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_98741"
    assert data["full_name"] == "Alex Morgan"


def test_update_learning_goal(client):
    """Test updating user target goal with auth token."""
    login_res = client.post(
        "/api/v1/auth/login",
        json={"email": "alex.morgan@ai-learning.io", "password": "password123"},
    )
    token = login_res.json()["access_token"]

    update_res = client.put(
        "/api/v1/users/usr_98741/goal",
        json={"learning_goal": "Lead RecSys Architect"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert update_res.status_code == 200
    data = update_res.json()
    assert data["learning_goal"] == "Lead RecSys Architect"

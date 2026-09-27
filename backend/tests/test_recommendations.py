def test_personalized_recommendations(client):
    """Test recommendation generation endpoint."""
    response = client.post(
        "/api/v1/recommendations/personalized",
        json={"user_id": "usr_98741", "limit": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "usr_98741"
    assert "recommendations" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["match_score"] > 0.5


def test_telemetry_event_tracking(client):
    """Test interaction event ingestion."""
    response = client.post(
        "/api/v1/recommendations/events/track",
        json={
            "user_id": "usr_98741",
            "event_type": "quiz_submitted",
            "lesson_id": "lsn_1",
            "payload": {"score": 0.85},
        },
    )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "ingested"

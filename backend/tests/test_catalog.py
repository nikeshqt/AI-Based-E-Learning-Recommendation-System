def test_list_courses(client):
    """Test retrieving course catalog listing."""
    response = client.get("/api/v1/catalog/courses")
    assert response.status_code == 200
    courses = response.json()
    assert len(courses) >= 3
    assert "course_id" in courses[0]


def test_get_course_detail(client):
    """Test fetching course details and lesson syllabus."""
    response = client.get("/api/v1/catalog/courses/crs_gnn_01")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Graph Neural Networks for Recommendation Systems"
    assert len(data["lessons"]) == 3

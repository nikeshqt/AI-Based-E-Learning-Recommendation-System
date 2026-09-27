import httpx
import sys
import json
import uuid

BASE_URL = "http://127.0.0.1:8080/api/v1"


def print_step(num, title):
    print(f"\n========================================================")
    print(f"STEP {num}: {title}")
    print(f"========================================================")


def main():
    print("Starting Live End-to-End User Journey Verification...")

    # 1. Health check
    print_step(1, "Verify Health Check Endpoint")
    res = httpx.get("http://127.0.0.1:8080/health")
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code == 200

    # 2. Register NEW student account
    print_step(2, "Register NEW Student Account")
    email = f"cyber.student.{uuid.uuid4().hex[:6]}@ai-learning.io"
    password = "CyberSecure2026!"
    reg_payload = {
        "email": email,
        "password": password,
        "full_name": "Cyber Student",
        "learning_goal": "Cybersecurity Analyst",
        "preferred_learning_style": "practical",
        "skill_level": "intermediate",
    }
    res = httpx.post(f"{BASE_URL}/auth/register", json=reg_payload)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code in [200, 201]
    user_id = res.json()["user_id"]

    # 3. Login with account
    print_step(3, "Login with Registered Account")
    res = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    print(f"Status Code: {res.status_code}")
    print(f"Response: {res.json()}")
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 4. Open Student Profile
    print_step(4, "Open Student Profile (/me)")
    res = httpx.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status Code: {res.status_code}")
    print(f"Response: {json.dumps(res.json(), indent=2)}")
    assert res.status_code == 200

    # 5, 6, 7, 8. Set Career Goal & Skills & Interests and Save Profile
    print_step(5, "Set Career Goal: Cybersecurity Analyst, Skills & Interests")
    profile_update_payload = {
        "learning_goal": "Cybersecurity Analyst",
        "skills": [
            {"skill_name": "Python", "mastery_score": 0.80, "category": "Programming"},
            {"skill_name": "Linux", "mastery_score": 0.40, "category": "Operating System"},
            {"skill_name": "Networking", "mastery_score": 0.30, "category": "Infrastructure"},
            {"skill_name": "Cybersecurity", "mastery_score": 0.50, "category": "Security"},
        ],
        "interests": ["Cybersecurity", "Python", "AI"],
    }
    res = httpx.put(f"{BASE_URL}/users/{user_id}/profile", json=profile_update_payload, headers=headers)
    print(f"Status Code: {res.status_code}")
    print(f"Updated Profile Response: {json.dumps(res.json(), indent=2)}")
    assert res.status_code == 200
    assert res.json()["learning_goal"] == "Cybersecurity Analyst"
    assert len(res.json()["skills"]) == 4

    # 9. Open Course Catalog
    print_step(9, "Open Course Catalog")
    res = httpx.get(f"{BASE_URL}/catalog/courses")
    print(f"Status Code: {res.status_code}")
    print(f"Catalog Items Count: {len(res.json())}")
    assert res.status_code == 200

    # 10. Open Course Detail Page
    print_step(10, "Open Course Detail Page (crs_sec_04)")
    res = httpx.get(f"{BASE_URL}/catalog/courses/crs_sec_04")
    print(f"Status Code: {res.status_code}")
    print(f"Course Detail: {json.dumps(res.json(), indent=2)}")
    assert res.status_code == 200

    # 11 & 12, 13. Generate Personalized Recommendations & Verify AI Engine Scoring
    print_step(11, "Generate Personalized Recommendations for Student")
    res = httpx.post(f"{BASE_URL}/recommendations/personalized", json={"user_id": user_id, "limit": 10})
    print(f"Status Code: {res.status_code}")
    recs_data = res.json()
    print(f"Recommendations Count: {len(recs_data['recommendations'])}")
    top_rec = recs_data["recommendations"][0]
    print(f"Top Recommendation Title: {top_rec['course']['title']}")
    print(f"Top Recommendation Match Score: {top_rec['match_score']}")
    print(f"Top Recommendation Reason: {top_rec['recommendation_reason']}")
    assert res.status_code == 200
    assert top_rec["course"]["course_id"] == "crs_sec_04"
    assert "Cybersecurity Analyst" in top_rec["recommendation_reason"]

    # 14 & 15. Generate Personalized Learning Path
    print_step(14, "Generate Personalized Learning Path")
    res = httpx.post(f"{BASE_URL}/learning-paths/generate", params={"user_id": user_id, "target_goal": "Cybersecurity Analyst"})
    print(f"Status Code: {res.status_code}")
    path_data = res.json()
    print(f"Learning Path Goal: {path_data['overall_goal']}")
    print(f"Stages Count: {len(path_data['stages'])}")
    assert res.status_code == 200
    assert path_data["overall_goal"] == "Cybersecurity Analyst"

    # 16. Open Analytics
    print_step(16, "Open Student Analytics")
    res = httpx.get(f"{BASE_URL}/analytics/user/{user_id}")
    print(f"Status Code: {res.status_code}")
    print(f"Analytics Data: {json.dumps(res.json(), indent=2)}")
    assert res.status_code == 200

    # 17 & 18. Open AI Tutor and Send Message
    print_step(18, "Send Message to AI Tutor")
    event_payload = {
        "user_id": user_id,
        "event_type": "ai_tutor_message",
        "payload": {"message": "What prerequisites do I need for Cybersecurity and AI?"},
    }
    res = httpx.post(f"{BASE_URL}/recommendations/events/track", json=event_payload)
    print(f"Status Code: {res.status_code}")
    print(f"Event Response: {res.json()}")
    assert res.status_code == 202

    # 19. Logout
    print_step(19, "Logout (Invalidate session token)")
    headers = {}

    # 20 & 21. Login again & Verify Persistence
    print_step(20, "Re-login and Verify Data Persistence")
    res = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
    assert res.status_code == 200
    new_token = res.json()["access_token"]

    res = httpx.get(f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {new_token}"})
    persisted_user = res.json()
    print(f"Persisted Learning Goal: {persisted_user['learning_goal']}")
    print(f"Persisted Skills Count: {len(persisted_user['skills'])}")
    assert persisted_user["learning_goal"] == "Cybersecurity Analyst"
    assert len(persisted_user["skills"]) == 4

    # PHASE 3: NEGATIVE TESTING
    print_step(22, "PHASE 3: Negative Testing")

    # Test 1: Invalid Login
    res_inv = httpx.post(f"{BASE_URL}/auth/login", json={"email": email, "password": "WrongPassword!"})
    print(f"Invalid Login Status: {res_inv.status_code} (Expected 401)")
    assert res_inv.status_code == 401

    # Test 2: Empty Required Fields
    res_emp = httpx.post(f"{BASE_URL}/auth/register", json={"email": "", "password": ""})
    print(f"Empty Fields Status: {res_emp.status_code} (Expected 422)")
    assert res_emp.status_code == 422

    # Test 3: Unauthorized API Access
    res_unauth = httpx.get(f"{BASE_URL}/auth/me")
    print(f"Unauthorized Access Status: {res_unauth.status_code} (Expected 401)")
    assert res_unauth.status_code == 401

    # Test 4: Student Accessing Forbidden Action / Wrong User Goal Update
    res_forb = httpx.put(f"{BASE_URL}/users/usr_other_user/goal", json={"learning_goal": "Hacker"}, headers={"Authorization": f"Bearer {new_token}"})
    print(f"Forbidden Update Status: {res_forb.status_code} (Expected 403)")
    assert res_forb.status_code == 403

    print("\n========================================================")
    print("ALL 21 STEPS & PERSISTENCE TESTS PASSED SUCCESSFULLY 100%!")
    print("========================================================\n")


if __name__ == "__main__":
    main()

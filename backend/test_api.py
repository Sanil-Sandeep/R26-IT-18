"""
test_api.py
============
Run this AFTER starting app.py to test all API endpoints.

How to use:
-----------
1. First run the server:    python backend/app.py
2. Open a NEW terminal
3. Run this test:           python backend/test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000/api"
STUDENT_ID = "test_student_1"

def print_result(test_name, response):
    """Prints test result in a readable format."""
    print(f"\n{'='*50}")
    print(f"TEST: {test_name}")
    print(f"Status: {response.status_code}")
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)[:300]}...")
        if response.status_code == 200:
            print("✅ PASSED")
        else:
            print("❌ FAILED")
    except:
        print(f"Raw: {response.text[:200]}")
        print("❌ FAILED")

def run_tests():
    print("\n" + "="*50)
    print("  ICT CHATBOT API TESTS")
    print("="*50)

    # Test 1: Health check
    r = requests.get(f"{BASE_URL}/health")
    print_result("Health Check", r)

    # Test 2: Basic chat - learning mode
    r = requests.post(f"{BASE_URL}/chat", json={
        "message": "explain what is a database",
        "student_id": STUDENT_ID,
        "emotion_state": "neutral"
    })
    print_result("Chat - Learning Mode", r)

    # Test 3: Chat - exam mode
    r = requests.post(f"{BASE_URL}/chat", json={
        "message": "define database 2 marks",
        "student_id": STUDENT_ID,
        "emotion_state": "neutral"
    })
    print_result("Chat - Exam Mode", r)

    # Test 4: Chat - confused emotion
    r = requests.post(f"{BASE_URL}/chat", json={
        "message": "what is ICT",
        "student_id": STUDENT_ID,
        "emotion_state": "confused"
    })
    print_result("Chat - Confused Emotion", r)

    # Test 5: Micro challenge
    r = requests.post(f"{BASE_URL}/chat/challenge", json={
        "student_id": STUDENT_ID,
        "topic": "Chapter 1"
    })
    print_result("Micro Challenge Request", r)

    # Test 6: Login quiz
    r = requests.get(f"{BASE_URL}/quiz/login?student_id={STUDENT_ID}")
    print_result("Login Quiz", r)

    # Test 7: Get topics
    r = requests.get(f"{BASE_URL}/topics")
    print_result("Get Topics", r)

    # Test 8: Student progress
    r = requests.get(f"{BASE_URL}/student/progress?student_id={STUDENT_ID}")
    print_result("Student Progress", r)

    # Test 9: Teacher alerts
    r = requests.get(f"{BASE_URL}/teacher/alerts")
    print_result("Teacher Alerts", r)

    # Test 10: Repeated query alert (ask same thing 3 times)
    print(f"\n{'='*50}")
    print("TEST: Repeated Query Detection")
    for i in range(3):
        r = requests.post(f"{BASE_URL}/chat", json={
            "message": "what is normalization",
            "student_id": STUDENT_ID
        })
        data = r.json()
        if data.get('teacher_alert'):
            print(f"✅ Teacher alert triggered on attempt {i+1}!")
            print(f"   Alert: {data.get('alert_message')}")
            break

    print(f"\n{'='*50}")
    print("All tests complete!")
    print("="*50)

if __name__ == "__main__":
    try:
        run_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to server!")
        print("Make sure the server is running first:")
        print("  python backend/app.py")
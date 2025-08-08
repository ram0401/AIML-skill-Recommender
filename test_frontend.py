#!/usr/bin/env python3
"""
Test script to verify the frontend integration with the backend
"""

import requests
import json
import os

def test_backend_endpoints():
    """Test the backend endpoints that the frontend uses"""
    base_url = "http://localhost:8000"
    
    print("Testing backend endpoints...")
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {e}")
    
    # Test 2: Get job roles
    try:
        response = requests.get(f"{base_url}/job-roles")
        if response.status_code == 200:
            job_roles = response.json()
            print(f"✅ Job roles endpoint passed - found {len(job_roles)} roles")
            for role in job_roles[:3]:  # Show first 3 roles
                print(f"   - {role['title']} ({role['id']})")
        else:
            print(f"❌ Job roles failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Job roles error: {e}")
    
    # Test 3: Test skill matching
    try:
        test_skills = ["python", "javascript", "react"]
        test_role = "software_engineer"
        
        data = {
            "user_skills": test_skills,
            "target_role": test_role
        }
        
        response = requests.post(f"{base_url}/match-skills", data=data)
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Skill matching passed - {result['overall_match_percentage']}% match")
        else:
            print(f"❌ Skill matching failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Skill matching error: {e}")
    
    # Test 4: Test roadmap generation
    try:
        data = {"skill": "python"}
        response = requests.post(f"{base_url}/generate-roadmap", data=data)
        if response.status_code == 200:
            roadmap = response.json()
            print(f"✅ Roadmap generation passed - {roadmap.get('skill', 'Unknown')} roadmap")
        else:
            print(f"❌ Roadmap generation failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Roadmap generation error: {e}")

def test_frontend_files():
    """Test if frontend files exist"""
    print("\nTesting frontend files...")
    
    frontend_files = [
        "frontend/index.html",
        "frontend/styles.css", 
        "frontend/script.js"
    ]
    
    for file_path in frontend_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")

def test_static_serving():
    """Test if static files are being served"""
    print("\nTesting static file serving...")
    
    base_url = "http://localhost:8000"
    
    # Test CSS file
    try:
        response = requests.get(f"{base_url}/static/styles.css")
        if response.status_code == 200:
            print("✅ CSS file is being served")
        else:
            print(f"❌ CSS file not served: {response.status_code}")
    except Exception as e:
        print(f"❌ CSS file error: {e}")
    
    # Test JS file
    try:
        response = requests.get(f"{base_url}/static/script.js")
        if response.status_code == 200:
            print("✅ JS file is being served")
        else:
            print(f"❌ JS file not served: {response.status_code}")
    except Exception as e:
        print(f"❌ JS file error: {e}")

if __name__ == "__main__":
    print("🚀 Testing AI/ML Skill Recommender Frontend Integration")
    print("=" * 60)
    
    test_frontend_files()
    test_backend_endpoints()
    test_static_serving()
    
    print("\n" + "=" * 60)
    print("🎉 Testing complete!")
    print("\nTo start the application:")
    print("1. Make sure the backend is running: python main.py")
    print("2. Open your browser and go to: http://localhost:8000")
    print("3. Enjoy the beautiful frontend interface!")

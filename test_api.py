#!/usr/bin/env python3
"""
Test script for the Skill Recommender API
"""

import requests
import json
import os

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    if response.status_code == 200:
        print("✅ Health check passed")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Health check failed: {response.status_code}")
    print()

def test_get_job_roles():
    """Test getting available job roles"""
    print("Testing get job roles...")
    response = requests.get(f"{BASE_URL}/job-roles")
    if response.status_code == 200:
        print("✅ Get job roles passed")
        roles = response.json()
        print(f"Found {len(roles)} job roles:")
        for role in roles[:3]:  # Show first 3 roles
            print(f"  - {role['title']}: {role['description']}")
    else:
        print(f"❌ Get job roles failed: {response.status_code}")
    print()

def test_skill_matching():
    """Test skill matching functionality"""
    print("Testing skill matching...")
    
    # Test data
    user_skills = ["python", "javascript", "react", "git"]
    target_role = "software_engineer"
    
    data = {
        "user_skills": user_skills,
        "target_role": target_role
    }
    
    response = requests.post(f"{BASE_URL}/match-skills", data=data)
    if response.status_code == 200:
        print("✅ Skill matching passed")
        result = response.json()
        print(f"Target role: {result['target_role']}")
        print(f"Overall match percentage: {result['overall_match_percentage']}%")
        print(f"Matched skills: {result['matched_skills']}")
        print(f"Missing skills: {result['missing_skills']}")
    else:
        print(f"❌ Skill matching failed: {response.status_code}")
        print(f"Response: {response.text}")
    print()

def test_roadmap_generation():
    """Test roadmap generation"""
    print("Testing roadmap generation...")
    
    skill = "python"
    data = {"skill": skill}
    
    response = requests.post(f"{BASE_URL}/generate-roadmap", data=data)
    if response.status_code == 200:
        print("✅ Roadmap generation passed")
        roadmap = response.json()
        print(f"Skill: {roadmap['skill']}")
        print(f"Title: {roadmap['title']}")
        print(f"Description: {roadmap['description']}")
        print(f"Total duration: {roadmap['estimated_total_duration']}")
        print(f"Number of levels: {len(roadmap['levels'])}")
        print(f"Number of resources: {len(roadmap['resources'])}")
    else:
        print(f"❌ Roadmap generation failed: {response.status_code}")
        print(f"Response: {response.text}")
    print()

def test_resume_upload():
    """Test resume upload (requires a test file)"""
    print("Testing resume upload...")
    
    # Check if test resume file exists
    test_files = ["test_resume.txt", "test_resume.pdf", "test_resume.docx"]
    test_file = None
    
    for file in test_files:
        if os.path.exists(file):
            test_file = file
            break
    
    if test_file:
        with open(test_file, 'rb') as f:
            files = {'file': (test_file, f, 'application/octet-stream')}
            response = requests.post(f"{BASE_URL}/upload-resume", files=files)
        
        if response.status_code == 200:
            print("✅ Resume upload passed")
            result = response.json()
            print(f"Filename: {result['filename']}")
            print(f"Extracted skills: {result['extracted_skills']}")
            print(f"Text length: {result['text_length']}")
        else:
            print(f"❌ Resume upload failed: {response.status_code}")
            print(f"Response: {response.text}")
    else:
        print("⚠️  No test resume file found. Skipping resume upload test.")
        print("   Create a test_resume.txt, test_resume.pdf, or test_resume.docx file to test this feature.")
    print()

def create_test_resume():
    """Create a test resume file for testing"""
    test_resume_content = """
    John Doe
    Software Engineer
    
    EXPERIENCE
    Senior Software Engineer at TechCorp (2020-2023)
    - Developed web applications using Python, JavaScript, and React
    - Implemented REST APIs and microservices architecture
    - Used Git for version control and Docker for containerization
    - Worked with SQL databases and MongoDB
    - Applied agile methodologies and CI/CD practices
    
    SKILLS
    Programming Languages: Python, JavaScript, Java, SQL
    Frameworks: React, Node.js, Django, Flask
    Tools: Git, Docker, AWS, Jenkins
    Databases: MySQL, PostgreSQL, MongoDB
    Methodologies: Agile, Scrum, DevOps
    """
    
    with open("test_resume.txt", "w") as f:
        f.write(test_resume_content)
    print("✅ Created test_resume.txt")

def main():
    """Run all tests"""
    print("🚀 Starting Skill Recommender API Tests")
    print("=" * 50)
    
    # Create test resume if it doesn't exist
    if not os.path.exists("test_resume.txt"):
        create_test_resume()
    
    # Run tests
    test_health_check()
    test_get_job_roles()
    test_skill_matching()
    test_roadmap_generation()
    test_resume_upload()
    
    print("🎉 All tests completed!")
    print("\nTo run the API server:")
    print("  uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    print("\nTo view API documentation:")
    print("  http://localhost:8000/docs")

if __name__ == "__main__":
    main()


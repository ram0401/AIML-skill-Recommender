import json
import os
from typing import List, Dict, Any
from difflib import SequenceMatcher

class SkillMatcher:
    def __init__(self):
        """Initialize the skill matcher with job role data"""
        self.job_roles = self._load_job_roles()
    
    def _load_job_roles(self) -> Dict[str, Any]:
        """Load job roles and their required skills from JSON file"""
        default_roles = {
            "software_engineer": {
                "title": "Software Engineer",
                "description": "Develops software applications and systems",
                "required_skills": [
                    "python", "java", "javascript", "git", "sql", "algorithms", 
                    "data structures", "object-oriented programming", "testing",
                    "agile", "scrum", "rest api", "microservices"
                ],
                "preferred_skills": [
                    "docker", "kubernetes", "aws", "react", "node.js", "spring",
                    "machine learning", "devops", "ci/cd"
                ]
            },
            "data_scientist": {
                "title": "Data Scientist",
                "description": "Analyzes data and builds machine learning models",
                "required_skills": [
                    "python", "sql", "statistics", "machine learning", "data analysis",
                    "pandas", "numpy", "matplotlib", "scikit-learn", "jupyter"
                ],
                "preferred_skills": [
                    "deep learning", "tensorflow", "pytorch", "spark", "hadoop",
                    "nlp", "computer vision", "r", "tableau", "power bi"
                ]
            },
            "frontend_developer": {
                "title": "Frontend Developer",
                "description": "Builds user interfaces and web applications",
                "required_skills": [
                    "html", "css", "javascript", "react", "git", "responsive design",
                    "webpack", "eslint", "bootstrap", "jquery"
                ],
                "preferred_skills": [
                    "typescript", "angular", "vue", "next.js", "tailwind", "sass",
                    "redux", "graphql", "pwa", "accessibility"
                ]
            },
            "backend_developer": {
                "title": "Backend Developer",
                "description": "Develops server-side applications and APIs",
                "required_skills": [
                    "python", "java", "sql", "rest api", "git", "algorithms",
                    "data structures", "object-oriented programming", "testing"
                ],
                "preferred_skills": [
                    "node.js", "spring", "django", "flask", "fastapi", "mongodb",
                    "redis", "docker", "kubernetes", "microservices"
                ]
            },
            "devops_engineer": {
                "title": "DevOps Engineer",
                "description": "Manages infrastructure and deployment pipelines",
                "required_skills": [
                    "linux", "git", "docker", "kubernetes", "aws", "ci/cd",
                    "jenkins", "terraform", "ansible", "nginx"
                ],
                "preferred_skills": [
                    "azure", "gcp", "prometheus", "grafana", "elasticsearch",
                    "kafka", "rabbitmq", "vault", "consul"
                ]
            },
            "machine_learning_engineer": {
                "title": "Machine Learning Engineer",
                "description": "Builds and deploys machine learning models",
                "required_skills": [
                    "python", "machine learning", "deep learning", "tensorflow",
                    "pytorch", "scikit-learn", "sql", "git", "docker"
                ],
                "preferred_skills": [
                    "kubernetes", "aws", "mlflow", "kubeflow", "spark", "hadoop",
                    "nlp", "computer vision", "mlops", "feature engineering"
                ]
            },
            "full_stack_developer": {
                "title": "Full Stack Developer",
                "description": "Develops both frontend and backend applications",
                "required_skills": [
                    "html", "css", "javascript", "python", "sql", "git",
                    "react", "node.js", "rest api", "algorithms"
                ],
                "preferred_skills": [
                    "typescript", "angular", "vue", "django", "flask", "mongodb",
                    "docker", "aws", "microservices", "graphql"
                ]
            },
            "data_engineer": {
                "title": "Data Engineer",
                "description": "Builds data pipelines and infrastructure",
                "required_skills": [
                    "python", "sql", "spark", "hadoop", "kafka", "airflow",
                    "docker", "kubernetes", "aws", "git"
                ],
                "preferred_skills": [
                    "snowflake", "databricks", "dbt", "presto", "hive",
                    "elasticsearch", "redis", "mlflow", "kubeflow"
                ]
            }
        }
        
        try:
            if os.path.exists('job_roles.json'):
                with open('job_roles.json', 'r') as f:
                    return json.load(f)
            else:
                return default_roles
        except Exception:
            return default_roles
    
    def get_available_job_roles(self) -> List[Dict[str, str]]:
        """Get list of available job roles"""
        roles = []
        for role_id, role_data in self.job_roles.items():
            roles.append({
                "id": role_id,
                "title": role_data["title"],
                "description": role_data["description"]
            })
        return roles
    
    def match_skills(self, user_skills: List[str], target_role: str) -> Dict[str, Any]:
        """
        Match user skills against target job role requirements
        """
        if target_role not in self.job_roles:
            raise ValueError(f"Unknown job role: {target_role}")
        
        role_data = self.job_roles[target_role]
        required_skills = set(role_data["required_skills"])
        preferred_skills = set(role_data["preferred_skills"])
        
        # Normalize user skills
        user_skills_normalized = [skill.lower().strip() for skill in user_skills]
        user_skills_set = set(user_skills_normalized)
        
        # Find matched skills
        matched_required = user_skills_set.intersection(required_skills)
        matched_preferred = user_skills_set.intersection(preferred_skills)
        
        # Find missing skills
        missing_required = required_skills - user_skills_set
        missing_preferred = preferred_skills - user_skills_set
        
        # Calculate match percentage
        total_required = len(required_skills)
        total_preferred = len(preferred_skills)
        
        required_match_percentage = (len(matched_required) / total_required) * 100 if total_required > 0 else 0
        preferred_match_percentage = (len(matched_preferred) / total_preferred) * 100 if total_preferred > 0 else 0
        
        # Overall match percentage (weighted: 70% required, 30% preferred)
        overall_match_percentage = (required_match_percentage * 0.7) + (preferred_match_percentage * 0.3)
        
        # Create skill gaps with descriptions
        skill_gaps = []
        
        for skill in missing_required:
            skill_gaps.append({
                "skill": skill,
                "type": "required",
                "priority": "high",
                "description": f"Required skill for {role_data['title']} position"
            })
        
        for skill in missing_preferred:
            skill_gaps.append({
                "skill": skill,
                "type": "preferred",
                "priority": "medium",
                "description": f"Preferred skill for {role_data['title']} position"
            })
        
        return {
            "target_role": role_data["title"],
            "role_description": role_data["description"],
            "matched_skills": {
                "required": list(matched_required),
                "preferred": list(matched_preferred)
            },
            "missing_skills": {
                "required": list(missing_required),
                "preferred": list(missing_preferred)
            },
            "skill_gaps": skill_gaps,
            "match_percentages": {
                "required": round(required_match_percentage, 2),
                "preferred": round(preferred_match_percentage, 2),
                "overall": round(overall_match_percentage, 2)
            },
            "overall_match_percentage": round(overall_match_percentage, 2)
        }
    
    def get_skill_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skills"""
        return SequenceMatcher(None, skill1.lower(), skill2.lower()).ratio()
    
    def find_similar_skills(self, skill: str, skill_list: List[str], threshold: float = 0.8) -> List[str]:
        """Find skills similar to the given skill"""
        similar_skills = []
        for s in skill_list:
            similarity = self.get_skill_similarity(skill, s)
            if similarity >= threshold:
                similar_skills.append(s)
        return similar_skills


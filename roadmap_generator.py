import json
import os
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup

class RoadmapGenerator:
    def __init__(self):
        """Initialize the roadmap generator with skill roadmaps data"""
        self.roadmaps = self._load_roadmaps()
        self.resources = self._load_resources()
    
    def _load_roadmaps(self) -> Dict[str, Any]:
        """Load skill roadmaps from JSON file or return default roadmaps"""
        default_roadmaps = {
            "python": {
                "title": "Python Programming",
                "description": "Learn Python programming from beginner to advanced",
                "levels": {
                    "beginner": {
                        "topics": [
                            "Python basics and syntax",
                            "Variables and data types",
                            "Control structures (if/else, loops)",
                            "Functions and modules",
                            "File handling",
                            "Error handling"
                        ],
                        "duration": "4-6 weeks",
                        "difficulty": "Beginner"
                    },
                    "intermediate": {
                        "topics": [
                            "Object-oriented programming",
                            "Decorators and generators",
                            "List comprehensions",
                            "Regular expressions",
                            "Working with APIs",
                            "Database connectivity"
                        ],
                        "duration": "6-8 weeks",
                        "difficulty": "Intermediate"
                    },
                    "advanced": {
                        "topics": [
                            "Advanced OOP concepts",
                            "Metaclasses and descriptors",
                            "Concurrency and threading",
                            "Async programming",
                            "Design patterns",
                            "Performance optimization"
                        ],
                        "duration": "8-10 weeks",
                        "difficulty": "Advanced"
                    }
                }
            },
            "machine learning": {
                "title": "Machine Learning",
                "description": "Master machine learning algorithms and techniques",
                "levels": {
                    "beginner": {
                        "topics": [
                            "Mathematics fundamentals (linear algebra, calculus)",
                            "Statistics and probability",
                            "Python for data science",
                            "Data preprocessing and cleaning",
                            "Supervised learning basics",
                            "Model evaluation metrics"
                        ],
                        "duration": "8-10 weeks",
                        "difficulty": "Beginner"
                    },
                    "intermediate": {
                        "topics": [
                            "Linear and logistic regression",
                            "Decision trees and random forests",
                            "Support vector machines",
                            "Clustering algorithms",
                            "Feature engineering",
                            "Cross-validation techniques"
                        ],
                        "duration": "10-12 weeks",
                        "difficulty": "Intermediate"
                    },
                    "advanced": {
                        "topics": [
                            "Neural networks and deep learning",
                            "Natural language processing",
                            "Computer vision",
                            "Reinforcement learning",
                            "Model deployment",
                            "MLOps and production"
                        ],
                        "duration": "12-16 weeks",
                        "difficulty": "Advanced"
                    }
                }
            },
            "javascript": {
                "title": "JavaScript Programming",
                "description": "Learn JavaScript for web development",
                "levels": {
                    "beginner": {
                        "topics": [
                            "JavaScript basics and syntax",
                            "Variables and data types",
                            "Functions and scope",
                            "Arrays and objects",
                            "DOM manipulation",
                            "Events and event handling"
                        ],
                        "duration": "4-6 weeks",
                        "difficulty": "Beginner"
                    },
                    "intermediate": {
                        "topics": [
                            "ES6+ features",
                            "Promises and async/await",
                            "Modules and bundlers",
                            "Testing with Jest",
                            "API integration",
                            "Local storage and cookies"
                        ],
                        "duration": "6-8 weeks",
                        "difficulty": "Intermediate"
                    },
                    "advanced": {
                        "topics": [
                            "Advanced JavaScript patterns",
                            "Functional programming",
                            "Design patterns",
                            "Performance optimization",
                            "Security best practices",
                            "Advanced debugging"
                        ],
                        "duration": "8-10 weeks",
                        "difficulty": "Advanced"
                    }
                }
            },
            "react": {
                "title": "React Development",
                "description": "Master React for building modern web applications",
                "levels": {
                    "beginner": {
                        "topics": [
                            "React fundamentals",
                            "Components and props",
                            "State and lifecycle",
                            "Event handling",
                            "Conditional rendering",
                            "Lists and keys"
                        ],
                        "duration": "4-6 weeks",
                        "difficulty": "Beginner"
                    },
                    "intermediate": {
                        "topics": [
                            "Hooks (useState, useEffect)",
                            "Context API",
                            "React Router",
                            "Forms and validation",
                            "API integration",
                            "Testing with React Testing Library"
                        ],
                        "duration": "6-8 weeks",
                        "difficulty": "Intermediate"
                    },
                    "advanced": {
                        "topics": [
                            "Advanced hooks",
                            "Performance optimization",
                            "State management (Redux, Zustand)",
                            "Server-side rendering",
                            "TypeScript with React",
                            "Advanced patterns"
                        ],
                        "duration": "8-10 weeks",
                        "difficulty": "Advanced"
                    }
                }
            },
            "docker": {
                "title": "Docker and Containerization",
                "description": "Learn Docker for containerization and deployment",
                "levels": {
                    "beginner": {
                        "topics": [
                            "Container basics",
                            "Docker installation",
                            "Docker images and containers",
                            "Dockerfile basics",
                            "Docker commands",
                            "Docker Hub"
                        ],
                        "duration": "3-4 weeks",
                        "difficulty": "Beginner"
                    },
                    "intermediate": {
                        "topics": [
                            "Multi-stage builds",
                            "Docker Compose",
                            "Networking in Docker",
                            "Volumes and data persistence",
                            "Docker security",
                            "Best practices"
                        ],
                        "duration": "4-6 weeks",
                        "difficulty": "Intermediate"
                    },
                    "advanced": {
                        "topics": [
                            "Docker Swarm",
                            "Kubernetes integration",
                            "CI/CD with Docker",
                            "Monitoring and logging",
                            "Advanced networking",
                            "Production deployment"
                        ],
                        "duration": "6-8 weeks",
                        "difficulty": "Advanced"
                    }
                }
            }
        }
        
        try:
            if os.path.exists('skill_roadmaps.json'):
                with open('skill_roadmaps.json', 'r') as f:
                    return json.load(f)
            else:
                return default_roadmaps
        except Exception:
            return default_roadmaps
    
    def _load_resources(self) -> Dict[str, List[Dict[str, str]]]:
        """Load learning resources from JSON file or return default resources"""
        default_resources = {
            "python": [
                {
                    "title": "Python for Everybody",
                    "type": "coursera",
                    "url": "https://www.coursera.org/specializations/python",
                    "description": "Comprehensive Python course for beginners",
                    "duration": "4 months",
                    "rating": "4.8"
                },
                {
                    "title": "Complete Python Bootcamp",
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=WGJJIrtnfpk",
                    "description": "Complete Python tutorial for beginners",
                    "duration": "6 hours",
                    "rating": "4.7"
                },
                {
                    "title": "Advanced Python Programming",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/python-programming",
                    "description": "Advanced Python concepts and techniques",
                    "duration": "8 weeks",
                    "rating": "4.6"
                }
            ],
            "machine learning": [
                {
                    "title": "Machine Learning by Andrew Ng",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/machine-learning",
                    "description": "Foundational machine learning course",
                    "duration": "11 weeks",
                    "rating": "4.9"
                },
                {
                    "title": "Machine Learning Full Course",
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=KNAWp2S3w94",
                    "description": "Complete machine learning tutorial",
                    "duration": "12 hours",
                    "rating": "4.8"
                },
                {
                    "title": "Deep Learning Specialization",
                    "type": "coursera",
                    "url": "https://www.coursera.org/specializations/deep-learning",
                    "description": "Advanced deep learning course",
                    "duration": "5 months",
                    "rating": "4.8"
                }
            ],
            "javascript": [
                {
                    "title": "JavaScript Algorithms and Data Structures",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/javascript-algorithms-data-structures",
                    "description": "JavaScript fundamentals and algorithms",
                    "duration": "6 weeks",
                    "rating": "4.7"
                },
                {
                    "title": "JavaScript Full Course",
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=W6NZfCO5SIk",
                    "description": "Complete JavaScript tutorial",
                    "duration": "3 hours",
                    "rating": "4.8"
                },
                {
                    "title": "Modern JavaScript",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/modern-javascript",
                    "description": "Modern JavaScript features and ES6+",
                    "duration": "4 weeks",
                    "rating": "4.6"
                }
            ],
            "react": [
                {
                    "title": "React Development",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/react-development",
                    "description": "React fundamentals and best practices",
                    "duration": "6 weeks",
                    "rating": "4.7"
                },
                {
                    "title": "React Full Course",
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=bMknfKXIFA8",
                    "description": "Complete React tutorial",
                    "duration": "8 hours",
                    "rating": "4.8"
                },
                {
                    "title": "Advanced React",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/advanced-react",
                    "description": "Advanced React patterns and optimization",
                    "duration": "8 weeks",
                    "rating": "4.6"
                }
            ],
            "docker": [
                {
                    "title": "Docker for Beginners",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/docker-basics",
                    "description": "Docker fundamentals and containerization",
                    "duration": "4 weeks",
                    "rating": "4.7"
                },
                {
                    "title": "Docker Tutorial for Beginners",
                    "type": "youtube",
                    "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
                    "description": "Complete Docker tutorial",
                    "duration": "2 hours",
                    "rating": "4.8"
                },
                {
                    "title": "Docker and Kubernetes",
                    "type": "coursera",
                    "url": "https://www.coursera.org/learn/docker-kubernetes",
                    "description": "Docker and Kubernetes integration",
                    "duration": "6 weeks",
                    "rating": "4.6"
                }
            ]
        }
        
        try:
            if os.path.exists('learning_resources.json'):
                with open('learning_resources.json', 'r') as f:
                    return json.load(f)
            else:
                return default_resources
        except Exception:
            return default_resources
    
    def generate_roadmap(self, skill: str) -> Dict[str, Any]:
        """
        Generate a learning roadmap for a specific skill
        """
        skill_lower = skill.lower().strip()
        
        # Check if roadmap exists for the skill
        if skill_lower not in self.roadmaps:
            # Try to find similar skills
            similar_skills = self._find_similar_skill(skill_lower)
            if similar_skills:
                skill_lower = similar_skills[0]
            else:
                # Generate a generic roadmap
                return self._generate_generic_roadmap(skill)
        
        roadmap_data = self.roadmaps[skill_lower]
        resources = self.resources.get(skill_lower, [])
        
        # Structure the roadmap
        roadmap = {
            "skill": skill,
            "title": roadmap_data["title"],
            "description": roadmap_data["description"],
            "levels": [],
            "resources": resources,
            "estimated_total_duration": self._calculate_total_duration(roadmap_data["levels"]),
            "difficulty_progression": ["beginner", "intermediate", "advanced"]
        }
        
        # Add levels with topics
        for level, level_data in roadmap_data["levels"].items():
            roadmap["levels"].append({
                "level": level,
                "difficulty": level_data["difficulty"],
                "duration": level_data["duration"],
                "topics": level_data["topics"],
                "learning_objectives": self._generate_learning_objectives(level_data["topics"])
            })
        
        return roadmap
    
    def _find_similar_skill(self, skill: str) -> List[str]:
        """Find similar skills in the available roadmaps"""
        similar_skills = []
        for available_skill in self.roadmaps.keys():
            if skill in available_skill or available_skill in skill:
                similar_skills.append(available_skill)
        return similar_skills
    
    def _generate_generic_roadmap(self, skill: str) -> Dict[str, Any]:
        """Generate a generic roadmap for unknown skills"""
        return {
            "skill": skill,
            "title": f"{skill.title()} Learning Path",
            "description": f"Comprehensive learning path for {skill}",
            "levels": [
                {
                    "level": "beginner",
                    "difficulty": "Beginner",
                    "duration": "4-6 weeks",
                    "topics": [
                        f"Introduction to {skill}",
                        f"Basic concepts and fundamentals",
                        "Getting started and setup",
                        "Core features and functionality",
                        "Basic projects and exercises"
                    ],
                    "learning_objectives": [
                        f"Understand basic {skill} concepts",
                        "Set up development environment",
                        "Complete basic projects"
                    ]
                },
                {
                    "level": "intermediate",
                    "difficulty": "Intermediate",
                    "duration": "6-8 weeks",
                    "topics": [
                        f"Advanced {skill} concepts",
                        "Best practices and patterns",
                        "Integration with other technologies",
                        "Performance optimization",
                        "Real-world applications"
                    ],
                    "learning_objectives": [
                        f"Master intermediate {skill} concepts",
                        "Apply best practices",
                        "Build real-world projects"
                    ]
                },
                {
                    "level": "advanced",
                    "difficulty": "Advanced",
                    "duration": "8-10 weeks",
                    "topics": [
                        f"Expert-level {skill} techniques",
                        "Advanced patterns and architectures",
                        "Performance and scalability",
                        "Security considerations",
                        "Industry best practices"
                    ],
                    "learning_objectives": [
                        f"Achieve expert-level {skill} proficiency",
                        "Design scalable solutions",
                        "Contribute to open source"
                    ]
                }
            ],
            "resources": [
                {
                    "title": f"Learn {skill} - Official Documentation",
                    "type": "documentation",
                    "url": f"https://docs.{skill.lower()}.org",
                    "description": f"Official {skill} documentation and tutorials",
                    "duration": "Self-paced",
                    "rating": "4.5"
                }
            ],
            "estimated_total_duration": "18-24 weeks",
            "difficulty_progression": ["beginner", "intermediate", "advanced"]
        }
    
    def _calculate_total_duration(self, levels: Dict[str, Any]) -> str:
        """Calculate total duration for all levels"""
        total_weeks = 0
        for level_data in levels.values():
            duration = level_data["duration"]
            # Extract weeks from duration string (e.g., "4-6 weeks" -> 5)
            if "weeks" in duration:
                parts = duration.split("-")
                if len(parts) == 2:
                    start, end = int(parts[0]), int(parts[1].split()[0])
                    total_weeks += (start + end) // 2
                else:
                    total_weeks += int(parts[0].split()[0])
        
        if total_weeks <= 12:
            return f"{total_weeks} weeks"
        else:
            months = total_weeks // 4
            return f"{months} months"
    
    def _generate_learning_objectives(self, topics: List[str]) -> List[str]:
        """Generate learning objectives from topics"""
        objectives = []
        for topic in topics:
            objective = f"Master {topic.lower()}"
            objectives.append(objective)
        return objectives
    
    def get_skill_resources(self, skill: str) -> List[Dict[str, str]]:
        """Get learning resources for a specific skill"""
        skill_lower = skill.lower().strip()
        return self.resources.get(skill_lower, [])
    
    def search_resources(self, query: str) -> List[Dict[str, str]]:
        """Search for learning resources based on query"""
        results = []
        query_lower = query.lower()
        
        for skill, resources in self.resources.items():
            if query_lower in skill:
                results.extend(resources)
            else:
                for resource in resources:
                    if (query_lower in resource["title"].lower() or 
                        query_lower in resource["description"].lower()):
                        results.append(resource)
        
        return results[:10]  # Limit to 10 results



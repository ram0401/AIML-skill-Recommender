import spacy
import re
from typing import List, Set
import json
import os

class SkillExtractor:
    def __init__(self):
        """Initialize the skill extractor with SpaCy model and skill keywords"""
        try:
            # Load SpaCy model (you may need to download it first: python -m spacy download en_core_web_sm)
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model not found, we'll use a fallback approach
            self.nlp = None
            print("Warning: SpaCy model not found. Using keyword-based extraction only.")
        
        # Common technical skills and programming languages
        self.technical_skills = {
            # Programming Languages
            'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'php', 'ruby', 'go', 'rust',
            'swift', 'kotlin', 'scala', 'r', 'matlab', 'perl', 'bash', 'powershell', 'sql',
            
            # Frameworks and Libraries
            'react', 'angular', 'vue', 'node.js', 'django', 'flask', 'spring', 'express', 'fastapi',
            'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
            'bootstrap', 'tailwind', 'jquery', 'lodash', 'axios', 'redux', 'vuex', 'next.js',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'sqlite', 'oracle', 'sql server',
            
            # Cloud and DevOps
            'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'git', 'github', 'gitlab',
            'terraform', 'ansible', 'nginx', 'apache', 'linux', 'ubuntu', 'centos',
            
            # Tools and Platforms
            'jira', 'confluence', 'slack', 'teams', 'zoom', 'figma', 'adobe', 'photoshop',
            'illustrator', 'sketch', 'invision', 'zeplin', 'postman', 'swagger', 'graphql',
            
            # Methodologies
            'agile', 'scrum', 'kanban', 'waterfall', 'devops', 'ci/cd', 'tdd', 'bdd',
            
            # Data Science and ML
            'machine learning', 'deep learning', 'data science', 'data analysis', 'statistics',
            'nlp', 'computer vision', 'neural networks', 'regression', 'classification',
            'clustering', 'recommendation systems', 'natural language processing',
            
            # Web Technologies
            'html', 'css', 'sass', 'less', 'webpack', 'babel', 'eslint', 'prettier',
            'rest api', 'soap', 'microservices', 'serverless', 'lambda',
            
            # Mobile Development
            'react native', 'flutter', 'xamarin', 'ionic', 'android', 'ios', 'swift',
            'kotlin', 'objective-c', 'xcode', 'android studio',
            
            # Other Technical Skills
            'algorithms', 'data structures', 'object-oriented programming', 'functional programming',
            'design patterns', 'software architecture', 'system design', 'distributed systems',
            'microservices', 'api design', 'testing', 'unit testing', 'integration testing',
            'performance optimization', 'security', 'cryptography', 'blockchain'
        }
        
        # Load skill keywords from JSON file
        self.skill_keywords = self._load_skill_keywords()
    
    def _load_skill_keywords(self) -> Set[str]:
        """Load skill keywords from JSON file or return default set"""
        try:
            if os.path.exists('skill_keywords.json'):
                with open('skill_keywords.json', 'r') as f:
                    data = json.load(f)
                    return set(data.get('skills', []))
            else:
                # Return default skills if file doesn't exist
                return self.technical_skills
        except Exception:
            return self.technical_skills
    
    def extract_skills(self, text: str) -> List[str]:
        """
        Extract skills from text using SpaCy NER and keyword matching
        """
        skills = set()
        
        # Convert text to lowercase for better matching
        text_lower = text.lower()
        
        # Method 1: Keyword-based extraction
        skills.update(self._extract_keyword_skills(text_lower))
        
        # Method 2: SpaCy NER extraction (if available)
        if self.nlp:
            skills.update(self._extract_ner_skills(text))
        
        # Method 3: Pattern-based extraction
        skills.update(self._extract_pattern_skills(text_lower))
        
        # Clean and normalize skills
        cleaned_skills = self._clean_skills(list(skills))
        
        return cleaned_skills
    
    def _extract_keyword_skills(self, text: str) -> Set[str]:
        """Extract skills using keyword matching"""
        found_skills = set()
        
        for skill in self.skill_keywords:
            # Check for exact matches and variations
            patterns = [
                skill,
                skill.replace(' ', ''),
                skill.replace(' ', '-'),
                skill.replace(' ', '_'),
                skill.upper(),
                skill.title()
            ]
            
            for pattern in patterns:
                if pattern in text:
                    found_skills.add(skill)
                    break
        
        return found_skills
    
    def _extract_ner_skills(self, text: str) -> Set[str]:
        """Extract skills using SpaCy NER"""
        skills = set()
        doc = self.nlp(text)
        
        # Look for entities that might be skills
        for ent in doc.ents:
            if ent.label_ in ['ORG', 'PRODUCT', 'GPE']:
                # Check if the entity matches any known skills
                entity_text = ent.text.lower()
                for skill in self.skill_keywords:
                    if skill in entity_text or entity_text in skill:
                        skills.add(skill)
        
        return skills
    
    def _extract_pattern_skills(self, text: str) -> Set[str]:
        """Extract skills using regex patterns"""
        skills = set()
        
        # Pattern for "X years of Y" or "experience with Y"
        patterns = [
            r'(\d+)\s*(?:years?|yrs?)\s*(?:of|in)\s*([a-zA-Z\s\+\#\.]+)',
            r'experience\s+(?:with|in)\s+([a-zA-Z\s\+\#\.]+)',
            r'proficient\s+in\s+([a-zA-Z\s\+\#\.]+)',
            r'skilled\s+in\s+([a-zA-Z\s\+\#\.]+)',
            r'expertise\s+in\s+([a-zA-Z\s\+\#\.]+)',
            r'knowledge\s+of\s+([a-zA-Z\s\+\#\.]+)',
            r'familiar\s+with\s+([a-zA-Z\s\+\#\.]+)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    # Handle groups in regex
                    for group in match:
                        if group.strip():
                            potential_skill = group.strip().lower()
                            if potential_skill in self.skill_keywords:
                                skills.add(potential_skill)
                else:
                    potential_skill = match.strip().lower()
                    if potential_skill in self.skill_keywords:
                        skills.add(potential_skill)
        
        return skills
    
    def _clean_skills(self, skills: List[str]) -> List[str]:
        """Clean and normalize extracted skills"""
        cleaned = []
        seen = set()
        
        for skill in skills:
            # Normalize skill name
            normalized = skill.lower().strip()
            
            # Remove common prefixes/suffixes
            normalized = re.sub(r'^(the\s+|a\s+|an\s+)', '', normalized)
            normalized = re.sub(r'\s+(framework|library|tool|technology|language|platform)$', '', normalized)
            
            # Skip if already seen or too short
            if normalized in seen or len(normalized) < 2:
                continue
            
            # Skip if it's just a common word
            common_words = {'the', 'and', 'or', 'with', 'in', 'on', 'at', 'to', 'for', 'of', 'by'}
            if normalized in common_words:
                continue
            
            cleaned.append(normalized)
            seen.add(normalized)
        
        return sorted(cleaned)

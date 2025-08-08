# AI/ML Skill Recommender

A comprehensive web application that helps users analyze their skills, match them against job requirements, and generate personalized learning roadmaps. Features both a FastAPI backend and a modern React-like frontend.

## Features

- **Modern Web Interface**: Beautiful, responsive frontend with glassmorphism effects and animations
- **Resume Upload & Skill Extraction**: Upload PDF, TXT, or DOCX resumes and extract skills using SpaCy NER and keyword matching
- **Job Role Matching**: Match user skills against predefined job role requirements with visual feedback
- **Skill Gap Analysis**: Identify missing skills and provide recommendations
- **Learning Roadmaps**: Generate personalized learning paths for specific skills
- **Resource Recommendations**: Curated learning resources from Coursera and YouTube
- **Interactive Dashboard**: Visual representation of skill matches and gaps

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- Modern web browser (Chrome 80+, Firefox 75+, Safari 13+, Edge 80+)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd AIML_skill_recommender
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download SpaCy model** (optional, for enhanced skill extraction):
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Starting the Application

```bash
# Development server
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or run directly
python main.py
```

### Accessing the Application

Once the server is running, you can access:

- **Web Application**: `http://localhost:8000` - The main frontend interface
- **Interactive API docs**: `http://localhost:8000/docs` - Backend API documentation
- **ReDoc documentation**: `http://localhost:8000/redoc` - Alternative API documentation

## Frontend Features

### 1. Home Page
- Modern landing page with animated elements
- Quick access to main features
- Responsive design with glassmorphism effects

### 2. Resume Upload
- Drag & drop file upload
- Support for PDF, TXT, and DOCX files
- Real-time skill extraction and display
- Visual feedback and progress indicators

### 3. Skill Matching
- Interactive skill input with removable tags
- Job role selection from comprehensive list
- Real-time skill matching with percentage visualization
- Detailed breakdown of matched and missing skills

### 4. Learning Roadmaps
- Skill selection from curated list
- Personalized learning paths with progression levels
- Curated resources with direct links
- Visual timeline representation

## Backend API Endpoints

### 1. Health Check
```http
GET /
GET /health
```

### 2. Upload Resume
```http
POST /upload-resume
Content-Type: multipart/form-data

file: <resume_file>
```

**Response**:
```json
{
  "filename": "resume.pdf",
  "extracted_skills": ["python", "javascript", "react", "git"],
  "text_length": 1500
}
```

### 3. Get Available Job Roles
```http
GET /job-roles
```

**Response**:
```json
[
  {
    "id": "software_engineer",
    "title": "Software Engineer",
    "description": "Develops software applications and systems"
  },
  {
    "id": "data_scientist",
    "title": "Data Scientist",
    "description": "Analyzes data and builds machine learning models"
  }
]
```

### 4. Match Skills
```http
POST /match-skills
Content-Type: application/x-www-form-urlencoded

user_skills: ["python", "javascript", "react"]
target_role: "software_engineer"
```

**Response**:
```json
{
  "target_role": "Software Engineer",
  "role_description": "Develops software applications and systems",
  "matched_skills": {
    "required": ["python", "javascript"],
    "preferred": ["react"]
  },
  "missing_skills": {
    "required": ["java", "git", "sql"],
    "preferred": ["docker", "kubernetes"]
  },
  "skill_gaps": [
    {
      "skill": "java",
      "type": "required",
      "priority": "high",
      "description": "Required skill for Software Engineer position"
    }
  ],
  "match_percentages": {
    "required": 28.57,
    "preferred": 10.0,
    "overall": 22.0
  },
  "overall_match_percentage": 22.0
}
```

### 5. Generate Learning Roadmap
```http
POST /generate-roadmap
Content-Type: application/x-www-form-urlencoded

skill: "python"
```

**Response**:
```json
{
  "skill": "python",
  "title": "Python Programming",
  "description": "Learn Python programming from beginner to advanced",
  "levels": [
    {
      "level": "beginner",
      "difficulty": "Beginner",
      "duration": "4-6 weeks",
      "topics": [
        "Python basics and syntax",
        "Variables and data types",
        "Control structures (if/else, loops)",
        "Functions and modules",
        "File handling",
        "Error handling"
      ],
      "learning_objectives": [
        "Master python basics and syntax",
        "Master variables and data types",
        "Master control structures (if/else, loops)",
        "Master functions and modules",
        "Master file handling",
        "Master error handling"
      ]
    }
  ],
  "resources": [
    {
      "title": "Python for Everybody",
      "type": "coursera",
      "url": "https://www.coursera.org/specializations/python",
      "description": "Comprehensive Python course for beginners",
      "duration": "4 months",
      "rating": "4.8"
    }
  ],
  "estimated_total_duration": "18 weeks",
  "difficulty_progression": ["beginner", "intermediate", "advanced"]
}
```

## Project Structure

```
AIML_skill_recommender/
├── main.py                 # FastAPI application entry point
├── skill_extractor.py      # Skill extraction using SpaCy and keyword matching
├── skill_matcher.py        # Skill matching against job requirements
├── roadmap_generator.py    # Learning roadmap generation
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── job_roles.json         # Job role definitions
├── skill_roadmaps.json    # Skill roadmap definitions
├── learning_resources.json # Learning resources
├── skill_keywords.json    # Skill keywords
└── frontend/              # Frontend application
    ├── index.html         # Main HTML file
    ├── styles.css         # CSS styles and animations
    ├── script.js          # JavaScript functionality
    └── README.md          # Frontend documentation
```

## Configuration

### Custom Job Roles

Create a `job_roles.json` file to define custom job roles:

```json
{
  "custom_role": {
    "title": "Custom Role",
    "description": "Description of the custom role",
    "required_skills": ["skill1", "skill2", "skill3"],
    "preferred_skills": ["skill4", "skill5"]
  }
}
```

### Custom Skill Roadmaps

Create a `skill_roadmaps.json` file to define custom learning roadmaps:

```json
{
  "custom_skill": {
    "title": "Custom Skill",
    "description": "Description of the skill",
    "levels": {
      "beginner": {
        "topics": ["topic1", "topic2"],
        "duration": "4-6 weeks",
        "difficulty": "Beginner"
      }
    }
  }
}
```

## Supported File Formats

- **PDF**: Resume in PDF format
- **TXT**: Plain text resume
- **DOCX**: Microsoft Word document

## Supported Skills

The system recognizes a wide range of technical skills including:

- **Programming Languages**: Python, Java, JavaScript, TypeScript, C++, C#, PHP, Ruby, Go, Rust, Swift, Kotlin, Scala, R, MATLAB, Perl, Bash, PowerShell, SQL
- **Frameworks & Libraries**: React, Angular, Vue, Node.js, Django, Flask, Spring, Express, FastAPI, TensorFlow, PyTorch, scikit-learn, Pandas, NumPy, Matplotlib, Seaborn, Bootstrap, Tailwind, jQuery, Lodash, Axios, Redux, Vuex, Next.js
- **Databases**: MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch, SQLite, Oracle, SQL Server
- **Cloud & DevOps**: AWS, Azure, GCP, Docker, Kubernetes, Jenkins, Git, GitHub, GitLab, Terraform, Ansible, Nginx, Apache, Linux, Ubuntu, CentOS
- **Tools & Platforms**: Jira, Confluence, Slack, Teams, Zoom, Figma, Adobe, Photoshop, Illustrator, Sketch, InVision, Zeplin, Postman, Swagger, GraphQL
- **Methodologies**: Agile, Scrum, Kanban, Waterfall, DevOps, CI/CD, TDD, BDD
- **Data Science & ML**: Machine Learning, Deep Learning, Data Science, Data Analysis, Statistics, NLP, Computer Vision, Neural Networks, Regression, Classification, Clustering, Recommendation Systems, Natural Language Processing
- **Web Technologies**: HTML, CSS, Sass, Less, Webpack, Babel, ESLint, Prettier, REST API, SOAP, Microservices, Serverless, Lambda
- **Mobile Development**: React Native, Flutter, Xamarin, Ionic, Android, iOS, Swift, Kotlin, Objective-C, Xcode, Android Studio
- **Other Technical Skills**: Algorithms, Data Structures, Object-Oriented Programming, Functional Programming, Design Patterns, Software Architecture, System Design, Distributed Systems, Microservices, API Design, Testing, Unit Testing, Integration Testing, Performance Optimization, Security, Cryptography, Blockchain

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on the GitHub repository.

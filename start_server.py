#!/usr/bin/env python3
"""
Startup script for the Skill Recommender API
"""

import uvicorn
import os
import sys

def main():
    """Start the FastAPI server"""
    print("🚀 Starting Skill Recommender API...")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ["main.py", "skill_extractor.py", "skill_matcher.py", "roadmap_generator.py"]
    missing_files = []
    
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        print("Please ensure all required files are present in the current directory.")
        sys.exit(1)
    
    # Check if virtual environment is activated (optional)
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected.")
        print("   It's recommended to activate a virtual environment before running the server.")
        print("   Run: python -m venv venv && source venv/bin/activate (Linux/Mac) or venv\\Scripts\\activate (Windows)")
        print()
    
    # Configuration
    host = "0.0.0.0"
    port = 8000
    reload = True
    
    print(f"📍 Server will be available at: http://localhost:{port}")
    print(f"📚 API Documentation: http://localhost:{port}/docs")
    print(f"📖 ReDoc Documentation: http://localhost:{port}/redoc")
    print()
    print("🔄 Starting server... (Press Ctrl+C to stop)")
    print("=" * 50)
    
    try:
        uvicorn.run(
            "main:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Setup Verification Script
Checks if the environment is properly configured
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.9+")
        return False

def check_dependencies():
    """Check if dependencies are installed"""
    required = [
        'streamlit',
        'langchain',
        'youtube_transcript_api',
        'beautifulsoup4',
        'requests',
        'tiktoken'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Not installed")
            missing.append(package)
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has keys"""
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   → Run: cp .env.example .env")
        print("   → Then add your API keys")
        return False
    
    print("✅ .env file exists")
    
    # Check if keys are configured
    from dotenv import load_dotenv
    load_dotenv()
    
    groq_key = os.getenv('GROQ_API_KEY', '')
    gemini_key = os.getenv('GOOGLE_API_KEY', '')
    
    if groq_key and groq_key != 'your_groq_api_key_here':
        print("✅ Groq API key configured")
        return True
    elif gemini_key and gemini_key != 'your_google_api_key_here':
        print("✅ Gemini API key configured")
        return True
    else:
        print("⚠️  No API keys configured")
        print("   → Edit .env file")
        print("   → Add GROQ_API_KEY or GOOGLE_API_KEY")
        return False

def check_structure():
    """Check project structure"""
    required_dirs = [
        'src',
        'src/extractors',
        'src/processors',
        'src/engines',
        'src/llm',
        'src/utils',
        'src/ui',
        '.streamlit'
    ]
    
    required_files = [
        'app.py',
        'requirements.txt',
        'README.md',
        '.env.example'
    ]
    
    all_ok = True
    
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - Missing")
            all_ok = False
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_ok = False
    
    return all_ok

def main():
    """Run all checks"""
    print("=" * 60)
    print("  Content Intelligence Platform - Setup Verification")
    print("=" * 60)
    
    print("\n📋 Checking Python version...")
    python_ok = check_python_version()
    
    print("\n📦 Checking dependencies...")
    deps_ok = check_dependencies()
    
    print("\n🔑 Checking environment configuration...")
    env_ok = check_env_file()
    
    print("\n📁 Checking project structure...")
    structure_ok = check_structure()
    
    print("\n" + "=" * 60)
    
    if python_ok and deps_ok and structure_ok:
        if env_ok:
            print("✅ ALL CHECKS PASSED! Ready to run.")
            print("\n🚀 Start the app:")
            print("   streamlit run app.py")
        else:
            print("⚠️  Setup incomplete - Add API keys to .env")
            print("\n📝 Next steps:")
            print("   1. Edit .env file")
            print("   2. Add API key (Groq or Gemini)")
            print("   3. Run: streamlit run app.py")
    else:
        print("❌ SETUP INCOMPLETE")
        if not python_ok:
            print("\n→ Upgrade Python to 3.9+")
        if not deps_ok:
            print("\n→ Install dependencies: pip install -r requirements.txt")
        if not structure_ok:
            print("\n→ Check project structure")
    
    print("=" * 60)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Simple runner script for plagiarism detection
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_plagiarism.txt"])
        print("✅ Requirements installed successfully")
    except subprocess.CalledProcessError:
        print("⚠️  Failed to install requirements. Please install manually:")
        print("pip install requests urllib3")

def main():
    print("🔍 Plagiarism Detection Tool")
    print("=" * 40)
    
    # Check if requirements are installed
    try:
        import requests
    except ImportError:
        print("📦 Installing requirements...")
        install_requirements()
    
    # Ask user which version to run
    print("\nChoose detection mode:")
    print("1. Basic plagiarism detection (predefined GitHub repos)")
    print("2. Enhanced detection (predefined GitHub + local repos)")
    print("3. GitHub-wide detection (searches ALL of GitHub) 🌟")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        print("\n🚀 Running basic plagiarism detection...")
        os.system("python3 plagiarism_detector.py")
    elif choice == "2":
        print("\n🚀 Running enhanced plagiarism detection...")
        os.system("python3 enhanced_plagiarism_detector.py")
    elif choice == "3":
        print("\n🌟 Running GitHub-wide plagiarism detection...")
        print("⚠️  This will search across all of GitHub and may take a while!")
        print("💡 Tip: Set GITHUB_TOKEN environment variable for better results")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm in ['y', 'yes']:
            os.system("python3 github_wide_simple.py")
        else:
            print("❌ GitHub-wide detection cancelled.")
    else:
        print("❌ Invalid choice. Please run the script again.")

if __name__ == "__main__":
    main()

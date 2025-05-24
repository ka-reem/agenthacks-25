#!/usr/bin/env python3
"""
Test script for GitHub-wide plagiarism detection
"""

import os
import sys

def test_github_wide_detector():
    """Test the GitHub-wide plagiarism detector initialization"""
    try:
        from github_wide_plagiarism_detector import GitHubWidePlagiarismDetector
        
        print("🧪 Testing GitHub-wide plagiarism detector...")
        
        # Initialize detector
        detector = GitHubWidePlagiarismDetector()
        print("✅ Detector initialized successfully")
        
        # Test repo info extraction
        test_repo = "https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten"
        repo_name = detector.get_repo_info(test_repo)
        print(f"✅ Repo name extraction: {repo_name}")
        
        # Test keyword extraction with mock data
        from github_wide_plagiarism_detector import FileInfo, RepoInfo
        
        mock_files = [
            FileInfo("main.py", "def dispatch_emergency():\n    pass", "hash1", 100, 2),
            FileInfo("server/app.js", "const dispatchServer = require('express')", "hash2", 50, 1)
        ]
        
        mock_repo = RepoInfo("test", "test", mock_files, 2, 3)
        keywords = detector.extract_search_keywords(mock_repo)
        print(f"✅ Keyword extraction: {keywords}")
        
        print("✅ All tests passed! GitHub-wide detector is ready to use.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    print("🔍 GitHub-Wide Plagiarism Detector Test")
    print("=" * 50)
    
    # Test basic functionality
    if test_github_wide_detector():
        print("\n🚀 Ready to run GitHub-wide plagiarism detection!")
        print("Use: python3 github_wide_plagiarism_detector.py")
        print("Or:  python3 run_plagiarism_check.py (option 3)")
    else:
        print("\n❌ Tests failed. Please check the installation.")

if __name__ == "__main__":
    main()

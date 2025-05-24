#!/usr/bin/env python3
"""
GitHub-Wide Plagiarism Detection Tool (Simplified)
Searches across all of GitHub to find potentially plagiarized repositories
"""

import requests
import os
import json
import hashlib
import difflib
import re
import time
from typing import Dict, List, Tuple, Set
from urllib.parse import urlparse, quote
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class FileInfo:
    """Information about a file in a repository"""
    path: str
    content: str
    hash: str
    size: int
    lines: int

@dataclass  
class RepoInfo:
    """Information about a repository"""
    url: str
    name: str
    files: List[FileInfo] = field(default_factory=list)
    total_files: int = 0
    total_lines: int = 0
    stars: int = 0
    language: str = ""
    description: str = ""

def get_repo_info(repo_url: str) -> str:
    """Extract repository information from GitHub URL"""
    if repo_url.startswith('http'):
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
    else:
        path_parts = repo_url.split('/')
    
    if len(path_parts) >= 2:
        owner = path_parts[0]
        repo = path_parts[1]
        return f"{owner}/{repo}"
    
    raise ValueError(f"Invalid GitHub repository: {repo_url}")

def search_github_repositories(keywords: List[str], github_token: str = None) -> List[Dict]:
    """Search GitHub for repositories using keywords"""
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
    
    print(f"🔍 Searching GitHub with keywords: {', '.join(keywords[:3])}...")
    
    all_repos = []
    search_queries = keywords[:3] + ["hackathon", "dispatch", "emergency"]
    
    for query in search_queries[:5]:  # Limit to avoid rate limits
        try:
            search_url = f"https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': 10
            }
            
            response = requests.get(search_url, headers=headers, params=params)
            
            if response.status_code == 403:
                print(f"⚠️  Rate limit hit. Waiting...")
                time.sleep(60)
                continue
            
            if response.status_code == 200:
                search_results = response.json()
                repos = search_results.get('items', [])
                
                for repo in repos:
                    repo_info = {
                        'name': repo['full_name'],
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'language': repo.get('language', ''),
                        'description': repo.get('description', ''),
                        'size': repo['size']
                    }
                    all_repos.append(repo_info)
                    
                print(f"📋 Found {len(repos)} repositories for query: '{query}'")
            
            time.sleep(2)  # Rate limiting
            
        except Exception as e:
            print(f"❌ Error searching for '{query}': {e}")
    
    # Remove duplicates
    unique_repos = {}
    for repo in all_repos:
        if repo['name'] not in unique_repos:
            unique_repos[repo['name']] = repo
    
    sorted_repos = sorted(unique_repos.values(), key=lambda x: x['stars'], reverse=True)
    print(f"📊 Total unique repositories found: {len(sorted_repos)}")
    
    return sorted_repos[:20]  # Return top 20

def fetch_file_content(download_url: str, headers: dict) -> str:
    """Fetch file content from GitHub"""
    try:
        response = requests.get(download_url, headers=headers)
        if response.status_code == 200:
            return response.text[:10000]  # Limit content size
    except:
        pass
    return None

def fetch_repo_contents(repo_name: str, github_token: str = None) -> RepoInfo:
    """Fetch repository contents from GitHub API"""
    headers = {}
    if github_token:
        headers['Authorization'] = f'token {github_token}'
        
    try:
        print(f"📥 Fetching repository: {repo_name}")
        
        api_url = f"https://api.github.com/repos/{repo_name}/contents"
        response = requests.get(api_url, headers=headers)
        
        if response.status_code != 200:
            return None
        
        items = response.json()
        files = []
        
        # Only get files from root directory to avoid rate limits
        for item in items[:10]:  # Limit files
            if item['type'] == 'file':
                file_path = item['path']
                file_ext = os.path.splitext(file_path)[1].lower()
                
                if file_ext in ['.py', '.js', '.ts', '.java', '.cpp', '.c']:
                    file_content = fetch_file_content(item['download_url'], headers)
                    if file_content and len(file_content) >= 50:
                        file_info = FileInfo(
                            path=file_path,
                            content=file_content,
                            hash=hashlib.md5(file_content.encode()).hexdigest(),
                            size=len(file_content),
                            lines=len(file_content.splitlines())
                        )
                        files.append(file_info)
        
        total_lines = sum(f.lines for f in files)
        
        return RepoInfo(
            url=f"https://github.com/{repo_name}",
            name=repo_name,
            files=files,
            total_files=len(files),
            total_lines=total_lines
        )
        
    except Exception as e:
        print(f"❌ Error fetching repository {repo_name}: {e}")
        return None

def normalize_code(content: str) -> str:
    """Normalize code content for comparison"""
    # Remove comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)
    
    # Remove whitespace and normalize
    content = re.sub(r'\s+', ' ', content)
    return content.strip().lower()

def calculate_similarity(content1: str, content2: str) -> float:
    """Calculate similarity between two pieces of content"""
    normalized1 = normalize_code(content1)
    normalized2 = normalize_code(content2)
    return difflib.SequenceMatcher(None, normalized1, normalized2).ratio()

def extract_keywords(repo_info: RepoInfo) -> List[str]:
    """Extract keywords from repository content"""
    keywords = set()
    
    for file_info in repo_info.files:
        # Add file names
        filename = os.path.splitext(os.path.basename(file_info.path))[0]
        if len(filename) > 3:
            keywords.add(filename.lower())
        
        # Extract function/class names
        content = file_info.content.lower()
        patterns = [r'class\s+(\w+)', r'function\s+(\w+)', r'def\s+(\w+)']
        for pattern in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if len(match) > 4:
                    keywords.add(match)
    
    return list(keywords)[:5]

def detect_plagiarism_github_wide(target_repo: str) -> Dict:
    """Detect plagiarism by searching across GitHub"""
    print(f"🔍 Starting GitHub-wide plagiarism detection for: {target_repo}")
    
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  No GitHub token found. Search will be limited.")
    
    # Fetch target repository
    target_repo_name = get_repo_info(target_repo)
    target_info = fetch_repo_contents(target_repo_name, github_token)
    if not target_info:
        return {"error": "Failed to fetch target repository"}
    
    print(f"✅ Target repo: {target_info.total_files} files, {target_info.total_lines} lines")
    
    # Extract keywords
    keywords = extract_keywords(target_info)
    print(f"🔑 Keywords: {', '.join(keywords)}")
    
    # Search GitHub
    candidate_repos = search_github_repositories(keywords, github_token)
    
    results = {
        "target_repo": target_repo,
        "target_stats": {
            "files": target_info.total_files,
            "lines": target_info.total_lines
        },
        "search_keywords": keywords,
        "candidates_found": len(candidate_repos),
        "suspicious_matches": [],
        "identical_files": []
    }
    
    print(f"📋 Analyzing {len(candidate_repos)} repositories...")
    
    # Compare with candidates
    for i, candidate in enumerate(candidate_repos):
        print(f"🔄 [{i+1}/{len(candidate_repos)}] {candidate['name']} (⭐{candidate['stars']})")
        
        if candidate['name'].lower() == target_repo_name.lower():
            continue
        
        comp_info = fetch_repo_contents(candidate['name'], github_token)
        if not comp_info:
            continue
        
        # Compare files
        for target_file in target_info.files:
            for comp_file in comp_info.files:
                if os.path.splitext(target_file.path)[1] == os.path.splitext(comp_file.path)[1]:
                    similarity = calculate_similarity(target_file.content, comp_file.content)
                    
                    if target_file.hash == comp_file.hash:
                        results["identical_files"].append({
                            "repo": candidate['name'],
                            "repo_url": candidate['url'],
                            "target_file": target_file.path,
                            "comparison_file": comp_file.path,
                            "stars": candidate['stars']
                        })
                    elif similarity > 0.8:
                        results["suspicious_matches"].append({
                            "repo": candidate['name'],
                            "repo_url": candidate['url'],
                            "target_file": target_file.path,
                            "comparison_file": comp_file.path,
                            "similarity": similarity,
                            "stars": candidate['stars']
                        })
        
        time.sleep(1)  # Rate limiting
    
    # Summary
    risk_level = "LOW"
    if len(results["identical_files"]) > 0:
        risk_level = "CRITICAL"
    elif len(results["suspicious_matches"]) > 5:
        risk_level = "HIGH"
    elif len(results["suspicious_matches"]) > 2:
        risk_level = "MEDIUM"
    
    results["summary"] = {
        "plagiarism_risk": risk_level,
        "total_suspicious": len(results["suspicious_matches"]),
        "total_identical": len(results["identical_files"])
    }
    
    return results

def generate_report(results: Dict):
    """Generate plagiarism report"""
    print("\n" + "="*80)
    print("GITHUB-WIDE PLAGIARISM DETECTION REPORT")
    print("="*80)
    print(f"Target: {results['target_repo']}")
    print(f"Risk Level: {results['summary']['plagiarism_risk']}")
    print(f"Keywords Used: {', '.join(results['search_keywords'])}")
    print(f"Repositories Found: {results['candidates_found']}")
    print(f"Suspicious Matches: {results['summary']['total_suspicious']}")
    print(f"Identical Files: {results['summary']['total_identical']}")
    print()
    
    if results["identical_files"]:
        print("🚨 IDENTICAL FILES FOUND:")
        for match in results["identical_files"]:
            print(f"  {match['repo']} (⭐{match['stars']})")
            print(f"    {match['target_file']} = {match['comparison_file']}")
        print()
    
    if results["suspicious_matches"]:
        print("⚠️  SUSPICIOUS MATCHES:")
        for match in results["suspicious_matches"][:10]:
            print(f"  {match['repo']} (⭐{match['stars']})")
            print(f"    {match['target_file']} → {match['comparison_file']} ({match['similarity']:.1%})")
        print()
    
    print("="*80)
    
    # Save report
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    with open(f"github_wide_report_{timestamp}.json", 'w') as f:
        json.dump(results, f, indent=2)
    print(f"📄 Report saved as: github_wide_report_{timestamp}.json")

def main():
    """Main function"""
    target_repo = "https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten"
    
    print("🚀 GitHub-Wide Plagiarism Detection")
    print("="*50)
    
    try:
        results = detect_plagiarism_github_wide(target_repo)
        
        if "error" in results:
            print(f"❌ {results['error']}")
            return
        
        generate_report(results)
        
        if results['summary']['plagiarism_risk'] in ['HIGH', 'CRITICAL']:
            print(f"\n🚨 {results['summary']['plagiarism_risk']} RISK DETECTED!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
GitHub-Wide Plagiarism Detection Tool
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
from dataclasses import dataclass
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
    files: List[FileInfo]
    total_files: int
    total_lines: int
    stars: int = 0
    language: str = ""
    description: str = ""

class GitHubWidePlagiarismDetector:
    def __init__(self, github_token: str = None):
        """
        Initialize the GitHub-wide plagiarism detector
        
        Args:
            github_token: GitHub personal access token for API access
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.headers = {}
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
        
        # File extensions to analyze for code plagiarism
        self.code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.sass', '.vue', '.svelte', '.dart',
            '.r', '.m', '.sql', '.sh', '.bash', '.ps1', '.yaml', '.yml',
            '.json', '.xml', '.md', '.txt', '.dockerfile', '.makefile'
        }
        
        # Search parameters
        self.min_file_size = 50
        self.similarity_threshold = 0.7
        self.max_repos_to_check = 50  # Limit for API rate limiting
        self.max_files_per_repo = 20  # Limit files analyzed per repo

    def get_repo_info(self, repo_url: str) -> str:
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

    def extract_search_keywords(self, repo_info: RepoInfo) -> List[str]:
        """
        Extract keywords from repository content for GitHub search
        
        Args:
            repo_info: Target repository information
            
        Returns:
            List of search keywords
        """
        keywords = set()
        
        # Extract from file names and paths
        for file_info in repo_info.files:
            # Add file names without extension
            filename = os.path.splitext(os.path.basename(file_info.path))[0]
            if len(filename) > 3 and filename not in ['main', 'index', 'app', 'test']:
                keywords.add(filename.lower())
            
            # Extract directory names
            dirs = file_info.path.split('/')[:-1]
            for dir_name in dirs:
                if len(dir_name) > 3 and dir_name not in ['src', 'lib', 'utils', 'components']:
                    keywords.add(dir_name.lower())
        
        # Extract from code content (function names, class names, etc.)
        code_patterns = [
            r'class\s+(\w+)',  # Class names
            r'function\s+(\w+)',  # Function names
            r'def\s+(\w+)',  # Python function names
            r'const\s+(\w+)',  # Constants
            r'let\s+(\w+)',  # Variables
            r'var\s+(\w+)',  # Variables
        ]
        
        for file_info in repo_info.files:
            content = file_info.content.lower()
            for pattern in code_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if len(match) > 4 and match not in ['main', 'init', 'test', 'index']:
                        keywords.add(match)
        
        # Filter and return top keywords
        filtered_keywords = [k for k in keywords if len(k) > 3 and k.isalpha()]
        return list(filtered_keywords)[:10]  # Return top 10 keywords

    def search_github_repositories(self, keywords: List[str], target_language: str = None) -> List[Dict]:
        """
        Search GitHub for repositories using keywords
        
        Args:
            keywords: List of search keywords
            target_language: Programming language filter
            
        Returns:
            List of repository information from search results
        """
        print(f"🔍 Searching GitHub with keywords: {', '.join(keywords[:5])}...")
        
        all_repos = []
        search_queries = []
        
        # Create different search query combinations
        if keywords:
            # Search with individual keywords
            for keyword in keywords[:5]:  # Use top 5 keywords
                search_queries.append(keyword)
            
            # Search with keyword combinations
            if len(keywords) >= 2:
                search_queries.append(f"{keywords[0]} {keywords[1]}")
            
            # Add language filter if detected
            if target_language:
                search_queries.append(f"language:{target_language}")
        
        # Fallback searches
        search_queries.extend([
            "dispatch emergency",
            "hackathon project",
            "ai assistant",
            "web application"
        ])
        
        for query in search_queries[:8]:  # Limit search queries
            try:
                # Search repositories
                search_url = f"https://api.github.com/search/repositories"
                params = {
                    'q': query,
                    'sort': 'stars',
                    'order': 'desc',
                    'per_page': 20
                }
                
                response = requests.get(search_url, headers=self.headers, params=params)
                
                if response.status_code == 403:
                    print(f"⚠️  Rate limit hit during search. Waiting 60 seconds...")
                    time.sleep(60)
                    response = requests.get(search_url, headers=self.headers, params=params)
                
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
                else:
                    print(f"❌ Search failed for query '{query}': {response.status_code}")
                
                # Rate limiting
                time.sleep(1)
                
            except Exception as e:
                print(f"❌ Error searching for '{query}': {e}")
        
        # Remove duplicates and sort by stars
        unique_repos = {}
        for repo in all_repos:
            if repo['name'] not in unique_repos:
                unique_repos[repo['name']] = repo
        
        sorted_repos = sorted(unique_repos.values(), key=lambda x: x['stars'], reverse=True)
        print(f"📊 Total unique repositories found: {len(sorted_repos)}")
        
        return sorted_repos[:self.max_repos_to_check]

    def fetch_repo_contents(self, repo_name: str) -> RepoInfo:
        """
        Fetch repository contents from GitHub API
        
        Args:
            repo_name: Repository name in format "owner/repo"
            
        Returns:
            RepoInfo object containing repository data
        """
        try:
            print(f"📥 Fetching repository: {repo_name}")
            
            api_url = f"https://api.github.com/repos/{repo_name}/contents"
            files = []
            files_processed = 0
            
            def fetch_directory(url: str, path: str = ""):
                """Recursively fetch directory contents"""
                nonlocal files_processed
                
                if files_processed >= self.max_files_per_repo:
                    return
                
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 403:
                        print(f"⚠️  Rate limit hit. Waiting 60 seconds...")
                        time.sleep(60)
                        response = requests.get(url, headers=self.headers)
                    
                    if response.status_code != 200:
                        return
                    
                    items = response.json()
                    
                    for item in items:
                        if files_processed >= self.max_files_per_repo:
                            break
                            
                        if item['type'] == 'file':
                            file_path = item['path']
                            file_ext = os.path.splitext(file_path)[1].lower()
                            
                            # Only process code files
                            if file_ext in self.code_extensions:
                                file_content = self.fetch_file_content(item['download_url'])
                                if file_content and len(file_content) >= self.min_file_size:
                                    file_info = FileInfo(
                                        path=file_path,
                                        content=file_content,
                                        hash=hashlib.md5(file_content.encode()).hexdigest(),
                                        size=len(file_content),
                                        lines=len(file_content.splitlines())
                                    )
                                    files.append(file_info)
                                    files_processed += 1
                        
                        elif item['type'] == 'dir' and files_processed < self.max_files_per_repo:
                            # Recursively fetch subdirectory
                            fetch_directory(item['url'], item['path'])
                
                except Exception as e:
                    print(f"❌ Error fetching directory {url}: {e}")
            
            fetch_directory(api_url)
            
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

    def fetch_file_content(self, download_url: str) -> str:
        """Fetch file content from GitHub"""
        try:
            response = requests.get(download_url, headers=self.headers)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"❌ Error fetching file content: {e}")
        return None

    def normalize_code(self, content: str) -> str:
        """
        Normalize code content for comparison
        
        Args:
            content: Raw file content
            
        Returns:
            Normalized content string
        """
        # Remove comments (basic patterns)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)  # Single-line comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)  # Multi-line comments
        content = re.sub(r'#.*$', '', content, flags=re.MULTILINE)   # Python/shell comments
        
        # Remove extra whitespace and normalize
        content = re.sub(r'\s+', ' ', content)
        content = content.strip().lower()
        
        return content

    def calculate_similarity(self, content1: str, content2: str) -> float:
        """
        Calculate similarity between two pieces of content
        
        Args:
            content1: First content string
            content2: Second content string
            
        Returns:
            Similarity ratio between 0 and 1
        """
        normalized1 = self.normalize_code(content1)
        normalized2 = self.normalize_code(content2)
        
        # Use SequenceMatcher for similarity calculation
        similarity = difflib.SequenceMatcher(None, normalized1, normalized2).ratio()
        return similarity

    def detect_plagiarism_github_wide(self, target_repo: str) -> Dict:
        """
        Detect plagiarism by searching across all of GitHub
        
        Args:
            target_repo: Repository URL to check for plagiarism
            
        Returns:
            Dictionary containing plagiarism analysis results
        """
        print(f"🔍 Starting GitHub-wide plagiarism detection for: {target_repo}")
        
        # Fetch target repository
        target_repo_name = self.get_repo_info(target_repo)
        target_info = self.fetch_repo_contents(target_repo_name)
        if not target_info:
            return {"error": "Failed to fetch target repository"}
        
        print(f"✅ Target repo: {target_info.total_files} files, {target_info.total_lines} lines")
        
        # Extract keywords for searching
        keywords = self.extract_search_keywords(target_info)
        print(f"🔑 Extracted keywords: {', '.join(keywords)}")
        
        # Detect primary language
        languages = {}
        for file_info in target_info.files:
            ext = os.path.splitext(file_info.path)[1].lower()
            languages[ext] = languages.get(ext, 0) + 1
        
        primary_language = None
        if languages:
            primary_ext = max(languages.keys(), key=languages.get)
            language_map = {
                '.py': 'Python', '.js': 'JavaScript', '.ts': 'TypeScript',
                '.java': 'Java', '.cpp': 'C++', '.c': 'C', '.cs': 'C#',
                '.php': 'PHP', '.rb': 'Ruby', '.go': 'Go'
            }
            primary_language = language_map.get(primary_ext)
        
        print(f"🔤 Detected primary language: {primary_language or 'Unknown'}")
        
        # Search GitHub for similar repositories
        candidate_repos = self.search_github_repositories(keywords, primary_language)
        
        results = {
            "target_repo": target_repo,
            "target_stats": {
                "files": target_info.total_files,
                "lines": target_info.total_lines,
                "primary_language": primary_language
            },
            "search_keywords": keywords,
            "candidates_found": len(candidate_repos),
            "comparisons": [],
            "suspicious_matches": [],
            "identical_files": [],
            "summary": {}
        }
        
        print(f"📋 Analyzing {len(candidate_repos)} candidate repositories...")
        
        # Compare with each candidate repository
        for i, candidate in enumerate(candidate_repos):
            print(f"\n🔄 [{i+1}/{len(candidate_repos)}] Comparing with: {candidate['name']} (⭐{candidate['stars']})")
            
            # Skip if it's the same repository
            if candidate['name'].lower() == target_repo_name.lower():
                print("⏭️  Skipping self-comparison")
                continue
            
            comparison_info = self.fetch_repo_contents(candidate['name'])
            if not comparison_info:
                print(f"❌ Failed to fetch: {candidate['name']}")
                continue
            
            print(f"✅ Repo stats: {comparison_info.total_files} files, {comparison_info.total_lines} lines")
            
            # Compare files
            matches = []
            identical_matches = []
            total_similarity = 0
            comparisons_made = 0
            
            for target_file in target_info.files:
                for comp_file in comparison_info.files:
                    # Compare files with similar paths or extensions
                    if (os.path.splitext(target_file.path)[1] == os.path.splitext(comp_file.path)[1] or
                        os.path.basename(target_file.path) == os.path.basename(comp_file.path)):
                        
                        similarity = self.calculate_similarity(target_file.content, comp_file.content)
                        total_similarity += similarity
                        comparisons_made += 1
                        
                        # Check for identical files (hash comparison)
                        if target_file.hash == comp_file.hash:
                            identical_match = {
                                "target_file": target_file.path,
                                "comparison_file": comp_file.path,
                                "repo": candidate['name'],
                                "repo_url": candidate['url'],
                                "lines": target_file.lines,
                                "stars": candidate['stars']
                            }
                            identical_matches.append(identical_match)
                            results["identical_files"].append(identical_match)
                        
                        elif similarity >= self.similarity_threshold:
                            match = {
                                "target_file": target_file.path,
                                "comparison_file": comp_file.path,
                                "similarity": similarity,
                                "target_lines": target_file.lines,
                                "comparison_lines": comp_file.lines
                            }
                            matches.append(match)
                            
                            if similarity > 0.9:
                                results["suspicious_matches"].append({
                                    "repo": candidate['name'],
                                    "repo_url": candidate['url'],
                                    "stars": candidate['stars'],
                                    "match": match
                                })
            
            avg_similarity = total_similarity / comparisons_made if comparisons_made > 0 else 0
            
            comparison_result = {
                "repo": candidate['name'],
                "repo_url": candidate['url'],
                "stars": candidate['stars'],
                "language": candidate['language'],
                "description": candidate['description'],
                "repo_stats": {
                    "files": comparison_info.total_files,
                    "lines": comparison_info.total_lines
                },
                "matches": matches,
                "identical_files": identical_matches,
                "average_similarity": avg_similarity,
                "high_similarity_files": len(matches)
            }
            
            results["comparisons"].append(comparison_result)
            
            if identical_matches or len(matches) > 0:
                print(f"🚨 Found {len(matches)} suspicious matches, {len(identical_matches)} identical files (avg: {avg_similarity:.2f})")
            else:
                print(f"✅ No significant matches found (avg: {avg_similarity:.2f})")
        
        # Generate summary
        total_suspicious = len(results["suspicious_matches"])
        total_identical = len(results["identical_files"])
        total_comparisons = len(results["comparisons"])
        
        # Determine risk level based on findings
        if total_identical > 5 or total_suspicious > 15:
            risk_level = "CRITICAL"
        elif total_identical > 2 or total_suspicious > 8:
            risk_level = "HIGH"
        elif total_identical > 0 or total_suspicious > 3:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        results["summary"] = {
            "total_repositories_searched": len(candidate_repos),
            "total_repositories_compared": total_comparisons,
            "total_suspicious_matches": total_suspicious,
            "total_identical_files": total_identical,
            "plagiarism_risk": risk_level
        }
        
        return results

    def generate_github_wide_report(self, results: Dict, output_file: str = None):
        """
        Generate a comprehensive GitHub-wide plagiarism report
        
        Args:
            results: Results from detect_plagiarism_github_wide()
            output_file: Optional file to save the report
        """
        report = []
        report.append("=" * 120)
        report.append("GITHUB-WIDE PLAGIARISM DETECTION REPORT")
        report.append("=" * 120)
        report.append(f"Target Repository: {results['target_repo']}")
        report.append(f"Target Stats: {results['target_stats']['files']} files, {results['target_stats']['lines']} lines")
        report.append(f"Primary Language: {results['target_stats']['primary_language']}")
        report.append(f"Search Keywords: {', '.join(results['search_keywords'])}")
        report.append(f"Plagiarism Risk: {results['summary']['plagiarism_risk']}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary section
        report.append("📊 SEARCH & ANALYSIS SUMMARY:")
        report.append("-" * 80)
        report.append(f"GitHub Repositories Searched: {results['summary']['total_repositories_searched']}")
        report.append(f"Repositories Successfully Analyzed: {results['summary']['total_repositories_compared']}")
        report.append(f"Suspicious Matches Found (>90% similarity): {results['summary']['total_suspicious_matches']}")
        report.append(f"Identical Files Found (100% match): {results['summary']['total_identical_files']}")
        report.append("")
        
        # Critical findings - Identical files
        if results['identical_files']:
            report.append("🚨 CRITICAL: IDENTICAL FILES FOUND (100% match)")
            report.append("-" * 80)
            for match in results['identical_files']:
                report.append(f"Repository: {match['repo']} (⭐{match['stars']} stars)")
                report.append(f"  URL: {match['repo_url']}")
                report.append(f"  Identical File: {match['target_file']} = {match['comparison_file']}")
                report.append(f"  Lines of Code: {match['lines']}")
                report.append("")
        
        # High-risk findings - Suspicious matches
        if results['suspicious_matches']:
            report.append("⚠️  HIGH RISK: SUSPICIOUS MATCHES (>90% similarity)")
            report.append("-" * 80)
            
            # Group by repository
            repo_matches = {}
            for match in results['suspicious_matches']:
                repo = match['repo']
                if repo not in repo_matches:
                    repo_matches[repo] = {
                        'url': match['repo_url'],
                        'stars': match['stars'],
                        'matches': []
                    }
                repo_matches[repo]['matches'].append(match['match'])
            
            for repo, info in repo_matches.items():
                report.append(f"Repository: {repo} (⭐{info['stars']} stars)")
                report.append(f"  URL: {info['url']}")
                report.append(f"  Suspicious Files ({len(info['matches'])}):")
                for match in info['matches']:
                    report.append(f"    {match['target_file']} → {match['comparison_file']} ({match['similarity']:.1%})")
                report.append("")
        
        # Detailed comparison results
        report.append("📋 DETAILED ANALYSIS RESULTS:")
        report.append("-" * 80)
        
        # Sort comparisons by risk (identical files, then high similarity, then stars)
        sorted_comparisons = sorted(
            results['comparisons'], 
            key=lambda x: (len(x['identical_files']), x['high_similarity_files'], x['stars']), 
            reverse=True
        )
        
        for comparison in sorted_comparisons[:20]:  # Show top 20 results
            risk_indicator = ""
            if comparison['identical_files']:
                risk_indicator = " 🚨 CRITICAL"
            elif comparison['high_similarity_files'] > 0:
                risk_indicator = " ⚠️  SUSPICIOUS"
            
            report.append(f"Repository: {comparison['repo']} (⭐{comparison['stars']} stars){risk_indicator}")
            report.append(f"  URL: {comparison['repo_url']}")
            report.append(f"  Language: {comparison['language']}")
            report.append(f"  Description: {comparison['description'][:100]}...")
            report.append(f"  Stats: {comparison['repo_stats']['files']} files, {comparison['repo_stats']['lines']} lines")
            report.append(f"  Average Similarity: {comparison['average_similarity']:.2%}")
            report.append(f"  High Similarity Files: {comparison['high_similarity_files']}")
            report.append(f"  Identical Files: {len(comparison['identical_files'])}")
            
            if comparison['identical_files']:
                report.append("  IDENTICAL FILES:")
                for match in comparison['identical_files']:
                    report.append(f"    {match['target_file']} = {match['comparison_file']}")
            
            if comparison['matches']:
                report.append("  SIMILAR FILES:")
                for match in comparison['matches'][:3]:  # Show top 3 matches
                    report.append(f"    {match['target_file']} ({match['similarity']:.1%})")
            report.append("")
        
        report.append("=" * 120)
        report.append("NOTE: This analysis searched across GitHub using extracted keywords and similarity matching.")
        report.append("High similarity scores may indicate code reuse, common patterns, or potential plagiarism.")
        report.append("Manual review is recommended for all flagged repositories.")
        report.append("=" * 120)
        
        report_text = "\n".join(report)
        print(report_text)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"📄 Report saved to: {output_file}")

def main():
    """Main function to run GitHub-wide plagiarism detection"""
    
    print("🚀 GitHub-Wide Plagiarism Detection Tool")
    print("=" * 80)
    print("This tool will search across all of GitHub to find potential plagiarism")
    print("⚠️  Note: This may take a while due to GitHub API rate limits")
    print()
    
    # Target repository to check for plagiarism
    target_repo = "https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten"
    
    # Initialize detector
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  No GitHub token found. Search capabilities will be limited.")
        print("   Set GITHUB_TOKEN environment variable for better results.")
        print()
    
    detector = GitHubWidePlagiarismDetector(github_token=github_token)
    
    try:
        # Run GitHub-wide plagiarism detection
        print(f"🎯 Analyzing repository: {target_repo}")
        results = detector.detect_plagiarism_github_wide(target_repo)
        
        if "error" in results:
            print(f"❌ {results['error']}")
            return
        
        # Generate and save report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"github_wide_plagiarism_report_{timestamp}.txt"
        detector.generate_github_wide_report(results, report_file)
        
        # Save results as JSON for further analysis
        json_file = f"github_wide_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 JSON results saved to: {json_file}")
        
        # Print final summary
        print(f"\n🎯 GITHUB-WIDE PLAGIARISM DETECTION COMPLETE")
        print(f"Risk Level: {results['summary']['plagiarism_risk']}")
        print(f"Repositories Searched: {results['summary']['total_repositories_searched']}")
        print(f"Repositories Analyzed: {results['summary']['total_repositories_compared']}")
        print(f"Identical Files: {results['summary']['total_identical_files']}")
        print(f"Suspicious Matches: {results['summary']['total_suspicious_matches']}")
        
        if results['summary']['plagiarism_risk'] in ['HIGH', 'CRITICAL']:
            print(f"\n🚨 WARNING: {results['summary']['plagiarism_risk']} plagiarism risk detected!")
            print("Manual review of flagged repositories is strongly recommended.")
        
    except Exception as e:
        print(f"❌ Error during GitHub-wide plagiarism detection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

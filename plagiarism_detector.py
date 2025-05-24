#!/usr/bin/env python3
"""
Plagiarism Detection Tool
Analyzes GitHub repositories to detect potential code plagiarism
"""

import requests
import os
import json
import hashlib
import difflib
import re
from typing import Dict, List, Tuple, Set
from urllib.parse import urlparse
import time
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

class PlagiarismDetector:
    def __init__(self, github_token: str = None):
        """
        Initialize the plagiarism detector
        
        Args:
            github_token: GitHub personal access token for API access
        """
        self.github_token = github_token
        self.headers = {}
        if github_token:
            self.headers['Authorization'] = f'token {github_token}'
        
        # File extensions to analyze for code plagiarism
        self.code_extensions = {
            '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h',
            '.cs', '.php', '.rb', '.go', '.rs', '.swift', '.kt', '.scala',
            '.html', '.css', '.scss', '.sass', '.vue', '.svelte', '.dart',
            '.r', '.m', '.sql', '.sh', '.bash', '.ps1', '.yaml', '.yml',
            '.json', '.xml', '.md', '.txt', '.dockerfile', '.makefile'
        }
        
        # Minimum file size to consider (in characters)
        self.min_file_size = 50
        
        # Similarity threshold for flagging potential plagiarism
        self.similarity_threshold = 0.7

    def get_repo_info(self, repo_url: str) -> str:
        """Extract repository information from GitHub URL"""
        parsed = urlparse(repo_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) >= 2:
            owner = path_parts[0]
            repo = path_parts[1]
            return f"{owner}/{repo}"
        
        raise ValueError(f"Invalid GitHub repository URL: {repo_url}")

    def fetch_repo_contents(self, repo_url: str) -> RepoInfo:
        """
        Fetch repository contents from GitHub API
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            RepoInfo object containing repository data
        """
        try:
            repo_name = self.get_repo_info(repo_url)
            print(f"📥 Fetching repository: {repo_name}")
            
            api_url = f"https://api.github.com/repos/{repo_name}/contents"
            files = []
            
            def fetch_directory(url: str, path: str = ""):
                """Recursively fetch directory contents"""
                try:
                    response = requests.get(url, headers=self.headers)
                    if response.status_code == 403:
                        print(f"⚠️  Rate limit hit. Waiting 60 seconds...")
                        time.sleep(60)
                        response = requests.get(url, headers=self.headers)
                    
                    if response.status_code != 200:
                        print(f"❌ Failed to fetch {url}: {response.status_code}")
                        return
                    
                    items = response.json()
                    
                    for item in items:
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
                        
                        elif item['type'] == 'dir':
                            # Recursively fetch subdirectory
                            fetch_directory(item['url'], item['path'])
                
                except Exception as e:
                    print(f"❌ Error fetching directory {url}: {e}")
            
            fetch_directory(api_url)
            
            total_lines = sum(f.lines for f in files)
            
            return RepoInfo(
                url=repo_url,
                name=repo_name,
                files=files,
                total_files=len(files),
                total_lines=total_lines
            )
            
        except Exception as e:
            print(f"❌ Error fetching repository {repo_url}: {e}")
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

    def detect_plagiarism(self, target_repo: str, comparison_repos: List[str]) -> Dict:
        """
        Detect plagiarism between target repository and comparison repositories
        
        Args:
            target_repo: Repository URL to check for plagiarism
            comparison_repos: List of repository URLs to compare against
            
        Returns:
            Dictionary containing plagiarism analysis results
        """
        print(f"🔍 Starting plagiarism detection for: {target_repo}")
        print(f"📋 Comparing against {len(comparison_repos)} repositories")
        
        # Fetch target repository
        target_info = self.fetch_repo_contents(target_repo)
        if not target_info:
            return {"error": "Failed to fetch target repository"}
        
        print(f"✅ Target repo: {target_info.total_files} files, {target_info.total_lines} lines")
        
        results = {
            "target_repo": target_repo,
            "target_stats": {
                "files": target_info.total_files,
                "lines": target_info.total_lines
            },
            "comparisons": [],
            "suspicious_matches": [],
            "summary": {}
        }
        
        # Compare with each repository
        for repo_url in comparison_repos:
            print(f"\n🔄 Comparing with: {repo_url}")
            
            comparison_info = self.fetch_repo_contents(repo_url)
            if not comparison_info:
                print(f"❌ Failed to fetch: {repo_url}")
                continue
            
            print(f"✅ Comparison repo: {comparison_info.total_files} files, {comparison_info.total_lines} lines")
            
            # Compare files
            matches = []
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
                        
                        if similarity >= self.similarity_threshold:
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
                                    "repo": repo_url,
                                    "match": match
                                })
            
            avg_similarity = total_similarity / comparisons_made if comparisons_made > 0 else 0
            
            comparison_result = {
                "repo": repo_url,
                "repo_stats": {
                    "files": comparison_info.total_files,
                    "lines": comparison_info.total_lines
                },
                "matches": matches,
                "average_similarity": avg_similarity,
                "high_similarity_files": len(matches)
            }
            
            results["comparisons"].append(comparison_result)
            print(f"📊 Found {len(matches)} suspicious matches (avg similarity: {avg_similarity:.2f})")
        
        # Generate summary
        total_suspicious = len(results["suspicious_matches"])
        total_comparisons = len(results["comparisons"])
        
        results["summary"] = {
            "total_repositories_compared": total_comparisons,
            "total_suspicious_matches": total_suspicious,
            "plagiarism_risk": "HIGH" if total_suspicious > 5 else "MEDIUM" if total_suspicious > 2 else "LOW"
        }
        
        return results

    def generate_report(self, results: Dict, output_file: str = None):
        """
        Generate a detailed plagiarism report
        
        Args:
            results: Results from detect_plagiarism()
            output_file: Optional file to save the report
        """
        report = []
        report.append("=" * 80)
        report.append("PLAGIARISM DETECTION REPORT")
        report.append("=" * 80)
        report.append(f"Target Repository: {results['target_repo']}")
        report.append(f"Target Stats: {results['target_stats']['files']} files, {results['target_stats']['lines']} lines")
        report.append(f"Plagiarism Risk: {results['summary']['plagiarism_risk']}")
        report.append("")
        
        if results['suspicious_matches']:
            report.append("🚨 SUSPICIOUS MATCHES (>90% similarity):")
            report.append("-" * 50)
            for match in results['suspicious_matches']:
                report.append(f"Repository: {match['repo']}")
                report.append(f"  {match['match']['target_file']} → {match['match']['comparison_file']}")
                report.append(f"  Similarity: {match['match']['similarity']:.2%}")
                report.append(f"  Lines: {match['match']['target_lines']} vs {match['match']['comparison_lines']}")
                report.append("")
        
        report.append("📊 DETAILED COMPARISON RESULTS:")
        report.append("-" * 50)
        
        for comparison in results['comparisons']:
            report.append(f"Repository: {comparison['repo']}")
            report.append(f"  Files: {comparison['repo_stats']['files']}, Lines: {comparison['repo_stats']['lines']}")
            report.append(f"  Average Similarity: {comparison['average_similarity']:.2%}")
            report.append(f"  High Similarity Files: {comparison['high_similarity_files']}")
            
            if comparison['matches']:
                report.append("  Matches:")
                for match in comparison['matches'][:5]:  # Show top 5 matches
                    report.append(f"    {match['target_file']} ({match['similarity']:.2%})")
            report.append("")
        
        report.append("=" * 80)
        
        report_text = "\n".join(report)
        print(report_text)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"📄 Report saved to: {output_file}")

def main():
    """Main function to run plagiarism detection"""
    
    # Target repository to check for plagiarism
    target_repo = "https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten"
    
    # List of repositories to compare against (from wins.txt and local repos)
    comparison_repos = [
        "https://github.com/IdkwhatImD0ing/DispatchAI",
        # Add more repositories here as needed
    ]
    
    # Initialize detector
    # You can set a GitHub token for higher API rate limits
    github_token = os.getenv('GITHUB_TOKEN')
    detector = PlagiarismDetector(github_token=github_token)
    
    try:
        # Run plagiarism detection
        results = detector.detect_plagiarism(target_repo, comparison_repos)
        
        # Generate and save report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"plagiarism_report_{timestamp}.txt"
        detector.generate_report(results, report_file)
        
        # Save results as JSON for further analysis
        json_file = f"plagiarism_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 JSON results saved to: {json_file}")
        
    except Exception as e:
        print(f"❌ Error during plagiarism detection: {e}")

if __name__ == "__main__":
    main()

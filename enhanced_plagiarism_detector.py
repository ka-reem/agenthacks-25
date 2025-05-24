#!/usr/bin/env python3
"""
Enhanced Plagiarism Detection Tool
Analyzes GitHub repositories and local repositories to detect potential code plagiarism
"""

import requests
import os
import json
import hashlib
import difflib
import re
import glob
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
    is_local: bool = False

class EnhancedPlagiarismDetector:
    def __init__(self, config_file: str = "plagiarism_config.json", github_token: str = None):
        """
        Initialize the enhanced plagiarism detector
        
        Args:
            config_file: Path to configuration file
            github_token: GitHub personal access token for API access
        """
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        self.headers = {}
        if self.github_token:
            self.headers['Authorization'] = f'token {self.github_token}'
        
        # Load configuration
        self.load_config(config_file)
        
    def load_config(self, config_file: str):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            self.target_repo = config.get('target_repository', '')
            self.comparison_repos = config.get('comparison_repositories', [])
            settings = config.get('settings', {})
            
            self.code_extensions = set(settings.get('code_extensions', ['.py', '.js', '.ts']))
            self.min_file_size = settings.get('min_file_size', 50)
            self.similarity_threshold = settings.get('similarity_threshold', 0.7)
            
        except FileNotFoundError:
            print(f"⚠️  Config file {config_file} not found. Using defaults.")
            self.target_repo = "https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten"
            self.comparison_repos = ["https://github.com/IdkwhatImD0ing/DispatchAI"]
            self.code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp'}
            self.min_file_size = 50
            self.similarity_threshold = 0.7

    def scan_local_repositories(self, base_path: str = "./stolen-repos") -> List[str]:
        """
        Scan for local repositories in the stolen-repos directory
        
        Args:
            base_path: Base path to scan for repositories
            
        Returns:
            List of local repository paths
        """
        local_repos = []
        
        if os.path.exists(base_path):
            for item in os.listdir(base_path):
                repo_path = os.path.join(base_path, item)
                if os.path.isdir(repo_path) and item != "delete":
                    local_repos.append(repo_path)
                    print(f"📁 Found local repository: {repo_path}")
        
        return local_repos

    def fetch_local_repo_contents(self, repo_path: str) -> RepoInfo:
        """
        Fetch repository contents from local filesystem
        
        Args:
            repo_path: Path to local repository
            
        Returns:
            RepoInfo object containing repository data
        """
        try:
            print(f"📥 Scanning local repository: {repo_path}")
            files = []
            
            # Walk through all files in the repository
            for root, dirs, filenames in os.walk(repo_path):
                # Skip common non-code directories
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', 'env']]
                
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, repo_path)
                    file_ext = os.path.splitext(filename)[1].lower()
                    
                    # Only process code files
                    if file_ext in self.code_extensions:
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                            
                            if len(content) >= self.min_file_size:
                                file_info = FileInfo(
                                    path=relative_path,
                                    content=content,
                                    hash=hashlib.md5(content.encode()).hexdigest(),
                                    size=len(content),
                                    lines=len(content.splitlines())
                                )
                                files.append(file_info)
                        except Exception as e:
                            print(f"⚠️  Error reading file {file_path}: {e}")
            
            total_lines = sum(f.lines for f in files)
            
            return RepoInfo(
                url=repo_path,
                name=os.path.basename(repo_path),
                files=files,
                total_files=len(files),
                total_lines=total_lines,
                is_local=True
            )
            
        except Exception as e:
            print(f"❌ Error scanning local repository {repo_path}: {e}")
            return None

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
                total_lines=total_lines,
                is_local=False
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

    def detect_plagiarism_comprehensive(self) -> Dict:
        """
        Comprehensive plagiarism detection including local repositories
        
        Returns:
            Dictionary containing plagiarism analysis results
        """
        print(f"🔍 Starting comprehensive plagiarism detection")
        print(f"🎯 Target repository: {self.target_repo}")
        
        # Fetch target repository
        target_info = self.fetch_repo_contents(self.target_repo)
        if not target_info:
            return {"error": "Failed to fetch target repository"}
        
        print(f"✅ Target repo: {target_info.total_files} files, {target_info.total_lines} lines")
        
        # Scan for local repositories
        local_repos = self.scan_local_repositories()
        
        # Combine remote and local repositories
        all_comparison_repos = self.comparison_repos + local_repos
        
        results = {
            "target_repo": self.target_repo,
            "target_stats": {
                "files": target_info.total_files,
                "lines": target_info.total_lines
            },
            "comparisons": [],
            "suspicious_matches": [],
            "identical_files": [],
            "summary": {}
        }
        
        print(f"📋 Comparing against {len(all_comparison_repos)} repositories ({len(local_repos)} local)")
        
        # Compare with each repository
        for repo in all_comparison_repos:
            print(f"\n🔄 Comparing with: {repo}")
            
            # Determine if it's a local or remote repository
            if os.path.exists(repo):
                comparison_info = self.fetch_local_repo_contents(repo)
            else:
                comparison_info = self.fetch_repo_contents(repo)
            
            if not comparison_info:
                print(f"❌ Failed to fetch: {repo}")
                continue
            
            print(f"✅ Comparison repo: {comparison_info.total_files} files, {comparison_info.total_lines} lines")
            
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
                                "repo": repo,
                                "lines": target_file.lines
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
                                    "repo": repo,
                                    "match": match
                                })
            
            avg_similarity = total_similarity / comparisons_made if comparisons_made > 0 else 0
            
            comparison_result = {
                "repo": repo,
                "is_local": comparison_info.is_local,
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
            print(f"📊 Found {len(matches)} suspicious matches, {len(identical_matches)} identical files (avg similarity: {avg_similarity:.2f})")
        
        # Generate summary
        total_suspicious = len(results["suspicious_matches"])
        total_identical = len(results["identical_files"])
        total_comparisons = len(results["comparisons"])
        
        # Determine risk level
        if total_identical > 3 or total_suspicious > 10:
            risk_level = "CRITICAL"
        elif total_identical > 0 or total_suspicious > 5:
            risk_level = "HIGH"
        elif total_suspicious > 2:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"
        
        results["summary"] = {
            "total_repositories_compared": total_comparisons,
            "total_suspicious_matches": total_suspicious,
            "total_identical_files": total_identical,
            "plagiarism_risk": risk_level
        }
        
        return results

    def generate_detailed_report(self, results: Dict, output_file: str = None):
        """
        Generate a detailed plagiarism report
        
        Args:
            results: Results from detect_plagiarism_comprehensive()
            output_file: Optional file to save the report
        """
        report = []
        report.append("=" * 100)
        report.append("COMPREHENSIVE PLAGIARISM DETECTION REPORT")
        report.append("=" * 100)
        report.append(f"Target Repository: {results['target_repo']}")
        report.append(f"Target Stats: {results['target_stats']['files']} files, {results['target_stats']['lines']} lines")
        report.append(f"Plagiarism Risk: {results['summary']['plagiarism_risk']}")
        report.append(f"Analysis Date: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Summary section
        report.append("📊 SUMMARY:")
        report.append("-" * 50)
        report.append(f"Repositories Compared: {results['summary']['total_repositories_compared']}")
        report.append(f"Suspicious Matches (>70% similarity): {results['summary']['total_suspicious_matches']}")
        report.append(f"Identical Files (100% match): {results['summary']['total_identical_files']}")
        report.append("")
        
        # Identical files (most serious)
        if results['identical_files']:
            report.append("🚨 IDENTICAL FILES (100% match - CRITICAL):")
            report.append("-" * 70)
            for match in results['identical_files']:
                report.append(f"Repository: {match['repo']}")
                report.append(f"  {match['target_file']} → {match['comparison_file']}")
                report.append(f"  Lines: {match['lines']}")
                report.append("")
        
        # Suspicious matches
        if results['suspicious_matches']:
            report.append("⚠️  SUSPICIOUS MATCHES (>90% similarity):")
            report.append("-" * 70)
            for match in results['suspicious_matches']:
                report.append(f"Repository: {match['repo']}")
                report.append(f"  {match['match']['target_file']} → {match['match']['comparison_file']}")
                report.append(f"  Similarity: {match['match']['similarity']:.2%}")
                report.append(f"  Lines: {match['match']['target_lines']} vs {match['match']['comparison_lines']}")
                report.append("")
        
        report.append("📋 DETAILED COMPARISON RESULTS:")
        report.append("-" * 70)
        
        for comparison in results['comparisons']:
            repo_type = "LOCAL" if comparison['is_local'] else "REMOTE"
            report.append(f"Repository: {comparison['repo']} ({repo_type})")
            report.append(f"  Files: {comparison['repo_stats']['files']}, Lines: {comparison['repo_stats']['lines']}")
            report.append(f"  Average Similarity: {comparison['average_similarity']:.2%}")
            report.append(f"  High Similarity Files: {comparison['high_similarity_files']}")
            report.append(f"  Identical Files: {len(comparison['identical_files'])}")
            
            if comparison['identical_files']:
                report.append("  IDENTICAL FILES:")
                for match in comparison['identical_files']:
                    report.append(f"    {match['target_file']} = {match['comparison_file']}")
            
            if comparison['matches']:
                report.append("  HIGH SIMILARITY MATCHES:")
                for match in comparison['matches'][:5]:  # Show top 5 matches
                    report.append(f"    {match['target_file']} ({match['similarity']:.2%})")
            report.append("")
        
        report.append("=" * 100)
        
        report_text = "\n".join(report)
        print(report_text)
        
        if output_file:
            with open(output_file, 'w') as f:
                f.write(report_text)
            print(f"📄 Report saved to: {output_file}")

def main():
    """Main function to run comprehensive plagiarism detection"""
    
    print("🚀 Starting Enhanced Plagiarism Detection Tool")
    print("=" * 60)
    
    # Initialize detector with configuration
    detector = EnhancedPlagiarismDetector()
    
    try:
        # Run comprehensive plagiarism detection
        results = detector.detect_plagiarism_comprehensive()
        
        if "error" in results:
            print(f"❌ {results['error']}")
            return
        
        # Generate and save report
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        report_file = f"comprehensive_plagiarism_report_{timestamp}.txt"
        detector.generate_detailed_report(results, report_file)
        
        # Save results as JSON for further analysis
        json_file = f"plagiarism_results_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 JSON results saved to: {json_file}")
        
        # Print summary
        print(f"\n🎯 PLAGIARISM DETECTION COMPLETE")
        print(f"Risk Level: {results['summary']['plagiarism_risk']}")
        print(f"Suspicious Matches: {results['summary']['total_suspicious_matches']}")
        print(f"Identical Files: {results['summary']['total_identical_files']}")
        
    except Exception as e:
        print(f"❌ Error during plagiarism detection: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

# GitHub-Wide Plagiarism Detection Tool 🕵️‍♂️

This enhanced tool searches **across all of GitHub** to find repositories that might contain plagiarized code from your target repository. Unlike traditional tools that only compare against predefined repositories, this tool dynamically discovers potential matches by searching GitHub's entire ecosystem.

## 🌟 Key Features

### **GitHub-Wide Search**
- 🔍 **Intelligent Keyword Extraction**: Automatically extracts meaningful keywords from your repository
- 🌐 **Dynamic Repository Discovery**: Searches GitHub using multiple strategies to find similar repositories
- 📊 **Smart Ranking**: Prioritizes results by stars, relevance, and similarity
- 🚨 **Comprehensive Analysis**: Detects both identical files and high-similarity matches

### **Detection Modes**
1. **Basic Detection**: Compare against predefined repositories
2. **Enhanced Detection**: Include local repositories + GitHub
3. **GitHub-Wide Detection**: Search ALL of GitHub for similar code 🌟

## 📁 Files Overview

### Core Detection Scripts
- `github_wide_simple.py` - **Main GitHub-wide detector** (recommended)
- `enhanced_plagiarism_detector.py` - Enhanced version with local repo support
- `plagiarism_detector.py` - Basic detection for predefined repos
- `run_plagiarism_check.py` - Menu-driven runner script

### Configuration & Setup
- `plagiarism_config.json` - Configuration for predefined repositories
- `github_wide_config.json` - Settings for GitHub-wide search
- `requirements_plagiarism.txt` - Python dependencies

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install requests urllib3
```

### 2. (Optional) Set GitHub Token for Better Results
```bash
export GITHUB_TOKEN=your_github_token_here
```
*This increases API rate limits and improves search quality*

### 3. Run Detection
```bash
python3 run_plagiarism_check.py
```
Choose option **3** for GitHub-wide detection!

## 🔍 How GitHub-Wide Detection Works

### **Step 1: Target Analysis**
- Fetches your target repository: `https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten`
- Analyzes file names, directory structure, and code content
- Extracts meaningful keywords (function names, class names, unique identifiers)

### **Step 2: GitHub Search**
- Uses extracted keywords to search GitHub's repository database
- Employs multiple search strategies:
  - **Keyword-based search**: Uses extracted terms
  - **Language-based search**: Filters by detected programming language
  - **Fallback searches**: Uses domain-specific terms (e.g., "hackathon", "dispatch")

### **Step 3: Repository Analysis**
- Downloads and analyzes code from discovered repositories
- Compares file-by-file for similarities
- Uses advanced text matching algorithms to detect code reuse

### **Step 4: Risk Assessment**
- **CRITICAL**: Identical files found (100% match)
- **HIGH**: Multiple high-similarity matches (>80%)
- **MEDIUM**: Several moderate matches (>70%)
- **LOW**: Few or no significant matches

## 📊 Sample Output

```
🔍 GitHub-Wide Plagiarism Detection
==================================================
Target: https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten
🔑 Keywords: dispatch, emergency, server, main, socket

📋 Found 15 repositories for query: 'dispatch'
📋 Found 8 repositories for query: 'emergency' 
📊 Total unique repositories found: 23

🔄 [1/23] user/emergency-dispatch (⭐156)
🔄 [2/23] team/dispatch-system (⭐89)

🚨 IDENTICAL FILES FOUND:
  user/emergency-dispatch (⭐156)
    main.py = server/main.py
    
⚠️  SUSPICIOUS MATCHES:
  team/dispatch-system (⭐89)
    client/app.js → frontend/app.js (94%)

Risk Level: CRITICAL
```

## ⚡ Performance & Limitations

### **GitHub API Considerations**
- **Rate Limits**: 60 requests/hour without token, 5000/hour with token
- **Search Limits**: Limited to ~50 repositories per analysis to avoid rate limits
- **File Limits**: Analyzes up to 20 files per repository for efficiency

### **Detection Accuracy**
- **High Precision**: Focuses on meaningful code files (excludes generated files)
- **Smart Normalization**: Removes comments and formatting differences
- **Context Aware**: Compares files with similar extensions and names

## 🔧 Advanced Configuration

### Setting Up GitHub Token
1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `public_repo` scope
3. Set environment variable: `export GITHUB_TOKEN=your_token`

### Customizing Search
Edit `github_wide_config.json` to modify:
- Number of repositories to analyze
- Similarity thresholds
- File types to include
- Search keywords

## 🎯 Current Target

**Repository Being Analyzed**: `https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten`

This tool will search GitHub to find any repositories that contain similar or identical code to this target repository.

## 📈 Results & Reporting

The tool generates comprehensive reports including:
- **JSON Output**: Machine-readable results for further analysis
- **Detailed Text Report**: Human-readable summary with findings
- **Risk Assessment**: Clear categorization of plagiarism likelihood
- **Repository Metadata**: Stars, language, description of flagged repos

## 🚨 Important Notes

### **Ethical Use**
- This tool is for legitimate verification and educational purposes
- Always respect repository licenses and terms of service
- Consider false positives - similar code doesn't always mean plagiarism

### **Legal Considerations**
- Code similarity can occur naturally (common patterns, tutorials, libraries)
- Manual review is always recommended for flagged repositories
- Consider the context and licensing of discovered similarities

## 🔍 Example Workflow

1. **Run GitHub-wide detection**:
   ```bash
   python3 github_wide_simple.py
   ```

2. **Review results**:
   - Check for identical files (highest priority)
   - Investigate high-similarity matches
   - Consider repository context (stars, age, description)

3. **Manual verification**:
   - Visit flagged repositories
   - Compare code sections manually
   - Consider timing and context

## 🤝 Contributing

This tool can be extended with:
- Additional search strategies
- More sophisticated similarity algorithms
- Support for more programming languages
- Integration with git history analysis

---

**Ready to detect plagiarism across all of GitHub?** 🕵️‍♂️

Run `python3 run_plagiarism_check.py` and choose option 3!

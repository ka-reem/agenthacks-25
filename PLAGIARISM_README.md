# Plagiarism Detection Tool

This tool analyzes GitHub repositories to detect potential code plagiarism by comparing the target repository against multiple comparison repositories.

## Features

- 🔍 **GitHub Repository Analysis**: Fetches and analyzes code from GitHub repositories
- 📁 **Local Repository Scanning**: Scans local repositories in the `stolen-repos` directory
- 🧮 **Code Similarity Detection**: Uses advanced text similarity algorithms
- 📊 **Comprehensive Reporting**: Generates detailed reports with similarity scores
- ⚙️ **Configurable Settings**: Customizable similarity thresholds and file types
- 🚨 **Risk Assessment**: Categorizes plagiarism risk levels (LOW, MEDIUM, HIGH, CRITICAL)

## Files

### Core Scripts
- `plagiarism_detector.py` - Basic plagiarism detection for GitHub repositories
- `enhanced_plagiarism_detector.py` - Enhanced version with local repository support
- `run_plagiarism_check.py` - Simple runner script with menu options

### Configuration
- `plagiarism_config.json` - Configuration file for target and comparison repositories
- `requirements_plagiarism.txt` - Python dependencies

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements_plagiarism.txt
   ```

2. **Optional: Set GitHub Token** (for higher API rate limits):
   ```bash
   export GITHUB_TOKEN=your_github_token_here
   ```

3. **Configure Repositories** (optional):
   Edit `plagiarism_config.json` to modify target and comparison repositories.

## Usage

### Quick Start
```bash
python3 run_plagiarism_check.py
```

### Direct Execution

**Basic Detection** (GitHub only):
```bash
python3 plagiarism_detector.py
```

**Enhanced Detection** (GitHub + Local):
```bash
python3 enhanced_plagiarism_detector.py
```

## Configuration

The `plagiarism_config.json` file allows you to customize:

- **Target Repository**: The repository to check for plagiarism
- **Comparison Repositories**: List of repositories to compare against
- **Similarity Threshold**: Minimum similarity score to flag (default: 0.7)
- **File Extensions**: Code file types to analyze
- **Minimum File Size**: Minimum file size to consider (default: 50 characters)

## Output

The tool generates several output files:

1. **Text Report**: `comprehensive_plagiarism_report_TIMESTAMP.txt`
   - Human-readable summary of findings
   - Risk assessment and detailed matches

2. **JSON Results**: `plagiarism_results_TIMESTAMP.json`
   - Machine-readable results for further analysis
   - Complete similarity data

## Risk Levels

- **CRITICAL**: Multiple identical files or extensive similarities
- **HIGH**: Some identical files or many suspicious matches
- **MEDIUM**: Several suspicious matches
- **LOW**: Few or no suspicious matches

## Detection Features

### File Analysis
- Normalizes code by removing comments and whitespace
- Calculates similarity using sequence matching algorithms
- Identifies identical files using hash comparison
- Filters by file extension and minimum size

### Repository Sources
- **GitHub Repositories**: Fetched via GitHub API
- **Local Repositories**: Scanned from `stolen-repos` directory
- **Rate Limiting**: Handles GitHub API rate limits automatically

### Similarity Metrics
- **Normalized Comparison**: Removes formatting differences
- **Multiple Algorithms**: Uses difflib.SequenceMatcher
- **Threshold-based Flagging**: Configurable similarity thresholds

## Example Output

```
🚨 IDENTICAL FILES (100% match - CRITICAL):
Repository: ./stolen-repos/DispatchAI
  main.py → server/main.py
  Lines: 145

⚠️  SUSPICIOUS MATCHES (>90% similarity):
Repository: https://github.com/IdkwhatImD0ing/DispatchAI
  client/src/app.js → client/src/app.js
  Similarity: 94.50%
  Lines: 89 vs 92
```

## Troubleshooting

### GitHub API Rate Limits
- Set a GitHub personal access token to increase rate limits
- The tool automatically handles rate limiting with delays

### Large Repositories
- The tool may take time for large repositories
- Consider adjusting file size thresholds for faster processing

### Missing Dependencies
- Run `pip install requests urllib3` if installation fails
- Ensure Python 3.6+ is installed

## Advanced Usage

### Adding More Repositories
Edit `plagiarism_config.json` to add more comparison repositories:

```json
{
  "comparison_repositories": [
    "https://github.com/user1/repo1",
    "https://github.com/user2/repo2",
    "./local-repo-path"
  ]
}
```

### Custom File Types
Modify the `code_extensions` in configuration to analyze different file types:

```json
{
  "settings": {
    "code_extensions": [".py", ".js", ".ts", ".java", ".cpp"]
  }
}
```

## Current Configuration

**Target Repository**: `https://github.com/ka-reem/agenthacks-25/commits/stolen_rewritten`

**Comparison Repositories**:
- `https://github.com/IdkwhatImD0ing/DispatchAI`
- Local repositories in `stolen-repos/` directory

## Legal Notice

This tool is for educational and legitimate verification purposes only. Always respect repository licenses and terms of service when analyzing code.

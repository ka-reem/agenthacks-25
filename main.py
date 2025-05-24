import os
import subprocess
from dotenv import load_dotenv

load_dotenv()
print("Loaded environment variables from .env")

# Get environment variables
git_author_name = os.getenv("GIT_AUTHOR_NAME")
git_author_email = os.getenv("GIT_AUTHOR_EMAIL")
print(f"GIT_AUTHOR_NAME: {git_author_name}")
print(f"GIT_AUTHOR_EMAIL: {git_author_email}")

# Read the first URL from wins.txt
wins_file_path = "wins.txt"
print(f"Attempting to read from {wins_file_path}...")
if os.path.exists(wins_file_path):
    with open(wins_file_path, "r") as f:
        first_url = f.readline().strip()
    print(f"Read first URL from {wins_file_path}: {first_url}")
else:
    print(f"Warning: {wins_file_path} not found. Using placeholder repo_url.")
    first_url = None # Ensure first_url is defined

# Look for the text "GitHub Repo" - save the link to a variable
# This part requires parsing the webpage content, which is complex.
# For now, let's assume we have a way to get the repo URL.
# Placeholder for repo URL
repo_url = "https://github.com/IdkwhatImD0ing/DispatchAI" # Example, replace with actual logic
# if first_url: # Potentially use the URL from wins.txt if parsing logic was implemented
    # repo_url = first_url # Or parsed GitHub link from first_url
print(f"Using repository URL: {repo_url}")

# Extract repo name from URL to create a dynamic path
repo_name = repo_url.split("/")[-1]
clone_dir_parent = "stolen-repos"
clone_dir = os.path.join(clone_dir_parent, repo_name)
print(f"Repository will be cloned to: {clone_dir}")

# Create parent directory if it doesn't exist
if not os.path.exists(clone_dir_parent):
    os.makedirs(clone_dir_parent)
    print(f"Created directory: {clone_dir_parent}")

# Automatically clone the repo
if not os.path.exists(clone_dir):
    print(f"Cloning {repo_url} into {clone_dir}...")
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
    print("Clone successful.")
else:
    print(f"Directory {clone_dir} already exists. Skipping clone.")

# Change commit history (author/email)
print(f"Changing commit history in {clone_dir} to use Author: {git_author_name}, Email: {git_author_email}")
filter_branch_command = f"""git filter-branch --env-filter \'
export GIT_AUTHOR_NAME="{git_author_name}"
export GIT_AUTHOR_EMAIL="{git_author_email}"
export GIT_COMMITTER_NAME="{git_author_name}"
export GIT_COMMITTER_EMAIL="{git_author_email}"
\' --tag-name-filter cat -- --branches --tags"""
try:
    subprocess.run(filter_branch_command, shell=True, cwd=clone_dir, check=True, text=True, capture_output=True)
    print("Commit history (author/email) changed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Error during git filter-branch execution: {e}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")
    exit(1)


# Define your target repository URL
target_repo_url = "https://github.com/ka-reem/agenthacks-25"
print(f"Target repository URL: {target_repo_url}")

# Update remote origin to your repository
print(f"Updating remote origin in {clone_dir}...")
print("Removing existing remote \'origin\'...")
subprocess.run(["git", "remote", "remove", "origin"], cwd=clone_dir, check=True)
print(f"Adding new remote \'origin\' pointing to {target_repo_url}...")
subprocess.run(["git", "remote", "add", "origin", target_repo_url], cwd=clone_dir, check=True)
print("Remote \'origin\' updated successfully.")

# --- Add git filter-repo to change commit timestamps ---
print("Preparing to change commit timestamps using git filter-repo...")

filter_repo_commit_callback_script = '''\
import datetime

# Base timestamp for commit dates
base_time = datetime.datetime(2024, 6, 20, 10, 0, 0, tzinfo=datetime.timezone.utc)

# Attempt at an in-script counter for commit spacing
# This counter needs to be managed carefully if git-filter-repo re-initializes the script for each commit.
if "commit_process_counter" not in globals():
    globals()["commit_process_counter"] = 0
globals()["commit_process_counter"] += 1

new_commit_time = base_time + datetime.timedelta(minutes=globals()["commit_process_counter"] * 3)

timestamp = int(new_commit_time.timestamp())
offset_str = new_commit_time.strftime('%z')
if not offset_str: # Fallback for UTC if strftime('%z') is empty
    offset_str = "+0000"

# Ensure commit object is available in this scope (provided by git-filter-repo)
commit.author_date = f"{timestamp} {offset_str}".encode('utf-8')
commit.committer_date = f"{timestamp} {offset_str}".encode('utf-8')
'''

filter_repo_command = [
    "git", "filter-repo",
    "--commit-callback", filter_repo_commit_callback_script,
    "--force"  # Use --force if the repo has already been filtered (e.g. by filter-branch)
]

# Prepare environment for subprocess
env = os.environ.copy()

print(f"Running git filter-repo in {clone_dir} to adjust commit timestamps...")
# Ensure git-filter-repo is installed, or this will fail.
try:
    subprocess.run(filter_repo_command, cwd=clone_dir, check=True, env=env, text=True, capture_output=True)
    print("Commit timestamps changed successfully using git filter-repo.")
except FileNotFoundError:
    print("Error: git-filter-repo command not found. Please install it (e.g., \'pip install git-filter-repo\') and ensure it\'s in your PATH.")
    exit(1)
except subprocess.CalledProcessError as e:
    print(f"Error during git filter-repo execution: {e}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")
    exit(1)


# Force push to the new origin
print(f"Force pushing all branches and tags from {clone_dir} to {target_repo_url}...")
try:
    subprocess.run(["git", "push", "--force", "--all", "origin"], cwd=clone_dir, check=True, text=True, capture_output=True)
    print("Force push of all branches successful.")
    subprocess.run(["git", "push", "--force", "--tags", "origin"], cwd=clone_dir, check=True, text=True, capture_output=True) # Ensure tags are pushed
    print("Force push of tags successful.")
except subprocess.CalledProcessError as e:
    print(f"Error during git push: {e}")
    print(f"stdout: {e.stdout}")
    print(f"stderr: {e.stderr}")
    exit(1)

print(f"Successfully processed repository from {repo_url}.")
print(f"Modified history and pushed to {target_repo_url}.")
print(f"Final repository location: {clone_dir}")

import os
import subprocess
from dotenv import load_dotenv

load_dotenv()

# Get environment variables
git_author_name = os.getenv("GIT_AUTHOR_NAME")
git_author_email = os.getenv("GIT_AUTHOR_EMAIL")

# Read the first URL from wins.txt
with open("wins.txt", "r") as f:
    first_url = f.readline().strip()

# Look for the text "GitHub Repo" - save the link to a variable
# This part requires parsing the webpage content, which is complex.
# For now, let's assume we have a way to get the repo URL.
# Placeholder for repo URL
repo_url = "https://github.com/IdkwhatImD0ing/DispatchAI" # Example, replace with actual logic

# Extract repo name from URL to create a dynamic path
repo_name = repo_url.split("/")[-1]
clone_dir = os.path.join("stolen-repos", repo_name)

# Automatically clone the repo
if not os.path.exists(clone_dir):
    subprocess.run(["git", "clone", repo_url, clone_dir], check=True)
else:
    print(f"Directory {clone_dir} already exists. Skipping clone.")

# Change commit history
filter_branch_command = f"""git filter-branch --env-filter '
export GIT_AUTHOR_NAME="{git_author_name}"
export GIT_AUTHOR_EMAIL="{git_author_email}"
export GIT_COMMITTER_NAME="{git_author_name}"
export GIT_COMMITTER_EMAIL="{git_author_email}"
' --tag-name-filter cat -- --branches --tags"""

subprocess.run(filter_branch_command, shell=True, cwd=clone_dir, check=True)

# Define your target repository URL
target_repo_url = "https://github.com/ka-reem/agenthacks-25"

# Update remote origin to your repository
print(f"Updating remote origin to {target_repo_url}...")
subprocess.run(["git", "remote", "remove", "origin"], cwd=clone_dir, check=True)
subprocess.run(["git", "remote", "add", "origin", target_repo_url], cwd=clone_dir, check=True)

# --- Add git filter-repo to change commit timestamps ---
# NOTE: git-filter-repo must be installed for this to work (e.g., pip install git-filter-repo).

filter_repo_commit_callback_script = '''
import datetime

# Base timestamp for commit dates
base_time = datetime.datetime(2024, 6, 20, 10, 0, 0, tzinfo=datetime.timezone.utc)

# Attempt at an in-script counter for commit spacing
if "commit_process_counter" not in globals():
    globals()["commit_process_counter"] = 0
globals()["commit_process_counter"] += 1

new_commit_time = base_time + datetime.timedelta(minutes=globals()["commit_process_counter"] * 3)

timestamp = int(new_commit_time.timestamp())
offset_str = new_commit_time.strftime('%z')
if not offset_str: # Fallback for UTC if strftime('%z') is empty
    offset_str = "+0000"

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
# You might need to guide the user to install it: pip install git-filter-repo
subprocess.run(filter_repo_command, cwd=clone_dir, check=True, env=env)

# Force push to the new origin
print(f"Force pushing changes to {target_repo_url}...")
subprocess.run(["git", "push", "--force", "origin"], cwd=clone_dir, check=True)

print(f"Processed repo from {repo_url}, modified history, and pushed to {target_repo_url}. Location: {clone_dir}")

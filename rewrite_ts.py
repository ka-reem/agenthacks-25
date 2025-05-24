#!/usr/bin/env python3
import os
import subprocess
import random
import datetime
import pytz

# ── CONFIG ───────────────────────────────────────────────────────────────
NAME   = "Name"  # Your name
EMAIL  = "Email@example.com"
TZ     = pytz.timezone("US/Pacific")
START  = TZ.localize(datetime.datetime(2025, 5, 23, 12, 30))
END    = TZ.localize(datetime.datetime(2025, 5, 24, 11, 0))
# ─────────────────────────────────────────────────────────────────────────

def run(*args, **kwargs):
    return subprocess.run(args, check=True, **kwargs)

# 1) Figure out your current branch
branch = (
    subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True, check=True
    )
    .stdout.strip()
)
print(f"> Retiming branch: {branch}")

# 2) List all commits in order
res = subprocess.run(
    ["git", "rev-list", "--reverse", branch],
    capture_output=True, text=True, check=True
)
commits = [c for c in res.stdout.splitlines() if c]
print(f"> Found {len(commits)} commits to process")

# 3) Make an orphan branch
run("git", "checkout", "--orphan", "retimed")
run("git", "reset", "--hard")

# 4) Replay each commit
for i, old in enumerate(commits, start=1):
    # 4a) Restore that commit's tree
    run("git", "checkout", old, "--", ".")
    # 4b) Stage everything
    run("git", "add", ".")
    # 4c) Grab the original commit message
    msg = (
        subprocess.run(
            ["git", "log", "-1", "--format=%B", old],
            capture_output=True, text=True, check=True
        )
        .stdout.rstrip()
    )
    # Remove the specified URL from the commit message
    msg = msg.replace("https://github.com/IdkwhatImD0ing/DispatcherAI", "")

    # 4d) Calculate sequential PST time in your window
    total_seconds = int((END - START).total_seconds())
    # Ensure at least 1 second increment if there are more commits than seconds
    increment_seconds = max(1, total_seconds // len(commits)) if len(commits) > 0 else 0
    
    # Calculate current commit's time offset
    # (i-1) because enumerate starts at 1 and we want the first commit at START or slightly after
    current_offset_seconds = (i - 1) * increment_seconds
    
    # Ensure the offset does not exceed the total_seconds for the last commit
    # This handles cases where rounding might push the last commit slightly beyond END
    if i == len(commits): # For the last commit
        dt = END
    elif len(commits) == 1: # For a single commit
        dt = START # Or END, or middle, depending on desired behavior for one commit. Let's use START.
    else:
        dt = START + datetime.timedelta(seconds=current_offset_seconds)
        # Ensure dt does not exceed END
        if dt > END:
            dt = END

    date_str = dt.strftime("%Y-%m-%dT%H:%M:%S%z")
    # 4e) Commit with new env
    env = os.environ.copy()
    env.update({
        "GIT_AUTHOR_NAME": NAME,
        "GIT_AUTHOR_EMAIL": EMAIL,
        "GIT_COMMITTER_NAME": NAME,
        "GIT_COMMITTER_EMAIL": EMAIL,
        "GIT_AUTHOR_DATE": date_str,
        "GIT_COMMITTER_DATE": date_str,
    })
    run("git", "commit", "--allow-empty", "-m", msg, env=env)
    print(f"[{i}/{len(commits)}] {old[:7]} @ {date_str}")

# 5) Rename your new branch to main (or whatever you like)
run("git", "branch", "-M", branch)
print(f"✅ All done!  Your new branch ‘{branch}’ has 100% your commits, timestamped PST.")

# #!/usr/bin/env python3
# import os, random, datetime, pytz
# from git import Repo, Actor

# # 1. Configuration
# NAME  = "Kareem"
# EMAIL = "kareemalmond@gmail.com"
# TZ    = pytz.timezone("US/Pacific")
# START = TZ.localize(datetime.datetime(2025, 5, 23, 12, 30))
# END   = TZ.localize(datetime.datetime(2025, 5, 24, 11, 0))

# # 2. Open repo and collect commits
# repo = Repo(os.getcwd())
# assert not repo.bare
# commits = list(repo.iter_commits("HEAD", reverse=True))
# print(f"Found {len(commits)} commits to retime.")

# # 3. Create new orphan branch
# repo.git.checkout("--orphan", "retimed")
# # Remove any files from index
# repo.git.rm("-rf", "--cached", ".")
# # Clean working tree
# repo.git.reset("--hard")

# # 4. Prepare author object
# author = committer = Actor(NAME, EMAIL)

# # 5. Replay commits
# for idx, old in enumerate(commits, start=1):
#     # 5a. Check out the tree of that old commit
#     repo.git.checkout(old.hexsha, "--", ".")

#     # 5b. Stage everything
#     repo.index.add([item.a_path for item in repo.index.entries])

#     # 5c. Pick a random timestamp in your window
#     total_sec = int((END - START).total_seconds())
#     rand_sec   = random.randint(0, total_sec)
#     new_dt     = START + datetime.timedelta(seconds=rand_sec)
#     date_str   = new_dt.strftime("%Y-%m-%dT%H:%M:%S%z")

#     # 5d. Commit with the old message, new date
#     repo.index.commit(
#         message=old.message,
#         author=author,
#         committer=committer,
#         author_date=date_str,
#         commit_date=date_str
#     )
#     print(f"[{idx}/{len(commits)}] retimed commit {old.hexsha[:7]} → {date_str}")

# # 6. Rename branch to main (or whatever)
# repo.git.branch("-M", "main")
# print("✅ All done! New branch 'main' has ordered, randomized PST timestamps.")

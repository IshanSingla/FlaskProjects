
from fcntl import flock
from telnetlib import PRAGMA_HEARTBEAT
from github import Github
import os
from pprint import pprint

try:
    os.system("clear")
    g = Github('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')
    repo = g.get_repo("IshanSingla/IshanSingla")
    folk= repo.get_forks()
    print(folk)
    clones = repo.get_clones_traffic(per="day")
    views = repo.get_views_traffic(per="day")

    print(f"Repository has {clones['count']} clones out of which {clones['uniques']} are unique.")
    print(f"Repository has {views['count']} views out of which {views['uniques']} are unique.")
    branch = repo.get_branch(branch="master")
    status = repo.get_commit(sha=branch.commit.sha).create_status(
        state="success",
        target_url="https://www.induced.me",
        description="CI in Progress",
        context="Just testing..."
    )
    print(status)
except Exception as e:
    print(e)
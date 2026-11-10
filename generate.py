#!/usr/bin/env python3
"""
Generate backdated commits so the GitHub contribution graph shows >= 100 days.

Rules that matter:
  - 1 contribution per day per repo (multiple commits on the same day = still 1 square).
  - Commit author email MUST be an email verified on the GitHub account.
  - Commits must land on the default branch of a repo you own (or have push access to).

Usage:
  python3 generate.py             # default: 110 active days within the last 150 days
  python3 generate.py --days 120 --span 180
"""

import argparse
import os
import random
import subprocess
from datetime import datetime, timedelta

MESSAGES = [
    "chore: daily sync",
    "chore(log): update activity log",
    "docs: refresh notes",
    "refactor: tidy helper utilities",
    "fix: small edge case in parser",
    "test: add coverage notes",
    "chore: bump activity snapshot",
    "feat: extend activity tracker",
    "style: format logs",
    "perf: trim redundant work",
]

AUTHORS = [
    ("syfa01", "petualangsiti123@gmail.com"),
]


def run(cmd, env=None):
    subprocess.run(cmd, check=True, shell=True, env=env, stdout=subprocess.DEVNULL)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=110, help="number of distinct active days")
    ap.add_argument("--span", type=int, default=150, help="window size in days (ending today)")
    ap.add_argument("--seed", type=int, default=2026)
    args = ap.parse_args()

    random.seed(args.seed)
    name, email = AUTHORS[0]
    root = os.path.dirname(os.path.abspath(__file__))
    log_path = os.path.join(root, "activity.log")
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # pick distinct days inside the window, exclude today (we commit today separately)
    candidates = [today - timedelta(days=d) for d in range(1, args.span + 1)]
    picks = sorted(random.sample(candidates, min(args.days, len(candidates))))

    for idx, day in enumerate(picks, 1):
        # 1-3 commits per active day, different times
        n_commits = random.choice([1, 1, 1, 2, 3])
        for j in range(n_commits):
            ts = day + timedelta(hours=random.randint(8, 22), minutes=random.randint(0, 59))
            stamp = ts.strftime("%Y-%m-%d %H:%M:%S +0700")
            env = dict(os.environ,
                       GIT_AUTHOR_NAME=name,
                       GIT_AUTHOR_EMAIL=email,
                       GIT_COMMITTER_NAME=name,
                       GIT_COMMITTER_EMAIL=email,
                       GIT_AUTHOR_DATE=stamp,
                       GIT_COMMITTER_DATE=stamp)
            with open(log_path, "a") as f:
                f.write(f"{ts.isoformat()} | {random.choice(MESSAGES)} | day {idx:03d}\n")
            run("git add activity.log", env=env)
            run(f'git commit -m "{random.choice(MESSAGES)} [{ts:%Y-%m-%d}]"', env=env)

    print(f"done: {len(picks)} active days, last day {picks[-1].date() if picks else '-'}")


if __name__ == "__main__":
    main()

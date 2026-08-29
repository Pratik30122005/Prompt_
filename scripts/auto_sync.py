#!/usr/bin/env python3
"""
auto_sync.py — lightweight git watcher for Prompt_ project.

Behaviour:
  - Detects any file changes in the repo via `git status --porcelain`.
  - Stages all changes with `git add -A`.
  - Generates a short, descriptive commit message based on changed filenames.
  - Pushes the commit to the `auto-sync` branch on GitHub.

The `main` branch is NEVER touched by this script.
To promote auto-sync changes to main, open a Pull Request on GitHub.

Usage (one-shot mode):
    python3 scripts/auto_sync.py

Usage (continuous watch mode — runs every 60 seconds):
    python3 scripts/auto_sync.py --watch
"""

import subprocess
import sys
import shlex
import time
from datetime import datetime, timezone

BRANCH = "auto-sync"
WATCH_INTERVAL = 60  # seconds


def run(cmd: str, check=True):
    result = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
    if check and result.returncode != 0:
        print(f"[auto-sync] ERROR running: {cmd}\n{result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result.stdout.strip()


def get_changed_files():
    out = run("git status --porcelain")
    return [line[3:].strip() for line in out.splitlines() if line.strip()]


def make_message(files):
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not files:
        return ""
    if len(files) == 1:
        return f"auto-sync: update {files[0]} [{ts}]"
    shown = ", ".join(files[:2])
    extra = f" (+{len(files)-2} more)" if len(files) > 2 else ""
    return f"auto-sync: update {shown}{extra} [{ts}]"


def sync_once():
    # Make sure we're on the correct branch
    current = run("git branch --show-current")
    if current != BRANCH:
        run(f"git checkout {BRANCH}")

    files = get_changed_files()
    if not files:
        print("[auto-sync] No changes detected.")
        return False

    run("git add -A")
    msg = make_message(files)
    run(f'git commit -m "{msg}"')
    push_out = run(f"git push origin {BRANCH}")
    print(f"[auto-sync] ✅ Pushed: {msg}")
    if push_out:
        print(push_out)
    return True


def main():
    watch_mode = "--watch" in sys.argv
    if watch_mode:
        print(f"[auto-sync] Watch mode active (every {WATCH_INTERVAL}s). Ctrl+C to stop.")
        while True:
            try:
                sync_once()
            except Exception as e:
                print(f"[auto-sync] Error: {e}", file=sys.stderr)
            time.sleep(WATCH_INTERVAL)
    else:
        sync_once()


if __name__ == "__main__":
    main()

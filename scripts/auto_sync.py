import time
import subprocess
import os

def run(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True)

def auto_sync():
    print("Starting auto-sync daemon...")
    while True:
        try:
            # Check for changes
            status = run("git status --porcelain")
            if not status.stdout.strip():
                time.sleep(30)
                continue
                
            print("Changes detected. Syncing...")
            run("git add -A")
            
            # Generate descriptive message based on files changed
            diff = run("git diff --cached --name-status")
            if not diff.stdout.strip():
                time.sleep(30)
                continue
                
            files_changed = []
            for line in diff.stdout.strip().split('\n'):
                parts = line.split()
                if len(parts) >= 2:
                    action = parts[0]
                    file = parts[1]
                    action_map = {'M': 'Modified', 'A': 'Added', 'D': 'Deleted', 'R': 'Renamed'}
                    action_str = action_map.get(action[0], action)
                    files_changed.append(f"- {action_str}: {file}")
            
            files_list = ", ".join([parts.split(': ')[1] for parts in files_changed[:3]])
            if len(files_changed) > 3:
                files_list += " and others"
                
            msg = f"Auto-sync: {files_list}"
            
            run(f'git commit -m "{msg}" -m "Changes:\n{"\n".join(files_changed)}"')
            print(f"Committed: {msg}")
            
            # Push to auto-sync branch
            push_res = run("git push origin HEAD:auto-sync")
            if push_res.returncode == 0:
                print("Pushed to origin/auto-sync successfully.")
            else:
                print(f"Push failed: {push_res.stderr}")
                
            time.sleep(30)
            
        except Exception as e:
            print(f"Error in auto-sync: {e}")
            time.sleep(60)

if __name__ == "__main__":
    auto_sync()

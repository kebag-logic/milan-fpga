"""Count command-table sha256 pins that do not match the pinned file at each named commit.
Usage: python3 -I pin_staleness.py <repo> <commit>..."""
import hashlib, json, subprocess, sys

def walk(node, out):
    if isinstance(node, dict):
        for key, value in node.items():
            if isinstance(value, dict) and "sha256" in value and "/" in key or (isinstance(value, dict) and "sha256" in value and key.endswith((".py", ".sh"))):
                out[key] = value["sha256"]
            walk(value, out)
    elif isinstance(node, list):
        for value in node:
            walk(value, out)

repo = sys.argv[1]
for commit in sys.argv[2:]:
    table = json.loads(subprocess.run(["git", "-C", repo, "show", commit + ":ci/image/command-table.json"],
                                      capture_output=True, check=True).stdout)
    pins = {}
    walk(table, pins)
    stale, absent = [], []
    for path, want in sorted(pins.items()):
        got = subprocess.run(["git", "-C", repo, "show", commit + ":" + path], capture_output=True)
        if got.returncode:
            absent.append(path)
        elif hashlib.sha256(got.stdout).hexdigest() != want:
            stale.append(path)
    print(f"{commit}: pins {len(pins)} stale {len(stale)} absent {len(absent)}")
    print("  stale:", " ".join(stale))

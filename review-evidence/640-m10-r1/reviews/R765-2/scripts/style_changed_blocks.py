"""Run check_doc_style.analyze() on a page at two revisions and report the
findings present at NEW but not at OLD (i.e. findings the delta introduced).

Usage: python3 -I style_changed_blocks.py <repo> <old-rev> <new-rev> <page>...
"""
import subprocess
import sys
from pathlib import Path

repo, old, new, *pages = sys.argv[1:]
sys.path.insert(0, str(Path(repo) / "scripts"))
import check_doc_style as s  # noqa: E402


def show(rev, page):
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{page}"],
                          check=True, capture_output=True, text=True).stdout


total = 0
key = lambda f: (f.reason, f.text)
for page in pages:
    before = {}
    for f in s.analyze(show(old, page)):
        before[key(f)] = before.get(key(f), 0) + 1
    after = s.analyze(show(new, page))
    added = []
    for f in after:
        if before.get(key(f), 0):
            before[key(f)] -= 1
        else:
            added.append(f)
    total += len(added)
    print(f"{page}: {len(after)} at {new[:10]}, introduced {len(added)}")
    for f in added:
        print(f"   line {f.line}: {f.reason}: {f.text}")
print("introduced findings:", total)
sys.exit(1 if total else 0)

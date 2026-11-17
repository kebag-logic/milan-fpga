"""Plant the four bad-link mutants one at a time in a clean clone, run the
link/anchor gates on each, restore, and print the result.
usage: mutants.py <clone> <python-with-renderer> <same_page_anchors.py>"""
import subprocess, sys
from pathlib import Path

clone, py, same = Path(sys.argv[1]), sys.argv[2], sys.argv[3]
GATES = (["scripts/docs_check.py"], ["scripts/gen_toc.py", "--verify-anchors"], ["scripts/check_doc_paths.py"])
MUTANTS = (
    ("M0 unmutated head", None, None, None),
    ("M1 AGENTS.md cross-page anchor -> #23-batched-mergez", "AGENTS.md",
     "CONTRIBUTING.md#23-batched-merges", "CONTRIBUTING.md#23-batched-mergez"),
    ("M2 CONTRIBUTING.md same-page anchor -> #23-batched-mergez", "CONTRIBUTING.md",
     "(#23-batched-merges)", "(#23-batched-mergez)"),
    ("M3 CI_WORKFLOWS.md path ../../CONTRIBUTING.md -> ../CONTRIBUTING.md", "docs/testing/CI_WORKFLOWS.md",
     "(../../CONTRIBUTING.md#23-batched-merges)", "(../CONTRIBUTING.md#23-batched-merges)"),
    ("M4 CI_WORKFLOWS.md anchor -> #23-batched-mergez", "docs/testing/CI_WORKFLOWS.md",
     "CONTRIBUTING.md#23-batched-merges", "CONTRIBUTING.md#23-batched-mergez"),
    ("M5 AGENTS.md new 2.1 link (round 3) -> #21-the-issue-to-merge-lanez", "AGENTS.md",
     "CONTRIBUTING.md#21-the-issue-to-merge-lane)", "CONTRIBUTING.md#21-the-issue-to-merge-lanez)"),
)

def run(cmd):
    r = subprocess.run(cmd, cwd=clone, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).splitlines()

head = subprocess.run(["git", "rev-parse", "--short=8", "HEAD"], cwd=clone, capture_output=True, text=True).stdout.strip()
print(f"# Planted mutants on a clean clone at {head}; each restored before the next\n")
for title, page, old, new in MUTANTS:
    print(title)
    if page:
        path = clone / page
        text = path.read_text()
        assert old in text, (page, old)
        path.write_text(text.replace(old, new, 1))
    for g in GATES:
        rc, out = run([py, "-I", *g])
        hits = [l for l in out if "MISS" in l or "broken link" in l or "23-batched" in l][:3]
        print(f"  [{' '.join(g)}] rc={rc}")
        for l in hits or out[-1:]:
            print(f"      {l.strip()}")
    rc, out = run([py, "-I", same, ".", "CONTRIBUTING.md"])
    print(f"  [same_page_anchors.py CONTRIBUTING.md] rc={rc}")
    for l in out:
        print(f"      {l}")
    if page:
        subprocess.run(["git", "checkout", "-q", "--", page], cwd=clone, check=True)
dirty = subprocess.run(["git", "status", "--porcelain"], cwd=clone, capture_output=True, text=True).stdout
print(f"\nclean after restore: {len(dirty.splitlines())} changed path(s)")

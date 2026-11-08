"""For every Markdown page a merge touched, apply check_doc_style's analyze() at the
merge and at both parents; report each finding at the merge that neither parent has.
Usage: python3 -I merge_style_probe.py <repo> <merge> ; rc 1 on any new finding.
Control: --control plants a 12-word sentence on the first page and must report it."""
import subprocess, sys
from collections import Counter
from pathlib import Path

repo = Path(sys.argv[1]).resolve(); merge = sys.argv[2]; control = "--control" in sys.argv
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as cds  # noqa: E402

git = lambda *a: subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, check=True).stdout
p1, p2 = git("rev-parse", f"{merge}^1", f"{merge}^2").split()
pages = sorted(set(git("diff", "--name-only", p1, merge, "--", "*.md").split())
               | set(git("diff", "--name-only", p2, merge, "--", "*.md").split()))


def show(rev, page):
    r = subprocess.run(["git", "-C", str(repo), "show", f"{rev}:{page}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def keys(text):
    return Counter((f.reason, " ".join(f.text.split())) for f in cds.analyze(text))


new_total = 0
for i, page in enumerate(pages):
    head = show(merge, page)
    if control and i == 0:
        head += "\nOne two three four five six seven eight nine ten eleven twelve.\n"
    at_head, a, b = keys(head), keys(show(p1, page)), keys(show(p2, page))
    new = at_head - (a | b)
    for (reason, text), n in new.items():
        print(f"NEW {page}: {reason}: {text[:160]}")
    print(f"{page}: {sum(at_head.values())} at merge, {sum(a.values())} at ^1, {sum(b.values())} at ^2, {sum(new.values())} new")
    new_total += sum(new.values())
print(f"merge style probe: {len(pages)} page(s), {new_total} new finding(s) [{p1[:8]} + {p2[:8]} -> {merge[:8]}]")
sys.exit(1 if new_total else 0)

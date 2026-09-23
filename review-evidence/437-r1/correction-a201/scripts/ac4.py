#!/usr/bin/env python3
"""Acceptance 4: the per-page classification of every tracked Markdown page,
under the base walk and the working-tree walk, on the base, live dev and
working trees. Compared: refusals, blocks, line_kinds, headings with
anchors, plan, existing() and generated_block."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import walks

CLONE = walks.CLONE
BASE = "574c29fa111c74e5e5ed63e4670aff1f492e28e2"
DEV = "ede8d48ecd7c7f589a14b957951f040d92c99c70"
RUNNER = r"""
import json, sys
sys.path.insert(0, sys.argv[1])
import gen_toc
pages = json.load(sys.stdin)
out = {}
for name, text in pages.items():
    rec = {"refusals": gen_toc.refusals(text), "blocks": gen_toc.blocks(text),
           "line_kinds": gen_toc.line_kinds(text), "headings": gen_toc.headings(text)}
    for fn in ("plan", "existing", "generated_block"):
        try:
            rec[fn] = repr(getattr(gen_toc, fn)(text))
        except Exception as exc:
            rec[fn] = "error " + type(exc).__name__
    out[name] = rec
json.dump(out, sys.stdout)
"""


def pages_at(rev):
    if rev == "work":
        names = subprocess.run(["git", "-C", str(CLONE), "ls-files", "*.md"], capture_output=True, text=True, check=True).stdout.split()
        return {n: (CLONE / n).read_text(encoding="utf-8") for n in names if (CLONE / n).is_file()}
    names = subprocess.run(["git", "-C", str(CLONE), "ls-tree", "-r", "--name-only", rev], capture_output=True, text=True, check=True).stdout.split("\n")
    out = {}
    for n in names:
        if n.endswith(".md"):
            blob = subprocess.run(["git", "-C", str(CLONE), "show", f"{rev}:{n}"], capture_output=True, check=True).stdout
            out[n] = blob.decode("utf-8")
    return out


def run(walk_rev, pages):
    res = subprocess.run([sys.executable, "-I", "-B", "-c", RUNNER, str(walks.tree(walk_rev))],
                         input=json.dumps(pages), capture_output=True, text=True, check=True)
    return json.loads(res.stdout)


def main():
    summary = []
    for tree in (BASE, DEV, "work"):
        pages = pages_at(tree)
        a, b = run(BASE, pages), run("work", pages)
        diff = sorted(n for n in pages if a[n] != b[n])
        digest = hashlib.sha256(json.dumps(a, sort_keys=True).encode()).hexdigest()
        summary.append({"tree": tree, "pages": len(pages), "differing": diff, "base_walk_digest": digest})
        print(tree, len(pages), "pages;", len(diff), "differ", diff[:5], "base-walk digest", digest[:16])
    Path(sys.argv[1]).write_text(json.dumps(summary, indent=1) + "\n")


if __name__ == "__main__":
    main()

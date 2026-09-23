#!/usr/bin/env python3
"""For each surviving mutant copy, find corpus pages where the mutant walk
and the head walk list different headings, render those pages with GitHub,
and report who agrees with the rendering. Extra pages may be added.

Usage: survivor_impact.py <head-scripts> <cache> <out.json> <corpus.json>... -- <mutant-dir>...
"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXTRA = [
    "text <!-- c\nmore -->\n<span>\n## Old\n\n## Real\n",
    "- a <!-- c\n  more -->\n  <span>\n## Old\n  </span>\n\n## Real\n",
    "- a\n\n  b <!-- c\n  -->\n<span>\n## Old\n</span>\n\n## Real\n",
    "text\n    <!-- c\n-->\n<span>\n## Old\n\n## Real\n",
    "- [a]: /u x\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
    "- [a]: /u x\n\n\n  ```\n## Old\n```\n\n## Real\n",
    "- [a]: /u \"t\" x\n\n\n  text\n<span>\n## Old\n</span>\n\n## Real\n",
    "[^1]: a\n  \n    b\n<span>\n## Old\n</span>\n\n## Real\n",
    "[^1]: a\n \n    ```\n## Old\n```\n\n## Real\n",
    "[^1]: a\n    \n    b\n<span>\n## Old\n</span>\n\n## Real\n",
    "[^1]: a\n\t\n    b\n<span>\n## Old\n</span>\n\n## Real\n",
]


def walk(scripts: str, pages: list) -> list:
    p = subprocess.run([sys.executable, "-B", str(HERE / "walk_worker.py"), scripts],
                       input=json.dumps(pages).encode(), capture_output=True, check=True)
    return [a["headings"] for a in json.loads(p.stdout)]


def main() -> int:
    sep = sys.argv.index("--")
    head, cache, out = sys.argv[1:4]
    corpora, mutants = sys.argv[4:sep], sys.argv[sep + 1:]
    pages = list(EXTRA)
    for c in corpora:
        pages += [r["page"] for r in json.loads(Path(c).read_text())]
    pages = list(dict.fromkeys(pages))
    h = walk(head, pages)
    report = {}
    for m in mutants:
        mw = walk(m, pages)
        idx = [i for i, (a, b) in enumerate(zip(h, mw)) if a != b]
        rp = subprocess.run([sys.executable, "-B", str(HERE / "render.py"), cache],
                            input=json.dumps([pages[i] for i in idx]).encode(), capture_output=True, check=False)
        rend = json.loads(rp.stdout) if idx else []
        rows = []
        for i, rec in zip(idx, rend):
            gh = rec["headings"] if rec["exit"] == 0 else None
            rows.append({"page": pages[i], "github": gh, "head": h[i], "mutant": mw[i],
                         "head_agrees": gh == h[i], "mutant_agrees": gh == mw[i],
                         "mutant_escape": gh is not None and any(x not in gh for x in mw[i])})
        report[Path(m).name] = rows
        print(f"{Path(m).name}: {len(pages)} pages, mutant differs from head on {len(idx)}; "
              f"head agrees with GitHub on {sum(r['head_agrees'] for r in rows)}, "
              f"mutant agrees on {sum(r['mutant_agrees'] for r in rows)}, "
              f"mutant lists a heading GitHub hides on {sum(r['mutant_escape'] for r in rows)}")
        for r in rows[:4]:
            print("   e.g.", repr(r["page"]), "gh", r["github"], "head", r["head"], "mutant", r["mutant"])
    Path(out).write_text(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Check every draft block (a)-(h) appears verbatim at HEAD, and that the
commit's added/removed lines are exactly the draft's.  usage: <draft> <repo> <base>"""
import re, subprocess, sys
from pathlib import Path
draft, repo, base = Path(sys.argv[1]).read_text(), Path(sys.argv[2]), sys.argv[3]
FILE = {"a": "CONTRIBUTING.md", "b": "CONTRIBUTING.md", "c": "CONTRIBUTING.md", "d": "AGENTS.md",
        "e": "AGENTS.md", "f": "AGENTS.md", "g": "AGENTS.md", "h": "docs/testing/CI_WORKFLOWS.md"}
blocks = {}
for m in re.finditer(r"\*\*\((\w)\)[^\n]*\n\n(`{3,4})(\w*)\n(.*?)\n\2\n", draft, re.S):
    blocks[m.group(1)] = (m.group(3), m.group(4))
want_add, want_del, bad = {}, {}, 0
for k in sorted(FILE):
    lang, body = blocks[k]
    text = (repo / FILE[k]).read_text()
    if lang == "diff":
        add = [l[1:] for l in body.splitlines() if l.startswith("+")]
        dele = [l[1:] for l in body.splitlines() if l.startswith("-")]
        ctx = [l[1:] for l in body.splitlines() if l.startswith(" ")]
        new = "\n".join(add)
        ok = new in text and all(c in text for c in ctx) and not any(d in text.splitlines() for d in dele)
    else:
        add, dele = body.splitlines(), []
        ok = body in text
    want_add.setdefault(FILE[k], []).extend(l for l in add if l.strip())
    want_del.setdefault(FILE[k], []).extend(dele)
    bad += not ok
    print(f"({k}) {FILE[k]}: {'VERBATIM' if ok else 'MISMATCH'} ({len(add)} added, {len(dele)} removed line(s) in draft)")
for f in sorted(set(FILE.values())):
    d = subprocess.run(["git", "-C", str(repo), "diff", "-U0", base, "HEAD", "--", f], capture_output=True, text=True, check=True).stdout
    got_add = [l[1:] for l in d.splitlines() if l.startswith("+") and not l.startswith("+++") and l[1:].strip()]
    got_del = [l[1:] for l in d.splitlines() if l.startswith("-") and not l.startswith("---")]
    same = sorted(got_add) == sorted(want_add[f]) and sorted(got_del) == sorted(want_del[f])
    bad += not same
    print(f"{f}: commit adds {len(got_add)} non-blank / removes {len(got_del)} line(s); equals draft: {same}")
print("RESULT", "PASS" if not bad else "FAIL")
sys.exit(1 if bad else 0)

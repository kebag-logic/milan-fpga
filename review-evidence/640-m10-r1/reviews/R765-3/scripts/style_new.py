"""List check_doc_style.analyze() findings present at HEAD but absent at a base,
compared by (reason, normalized text), for the given pages.

usage: python3 -I -B style_new.py <repo> <base> <page>...   (rc 1 on any new finding)
"""
import subprocess, sys
from pathlib import Path

repo, base, pages = Path(sys.argv[1]).resolve(), sys.argv[2], sys.argv[3:]
sys.path.insert(0, str(repo / "scripts"))
import check_doc_style as cds  # noqa: E402

def keyset(text):
    return {(f.reason, " ".join(f.text.split())): f.line for f in cds.analyze(text)}

total = 0
for page in pages:
    head = (repo / page).read_text(encoding="utf-8")
    old = subprocess.run(["git", "-C", str(repo), "show", f"{base}:{page}"],
                         capture_output=True, text=True, check=True).stdout
    h, o = keyset(head), keyset(old)
    new = [(ln, k) for k, ln in h.items() if k not in o]
    for ln, (reason, text) in sorted(new):
        print(f"{page}:{ln}: {reason}: {text[:160]}")
    print(f"{page}: head findings {len(h)}, base findings {len(o)}, new {len(new)}")
    total += len(new)
sys.exit(1 if total else 0)

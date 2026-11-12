#!/usr/bin/env python3
"""Copy the lane's measurements into receipts/, host paths replaced by names (lane 895 helper)."""
import re, subprocess, sys
from pathlib import Path
O = Path("$MANAGEMENT/2026-09-23/895-a775/receipts")
T = Path("/data-2/milan/tmp/895-a775")
SUBS = [(str(T), "<scratch>"), ("/data-2/milan/tmp/665s2b-a683zm/builds", "<round 28 builds>"),
        ("$LANES/895-talker", "<lane>"), ("$LANES/665-s2b-cycles", "<the #810 lane>"),
        ("$WORKSPACE_HOME", "<home>")]
def scrub(text):
    for a, b in SUBS:
        text = text.replace(a, b)
    return text
def put(rel, text):
    p = O / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(scrub(text))
def read(p):
    p = Path(p); return p.read_text() if p.exists() else ""
for t, img in (("base", "img-base"), ("head", "img-h3"), ("merge", "img-m3")):
    put(f"rom/images-{t}.md", read(T / f"{img}/HEAD.txt") + read(T / f"{img}.txt"))
    put(f"rom/refused-8x8-if2-{t}.txt", "".join(l for f in sorted((T / img).glob("*-8x8-if2.log"))
                                                for l in read(f).splitlines(True) if "REFUSED" in l))
for t, k in (("base", "keyed-base.log"), ("head", "keyed-h3.log"), ("merge", "keyed-m3.log")):
    put(f"rom/platform-8x8-if2-keyed-{t}.txt", "".join(l for l in read(T / k).splitlines(True) if "REFUSED" in l))
put("rom/merge-commits.txt", subprocess.run(["git", "-C", str(T / "m3"), "log", "--oneline", "-3"],
                                             capture_output=True, text=True).stdout)
put("tests/suites-at-head.txt", "".join(l for l in read(T / "arms-h3.log").splitlines(True)
                                        if l.startswith("[") or "verdict" in l or "tsn-c-stack" in l))
for run in ("v3-t2", "v3-t1", "v3-p2", "v3-p1", "v3-c"):
    out = []
    for f in sorted((T / run).rglob("*.log")):
        fails = [l for l in read(f).splitlines() if "[FAIL]" in l][:3]
        out.append(f"== {f.stem}\n" + "\n".join(fails) + "\n")
    put(f"plants/{run}.txt", "".join(out))
# the index, from the files present
rows = [f"| `{p.relative_to(O)}` | {p.stat().st_size} |" for p in sorted(O.rglob("*")) if p.is_file() and p.name != "INDEX.md"]
(O / "INDEX.md").write_text("# Receipts index (generated from the files present)\n\n| File | Bytes |\n|---|---:|\n" +
                            "\n".join(rows) + "\n")
big = [p for p in O.rglob("*") if p.is_file() and p.stat().st_size > 200_000]
hosts = [p for p in O.rglob("*") if p.is_file() and re.search(r"/data-2/|$VALIDATION_STORAGE|$WORKSPACE_HOME", p.read_text(errors="ignore"))]
print("files", len(rows), "over 200 KB", big, "with host paths", hosts)

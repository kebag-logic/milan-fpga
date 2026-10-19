"""Scan the comment lines a diff adds (C/C++/SV '//', Python/Make/shell '#') for bench
check labels; prints each hit. usage: r2_label_scan.py <repo> <base> [<head>]"""
import re, subprocess, sys
repo, base = sys.argv[1], sys.argv[2]
head = sys.argv[3] if len(sys.argv) > 3 else None
args = ["git", "-C", repo, "diff", "-U0", base] + ([head] if head else []) + ["--", "hdl", "tb", "scripts"]
diff = subprocess.run(args, capture_output=True, text=True, check=True).stdout
LABEL = re.compile(r"\b(RDC\d+[a-z]?|RC\d|LK\d+[a-z]?|LN\d?|LF\d?[a-z]?|LC\d|L5b|L6d|L3b?|TD1|RN|AX|P12|CQ\d?|OC\d?|DR\d?|SC\d)\b")
path = None; hits = 0; seen = 0
for line in diff.splitlines():
    if line.startswith("+++ "):
        path = line[6:]
        continue
    if not line.startswith("+") or line.startswith("+++"):
        continue
    text = line[1:]
    if path.endswith((".md", ".json", ".patch", ".vlt")):
        continue
    m = re.search(r"(//!?|#)(.*)$", text)
    if not m:
        continue
    comment = m.group(2)
    # skip string literals: the '#'/'//' must not sit inside quotes
    before = text[:m.start()]
    if before.count('"') % 2 == 1 or before.count("'") % 2 == 1:
        continue
    seen += 1
    for h in LABEL.finditer(comment):
        hits += 1
        print(f"{path}: {h.group(0)}: {text.strip()[:110]}")
print(f"added comment lines scanned: {seen}; label hits: {hits}")

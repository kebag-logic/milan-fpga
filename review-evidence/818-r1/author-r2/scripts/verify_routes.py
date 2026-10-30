"""(#818 round 2) verify_routes.py <route-reports.tsv> <set>=<root>...: check every recorded report's size and sha256."""
import hashlib
from pathlib import Path
import sys

tsv, *roots = sys.argv[1:]
base = dict(root.split("=", 1) for root in roots)
good = bad = 0
for line in Path(tsv).read_text().splitlines()[1:]:
    route_set, sub, report, size, sha = line.split("\t")
    path = Path(base[route_set]) / sub / report
    data = path.read_bytes() if path.is_file() else b""
    if len(data) == int(size) and hashlib.sha256(data).hexdigest() == sha:
        good += 1
    else:
        bad += 1
        print("MISMATCH", route_set, sub, report)
print(f"route reports: {good} match, {bad} mismatch")
sys.exit(1 if bad else 0)

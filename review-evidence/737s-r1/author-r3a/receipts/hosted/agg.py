"""Per-run aggregate span, its checkout step, and the depth-1 checkouts of the watcher and tail jobs (#737 round 3)."""
import json, sys
from datetime import datetime as D
from pathlib import Path

def t(s):
    return D.fromisoformat(s.replace("Z", "+00:00")).timestamp()

for path in sys.argv[1:]:
    jobs = json.loads(Path(path).read_text())["jobs"]
    print("==", Path(path).stem)
    for j in sorted(jobs, key=lambda j: j["name"]):
        if j["name"] not in ("elaborate", "Fail fast across this head", "Cancel late CI failures", "Collect CI manifest"):
            continue
        if not j["started_at"] or not j["completed_at"]:
            print("  ", j["name"], "incomplete"); continue
        span = t(j["completed_at"]) - t(j["started_at"])
        co = [st for st in j["steps"] if st["name"].startswith("Run actions/checkout")]
        cos = (t(co[0]["completed_at"]) - t(co[0]["started_at"])) if co and co[0]["completed_at"] and co[0]["started_at"] else None
        print(f"  {j['name']:28} {j['conclusion']:10} span {span:5.0f} checkout {cos if cos is None else round(cos)} {co[0]['conclusion'] if co else ''} less-checkout {span - (cos or 0):5.0f}")

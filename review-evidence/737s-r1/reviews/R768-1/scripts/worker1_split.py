#!/usr/bin/env python3
"""For elaborate-gates-1 in saved GitHub jobs JSON: seconds before the LiteX aggregate step,
the step itself, after it, the builder step, and the job outside the two gate steps."""
import json, sys
from datetime import datetime
def t(s): return datetime.fromisoformat(s.replace("Z", "+00:00"))
for path in sys.argv[1:]:
    for job in json.load(open(path))["jobs"]:
        if job["name"] != "elaborate-gates-1": continue
        s, e = t(job["started_at"]), t(job["completed_at"])
        lit = next(x for x in job["steps"] if x["name"].startswith("Standalone LiteX"))
        bld = next(x for x in job["steps"] if x["name"].startswith("Elaboration gates, leg"))
        ls, le = t(lit["started_at"]), t(lit["completed_at"])
        bd = (t(bld["completed_at"]) - t(bld["started_at"])).total_seconds()
        pre = (ls - s).total_seconds(); post = (e - le).total_seconds(); ld = (le - ls).total_seconds()
        print(f"{path}: job {(e-s).total_seconds():.0f} pre-LiteX {pre:.0f} LiteX {ld:.0f} ({lit['conclusion']}) "
              f"post {post:.0f} builder {bd:.0f} job-less-LiteX {pre+post:.0f} outside-gates {pre+post-bd:.0f}")

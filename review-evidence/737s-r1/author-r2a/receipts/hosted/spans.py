"""Job spans of one run relative to its run_started_at (#737 round 2)."""
import json, sys
from datetime import datetime as D
t = lambda s: D.fromisoformat(s.replace("Z", "+00:00")).timestamp()
jobs = json.load(open(sys.argv[1]))["jobs"]
r0 = t(sys.argv[2])
for x in jobs:
    print(f"{x['name']:26} created+{t(x['created_at']) - r0:5.0f} start+{t(x['started_at']) - r0:5.0f}"
          f" end+{t(x['completed_at']) - r0:5.0f}")

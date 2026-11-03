#!/usr/bin/env python3
"""Per-job queue, execution and offset seconds from a saved GitHub Actions jobs API response.
Usage: job_timing.py <jobs.json>.  exec_s runs from the first step start to job completion
(the runner's own span); queued_s from job creation to the first step start."""
import json, sys, datetime as d
p = lambda s: d.datetime.fromisoformat(s.replace('Z', '+00:00')) if s else None
jobs = json.load(open(sys.argv[1]))['jobs']
rows = []
for j in jobs:
    st = [p(s['started_at']) for s in j['steps'] if s.get('started_at')]
    rows.append((j['name'], j['conclusion'], p(j['created_at']), min(st) if st else None, p(j['completed_at']), j))
t0 = min(r[3] for r in rows if r[3])
print('head_sha', jobs[0]['head_sha'], 'run', jobs[0]['run_id'], 'attempt', jobs[0]['run_attempt'])
for n, c, cr, a, b, j in rows:
    f = lambda x: '-' if x is None else str(int(x))
    print(f"{n:28} {str(c):9} queued_s={f((a-cr).total_seconds() if a else None):>5} exec_s={f((b-a).total_seconds() if a and b else None):>5} "
          f"start+={f((a-t0).total_seconds() if a else None):>5} end+={f((b-t0).total_seconds() if b else None):>5}")
    for s in j['steps']:
        sa, sb = p(s.get('started_at')), p(s.get('completed_at'))
        if sa and sb and (sb - sa).total_seconds() >= 60:
            print(f"      {int((sb-sa).total_seconds()):5} s  {s['conclusion']:8} {s['name']}")

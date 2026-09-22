#!/usr/bin/env python3
"""Capture completed hosted job logs as raw files; do not render control codes."""
import concurrent.futures
import json
from collect import OUT,DONOR,capture

jobs=[]
for run in [35772531911,35772526304]:
    v=json.loads((OUT/f'public/hosted-{run}-jobs.json').read_text())
    for j in v['jobs']:
        if j['status']=='completed': jobs.append((run,j))
def fetch(entry):
    run,j=entry
    b=capture(f'public/hosted-{run}-{j["name"]}.raw.log',
              ['gh','api','--allow-escape-sequences',f'repos/{DONOR}/actions/jobs/{j["id"]}/logs'])
    return (run,j['name'],len(b))
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for row in pool.map(fetch,jobs): print(*row)

#!/usr/bin/env python3
"""Compare reviewer reruns (result.json or run.py receipts) with the published round-2 receipts.

Usage: compare_runs.py <author-receipts-dir> <label>=<rerun-json> ...
Label is the published receipt stem, e.g. round2-1x1-queued-input.
"""
import json, sys
from pathlib import Path
auth = Path(sys.argv[1])
ok = True
for arg in sys.argv[2:]:
    label, path = arg.split('=', 1)
    a, m = json.loads((auth / (label + '.json')).read_text()), json.loads(Path(path).read_text())
    same = {k: a[k] == m[k] for k in ('log_sha256', 'rows', 'heartbeat', 'liveness', 'budget_findings')}
    ok &= all(same.values())
    print(label, same, 'findings:', m['budget_findings'])
sys.exit(0 if ok else 1)

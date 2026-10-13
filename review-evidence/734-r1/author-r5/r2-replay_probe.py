#!/usr/bin/env python3
"""Run the unchanged review probe with explicit source revisions, then grade its JSON."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys

probe, repo, work, head = sys.argv[1:]
spec = importlib.util.spec_from_file_location('review_probe', probe)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
original_head = module.HEAD
module.HEAD = head
module.PARENT = original_head
sys.argv = [probe, repo, work]
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    assert module.main() == 0
raw = buf.getvalue()
print(raw, end='')
rows = [json.loads(line) for line in raw.splitlines()]
checked = 0
for row in rows:
    if row.get('bodies') != 'head':
        continue
    assert row['rc'] == 0, row
    if row['case'].startswith('B16 hosted'):
        assert row['rtl'] == 'false' and row['n'] == 2, row
    else:
        assert row['rtl'] == 'true' and 'hdl/x.sv' in row['files'], row
    checked += 1
assert checked == 9, checked
print(json.dumps({'graded': checked, 'result': 'PASS', 'head': head,
                  'parent': original_head,
                  'probe_sha256': hashlib.sha256(Path(probe).read_bytes()).hexdigest()}))

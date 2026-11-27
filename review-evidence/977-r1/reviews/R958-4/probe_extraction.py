#!/usr/bin/env python3
"""Falsify per-record coverage of the published extractor using queued receive marks."""
import contextlib
import io
import json
import runpy
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

root = Path(sys.argv[1]).resolve()
packet = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import grade
import poll_grade

extractor = packet / 'published/deliv12.py.txt'
marks = ''.join(f'MARK 9000 srp.register_burst.t0.r{r}.if0\n' for r in range(3))
receives = ''.join(f'RXC {cycle} 4\n' for cycle in (10000, 20000, 30000))
bases = [(k * 10000, 1000 if k == 6 else 10) for k in range(1, 31)]
sections = [(start, start + cost, start) for start, cost in bases]
with tempfile.TemporaryDirectory(dir=packet / 'scratch') as tmp:
    path = Path(tmp) / 'queued.log'
    path.write_text(marks + receives)
    output = io.StringIO()
    with patch.object(grade, 'parse', return_value=object()), \
         patch.object(poll_grade, 'spans', return_value={}), \
         patch.object(poll_grade, 'committed', return_value={}), \
         patch.object(poll_grade, 'long_notices', return_value=[]), \
         patch.object(poll_grade, 'sections', return_value=sections), \
         patch.object(poll_grade, 'instances', return_value=[]), \
         patch.object(sys, 'argv', [str(extractor), '1x1', '2', str(path)]), \
         contextlib.redirect_stdout(output):
        runpy.run_path(str(extractor), run_name='__main__')
    published = output.getvalue().replace(Path(tmp).name, '<fixture>')
expected = {str(cycle): sum(max(0, cost - 10) for start, cost in
            [(s, c) for s, c in bases if s >= cycle][:5]) / 2
            for cycle in (10000, 20000, 30000)}
assert published.count('record at bus 10000:') == 3, published
assert 'record at bus 20000:' not in published and 'record at bus 30000:' not in published
assert 'over the after base: 0 cycles a sink' in published
assert max(expected.values()) == 495
print(json.dumps({'fixture_input': marks + receives, 'poll_bases': bases,
                  'extractor_stdout': published,
                  'per_distinct_record_excess_per_sink': expected,
                  'result': 'Confirmed: repeated first-commit selection can omit a larger later window.',
                  'limit': 'Synthetic association probe, not a new measurement of the product.'}, indent=2))

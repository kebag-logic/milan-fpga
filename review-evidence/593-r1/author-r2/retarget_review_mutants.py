#!/usr/bin/env python3
"""Re-anchor changed review controls without modifying either review packet."""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

source = Path('$LANES/593-mr-tu-soak/tb/tools/torture_campaign.py')
text = source.read_text()
rows = [
 ('R362 R01', '                   <= Decimal(str(resolution_s))\n',
  '                   <= 2 * Decimal(str(resolution_s))\n'),
 ('R362 R02', '                   <= Decimal(str(resolution_s))\n',
  '                   < Decimal(str(resolution_s))\n'),
 ('R363 M01', '    for toggle in toggles:\n        matches =',
  '    for toggle in []:\n        matches ='),
 ('R363 M40', '    for toggle in toggles:\n        matches =',
  '    for toggle in toggles[1:]:\n        matches ='),
 ('R363 M41', '    for toggle in toggles:\n        matches =',
  '    for toggle in toggles[:-1]:\n        matches ='),
 ('R363 M48', 'gm_events_s = gm_changes_s',
  'gm_events_s = [event_s for event_s in gm_changes_s if observed_start_s <= event_s]'),
 ('R362 R13 / R363 M14 replacement: ignore reset', 'if after["value"] < before["value"]:',
  'if False:'),
 ('R362 R24 / R363 M26 replacement: restore ignored GM edges', 'gm_events_s = gm_changes_s',
  'gm_events_s = [event_s for event_s in gm_changes_s if event_s < clear_s]'),
]
with tempfile.TemporaryDirectory(prefix='593-r2-reanchors-') as directory:
 candidate = Path(directory)/source.name
 candidate.write_text(text)
 command = [sys.executable, '-B', str(candidate), '--self-test']
 baseline = subprocess.run(command, capture_output=True, text=True, timeout=1800)
 assert baseline.returncode == 0, baseline.stderr
 print('Baseline rc 0')
 for label, old, new in rows:
  assert text.count(old) == 1, (label, text.count(old))
  candidate.write_text(text.replace(old, new))
  result = subprocess.run(command, capture_output=True, text=True, timeout=1800)
  failures = re.findall(r'^FAIL: (\w+)', result.stderr, re.M)
  assert result.returncode == 1 and failures, (label, result.stderr)
  print(label, 'KILLED', ', '.join(failures))
assert source.read_text() == text
print('All 8 re-anchored or replacement controls killed; source unchanged')

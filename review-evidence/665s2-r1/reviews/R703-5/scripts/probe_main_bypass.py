"""Probe M1: main() writes results.json without run.summary (composed_maximum dropped).
Usage: python3 -I probe_main_bypass.py <copy of harness dir>; edits run.py in that copy only."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'run.py'
s = p.read_text()
old = "    (out / 'results.json').write_text(json.dumps(summary(args.point, spec['executable_sha256'], results, refusals,\n                                                         misses), indent=1) + '\\n')"
assert s.count(old) == 1, 'anchor'
new = "    (out / 'results.json').write_text(json.dumps(dict(summary(args.point, spec['executable_sha256'], results, refusals,\n                                                         misses), composed_maximum=None), indent=1) + '\\n')"
p.write_text(s.replace(old, new))
print('M1 planted')

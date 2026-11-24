#!/usr/bin/env python3
"""mutcmp.py DIR...: every mutation driver's log in each run directory against the first directory's, after
removing only host text (logcmp.py's rule, plus the staging directory's name: tempfile's random one or
mutant_stage's stable slot, which is what the change under test moves). Also lists each run's verdict lines
([PASS]/[FAIL]/named rejection/ok/FAIL lines) so a reader sees every mutant and the check that killed it."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import importlib.util
spec = importlib.util.spec_from_file_location('logcmp', '/data-2/milan/tmp/cicd-a839/bin/logcmp.py')
lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
STAGE = [(re.compile(r'<TMP>/[A-Za-z0-9_.-]+'), '<STAGE>'), (re.compile(r'milan-mutant-stage-\d+/[A-Za-z0-9_.-]+'), '<STAGE>'),
         (re.compile(r'<TMP>/<STAGE>'), '<STAGE>')]
def norm(p):
    out = []
    for l in lc.norm(p):
        for r, s in STAGE: l = r.sub(s, l)
        out.append(l)
    return out
dirs = [Path(d) for d in sys.argv[1:]]
for log in sorted(dirs[0].glob('*.log')):
    ref = norm(log)
    verdicts = [l for l in ref if re.match(r'^(\[PASS\]|\[FAIL\]|  named rejection|ok |FAIL |PASS |== )', l)]
    for d in dirs[1:]:
        other = d / log.name
        if not other.exists():
            print(f'{log.stem}: {d.name}: MISSING'); continue
        o = norm(other)
        print(f'{log.stem}: {dirs[0].name} vs {d.name}: ' + ('IDENTICAL (%d normalised lines, %d verdict lines)' % (len(ref), len(verdicts)) if o == ref else 'DIFFER'))
        if o != ref:
            import difflib; print('\n'.join(list(difflib.unified_diff(ref, o, n=0, lineterm=''))[:12]))

#!/usr/bin/env python3
"""Reapply review mutations to current production anchors, never test text.

The original packets stay read-only. Retargets preserve the same defect where
round 3 moved metadata, renamed the resolution limit, or replaced its text.
Assertion failures and crash-only detections are reported separately. A crash
never supplies a kill claim; its verdict-preserving replacement must fail too.
"""
import importlib.util
import json
from pathlib import Path
import re
import runpy
import subprocess
import sys
import tempfile

ROOT = Path('$LANES/593-mr-tu-soak')
OUT = Path(__file__).resolve().parent
INTERNAL = Path('$REVIEWS/593-r362-2-packet/probes')
EXTERNAL = Path('$REVIEWS/593-r363-2-packet/scripts')


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def retarget(mid, old, new):
    if mid == 'internal-C17':
        return ('              "resolution_limit_s": resolution_limit_s}\n', '              }\n')
    if mid == 'internal-C18':
        return ('              "resolution_limit_s": resolution_limit_s,\n', '')
    if mid == 'external-M13':
        return ('resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S / 2\n',
                'resolution_limit_s = MILAN_MAX_OBSERVATION_INTERVAL_S\n')
    if mid == 'internal-T23':
        return ('require 2 * R < 0.25 s so an instant clear fails; ',
                'observation_resolution_s must be less than 0.5 s; ')
    substitutions = {
        'min(0.25, holdover_bound_s)': 'RELEASE_TU_RESOLUTION_LIMIT_S',
        'observation_resolution_s < 0.25': 'observation_resolution_s < RELEASE_TU_RESOLUTION_LIMIT_S',
        'observation_resolution_s <= 0.25': 'observation_resolution_s <= RELEASE_TU_RESOLUTION_LIMIT_S',
        'observation_resolution_s must be less than min(0.25 s, 0.5 s); ': 
            'require 2 * R < 0.25 s so an instant clear fails; ',
    }
    for before, after in substitutions.items():
        old, new = old.replace(before, after), new.replace(before, after)
    return old, new


def main():
    internal = load(INTERNAL / 'r362_2_mutants.py', 'internal_mutations')
    external = load(EXTERNAL / 'reviewer_mutants.py', 'external_mutations')
    cases = [('internal-' + mid, name, old, new) for mid, name, old, new in internal.MUTANTS]
    cases += [('external-' + name.split()[0], name, old, new) for name, old, new in external.MUTANTS]
    previous = runpy.run_path(str(EXTERNAL / 'round1_reanchored.py'))['runner'].MUTANTS
    cases += [('previous-' + name.split()[0], name, old, new) for name, old, new in previous]
    cases += [('internal-T25', 'PHC/fabric examples negated',
               '"(including PHC settime/adjtime and fabric discontinuity); "',
               '"(excluding PHC settime/adjtime and fabric discontinuity); "')]
    cases += [('previous-R1-M01r-safe', 'Accept an uncaused toggle without indexing an empty match list',
               'return "FAIL", {"why": "mr toggle without a recorded media-clock cause", "toggle": toggle}',
               'return "PASS", {"toggles_s": [toggle["timestamp_s"] for toggle in toggles]}')]
    source = (ROOT / 'tb/tools/torture_campaign.py').read_text()
    marker = 'class _ReleasePlanChecks:'
    production, tests = source.split(marker, 1)
    head = subprocess.run(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], cwd=ROOT,
                          capture_output=True, text=True, check=True, timeout=60).stdout.strip()
    rows = []
    with tempfile.TemporaryDirectory(prefix='593-round3-mutations-') as temp:
        candidate = Path(temp) / 'torture_campaign.py'
        command = ['rtk', 'proxy', 'python3', '-B', str(candidate), '--self-test']
        candidate.write_text(source)
        baseline = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=900)
        if baseline.returncode or '\nOK\n' not in baseline.stderr:
            raise RuntimeError('Pristine self-test failed')
        for mid, name, old, new in cases:
            old, new = retarget(mid, old, new)
            count = production.count(old)
            row = dict(id=mid, description=name, old=old, new=new, count=count, head=head)
            if count != 1:
                row.update(verdict='ANCHOR-ERROR', failures=[])
            else:
                candidate.write_text(production.replace(old, new) + marker + tests)
                result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=900)
                failures = sorted(set(re.findall(r'^FAIL: (\w+)', result.stderr, re.M)))
                errors = sorted(set(re.findall(r'^ERROR: (\w+)', result.stderr, re.M)))
                row.update(verdict='KILLED' if result.returncode == 1 and failures else 'SURVIVED',
                           rc=result.returncode, failures=failures, errors=errors)
                if (mid == 'previous-R1-M01r' and result.returncode == 1
                        and 'test_release_mr_no_cause' in errors and 'IndexError' in result.stderr):
                    row.update(verdict='CRASH-ONLY',
                               reason='Removing the guard indexes matches[0] on an empty list; '
                                      'the safe replacement preserves verdict evaluation.')
            rows.append(row)
            print(mid, row['verdict'], ','.join(row['failures']), flush=True)
    (OUT / 'review-reanchors.json').write_text(json.dumps(rows, indent=2) + '\n')
    killed = sum(row['verdict'] == 'KILLED' for row in rows)
    crashes = sum(row['verdict'] == 'CRASH-ONLY' for row in rows)
    print(f'SUMMARY killed={killed} crash_only={crashes} total={len(rows)}')
    return 0 if killed + crashes == len(rows) else 1


if __name__ == '__main__':
    raise SystemExit(main())

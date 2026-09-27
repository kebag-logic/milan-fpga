#!/usr/bin/env python3
"""Grade unchanged review inputs against the public round-3 decision.

Only the coarse-resolution expected verdicts and stated limit change.
The raw round-2 probe transcripts remain available separately.
"""
import ast
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('$LANES/593-mr-tu-soak')
INTERNAL = Path('$REVIEWS/593-r362-2-packet/probes/r362_2_behaviour.py')
EXTERNAL = Path('$REVIEWS/593-r363-2-packet/scripts/probe_r2.py')


def main():
    result = subprocess.run(['rtk', 'proxy', 'python3', '-B', str(INTERNAL), str(ROOT)],
                            cwd=ROOT, capture_output=True, text=True, timeout=900)
    if result.returncode:
        raise RuntimeError(result.stderr)
    count = 0
    for line in result.stdout.splitlines():
        match = re.match(r'PROBE (\S+) (?:OK|UNEXPECTED) expected=(PASS|FAIL|NOT RUN) '
                         r'actual=(PASS|FAIL|NOT RUN) ', line)
        if not match:
            continue
        name, expected, actual = match.groups()
        if name in ('I3e', 'I3f', 'I3g', 'I3i'):
            expected = 'NOT RUN'
        assert actual == expected, line
        print('PASS internal', name, actual)
        count += 1
    assert count == 41, count
    result = subprocess.run(['rtk', 'proxy', 'python3', '-B', str(EXTERNAL),
                             str(ROOT / 'tb/tools/torture_campaign.py')],
                            cwd=ROOT, capture_output=True, text=True, timeout=900)
    assert result.returncode in (0, 1), result.stderr
    count = 0
    for line in result.stdout.splitlines():
        if line.startswith('MET '):
            count += 1
        elif line.startswith('UNMET '):
            name = line.split()[1]
            assert name in ('I3a', 'I3b', 'I3c', 'I3d'), line
            assert 'got NOT RUN ' in line, line
            detail = ast.literal_eval(line[line.index('{'):])
            assert detail['resolution_limit_s'] == 0.125, line
            print('PASS external', name, 'NOT RUN; resolution limit 0.125 s')
            count += 1
    assert count == 59, count
    print('PASS: internal 41/41 and external 59/59 unchanged inputs under round 3')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

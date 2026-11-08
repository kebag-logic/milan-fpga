# SPDX-License-Identifier: MIT
# usage: per_test_escape.py MUT_WORK ESCAPE_JSON OUT_JSON
# For each round 5 test and each plant that fails it on the full binary, run that plant's binary without only
# that test: rc 0 means the test is the plant's sole killer, so the plant escapes without it.
import json, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
work, esc, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
NEW = ['KeptCommandsBehindSevenOwedLeaveOnePassSooner', 'AnsweredProbeEndsTheHoldOfItsRetry']
env = {'LD_LIBRARY_PATH': '<tools>/gtest-1.14.0/lib', 'PATH': '/usr/bin'}
rows = {}
for t in NEW:
    full = 'AcmpOwed.' + t
    rows[t] = []
    for r in esc:
        if full in r.get('full_suite', {}).get('failed', []):
            b = work / r['plant'] / 'acmp'
            x = work / r['plant'] / ('without-' + t + '.xml')
            x.unlink(missing_ok=True)
            p = subprocess.run([str(b), '--gtest_output=xml:' + str(x), '--gtest_filter=-' + full], env=env,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
            failed = sorted(c.get('classname') + '.' + c.get('name') for c in ET.parse(x).getroot().iter('testcase')
                            if c.findall('failure')) if x.exists() else ['CRASHED']
            rows[t].append({'plant': r['plant'], 'rc_without_this_test': p.returncode, 'still_failing': failed,
                            'escapes_without_this_test': p.returncode == 0 and not failed})
out.write_text(json.dumps(rows, indent=1) + '\n')
for t, v in rows.items():
    sole = [x['plant'] for x in v if x['escapes_without_this_test']]
    print(f"{t}: fails under {len(v)} plants; sole killer of {len(sole)}: {', '.join(sole)}")

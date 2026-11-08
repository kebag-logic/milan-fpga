# SPDX-License-Identifier: MIT
# usage: escape5.py WORK MUTATIONS_JSON OUT
# For each owed-bound plant built by scripts/mutation.py under WORK, run its full ACMP test binary, then run it
# again without the tests that failed (its killers), and again without only the two round 5 tests.
import json, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
work, mutations, out_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
NEW = ['AcmpOwed.KeptCommandsBehindSevenOwedLeaveOnePassSooner', 'AcmpOwed.AnsweredProbeEndsTheHoldOfItsRetry']
EXTRA = ('acmp-full-queue-acts', 'acmp-stop-keeps-the-hold', 'acmp-probe-before-response', 'acmp-rebind-same-reprobes',
         'acmp-owed-probe-no-resp-2s', 'acmp-lost-probe-uncounted', 'acmp-poll-newest-first', 'acmp-poll-drains-everything',
         'acmp-response-passes-an-owed-frame')
plants = [m for m in json.loads(mutations.read_text())
          if m['name'].startswith('owed-') or m['name'] in EXTRA]
env = {'LD_LIBRARY_PATH': '<tools>/gtest-1.14.0/lib', 'PATH': '/usr/bin'}
def run(binary, xml, filt=None):
    xml.unlink(missing_ok=True)
    cmd = [str(binary), '--gtest_output=xml:' + str(xml)] + (['--gtest_filter=' + filt] if filt else [])
    r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
    if not xml.exists():
        return r.returncode, 0, ['CRASHED']
    doc = ET.parse(xml).getroot()
    failed = sorted(c.get('classname') + '.' + c.get('name') for c in doc.iter('testcase') if c.findall('failure'))
    return r.returncode, int(doc.get('tests')), failed
report = []
for m in plants:
    d = work / m['name']
    b = d / 'acmp'
    if not b.exists():
        report.append({'plant': m['name'], 'error': 'no binary'})
        print(m['name'], 'NO BINARY')
        continue
    rc, n, failed = run(b, d / 'full-suite.xml')
    row = {'plant': m['name'], 'registered_killers': sorted({k['test'] for k in m['kills']}),
           'full_suite': {'rc': rc, 'tests': n, 'failed': failed}}
    if failed:
        rc2, n2, failed2 = run(b, d / 'without-killers.xml', '-' + ':'.join(failed))
        row['without_its_killers'] = {'excluded': failed, 'rc': rc2, 'tests': n2, 'failed': failed2,
                                      'escapes': rc2 == 0 and not failed2}
    rc3, n3, failed3 = run(b, d / 'without-round5-tests.xml', '-' + ':'.join(NEW))
    row['without_round5_tests'] = {'rc': rc3, 'tests': n3, 'failed': failed3, 'escapes': rc3 == 0 and not failed3}
    report.append(row)
    print(m['name'], 'full_rc', rc, 'tests', n, 'failing', len(failed),
          'escapes_without_killers', row.get('without_its_killers', {}).get('escapes'),
          'escapes_without_round5', row['without_round5_tests']['escapes'])
out_path.write_text(json.dumps(report, indent=1) + '\n')

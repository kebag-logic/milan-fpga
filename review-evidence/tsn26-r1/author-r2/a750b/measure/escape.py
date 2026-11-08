import json, subprocess, sys, xml.etree.ElementTree as ET
from pathlib import Path
work = Path(sys.argv[1]); out_path = Path(sys.argv[2])
plants = [m for m in json.load(open('$LANES/tsn-c-stack-26-owed/tests/mutations.json'))
          if m['name'].startswith('owed-') or m['name'] == 'acmp-full-queue-acts']
env = {'LD_LIBRARY_PATH': '$VALIDATION_TOOLS/gtest-1.14.0/lib', 'PATH': '/usr/bin'}
def run(binary, xml, filt=None):
    xml.unlink(missing_ok=True)
    cmd = [str(binary), '--gtest_output=xml:' + str(xml)] + (['--gtest_filter=' + filt] if filt else [])
    r = subprocess.run(cmd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=120)
    doc = ET.parse(xml).getroot()
    failed = sorted(c.get('classname') + '.' + c.get('name') for c in doc.iter('testcase') if c.findall('failure'))
    return r.returncode, int(doc.get('tests')), failed
report = []
for m in plants:
    b = work / m['name'] / 'acmp'
    rc, n, failed = run(b, work / m['name'] / 'full-suite.xml')
    row = {'plant': m['name'], 'registered_killers': sorted({k['test'] for k in m['kills']}),
           'full_suite': {'rc': rc, 'tests': n, 'failed': failed}}
    if failed:
        rc2, n2, failed2 = run(b, work / m['name'] / 'without-killers.xml', '-' + ':'.join(failed))
        row['without_its_killers'] = {'excluded': failed, 'rc': rc2, 'tests': n2, 'failed': failed2,
                                      'escapes': rc2 == 0 and not failed2}
    report.append(row)
    print(m['name'], rc, n, failed, row.get('without_its_killers', {}).get('escapes'))
out_path.write_text(json.dumps(report, indent=1) + '\n')

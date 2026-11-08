#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Run each named mutant's ACMP test binary on the whole suite and list every failing test.

Usage: full_suite_killers.py MUTATION_WORK OUT_JSON NAME...
"""
import json, os, subprocess, sys, tempfile, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
work, out, names = sys.argv[1], sys.argv[2], sys.argv[3:]
env = {k: v for k, v in os.environ.items() if not k.startswith('GTEST_')}
def one(name):
    binary = os.path.join(work, name, 'acmp')
    with tempfile.TemporaryDirectory() as d:
        xml = os.path.join(d, 'r.xml')
        rc = subprocess.run([binary, '--gtest_output=xml:' + xml], env=env, stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL, timeout=300).returncode
        root = ET.parse(xml).getroot()
        failed = sorted(c.get('classname') + '.' + c.get('name') for c in root.iter('testcase') if c.findall('failure'))
        return {'name': name, 'rc': rc, 'tests': int(root.get('tests')), 'failing': failed}
with ThreadPoolExecutor(8) as pool:
    results = list(pool.map(one, names))
json.dump(results, open(out, 'w'), indent=2)
for r in results:
    print(f"{r['name']}: rc {r['rc']} tests {r['tests']} failing {len(r['failing'])}: {', '.join(r['failing'])}")

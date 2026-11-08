# SPDX-License-Identifier: MIT
# usage: needles_failing.py MUT_WORK PLANT...   (runs each plant's ACMP binary on the whole suite; prints test | message)
import os, re, subprocess, sys, tempfile, xml.etree.ElementTree as ET
work = sys.argv[1]
env = {'LD_LIBRARY_PATH': '<tools>/gtest-1.14.0/lib', 'PATH': '/usr/bin'}
for name in sys.argv[2:]:
    with tempfile.TemporaryDirectory(dir='<scratch>/tmp') as d:
        x = os.path.join(d, 'r.xml')
        subprocess.run([os.path.join(work, name, 'acmp'), '--gtest_output=xml:' + x], env=env,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        if not os.path.exists(x):
            print(name, 'CRASHED'); continue
        seen = set()
        for c in ET.parse(x).getroot().iter('testcase'):
            for f in c.findall('failure'):
                for m in re.findall(r'TSN_MESSAGE_BEGIN_\w+\n(.*?)\nTSN_MESSAGE_END', f.get('message', '') + (f.text or ''), re.S):
                    seen.add((c.get('name'), m))
        for t, m in sorted(seen):
            print(f'{name} | {t} | {m}')

#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Reviewer probe for the entity generator: plant one edit in scripts/entity_yaml.py
and run the golden check and the schema self-test, then remove only the named
self-test method and rerun the self-test.

Usage: gen_probe.py --src TREE --work DIR --plants PLANTS.json --out RESULTS.json
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def run(argv, cwd):
    r = subprocess.run(argv, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    return r.returncode, r.stdout


def remove_method(path, method):
    lines = path.read_text().split('\n')
    for i, line in enumerate(lines):
        if re.match(r'^    def ' + re.escape(method) + r'\(', line):
            j = i + 1
            while j < len(lines) and (lines[j].startswith('        ') or lines[j].strip() == ''):
                j += 1
            del lines[i:j]
            path.write_text('\n'.join(lines))
            return True
    return False


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--src', type=Path, required=True)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--plants', type=Path, required=True)
    p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    results = []
    for plant in json.loads(args.plants.read_text()):
        root = args.work / plant['name']
        shutil.rmtree(root, ignore_errors=True)
        shutil.copytree(args.src, root, ignore=shutil.ignore_patterns('.git'))
        r = {'plant': plant['name'], 'killer': plant.get('killer')}
        if plant.get('path'):
            target = root / plant['path']
            text = target.read_text()
            if text.count(plant['old']) != 1:
                r['result'] = 'ERROR'
                results.append(r)
                continue
            target.write_text(text.replace(plant['old'], plant['new']))
        golden_rc, golden = run([sys.executable, 'scripts/entity_yaml.py', '--examples', '--check'], root)
        self_rc, selfout = run([sys.executable, 'scripts/entity_selftest.py', '--work', str(root / 'work')], root)
        failed = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\w+)', selfout, re.M)))
        r.update(golden_rc=golden_rc, golden_tail=golden.strip().splitlines()[-1:] if golden.strip() else [],
                 selftest_rc=self_rc, selftest_failed=failed)
        r['result'] = 'CAUGHT' if (golden_rc or self_rc) else 'ESCAPED'
        if plant.get('killer') and self_rc:
            remove_method(root / 'scripts/entity_selftest.py', plant['killer'])
            rc2, out2 = run([sys.executable, 'scripts/entity_selftest.py', '--work', str(root / 'work2')], root)
            r['removed_selftest_rc'] = rc2
            r['removed_failed'] = sorted(set(re.findall(r'^(?:FAIL|ERROR): (\w+)', out2, re.M)))
        results.append(r)
        print(r['plant'], r['result'], 'golden', golden_rc, 'selftest', self_rc, failed,
              'removed_rc', r.get('removed_selftest_rc'), flush=True)
    args.out.write_text(json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    raise SystemExit(main())

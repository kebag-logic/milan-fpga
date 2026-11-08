#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Drive scripts/mutation.py with a small plant table that exercises the header-plant
build rule and the unknown-arm path, once with the head driver and once with the base
driver, both against the head sources. Records each campaign's rc, summary and statuses."""
import argparse, copy, json, os, subprocess
from pathlib import Path

HEAD = 'c687810b74b53b69c1fbdff7bfd0ec9da94eaa78'
BASE = '70936b77dc41981e192438388cd0aced69954f18'

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', type=Path, required=True)
    ap.add_argument('--work', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    table = json.loads(subprocess.run(['git', '-C', str(a.clone), 'show', HEAD + ':tests/mutations.json'],
                                      stdout=subprocess.PIPE, check=True).stdout)
    by = {m['name']: m for m in table}
    plants = []
    def add(name, source, arm='keep'):
        m = copy.deepcopy(by[source]); m['name'] = name
        for k in m['kills']:
            if arm is None:
                k.pop('arm', None)
            elif arm != 'keep':
                k['arm'] = arm
        plants.append(m)
    add('p1-header-with-source-unknown-arm', 'acmp-header-version-1', 'bogus')
    add('p2-wire-unknown-arm', 'wire-put-be-skips-an-odd-field-first-byte', 'bogus')
    add('p3-wire-no-arm', 'wire-put-be-skips-an-odd-field-first-byte', None)
    add('p4-wire-genuine-acmp', 'wire-put-be-writes-past-an-odd-field')
    add('p5-wire-genuine-adp-arm', 'wire-put-be-writes-past-an-odd-field', 'adp')
    add('p6-header-with-source-genuine', 'maap-retransmit-count')
    summary = {}
    for side, driver in (('head', HEAD), ('base-driver', BASE)):
        tree = a.work / side / 'tree'
        subprocess.run(['rm', '-rf', str(a.work / side)], check=True)
        tree.mkdir(parents=True)
        archive = subprocess.run(['git', '-C', str(a.clone), 'archive', HEAD], stdout=subprocess.PIPE, check=True).stdout
        subprocess.run(['tar', '-x', '-C', str(tree)], input=archive, check=True)
        (tree / 'scripts/mutation.py').write_bytes(subprocess.run(
            ['git', '-C', str(a.clone), 'show', driver + ':scripts/mutation.py'], stdout=subprocess.PIPE, check=True).stdout)
        (tree / 'tests/mutations.json').write_text(json.dumps(plants, indent=2) + '\n')
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        r = subprocess.run(['python3', str(tree / 'scripts/mutation.py'), '--work', str(a.work / side / 'campaign'),
                            '--jobs', str(a.jobs)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, env=env)
        (a.work / side / 'campaign.log').write_text(r.stdout)
        res_path = a.work / side / 'campaign/results.json'
        results = json.loads(res_path.read_text()) if res_path.exists() else None
        summary[side] = {'driver': driver, 'rc': r.returncode, 'results_json_written': results is not None,
                         'tail': r.stdout.strip().splitlines()[-3:],
                         'statuses': {x['name']: [x['status'], x.get('error', '')] for x in results} if results else None}
    print(json.dumps(summary, indent=1))

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Run independent source-head checks concurrently; join all work before exit."""
import argparse
import concurrent.futures
import hashlib
import json
from pathlib import Path
import subprocess
import time

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path, required=True)
    ap.add_argument('--packet', type=Path, required=True)
    ap.add_argument('--jobs', type=int, default=4)
    a = ap.parse_args()
    repo, packet = a.repo.resolve(), a.packet.resolve()
    scratch = packet / 'scratch'
    scratch.mkdir(exist_ok=True, parents=True)
    receipts = packet / 'receipts'
    receipts.mkdir(exist_ok=True)
    tasks = {}
    for profile in ('OFF', 'ON'):
        tasks['differential-' + profile.lower()] = [
            ['python3', '-B', 'tests/check_differential.py', '--work-dir',
             str(scratch / ('differential-' + profile.lower())), '--milan', profile]]
    tasks['docs'] = [['python3', '-B', 'doc/tools/' + script, *extra] for script, extra in (
        ('check_sentences.py', []), ('check_references.py', []), ('check_references.py', ['--self-test']))]
    tasks['freestanding'] = [['python3', '-B', 'tests/check_freestanding.py'],
                            ['python3', '-B', 'tests/check_embedded.py', '--work-dir', str(scratch / 'embedded')]]
    def run(name, commands):
        start = time.monotonic()
        codes = []
        with (receipts / (name + '.log')).open('w') as log:
            for command in commands:
                log.write('$ ' + ' '.join(command) + '\n')
                log.flush()
                try:
                    r = subprocess.run(command, cwd=repo, stdout=log, stderr=subprocess.STDOUT, timeout=1800)
                    codes.append(r.returncode)
                except subprocess.TimeoutExpired:
                    codes.append(124)
                log.write('RETURN_CODE=' + str(codes[-1]) + '\n')
                log.flush()
        row = {'name': name, 'return_codes': codes, 'elapsed_seconds': round(time.monotonic()-start, 2)}
        (receipts / (name + '.rc')).write_text(json.dumps(row) + '\n')
        if name.startswith('differential'):
            result = scratch / name / 'differential.json'
            if result.exists():
                (receipts / (name + '.json')).write_bytes(result.read_bytes())
        return row
    with concurrent.futures.ThreadPoolExecutor(max_workers=min(a.jobs, 16)) as pool:
        futures = [pool.submit(run, name, commands) for name, commands in tasks.items()]
        for future in concurrent.futures.as_completed(futures):
            print(json.dumps(future.result()), flush=True)

if __name__ == '__main__':
    main()

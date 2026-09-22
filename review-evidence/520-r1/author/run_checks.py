#!/usr/bin/env python3
"""Portable focused checks with exact command, tree, exit and raw-log receipts."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

BASE = '483a133ed08867ea0d300d2b4a027b5b48a4282f'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--tree', type=Path, default=Path.cwd())
    args = parser.parse_args()
    out, tree = args.out.resolve(), args.tree.resolve()
    out.mkdir(parents=True, exist_ok=True)
    def git(*argv):
        return subprocess.check_output(['git', *argv], cwd=tree, text=True).strip()
    state = dict(head=git('rev-parse', 'HEAD'), tree=git('rev-parse', 'HEAD^{tree}'),
                 status=git('status', '--porcelain'),
                 working_diff_sha256=hashlib.sha256(git('diff', 'HEAD').encode()).hexdigest(),
                 recorded=datetime.now(timezone.utc).isoformat(),
                 max_parallel=4, affinity=sorted(os.sched_getaffinity(0)))
    (out / 'state.json').write_text(json.dumps(state, indent=2) + '\n')
    commands = [
        ['python3', 'syn/yosys/result_cache.py', '--selftest'],
        ['python3', 'syn/yosys/cache_selftest.py', '--logs', str(out / 'cache-fixtures')],
        ['bash', '-n', 'syn/yosys/run.sh'],
        ['bash', 'syn/yosys/check_list_hermetic.sh'],
        ['python3', 'scripts/yosys_tally.py', '--selftest'],
        ['python3', 'scripts/yosys_shards.py', '--selftest'],
        ['python3', 'scripts/pp_srcs.py', '--check', '--selftest'],
        ['python3', 'scripts/ci_events.py', '--check'],
        ['python3', 'scripts/ci_events.py', '--selftest'],
        ['python3', 'scripts/docs_check.py'],
        ['python3', 'scripts/check_doc_style.py'],
        ['python3', 'scripts/check_doc_style.py', '--selftest'],
        ['python3', 'scripts/check_doc_paths.py'],
        ['python3', 'scripts/gen_toc.py', '--check'],
        ['python3', 'scripts/gen_toc.py', '--verify-anchors'],
        ['python3', 'scripts/check_em_dash.py', '--base', BASE],
        ['python3', 'scripts/check_py_idiom.py'],
        ['python3', 'scripts/check_py_idiom.py', '--selftest'],
        ['python3', 'scripts/check_sh_idiom.py'],
        ['python3', 'scripts/check_sh_idiom.py', '--selftest'],
        ['python3', 'scripts/measure_fail_fast.py', '--check'],
        ['python3', 'scripts/measure_fail_fast.py', '--selftest'],
        ['python3', 'scripts/measure_test_evidence.py', '--check'],
        ['python3', 'scripts/measure_test_evidence.py', '--selftest'],
        ['git', 'diff', '--check', BASE],
    ]
    def run(item):
        index, command = item
        start = time.monotonic()
        path = out / f'{index:02d}.log'
        env = dict(os.environ, MAKEFLAGS='-j8', OMP_NUM_THREADS='8', PYTHONUNBUFFERED='1')
        with path.open('w') as log:
            result = subprocess.run(command, cwd=tree, env=env, stdout=log, stderr=subprocess.STDOUT)
        row = dict(command=command, exit=result.returncode, seconds=round(time.monotonic()-start,3),
                   log=path.name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        (out / f'{index:02d}.json').write_text(json.dumps(row, indent=2) + '\n')
        print(f'{index:02d} exit={result.returncode}: {" ".join(command)}', flush=True)
        return row
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, enumerate(commands, 1)))
    state['end_head'] = git('rev-parse', 'HEAD')
    state['end_status'] = git('status', '--porcelain')
    (out / 'complete.json').write_text(json.dumps(dict(state, results=results), indent=2) + '\n')
    return int(any(row['exit'] for row in results))


if __name__ == '__main__':
    sys.exit(main())

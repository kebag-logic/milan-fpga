#!/usr/bin/env python3
"""Validate the consumer at the source head, restoring its index without committing."""
import hashlib
import json
from pathlib import Path
from runpy import run_path
import subprocess
import time

CONFIG = run_path(str(Path(__file__).with_name('run-gates.py')))
PACKET = CONFIG['PACKET']
ENV = CONFIG['ENV']
ROOT = Path('$LANES/pp94-parent-consumer')
GATES = [
    ('cpp-idiom', ['python3', 'scripts/check_cpp_idiom.py']),
    ('py-idiom', ['python3', 'scripts/check_py_idiom.py']),
    ('xvlog', ['python3', 'scripts/xvlog_gate.py', '--check']),
    ('rtl-source-lists', ['python3', 'scripts/check_rtl_source_lists.py']),
    ('pp-shadow', ['make', '-C', 'tb/verilator/pp_shadow', '-j8']),
]


def git_text(*args: str) -> str:
    """Read parent metadata without changing it."""
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True, timeout=60,
                                   env={**ENV, 'GIT_OPTIONAL_LOCKS': '0'}).rstrip()


def main() -> int:
    """Stage only the tested gitlink for the pin checks, then restore the exact index."""
    index = Path(git_text('rev-parse', '--path-format=absolute', '--git-path', 'index'))
    original = index.read_bytes()
    state = {'parent_head': git_text('rev-parse', 'HEAD'),
             'status_before': git_text('status', '--porcelain'),
             'index_tree_before': git_text('write-tree'),
             'pin_before': git_text('rev-parse', ':protocol-processor'),
             'index_sha256_before': hashlib.sha256(original).hexdigest()}
    results = []
    with (PACKET / 'parent-fetch-checkout.log').open('w') as stream:
        rc = subprocess.run(['bash', '-lc',
            'git -C protocol-processor fetch $LANES/pp94-desc-mem-guard HEAD'
            ' && git -C protocol-processor checkout --detach FETCH_HEAD'],
            cwd=ROOT, stdout=stream, stderr=subprocess.STDOUT, timeout=600).returncode
    if rc:
        return rc
    try:
        subprocess.run(['git', 'add', '--', 'protocol-processor'], cwd=ROOT,
                       check=True, timeout=60)
        state['tested_pin'] = git_text('rev-parse', ':protocol-processor')
        state['submodule_head'] = git_text('-C', 'protocol-processor', 'rev-parse', 'HEAD')
        assert state['tested_pin'] == state['submodule_head']
        state['temporary_index_delta'] = git_text('diff', '--cached', '--raw', '--', 'protocol-processor')
        for name, command in GATES:
            print(f'START {name}: {" ".join(command)}', flush=True)
            start = time.monotonic()
            with (PACKET / f'parent-{name}.log').open('w') as stream:
                try:
                    rc = subprocess.run(command, cwd=ROOT, env=ENV, stdout=stream,
                                        stderr=subprocess.STDOUT, timeout=7200).returncode
                except subprocess.TimeoutExpired:
                    rc = 124
            result = {'gate': name, 'command': command, 'rc': rc,
                      'seconds': round(time.monotonic() - start, 2)}
            results.append(result)
            (PACKET / 'parent-results.json').write_text(json.dumps(results, indent=2) + '\n')
            print(f'END {name}: rc={rc}; seconds={result["seconds"]}', flush=True)
    finally:
        index.write_bytes(original)
        state['index_tree_after'] = git_text('write-tree')
        state['parent_head_after'] = git_text('rev-parse', 'HEAD')
        state['pin_after'] = git_text('rev-parse', ':protocol-processor')
        state['status_after'] = git_text('status', '--porcelain')
        index.write_bytes(original)  # Preserve bytes even if write-tree refreshed a cache.
        state['index_sha256_after'] = hashlib.sha256(index.read_bytes()).hexdigest()
        state['index_restored'] = state['index_sha256_before'] == state['index_sha256_after']
        (PACKET / 'parent-state.json').write_text(json.dumps(state, indent=2) + '\n')
    assert state['index_restored'] and state['parent_head'] == state['parent_head_after']
    return int(any(result['rc'] for result in results))


if __name__ == '__main__':
    raise SystemExit(main())

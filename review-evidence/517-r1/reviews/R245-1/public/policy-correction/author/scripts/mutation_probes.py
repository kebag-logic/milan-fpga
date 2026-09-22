#!/usr/bin/env python3
"""Reject broadened and removed policy masks using only disposable checker copies."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import time

SOURCE = Path('$CANDIDATE/scripts/check_baremetal_only.py')
OUTPUT = Path(__file__).resolve().parents[1] / 'mutations'
HOME = 'tb/verilator/milan_dp/'
MUTANTS = (
    ('remove-runner-terms', f'del TERM_MASKS[{HOME + "sim_pool.py"!r}]', '-allowed] clean fixture flagged'),
    ('remove-test-terms', f'del TERM_MASKS[{HOME + "test_sim_pool.py"!r}]', '-allowed] clean fixture flagged'),
    ('remove-readme-term', f'del TERM_MASKS[{HOME + "README.md"!r}]', '-allowed] clean fixture flagged'),
    ('remove-runner-runtime', f'del HOST_RUNTIME_MASKS[{HOME + "sim_pool.py"!r}]', '-allowed] clean fixture flagged'),
    ('remove-test-runtime', f'del HOST_RUNTIME_MASKS[{HOME + "test_sim_pool.py"!r}]', '-allowed] clean fixture flagged'),
    ('broaden-runner-term', f'TERM_MASKS[{HOME + "sim_pool.py"!r}] = re.compile("linux", re.IGNORECASE)',
     '-unrelated-same-file-T] planted defect not caught'),
    ('broaden-test-runtime', f'HOST_RUNTIME_MASKS[{HOME + "test_sim_pool.py"!r}] = re.compile("/proc")',
     '-different-path-same-context] planted defect not caught'),
    ('swallow-runner-line', f'TERM_MASKS[{HOME + "sim_pool.py"!r}] = re.compile(".*")',
     '-extra-rootfs] planted defect not caught'),
    ('leak-wrong-file', f'TERM_MASKS["other.py"] = TERM_MASKS[{HOME + "sim_pool.py"!r}]',
     '-wrong-file-T] planted defect not caught'),
    ('allow-bare-literal-path',
     f'HOST_RUNTIME_MASKS[{HOME + "sim_pool.py"!r}] = re.compile(re.escape("/proc/self/task/{{os.getpid()}}/children"))',
     '-path-without-context] planted defect not caught'),
)


def main():
    source = SOURCE.read_text()
    marker = 'if __name__ == "__main__":'
    assert source.count(marker) == 1
    OUTPUT.mkdir(exist_ok=False)
    receipts = []
    for label, change, expected in MUTANTS:
        mutated = source.replace(marker, change + '\n\n' + marker)
        (OUTPUT / (label + '.patch')).write_text(''.join(difflib.unified_diff(
            source.splitlines(keepends=True), mutated.splitlines(keepends=True),
            fromfile='original/check_baremetal_only.py', tofile='mutated/check_baremetal_only.py')))
        with tempfile.TemporaryDirectory(prefix='517-policy-mutation-') as directory:
            target = Path(directory) / 'scripts' / 'check_baremetal_only.py'
            target.parent.mkdir()
            target.write_text(mutated)
            argv = ['rtk', 'proxy', 'python3', str(target), '--selftest']
            start = time.monotonic()
            run = subprocess.run(argv, capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'),
                                 check=False, timeout=60)
            stdout = run.stdout.decode(errors='replace')
            stderr = run.stderr.decode(errors='replace')
            (OUTPUT / (label + '.stdout')).write_bytes(run.stdout)
            (OUTPUT / (label + '.stderr')).write_bytes(run.stderr)
            record = dict(label=label, argv=argv, cwd=str(Path.cwd()), exit=run.returncode,
                          elapsed_seconds=time.monotonic()-start,
                          source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                          mutant_sha256=hashlib.sha256(mutated.encode()).hexdigest(),
                          expected_control=expected,
                          detected=run.returncode == 2 and expected in stderr)
            receipts.append(record)
            (OUTPUT / (label + '.json')).write_text(json.dumps(record, indent=2) + '\n')
            print(json.dumps(record), flush=True)
    (OUTPUT / 'receipts.json').write_text(json.dumps(receipts, indent=2) + '\n')
    assert all(row['detected'] for row in receipts), 'An intentional mutant escaped the required control'
    assert SOURCE.read_text() == source, 'Source checker changed during disposable probes'
    print(f'{len(receipts)}/{len(receipts)} representative removed/broadened masks rejected')


if __name__ == '__main__':
    main()

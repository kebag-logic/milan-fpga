"""Run the round-3 local gate set at the merge head, recording every result."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

root = Path.cwd()
out = Path(__file__).parent
round3 = Path('$MANAGEMENT/2026-09-23/590-a411')
assert root == Path('$LANES/590-592-599-firmware')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip()
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip()
# The merge's dev parent is the merge base the change is judged against.
base = '7a7582f03ce5ba7863a90ac342c21be18d90db0b'
assert subprocess.check_output(['git', 'merge-base', 'HEAD', base], text=True).strip() == base
python = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3'
checks = [
    ('host', ['sw/firmware/nvm_hosttest/test_nvm_firmware.py', '--self-test']),
    ('capture-receipt', ['scripts/check_nvm_capture.py']),
    ('kept-native-capture-oracles', [str(round3 / 'verify_packet.py')]),
    ('service-selftest', ['tb/verilator/fw_service_budget/run.py', '--self-test']),
    ('ci-scope', ['scripts/ci_scope.py', '--selftest']),
    ('docs', ['scripts/docs_check.py']),
    ('doc-paths', ['scripts/check_doc_paths.py']),
    ('doc-style', ['scripts/check_doc_style.py']),
    ('archive', ['scripts/check_archive.py']),
    ('toc', ['scripts/gen_toc.py', '--check']),
    ('em-dash', ['scripts/check_em_dash.py', '--base', base]),
    ('features', ['scripts/check_feature_status.py', '--self-test']),
    ('pp-sources', ['scripts/pp_srcs.py', '--check']),
    ('baremetal-only', ['scripts/check_baremetal_only.py', '--check']),
    ('entity-shape', ['scripts/check_entity_shape.py', '--self-test']),
    ('python-idiom', ['scripts/check_py_idiom.py']),
    ('cpp-idiom', ['scripts/check_cpp_idiom.py']),
    ('hygiene', ['scripts/check_hygiene.py', '--check']),
    ('test-evidence', ['scripts/measure_test_evidence.py', '--check']),
]
results = []
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
(out / 'logs').mkdir(exist_ok=True)
for name, args in checks + [('diff-whitespace', [])]:
    command = ['timeout', '1800', python, '-B', *args] if args else ['timeout', '60', 'git', 'diff', '--check', base]
    log = out / 'logs' / ('gate-' + name + '.log')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, env=environment)
    results.append(dict(name=name, head=head, command=command, rc=result.returncode,
                        seconds=round(time.monotonic() - start, 3), path=str(log.relative_to(out)),
                        size=log.stat().st_size, sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    (out / 'gates.json').write_text(json.dumps(results, indent=2) + '\n')
    print(name, 'rc', result.returncode, flush=True)
assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip() == head
assert not subprocess.check_output(['git', 'status', '--porcelain'], text=True).strip(), 'gates left the worktree dirty'
failed = [r['name'] for r in results if r['rc'] != 0]
print('FAILED: ' + ', '.join(failed) if failed else 'PASS: all local gates rc 0 at ' + head)

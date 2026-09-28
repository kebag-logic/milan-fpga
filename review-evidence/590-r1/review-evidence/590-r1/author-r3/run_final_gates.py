"""Execute the required local gates at one committed head, recording every result."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import time

root = Path.cwd()
out = Path(__file__).parent
assert root == Path('$LANES/590-592-599-firmware')
head = subprocess.check_output(['rtk', 'proxy', 'git', 'rev-parse', 'HEAD'], text=True).strip()
assert not subprocess.check_output(['rtk', 'proxy', 'git', 'diff', '--name-only'], text=True).strip()
python = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python3'
checks = [
 ('host', ['sw/firmware/nvm_hosttest/test_nvm_firmware.py','--self-test']),
 ('capture-receipt', ['scripts/check_nvm_capture.py']),
 ('kept-native-capture-oracles', [str(out/'verify_packet.py')]),
 ('service-selftest', ['tb/verilator/fw_service_budget/run.py','--self-test']),
 ('ci-scope', ['scripts/ci_scope.py','--selftest']),
 ('docs', ['scripts/docs_check.py']),
 ('doc-paths', ['scripts/check_doc_paths.py']),
 ('doc-style', ['scripts/check_doc_style.py']),
 ('archive', ['scripts/check_archive.py']),
 ('toc', ['scripts/gen_toc.py','--check']),
 ('em-dash', ['scripts/check_em_dash.py','--base','20aa4eabf']),
 ('features', ['scripts/check_feature_status.py','--self-test']),
 ('pp-sources', ['scripts/pp_srcs.py','--check']),
 ('baremetal-only', ['scripts/check_baremetal_only.py','--check']),
 ('entity-shape', ['scripts/check_entity_shape.py','--self-test']),
 ('python-idiom', ['scripts/check_py_idiom.py']),
 ('cpp-idiom', ['scripts/check_cpp_idiom.py']),
 ('hygiene', ['scripts/check_hygiene.py','--check']),
 ('test-evidence', ['scripts/measure_test_evidence.py','--check']),
]
results = []
environment = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
for name, args in checks + [('diff-whitespace', [])]:
    command = ['rtk','proxy','timeout','1800',python,'-B',*args] if args else ['rtk','proxy','timeout','60','git','diff','--check','20aa4eabf']
    (out/'logs').mkdir(exist_ok=True)
    log = out/'logs'/('gate-' + name + '.log')
    start = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, stdout=stream, stderr=subprocess.STDOUT, env=environment)
    results.append(dict(name=name, head=head, command=command, rc=result.returncode,
                        seconds=round(time.monotonic()-start,3), path=str(log),
                        size=log.stat().st_size, sha256=hashlib.sha256(log.read_bytes()).hexdigest()))
    (out/'final-gates.json').write_text(json.dumps(results,indent=2)+'\n')
    print(name, 'rc', result.returncode, flush=True)
assert subprocess.check_output(['rtk', 'proxy', 'git','rev-parse','HEAD'],text=True).strip() == head
assert all(r['rc']==0 for r in results), 'a required gate failed'
assert not subprocess.check_output(['rtk', 'proxy', 'git','status','--porcelain'],text=True).strip(), 'gates left the worktree dirty'

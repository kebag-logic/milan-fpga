"""Run assigned gates serially in the foreground and retain exact exit codes."""
from pathlib import Path
import datetime
import hashlib
import json
import os
import subprocess
import time

root = Path('$LANES/395-timing-grade')
work = Path('$VALIDATION_STORAGE/395-a393-work')
out = Path('$MANAGEMENT/2026-09-23/395-a393')
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
assert head == '3b5603e3d16a164c35329efeb633800fe4fe9f95'
base = '8bc97021f28fb7f729418d3a00851c84ea0b50fd'
md = '$VALIDATION_TOOLS/md-venv-40cdefe08ebd/bin/python'
checkpoint = '$WORKSPACE_HOME/litex-milan/work/build_ax7101_eto_tdm8dev9e9954e9/gateware/alinx_ax7101_route.dcp'
reports = work / ('reports-' + head[:9])
logs = work / ('gates-' + head[:9])
reports.mkdir(exist_ok=True)
logs.mkdir(exist_ok=True)
os.sched_setaffinity(0, sorted(os.sched_getaffinity(0))[:16])
env = dict(os.environ, PYTHONUNBUFFERED='1', PYTHONDONTWRITEBYTECODE='1',
           PYTHONHASHSEED='0', TMPDIR=str(work / 'tmp'), MAKEFLAGS='-j16',
           JAVA_TOOL_OPTIONS='-XX:ActiveProcessorCount=16', OMP_NUM_THREADS='16',
           OPENBLAS_NUM_THREADS='16', MILAN_LITEX_PYTHON='$WORKSPACE_HOME/litex-milan/venv/bin/python3')
gates = [
    ('baremetal-check', 600, ['python3', '-B', 'scripts/check_baremetal_only.py', '--check'], root),
    ('baremetal-selftest', 600, ['python3', '-B', 'scripts/check_baremetal_only.py', '--selftest'], root),
    ('standalone-pll', 900, ['python3', '-B', str(out / 'check_standalone_pll.py')], root),
    ('ci-scope-selftest', 300, ['python3', '-B', 'scripts/ci_scope.py', '--selftest'], root),
    ('docs', 600, ['python3', '-B', 'scripts/docs_check.py'], root),
    ('doc-paths', 300, ['python3', '-B', 'scripts/check_doc_paths.py'], root),
    ('toc', 300, [md, '-B', 'scripts/gen_toc.py', '--check'], root),
    ('em-dash', 300, [md, '-B', 'scripts/check_em_dash.py', '--base', base], root),
    ('feature-status', 300, ['python3', '-B', 'scripts/check_feature_status.py', '--self-test'], root),
    ('doc-style', 300, ['python3', '-B', 'scripts/check_doc_style.py'], root),
    ('doc-style-selftest', 300, ['python3', '-B', 'scripts/check_doc_style.py', '--selftest'], root),
    ('solution-docs', 300, ['python3', '-B', 'scripts/check_solution_docs.py'], root),
    ('python-idiom', 600, ['python3', '-B', 'scripts/check_py_idiom.py'], root),
    ('python-idiom-selftest', 600, ['python3', '-B', 'scripts/check_py_idiom.py', '--selftest'], root),
    ('diff-committed', 300, ['git', 'diff', '--check', base, 'HEAD'], root),
    ('diff-worktree', 300, ['git', 'diff', '--check'], root),
    ('timing-script', 300, ['python3', '-B', 'sw/litex/report_timing_grade.py', checkpoint, str(reports)], root),
    ('timing', 1800, ['$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado', '-mode', 'batch', '-nojournal', '-notrace',
                      '-log', str(reports / 'vivado.log'), '-source', str(reports / 'report.tcl')], reports),
    ('crossings', 1800, ['$WORKSPACE_HOME/Xilinx2/2026.1/Vivado/bin/vivado', '-mode', 'batch', '-nojournal', '-notrace',
                         '-log', str(reports / 'crossings.log'), '-source', str(out / 'crossings.tcl'),
                         '-tclargs', checkpoint, str(reports)], reports),
    ('builder-present', 14400, ['python3', '-B', 'sw/builder/test_builder.py', '--require-rv32', '--require-elaboration'], root),
    ('builder-absent', 14400, ['python3', '-B', str(out / 'run_builder_absent.py')], root),
]
results = []
if (out / 'gate-results.json').exists():
    prior = json.loads((out / 'gate-results.json').read_text())
    assert all(row['head'] == head for row in prior)
    results = [row for row in prior if row['returncode'] == 0]
for name, seconds, argv, cwd in gates:
    if any(row['gate'] == name for row in results):
        continue
    assert subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip() == head
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f'START {name} {started}', flush=True)
    log = logs / (name + '.log')
    command = ['timeout', '--foreground', str(seconds), *argv]
    now = time.monotonic()
    with log.open('w') as stream:
        result = subprocess.run(command, cwd=cwd, env=env, stdout=stream, stderr=subprocess.STDOUT, check=False)
    data = log.read_bytes()
    row = dict(gate=name, head=head, command=command, cwd=str(cwd), started=started,
               seconds=round(time.monotonic() - now, 2), returncode=result.returncode,
               log=str(log), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
    results.append(row)
    (out / 'gate-results.json').write_text(json.dumps(results, indent=2) + '\n')
    if len(data) <= 200000:
        (out / 'gates').mkdir(exist_ok=True)
        (out / 'gates' / log.name).write_bytes(data)
    print(f'END {name} rc={result.returncode} seconds={row["seconds"]} bytes={len(data)}', flush=True)
    if result.returncode:
        print(data.decode(errors='replace')[-6000:], flush=True)
        raise SystemExit(result.returncode)
print(f'ALL {len(results)} GATES RC 0 at {head}', flush=True)

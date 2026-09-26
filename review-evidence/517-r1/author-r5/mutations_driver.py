import hashlib
from pathlib import Path
import subprocess
from run_gate import OUT, ROOT, run

INTERNAL = '/tmp/517-a324-evidence/review-evidence/517-r1/reviews/R245-3/scripts'
EXTERNAL = '/tmp/517-a324-evidence/review-evidence/517-r1/reviews/R246-1/scripts'
paths = ['tb/verilator/milan_dp/sim_pool.py', 'tb/verilator/milan_dp/Makefile']
originals = {p: (ROOT/p).read_bytes() for p in paths}
try:
    run('mutants-internal', ['python3', 'scripts/owned_process.py', '--', 'python3',
        INTERNAL+'/mutate_pool.py', str(ROOT), str(OUT/'mutants-internal'),
        'no-exclusion', 'group-reverse-order', 'no-independent-overlap',
        'mk-drop-crflic', 'mk-swap-order', 'mk-default-one', 'mk-ignore-errors',
        'drain-blocking-write', 'drain-ignores-signals', 'final-drain-waits', 'fd-flags-not-restored'])
    assert all((ROOT/p).read_bytes() == data for p,data in originals.items())
    run('mutants-external', ['python3', 'scripts/owned_process.py', '--', 'python3',
        EXTERNAL+'/mutants.py', str(ROOT), str(OUT/'mutants-external'),
        'M03-no-exclusion', 'M04-group-order-reversed', 'M15-blocking-stdout',
        'M16-final-drain-waits', 'M17-flags-not-restored', 'M28-make-drop-prune',
        'M32-make-crflic-exclusive'])
    assert all((ROOT/p).read_bytes() == data for p,data in originals.items())
    old = subprocess.check_output(['git', 'cat-file', 'blob', '761ec858'], cwd=ROOT)
    (ROOT/paths[0]).write_bytes(old)
    run('old-runner-backpressure', ['python3', 'scripts/owned_process.py', '--',
        'python3', 'tb/verilator/milan_dp/test_sim_pool_backpressure.py'])
finally:
    for p,data in originals.items():
        (ROOT/p).write_bytes(data)
    assert all((ROOT/p).read_bytes() == data for p,data in originals.items())
print('All mutation targets restored byte-for-byte.', flush=True)

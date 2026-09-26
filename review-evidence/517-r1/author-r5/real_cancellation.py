import json
import signal
import subprocess
from run_gate import ENV, OUT, ROOT, run

for signo in (signal.SIGINT, signal.SIGTERM, signal.SIGHUP):
    signal.signal(signo, signal.SIG_DFL)
signal.pthread_sigmask(signal.SIG_SETMASK, set())
internal = '/tmp/517-a324-evidence/review-evidence/517-r1/reviews/R245-3/scripts/probe_real_cancel.py'
external = '/tmp/517-a324-evidence/review-evidence/517-r1/reviews/R246-1/scripts/real_cancel.py'
toolbin = '$VALIDATION_STORAGE/517-manager-r4/pinned-tool-bin'
rows = []
for signame, mode in [('SIGINT', 'blocked'), ('SIGTERM', 'blocked'),
                      ('SIGHUP', 'blocked'), ('SIGTERM', 'file')]:
    name = f'real-internal-{mode}-{signame}'
    rc = run(name, ['python3', 'scripts/owned_process.py', '--', 'python3', internal,
                   str(ROOT), toolbin, signame, str(OUT / name), mode])
    rows.append(dict(probe='internal', signal=signame, mode=mode, exit=rc))
    (OUT / 'real-cancellation-exits.json').write_text(json.dumps(rows, indent=2)+'\n')
suite = ROOT / 'tb/verilator/milan_dp'
dry = subprocess.check_output(['make', '-n', 'run'], cwd=suite, env=ENV, text=True)
lines = dry.replace('\\\n', ' ').splitlines()
indices = [i for i, line in enumerate(lines) if line.startswith('exec python3 sim_pool.py')]
assert len(indices) == 1, indices
plan = OUT / 'real-pool-plan.json'
plan.write_text(json.dumps(dict(lines=lines), indent=2)+'\n')
name = 'real-external-generator'
rc = run(name, ['python3', 'scripts/owned_process.py', '--', 'python3', external,
               str(suite), str(plan), str(indices[0]), '-1', str(OUT / (name+'.receipt.json'))])
rows.append(dict(probe='external', signal='SIGTERM', mode='blocked; live generator', exit=rc))
(OUT / 'real-cancellation-exits.json').write_text(json.dumps(rows, indent=2)+'\n')
assert all(row['exit'] == 0 for row in rows), rows

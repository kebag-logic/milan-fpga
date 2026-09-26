import json
import signal
import subprocess
import sys
from pathlib import Path
from run_gate import ENV, OUT, ROOT

rows = []
for index in range(20):
    def signals():
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        signal.pthread_sigmask(signal.SIG_SETMASK, set())
    result = subprocess.run(['python3', 'tb/verilator/milan_dp/test_sim_pool_backpressure.py'],
                            cwd=ROOT, env=ENV, capture_output=True, text=True,
                            preexec_fn=signals, timeout=180)
    (OUT / f'repeat-ignored-{index:02}.log').write_text(result.stdout + result.stderr)
    row = dict(repeat=index+1, exit=result.returncode,
               verdict=result.stdout.splitlines()[-1] if result.stdout else '')
    rows.append(row)
    (OUT / 'repeat-ignored-results.json').write_text(json.dumps(rows, indent=1)+'\n')
    print(json.dumps(row), flush=True)
assert all(row['exit'] == 0 and row['verdict'] == '28 backpressure controls: 28 PASS, 0 FAIL' for row in rows)

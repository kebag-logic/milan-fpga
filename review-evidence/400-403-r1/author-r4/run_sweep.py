import json
import sys
from run_gate import OUT, run
for index in range(int(sys.argv[1]), int(sys.argv[2])):
    label = f'sweep-{index}-of-5'
    rc = run(label, ['scripts/run_all_suites.sh', str(OUT / label), '--shard', f'{index}/5'])
    if rc:
        raise SystemExit(rc)

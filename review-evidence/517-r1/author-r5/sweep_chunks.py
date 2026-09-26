import json
from run_gate import OUT, run

rows = []
for index in range(5):
    name = f'sweep-{index}'
    rc = run(name, ['env', 'VERILATOR_JOBS=16', 'taskset', '-c', '16-31', 'scripts/run_all_suites.sh',
                    str(OUT / name), '--shard', f'{index}/5'])
    rows.append(dict(chunk=f'{index}/5', exit=rc))
    (OUT / 'sweep-exits.json').write_text(json.dumps(rows, indent=2)+'\n')
assert all(row['exit'] == 0 for row in rows), rows

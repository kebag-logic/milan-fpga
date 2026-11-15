"""The enlarged-row input against the tree's egress_ledger.py: all seven rows at their ledger figure, then one at 100.0 ms,
then one a bus cycle over. usage: probe_enlarged.py CHECKOUT OUTDIR"""
import json, subprocess, sys
from pathlib import Path
co, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
tool = co / 'tb/verilator/ctrl_service_budget/egress_ledger.py'
L = {'backlog.owed.if0': 63.24, 'backlog.owed_behind0.if0': 63.47, 'backlog.owed_behind1.if0': 63.69,
     'backlog.owed_behind2.if0': 63.91, 'backlog.owed_behind3.if0': 64.20,
     'backlog-owed.service.acmp.last.if0': 62.18, 'backlog-owed.service.aecp.last.if0': 61.83}
for name, change in (('unchanged', {}), ('enlarged', {'backlog.owed.if0': 100.0}),
                     ('one-cycle', {'backlog-owed.service.aecp.last.if0': 61.83001})):
    d = out / name; d.mkdir(parents=True, exist_ok=True)
    probes = [dict(probe=n, status='measured', ms=v, budget_ms=20.0, within_budget=False) for n, v in {**L, **change}.items()]
    (d / 'backlog-owed.json').write_text(json.dumps(dict(group='backlog-owed', probes=probes, passes={})))
    r = subprocess.run([sys.executable, '-I', str(tool), '--point', '8x8-1if', str(d)], capture_output=True, text=True)
    lines = r.stdout.strip().splitlines()
    print(f'{name}: rc {r.returncode}; ' + ' | '.join(l for l in lines if l.startswith(('RESULT', '- '))))

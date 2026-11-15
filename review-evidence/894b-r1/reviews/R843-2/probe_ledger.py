"""Probes of egress_ledger.py's results-directory mode. usage: probe_ledger.py CHECKOUT OUTDIR"""
import json, subprocess, sys
from pathlib import Path
co, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
tool = co / 'tb/verilator/ctrl_service_budget/egress_ledger.py'
sys.path.insert(0, str(tool.parent)); import egress_ledger as E
L = E.LEDGER['8x8-1if']
def mk(name, results, extra=None):
    d = out / name; d.mkdir(parents=True, exist_ok=True)
    probes = [dict(probe=n, status='measured', ms=v, budget_ms=20.0, within_budget=False) for n, v in L.items()]
    (d / 'backlog-owed.json').write_text(json.dumps(dict(group='backlog-owed', probes=probes, passes={})))
    if extra: (d / 'other.json').write_text(json.dumps(dict(group='other', probes=extra, passes={})))
    (d / 'results.json').write_text(json.dumps(results)); return d
cases = {
 'P1 a refused group recorded only in results.json': mk('p1', dict(refusals=['aecp-answering: no end: the run did not reach its end'], misses=[])),
 'P2 a miss recorded only in results.json': mk('p2', dict(refusals=[], misses=['aecp-x.service.aecp.last.if0: 25.000 ms over its budget 20 ms'])),
 'P3 a measured probe over budget with no within_budget key': mk('p3', {}, [dict(probe='x.service.aecp.last.if0', status='measured', ms=25.0, budget_ms=20.0)]),
}
for k, d in cases.items():
    r = subprocess.run([sys.executable, '-I', str(tool), '--point', '8x8-1if', str(d)], capture_output=True, text=True)
    print(f'{k}: rc {r.returncode}; {r.stdout.strip().splitlines()[-1]}')

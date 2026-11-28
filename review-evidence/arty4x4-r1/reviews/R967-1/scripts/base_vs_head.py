"""The existing points' harness tables at the base (c0b625d1) and the head: every value outside arty-4x4 unchanged.
usage: python3 -I base_vs_head.py BASE_TREE HEAD_TREE      (each tree is read in its own process)
       python3 -I base_vs_head.py --dump TREE"""
import importlib, json, subprocess, sys
from pathlib import Path
if sys.argv[1] == '--dump':
    sys.path.insert(0, str(Path(sys.argv[2]) / 'tb/verilator/ctrl_service_budget'))
    m = {n: importlib.import_module(n) for n in ('egress_ledger', 'load_grade', 'poll_grade', 'rows_tiers', 'rows_grade',
                                                 'edit_rows', 'bind_save')}
    out = dict(ledger=m['egress_ledger'].LEDGER, measured=m['egress_ledger'].MEASURED,
               stated=m['load_grade'].STATED_US, donor=m['load_grade'].STATED_US_DONOR,
               poll={str(tuple(k)): v for k, v in m['poll_grade'].STATED_US.items()},
               datapath=m['rows_tiers'].DATAPATH_US, long=m['rows_tiers'].LONG_RECORD_US,
               rowcosts=m['rows_grade'].ROW_COSTS, paced=m['edit_rows'].PACED,
               flight=m['bind_save'].FLIGHT_MS, saves=m['bind_save'].BURST_SAVES, ceiling=m['load_grade'].CEILING)
    print(json.dumps(out, default=str)); sys.exit(0)
def dump(tree):
    return json.loads(subprocess.run([sys.executable, '-I', '-B', __file__, '--dump', tree], check=True,
                                     capture_output=True, text=True, cwd=tree).stdout)
base, head = dump(sys.argv[1]), dump(sys.argv[2])
bad = 0
for table in base:
    for key, val in base[table].items():
        if head[table].get(key) != val:
            bad += 1; print(f'CHANGED {table}[{key}]')
    print(f'{table}: {len(base[table])} existing entries unchanged; added {sorted(set(head[table]) - set(base[table]))}')
print('RESULT', 'PASS' if not bad else f'FAIL {bad}'); sys.exit(bool(bad))

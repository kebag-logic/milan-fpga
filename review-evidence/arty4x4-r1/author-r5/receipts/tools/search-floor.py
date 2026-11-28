"""The rule's candidate search at arty-4x4 with the stated costs as they stand (the 1x1's): every queued bound and pace,
the slice by the rule, the rows and the owner findings. An indicator only: the census's measured costs decide."""
import json, sys
from pathlib import Path
from unittest.mock import patch
root = Path('$LANES/arty-4x4')
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import arty_grade, load_grade, paced_rows, queued_bound, rows_tiers as rt
point = 'arty-4x4'
i = rt.point_inputs(root, point)
load = sum(load_grade.load(root, point, load_grade.STATED_US).values())
out = []
for queued in (125, 130, 135, 140):
    for pace in range(1, paced_rows.PACE_MOST_MS + 1):
        base = i._replace(h={**i.h, 'AECP_QUEUED_MS': queued}, pace_ms=pace)
        with patch.object(rt, 'point_inputs', lambda *a: base):
            sl, margin = rt.slice_choice(root, point)
        at = base._replace(slice_us=sl)
        with patch.object(rt, 'point_inputs', lambda *a: at):
            taken = paced_rows.choice(root, point)
        rows = {n: v for n, (v, _) in rt.rows(root, point, rt.BUILT, at).items()}
        out.append(dict(queued_ms=queued, pace_ms=pace, slice_us=sl, pace_rule=taken,
                        queued_rule=queued_bound.ruled(rows['last']), rows_ms=rows,
                        owner=arty_grade.owner_findings(load, rows)))
best = min(out, key=lambda r: (len(r['owner']), r['rows_ms']['txL'] or 1e9))
print(json.dumps(dict(load=load, least_txL=min(r['rows_ms']['txL'] or 1e9 for r in out),
                      least_ACMP=min(r['rows_ms']['ACMP'] or 1e9 for r in out),
                      least_last=min(r['rows_ms']['last'] or 1e9 for r in out),
                      qualifying=[r for r in out if not r['owner']], best=best), indent=1))
Path(sys.argv[1]).write_text(json.dumps(out, indent=1) + '\n')

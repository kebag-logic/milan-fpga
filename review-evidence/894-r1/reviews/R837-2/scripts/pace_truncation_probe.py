"""Reviewer probe (R837-2): txL at 1x1/1if under the built design with THE PACE's edits counted as the firmware's
whole-millisecond gate allows. The gate (aecp_mbx.c, ready) opens once the core's millisecond clock, a read of
MBX_REG_NOW_MS, is AECP_PACE_MS past the millisecond the edit was stamped in (aecp_maps.c, a->edited_ms = a->now, the
read aecp_rx makes as it takes the record), so floor(t[k+1]) >= floor(t[k]) + P and N edits span more than
P (N - 1) - 1 ms: a window of w ms holds at most ceil((w + 1) / P) of them, where the model (paced_rows.record)
counts 1 + floor(w / P). The two differ only where w mod P is over P - 1. Read-only: patches the model in memory.
usage: python3 -I pace_truncation_probe.py TREE"""
import math
import sys
from pathlib import Path
from unittest import mock

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import paced_rows  # noqa: E402
import rows_tiers as rt  # noqa: E402


def record(row, i, w_ms):
    """paced_rows.record with the whole-millisecond count."""
    long, short = max(i.c['record.aecp'], i.c['record.aecp.long']), i.c['record.aecp']
    if row != 'txL' or not i.pace_ms:
        return long
    arrivals = i.rate['aecp'][0] + math.floor(w_ms / i.rate['aecp'][1])
    paced = min(arrivals, math.ceil((w_ms + 1) / i.pace_ms - 1e-9))
    return (paced * long + (arrivals - paced) * short) / arrivals


i = rt.point_inputs(tree, '1x1/1if')
print(f'tree: AECP_PACE_MS {i.pace_ms}, txL bound {i.tx_bound} ms')
diff = [w / 100 for w in range(1, 20000) if 1 + math.floor(w / 100 / i.pace_ms) != math.ceil((w / 100 + 1) / i.pace_ms - 1e-9)]
print(f'windows up to 200 ms where the counts differ: {len(diff)}, e.g. {diff[:3]} ... (w mod {i.pace_ms} over {i.pace_ms - 1})')
for pace in range(1, 14):
    at = i._replace(pace_ms=pace)
    model = rt.solve('txL', at, rt.BUILT)[0]
    with mock.patch.object(paced_rows, 'record', record):
        exact = rt.solve('txL', at, rt.BUILT)[0]
    r4l = rt.solve('R4L', at, rt.BUILT)[0]
    print(f'P {pace:2d}: txL model {model} ms, whole-ms count {exact} ms, R4L {r4l} ms')

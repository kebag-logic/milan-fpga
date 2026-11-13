#!/usr/bin/env python3
"""Record the model's complete inputs and arithmetic for published cost spot checks."""
import json
import math
from pathlib import Path
import sys

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root/'tb/verilator/ctrl_service_budget'))
import rows_tiers as rt
import paced_rows
import poll_grade

i = rt.point_inputs(root, '1x1/1if')
published = {
    'record.aecp.long': (89126, 940),
    'item.aecp.long': (34359, 365),
    'item.acmp': (4744, 50),
    'item.acmp_declined': (1589, 20),
    'base': (19159, 205),
    'build_one': (68951, 725),
    'AVB_INFO_CHANGED': (3196, 35),
    'AS_PATH_CHANGED': (2906, 35),
    'AMAP_LIVE_WRITE': (2333, 25),
}
checks = {}
for name, (cycles, stated) in published.items():
    required = math.ceil(cycles * 105 / 10000 / 5) * 5
    checks[name] = {'published_max_cycles':cycles, 'max_plus_5pct_rounded_up_5us':required,
                    'stated_us':stated, 'holds':stated >= required}
    assert stated >= required
print(json.dumps({'point':'1x1/1if','cost_table_us':i.c,'header_inputs':i.h,
                  'rates':i.rate,'pace_ms':i.pace_ms,'selected_pace_ms':paced_rows.choice(root),
                  'slice_choice':rt.slice_choice(root), 'bounds_ms':rt.bounds_at(i),
                  'rows':rt.rows(root, '1x1/1if', rt.BUILT, i),
                  'arithmetic_spotchecks':checks,
                  'limit':'Spot checks verify arithmetic on published maxima; they do not establish '
                          'a new maximum over unprovided raw traces or adversarial commands.'}, indent=2))

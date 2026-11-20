#!/usr/bin/env python3
"""partial.py TREE SHAPE LOG...: a running group's figures so far, by the harness's own poll_grade.held on the log as
it stands (its last, possibly cut, line dropped): the polls base, each item and the SRP record's apply, with the
heaviest srp_mbx:receive span (record.srp). SHAPE is n_if,sources,sinks (1,9,9 is 8x8/1if). Scratch only."""
import math
import sys
from pathlib import Path

tree = Path(sys.argv[1])
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import poll_grade  # noqa: E402
import shape_costs  # noqa: E402

n, so, si = (int(x) for x in sys.argv[2].split(','))
shape = shape_costs.Shape(n, so, si)
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)  # noqa: E731
for path in sys.argv[3:]:
    text = Path(path).read_text(errors='replace')
    text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    h = poll_grade.held(log, shape)['heaviest']
    srp = max((int(l.split()[3]) for l in text.splitlines() if l.startswith('SPAN ') and l.endswith(' srp_mbx:receive')),
              default=0)
    last = next((l.split()[1] for l in reversed(text.splitlines()) if l.startswith('SPAN ')), '0')
    keep = {k: v for k, v in h.items() if v}
    print(f'{path}: to sys {int(last):.3e}; record.srp {srp:,} ({rule(srp)}); ' +
          ', '.join(f'{k} {v:,} ({rule(v)})' for k, v in sorted(keep.items())))

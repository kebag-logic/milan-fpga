"""Prototype (#894 contingent ruling item 4): each participant's join intervals from a harness log. A participant is an
interface and an MRP application (the MRPDU's EtherType: MSRP 0x22EA, MVRP 0x88F5); a join interval is the time between
two consecutive MRPDUs of one participant with a join timer's run-out between them and no periodic or LeaveAll one.
usage: join_proto.py TREE LOG..."""
import sys
from bisect import bisect_left
from pathlib import Path
tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade, scenario  # noqa: E402
for p in map(Path, sys.argv[2:]):
    text = p.read_text(errors='replace'); text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    srp = scenario.CH['srp']
    joins = sorted(c for c, n in log.entries if n == 'on_join_timer')
    others = sorted(c for c, n in log.entries if n in ('on_pt_timer', 'on_la_timer'))
    by = {}
    for c, ch, i, fr in log.tx:
        if ch == srp and len(fr) > 14:
            by.setdefault((i, fr[12] << 8 | fr[13]), []).append(c)
    gaps = []
    for key, cs in by.items():
        cs.sort()
        for a, b in zip(cs, cs[1:]):
            if bisect_left(joins, b) > bisect_left(joins, a) and bisect_left(others, b) == bisect_left(others, a):
                gaps.append(((b - a) / 100_000, key))
    gaps.sort()
    print(p.stem, len(gaps), 'intervals', f'shortest {gaps[0][0]:.2f} ms {gaps[0][1]}' if gaps else '',
          f'longest {gaps[-1][0]:.2f} ms {gaps[-1][1]}' if gaps else '', 'entries', len(joins), len(others))

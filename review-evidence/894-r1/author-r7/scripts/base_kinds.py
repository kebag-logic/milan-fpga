"""The polls' base by pass kind (#908 lever a), from harness logs: each pass's base (poll_grade) with its delivery polls'
spans, classified by what the two delivery polls did: `bind` (ctrl_app_srp:deliver over SRP_D cycles: SRP's binding of a
sink, srp_mbx_bind), `latch` (ctrl_app_aecp:deliver over AECP_D cycles: the store's latch of a changed setting and the
face's status), `both`, or `ordinary`. Prints each kind's count, its heaviest base and where, and the ordinary base's
heaviest ten. usage: python3 -I base_kinds.py TREE INTERFACES SRP_D AECP_D LOG..."""
import collections
import sys
from bisect import bisect_left
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import poll_grade  # noqa: E402

n_if, srp_d, aecp_d = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
kinds = collections.defaultdict(list)
for path in map(Path, sys.argv[5:]):
    text = path.read_text(errors='replace')
    text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    traced, commits, longs = poll_grade.spans(log), poll_grade.committed(log), poll_grade.long_notices(log)
    sd, ad = traced.get('ctrl_app_srp:deliver', []), traced.get('ctrl_app_aecp:deliver', [])
    for start, end, start_sys in poll_grade.sections(traced):
        items = poll_grade.instances(log, traced, commits, start, end, longs)
        base = end - start - sum(c for _, c in items)
        def inside(rows):
            k = bisect_left(rows, (start, -1, -1))
            return rows[k][1] if k < len(rows) and rows[k][0] < end else 0
        s, a = inside(sd), inside(ad)
        kind = {(True, True): 'both', (True, False): 'bind', (False, True): 'latch'}.get((s > srp_d, a > aecp_d),
                                                                                          'ordinary')
        kinds[kind].append((base, path.stem, start_sys, s, a))
for kind, rows in sorted(kinds.items()):
    rows.sort(reverse=True)
    b, g, at, s, a = rows[0]
    print(f'{kind:9s} {len(rows):7d} passes; heaviest base {b} cycles ({g} sys {at}; srp.d {s}, aecp.d {a})')
print('# the ordinary base, the heaviest ten:')
for b, g, at, s, a in kinds['ordinary'][:10]:
    print(f'  {b:6d} {g} sys {at} srp.d {s} aecp.d {a}')

"""Each probe of a leg that ends at a response: its expectation and the response its log holds (by sequence).
usage: audit_rows.py HARNESS_DIR BUILD_JSON POINT RESULTS_DIR"""
import json, sys
from pathlib import Path
h = sys.argv[1]
sys.path[:0] = [h, str(Path(h).parents[2] / 'sw/mailbox')]
import grade, run, scenario
spec = json.load(open(sys.argv[2]))
p = scenario.point(sys.argv[3], spec)
res = Path(sys.argv[4])
seen = {}
for g in run.all_groups(p, spec):
    log = res / f'{g.name}.log'
    if not log.is_file():
        print(f'{g.name}: no log'); continue
    L = grade.parse(log.read_text(), spec['sys_hz'], spec['cpu_hz'])
    for pr in g.probes:
        for e in pr.ends:
            if not e.startswith('resp:'):
                continue
            _, ch, seq = e.split(':')
            ch, seq = int(ch), int(seq, 16)
            hits = [fr for c, k, i, fr in L.tx if k == ch and grade.response_sequence(fr) == seq]
            if not hits:
                desc = 'NO RESPONSE'
            else:
                fr = hits[0]
                mt, st = fr[15] & 0xF, fr[16] >> 3
                if fr[14] == 0xFB:
                    cmd = int.from_bytes(fr[42:44] if mt == 7 else fr[36:38], 'big') & 0x7FFF
                    desc = f'{"MVU" if mt == 7 else "AEM"} cmd={cmd:04x} status={st}'
                else:
                    desc = f'ACMP mt={mt} status={st}'
            key = (pr.path_key()[0], pr.row, pr.expect, desc)
            seen.setdefault(key, []).append(f'{g.name}:{pr.name}')
for (path, row, expect, desc), where in sorted(seen.items()):
    print(f'{path} | {row} | expect={expect or "-"} | {desc} | {len(where)}x e.g. {where[0]}')

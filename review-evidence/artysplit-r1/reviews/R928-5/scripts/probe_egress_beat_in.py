#!/usr/bin/env python3
"""Probe what the 100 Mb/s egress grade's agreement check compares.

1. A synthetic testbench log (the module's own testbench_log) with one EGRESS line's beat-in field moved by one
   datapath cycle, its last octet unchanged: does grade_case report a disagreement?
2. Over a published packet or extract: does the anchored replay's beat-in equal every EGRESS line's beat-in?

usage: python3 -B probe_egress_beat_in.py SOURCE [PACKET]
"""
import hashlib
import json
import sys
from pathlib import Path


def main(source: Path, packet: Path | None) -> int:
    sys.path.insert(0, str(source / 'tb/verilator/ctrl_service_budget'))
    import egress_mii as em
    import receipt_regrade as rr
    p = em.params(em.arty_spec())
    quiet = (p.sr_period_ps * 8 + 20 * 10**6) // p.sys_ps
    log = em.testbench_log(p, [(quiet, 2, 64), (quiet + 1, 2, 64)])
    clean = em.grade_case(log, p)
    line = [l for l in log.splitlines() if l.startswith('EGRESS ')][1]
    f = line.split()
    for label, index in (('beat-in (field 5)', 4), ('last octet (field 6)', 5)):
        g = list(f)
        g[index] = str(int(g[index]) + p.dp_ps)
        row = em.grade_case(log.replace(line, ' '.join(g)), p)
        ok, _ = em.verdict({'planted': row}, p)
        print(f'planted {label} one datapath cycle late: agree_ps={row.get("agree_ps")} verdict={"PASS" if ok else "FAIL"}')
    print(f'unplanted: agree_ps={clean.get("agree_ps")}')
    if packet is None:
        return 0
    census = json.loads((packet / 'census.json').read_text())
    limit = min(census['part_limit'] + 1, rr.EXTRACT_PART_LIMIT)
    cases = records = differing = 0
    worst = 0
    for row in census['cases']:
        path = packet / row['manifest']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        manifest = json.loads(path.read_text())
        text = rr.read_parts(path.parent, manifest['extract'], limit).decode(errors='replace')
        parsed = em.parse(text)
        recs = em.records(parsed)
        first = em.replay(recs, parsed['holds'], p, 0, anchored=True)
        cases += 1
        for (tail, t_in, end), r in zip(first, recs):
            records += 1
            delta = abs(t_in - r.egress[3])
            worst = max(worst, delta)
            differing += delta != 0
            assert tail == r.wire and end == r.egress[4], row['case']
    print(f'PACKET {cases} cases, {records} records: beat-in differs in {differing}, largest difference {worst} ps')
    return 0


if __name__ == '__main__':
    sys.exit(main(Path(sys.argv[1]), Path(sys.argv[2]) if len(sys.argv) > 2 else None))

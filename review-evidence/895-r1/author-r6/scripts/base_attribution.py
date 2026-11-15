#!/usr/bin/env python3
"""base_attribution.py HARNESS_DIR LABEL=LOG ...: each log's heaviest polls' base (poll_grade's own sections and items,
the quantity poll_grade.held holds to STATED_US' base) and the PASS line of the pass that holds it: its instructions,
instruction-fetch refills and cycles, mailbox and CSR waits, and its cycles by module. Then, for the first two logs,
each module's cycles in that pass, the second's less the first's. Equal instructions with more refills or waits is the
code's placement; more instructions is code (the harness README's PASS lines). Each log's build.json is in its
results directory's parent."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import grade  # noqa: E402
import poll_grade  # noqa: E402


def heaviest(path: Path):
    spec = json.loads((path.parent.parent / 'build.json').read_text())
    text = path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], spec['sys_hz'], spec['cpu_hz'])
    traced, commits, longs = poll_grade.spans(log), poll_grade.committed(log), poll_grade.long_notices(log)
    best = (0, 0)
    for start, end, _ in poll_grade.sections(traced):
        items = poll_grade.instances(log, traced, commits, start, end, longs)
        base = end - start - sum(cycles for _, cycles in items)
        best = max(best, (base, start))
    base, start = best
    for line in text.splitlines():
        f = line.split()
        if len(f) > 5 and f[0] == 'PASS' and int(f[3]) <= start < int(f[3]) + int(f[4]):
            fields = dict(x.split('=', 1) for x in f[5:] if '=' in x)
            mods = dict((m.rsplit(':', 1)[0], int(m.rsplit(':', 1)[1])) for m in fields.get('mods', '').split(',') if m)
            return base, int(f[4]), fields, mods
    return base, None, {}, {}


rows = []
for arg in sys.argv[2:]:
    label, path = arg.split('=', 1)
    base, cycles, fields, mods = heaviest(Path(path))
    rows.append((label, base, mods))
    print(f'{label}: heaviest base {base:,} CPU cycles ({poll_grade.__name__}); its pass {cycles:,} cycles, '
          + ' '.join(f'{k}={fields[k]}' for k in ('instr', 'fetch_rom', 'wait_mbx', 'wait_csr', 'code_words')
                     if k in fields))
if len(rows) >= 2:
    (a, ba, ma), (b, bb, mb) = rows[:2]
    print(f'base {b} - {a}: {bb - ba:+,} cycles; the pass by module, {b} - {a}:')
    for m in sorted(set(ma) | set(mb), key=lambda m: -(abs(mb.get(m, 0) - ma.get(m, 0)))):
        d = mb.get(m, 0) - ma.get(m, 0)
        if d:
            print(f'  {m:20s} {ma.get(m, 0):6,} -> {mb.get(m, 0):6,}  {d:+,}')


def polls_split(path: Path):
    """The heaviest base's section by poll function: each traced poll span inside it, CPU cycles (nested spans are
    their callers' too)."""
    spec = json.loads((path.parent.parent / 'build.json').read_text())
    text = path.read_text(errors='replace')
    log = grade.parse(text[:text.rfind('\n') + 1], spec['sys_hz'], spec['cpu_hz'])
    traced, commits, longs = poll_grade.spans(log), poll_grade.committed(log), poll_grade.long_notices(log)
    best = (0, 0, 0)
    for start, end, _ in poll_grade.sections(traced):
        items = poll_grade.instances(log, traced, commits, start, end, longs)
        best = max(best, (end - start - sum(c for _, c in items), start, end))
    _, start, end = best
    out = {}
    for name in ('adp_mbx:on_poll', 'acmp_mbx:on_poll', 'maap_mbx:poll', 'aecp_mbx:poll', 'ctrl_app_aecp:deliver',
                 'srp_mbx:poll', 'ctrl_app_srp:deliver'):
        out[name] = sum(c for s, c, _ in traced.get(name, []) if start <= s < end)
    return out


if len(sys.argv) > 3:
    split = [(arg.split('=', 1)[0], polls_split(Path(arg.split('=', 1)[1]))) for arg in sys.argv[2:4]]
    (a, sa), (b, sb) = split
    print(f'the heaviest base section by poll, {a} -> {b}:')
    for k in sa:
        print(f'  {k:22s} {sa[k]:6,} -> {sb[k]:6,}  {sb[k] - sa[k]:+,}')

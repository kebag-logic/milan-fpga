#!/usr/bin/env python3
"""Compare next-state cells of appl_table/reg_table in src/core/mrp_mad.c with a reviewer's local
transcription of IEEE 802.1Q-2018 Tables 10-3/10-4 (TSV: machine<TAB>event<TAB>space-separated cells,
'-' = no state change). The transcription is kept outside the published packet; this prints only
per-cell differences and match counts. A self-loop (state -> same state) on either side counts as '-'.
Usage: compare_state_tables.py <repo-root> <transcription.tsv>"""
import re, sys
from pathlib import Path
root = Path(sys.argv[1])
src = (root / 'src/core/mrp_mad.c').read_text()
hdr = (root / 'src/include/shish_lan/mrp.h').read_text()
enum = hdr[hdr.index('enum mrp_event {'):]; enum = enum[:enum.index('};')]
EV = [e for e in re.findall(r'MRP_EVENT_(\w+)', enum) if e != 'COUNT']
COLS = {'A': 'VO VP VN AN AA QA LA AO QO AP QP LO'.split(), 'R': 'IN LV MT'.split()}
def table(start, nostate, entry):
    body = src[src.index(start):]; body = body[:body.index('\n};')]
    body = re.sub(r'/\*.*?\*/', '', body, flags=re.S)
    cells = [None if m.group(0) == nostate else m.group(1)
             for m in re.finditer(nostate + r'\b|' + entry, body)]
    return cells
code = {'A': table('appl_table[MRP_EVENT_COUNT]', '_X', r'_S\(\s*TX_MSG_\w+\s*,\s*MRP_APPL_STATE_(\w+)\s*\)'),
        'R': table('reg_table[MRP_EVENT_COUNT]', '_RX', r'_RE\(\s*REG_IND_\w+\s*,\s*REG_TIMER_\w+\s*,\s*MRP_REG_STATE_(\w+)\s*\)')}
for k, n in (('A', 12), ('R', 3)):
    assert len(code[k]) == len(EV) * n, (k, len(code[k]), len(EV) * n)
match = {'A': 0, 'R': 0}; diff = []
for line in Path(sys.argv[2]).read_text().splitlines():
    if not line.strip() or line.startswith('#'): continue
    m, ev, cells = line.split('\t'); cells = cells.split()
    cols = COLS[m]; i = EV.index(ev); n = len(cols)
    for j, (want, st) in enumerate(zip(cells, cols)):
        got = code[m][i * n + j]
        got = '-' if got in (None, st) else got
        want = '-' if want == st else want
        if got == want: match[m] += 1
        else: diff.append(f'{"Applicant" if m == "A" else "Registrar"} {ev:10s} {st}: code -> {got}, table -> {want}')
print(f'Applicant cells matching: {match["A"]}; Registrar cells matching: {match["R"]}; differing: {len(diff)}')
print('\n'.join(diff))

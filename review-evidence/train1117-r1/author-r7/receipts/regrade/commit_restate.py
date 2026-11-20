#!/usr/bin/env python3
"""commit_restate.py TREE SPEC.json: the statements SPEC restates, by the unchanged rule (the most measured plus 5 %,
rounded up to 5 us), as edits to TREE's harness tables, each with its measurement: SPEC is a list of
{"table": own81|e1|two|one|s2|s1|paced, "point": ..., "key": ..., "us": N, "cycles": C, "where": "..."}.
8x8/1if's own costs go into load_grade.OWN with their OWN_MEASURED entries (own_findings checks them); the polls'
into poll_grade's EIGHT_ONE, ONE or TWO; 8x8/2if's and 1x1/1if's records and events into STATED_US and
STATED_US_DONOR; a paced record into edit_rows.PACED. Each table's comment gains the measurement."""
import json
import re
import sys
from pathlib import Path

T = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
spec = json.loads(Path(sys.argv[2]).read_text())
NOTE = "On the composed flip train's final head with attempt 2's cuts (#665's ruling of 2026-11-18, item 2): "


def edit(path, f):
    p = T / path; p.write_text(f(p.read_text()))


def own81(t, e):
    m = re.search(r"OWN = \{'8x8/1if': \{([^}]*)\}\}", t)
    body = m.group(1)
    body = re.sub(rf"'{re.escape(e['key'])}': \d+", f"'{e['key']}': {e['us']}", body) if f"'{e['key']}'" in body \
        else body + f", '{e['key']}': {e['us']}"
    t = t[:m.start(1)] + body + t[m.end(1):]
    m = re.search(r"OWN_MEASURED = \{'8x8/1if': \{(.*?)\}\}\n", t, re.S)
    body = m.group(1)
    entry = f"'{e['key']}': ({e['cycles']:_}, '{e['where']}')"
    if f"'{e['key']}': (" in body:
        body = re.sub(rf"'{re.escape(e['key'])}': \([^)]*\)", entry, body)
    else:
        body = body.rstrip() + ',\n                            ' + entry
    return t[:m.start(1)] + body + t[m.end(1):]


def poll(table):
    def f(t, e):
        m = re.search(rf'^{table} = dict\((.*?)\)', t, re.S | re.M)
        body, n = re.subn(rf"\b{e['key']}=\d+", f"{e['key']}={e['us']}", m.group(1))
        assert n == 1, (table, e)
        return t[:m.start(1)] + body + t[m.end(1):]
    return f


def stated_tables(t, e):
    n = 0
    for table in ('STATED_US', 'STATED_US_DONOR'):
        i = t.index(f'\n{table} = {{') + 1
        j = t.index(f"'{e['point']}'", i); k = t.index('}', j)
        seg, c = re.subn(rf"'{re.escape(e['key'])}': \d+", f"'{e['key']}': {e['us']}", t[j:k])
        n += c; t = t[:j] + seg + t[k:]
    assert n >= 1, e
    return t


def paced(t, e):
    i = t.index('PACED = {'); j = t.index(f"'{e['point']}': {{", i); k = t.index('}', j)
    seg, n = re.subn(rf"('{re.escape(e['key'])}': )\d+", rf"\g<1>{e['us']}", t[j:k])
    assert n == 1, e
    return t[:j] + seg + t[k:]


FILES = {'own81': ('load_grade.py', own81), 'e1': ('poll_grade.py', poll('EIGHT_ONE')), 'two': ('poll_grade.py', poll('TWO')),
         'one': ('poll_grade.py', poll('ONE')), 's2': ('load_grade.py', stated_tables), 's1': ('load_grade.py', stated_tables),
         'paced': ('edit_rows.py', paced)}
notes = {}
for e in spec:
    path, f = FILES[e['table']]
    edit(path, lambda t, f=f, e=e: f(t, e))
    notes.setdefault(path, []).append(f"{e['point']} {e['key']} {e['cycles']:,} CPU cycles ({e['where']}), {e['us']} us")
ANCHORS = {'load_grade.py': "OWN = {'8x8/1if'", 'poll_grade.py': 'EIGHT_ONE = dict(', 'edit_rows.py': 'PACED = {'}
for path, items in notes.items():
    p = T / path; t = p.read_text(); i = t.index(ANCHORS[path])
    text = NOTE + '; '.join(items) + ', each by the rule.'
    words, lines, line = text.split(), [], '#:'
    for w in words:
        if len(line) + 1 + len(w) > 118:
            lines.append(line); line = '#:'
        line += ' ' + w
    lines.append(line)
    p.write_text(t[:i] + '\n'.join(lines) + '\n' + t[i:])
print('restated', len(spec), 'statements in', ', '.join(notes))

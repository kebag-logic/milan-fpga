#!/usr/bin/env python3
"""restate.py TREE KEY=VALUE...: the statement tables restated by real edits in TREE's harness (scratch), the keys:
paced1x1 (edit_rows.PACED 1x1/1if one-row edit), own81.<cost> (load_grade.OWN 8x8/1if), e1.<item> (poll_grade
EIGHT_ONE), two.<item> (poll_grade TWO), s2.<cost> (load_grade.STATED_US and STATED_US_DONOR at 8x8/2if)."""
import re
import sys
from pathlib import Path
H = Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'
def sub(path, pat, rep, count=1):
    p = H / path; t = p.read_text(); t2, n = re.subn(pat, rep, t, count=count)
    assert n == count, (path, pat, n); p.write_text(t2)
for kv in sys.argv[2:]:
    k, v = kv.split('='); v = int(v)
    if k == 'paced1x1':
        sub('edit_rows.py', r"(PACED = \{'1x1/1if': \{'a one-row edit': )\d+", rf'\g<1>{v}')
    elif k.startswith('paced.'):
        _, point, member = k.split('.', 2)
        member = {'row': 'a one-row edit', 'setcfg': 'an accepted SET_CONFIGURATION'}[member]
        p = H / 'edit_rows.py'; t = p.read_text()
        i = t.index("PACED = {"); j = t.index(f"'{point}': {{", i); kk = t.index('}', j)
        seg = t[j:kk]; seg2, n = re.subn(rf"('{member}': )\d+", rf'\g<1>{v}', seg); assert n == 1, (point, member)
        p.write_text(t[:j] + seg2 + t[kk:])
    elif k.startswith('own81.'):
        c = k.split('.', 1)[1]
        p = H / 'load_grade.py'; t = p.read_text()
        m = re.search(r"OWN = \{'8x8/1if': \{([^}]*)\}\}", t); body = m.group(1)
        if f"'{c}'" in body:
            body = re.sub(rf"'{re.escape(c)}': \d+", f"'{c}': {v}", body)
        else:
            body = body + f", '{c}': {v}"
        p.write_text(t[:m.start(1)] + body + t[m.end(1):])
    elif k.startswith('e1.') or k.startswith('two.'):
        name, item = k.split('.', 1)
        table = 'EIGHT_ONE' if name == 'e1' else 'TWO'
        p = H / 'poll_grade.py'; t = p.read_text()
        m = re.search(rf'^{table} = dict\((.*?)\)', t, re.S | re.M); body = m.group(1)
        body2, n = re.subn(rf'\b{item}=\d+', f'{item}={v}', body); assert n == 1, (table, item)
        p.write_text(t[:m.start(1)] + body2 + t[m.end(1):])
    elif k.startswith('s2.'):
        c = k.split('.', 1)[1]
        p = H / 'load_grade.py'; t = p.read_text()
        n_tot = 0
        for table in ('STATED_US', 'STATED_US_DONOR'):
            i = t.index(f'\n{table} = {{') + 1
            j = t.index("'8x8/2if'", i)
            k2 = t.index('}', j)
            seg = t[j:k2]
            seg2, n = re.subn(rf"'{re.escape(c)}': \d+", f"'{c}': {v}", seg)
            n_tot += n
            t = t[:j] + seg2 + t[k2:]
        assert n_tot >= 1, (c, n_tot)
        p.write_text(t)
    else:
        raise SystemExit(f'unknown key {k}')
print('restated', ' '.join(sys.argv[2:]))

"""Desk projection (#955): the row rules at a tree with each thin record at its worse value plus the rule.

usage: python3 -I project.py ROOT [scenario ...]
Each scenario is name=value pairs joined by ',': edit=US (1x1/1if one-row edit), long8=US (8x8/1if largest legal
command), aecp1=US (1x1/1if ordinary AECP record, both columns), and any load_grade cost key at a point,
'P:key=US' (e.g. 1x1/1if:record.srp=300). Prints every row at the three points and every finding of the flip
check's, the load gate's, the queued bound's, the pace's and the shapes' rules.
"""
import contextlib, copy, io, sys
from pathlib import Path
from unittest import mock

root = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(root / 'tb/verilator/ctrl_service_budget'))
import load_grade, rows_tiers as rt, edit_rows, paced_rows, queued_bound, flip_grade, shape_costs  # noqa: E402
import poll_grade  # noqa: E402
POLLS = {'poll1': shape_costs.Shape(1, 2, 2), 'poll8': shape_costs.Shape(1, 9, 9)}

BASE = dict(pin=copy.deepcopy(load_grade.STATED_US), donor=copy.deepcopy(load_grade.STATED_US_DONOR),
            paced=copy.deepcopy(edit_rows.PACED), long=dict(rt.LONG_RECORD_US),
            polls={k: dict(poll_grade.STATED_US[v]) for k, v in POLLS.items()})


OWN8 = {}


def apply(spec):
    OWN8.clear()
    pin, donor = copy.deepcopy(BASE['pin']), copy.deepcopy(BASE['donor'])
    paced, long = copy.deepcopy(BASE['paced']), dict(BASE['long'])
    polls = copy.deepcopy(BASE['polls'])
    for part in filter(None, spec.split(',')):
        k, v = part.split('=')
        v = int(v)
        if k == 'edit':
            paced['1x1/1if']['a one-row edit'] = v
        elif k == 'setcfg':
            paced['1x1/1if']['an accepted SET_CONFIGURATION'] = v
        elif k == 'long8':
            long['8x8/1if'] = v
        elif k == 'long1':
            long['1x1/1if'] = v
        elif k == 'aecp1':
            pin['1x1/1if']['record.aecp'] = v
            donor['1x1/1if']['record.aecp'] = v
        elif k.startswith('own8:'):
            # train1117 addition: 8x8/1if's own statements (load_grade.OWN), e.g. own8:record.srp=380
            OWN8[k.split(':')[1]] = v
        elif k.split(':')[0] in POLLS:
            polls[k.split(':')[0]][k.split(':')[1]] = v
        elif ':' in k:
            p, key = k.split(':')
            pin[p][key] = v
            if key in donor.get(p, {}):
                donor[p][key] = v
        else:
            raise SystemExit(f'unknown {k}')
    return pin, donor, paced, long, polls


def run(spec):
    pin, donor, paced, long, polls = apply(spec)
    pts = ('1x1/1if', '8x8/1if', '8x8/2if')
    with contextlib.ExitStack() as st:
        for tbl, new in ((load_grade.STATED_US, pin), (load_grade.STATED_US_DONOR, donor)):
            for p in tbl:
                st.enter_context(mock.patch.dict(tbl[p], new[p]))
        for p in edit_rows.PACED:
            st.enter_context(mock.patch.dict(edit_rows.PACED[p], paced[p]))
        st.enter_context(mock.patch.dict(edit_rows.EDIT_RECORD_US, {p: max(m.values()) for p, m in paced.items()}))
        st.enter_context(mock.patch.dict(rt.LONG_RECORD_US, long))
        st.enter_context(mock.patch.dict(load_grade.OWN['8x8/1if'], OWN8))
        for k, shape in POLLS.items():
            st.enter_context(mock.patch.dict(poll_grade.STATED_US[shape], polls[k]))
        st.enter_context(mock.patch.dict(rt.LONG_NOTICE_US, {
            p: poll_grade.stated_us(shape_costs.of_point(p))[poll_grade.LONG] for p in rt.LONG_NOTICE_US}))
        out = []
        for p in pts:
            i = rt.point_inputs(root, p)
            b = rt.bounds_at(i)
            for row, (w, terms) in rt.rows(root, p, rt.BUILT, i).items():
                out.append((p, row, w, b[row]))
        f = []
        f += rt.findings(root, rt.BUILT, ('1x1/1if',))
        f += queued_bound.statements(root)
        f += rt.tx_statements(root, ('1x1/1if',))
        f += flip_grade.tx_held(root, ('8x8/1if',))
        f += flip_grade.findings(root, ceiling={'8x8/1if': 0.75})  # the flip's points: 8x8/1if 0.75
        f += load_grade.findings(root)  # 1x1/1if 0.70, both columns
        f += paced_rows.statements(root)
        f += shape_costs.findings(root)
        loads = {p: sum(load_grade.load(root, p, load_grade.STATED_US).values()) for p in ('1x1/1if', '8x8/2if', '8x8/1if')}
        loads['1x1/1if donor'] = sum(load_grade.load(root, '1x1/1if', load_grade.STATED_US_DONOR).values())
        pace = paced_rows.choice(root)
        f += [x for x in flip_grade.findings(root, ceiling={'8x8/2if': 0.70}) if spec == '']  # shown once
    return out, f, loads, pace


for spec in ['', *sys.argv[2:]]:
    rows, found, loads, pace = run(spec)
    print(f'## scenario: {spec or "base (as stated)"}')
    print('| Point | Row | W, ms | Bound, ms | Margin, ms |')
    print('|---|---|---:|---:|---:|')
    for p, row, w, b in rows:
        print(f'| {p} | {row} | {"none" if w is None else f"{w:.2f}"} | {b} | {"" if w is None else f"{b - w:+.2f}"} |')
    print('loads: ' + ', '.join(f'{k} {v:.4f}' for k, v in loads.items()) + f'; the pace the model takes: {pace} ms')
    for line in found:
        print('BREAKS', line)
    print('RESULT:', 'BREAKS' if found else 'HOLDS')
    print()

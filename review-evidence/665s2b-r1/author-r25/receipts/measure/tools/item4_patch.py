"""Item 4 of the round 25 ruling (#665 issuecomment-6751196896): the load gate's ceiling of 0.70 at 1x1/1if and
8x8/2if; 32x32/2if reported, not held, pending the owner's choice, with the compute its graded load would need for
0.70; a control that a held point is held. usage: python3 -I item4_patch.py LANE"""
import sys
from pathlib import Path

lane = Path(sys.argv[1])


def rep(t, a, b):
    assert t.count(a) == 1, (t.count(a), a)
    return t.replace(a, b)


p = lane / 'tb/verilator/ctrl_service_budget/load_grade.py'
t = p.read_text()
t = rep(t, """At or above 1.0 no ordering of the work bounds a row; CEILING leaves room for the rows (#665
issuecomment-6734415848, item 2: 0.70 at 8x8/2if and 32x32/2if). No term is kept as a margin: each has its source,
and one without a source fails.""", """At or above 1.0 no ordering of the work bounds a row; CEILING leaves room for the rows: 0.70 at 1x1/1if and 8x8/2if
(#665 issuecomment-6751196896, item 4). 32x32/2if is reported, not held, pending the owner's choice between more
compute and contract rates per shape; the table gives the compute its graded load would need for 0.70, its load over
0.70, since every stated cost is CPU time at the split CPU's clock. No term is kept as a margin: each has its source,
and one without a source fails.""")
t = rep(t, """#: The ceiling a point's load is held to (#665 issuecomment-6734415848, item 2); 1x1/1if is reported, not held.
CEILING = {'8x8/2if': 0.70, '32x32/2if': 0.70}""", """#: The ceiling a point's load is held to (#665 issuecomment-6751196896, item 4); 32x32/2if is reported, not held,
#: pending the owner's choice (more compute, or contract rates per shape).
CEILING = {'1x1/1if': 0.70, '8x8/2if': 0.70}
#: What the table says in a point's ceiling column where CEILING holds none.
PENDING = 'reported, pending the owner'
#: The load the compute factor is reported against: the ceiling the held points are held to.
TARGET = 0.70""")
t = rep(t, '''    """The load table: each point's load at the pin and with tsn-c-stack#32 (graded), its ceiling, its pass's own cost
    and every graded term by share."""
    lines = ['| Point | Load at the pin | Load with tsn-c-stack#32 (graded, owed to the pin move) | Ceiling | '
             'A pass\\'s own cost, us | Terms by share (graded) |',
             '|---|---:|---:|---:|---:|---|']''', '''    """The load table: each point's load at the pin and with tsn-c-stack#32 (graded), its ceiling, the compute the
    graded load would need for TARGET (its load over TARGET, at least 1), its pass's own cost and every graded term by
    share."""
    lines = ['| Point | Load at the pin | Load with tsn-c-stack#32 (graded, owed to the pin move) | Ceiling | '
             f'Compute for {TARGET:.2f} | A pass\\'s own cost, us | Terms by share (graded) |',
             '|---|---:|---:|---:|---:|---:|---|']''')
t = rep(t, """            lines.append(f'| {point} | none | none | {CEILING.get(point, "reported")} | | no stated cost {missing} |')""",
        """            lines.append(f'| {point} | none | none | {CEILING.get(point, PENDING)} | | | no stated cost {missing} |')""")
t = rep(t, """        lines.append(f"| {point} | {sum(pin.values()):.3f} | {sum(terms.values()):.3f} | "
                     f"{CEILING.get(point, 'reported')} | {pass_own_us(root, point, table):.0f} | "
                     + ', '.join(f'{t} {v:.3f}' for t, v in ranked) + ' |')""",
        """        total = sum(terms.values())
        lines.append(f"| {point} | {sum(pin.values()):.3f} | {total:.3f} | {CEILING.get(point, PENDING)} | "
                     f"{max(1.0, total / TARGET):.2f}x | {pass_own_us(root, point, table):.0f} | "
                     + ', '.join(f'{t} {v:.3f}' for t, v in ranked) + ' |')""")
t = rep(t, """    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['record.acmp'] = 100_000
    if not any('8x8/2if: the load' in f for f in findings(root, raised, {'8x8/2if': 0.70})):
        escaped.append('a cost over the ceiling')
""", """    raised = {p: dict(v) for p, v in base.items()}
    raised['8x8/2if']['record.acmp'] = 100_000
    if not any('8x8/2if: the load' in f for f in findings(root, raised, {'8x8/2if': 0.70})):
        escaped.append('a cost over the ceiling')
    # each point the ruling holds (#665 issuecomment-6751196896, item 4), held by the gate's own ceiling: a cost raised
    # at 1x1/1if and at 8x8/2if until the load passes 0.70 must fail the gate as it stands
    for point in ('1x1/1if', '8x8/2if'):
        over = {p: dict(v) for p, v in base.items()}
        over[point]['record.acmp'] = 100_000
        if CEILING.get(point) != 0.70 or not any(f'{point}: the load' in f for f in findings(root, over)):
            escaped.append('a held point not held')
            break
""")
t = rep(t, """CONTROLS = ('a cost over the ceiling', 'a stated cost missing', 'the retained retry counted once a record',
""", """CONTROLS = ('a cost over the ceiling', 'a held point not held', 'a stated cost missing',
            'the retained retry counted once a record',
""")
p.write_text(t)

p = lane / 'tb/verilator/ctrl_service_budget/README.md'
t = p.read_text()
t = rep(t, "A pass's own cost is no source and is reported beside the load. A point over its ceiling, 0.70 at 8x8/2if and "
        "32x32/2if, fails the gate,",
        "A pass's own cost is no source and is reported beside the load. The ceiling is 0.70 at 1x1/1if and 8x8/2if "
        "(#665, the round 25 ruling, item 4); 32x32/2if is reported, pending the owner's choice between more compute and "
        "contract rates per shape, with the compute its graded load would need for 0.70. A point over its ceiling fails "
        "the gate,")
t = rep(t, "The load gate has nine planted defects and one an arrival bound,",
        "The load gate has ten planted defects and one an arrival bound,")
t = rep(t, "a cost raised over the ceiling at 8x8/2if, a cost the load needs missing",
        "a cost raised over the ceiling at 8x8/2if, a cost raised at 1x1/1if and at 8x8/2if that the gate's own ceiling "
        "must hold (`load_grade.CEILING`), a cost the load needs missing")
p.write_text(t)
print('item 4 applied')

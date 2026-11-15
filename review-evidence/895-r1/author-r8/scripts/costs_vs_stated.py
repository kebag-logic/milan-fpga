#!/usr/bin/env python3
"""costs_vs_stated.py TREE POINT COSTS_DIR LABEL=RESULTS_DIR...: every stated cost the rows by every source read at a
point, against that point's legs by the rule (the most measured plus 5 %, rounded up to 5 us at 100 CPU cycles a us).

TREE is the tree whose tables are surveyed (its tb/verilator/ctrl_service_budget modules are imported from it, so
each table is the tree's own). COSTS_DIR holds round 1's parsers' output over the same legs (costs.sh: costs.txt,
events.json, aecp.json). Each RESULTS_DIR is a graded run.py --out directory (results.json and the group logs), its
build.json beside it or in its parent; LABEL names it in the report.

Measurements, each the most over every instance of every leg given:
  parser    costs.txt's keys (records, events, a centisecond, a pass's events' fixed part, the polls' items) and
            events.json's coalesced datapath events (eventcost.py: from the take that returned the event to the next
            take, less the TICK spans inside)
  harness   each group's results.json: poll_grade.held's heaviest base and items, whole_grade.held's heaviest pass
            given whole (the gate's own quantities), over every group of arm A, the answering-every-port and the
            valid-destinations arms, and arm B's aecp and aecp-largest-notice (record_classes.HELD_IN_ARM_B; the 8x8
            shape's largest notice is measured there)
  classes   record_classes.py's AECP records by class (its read_leg, classes and held): the held legs' records only
  datapath  reported beside DATAPATH_US, not held: each datapath-events pass that took one coalesced event alone,
            the event's take to the pass's first service_rx less the TICK spans inside, which also holds the empty
            take a pass's events' fixed part (events_none) charges; DATAPATH_US is held to eventcost.py's take and
            sinks, the measure #894 states it by (issuecomment-6872978311)
Tables: load_grade.STATED_US and STATED_US_DONOR, poll_grade.STATED_US, whole_grade.stated_us (ctrl_loop.h's pass
costs), rows_grade.ROW_COSTS, rows_tiers.DATAPATH_US, LONG_NOTICE_US and LONG_RECORD_US, edit_rows.EDIT_RECORD_US.
A cost no leg stages is reported "not staged" (its statement is derived, as the table's comment says). record.aecp is
the ruled AECP record (the ruling of 2026-11-14 on #895's composition, item 3) and is reported, not counted.
Prints the table, then 'UNDER n' (the count of statements below their rule figure, the ruled one apart); exit 1
when n > 0."""
import bisect
import json
import math
import sys
from pathlib import Path

tree, point, costs_dir = Path(sys.argv[1]).resolve(), sys.argv[2], Path(sys.argv[3])
legs = [(a.split('=', 1)[0], Path(a.split('=', 1)[1])) for a in sys.argv[4:]]
H = tree / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(H))
import edit_rows  # noqa: E402
import grade  # noqa: E402
import load_grade  # noqa: E402
import poll_grade  # noqa: E402
import record_classes  # noqa: E402
import rows_grade  # noqa: E402
import rows_tiers  # noqa: E402
import whole_grade  # noqa: E402

N_IF = load_grade.POINTS[point]['n_if']
CPU_PER_US = 100
DATAPATH_TYPES = {6: 'AVB_INFO_CHANGED', 7: 'AS_PATH_CHANGED', 8: 'AMAP_LIVE_WRITE'}


def rule(cycles: int) -> int:
    """The stated cost a most-measured figure owes: plus 5 %, rounded up to 5 us."""
    return int(math.ceil(cycles * 1.05 / CPU_PER_US / 5 - 1e-9) * 5)


most: dict[str, tuple[int, str]] = {}


def note(key: str, cycles: int, where: str) -> None:
    if cycles > most.get(key, (-1, ''))[0]:
        most[key] = (cycles, where)


# parser: round 1's
for line in (costs_dir / 'costs.txt').read_text().splitlines():
    f = line.split()
    if len(f) > 6 and f[0] == point and f[2] == 'most':
        note('parser.' + f[1], int(f[3].replace(',', '')), line.split('; ', 1)[1])
events = json.loads((costs_dir / 'events.json').read_text())
for code, kind in DATAPATH_TYPES.items():
    # eventcost.py names an interface-0 event by its type; an event of interface 1 carries 0x100 in its type word
    for key, at in ((kind, 'interface 0'), (str(0x100 + code), 'interface 1')):
        if key in events:
            note('parser.datapath.' + kind, events[key]['most_cycles'], f"eventcost, {at}, {events[key]['taken']} taken")
aecp_json = costs_dir / 'aecp.json'
if aecp_json.is_file():
    for kind, v in json.loads(aecp_json.read_text()).items():
        if isinstance(v, dict) and 'most_cycles' in v:
            note('parser.aecp.' + kind, v['most_cycles'], f"aecp_kinds, {v.get('where', '')}")


def spec_of(results: Path) -> dict:
    p = next(q for q in (results / 'build.json', results.parent / 'build.json') if q.is_file())
    return json.loads(p.read_text())


def datapath(text: str) -> list[tuple[str, int]]:
    """Each pass that took one coalesced datapath event alone: (its kind, the take to the first service_rx, less the
    TICK spans inside, CPU cycles)."""
    written, passes, takes, rx, ticks, words = [], [], [], [], [], []
    for line in text.splitlines():
        f = line.split()
        if not f:
            continue
        if f[0] == 'EVW':
            words.append(int(f[3], 16))
            if len(words) == 4:
                written.append(words[0] & 0xffff)
                words = []
        elif f[0] == 'PASS':
            passes.append((int(f[3]), int(f[4])))
        elif f[0] == 'CALL' and f[3] == 'mbx_event_take':
            takes.append(int(f[2]))
        elif f[0] == 'CALL' and f[3] == 'ctrl_loop:service_rx':
            rx.append(int(f[2]))
        elif f[0] == 'SPAN' and f[5] == 'ctrl_loop:dispatch_ticks':
            ticks.append((int(f[2]), int(f[3])))
    takes.sort(); rx.sort(); ticks.sort()
    tick_at = [s for s, _ in ticks]
    out, taken = [], 0
    for start, cycles in passes:
        end = start + cycles
        firsts = rx[bisect.bisect_left(rx, start):bisect.bisect_left(rx, end)]
        if not firsts:
            continue
        stop = firsts[0]
        mine = takes[bisect.bisect_left(takes, start):bisect.bisect_left(takes, stop)]
        got = len(mine) if len(mine) == 8 else len(mine) - 1
        kinds = written[taken:taken + max(got, 0)]
        taken += max(got, 0)
        if got == 1 and kinds and kinds[0] in DATAPATH_TYPES:
            lo, hi = bisect.bisect_left(tick_at, mine[0]), bisect.bisect_left(tick_at, stop)
            out.append((DATAPATH_TYPES[kinds[0]], stop - mine[0] - sum(d for _, d in ticks[lo:hi])))
    return out


# harness, classes and datapath, leg by leg
stated_classes = record_classes.statements(point, tree)
for label, results in legs:
    spec = spec_of(results)
    variant = spec.get('variant') or 'none'
    for g in json.loads((results / 'results.json').read_text())['results']:
        if variant == 'answering-ports' and g['group'] not in record_classes.HELD_IN_ARM_B:
            continue
        for src, short in (('polls', 'poll'), ('stated', 'whole')):
            for kind, cycles in g['passes'][src]['heaviest'].items():
                note(f'harness.{short}.{kind}', cycles, f"{label}/{g['group']}")
    leg, _ = record_classes.read_leg(results)
    for group in leg.groups:
        for kind, r, cost, bound, why in record_classes.classes(leg, group, stated_classes):
            if record_classes.held(leg, group, kind):
                note(f'classes.{kind}', r.cycles, f'{label}/{group} ({why})')
    dp = results / 'datapath-events.log'
    if dp.is_file():
        for kind, cycles in datapath(dp.read_text(errors='replace')):
            note('datapath.' + kind, cycles, f'{label}/datapath-events, one event a pass')

# the tables and what measures each key
POLL = {'base': 'base', 'item.reclaim': 'reclaim', 'item.mrpdu': 'mrpdu', 'item.acmp': 'acmp', 'item.walk': 'walk',
        'item.aecp.notice': 'aecp', 'item.retained': 'retained'}
WHOLE = {'build': 'build', 'build_one': 'build-one', 'step': 'step'}


def sources(table: str, key: str) -> list[str]:
    """The measurements a table's key is held to."""
    if table in ('load_grade.STATED_US', 'load_grade.STATED_US_DONOR'):
        if key == 'record.aecp':
            return ['classes.other']
        if key in POLL:
            extra = ['harness.poll.record'] if key == 'item.retained' else []
            return [f'harness.poll.{POLL[key]}', f'parser.{key.replace(".notice", "")}', *extra]
        if key in WHOLE:
            return [f'harness.whole.{WHOLE[key]}', f'parser.{key}']
        if key in ('item.aecp.response', 'item.aecp.probe'):
            return [f'parser.aecp.{key.rsplit(".", 1)[1]}']
        return [f'parser.{key}']
    if table == 'poll_grade.STATED_US':
        extra = {'retained': ['harness.poll.record'], 'acmp_declined': ['parser.item.acmp_declined']}.get(key, [])
        return [f'harness.poll.{key}', *extra]
    if table == 'whole_grade.stated_us':
        return [f'harness.whole.{key}', f'parser.{ {"build-one": "build_one"}.get(key, key)}']
    if table == 'rows_grade.ROW_COSTS':
        return [f'parser.{key}']
    if table == 'rows_tiers.DATAPATH_US':
        return [f'parser.datapath.{key}']
    if table == 'rows_tiers.LONG_NOTICE_US':
        return ['harness.poll.aecp_long', 'parser.item.aecp_long']
    if table == 'rows_tiers.LONG_RECORD_US':
        return ['classes.long']
    if table == 'edit_rows.EDIT_RECORD_US':
        return ['classes.edit']
    return []


tables = {
    'load_grade.STATED_US': load_grade.STATED_US[point],
    'load_grade.STATED_US_DONOR': load_grade.STATED_US_DONOR[point],
    'poll_grade.STATED_US': poll_grade.STATED_US[N_IF],
    'whole_grade.stated_us': whole_grade.stated_us(N_IF),
    'rows_grade.ROW_COSTS': rows_grade.ROW_COSTS[point],
    'rows_tiers.DATAPATH_US': rows_tiers.DATAPATH_US[point],
    'rows_tiers.LONG_NOTICE_US': {'aecp_long': rows_tiers.LONG_NOTICE_US[point]},
    'rows_tiers.LONG_RECORD_US': {'record.aecp.long': rows_tiers.LONG_RECORD_US[point]},
    'edit_rows.EDIT_RECORD_US': {'record.aecp.edit': edit_rows.EDIT_RECORD_US[point]},
}
rows, under = [], 0
print(f'# {point}: every stated cost the rows read, against the legs by the rule (most + 5 %, up to 5 us)')
print(f'# tree {tree.name}; legs {", ".join(label for label, _ in legs)}')
print('| Table | Key | Stated us | Most measured, CPU cycles | Rule us | Measured by, where | Verdict |')
print('|---|---|---:|---:|---:|---|---|')
for table, entries in tables.items():
    for key, stated in sorted(entries.items()):
        found = [(most[s][0], s, most[s][1]) for s in sources(table, key) if s in most]
        cycles, src, where = max(found) if found else (0, '-', '-')
        need = rule(cycles)
        if cycles == 0:
            verdict = 'not staged'
        elif key == 'record.aecp':
            verdict = 'RULED (item 3): ' + ('within' if stated >= need else f'under by {need - stated}')
        elif stated < need:
            verdict = f'UNDER by {need - stated}'
            under += 1
        else:
            verdict = 'within'
        rows.append(dict(table=table, key=key, stated=stated, cycles=cycles, rule=need, source=src, where=where,
                         verdict=verdict))
        if table == 'rows_tiers.DATAPATH_US' and f'datapath.{key}' in most:
            where += f'; one-event pass {most[f"datapath.{key}"][0]:,} (reported)'
        print(f'| {table} | {key} | {stated} | {cycles:,} | {need} | {src}: {where} | {verdict} |')
print(f'UNDER {under}')
sys.exit(1 if under else 0)

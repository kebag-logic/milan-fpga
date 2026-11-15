#!/usr/bin/env python3
"""class_evidence.py TREE OUT: the AECP record classes' evidence for R836-4-F2 (lane 895 round 10), on the head's
graders (TREE's record_classes.py) and round 8/9's preserved legs.

1. Arm B's aecp-fanout at both points, record by record (record_classes.read_leg, classes, held): each accepted
   SET_CONFIGURATION, SET_STREAM_INFO and checked edit, its CPU cycles, its cost by the rule, its class's statement,
   and whether the formal measurement holds it with its command passed (as record_classes.findings does) and without
   (as round 8's survey called it).
2. The planted controls on the same evidence path as the real pass: a copy of arm B's leg at a point with one record's
   SPAN raised (an accepted SET_CONFIGURATION over the paced record; a SET_STREAM_INFO over the ordinary record), then
   record_classes.py's CLI over every leg of both points with that copy in place of arm B's, and the corrected survey
   (round10/scripts/costs_vs_stated.py) and round 8's survey at that point with it. An unplanted copy is the control
   that the copying itself changes nothing. Each run's log and rc in OUT; OUT/summary.md the table.
Read-only on TREE and on the legs."""
import json
import shutil
import subprocess
import sys
from pathlib import Path

tree, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
H = tree / 'tb/verilator/ctrl_service_budget'
sys.path.insert(0, str(H))
import record_classes as rc  # noqa: E402

B = Path('/data-2/milan/tmp/895-a775/builds')
C = Path('/data-2/milan/tmp/895-a775/r8')
M = Path('$MANAGEMENT/2026-09-23/895-a775')
LEGS = {'1x1/1if': [B / 'R8-A1-view/results', B / 'R8-N1/results', B / 'R8-W1/results', B / 'R8-B1/results'],
        '8x8/2if': [B / 'R8-A8-view/results', B / 'R8-N8/results', B / 'R9-W8/results', B / 'R8-B8/results']}
COSTS = {'1x1/1if': C / 'costs-1x1', '8x8/2if': C / 'costs-8x8'}
SURVEYS = {'corrected': M / 'round10/scripts/costs_vs_stated.py', 'round 8': M / 'round8/scripts/costs_vs_stated.py'}
#: The plants: (name, point, command, accepted only, the cycles the SPAN is raised to).
PLANTS = [('paced-over', '1x1/1if', rc.SET_CONFIGURATION, True, 40_000),
          ('stream-info-over', '1x1/1if', rc.SET_STREAM_INFO, False, 30_000),
          ('paced-over', '8x8/2if', rc.SET_CONFIGURATION, True, 60_000),
          ('stream-info-over', '8x8/2if', rc.SET_STREAM_INFO, False, 30_000)]
out.mkdir(parents=True, exist_ok=True)
lines = ['# Arm B aecp-fanout records by class (round 10, R836-4-F2)', '']


def fanout_rows(point: str) -> list[tuple]:
    leg, _ = rc.read_leg(LEGS[point][3])
    s = rc.statements(point, tree)
    return [(kind, r, cost, bound, why, rc.held(leg, 'aecp-fanout', kind, r.command),
             rc.held(leg, 'aecp-fanout', kind)) for kind, r, cost, bound, why in rc.classes(leg, 'aecp-fanout', s)]


for point in LEGS:
    lines += [f'## {point}: {LEGS[point][3].parent.name}', '',
              '| Record start (bus cycles) | Command | Status | Class | CPU cycles | Rule us | Stated us | '
              'Held (command passed) | Held (round 8 survey call) |', '|---:|---|---:|---|---:|---:|---:|---|---|']
    for kind, r, cost, bound, why, with_cmd, without in fanout_rows(point):
        if r.command in (rc.SET_CONFIGURATION, rc.SET_STREAM_INFO) or r.command in rc.EDITS:
            lines.append(f'| {r.start} | 0x{r.command:02x} {why} | {r.status} | {kind} | {r.cycles:,} | {cost} | '
                         f'{bound} | {with_cmd} | {without} |')
    lines.append('')


def planted(name: str, point: str, command: int | None, accepted: bool, cycles: int | None) -> Path:
    """A copy of arm B's leg at the point, one record's SPAN raised to `cycles` (none for the control)."""
    src = LEGS[point][3]
    dst = out / 'legs' / f"{name}-{point.replace('/', '-')}" / 'results'
    if dst.parent.exists():
        shutil.rmtree(dst.parent)
    shutil.copytree(src, dst)
    shutil.copy(src.parent / 'build.json', dst.parent / 'build.json')
    if command is None:
        return dst
    leg, _ = rc.read_leg(src)
    s = rc.statements(point, tree)
    target = next(r for kind, r, *_ in rc.classes(leg, 'aecp-fanout', s)
                  if r.command == command and (not accepted or r.status in rc.ACCEPTED))
    log = dst / 'aecp-fanout.log'
    text = log.read_text(errors='replace').splitlines(keepends=True)
    hits = [k for k, l in enumerate(text) if l.startswith(f'SPAN {target.start} ') and l.rstrip().endswith('aecp_mbx:frame')]
    assert len(hits) == 1, (name, point, len(hits))
    f = text[hits[0]].split(' ')
    assert int(f[3]) == target.cycles
    f[3] = str(cycles)
    text[hits[0]] = ' '.join(f)
    log.write_text(''.join(text))
    return dst


def run(tag: str, argv: list[str]) -> tuple[int, str]:
    p = subprocess.run([sys.executable, '-I', '-B', *argv], cwd=H, capture_output=True, text=True)
    (out / f'{tag}.log').write_text(p.stdout + p.stderr)
    (out / f'{tag}.rc').write_text(f'{p.returncode}\n')
    return p.returncode, p.stdout


rows = ['| Plant | Point | Raised record | Evidence path | rc | Its line |', '|---|---|---|---|---:|---|']
for name, point, command, accepted, cycles in [('control', '1x1/1if', None, False, None),
                                                ('control', '8x8/2if', None, False, None)] + PLANTS:
    copy = planted(name, point, command, accepted, cycles)
    legs = LEGS['1x1/1if'] + LEGS['8x8/2if']
    legs = [copy if l == LEGS[point][3] else l for l in legs]
    tag = f"{name}-{point.replace('/', '-')}"
    what = 'none' if command is None else (f"{rc.HELD_COMMANDS[command]}{' accepted' if accepted else ''} -> "
                                           f"{cycles:,} cycles")
    code, text = run(f'{tag}-record_classes', ['record_classes.py', *map(str, legs)])
    hit = next((l for l in text.splitlines() if l.startswith('REFUSED')), text.strip().splitlines()[-1])
    rows.append(f'| {name} | {point} | {what} | record_classes.py (every leg, both points) | {code} | {hit[:220]} |')
    labels = ['A', 'N', 'W', 'B']
    pl = [copy if l == LEGS[point][3] else l for l in LEGS[point]]
    for sname, script in SURVEYS.items():
        code, text = run(f'{tag}-survey-{sname.replace(" ", "")}',
                         [str(script), str(tree), point, str(COSTS[point]), *[f'{a}={l}' for a, l in zip(labels, pl)]])
        under = [l for l in text.splitlines() if 'UNDER by' in l]
        hit = under[0] if under else (text.strip().splitlines()[-1] if text.strip() else '(no output)')
        rows.append(f'| {name} | {point} | {what} | {sname} survey | {code} | {hit[:220]} |')
lines += ['## The planted controls on the real pass\'s evidence path', ''] + rows + ['']
(out / 'summary.md').write_text('\n'.join(lines))
print('\n'.join(lines))

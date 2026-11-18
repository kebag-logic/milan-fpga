"""8x8/1if's stated-table survey over the measurement's legs (round 5): two views of the legs, read only, symlinks and a
filtered results.json each, then #665 round 28's tools (costs_r5.sh) and compare_8x8_1if.py over each:
  ordinary: every group but aecp-largest-notice, whose AECP notice is the largest legal one (poll_grade's aecp_long)
            and its records the long class: the records', events', polls', builds' and items' statements;
  long:     aecp-largest-notice alone: its notice item against aecp_long, its notice kind against the same.
The datapath events are eventcost.py's over arm A's datapath-events log. record_classes.py (the tree's) holds the AECP
records by class; it is run apart. usage: python3 -I survey_r5.py TREE TOOLS OUT LEG_DIR... (each with results/ and
build.json)"""
import json
import subprocess
import sys
from pathlib import Path

tree, tools, out = (Path(a).resolve() for a in sys.argv[1:4])
import os
POINT = os.environ.get('SURVEY_POINT', '8x8/1if')
legs = [Path(a).resolve() for a in sys.argv[4:]]
LONG = 'aecp-largest-notice'
here = Path(__file__).resolve().parent


def view(name: str, keep) -> list[Path]:
    made = []
    for leg in legs:
        src = leg / 'results'
        d = out / name / leg.name
        (d / 'results').mkdir(parents=True, exist_ok=True)
        (d / 'build.json').unlink(missing_ok=True)
        (d / 'build.json').symlink_to(leg / 'build.json')
        r = json.loads((src / 'results.json').read_text())
        r['results'] = [g for g in r['results'] if keep(g['group'])]
        if not r['results']:
            continue
        (d / 'results' / 'results.json').write_text(json.dumps(r))
        for f in src.iterdir():
            if f.name != 'results.json' and keep(f.name.split('.')[0]):
                link = d / 'results' / f.name
                link.unlink(missing_ok=True)
                link.symlink_to(f)
        made.append(d)
    return made


def run(args: list, log: Path) -> int:
    with log.open('w') as f:
        return subprocess.run(args, stdout=f, stderr=subprocess.STDOUT).returncode


out.mkdir(parents=True, exist_ok=True)
harness = tree / 'tb/verilator/ctrl_service_budget'
rc = {}
for name, keep in (('ordinary', lambda g: g != LONG), ('long', lambda g: g == LONG)):
    made = view(name, keep)
    if not made:
        continue
    rc[f'{name} costs'] = run(['bash', str(here / 'costs_r5.sh'), str(tools), str(out / f'{name}-costs'), POINT, '1',
                               str(harness), *map(str, made)], out / f'{name}-costs.out')
logs = sorted(str(p) for leg in legs for p in (leg / 'results').glob('datapath-events.log'))
with (out / 'datapath.json').open('w') as f:
    rc['datapath'] = subprocess.run([sys.executable, '-I', str(tools / 'eventcost_dp.py'), str(tree), *logs],
                                    stdout=f, stderr=subprocess.STDOUT).returncode if logs else 0
if not logs:
    (out / 'datapath.json').write_text('{}')
rc['compare ordinary'] = run([sys.executable, '-I', str(here / 'compare_point.py'), str(tree),
                              str(out / 'ordinary-costs/costs.json'), str(out / 'ordinary-costs/aecp.json'),
                              str(out / 'datapath.json'), POINT], out / 'compare-ordinary.txt')
sys.path.insert(0, str(harness))
import poll_grade  # noqa: E402
import shape_costs  # noqa: E402
import math  # noqa: E402
long_us = poll_grade.stated_us(shape_costs.of_point(POINT, tree))[poll_grade.LONG]
rule = lambda c: int(math.ceil(c * 1.05 / 100 / 5 - 1e-9) * 5)  # noqa: E731
lines, over = [], 0
if (out / 'long-costs/costs.json').is_file():
    c = json.loads((out / 'long-costs/costs.json').read_text())
    k = json.loads((out / 'long-costs/aecp.json').read_text())
    for name, cycles, at in ((f'item.{poll_grade.LONG} (the polls)', c['_most_cycles'].get(f'item.{poll_grade.LONG}', 0),
                              c['_where'].get(f'item.{poll_grade.LONG}', '-')),
                             ('the notice kind (aecp_kinds.py)', k.get('notice', {}).get('most_cycles', 0),
                              k.get('notice', {}).get('where', '-'))):
        verdict = 'OVER' if rule(cycles) > long_us else 'within'
        over += verdict == 'OVER'
        lines.append(f'{name}: {cycles:,} CPU cycles, {rule(cycles)} us by the rule, against aecp_long {long_us} us at '
                     f'{POINT}: {verdict}; {at}')
(out / 'compare-long.txt').write_text('\n'.join(['# aecp-largest-notice: its notices against the largest legal '
                                                 f"notice's statement at {POINT} (poll_grade aecp_long)", *lines,
                                                 f'# {over} exceeded']) + '\n')
print(json.dumps(rc), '| long:', '; '.join(lines))
print((out / 'compare-ordinary.txt').read_text().split('\n# ', 1)[-1])
sys.exit(1 if any(rc.values()) or over else 0)

"""The polls' base and ACMP's item, pass by pass, from harness logs (#908 levers a and b): for each pass's polls
(poll_grade.sections) its base (the section less its items, poll_grade.instances), the channels committed inside the
section, and each traced module poll's span inside it; and for each ACMP item (acmp_mbx:on_poll that committed an
ACMP frame) its cycles, the acmp_mbx:on_frame spans nested in it (the redelivered records) and the rest.

usage: python3 -I base_parts.py TREE INTERFACES LOG... ; prints per log and over all logs:
  - the heaviest bases, each with its committed channels and its traced module polls;
  - the heaviest base of the passes that committed nothing, and of those by the channel set they committed;
  - the heaviest ACMP items, each split into its nested on_frame records and the rest.
"""
import collections
import sys
from bisect import bisect_left
from pathlib import Path

tree = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(tree / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import poll_grade  # noqa: E402
import scenario  # noqa: E402

n_if = int(sys.argv[2])
CH = {v: k for k, v in scenario.CH.items()}
POLLS = ('adp_mbx:on_poll', 'acmp_mbx:on_poll', 'maap_mbx:poll', 'aecp_mbx:poll', 'ctrl_app_aecp:deliver',
         'srp_mbx:poll', 'ctrl_app_srp:deliver')
SHORT = dict(zip(POLLS, ('adp', 'acmp', 'maap', 'aecp', 'aecp.d', 'srp', 'srp.d')))
by_set = collections.defaultdict(lambda: (0, ''))
heavy, acmp_items = [], []
for path in map(Path, sys.argv[3:]):
    text = path.read_text(errors='replace')
    text = text[:text.rfind('\n') + 1]
    log = grade.parse(text, 100_000_000, 100_000_000)
    traced, commits, longs = poll_grade.spans(log), poll_grade.committed(log), poll_grade.long_notices(log)
    all_commits = sorted((cycle, ch) for cycle, ch, _ in log.commits)
    cycles_only = [c for c, _ in all_commits]
    frames = traced.get('acmp_mbx:on_frame', [])
    for start, end, start_sys in poll_grade.sections(traced):
        items = poll_grade.instances(log, traced, commits, start, end, longs)
        base = end - start - sum(cycles for _, cycles in items)
        end_sys = start_sys + (end - start)
        chans = sorted({CH.get(ch, str(ch)) for cyc, ch in all_commits[bisect_left(cycles_only, start_sys):
                                                                          bisect_left(cycles_only, end_sys)]})
        polls = {}
        for label in POLLS:
            rows = traced.get(label, [])
            k = bisect_left(rows, (start, -1, -1))
            if k < len(rows) and rows[k][0] < end:
                polls[SHORT[label]] = rows[k][1]
        key = ','.join(chans) or '(none)'
        if base > by_set[key][0]:
            by_set[key] = (base, f'{path.stem} sys {start_sys}')
        heavy.append((base, path.stem, start_sys, chans, [k for k, _ in items], polls))
    rows = traced.get('acmp_mbx:on_poll', [])
    marks = commits.get(scenario.CH['acmp'], [])
    for s, cycles, s_sys in rows:
        e_sys = s_sys + cycles
        if bisect_left(marks, e_sys) == bisect_left(marks, s_sys):
            continue
        nested = [c for fs, c, _ in frames[bisect_left(frames, (s, -1, -1)):] if fs < s + cycles]
        acmp_items.append((cycles, path.stem, s_sys, len(nested), sum(nested)))

heavy.sort(key=lambda r: -r[0])
print(f'# {len(heavy)} passes; the 25 heaviest bases (CPU cycles): base, group, bus cycle, channels committed, '
      'items, module polls (cycles)')
for base, group, sys_, chans, items, polls in heavy[:25]:
    print(f'{base:7d} {group} {sys_} [{",".join(chans)}] items={items} {polls}')
print('# the heaviest base by the set of channels the pass committed')
for key, (base, where) in sorted(by_set.items(), key=lambda kv: -kv[1][0]):
    print(f'{base:7d} {key:40s} {where}')
acmp_items.sort(key=lambda r: -r[0])
print(f'# {len(acmp_items)} ACMP items; the 15 heaviest: cycles, group, bus cycle, redelivered on_frame records, their '
      'cycles, the rest')
for cycles, group, s_sys, n, nested in acmp_items[:15]:
    print(f'{cycles:7d} {group} {s_sys} records={n} {nested} rest={cycles - nested}')
rest = sorted((c - nested for c, _, _, _, nested in acmp_items), reverse=True)
print(f'# ACMP items without their nested records: the heaviest {rest[:5]}; with none nested: '
      f'{max((c for c, _, _, n, _ in acmp_items if n == 0), default=0)}')

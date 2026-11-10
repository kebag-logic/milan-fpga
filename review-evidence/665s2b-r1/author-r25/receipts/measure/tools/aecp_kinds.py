#!/usr/bin/env python3
"""Round 25 (#665, issuecomment-6751196896, item 2): AECP's owed frame by what it sends, from budget-harness logs.

usage: python3 -I aecp_kinds.py HARNESS_DIR OUT.json BUILD_DIR...

HARNESS_DIR is the tb/verilator/ctrl_service_budget directory of the tree the legs ran (its grade.py, poll_grade.py
and scenario.py read the logs). Each BUILD_DIR holds a leg's build.json and results/<group>.log. A poll's AECP item is
an aecp:transmit span inside a pass's polls that committed an AECP frame (poll_grade.instances). Its kind is read from
the AECP frames the span committed (grade.Log.tx, the channel's records by their TX_HEAD commit):
  probe     one frame, an AEM_COMMAND CONTROLLER_AVAILABLE (Milan v1.2 5.4.5.3, IEEE 1722.1-2021 7.4.34)
  response  one AEM_RESPONSE, its unsolicited flag clear (a command's answer, IEEE 1722.1-2021 9.2.1.1.5)
  notice    AEM_RESPONSE frames with the unsolicited flag set, one a registered controller, and with them at most the
            command's own response (Milan v1.2 5.4.5.1; aecp.c fan_out)
For each kind: the most CPU cycles over every instance, where, the most recipients, and the count. An item outermost
in its pass is its own (poll_grade.outermost).
"""
import json
import sys
from bisect import bisect_left, bisect_right
from pathlib import Path

harness = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(harness))
import grade  # noqa: E402
import poll_grade  # noqa: E402
import scenario  # noqa: E402

AECP = scenario.CH['aecp']


def kind_of(frames):
    """A transmit's kind from the AECP frames it committed: (kind, recipients)."""
    unsolicited = [f for f in frames if (f[15] & 15) == 1 and (f[36] & 0x80)]
    if unsolicited:
        return 'notice', len(unsolicited)
    if len(frames) == 1 and (frames[0][15] & 15) == 0 and (((frames[0][36] << 8) | frames[0][37]) & 0x7FFF) == 3:
        return 'probe', 1
    if len(frames) == 1 and (frames[0][15] & 15) == 1:
        return 'response', 1
    return 'other', len(frames)


def items(log):
    """Each pass's outermost AECP transmit that committed a frame: (start bus cycle, end bus cycle, CPU cycles)."""
    traced = poll_grade.spans(log)
    commits = poll_grade.committed(log)
    marks = commits.get(AECP, [])
    out = []
    label = poll_grade.ITEMS['aecp'][0]
    rows = traced.get(label, [])
    for start, end, _ in poll_grade.sections(traced):
        found = poll_grade.instances(log, traced, commits, start, end)
        kinds = [k for k, _ in found]
        if 'aecp' not in kinds:
            continue
        for s, cycles, s_sys in rows[bisect_left(rows, (start, -1, -1)):]:
            if s >= end:
                break
            end_sys = s_sys + cycles * log.sys_hz // log.cpu_hz
            if bisect_left(marks, end_sys) != bisect_left(marks, s_sys) and ('aecp', cycles) in found:
                out.append((s_sys, end_sys, cycles))
    return out


most = {}
for d in map(Path, sys.argv[3:]):
    spec = json.loads((d / 'build.json').read_text())
    for log_path in sorted((d / 'results').glob('*.log')):
        text = log_path.read_text(errors='replace')
        if 'RESULT' not in text:
            continue
        log = grade.parse(text, spec['sys_hz'], spec['cpu_hz'])
        tx = sorted((c, fr) for c, ch, _i, fr in log.tx if ch == AECP)
        cycles_at = [c for c, _ in tx]
        for s_sys, e_sys, cycles in items(log):
            frames = [fr for _, fr in tx[bisect_left(cycles_at, s_sys):bisect_right(cycles_at, e_sys)]]
            kind, n = kind_of(frames)
            m = most.setdefault(kind, {'most_cycles': 0, 'where': '', 'count': 0, 'most_recipients': 0})
            m['count'] += 1
            m['most_recipients'] = max(m['most_recipients'], n)
            if cycles > m['most_cycles']:
                m['most_cycles'], m['where'] = cycles, f'{d.name}/{log_path.stem} ({n} frame(s))'
Path(sys.argv[2]).write_text(json.dumps(most, indent=1) + '\n')
for k, v in sorted(most.items()):
    print(f"{k:9} most {v['most_cycles']:>7,} CPU cycles over {v['count']:>6} instance(s), at most {v['most_recipients']}"
          f" recipient(s); {v['where']}")

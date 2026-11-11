#!/usr/bin/env python3
"""Insert round 2's walk plants after the last walk- plant of tests/mutations.json, keeping the table's layout."""
import json
import sys
from pathlib import Path

root = Path(sys.argv[1])
path = root / 'tests/mutations.json'
table = json.loads(path.read_text())
source = (root / 'src/acmp.c').read_text()
TRACE = "the changed-sink walk makes the full walk's calls"
SINK = 'a completed entry leaves no sink marked'
IFACE = 'a completed entry leaves no interface marked'
ALL = ['AcmpWalk.EightSinksMatchTheFullWalk', 'AcmpWalk.OneSinkMatchesTheFullWalk',
       'AcmpWalk.ThirtyThreeSinksMatchTheFullWalk', 'AcmpWalk.ThirtyTwoSinksMatchTheFullWalk']
WIDE = ['AcmpWalk.ThirtyThreeSinksMatchTheFullWalk']


def plant(name, old, new, tests, needle):
    if source.count(old) != 1:
        raise SystemExit(name + ': anchor matches ' + str(source.count(old)) + ' times')
    kills = [{'test': t, 'needle': needle, 'arm': 'acmp_walk'} for t in tests]
    return {'name': name, 'path': 'src/acmp.c', 'old': old, 'new': new, 'kills': kills,
            'original_tests': [k['test'] for k in kills]}


new = [
    plant('walk-bind-second-word-unmarked',
          '\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tbool sw',
          '\tstruct acmp_sink *s = &a->sinks[k];\n\tif (k < 32u) {\n\t\tmark(a, k);\n\t}\n\tbool sw', WIDE, TRACE),
    plant('walk-unbind-second-word-unmarked',
          '\tstruct acmp_sink *s = &a->sinks[k];\n\tmark(a, k);\n\tif (s->state',
          '\tstruct acmp_sink *s = &a->sinks[k];\n\tif (k < 32u) {\n\t\tmark(a, k);\n\t}\n\tif (s->state', WIDE, TRACE),
    plant('walk-release-second-word-unmarked',
          '\t\t\t\t\tmark(a, k);\n\t\t\t\t\ta->sinks[k].change_owed--;',
          '\t\t\t\t\tif (k < 32u) {\n\t\t\t\t\t\tmark(a, k);\n\t\t\t\t\t}\n\t\t\t\t\ta->sinks[k].change_owed--;', WIDE, TRACE),
    plant('walk-probe-left-second-word-unmarked',
          '\t\tmark(a, o->probe_of - 1u);\n',
          '\t\tif (o->probe_of - 1u < 32u) {\n\t\t\tmark(a, o->probe_of - 1u);\n\t\t}\n', WIDE, TRACE),
    plant('walk-marks-never-cleared',
          '\tmemset(a->dirty, 0, sizeof a->dirty);\n', '', ALL, SINK),
    plant('walk-interface-marks-never-cleared',
          '\ta->dirty_if = 0u;\n', '', ALL, IFACE),
    plant('walk-clear-first-word-only',
          '\tmemset(a->dirty, 0, sizeof a->dirty);',
          '\tmemset(a->dirty, 0, sizeof a->dirty[0]);', WIDE, SINK),
]
names = {m['name'] for m in table}
if names & {m['name'] for m in new}:
    raise SystemExit('plants already present')
last = max(i for i, m in enumerate(table) if m['name'].startswith('walk-'))
table[last + 1:last + 1] = new
text = path.read_text()
indent = 2 if text.startswith('[\n  {') else None
path.write_text(json.dumps(table, indent=indent, ensure_ascii=False) + '\n')
print('inserted', len(new), 'after', table[last]['name'], 'total', len(table))

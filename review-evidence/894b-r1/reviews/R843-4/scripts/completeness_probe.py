"""Reviewer probe of record_classes.py's completeness rule (argument: the ctrl_service_budget directory to import).

In process, no file written. Each case is a pass built from the module's own synthetic passes, its completeness map
built as main() builds it (a point enters it only where the pass runs arm A there). Prints each case's findings and
whether the outcome is the expected one; exit 1 on any unexpected outcome.
"""
import copy
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]).resolve()))
import record_classes as rc  # noqa: E402

legs1, groups1, stated1 = rc.synthetic()
legs8, groups8, at8 = rc.synthetic_8x8()
own = {'1x1/1if': stated1, '8x8/1if': at8('8x8/1if'), '8x8/2if': at8('8x8/1if')}
groups = {'1x1/1if': groups1, '8x8/1if': groups8['8x8/1if']}


def arm_map(legs):
    return {leg.point: groups[leg.point] for leg in legs if leg.point in rc.COMPLETE and leg.variant == 'none'}


def run(name, legs, expect):
    found, _ = rc.findings(legs, arm_map(legs), lambda point: own[point])
    ok = all(any(e in f for f in found) for e in expect) if expect else not found
    print(f'{"ok " if ok else "BAD"} {name}: {len(found)} findings')
    for f in found:
        print('     ', f)
    return ok


def ports(legs):
    return copy.deepcopy([leg for leg in legs if leg.variant == 'answering-ports'])


def drop_setcfg(legs):
    for leg in legs:
        leg.groups['aecp-fanout'] = [r for r in leg.groups.get('aecp-fanout', []) if r.command != rc.SET_CONFIGURATION]
    return legs


def as_point(legs, point):
    for leg in legs:
        leg.point = point
    return legs


cases = [
    ('1x1/1if complete alone (as #902 held it)', copy.deepcopy(legs1), []),
    ('8x8/1if complete alone (its own requirement)', copy.deepcopy(legs8), []),
    ('both points complete', copy.deepcopy(legs1) + copy.deepcopy(legs8), []),
    ('R843-3 F2 shape: 8x8/1if complete + 1x1/1if ports leg, SET_CONFIGURATION dropped',
     copy.deepcopy(legs8) + drop_setcfg(ports(legs1)),
     ['the pass runs no arm A leg at 1x1/1if', "SET_CONFIGURATION: no answering-ports leg at 1x1/1if"]),
    ('reverse: 1x1/1if complete + 8x8/1if ports leg alone (its arm B intact)',
     copy.deepcopy(legs1) + ports(legs8), ['the pass runs no arm A leg at 8x8/1if']),
    ('8x8/1if complete + 1x1/1if ports leg intact (no arm A at 1x1/1if)',
     copy.deepcopy(legs8) + ports(legs1), ['the pass runs no arm A leg at 1x1/1if']),
    ('8x8/1if ports leg alone', ports(legs8), ['the pass runs no arm A leg at 8x8/1if']),
    ('only an uncomplete point (8x8/2if legs)', as_point(copy.deepcopy(legs8), '8x8/2if'),
     ['the pass runs no arm A leg at a point it is held at']),
    ('empty pass', [], ['the pass runs no arm A leg at a point it is held at']),
]
bad = sum(not run(*c) for c in cases)
print(f'RESULT: {"PASS" if not bad else "FAIL"}: {len(cases) - bad} of {len(cases)} as expected')
sys.exit(int(bool(bad)))

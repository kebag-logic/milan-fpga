#!/usr/bin/env python3
"""r7_buildcheck.py HARNESS NEW.log [OLD.log]: a trace written by the round-7 testbench, which names each MRPDU build's
participant (ENTRY <cycle> build_mrpdu <owner>): how many builds carry a participant, unresolved, or none; whether each
build that commits an MRPDU of its own run names that MRPDU's participant (the frames between it and the next build,
one participant's a build); and, given OLD, the round-4 trace of the same group, whether NEW equals it line for line
once the build's participant is taken off each build_mrpdu ENTRY."""
import itertools
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(sys.argv[1]) / 'tb/verilator/ctrl_service_budget'))
import grade  # noqa: E402
import mrpdu_grade as m  # noqa: E402

new = Path(sys.argv[2])
BUILD = re.compile(r'^(ENTRY \d+ build_mrpdu)(?: (if\d+ (?:MSRP|MVRP)|unresolved [0-9a-f]{8}))?$')
out = dict(trace=new.name)
if len(sys.argv) > 3:
    def stripped(lines):
        for line in lines:
            mt = BUILD.match(line.rstrip('\n'))
            yield (mt.group(1) + '\n') if mt else line
    differ = n = 0
    with Path(sys.argv[3]).open(errors='replace') as a, new.open(errors='replace') as b:
        for n, (x, y) in enumerate(itertools.zip_longest(a, stripped(b)), 1):
            differ += x != y
    out.update(lines=n, differ_once_build_participant_removed=differ)
text = new.read_text(errors='replace')
log = grade.parse(text[:text.rfind('\n') + 1], 100_000_000, 100_000_000)
builds = m.index(log)[0]
named = {b: log.owners.get((b, m.BUILD), 'none') if (b, m.BUILD) in log.owners else 'none' for b in builds}
out['builds'] = len(builds)
out['by_participant'] = {k: sum(1 for v in named.values() if (v or 'unresolved') == k) for k in sorted({v or 'unresolved' for v in named.values()})}
at = m.sends(log)[1]
sent = m.index(log)[2]
agree = disagree = 0
bad = []
for k, b in enumerate(builds):
    stop = builds[k + 1] if k + 1 < len(builds) else 1 << 62
    mine = {w for c in sent if b < c[0] < stop for w in at.get(c, ())}
    if mine and named[b] not in ('none', None):
        if named[b] in mine:
            agree += 1
        else:
            disagree += 1
            bad.append(dict(build_ms=round(b / 1e5, 3), recorded=named[b], frames=sorted(mine)))
out.update(frame_bearing_builds_agreeing=agree, disagreeing=disagree, disagreements=bad[:10])
print(json.dumps(out))

#!/bin/bash
# mkunit.sh REV US DIR: a scratch clone of REV whose ctrl_loop.h states CTRL_LOOP_SRP_UNIT_US US in the 8x8/1if shape's
# block (CTRL_LOOP_SHAPE(1u, 9u, 9u)) and nothing else, committed in the clone only: the variant in which THE DRAIN's
# unit follows a restated 8x8/1if SRP record, for measurement. Never pushed, never on a lane branch.
set -euo pipefail
T=<scratch>; REV=$1; US=$2; D=$3
$T/bin/clone.sh $REV $D > /dev/null
H=$D/sw/firmware/ctrl/loop/ctrl_loop.h
python3 -I - "$H" "$US" <<'PY'
import sys
from pathlib import Path
p, us = Path(sys.argv[1]), sys.argv[2]
lines = p.read_text().splitlines(keepends=True)
k = next(i for i, l in enumerate(lines) if l.startswith('#elif CTRL_LOOP_SHAPE(1u, 9u, 9u)'))
j = next(i for i in range(k, k + 12) if lines[i].startswith('#define CTRL_LOOP_SRP_UNIT_US '))
assert lines[j] == '#define CTRL_LOOP_SRP_UNIT_US 365u\n', lines[j]
lines[j] = f'#define CTRL_LOOP_SRP_UNIT_US {us}u\n'
p.write_text(''.join(lines))
PY
git -C $D -c user.name=scratch -c user.email=scratch@invalid commit -q -am "scratch: $REV with the 8x8/1if SRP unit at $US us, for measurement only"
echo "$D $(git -C $D rev-parse --short HEAD) $(git -C $D diff --stat HEAD~1 | tail -1)"

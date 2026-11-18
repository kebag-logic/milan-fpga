#!/bin/bash
# The instruction aid's neutrality: #931's head built without patch_sim.py, arm A's aecp-largest-notice alone; its
# record spans must equal the patched build's, cycle for cycle.
set -u
T=<scratch>
. $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
C=$T/attr/clones/931-np B=$T/attr/b/931-np
mkdir -p $B
[ -d $C ] || $T/bin/clone.sh d06ded5a $C || exit 2
echo "HEAD $(git -C $C rev-parse HEAD) dirty $(git -C $C status --porcelain --untracked-files=no | wc -l)"
python3 -B $T/tools/legs.py build $C $B/none 1x1 none 1 aecp-largest-notice > $B/none.build.log 2>&1 || exit 3
python3 -B $T/tools/legs.py run $C $B/none 1x1 none 0 1 > $B/none.run.log 2>&1; echo "run rc=$?"

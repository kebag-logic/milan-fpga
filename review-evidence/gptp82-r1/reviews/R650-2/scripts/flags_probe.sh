#!/bin/sh
# Reviewer probe: print the published flags of the phase-36 asCapable-fall
# commit and of the following thisClock commit. Instruments a COPY of the
# harness only (an extra printf); applies the named probe_mutant.py mutation
# first when NAME is not 'clean'. Usage: flags_probe.sh HEAD_TREE WORK NAME
set -e
HEAD=$1; WORK=$2; NAME=$3; HERE=$(dirname "$0")
python3 -I - "$HEAD" "$WORK.src" <<'PY'
import shutil, sys
from pathlib import Path
src, dst = Path(sys.argv[1]), Path(sys.argv[2])
if dst.exists(): shutil.rmtree(dst)
shutil.copytree(src, dst, symlinks=True)
p = dst / "tb/verilator/engine/sim_main.cpp"
t = p.read_text()
pat = '    expect("#82 Pdelay loss: thisClock is committed within 2 ms of the fall",\n'
assert t.count(pat) == 1
add = ('    if (fell && self) printf("PROBE fall flags=%x gm=%016llx self flags=%x parent=%016llx\\n",'
       ' fell->flags, (unsigned long long)fell->gm, self->flags, (unsigned long long)self->parent);\n')
p.write_text(t.replace(pat, add + pat))
PY
python3 -I "$HERE/probe_mutant.py" "$WORK.src" "$WORK" "$NAME" > /dev/null || true
cd "$WORK/tb/verilator/engine" && ./obj_dir/Vengine_sim | grep -E 'PROBE|checks:'

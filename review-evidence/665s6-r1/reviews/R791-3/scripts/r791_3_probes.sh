#!/usr/bin/env bash
# R791-3 probes, portable. Usage: r791_3_probes.sh <copy-of-clone-at-e6d27f3a> <out-dir> <verilator>
# Runs on a disposable copy only; never on the review clone.
#   P0  the split leg, the CDC check and the placement self-tests at head
#   M   the split mutant campaign (24 arms)
#   P1  sim_split.cpp minus its one 24-byte frame: the full-FIFO guard must FAIL
#   P2  P1 minus the guard, with the runt-counting arm in KL_ctrl_split: the runt check alone passes (arm survives)
set -u
SRC=$(realpath "$1"); OUT=$(realpath "$2"); V=$3
mkdir -p "$OUT"
D=$SRC/tb/verilator/milan_dp
(cd "$SRC" && make -C tb/verilator/milan_dp split VERILATOR="$V" VERILATOR_JOBS=6) > "$OUT/split-leg.log" 2>&1; echo $? > "$OUT/split-leg.rc"
(cd "$SRC" && make -C tb/verilator/milan_dp split-cdc) > "$OUT/split-cdc.log" 2>&1; echo $? > "$OUT/split-cdc.rc"
(cd "$SRC" && python3 syn/ooc/pp_placement_selftest.py && python3 syn/ooc/pp_baseline.py --selftest) > "$OUT/pp-placement.log" 2>&1; echo $? > "$OUT/pp-placement.rc"
(cd "$SRC" && VERILATOR="$V" VERILATOR_JOBS=5 make -C tb/verilator/milan_dp split-mutants) > "$OUT/split-mutants.log" 2>&1; echo $? > "$OUT/split-mutants.rc"
PROBE=$(mktemp -d); cp -a "$SRC/." "$PROBE/"; PD=$PROBE/tb/verilator/milan_dp
python3 -I - "$PD" <<'EOF'
import sys
from pathlib import Path
p = Path(sys.argv[1]) / 'sim_split.cpp'; t = p.read_text()
old = "    kept.push_back(tap_frame(kDaAdp, 0x22F0, 0xFA, 0x7Fu, 24));\n"
assert t.count(old) == 1; p.write_text(t.replace(old, ""))
EOF
make -C "$PD" split SPLIT_MDIR=obj_p1 VERILATOR="$V" VERILATOR_JOBS=3 > "$OUT/probe-p1-no-24-byte.log" 2>&1; echo $? > "$OUT/probe-p1-no-24-byte.rc"
python3 -I - "$PD" "$PROBE" <<'EOF'
import sys
from pathlib import Path
d, root = Path(sys.argv[1]), Path(sys.argv[2])
p = d / 'sim_split.cpp'; t = p.read_text()
old = '    tb.check("[TAP] the burst leaves the FIFO full to its last word", d->tap_full);\n'
assert t.count(old) == 1; p.write_text(t.replace(old, ""))
src = (root / 'hdl/milan/KL_ctrl_split.sv').read_text()
o = "      last_kept_r <= (tap_r == TAP_BODY_S) || ((tap_r == TAP_HEAD1_S) && accept_w);"
assert src.count(o) == 1
(root / 'KL_ctrl_split_runt.sv').write_text(src.replace(o, o[:-1] + " || (tap_r == TAP_HEAD0_S);"))
EOF
make -C "$PD" split SPLIT_MDIR=obj_p2 VERILATOR="$V" VERILATOR_JOBS=8 CTLS_SRC="$PROBE/KL_ctrl_split_runt.sv" > "$OUT/probe-p2-runt-without-fill.log" 2>&1; echo $? > "$OUT/probe-p2-runt-without-fill.rc"
rm -rf "$PROBE"

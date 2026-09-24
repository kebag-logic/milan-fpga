#!/bin/sh
# Probe: which "pending" boundary does tkdiag T17 grade?
# Builds tkdiag against a copy of KL_media_clock_restart.sv in which a request
# also merges while the stream has adopted its new level but no PDU carrying it
# has completed yet (hold_r == 0), i.e. "pending = requested and not yet on the
# wire". Usage: probe_pending_boundary.sh <repo-at-head> <work-dir>
# Requires a Verilator 5.050 first on PATH. Never edits the repository.
set -eu
REPO=$1; WORK=$2
mkdir -p "$WORK"
SRC="$REPO/hdl/ieee1722/avtp/KL_media_clock_restart.sv"
MUT="$WORK/KL_media_clock_restart_wire_boundary.sv"
python3 - "$SRC" "$MUT" <<'PY'
import sys
src = open(sys.argv[1]).read()
old = "      if (restart_p_i | src_change_w) tgt_r <= ~mr_o;\n"
new = ("      if (restart_p_i | src_change_w)\n"
       "        for (int t = 0; t < N_TALKERS_P; t++)\n"
       "          if (!(streaming_i[t] && (mr_o[t] == tgt_r[t]) && (hold_r[t] == '0)))\n"
       "            tgt_r[t] <= ~mr_o[t];\n")
assert src.count(old) == 1, "anchor moved"
open(sys.argv[2], "w").write(src.replace(old, new))
PY
make -s -C "$REPO/tb/verilator/tkdiag" build MCR_SRC="$MUT" TKDIAG_MDIR="$WORK/obj_wire" >"$WORK/build.log" 2>&1
cd "$REPO/tb/verilator/tkdiag" && "$WORK/obj_wire/Vtkdiag_sim" || true

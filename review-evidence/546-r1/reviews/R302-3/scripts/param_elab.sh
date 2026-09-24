#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# R302-3: elaborate KL_crf_rx's jump thresholds at a commit with Verilator.
# Usage: VERILATOR=<5.050> param_elab.sh <clone> <commit> <scratch-dir>
# Copies the receiver out of the commit, appends one $display after the
# TS_JUMP_NS_C declaration (scratch copy only), builds, runs, prints values.
set -eu
C="$1"; REV="$2"; S="$3"
rm -rf "$S"; mkdir -p "$S"
git -C "$C" show "$REV:hdl/ieee1722/crf/KL_crf_rx.sv" > "$S/KL_crf_rx.sv"
python3 - "$S/KL_crf_rx.sv" <<'PY'
import sys, re
p = sys.argv[1]; s = open(p).read()
m = re.search(r"localparam logic \[63:0\] TS_JUMP_NS_C =[^;]*;", s)
assert m and s.count("TS_JUMP_NS_C =") == 1, "anchor"
ins = ('\n  initial $display("ELAB RATE_DRIFT_NS_C=%0d TS_JUMP_NS_C=%0d",'
       ' RATE_DRIFT_NS_C, TS_JUMP_NS_C);')
open(p, "w").write(s[:m.end()] + ins + s[m.end():])
PY
cd "$S"
"${VERILATOR:-verilator}" --binary -j 4 --top-module KL_crf_rx -Wno-fatal -Wno-lint -Wno-style \
  KL_crf_rx.sv -o Velab >build.log 2>&1 || { tail -20 build.log; exit 1; }
./obj_dir/Velab | grep '^ELAB' | sed "s/^/$REV /"

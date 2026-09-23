#!/bin/bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reviewer probes on the parent consumer (kebag-logic/milan-fpga dev
# 574c29fa) with the FPGA-gPTP gitlink content at the PR head and at its
# base. Builds disposable replicas under $WORK (never a real checkout) and
# runs ONLY tb/verilator/gptp_shadow's `run` target, at -j 8:
#   A  unmodified suite                        (reproduces the manager's 2 FAIL)
#   B  instrumented suite (report-only lines)  (addend at each graded launch)
#   C  B + closed-loop phase rescripted as a first sync over 1 s (counterfactual)
#   D  the #68 900 ms first-sync case for 20 s through the real consumer path
# Usage: parent_probes.sh <WORK dir> <receipts dir>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
. "$here/env.sh"
WORK="$1"; OUT="$2"
AXIS_SHA=48ff7a7e2ef782cf778d47910cf85835c64b1bce
mkdir -p "$WORK" "$OUT"
cd "$WORK"
[ -d parent ] || git clone -q --filter=blob:none --no-checkout \
  https://github.com/kebag-logic/milan-fpga.git parent
git -C parent fetch -q origin "$PARENT_DEV"
git -C parent checkout -q --detach "$PARENT_DEV"
test "$(git -C parent rev-parse HEAD)" = "$PARENT_DEV"
test "$(git -C parent ls-files -s gptp-processor | cut -d' ' -f2)" = "$BASE_SHA"
[ -d axis ] || git clone -q https://github.com/alexforencich/verilog-axis axis
git -C axis checkout -q --detach "$AXIS_SHA"
for d in head base; do
  [ -d "gptp-$d" ] || git clone -q --no-hardlinks "$REVIEW_CLONE" "gptp-$d"
done
git -C gptp-head checkout -q --detach "$HEAD_SHA"
git -C gptp-base checkout -q --detach "$BASE_SHA"

mk_replica() {  # <name> <head|base>
  rm -rf "$1"; mkdir -p "$1/tb/verilator" "$1/third_party/verilog-axis" "$1/gptp-processor"
  cp -r parent/hdl "$1/"; cp -r parent/tb/common "$1/tb/"
  cp -r parent/tb/verilator/gptp_shadow "$1/tb/verilator/"
  cp -r axis/rtl "$1/third_party/verilog-axis/"
  cp -r "gptp-$2/hdl" "$1/gptp-processor/"
  rm -rf "$1/tb/verilator/gptp_shadow/obj_dir" "$1/tb/verilator/gptp_shadow/gptp_ucode.hex"
}
vflags() {  # the suite's own flags, with Verilator's build jobs capped at 8
  local db
  db="$(cd parent/tb/verilator/gptp_shadow && make -pn run 2>/dev/null || true)"
  printf '%s\n' "$db" | sed -n 's/^VFLAGS = //p' | sed -n '1{s/-j 0/-j 8/;p}'
}
VF="$(vflags)"
run_suite() {  # <replica> <tag>
  local rc=0
  (cd "$1/tb/verilator/gptp_shadow" && timeout 1500 make run VFLAGS="$VF" \
     >"$OUT/$2.stdout.raw" 2>"$OUT/$2.stderr.raw") || rc=$?
  grep -E 'gptp_ucode.hex:|^legs:|^FAIL|checks:|^TX flags|PROBE' "$OUT/$2.stdout.raw" \
    >"$OUT/$2.stdout.log" || true
  grep -E '^PROBE' "$OUT/$2.stderr.raw" >"$OUT/$2.probe.log" || true
  rm -f "$OUT/$2.stdout.raw" "$OUT/$2.stderr.raw"
  echo "$rc" >"$OUT/$2.exit"
  echo "$2: exit $rc; $(grep 'checks:' "$OUT/$2.stdout.log" || echo 'no summary')"
}
wrap_trace() {  # <replica>: report-only $display of step pulses and addend changes
  python3 - "$1/tb/verilator/gptp_shadow/gptp_shadow_wrap.sv" <<'EOF'
import pathlib, sys
p = pathlib.Path(sys.argv[1]); s = p.read_text()
anchor = "  timestamp_counter #(\n"
add = ("  // PROBE (review only): trace every step pulse and addend change\n"
       "  logic signed [31:0] probe_adj_q;\n"
       "  always @(posedge clk_i) begin\n"
       "    probe_adj_q <= adj_w;\n"
       "    if (step_we_w) $display(\"PROBE STEP step=%0d\", $signed(step_w));\n"
       "    if (adj_w != probe_adj_q) $display(\"PROBE ADDEND adj=%0d\", adj_w);\n"
       "  end\n")
assert s.count(anchor) == 1
p.write_text(s.replace(anchor, add + anchor))
EOF
}

for d in head base; do
  mk_replica "A-$d" "$d";  run_suite "A-$d" "A-$d"
  mk_replica "B-$d" "$d";  python3 "$here/instrument_gptp_shadow.py" "B-$d/tb/verilator/gptp_shadow/sim_main.cpp"
  run_suite "B-$d" "B-$d"
  mk_replica "C-$d" "$d";  python3 "$here/instrument_gptp_shadow.py" "C-$d/tb/verilator/gptp_shadow/sim_main.cpp"
  python3 "$here/counterfactual_first_sync_loop.py" "C-$d/tb/verilator/gptp_shadow/sim_main.cpp"
  run_suite "C-$d" "C-$d"
  mk_replica "D-$d" "$d";  python3 "$here/probe_long_slew.py" "D-$d/tb/verilator/gptp_shadow/sim_main.cpp" -900000000
  wrap_trace "D-$d"; run_suite "D-$d" "D-$d"
done

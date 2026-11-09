#!/usr/bin/env bash
# launch.sh: start the reviewer's gate sets detached, one log/rc per gate.
# Paths: PKT (packet root), clones PKT/scratch/{hcamp,hsuite,hdocs} at the reviewed head.
set -u
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
G=$PKT/scripts/run_gate.sh
export VERILATOR_DIR=${VERILATOR_DIR:?set VERILATOR_DIR to a Verilator 5.050 bin dir}
S=$PKT/scratch
# 1) SRP mutation campaign
setsid nohup bash -c "$G camp_srp $S/hcamp python3 -B tb/srp_top/mutants.py --output $S/camp-srp-out --jobs 5" >/dev/null 2>&1 &
# 2) focused suites, serially
setsid nohup bash -c "for t in srp_top srp_encoder srp_stream_fsms pp_top; do $G suite_\$t $S/hsuite/tb/\$t make -j4; done" >/dev/null 2>&1 &
# 3) docs, matrix, lint, whitespace
setsid nohup bash -c "$G make_check $S/hdocs make check; $G gen_matrix $S/hdocs python3 scripts/gen_matrix.py --check; $G lint_hdl $S/hdocs bash scripts/lint_hdl.sh; $G diff_check $S/hdocs git diff --check 044cb25f 60094a268c0df46703a3bee08c94118153634fd9" >/dev/null 2>&1 &
echo launched

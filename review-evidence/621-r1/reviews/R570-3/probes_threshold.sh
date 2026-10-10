#!/usr/bin/env bash
# Threshold-pinning probes: the lost-response limit one lower and one higher.
# Usage: probes_threshold.sh <repo-root> <packet-dir>
set -u
ROOT=$(cd "$1" && pwd); PKT=$(cd "$2" && pwd)
S=$PKT/scratch/probe_thr; R=$PKT/receipts; BIN=$PKT/scratch/head/work/obj/phc_step
rm -rf "$S"; mkdir -p "$S"
python3 -I - "$ROOT/gptp-processor/hdl/ucode/gen_gptp_ucode.py" "$S" <<'PY'
import sys, os
src = open(sys.argv[1]).read(); out = sys.argv[2]
old = 'p.emit("CMP", ra=RB, rb=0, fmt=FMT_D, imm=LOST_N_C + 1)'
assert src.count(old) == 1
for name, new in (("t3-third-loss", "LOST_N_C"), ("t5-fifth-loss", "LOST_N_C + 2")):
    os.makedirs(f"{out}/{name}")
    open(f"{out}/{name}/generate.py", "w").write(src.replace(old, old.replace("LOST_N_C + 1", new)))
PY
for n in t3-third-loss t5-fifth-loss; do
  (cd "$S/$n" && python3 generate.py --clk-hz 8000000 -o gptp_ucode.hex > generate.log 2>&1 && "$BIN" > run.log 2>&1; echo $? > run.rc) &
done
wait
for n in t3-third-loss t5-fifth-loss; do
  echo "== $n rc=$(cat "$S/$n/run.rc")"; grep -E '^(LOSS|ARM (liveness|unanswered))|\[FAIL\]|checks:' "$S/$n/run.log"
  cp "$S/$n/run.log" "$R/probe_thr_$n.log"
done | tee "$R/probes_threshold_summary.log"

#!/usr/bin/env bash
# Disposable mutation probes of the #539 step guard in a SCRATCH copy of the
# candidate. Each mutant must make Vphc_step exit non-zero; the copy is
# restored to HEAD bytes after every mutant.
# Usage: mutate_servo.sh <scratch-candidate-copy> <verilator> <receipt-dir>
set -u
cand=$1; vl=$2; out=$3
f=hdl/ieee1722/crf/KL_mmcm_drp_servo.sv
cd "$cand" || exit 2
mkdir -p "$out"
: > "$out/mutants_summary.txt"
probe() {
  local name=$1 from=$2 to=$3
  git checkout -q -- "$f"
  python3 - "$f" "$from" "$to" <<'EOF' || { echo "$name: pattern not found" >> "$out/mutants_summary.txt"; return; }
import sys
p, a, b = sys.argv[1:4]
s = open(p).read()
if s.count(a) != 1:
    sys.exit(1)
open(p, "w").write(s.replace(a, b))
EOF
  ( cd tb/verilator/mmcm_servo && rm -rf obj_phc && make -s VERILATOR="$vl" phc_step_build >/dev/null 2>&1 && ./obj_phc/Vphc_step ) > "$out/mutant_$name.log" 2>&1
  local rc=$?
  local verdict=KILLED; [ "$rc" -eq 0 ] && verdict=SURVIVED
  printf '%-28s rc=%d %s  %s\n' "$name" "$rc" "$verdict" "$(grep -E 'checks:|RESULT' "$out/mutant_$name.log" | tail -n 1)" >> "$out/mutants_summary.txt"
}
probe no_step_guard  "wire step_hit_w  = ptp_jump_r && win_valid_r;" "wire step_hit_w  = 1'b0;"
probe no_step_tally  "7'(guard_hit_w) + 7'(step_hit_w);" "7'(guard_hit_w);"
probe det_thr_1ms    "localparam logic [31:0] STEP_DET_NS_C = 32'd4096;" "localparam logic [31:0] STEP_DET_NS_C = 32'd1000000;"
git checkout -q -- "$f"
git status --porcelain -- "$f" >> "$out/mutants_summary.txt"
echo "restored $(git rev-parse HEAD:$f) == $(git hash-object $f)" >> "$out/mutants_summary.txt"
cat "$out/mutants_summary.txt"

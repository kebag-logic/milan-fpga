#!/bin/sh
# [R312] R312-2 probe: does tb/verilator/nvm_cosim detect a wrong firmware
# output-length table (the claim SAVED_STATE_FASTCONNECT.md section 4.2 adds
# at dd6a68e9)? Runs the suite's 8x8 builds without its mutant sweep, first on
# the exact head (control), then with the firmware's backend table write ONLY
# planted with the old 9-entry output length (the same plant as the round-1
# firmware_map_probe.py "rebase_old_len" arm). The firmware file is restored
# from HEAD afterwards and the suite's build directory removed.
# Run from the repository root with the pinned Verilator first on PATH.
set -u
F=sw/firmware/milan_baremetal/milan_baremetal.c
B=tb/verilator/nvm_cosim/build
restore() { git show HEAD:$F > $F; git diff --quiet -- $F || { echo "RESTORE FAILED"; exit 3; }; rm -rf $B; }
trap restore EXIT
run() {
  out=$(cd tb/verilator/nvm_cosim && python3 -B run_cases.py --shapes 8x8 --jobs 8 --pool 8 --skip-mutants 2>&1); rc=$?
  echo "== $1: rc=$rc"
  echo "$out" | grep -E 'FAIL|checks|PASS|passed|failed|RESULT|total' | sort | uniq -c | sort -rn | head -12 | cut -c1-240
  rm -rf $B
}
run control_head
python3 - "$F" <<'PY'
import sys; p = sys.argv[1]; s = open(p).read()
o = "unsigned int flen = REC_HDR + NVM_MAP_ENTRY * entries;"; assert s.count(o) == 1
open(p, "w").write(s.replace(o, "unsigned int flen = REC_HDR + NVM_MAP_ENTRY * (dir ? 9u : entries);"))
PY
run fw_table_old_output_length
restore
echo "restored: $(git hash-object $F) vs HEAD $(git rev-parse HEAD:$F)"

#!/usr/bin/env bash
# Reviewer pin probes, in place on a checkout's tsn-c-stack submodule, restored after every arm.
# Usage: pin_probes.sh <checkout> <work>   (MILAN_RV32_CC must name the pinned RV32 compiler)
set -u
R=$(cd "$1" && pwd); W=$2; mkdir -p "$W"; W=$(cd "$W" && pwd)
S=$R/third_party/tsn-c-stack; T=$R/sw/firmware/ctrl/test
restore() {
  git -C "$S" update-index --no-assume-unchanged src/adp.c src/maap.c include/wire.h 2>/dev/null
  git -C "$S" checkout --quiet -- . ; git -C "$S" clean -fdq -- src include tests
  [ -z "$(git -C "$S" status --porcelain)" ] || { echo "RESTORE FAILED"; exit 9; }
}
arm() {  # name, spoil, command...
  local name=$1 spoil=$2; shift 2
  restore; eval "$spoil"
  local log=$W/$name.log
  ( cd "$R" && VERILATOR=false timeout 600 "$@" ) > "$log" 2>&1; local rc=$?
  local said; said=$(grep -m1 -E "differs from the pinned|is not the pinned|PLANTED_WIRE_EDIT|REFUSED|UNMEASURED" "$log" | cut -c1-200)
  printf '%s rc=%s : %s\n' "$name" "$rc" "${said:-no pin verdict}"
}
EDIT='printf "\n" >> "$S/src/maap.c"'
HIDE='printf "\n" >> "$S/src/adp.c"; git -C "$S" update-index --assume-unchanged src/adp.c; [ -z "$(git -C "$S" status --porcelain)" ] && echo "  (git status of the stack is empty)"'
UNTRACKED='printf "int x;\n" > "$S/src/extra.c"'
WIRE='printf "#error PLANTED_WIRE_EDIT\n" >> "$S/include/wire.h"'
O=$W/out
for s in EDIT HIDE; do
  arm "$s-test_ctrl_firmware" "${!s}" python3 -B "$T/test_ctrl_firmware.py" --require-rv32
  arm "$s-fw_coverage_check" "${!s}" python3 -B sw/firmware/gtest/fw_coverage.py --check --jobs 4
  arm "$s-maap_differential" "${!s}" python3 -B "$T/maap_differential.py"
  arm "$s-maap_differential_selftest" "${!s}" python3 -B "$T/maap_differential.py" --self-test
  arm "$s-mbx_run_cosim" "${!s}" make --no-print-directory -C tb/verilator/mbx run-cosim
  arm "$s-aecp_arms_app" "${!s}" python3 -B "$T/aecp_arms.py" --app --output "$O/aecp"
  arm "$s-aecp_mutants" "${!s}" python3 -B "$T/aecp_mutants.py" --shard 0 1000 --output "$O/aecpm"
  arm "$s-aecp_wire" "${!s}" python3 -B "$T/aecp_wire.py" --output "$O/aecpw" --reference "$R/protocol-processor" --verilator false
  arm "$s-ctrl_image" "${!s}" python3 -B "$T/ctrl_image.py"
  arm "$s-ctrl_srp_image_aecp" "${!s}" python3 -B "$T/ctrl_srp_image.py" --config configs/endstation_ax7101_1x1_tdm8.yaml --output "$O/srpimg" --with-aecp --libc /nonexistent --compiler-runtime /nonexistent
  arm "$s-ctrl_boundary" "${!s}" python3 -B "$T/ctrl_boundary.py" --require-rv32
  arm "$s-ctrl_build_cli" "${!s}" python3 -B "$T/ctrl_build.py" --stack-pin
done
arm "UNTRACKED-ctrl_build_cli" "$UNTRACKED" python3 -B "$T/ctrl_build.py" --stack-pin
arm "WIRE-mbx_run_cosim" "$WIRE" make --no-print-directory -C tb/verilator/mbx run-cosim
arm "WIRE-mbx_run_if2" "$WIRE" make --no-print-directory -C tb/verilator/mbx run-if2 IF2="$O/if2" VERILATOR=true
restore
echo "restored: $(git -C "$S" rev-parse HEAD) status='$(git -C "$S" status --porcelain)'"

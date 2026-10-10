#!/usr/bin/env bash
# Reviewer probes for the shared tsn-c-stack pin check of PR #705 (ctrl_build.stack_pin).
# Usage: pin_probes.sh <disposable clone at the PR head, submodules initialised> <scratch dir> <rv32 cc>
# Each spoil is applied to the clone's own submodule, every entry point that builds the stack is run
# against it, and the line it prints about the stack is recorded. The clone is restored between spoils.
set -u
C=$(cd "$1" && pwd); W=$2; RV=$3
SUB=$C/third_party/tsn-c-stack
PIN=$(git -C "$C" ls-files --stage -- third_party/tsn-c-stack | awk '{print $2}')
T=$C/sw/firmware/ctrl/test
mkdir -p "$W"
export MILAN_RV32_CC=$RV

restore() {
  # one flag per call: git update-index applies only one of the two when both are given
  git -C "$SUB" ls-files -z | xargs -0 git -C "$SUB" update-index --no-assume-unchanged
  git -C "$SUB" ls-files -z | xargs -0 git -C "$SUB" update-index --no-skip-worktree
  git -C "$SUB" checkout -q -f "$PIN" && git -C "$SUB" reset -q --hard "$PIN" && git -C "$SUB" clean -qfdx
  rm -rf "$C/tb/verilator/mbx/obj_fw" "$C/tb/verilator/mbx/obj_if2" "$W/out"
}

say() { # name rc output-file
  local line; line=$(grep -a 'tsn-c-stack\|PIN-PROBE' "$3" | tail -1)
  printf '%s | rc=%s | %s\n' "$1" "$2" "${line:-no stack verdict}"
}

tools() { # label
  local L=$1 o
  run() { local n=$1; shift; o=$W/$L.$n.out; ( cd "$C" && timeout 900 "$@" ) >"$o" 2>&1; say "$L | $n" $? "$o"; }
  run stack-pin-cli    python3 -B "$T/ctrl_build.py" --stack-pin
  run make-stack-pin   make --no-print-directory -C "$C/tb/verilator/mbx" stack-pin
  run make-libctrlfw   make --no-print-directory -C "$C/tb/verilator/mbx" CC=false obj_fw/libctrlfw.a
  run maap-diff        env VERILATOR=false python3 -B "$T/maap_differential.py"
  run maap-diff-self   env VERILATOR=false python3 -B "$T/maap_differential.py" --self-test
  run aecp-arms        env VERILATOR=false python3 -B "$T/aecp_arms.py" --output "$W/out/a" --app
  run aecp-mutants     env VERILATOR=false python3 -B "$T/aecp_mutants.py" --output "$W/out/m" --shard 0 1000
  run aecp-wire        python3 -B "$T/aecp_wire.py" --reference "$C/protocol-processor" --output "$W/out/w" --verilator false
  run ctrl-image       python3 -B "$T/ctrl_image.py" --shape endstation_ax7101_1x1_tdm8 --out "$W/out/i"
  run fw-gate          python3 -B "$T/test_ctrl_firmware.py" --require-rv32 --jobs 1
  run boundary         python3 -B "$T/ctrl_boundary.py" --require-rv32
}

restore
echo "pin $PIN"
# S0 pristine: only the pin itself (the tools would go on to build)
( cd "$C" && python3 -B "$T/ctrl_build.py" --stack-pin ) > "$W/S0.out" 2>&1; say "S0 pristine | stack-pin-cli" $? "$W/S0.out"

# S1 a content edit of a core source
restore; ( cd "$C" && python3 -B "$T/ctrl_build.py" --stack-pin ) | sed 's/^/before S1: /'
printf '\n' >> "$SUB/src/maap.c"; tools S1-modified-src

# S2 an edit hidden from git status by assume-unchanged
restore; printf '/* hidden */\n' >> "$SUB/src/adp.c"; git -C "$SUB" update-index --assume-unchanged src/adp.c
echo "S2 git status --porcelain: [$(git -C "$SUB" status --porcelain)]"; tools S2-assume-unchanged

# S3 an edit hidden by skip-worktree, in a public header
restore; printf '/* hidden */\n' >> "$SUB/include/wire.h"; git -C "$SUB" update-index --skip-worktree include/wire.h
echo "S3 git status --porcelain: [$(git -C "$SUB" status --porcelain)]"; tools S3-skip-worktree

# S4 a header the pinned tree does not hold, ignored by nothing
restore; ( cd "$C" && python3 -B "$T/ctrl_build.py" --stack-pin ) | sed 's/^/before S4: /'
printf '#define EXTRA 1\n' > "$SUB/include/extra.h"; tools S4-untracked-header

# S5 the stack's own boundary script edited (the gate runs it)
restore; printf '\n' >> "$SUB/scripts/check_boundary.py"
( cd "$C" && python3 -B "$T/ctrl_build.py" --stack-pin ) > "$W/S5.out" 2>&1; say "S5 script edited | stack-pin-cli" $? "$W/S5.out"
( cd "$C" && timeout 900 python3 -B "$T/ctrl_boundary.py" --require-rv32 ) > "$W/S5b.out" 2>&1; say "S5 script edited | boundary" $? "$W/S5b.out"

# S6 GAP: run-if2 compiles the firmware's host model against the stack's include/ without the pin
restore; printf '#error PIN-PROBE: the stack header was compiled without the pin check\n' >> "$SUB/include/wire.h"
( cd "$C" && timeout 900 make --no-print-directory -C tb/verilator/mbx VERILATOR=true run-if2 ) > "$W/S6.out" 2>&1
say "S6 wire.h poisoned | make run-if2 (alone)" $? "$W/S6.out"
grep -a -m3 'PIN-PROBE\|REFUSED\|mbx_model' "$W/S6.out" | sed 's/^/    /'
restore
echo "restored: submodule HEAD $(git -C "$SUB" rev-parse HEAD), status [$(git -C "$SUB" status --porcelain)], flagged [$(git -C "$SUB" ls-files -v | grep -v '^H')]"
( cd "$C" && python3 -B "$T/ctrl_build.py" --stack-pin ) | sed 's/^/restored pin: /' 

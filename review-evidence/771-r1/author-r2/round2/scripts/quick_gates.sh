#!/usr/bin/env bash
# quick_gates.sh OUTDIR: the fast gates the round-2 change touches, each with
# its own log and rc, run from the physical worktree path with the lane env.
set -u
out="$1"
mkdir -p "$out"
source $VALIDATION_STORAGE/scratch/a662/env.sh
export MILAN_RV32_CC=$VALIDATION_STORAGE/771-a662-r2/rv32-sdk/host/bin/riscv32-linux-gcc
cd $LANES/771-pin4 || exit 2
M=$WORKSPACE_HOME/litex-milan/work/a662-771/m1
run() {
    local name="$1"; shift
    local t0=$SECONDS
    "$@" > "$out/$name.log" 2>&1
    local rc=$?
    echo "$rc" > "$out/$name.rc"
    printf '%-28s rc=%s %4ss  %s\n' "$name" "$rc" "$((SECONDS - t0))" "$(tail -n 1 "$out/$name.log" | cut -c1-150)"
}
echo "head $(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)"
run lint_rtl python3 scripts/lint_rtl.py --check
run port_contracts python3 scripts/check_port_contracts.py
run naming python3 scripts/measure_naming.py --check
run test_evidence python3 scripts/measure_test_evidence.py --check
run hygiene python3 scripts/check_hygiene.py --check
run pp_srcs python3 scripts/pp_srcs.py --check
run check_baseline python3 syn/ooc/pp_resource_gate.py check-baseline
run check_route_1x1 python3 syn/ooc/pp_resource_gate.py check "$M/ax7101/gateware" --endpoint route-1x1
run check_ooc_1x1 python3 syn/ooc/pp_resource_gate.py check "$M/ax7101-ooc" --endpoint ooc-1x1
run check_ooc_8x8 python3 syn/ooc/pp_resource_gate.py check "$M/ax8x8-ooc" --endpoint ooc-8x8
run rom_digests bash syn/yosys/ooc.sh --record-rom-digests
run rom_digests_diff git diff --exit-code syn/yosys/rom_digests.tsv
run integrator_params python3 protocol-processor/scripts/check-integrator-params.py
run submodule_docs python3 scripts/check_submodule_docs.py
run gptp_docs python3 scripts/check_gptp_docs.py --with-submodule
run nvm_capture python3 scripts/check_nvm_capture.py
run diag_boundaries python3 docs/diagrams/submodule_boundaries.gen.py --check
run diag_timesync python3 docs/diagrams/timesync_chain.gen.py --check
run docs_check python3 scripts/docs_check.py
run feature_status python3 scripts/check_feature_status.py
echo "after: head $(git rev-parse HEAD) dirty=$(git status --porcelain | wc -l)"

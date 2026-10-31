#!/usr/bin/env bash
# #787 round 4: dynmap-mutants' two end-to-end arms (36, the listener leg in milan_dp_render, and 37, the talker
# leg in capture_coherence) with their clean controls, at <rev> in the campaigns clone. The campaign's builds keep
# each leg's generated inputs unmade (`make -o`), so those inputs are made first by the legs' own suites; then
# dynmap_mutants.py runs from tb/verilator/milan_dp with MAKEFLAGS cleared, not under an outer make.
# usage: dynmap_e2e_run.sh <rev>
set -u
rev=$1; X=$VALIDATION_STORAGE/787-a700f; C=$X/clone-campaigns-${rev:0:8}; O=$X/r/campaigns-${rev:0:8}; D=$(cd "$(dirname "$0")" && pwd)
cd "$C" || exit 2
[ "$(git rev-parse HEAD)" = "$rev" ] || exit 2
source "$D/env.sh"; source "$D/fw_env.sh"; export VERILATOR_JOBS=4
unset MAKEFLAGS MAKELEVEL MFLAGS
run() { n=$1; shift; s=$(date +%s); "$@" > "$O/$n.log" 2>&1; rc=$?; echo "$rc $(( $(date +%s)-s ))s $n: $*" >> "$O/table-dynmap-e2e.txt"; }
run e2e_inputs_listener make -C tb/verilator/milan_dp_render ltn_rom.hex ucode.hex tdm8r_aemi.bin
run e2e_inputs_talker make -C tb/verilator/capture_coherence ltn_rom.hex ucode.hex
cd tb/verilator/milan_dp || exit 2
run dynmap_mutants_e2e_arms python3 dynmap_mutants.py --jobs 2 36 37
cd "$C" || exit 2
git status --porcelain --untracked-files=no > "$O/clone-status-after-dynmap-e2e.txt"
echo DYNMAP-E2E-DONE >> "$O/table-dynmap-e2e.txt"

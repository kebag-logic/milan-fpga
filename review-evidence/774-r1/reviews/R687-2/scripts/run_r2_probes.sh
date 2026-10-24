#!/usr/bin/env bash
# Round-2 review probes for PR #778 at one exact head, each in its own
# disposable copy of a clean clone, one log + rc file each.
# usage: run_r2_probes.sh <clean-clone-at-head> <dev-sha> <packet-dir> <verilator> <pinned-shfmt>
# The clone itself is only copied; nothing runs inside it.
set -u
clone=$1 dev=$2 pkt=$3 vlt=$4 shfmt=$5
s=$pkt/scratch r=$pkt/receipts
mkdir -p "$s" "$r"/{bdd,inventory,legs,gates,docs}
for d in bdd-head inv-head inv-dev sim-head sim2-head; do cp -a "$clone" "$s/$d"; done
(cd "$s/inv-dev" && git checkout -q "$dev")
run() { local out=$1; shift; "$@" > "$out.log" 2>&1; echo "rc=$?" > "$out.rc"; }
# behave, the two walks and the two legs concurrently
(cd "$s/bdd-head/tests" && run "$r/bdd/behave-head" behave --no-capture -f plain) &
(cd "$s/inv-head" && CI_IMAGE_SHFMT=$shfmt run "$r/inventory/walk-head" python3 -I "$pkt/scripts/inventory_walk.py" "$s/inv-head") &
(cd "$s/inv-dev" && CI_IMAGE_SHFMT=$shfmt run "$r/inventory/walk-dev" python3 -I "$pkt/scripts/inventory_walk.py" "$s/inv-dev") &
(cd "$s/sim-head/tb/verilator/milan_dp" && run "$r/legs/crflic-head" make -j8 VERILATOR="$vlt" crflic) &
(cd "$s/sim2-head/tb/verilator/milan_dp" && run "$r/legs/tspec8-head" make -j6 VERILATOR="$vlt" tspec8) &
wait
head=$(git -C "$clone" rev-parse HEAD)
run "$r/bdd/frame_bytes_probe_head" python3 "$pkt/scripts/bdd_frame_bytes_probe.py" "$s/bdd-head" "$head"
run "$r/docs/matrix_clause_probe" python3 -I "$pkt/scripts/matrix_clause_probe.py" "$s/bdd-head" "$dev" "$head"
run "$r/inventory/tspec8_pattern_probe" python3 -I "$pkt/scripts/tspec8_pattern_probe.py" "$s/bdd-head"
export PATH="$(dirname "$vlt"):$PATH"
cd "$s/bdd-head" || exit 2
run "$r/gates/lint_rtl_check" python3 scripts/lint_rtl.py --check &
run "$r/gates/gen_module_matrix_check" python3 docs/traceability/gen_module_matrix.py --check &
run "$r/gates/docs_check" python3 scripts/docs_check.py &
run "$r/gates/test_sim_pool" python3 tb/verilator/milan_dp/test_sim_pool.py &
wait
for f in "$r"/*/*.rc; do echo "$f $(cat "$f")"; done

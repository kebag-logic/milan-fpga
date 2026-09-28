#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reproduce the R377-3 reviewer runs. Never writes to CLONE.
# Usage: run_r377_3.sh CLONE REV VERILATOR WORK OUT [PARENT_DIR]
#   CLONE      processor clone containing REV
#   REV        exact head under review (66451539ee49262d97403bc6b010202bb773d272)
#   VERILATOR  simulator executable (5.050 was used)
#   WORK       disposable scratch directory
#   OUT        receipt directory (created)
#   PARENT_DIR optional: holds KL_pp_maap_shim.sv (parent@931f396e, identical at 54ce8773)
#              and reproduce_first_probe.cpp (parent@b367df5d review-evidence/pp128-r1/author)
# At most 8 CPUs are used (taskset) and at most 8 parallel jobs are started.
set -euo pipefail
clone=$1; rev=$2; vl=$3; work=$4; out=$5; parent=${6:-}
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work/bin" "$out"
cp "$vl" "$work/bin/verilator"
export VERILATOR="$work/bin/verilator" TMPDIR="$work/tmp" PATH="$work/bin:$PATH"
mkdir -p "$TMPDIR"
cap="taskset -c 0-7"
head="$work/head"; rm -rf "$head"; mkdir -p "$head"
git -C "$clone" archive "$rev" | tar -x -C "$head"

# 1. ACMP, SRP, MAAP and pp_top suites at the merge head
mkdir -p "$out/10-suites-head"
for t in acmp_talker acmp_listener acmp_nvm srp_admission srp_decoder srp_encoder \
         srp_stream_fsms srp_top maap pp_top; do
  set +e; (cd "$head/tb/$t" && $cap make VERILATOR="$VERILATOR") > "$out/10-suites-head/$t.log" 2>&1
  rc=$?; set -e
  echo "$t rc=$rc $(grep -Eo '[0-9]+ checks: [0-9]+ PASS, [0-9]+ FAIL' "$out/10-suites-head/$t.log" | tail -1)"
done | tee "$out/10-suites-head/summary.txt"

# 2. both committed mutation campaigns (sequential drivers, run side by side)
( cd "$head" && $cap python3 tb/acmp_talker/retry_mutants.py --logs "$out/20-retry-campaign" \
    > "$out/20-retry-campaign.stdout" 2>&1; echo "retry_mutants rc=$?" >> "$out/20-retry-campaign.stdout" ) &
( cd "$head" && $cap make -C tb/srp_top mutants MUTANT_OUTPUT="$out/21-srp-campaign" \
    > "$out/21-srp-campaign.stdout" 2>&1; echo "srp mutants rc=$?" >> "$out/21-srp-campaign.stdout" ) &
wait
python3 "$here/compare_readme.py" "$head/tb/acmp_talker/README.md" "$out/20-retry-campaign" \
    > "$out/22-readme-table-vs-rerun.txt" || true

# 3. static: comment-only RTL delta, interface identity, lint and doc gates, declaration order
for r in cc7c911e933aed4bfc9324eb5da473ae73bef618 8eefb7b971f798f0c161559bf9c9070627a2c3e6 "$rev"; do
  git -C "$clone" show "$r:hdl/acmp/KL_acmp_talker.sv" > "$work/t.sv"
  echo "$(python3 "$here/strip_sv_comments.py" "$work/t.sv" | sha256sum | cut -d' ' -f1) stripped talker @$r"
done > "$out/30-rtl-identity-interface.txt"
(cd "$head/tb/acmp_talker" && make lint VERILATOR="$VERILATOR") > "$out/31-lint-docs.txt" 2>&1
(cd "$head" && make check && python3 scripts/gen_matrix.py --check) >> "$out/31-lint-docs.txt" 2>&1
bash "$here/r1/forward_ref_check.sh" "$clone" "$rev" "$work/fwd" > "$out/32-forward-ref.txt"

# 4. reviewer single edits against the committed suite, and observational lockstep
$cap python3 "$here/r377_mutants.py" suite --src "$head" --work "$work/mut" --out "$out/40-reviewer-suite" --jobs 8
$cap python3 "$here/r377_mutants.py" lockstep --src "$head" --work "$work/ls" --out "$out/41-lockstep" \
    --jobs 8 --seeds 16 --cycles 3000000
$cap python3 "$here/r377_mutants.py" lockstep --src "$head" --work "$work/ls64" --out "$out/42-lockstep-64" \
    --jobs 5 --seeds 64 --cycles 3000000 --only identity ctl_kill_no_live_conflict \
    init_busy_else_removed kill_w_no_off eq_sticky_kill_ignores_accept

# 5. reviewer probe P7 and round-1 probes P1-P6 at this head
python3 "$here/apply_probe.py" "$head" "$work/head-p7" "$here/r377_event_classes.hpp"
$cap python3 "$here/r377_mutants.py" suite --src "$work/head-p7" --work "$work/mut-p7" --out "$out/43-probe-p7" \
    --jobs 5 --only identity elig_drop_conflict elig_drop_pcp elig_drop_tmr elig_drop_lsn
python3 "$here/apply_probe.py" "$head" "$work/head-r1p" "$here/r1/probe_cases.hpp" "$here/r377_1_adapter.hpp"
$cap python3 "$here/r377_mutants.py" suite --src "$work/head-r1p" --work "$work/mut-r1p" --out "$out/44-r1-probes" \
    --only identity

# 6. parent first-probe harness (#128 acceptance), if the parent inputs are supplied
if [ -n "$parent" ]; then
  bash "$here/r1/parent_first_probe.sh" "$clone" "$rev" "$parent/KL_pp_maap_shim.sv" \
    "$parent/reproduce_first_probe.cpp" "$work/fp" "$VERILATOR" "$out/50-parent-first-probe-${rev:0:8}.txt"
fi

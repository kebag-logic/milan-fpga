#!/usr/bin/env bash
# Reviewer-owned mutants (mutations/r400-*.patch) against the exact head:
# each runs the head's own suite(s); the Release! mutants also run the probe
# build. Plus the probe build on the BASE KL_pp_maap.sv (pre-existence of P2/P3).
# Receipts: receipts/r400-mutants/<arm>-<suite>.log, receipts/r400-mutants/summary.txt
source "$(dirname "$0")/common.sh"
OUT=$RECEIPTS/r400-mutants
rm -rf "$OUT"; mkdir -p "$OUT"
SUM=$OUT/summary.txt; : >"$SUM"

arm() {  # arm-name suite target [probes]
  local name=$1 suite=$2 target=$3 probes=${4:-}
  local T=$SCRATCH/mut-$name-$suite${probes:+-probes}
  export_tree "$T"
  git -C "$T" init -q 2>/dev/null || true
  (cd "$T" && git apply --check "$PACKET/mutations/$name.patch" && git apply "$PACKET/mutations/$name.patch")
  [ -n "$probes" ] && python3 "$PACKET/probes/insert_probes.py" "$T/tb/maap/sim_main.cpp"
  local log=$OUT/$name-$suite${probes:+-probes}.log
  run_target "$T" "$suite" "$target" "$log" | sed "s/^/$name ${probes:+(probes) }/" | tee -a "$SUM"
  { grep "^FAIL" "$log" || true; } | head -12 | sed "s/^/    /" | tee -a "$SUM"
  rm -rf "$T"
}

arm r400-release-waits-for-draw maap run
arm r400-release-waits-for-draw maap run probes
arm r400-release-clears-mark-only-if-prng-idle maap run
arm r400-seed-clamp-off-by-one maap run
arm r400-compare-mac-word-reversed maap run
arm r400-compare-mac-word-reversed pp_top maap-internal
arm r400-compare-mac-last-octet-only maap run
arm r400-compare-mac-last-octet-only pp_top maap-internal

# pre-existence: the probes on the base RTL of KL_pp_maap.sv (head harness)
T=$SCRATCH/base-rtl-probes
export_tree "$T"
git -C "$CLONE" show "$BASE_SHA:hdl/maap/KL_pp_maap.sv" >"$T/hdl/maap/KL_pp_maap.sv"
python3 "$PACKET/probes/insert_probes.py" "$T/tb/maap/sim_main.cpp"
run_target "$T" maap run "$OUT/base-rtl-probes-maap.log" | sed 's/^/base-rtl (probes) /' | tee -a "$SUM"
{ grep -E "^FAIL|^  P[0-9]" "$OUT/base-rtl-probes-maap.log" || true; } | sed "s/^/    /" | tee -a "$SUM"
rm -rf "$T"

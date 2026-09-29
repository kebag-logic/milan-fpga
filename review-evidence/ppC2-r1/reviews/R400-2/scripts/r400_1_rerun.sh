#!/usr/bin/env bash
# Re-run the published R400-1 probes (P1..P5) and reviewer mutants at a new head.
# usage: r400_1_rerun.sh CLONE REV R400_1_DIR WORK VERILATOR OUTDIR
# R400_1_DIR holds the published R400-1 packet (probes/, mutations/).
set -uo pipefail
clone=$1 rev=$2 r1=$3 work=$4 vl=$5 out=$6
mkdir -p "$out"
export_tree() { rm -rf "$1"; mkdir -p "$1"; git -C "$clone" archive "$rev" | tar -x -C "$1"; }
run() {  # tree suite target log
  ( cd "$1/tb/$2" && make VERILATOR="$vl" "$3" ) >"$4" 2>&1; echo "rc=$?" >>"$4"
  echo "$(basename "$4"): $(tail -1 "$4") tally: $(grep -E '[0-9]+ checks' "$4" | tail -1)"
}
T=$work/probes; export_tree "$T"
python3 "$r1/probes/insert_probes.py" "$T/tb/maap/sim_main.cpp"
run "$T" maap run "$out/probes-head-maap.log"
grep -E '^FAIL|^  P[0-9]' "$out/probes-head-maap.log"
for spec in "r400-release-waits-for-draw maap run" "r400-release-clears-mark-only-if-prng-idle maap run" \
            "r400-seed-clamp-off-by-one maap run" "r400-compare-mac-word-reversed maap run" \
            "r400-compare-mac-last-octet-only maap run" "r400-compare-mac-last-octet-only pp_top maap-internal"; do
  set -- $spec
  T=$work/mut-$1-$2; export_tree "$T"
  (cd "$T" && git apply --check "$r1/mutations/$1.patch" && git apply "$r1/mutations/$1.patch") || { echo "$1: APPLY FAILED"; continue; }
  run "$T" "$2" "$3" "$out/$1-$2.log"
  grep '^FAIL' "$out/$1-$2.log" | head -4 | sed 's/^/    /'
  rm -rf "$T"
done

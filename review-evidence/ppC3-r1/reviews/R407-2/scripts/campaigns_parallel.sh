#!/usr/bin/env bash
# The #132 / C1 / pre-existing mutation campaigns at the exact head, each with the
# repository's own driver, 6 concurrent jobs on 8 CPUs; logs in scratch, summaries in receipts.
set -u
source "$(dirname "$0")/env.sh"
R="$PKT/receipts/campaigns"; S="$PKT/scratch/campaigns"; mkdir -p "$R" "$S"
cd "$CLONE"
run() { local name="$1"; shift; ( /usr/bin/time -f '%e s' $CAP "$@" > "$R/$name.txt" 2>&1; echo "rc=$?" >> "$R/$name.txt" ) & }
run srp_top_mutants   make -C tb/srp_top mutants MUTANT_OUTPUT="$S/srp_top"
run gsi_mutants       python3 tb/pp_top/gsi_mutants.py --output "$S/gsi" --verilator "$PINNED_BIN/verilator"
run name_wr_mutant    python3 tb/pp_top/name_wr_mutant.py --output "$S/name_wr"
run retry_mutants     python3 tb/acmp_talker/retry_mutants.py --logs "$S/retry"
run srp_admission_mut python3 tb/srp_admission/mutants.py --output "$S/srp_admission"
run desc_mem_guard    python3 tb/desc_mem_guard/mutate.py --output "$S/desc_mem_guard"
wait
for f in "$R"/*.txt; do echo "== $(basename "$f")"; tail -4 "$f"; done

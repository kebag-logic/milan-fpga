#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Reproduce the R377-2 reviewer runs. Never writes to CLONE.
# Usage: run_r377_2.sh CLONE REV VERILATOR WORK OUT
#   CLONE     processor clone containing REV
#   REV       exact head under review
#   VERILATOR simulator executable (5.050 was used)
#   WORK      disposable scratch directory
#   OUT       receipt directory (created)
set -euo pipefail
clone=$1; rev=$2; vl=$3; work=$4; out=$5
here=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$work" "$out"
export VERILATOR="$vl" TMPDIR="$work/tmp"; mkdir -p "$TMPDIR"
head="$work/head"; rm -rf "$head"; mkdir -p "$head"
git -C "$clone" archive "$rev" | tar -x -C "$head"
# 1. committed suite and committed mutation campaign
( cd "$head/tb/acmp_talker" && make VERILATOR="$vl" ) > "$out/suite-acmp_talker.log" 2>&1
( cd "$head" && PATH="$(dirname "$vl"):$PATH" python3 tb/acmp_talker/retry_mutants.py \
    --logs "$out/author-campaign" ) > "$out/author-campaign.stdout" 2>&1
# 2. reviewer single-edit mutants against the committed suite
python3 "$here/r377_mutants.py" suite --src "$head" --work "$work/mut" --out "$out/reviewer-suite"
# 3. observational lockstep (16 seeds x 3M cycles per edit)
python3 "$here/r377_mutants.py" lockstep --src "$head" --work "$work/ls" --out "$out/lockstep" \
    --seeds 16 --cycles 3000000
# 4. reviewer probe P7 (event classes under continuous commands), head and mutants
python3 "$here/apply_probe.py" "$head" "$work/head-p7" "$here/r377_event_classes.hpp"
python3 "$here/r377_mutants.py" suite --src "$work/head-p7" --work "$work/mut-p7" \
    --out "$out/probe-p7" --only identity elig_drop_conflict elig_drop_pcp elig_drop_tmr elig_drop_lsn
# 5. round-1 reviewer probes P1-P6 and round-1 mutant set at this head
python3 "$here/apply_probe.py" "$head" "$work/head-r1p" "$here/r1/probe_cases.hpp" "$here/r377_1_adapter.hpp"
python3 "$here/r377_mutants.py" suite --src "$work/head-r1p" --work "$work/mut-r1p" \
    --out "$out/r1-probes" --only identity
python3 "$here/r1/reviewer_mutants.py" "$clone" "$work/r1mut" "$vl" "$out/r1-mutants"
# 6. declaration order at head, round-1 head and base
for r in "$rev" 9476898b28ffc8f77b2aa5f873f3899a17287d3a 16be6768f710e79450aace277abacd6c2c3336e5; do
  bash "$here/r1/forward_ref_check.sh" "$clone" "$r" "$work/fwd"
done > "$out/forward-ref.txt"

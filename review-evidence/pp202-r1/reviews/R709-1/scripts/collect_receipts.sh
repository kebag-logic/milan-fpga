#!/usr/bin/env bash
# SPDX-License-Identifier: CERN-OHL-W-2.0
# Build the publishable receipts (R709-1) from the raw logs under scratch/logs.
# Receipts are excerpts: tallies, every FAIL line, verdict lines and the probe
# prints. Local install paths are replaced by <simulator-root> and the packet
# path by <packet>; nothing else is changed.
set -euo pipefail
pk=$(cd "$(dirname "$0")/.." && pwd)
L=$pk/scratch/logs; R=$pk/receipts
mkdir -p "$R"
san() { sed -E -e 's#/home/[^ ]*/overlay/[0-9a-f]+/diff#<simulator-root>#g' \
               -e "s#$pk#<packet>#g" -e 's#/home/[A-Za-z0-9_.-]+#<home>#g'; }
pick() { grep -E "$2" "$L/$1" | san || true; }
{ echo "== tb/acmp_talker at head (rc $(cat $L/head-tal.rc))"; pick head-tal.log '^FAIL|checks:|^S5'
  echo "== tb/acmp_talker at base ed211803 (rc $(cat $L/base-tal.rc))"; pick base-tal.log '^FAIL|checks:'
} > "$R/talker-suite-head-and-base.txt"
{ echo "== head bench against the base talker RTL, src_stream_id_o stubbed to cfg_stream_id_i (old behaviour)"
  pick oldrtl.log '^FAIL|checks:'; } > "$R/talker-head-bench-on-old-rtl.txt"
{ echo "== tb/pp_top make run at head (rc $(cat $L/head-top.rc))"; pick head-top.log '^FAIL|checks:|^MP8'; } > "$R/pp_top-suite-head.txt"
{ echo "== tb/pp_top/acmp_mutants.py STREAM_ID group, --jobs 8 (rc $(cat $L/mut-sid.rc))"; san < "$L/mut-sid.log"; } > "$R/stream-id-mutants.txt"
san < "$pk/scratch/mut-sid/results.json" > "$R/stream-id-mutants.results.json"
{ echo "== reviewer probes (r709_cases.hpp) on the head talker bench (rc of the bench; RP1[fresh] is the expected failure)"
  pick p-head.log '^FAIL|^RP|checks:'; } > "$R/reviewer-probes-head.txt"
{ for m in own_search_unchecked_step own_pub_upper_slot0 own_search_skips_self own_probe_ignores_da_valid own_output_lags_declaration; do
    echo "== $m (bench rc $(cat $L/m-$m.rc); RP1[fresh] fails at head too and is not a kill witness)"
    pick m-$m.log '^FAIL|checks:'
  done; } > "$R/reviewer-mutants-talker-bench.txt"
{ echo "== own_pub_upper_slot0 through the repository judge (rc $(cat $L/mut-own.rc))"; san < "$L/mut-own.log"; } > "$R/reviewer-mutant-suites.txt"
san < "$pk/scratch/mut-own/results.json" > "$R/reviewer-mutant-suites.results.json"
{ echo "== tb/acmp_talker/retry_mutants.py --jobs 8 at head (rc $(cat $L/retry.rc))"; pick retry.log '^(KILLED|EQUIVALENT|PERFORMANCE|PASS|FAIL)'; } > "$R/retry-campaign-head.txt"
{ echo "== scripts/lint_hdl.sh at head (rc $(cat $L/lint.rc))"; san < "$L/lint.log"
  echo "== make -j16 check at head in a scratch clone (rc $(cat $L/makecheck.rc))"; tail -n 6 "$L/makecheck.log" | san; } > "$R/lint-and-doc-gates-head.txt"
cp "$L/env.txt" "$R/env.txt"
cp "$L/parent-patch.txt" "$R/parent-patch-review.txt"

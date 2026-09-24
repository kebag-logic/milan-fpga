#!/usr/bin/env bash
# R269-3: turn the scratch run logs into publishable receipts.
# usage: collect_receipts.sh <packet dir>
set -u
P=$1
S=$P/scratch
R=$P/receipts
mkdir -p "$R/logs" "$R/mutants"
cd "$S" || exit 90

tally() { grep -E '^checks:' "$1" | tail -1; }

# 1. head legs (exact head, unmutated)
{
  echo "# exact-head milan_dp legs, pinned simulator 5.050, built through probe.mk"
  printf 'leg\ttally\tCTRS-CRF ok\tNOTIFY-CRF ok\n'
  for pair in "nxn:run_base_nxn.log" "nxn8:base_nxn8.run.log" "notify:base_notify.run.log" \
              "nxndv:logs/base_nxndv.run.log" "nxn4c:logs/base_nxn4c.run.log"; do
    leg=${pair%%:*} f=${pair#*:}
    printf '%s\t%s\t%s\t%s\n' "$leg" "$(tally "$f")" \
      "$(grep -c '\[ok\]   \[CTRS-CRF\]' "$f")" "$(grep -c '\[ok\]   \[NOTIFY-CRF\]' "$f")"
    gzip -9 -n -c "$f" > "$R/logs/head_$leg.run.log.gz"
  done
} > "$R/23_head_legs.tsv"

# 2. criterion-3 and related mutants / probes: tally and every FAIL line
{
  printf 'run\ttally\tFAIL lines\n'
  for f in logs/X*__*.run.log logs/H*__*.run.log; do
    n=$(basename "$f" .run.log)
    fails=$(grep -E '^\s*\[FAIL\]' "$f" | sed -E 's/^\s+//' | paste -sd '|' -)
    printf '%s\t%s\t%s\n' "$n" "$(tally "$f")" "${fails:-none}"
    gzip -9 -n -c "$f" > "$R/logs/$n.run.log.gz"
  done
} > "$R/20_mutants_and_probes.tsv"

# 3. the instrumentation lines of H2 (window, delivery step, uns_log sizes)
{
  for f in logs/H2_instrument__*.run.log; do
    echo "== $(basename "$f" .run.log)"; grep '\[r269\]' "$f"
  done
} > "$R/21_window_and_log_instrumentation.txt"

# 4. the CRF-sink-less shape probe
{
  echo "# builder-generated 4x4 shape with clocking.crf_sink false (scratch config)"
  diff "$S/base/configs/endstation_arty_4x4.yaml" "$S/nocrf/endstation_arty_4x4_nocrf.yaml"
  echo "# generated shape constants"
  grep -E 'ADP_(TALKER_SRC|LISTENER_SINK)_C' "$S/nocrf/out/endstation_arty_4x4_nocrf/gen/adp_shape_defaults.svh"
  echo "# simulator stage (elaboration) diagnostics of error class, then the C++ stage error"
  grep -E '%Error-|%Warning-(UNDRIVEN|USERERROR)' logs/nocrf_nxn.build.log || echo "(no elaboration error or UNDRIVEN/USERERROR diagnostic)"
  grep -E 'error:' logs/nocrf_nxn.build.log
} > "$R/22_nocrf_shape_probe.txt" 2>&1
cp "$S/nocrf/endstation_arty_4x4_nocrf.yaml" "$R/mutants/endstation_arty_4x4_nocrf.yaml"

# 5. the 45 exchanges: per-run tally and digest of each full log
{
  printf 'run\ttally\tsha256(full run log)\n'
  for f in logs/S_*__*.run.log; do
    printf '%s\t%s\t%s\n' "$(basename "$f" .run.log)" "$(tally "$f")" "$(sha256sum "$f" | cut -d' ' -f1)"
  done
} > "$R/32_exchange_runs.tsv"

# 6. every mutant as a unified diff against the exact head
for d in mut/*/; do
  n=$(basename "$d")
  if [ -f "$d/milan_datapath.sv" ]; then
    diff -u "base/hdl/milan/milan_datapath.sv" "$d/milan_datapath.sv" \
      | sed -e "1s|.*|--- head/hdl/milan/milan_datapath.sv|" -e "2s|.*|+++ $n/hdl/milan/milan_datapath.sv|" > "$R/mutants/$n.diff"
  else
    diff -u "base/tb/verilator/milan_dp/sim_nxn.cpp" "$d/sim_nxn.cpp" \
      | sed -e "1s|.*|--- head/tb/verilator/milan_dp/sim_nxn.cpp|" -e "2s|.*|+++ $n/tb/verilator/milan_dp/sim_nxn.cpp|" > "$R/mutants/$n.diff"
  fi
done
cp mut/MUTANTS.tsv "$R/mutants/MUTANTS.tsv"
cp swaps/SWAPS.tsv "$R/mutants/SWAPS.tsv"
for d in swaps/S_*/; do
  n=$(basename "$d")
  diff -u base/hdl/milan/milan_datapath.sv "$d/milan_datapath.sv" \
    | sed -e "1s|.*|--- head/hdl/milan/milan_datapath.sv|" -e "2s|.*|+++ $n/hdl/milan/milan_datapath.sv|"
done > "$R/mutants/exchanges_all45.diff"
echo done

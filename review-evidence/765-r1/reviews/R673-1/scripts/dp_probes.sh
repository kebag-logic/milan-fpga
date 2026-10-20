#!/bin/bash
# dp_probes.sh PACKET : the two milan_dp reviewer probes, built one after another.
#  dp6 = the [762-DP] stimulus put back to dev's fixed 2-channel PDU (does the case need the current format?)
#  dp7 = the #762 tie-off plant at milan_datapath's .stopped_i (do the [762-DP] checks still catch it?)
P=$1; export PATH=$P/scratch/bin:$PATH
run() { # tree target name
  ( cd "$P/scratch/$1/tb/verilator/milan_dp" && make --no-print-directory "$2" ) > "$P/receipts/dp-probes/$3.log" 2>&1
  echo "$3 rc=$? $(grep -E 'checks: *[0-9]+ *failures: *[0-9]+|[0-9]+ checks: [0-9]+ PASS' "$P/receipts/dp-probes/$3.log" | tail -1)" >> "$P/receipts/dp-probes/SUMMARY.txt"
  grep -E '^\s*\[(FAIL|fail)\]|FAIL ' "$P/receipts/dp-probes/$3.log" | head -10 | sed "s/^/  $3: /" >> "$P/receipts/dp-probes/SUMMARY.txt"
}
mkdir -p "$P/receipts/dp-probes"; : > "$P/receipts/dp-probes/SUMMARY.txt"
run dp6 run-dynmap dp6_stim2ch_dynmap
run dp6 run-nxn4c dp6_stim2ch_nxn4c
run dp7 run-dynmap dp7_tie0_dynmap
cat "$P/receipts/dp-probes/SUMMARY.txt"

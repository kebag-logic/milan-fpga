#!/usr/bin/env bash
# Re-run the packet's own analysis tools on a copy of the published raw data
# and compare their output byte for byte with the published analysis files.
#
# usage: scripts/rerun_packet_analysis.sh <review-evidence/117-r1 dir> <scratch dir>
set -euo pipefail

ev=$1
work=$2
rm -rf "$work"
mkdir -p "$work/out"
cp -r "$ev/bench-a200" "$ev/bench-a202" "$work/"

same() { cmp -s "$1" "$2" && echo SAME || echo DIFF; }

cd "$work/bench-a202"
for n in 1 2 3 4 5 6; do
  python3 tools/analyze_cycle.py "bench/cycle$n" --json "$work/out/c$n.json" > "$work/out/c$n.txt" 2>&1
  echo "a202 cycle $n analysis.txt $(same "$work/out/c$n.txt" "bench/cycle$n/analysis.txt")" \
       "analysis.json $(same "$work/out/c$n.json" "bench/cycle$n/analysis.json")"
done
python3 tools/summarize.py bench 1 2 3 4 5 6 > "$work/out/summary.txt" 2>&1
echo "a202 summary.txt $(same "$work/out/summary.txt" bench/summary.txt)"

cd "$work/bench-a200"
python3 tools/wire_summary.py bench/runA/tap-runA.pcap > "$work/out/wsA.txt" 2>&1
echo "a200 runA wire-summary.txt $(same "$work/out/wsA.txt" bench/runA/wire-summary.txt)"
python3 tools/pdelay_turnaround.py bench/runA/tap-runA.pcap > "$work/out/pdA.txt" 2>&1
echo "a200 runA pdelay-turnaround.txt $(same "$work/out/pdA.txt" bench/runA/pdelay-turnaround.txt)"

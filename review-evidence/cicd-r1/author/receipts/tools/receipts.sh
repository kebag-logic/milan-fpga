#!/bin/bash
# receipts.sh: copy the text receipts (perf CSVs, times, verdicts, identity comparisons, profiles) into
# the round's receipts/ directory, uncompressed, and report the total size.
set -u
R=$MANAGEMENT/2026-09-23/cicd-a839/round1/receipts
S=/data-2/milan/tmp/cicd-a839/runs
mkdir -p "$R"/{ab,talker,budget,prof,fwb,ccache,bisect,shards,pre}
for d in "$S"/ab/*/*; do
  v=$(basename "$(dirname "$d")"); s=$(basename "$d")
  for f in perf time verdict cmd; do [ -f "$d/$f" ] && cp "$d/$f" "$R/ab/$v.$s.$f"; done
done
P=/data-2/milan/tmp/cicd-a839/pub/tb/verilator/crf_rx
for v in flat vlt vltO2 vltO3; do cp "$P/ts_$v.perf" "$P/ts_$v.time" "$R/talker/" 2>/dev/null; done
md5sum "$P"/ts_*.out | sed 's#/[^ ]*/##' > "$R/talker/outputs.md5"
cp "$P"/prof_flat.txt "$P"/prof_vltO2.txt "$R/talker/" 2>/dev/null
for n in flat vltO2; do perf report -i "$P/prof_$n.data" --stdio --no-children --sort dso,symbol 2>/dev/null | grep -E '^ +[0-9]+\.[0-9]+%' | head -30 > "$R/talker/perf-report-$n.txt"; done
cp "$S"/bud-ab3/*.perf "$S"/bud-ab3/*.time "$R/budget/" 2>/dev/null
md5sum "$S"/bud-ab3/*.log "$S"/bud-ab1/*.log "$S"/bud-ab2/*.log | sed 's#/data-2/milan/tmp/cicd-a839/runs/##' > "$R/budget/outputs.md5"
cp "$S"/prof/*.txt "$S"/prof/*.time "$R/prof/" 2>/dev/null
perf report -i "$S/prof_mdp_gptp.data" --stdio --no-children --sort dso,symbol 2>/dev/null | grep -E '^ +[0-9]+\.[0-9]+%' | head -30 > "$R/prof/milan_dp-gptp-60s.sym.txt"
cp "$S/stat_mdp_gptp.perf" "$R/prof/milan_dp-gptp-60s.perf"
cp "$S"/fwb-base/out.log "$R/fwb/timeline.log"; cp "$S"/fwb-base/time.txt "$S"/fwb-base/perf.txt "$R/fwb/"
cp "$S"/cc/*.time "$R/ccache/"; grep -E "checks:|RESULT" "$S"/cc/*.log | sed 's#.*/##' > "$R/ccache/verdicts.txt"
cp "$S"/pre/*.perf "$R/pre/" 2>/dev/null; tail -1 "$S"/pre/test_suite_cancellation.log "$S"/pre/cancel-after.log > "$R/pre/cancellation-verdicts.txt" 2>/dev/null
B=/data-2/milan/tmp/cicd-a839/tree/pub/tb/verilator/fr_bis
for f in "$B"/r_*.out; do m=$(basename "$f" .out); m=${m#r_}
  if cmp -s "$f" "$S/fr/base-pullin.out"; then echo "$m: IDENTICAL to base"; else echo "$m: differs, $(grep -c FAIL "$f") FAIL, $(grep -o 'render slips [0-9]* across' "$f")"; fi
done > "$R/bisect/follow_ring-pullin-bisect.txt"
diff "$S/fr/base-pullin.out" "$S/fr/pub-pullin.out" | head -40 > "$R/bisect/base-vs-probes-pullin.diff"
cp "$B"/p_KL_chan_map_capture.vlt "$B"/probes.vlt "$R/bisect/" 2>/dev/null
[ -d "$S/shards" ] && cp -r "$S"/shards/*.txt "$R/shards/" 2>/dev/null
du -sb "$R" | awk '{print "receipts total bytes:", $1}'
find "$R" -name '*.gz' | head

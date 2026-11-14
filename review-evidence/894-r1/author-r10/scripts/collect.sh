#!/bin/bash
# Round 10: the gate receipts from the pass's outputs: the workflow step table (verify_wf.py, with round 10's copy of
# not_run.json, whose sweep reasons say the sweep was not run this round), the dispatcher's and the lane gates'
# summaries, the short logs a receipt names, and every log's sha256. No sweep and no harness legs ran (every image
# byte-identical to 5b264bf2's). Host paths are replaced by placeholders. usage: collect.sh HEAD
set -u
H=$1
T=<scratch> G=$T/r10/gates-out V=$T/r10/gates-verify
R=<packet>/receipts/gates
mkdir -p "$R" "$V"
scrub() {
    sed -e "s#$T#<scratch>#g" -e "s#<lane>#<lane>#g" -e "s#<tool-path>[A-Za-z0-9_.-]*#<clone>#g" \
        -e "s#<home-path>[A-Za-z0-9_./-]*#<home-path>#g" -e "s#/data-2/milan/tmp/[A-Za-z0-9_./-]*#<tmp-path>#g" \
        -e "s#<tool-path>[A-Za-z0-9_./-]*#<tool-path>#g" -e "s#/tmp/[A-Za-z0-9_./-]*#<tmp-path>#g" \
        -e "s#/opt/[A-Za-z0-9_./-]*#<opt-path>#g" -e "s#/usr/[A-Za-z0-9_./-]*#<sys-path>#g"
}
cp $T/gates/verify_wf.py $V/verify_wf.py
/usr/bin/python3 - $T/gates/not_run.json $V/not_run.json <<'EOF'
import json, sys
src, dst = sys.argv[1:3]
d = json.load(open(src))
n = 0
for k, v in d.items():
    if "full sweep" in v:
        d[k] = ("not run in round 10: the Verilator sweep is skipped by the round's rule, every image byte-identical "
                "to 5b264bf2's (receipts/images); round 9 ran it at 5b264bf2, 65 suites, 0 failures")
        n += 1
json.dump(d, open(dst, "w"), indent=1, sort_keys=True)
print(f"{n} sweep reasons restated")
EOF
/usr/bin/python3 $V/verify_wf.py "$H" $G/wf rtl-fast.yml rtl.yml elaborate.yml docs.yml \
    --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4 > $T/r10/verify.txt 2>&1
echo "verify rc=$?"
scrub < $T/r10/verify.txt > $R/workflows-verify.md
scrub < $G/dispatch.txt > $R/dispatch.txt
for n in $(cut -d' ' -f1 $G/queue.txt); do echo "$n rc=$(cat $T/units/$n.rc 2>/dev/null || echo '?')"; done > $R/unit-rcs.txt
scrub < $G/lane/summary.txt > $R/lane-summary.txt
for g in em_dash tier_grid py_idiom cpp_idiom docs_check rows_tiers_selftest rows_tiers_report_exits_1 \
         load_selftest load_check flip_selftest flip_check_1x1 flip_check_1x1_as_built_exits_1 flip_check_8x8_exits_1 flip_check_exits_1 \
         fw_coverage_selftest diffcheck_round9_start diffcheck_round10_start ctrl_hot_check ctrl_hot_selftest; do
    scrub < $G/lane/$g.log > $R/lane-$g.txt
done
grep -E "^(MUTANT|self-test|CONTROL .* caught)" $G/lane/harness_selftest.log | scrub | tail -n 40 > $R/lane-harness_selftest.summary.txt
{ grep -c "^MUTANT caught" $G/lane/harness_selftest.log | sed 's/^/MUTANT caught lines: /'
  grep -c "^MUTANT ESCAPED" $G/lane/harness_selftest.log | sed 's/^/MUTANT ESCAPED lines: /'; } >> $R/lane-harness_selftest.summary.txt
tail -n 25 $G/lane/test_builder.log | scrub > $R/lane-test_builder.summary.txt
tail -n 4 $G/lane/behave.log | scrub > $R/lane-behave.summary.txt
for g in twin twin_plants; do tail -n 4 $G/lane/$g.log | scrub > $R/lane-$g.summary.txt; done
for g in nvm_selftest boot_1x1 boot_8x8 boot_native boot_plants; do
    tail -n 6 $G/lane/$g.log | scrub > $R/lane-$g.summary.txt
done
L=$G/wf/logs
{ echo "# the firmware jobs' named steps at $H (run_wf.py, each job on its own clean clone): each step's rc and last line"
  for f in $L/rtl-fast__firmware-*__ci_step_*.log; do
      echo "$(basename "$f" .log) rc=$(cat "${f%.log}.rc" 2>/dev/null || echo '?'): $(tail -n 1 "$f" | cut -c1-200)"
  done
  echo "# the AECP campaign (rtl-fast firmware-aecp-mutants, ci_step_9): $(grep -c '^\[ok\]' $L/rtl-fast__firmware-aecp-mutants__ci_step_9.log) ok, $(grep -c 'ESCAPED' $L/rtl-fast__firmware-aecp-mutants__ci_step_9.log) escaped"
  grep "map-table-each-direction-alone" $L/rtl-fast__firmware-aecp-mutants__ci_step_9.log; } | scrub > $R/firmware-jobs.txt
( cd $G && find wf/logs lane -type f \( -name '*.log' -o -name '*.rc' -o -name 'summary.txt' -o -name 'DONE' \) \
    -print0 | sort -z | xargs -0 sha256sum ) | scrub > $R/gate-logs.sha256
echo "collected into $R: $(ls $R | wc -l) files"

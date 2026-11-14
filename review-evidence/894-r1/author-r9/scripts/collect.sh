#!/bin/bash
# Round 9: the gate receipts from the full pass's outputs: the workflow step table (verify_wf.py), the dispatcher's and the
# lane gates' summaries, the short logs a receipt names, the sweep's shard summaries, the harness legs' first and last
# lines, and every log's sha256. Host paths are replaced by placeholders. usage: collect.sh HEAD
set -u
H=$1
T=<scratch> G=$T/r9/gates-out
R=<management>/894-a773/round9/receipts/gates
mkdir -p "$R"
scrub() {
    sed -e "s#$T#<scratch>#g" -e "s#<lane>#<lane>#g" -e "s#<tool-path>[A-Za-z0-9_.-]*#<clone>#g" \
        -e "s#<home-path>[A-Za-z0-9_./-]*#<home-path>#g" -e "s#/data-2/milan/tmp/[A-Za-z0-9_./-]*#<tmp-path>#g" \
        -e "s#<tool-path>[A-Za-z0-9_./-]*#<tool-path>#g" -e "s#/tmp/[A-Za-z0-9_./-]*#<tmp-path>#g" \
        -e "s#/opt/[A-Za-z0-9_./-]*#<opt-path>#g" -e "s#/usr/[A-Za-z0-9_./-]*#<sys-path>#g"
}
/usr/bin/python3 $T/gates/verify_wf.py "$H" $G/wf rtl-fast.yml rtl.yml elaborate.yml docs.yml \
    --matrix=yosys-shards=shard:0-4,1-4,2-4,3-4 > $T/r9/verify.txt 2>&1
echo "verify rc=$?"
scrub < $T/r9/verify.txt > $R/workflows-verify.md
scrub < $G/dispatch.txt > $R/dispatch.txt
# each queued unit's own rc (a dispatcher stopped to re-spread its unstarted lines logs no end for the units it started)
for n in $(cut -d' ' -f1 $G/queue.txt); do echo "$n rc=$(cat $T/units/$n.rc 2>/dev/null || echo '?')"; done > $R/unit-rcs.txt
scrub < $G/lane/summary.txt > $R/lane-summary.txt
for g in em_dash tier_grid py_idiom cpp_idiom docs_check rows_tiers_selftest rows_tiers_report_exits_1 \
         load_selftest load_check flip_selftest flip_check_1x1 flip_check_1x1_as_built_exits_1 flip_check_8x8_exits_1 flip_check_exits_1 \
         fw_coverage_selftest diffcheck_round5 diffcheck_810_084cf7a8 diffcheck_round6 diffcheck_round7_start diffcheck_round8_start diffcheck_round9_start ctrl_hot_check ctrl_hot_selftest; do
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
for k in 0 1 2 3; do
    S=$G/sweep/shard-$k
    { echo "# head $H, its own clone, exit_code $(/usr/bin/python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print(d['exit_code'], 'head', d['head'])" $S/spec/complete.json 2>/dev/null || echo '?')"
      sed -n '/^shard: /,$p' $S/spec/01.log | grep -v '^logs: '; } | scrub > $R/sweep-shard$k.txt
done
{ echo "# the CPU budget harness built at $H on a clean clone (leg.sh: run.py --point P --groups G), the committed ledger;"
  echo "# each build's first and last lines and its image plan"
  for b in H-L1A H-L1N H-L8A H-L8N H-L1L H-L8L H-81L H-81A H-81N H-L1O H-L8O C-R1 H-J1 H-J8 H-J81; do
      echo "== $b"; head -n 1 $T/units/$b.log; grep -E "groups graded|^SLICES|^JOINS|^STATED|^SHARE|^CLOCK|^CONTROL|^END" $T/units/$b.log
      /usr/bin/python3 -c "import json,sys; p=json.load(open(sys.argv[1]))['ctrl_plan']; print(f\"image plan: rom {p['rom']['bytes']} B in {sum(p['rom']['banks'])}, sram {p['sram']['bytes']} B in {sum(p['sram']['banks'])}, {p['tiles']} RAMB36, ledgered {p.get('ledgered')} {p.get('ledgered_tiles')}\")" \
          $G/builds/$b/build.json 2>/dev/null
  done; } | scrub > $R/harness-head-builds.txt
( cd $G && find wf/logs lane sweep -type f \( -name '*.log' -o -name '*.rc' -o -name 'summary.txt' -o -name 'DONE' \) \
    -print0 | sort -z | xargs -0 sha256sum ) | scrub > $R/gate-logs.sha256
echo "collected into $R: $(ls $R | wc -l) files"

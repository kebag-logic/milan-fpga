#!/bin/bash
# collect_r2.sh: copy this round's receipts into the output directory's receipts/, host prefixes replaced
# (collect.py, sanitize.py), files over 200 KB listed in LARGE.tsv by size and sha256, then write receipts/INDEX.md
set -eu
S=<scratch>; G=$S/gates; R=$G/pass1
D=<management>/2026-09-23/665s11-a761c/receipts
P=$G/prefixes.tsv
C="$S/venv/bin/python3 $G/tools/wf/collect.py $P"
rm -rf $D; mkdir -p $D
[ -d $R/logs ] && $C $R/logs $D/gates/wf '*'
[ -d $R/docs/logs ] && $C $R/docs/logs $D/gates/docs '*'
[ -d $R/lane ] && $C $R/lane $D/gates/lane '*'
[ -d $R/drivers ] && $C $R/drivers $D/gates/drivers '*'
for s in 0 1 2 3; do
  [ -d $G/sweep/out2/shard-$s ] && $C $G/sweep/out2/shard-$s $D/sweep/shard-$s 'spec/*' 'logs/*.log' 'logs/preflight/*'
done
$C $G/sweep $D/sweep 'full-native.json' 'launch2.txt' 'sweep_launch.py'
$C $G/tools $D/gates/tools '*.sh' '*.py' '*.json' 'wf/*.py' 'wf/*.json'
$C $S/stage/s2-base $D/s2-base '*'
$C $S/stage/history-9534d51f $D/history-9534d51f '*'
$C $S/probes $D/probes 'r821.log' 'r821.rc' 'r821/results.json' 'r821/*.log' 'r822.log' 'r822.rc' 'b20mut.out' 'b20mut/platboot1.log'
$C $S/exports $D/exports 'compare.txt' '*.commit' '*.status' '*-ax7101_*.log'
$C $S/scripts $D/scripts '*.py' '*.sh' 'tie.patch' 'reviewer/*'
$C $S/size $D/size 'wt1/*.txt' 'wt1/*.log' 'base-1d6bf555/*.txt' 'base-1d6bf555/*.log' 'delta.md'
$C $S/stage/coverage $D/coverage '*'
$C $S/stage/history-10b0fe93 $D/history-10b0fe93 '*'
$C $S/stage/history-d08d30c6-census $D/history-d08d30c6-census '*'
$C $S/tools $D/scripts/env 'env.sh' 'launch.sh'
for t in wf-table.md docs-table.md; do
  [ -f $G/$t ] && cp $G/$t $D/gates/$t && $S/venv/bin/python3 $G/tools/wf/sanitize.py $P $D/gates/$t
done
$S/venv/bin/python3 $G/tools/wf/make_index.py $D
find $D -type f -size +200k

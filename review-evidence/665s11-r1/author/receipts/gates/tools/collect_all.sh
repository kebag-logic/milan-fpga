#!/bin/bash
# collect_all.sh <pass root>: copy the final gate pass's logs, tables and tools into the output directory's
# receipts/, host prefixes replaced (collect.py, sanitize.py), then write receipts/INDEX.md
set -eu
R=$1
G=<scratch>/gates
D=<management>/2026-09-23/665s11-a761/receipts
P=$G/prefixes.tsv
C="$G/venv/bin/python3 $G/tools/wf/collect.py $P"
rm -rf $D/gates $D/sweep $D/s2-base $D/history-bc939bc727
# the pass at bc939bc727 the HANDOFF's history cites: the boundary refusal, gate_19's two UNKNOWN runs, the
# timing-cuts test alone
$C $G/pass3/logs $D/history-bc939bc727 'rtl-fast.firmware-boundary__ci_step_9.*' \
  'elaborate.elaborate-gates-1__gate_19.try*' 'elaborate.elaborate-gates-1__gate_19.rerun-note' 'standalone.*'
$C $R/logs $D/gates/wf '*'
$C $R/docs/logs $D/gates/docs '*'
$C $R/lane $D/gates/lane '*'
$C $R/drivers $D/gates/drivers '*'
for s in 0 1 2 3; do
  $C $G/sweep/out4/shard-$s $D/sweep/shard-$s 'spec/*' 'logs/*.log' 'logs/preflight/*'
done
$C $G/sweep $D/sweep 'full-native.json' 'launch4.sh' 'launch4.txt'
[ -d $G/base/lane ] && $C $G/base/lane $D/s2-base '*'
$C $G/tools $D/gates/tools '*.sh' '*.py' '*.json' 'wf/*.py' 'wf/*.json'
$C <scratch>/tools $D/gates/tools/bg 'bg.sh' 'waitev.sh' 'stage4.sh' 'g19*.sh'
for t in wf-table.md docs-table.md; do
  [ -f $R/$t ] && cp $R/$t $D/gates/$t && $G/venv/bin/python3 $G/tools/wf/sanitize.py $P $D/gates/$t
done
$G/venv/bin/python3 $G/tools/wf/make_index.py $D
find $D -type f -size +200k

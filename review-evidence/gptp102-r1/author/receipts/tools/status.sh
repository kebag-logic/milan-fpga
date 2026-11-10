#!/bin/bash
# one-line status of my units: baseline verdicts, eq progress (mutant dirs per run), after state
S=/data-2/milan/tmp/gptp102-a762
b=$(grep -c "mutant caught\|SURVIVED\|\] mutant\|\] mutation\|unmutated" $S/runs/before/make.log 2>/dev/null)
bl=$(tail -1 $S/runs/before/make.log 2>/dev/null | awk '{print $1}')
eq=$(for d in $S/tmp/eq/engine-mutants-*; do [ -d "$d" ] && ls -d $d/mutant-* 2>/dev/null | wc -l; done | tr '\n' '/')
a=$(tail -1 $S/runs/after/make.log 2>/dev/null | cut -c1-60)
echo "$(date +%T) before[$(systemctl --user is-active milan-gptp102-a762-before)] verdicts=$b t=$bl | eq[$(systemctl --user is-active milan-gptp102-a762-eq)] mutant-dirs=$eq | after[$(systemctl --user is-active milan-gptp102-a762-after)] $a | scratch $(du -sh $S 2>/dev/null | cut -f1)"

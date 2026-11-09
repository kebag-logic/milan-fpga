#!/usr/bin/env bash
# st.sh: one screen of this round's progress
S=$VALIDATION_STORAGE/scratch/a746f; H=$(cat $S/HEAD.txt); R=$S/ci/${H:0:12}
n=$(ls $R/jobs/*/result.json 2>/dev/null | wc -l)
bad=$(for j in $R/jobs/*/result.json; do python3 -c "import json,sys; r=json.load(open('$j')); print(r['result'])"; done 2>/dev/null | grep -vc "success\|skipped")
run=$(for d in $R/jobs/*/; do [ -f $d/result.json ] || basename $d; done | tr '\n' ' ')
echo "$(date +%T) replay $n/69, not success $bad; running: $run"
grep -h "rc [1-9]" $S/logs/ci-local*.log
tail -n 1 $S/logs/gates.log
for k in 0 1 2 3; do f=$S/sweep/shard-$k/spec/01.log; [ -f $f ] && echo "shard $k: $(grep -c "PASS\|passed" $f 2>/dev/null) pass-lines, last: $(tail -n 1 $f | cut -c1-100)"; done
systemctl --user list-units --plain --no-legend 'milan-a746f-*' | awk '{print $1}' | sed 's/milan-a746f-//;s/.service//' | tr '\n' ' '; echo
grep MemAvailable /proc/meminfo

#!/usr/bin/env bash
# status_h.sh: one view of every exact-head gate, the CPU booking and memory.
H=519d9c2be139d2f777127a4aa19ea9ed251392a5; S=<scratch>; G=$S/gates-$H
date +%H:%M:%S
for f in $S/camp-logs-$H $G/fw $G/rtl $G/builder $G/builder-litex; do
  n=$(ls $f/*.rc 2>/dev/null | wc -l); bad=$(for r in $f/*.rc; do [ -e "$r" ] && [ "$(cat $r)" != 0 ] && echo "${r##*/}=$(cat $r)"; done | tr '\n' ' ')
  printf '%-14s rc files %-3s done %-3s nonzero: %s| last: %s\n' "${f##*/}" "$n" "$([ -e $f/DONE ] && echo yes || echo no)" "$bad" "$(tail -1 $f/progress.txt 2>/dev/null | cut -c1-50)"
done
R=$S/docsyml-$H; printf 'docsyml        runner lines %s nonzero: %s| all_done %s verify %s| %s\n' "$(grep -c 'rc=' $R/runner.out)" "$(grep -E 'rc=[1-9]' $R/runner.out | tr '\n' ' ')" "$([ -e $R/ALL_DONE ] && echo yes || echo no)" "$(cat $R/verify.rc 2>/dev/null)" "$(tail -1 $R/runner.out | cut -c1-50)"
python3 <mgmt>/cpu_ranges.py show
echo "pick: $(python3 <mgmt>/cpu_ranges.py pick)"
grep MemAvailable /proc/meminfo | awk '{printf "MemAvailable %.1f GB\n",$2/1048576}'
systemctl --user list-units 'milan-845-a738b-*' --no-legend --plain | awk '{printf "%s ", $1}'; echo
for k in 0 1 2 3; do d=$S/sweep-${H:0:8}/shard-$k; [ -d "$d" ] || continue; c=""; [ -e $d/spec/complete.json ] && c=$(python3 -c "import json;print('exit',json.load(open('$d/spec/complete.json'))['exit_code'])"); printf 'shard %s logs %-3s %s | %s\n' $k "$(ls $d/logs 2>/dev/null | wc -l)" "$c" "$(tail -1 $d/spec/01.log 2>/dev/null | cut -c1-70)"; done

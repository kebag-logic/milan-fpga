#!/usr/bin/env bash
# The tdm8render-pullin recipe of tb/verilator/milan_dp_render/Makefile, run
# on the clean shipping binary the tdm8render-mutants campaign built at the
# same head with the same recipe (tdm8render-build), copied in, so no third
# Verilator build runs beside the two campaigns. PULLIN_JOBS=4.
# usage: pullin_legs.sh <clone>
set -u
here=$(cd "$(dirname "$0")" && pwd)
source "$here/env.sh"
O=$VALIDATION_STORAGE/scratch/632-a659/r7/camp/pullin
mkdir -p "$O"
cd "$1/tb/verilator/milan_dp_render" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
sha256sum obj_tdm8r/Vmilan_dp_tdm8r > "$O/binary.sha256"
PULLIN_PHASES="0 130 260 391 521 651 781 911 927 1042 1156 1172 1302 1432 1562 1693 1823 1953"
mkdir -p obj_pullin
date -Is > "$O/start"
printf '%s\n' history $PULLIN_PHASES | xargs -P 4 -I{} \
  sh -c 'case "$1" in history) mode=--with-pullin;; *) mode=--pullin=$1;; esac; \
    ./obj_tdm8r/Vmilan_dp_tdm8r "$mode" > obj_pullin/pullin_$1.log 2>&1; echo $? > obj_pullin/pullin_$1.rc' sh {}
echo $? > "$O/rc"
grep -h -e "settle recentre came" -e "FAIL" obj_pullin/pullin_*.log > "$O/grep.txt"
date -Is > "$O/end"
for f in obj_pullin/pullin_*.log; do
  p=${f#obj_pullin/pullin_}; p=${p%.log}
  printf '%s rc=%s %s\n' "$p" "$(cat obj_pullin/pullin_$p.rc)" "$(grep -E 'checks: *[0-9]+ +failures' "$f" | tail -1)"
done > "$O/legs.txt"
cp obj_pullin/pullin_*.log "$O/"

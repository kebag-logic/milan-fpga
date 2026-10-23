#!/usr/bin/env bash
# Round 7b: the tdm8render-pullin recipe of tb/verilator/milan_dp_render/Makefile
# (history + the 18 PULLIN_PHASES, PULLIN_JOBS=4), run in its own clean clone at
# <rev> on the clean shipping binary that the tdm8render-mutants campaign's
# tdm8render-build made at the same head with the same recipe, copied in with
# the three runtime files it reads (sha256 of both copies recorded), so no
# third Verilator build runs beside the two campaigns. The mutants build in a
# temporary directory, so the campaign clone's obj_tdm8r stays the clean build.
# Waits for the campaign log to pass both builds first.
# usage: pullin_legs.sh <rev> <campaign clone>
set -u
rev=$1; src=$2; h=${rev:0:8}
R7=$MANAGEMENT/2026-09-23/632-a659/scripts/round7
source "$R7/env.sh"
S=$VALIDATION_STORAGE/scratch/632-a659/r7
O=$S/camp/pullin-$h
C=$S/clone-pullin-$h
mkdir -p "$O"
until grep -q -e "#447 render lane" "$S/camp/tdm8m-$h/log" 2>/dev/null; do
  [ -f "$S/camp/tdm8m-$h/rc" ] && { echo "campaign ended before its builds"; exit 3; }
  sleep 30
done
[ -d "$C" ] || bash "$R7/make_clone.sh" "$C" "$rev" > "$O/clone.log" 2>&1
D=tb/verilator/milan_dp_render
mkdir -p "$C/$D/obj_tdm8r"
for f in obj_tdm8r/Vmilan_dp_tdm8r ltn_rom.hex ucode.hex tdm8r_aemi.bin; do cp -p "$src/$D/$f" "$C/$D/$f"; done
( cd "$S" && for f in obj_tdm8r/Vmilan_dp_tdm8r ltn_rom.hex ucode.hex tdm8r_aemi.bin; do
    sha256sum "clone-tdm8m-$h/$D/$f" "clone-pullin-$h/$D/$f"; done ) > "$O/binary_provenance.sha256"
printf '%s\n' "the Makefile's tdm8render-pullin recipe (PULLIN_JOBS=4) via scripts/round7b/pullin_legs.sh, on obj_tdm8r/Vmilan_dp_tdm8r built by tdm8render-build inside the tdm8render-mutants campaign at the same head" > "$O/command.txt"
cd "$C/$D" || exit 2
git rev-parse HEAD > "$O/HEAD.txt"
git status --short --ignored=no > "$O/status.txt"
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

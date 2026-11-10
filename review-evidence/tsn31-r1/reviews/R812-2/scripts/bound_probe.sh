#!/bin/bash
# usage: bound_probe.sh <packet> <head clone> <scratch work dir>
# 1. Run R811-1's every-sink probe (published) and this packet's last-sink probe at N = 33, 64, 65, 255 sinks under
#    -fsanitize=shift,undefined without recovery, against the head's src/acmp.c (exported by git archive).
# 2. Plant each of the two _Static_asserts (off by one, removed) into an exported copy and run the conditional gate's
#    capacity_controls() from that copy: each plant must make the control raise. The unplanted copy must pass.
P=$1 C=$2 W=$3; . "$P/scripts/env.sh"
rm -rf "$W"; mkdir -p "$W/head"; git -C "$C" archive HEAD | tar -x -C "$W/head"; H=$W/head
GT=$(pkg-config --cflags gmock gtest); GL=$(pkg-config --libs gmock gtest)
SAN="-fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
g++ -std=c++20 -O0 -g $GT -c "$H/tests/main.cpp" -o "$W/main.o" || exit 9
echo "== 1. functional probes at wide sink counts"
for n in 33 64 65 255; do
  gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -DACMP_MAX_SINKS=${n}u $SAN -I"$H/include" -c "$H/src/acmp.c" -o "$W/a$n.o" || { echo "N=$n core build rc=$?"; continue; }
  for t in "$P/scratch/r811pub/scripts/every_sink_probe.cpp" "$P/scripts/last_sink_probe.cpp"; do
    b=$W/$(basename "$t" .cpp)-$n
    g++ -std=c++20 -O0 -g -DACMP_MAX_SINKS=${n}u $SAN $GT -I"$H/include" -I"$H/tests" "$t" "$W/a$n.o" "$W/main.o" $GL -o "$b" || { echo "N=$n $(basename $t) build failed"; continue; }
    "$b" > "$b.log" 2>&1; echo "N=$n $(basename "$t" .cpp) rc=$? $(grep -E '^\[  (PASSED|FAILED)  \]' "$b.log" | head -2 | tr '\n' ' ') $(grep -c 'runtime error' "$b.log") sanitizer reports"
  done
done
echo "== 2. capacity controls of scripts/check_conditionals.py against planted refusals"
M='_Static_assert(sizeof ((struct acmp_owed *)0)->release * 8u >= ACMP_MAX_SINKS,'
Q='_Static_assert(ACMP_MAX_SINKS <= UINT8_MAX,'
for plant in none mask-off-by-one mask-removed probe-off-by-one probe-removed; do
  D=$W/cc-$plant; mkdir -p "$D"; git -C "$C" archive HEAD | tar -x -C "$D"
  case $plant in
    mask-off-by-one) old=$M; new='_Static_assert(sizeof ((struct acmp_owed *)0)->release * 8u > ACMP_MAX_SINKS,';;
    mask-removed) old=$M$'\n\t       "the owed release mask holds a bit for every sink");\n'; new='';;
    probe-off-by-one) old=$Q; new='_Static_assert(ACMP_MAX_SINKS < UINT8_MAX,';;
    probe-removed) old=$Q' "the owed probe_of names one plus the index of every sink");'$'\n'; new='';;
    *) old=;;
  esac
  if [ -n "$old" ]; then python3 -I -c 'import sys; p,o,n=sys.argv[1:]; t=open(p).read(); assert t.count(o)==1, "match"; open(p,"w").write(t.replace(o,n))' "$D/src/acmp.c" "$old" "$new" || { echo "$plant: plant did not apply"; continue; }; fi
  mkdir -p "$D/work"
  python3 -I -c 'import sys; sys.path.insert(0, sys.argv[1]); import check_conditionals as c; c.capacity_controls(__import__("pathlib").Path(sys.argv[2]))' "$D/scripts" "$D/work" > "$D/cc.log" 2>&1; rc=$?
  echo "plant=$plant capacity_controls rc=$rc :: $(grep -E 'capacity control' "$D/cc.log" | tail -1 | cut -c1-150)"
done

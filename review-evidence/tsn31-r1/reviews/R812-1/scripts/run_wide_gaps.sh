#!/bin/bash
# Build scripts/test_wide_gaps.cpp at 33 sinks against a tsn-c-stack tree, unplanted and with three plants.
# usage: run_wide_gaps.sh <packet> <clean tree> <scratch work dir>
P=$1 T=$2 W=$3
. "$P/scripts/env.sh" "$P"
GT=$(pkg-config --cflags gmock gtest); GL=$(pkg-config --libs gmock gtest)
F="-DACMP_MAX_SINKS=33u -fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
rm -rf "$W"; mkdir -p "$W"
g++ -std=c++20 -O0 -g $GT -c "$T/tests/main.cpp" -o "$W/main.o" || exit 9
g++ -std=c++20 -O0 -g -Wall -Wextra -Werror $F $GT -I"$T/include" -I"$T/tests" -c "$P/scripts/test_wide_gaps.cpp" -o "$W/gaps.o" || exit 9
for plant in none memset-first-word-only memset-removed set-index-off-by-one; do
  D=$W/$plant; mkdir -p "$D"; cp -r "$T/src" "$T/include" "$D/"
  case $plant in
    memset-first-word-only) old='memset(o->release, 0, sizeof o->release);'; new='memset(o->release, 0, sizeof o->release[0]);';;
    memset-removed) old='memset(o->release, 0, sizeof o->release);'; new=';';;
    set-index-off-by-one) old='o->release[(release - 1u) / 32u] ='; new='o->release[release / 32u] =';;
    *) old=; new=;;
  esac
  if [ -n "$old" ]; then
    python3 -I -c 'import sys; p,o,n=sys.argv[1:]; t=open(p).read(); assert t.count(o)==1, "match"; open(p,"w").write(t.replace(o,n))' "$D/src/acmp.c" "$old" "$new" || exit 9
  fi
  gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT $F -I"$D/include" -c "$D/src/acmp.c" -o "$D/acmp.o" || exit 9
  g++ "$D/acmp.o" "$W/gaps.o" "$W/main.o" -fsanitize=shift,undefined $GL -o "$D/gaps" || exit 9
  "$D/gaps" > "$D/run.log" 2>&1; rc=$?
  echo "plant=$plant rc=$rc failed=$(grep -c '^\[  FAILED  \] WideGaps' "$D/run.log") $(grep -o 'GAP[12] [^"]*' "$D/run.log" | sort -u | tr '\n' ';')"
done

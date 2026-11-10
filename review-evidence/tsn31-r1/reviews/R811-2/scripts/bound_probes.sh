#!/bin/sh
# SPDX-License-Identifier: MIT
# Paths in receipts are shown as $PACKET (this packet), $CLONE (the review clone at the head), $TOOLS and $HOME.
# usage: bound_probes.sh TREE WORK -- (1) the probe_of runtime probe at 254 and 255 sinks on the committed core, and at
# 256 sinks with only the probe_of _Static_assert removed; (2) the conditional gate's capacity controls on an exact
# copy and on copies with each _Static_assert removed (each must fail); (3) direct gcc/clang refusals and their texts.
TREE=$1 W=$2
. "$(dirname "$0")/r1/env.sh"
H=$(cd "$(dirname "$0")" && pwd)
G=$CMAKE_PREFIX_PATH
mkdir -p "$W"
copy() { rm -rf "$W/$1"; mkdir -p "$W/$1"; (cd "$TREE" && git archive HEAD) | tar -x -C "$W/$1"; }
drop() { python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();assert s.count(sys.argv[2])==1;open(p,'w').write(s.replace(sys.argv[2],''))" "$1/src/acmp.c" "$2"; }
MASK='_Static_assert(sizeof ((struct acmp_owed *)0)->release * 8u >= ACMP_MAX_SINKS,
	       "the owed release mask holds a bit for every sink");'
PROBE='_Static_assert(ACMP_MAX_SINKS <= UINT8_MAX, "the owed probe_of names one plus the index of every sink");'
copy committed; copy no-probe-assert; drop "$W/no-probe-assert" "$PROBE"; copy no-mask-assert; drop "$W/no-mask-assert" "$MASK"
probe() { t=$1 n=$2; b=$W/$t.probe$n
  gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -DACMP_MAX_SINKS=${n}u -fsanitize=shift,undefined \
    -fno-sanitize-recover=shift,undefined -I "$W/$t/include" -c "$W/$t/src/acmp.c" -o $b.o > $b.build 2>&1 &&
  g++ -std=c++20 -O0 -g -DACMP_MAX_SINKS=${n}u -fsanitize=shift,undefined -I "$W/$t/include" -I "$TREE/tests" -I "$G/include" \
    "$H/probe_of_bound.cpp" "$TREE/tests/main.cpp" $b.o "$G/lib/libgmock.a" "$G/lib/libgtest.a" -lpthread -o $b >> $b.build 2>&1 ||
    { echo "$t at $n sinks: BUILD rc $? $(grep -o 'error: .*' $b.build | head -1)"; return; }
  $b > $b.out 2>&1; rc=$?; echo "$t at $n sinks: run rc $rc; $(grep -h 'PASSED  \]\|FAILED  \]\|Which is\|runtime error' $b.out | head -3 | tr '\n' ' ')"; }
probe committed 254; probe committed 255; probe committed 256; probe no-probe-assert 256
for t in committed no-probe-assert no-mask-assert; do
  mkdir -p "$W/$t/build-conditionals"
  (cd "$W/$t" && python3 scripts/check_conditionals.py --selftest --work build-conditionals --jobs 16 > "$W/$t.cond.log" 2>&1); rc=$?
  echo "conditional selftest on $t: rc $rc; $(grep -h 'capacity control' "$W/$t.cond.log" | tr '\n' ' ' | cut -c1-700)"
done
for cc in gcc clang; do for n in 255 256; do
  $cc -x c -std=c11 -Wall -Wextra -Werror -I "$W/committed/include" -DACMP_MAX_SINKS=${n}u -fsyntax-only "$W/committed/src/acmp.c" > "$W/$cc.$n.syn" 2>&1
  echo "$cc $($cc --version | head -1) at $n sinks: rc $?; $(grep -o 'error: .*' "$W/$cc.$n.syn" | head -2 | tr '\n' ' ')"; done; done

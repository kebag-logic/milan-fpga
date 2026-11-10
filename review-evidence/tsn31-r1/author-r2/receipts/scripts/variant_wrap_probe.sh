#!/bin/sh
# usage: variant_wrap_probe.sh TREE WORK -- the slot-reuse tests of TREE, built at 16 and 33 sinks with mutation.py's flags,
# against four cores: TREE's, TREE's with the release clear deleted (acmp-owed-release-not-cleared), R812-1 S1's
# direct increment (direct_increment_variant.py), and that variant with the clear deleted.
T=$1 W=$2; H=$(dirname "$0")
rm -rf "$W"; mkdir -p "$W"
GT=$(pkg-config --cflags gmock gtest); GL=$(pkg-config --libs gmock gtest)
WIDE="-DACMP_MAX_SINKS=33u -fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
g++ -std=c++20 -O0 -g $GT -c "$T/tests/main.cpp" -o "$W/main.o" || exit 9
g++ -std=c++20 -O0 -g -Wall -Wextra -Werror $GT -I"$T/include" -I"$T/tests" -I"$T/examples" -c "$T/tests/test_acmp.cpp" -o "$W/t16.o" || exit 9
g++ -std=c++20 -O0 -g -Wall -Wextra -Werror $WIDE $GT -I"$T/include" -I"$T/tests" -c "$T/tests/test_acmp_wide.cpp" -o "$W/t33.o" || exit 9
python3 -I "$H/direct_increment_variant.py" "$T" "$W/variant" > /dev/null || exit 9
mkdir -p "$W/head"; cp -r "$T/src" "$T/include" "$W/head/"
for core in head variant; do
  cp -r "$W/$core" "$W/$core-uncleared"
  python3 -I -c 'import sys; p=sys.argv[1]; o="\tmemset(o->release, 0, sizeof o->release);\n"; t=open(p).read(); assert t.count(o)==1; open(p,"w").write(t.replace(o,""))' "$W/$core-uncleared/src/acmp.c" || exit 9
done
for core in head head-uncleared variant variant-uncleared; do D=$W/$core
  gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -I"$D/include" -c "$D/src/acmp.c" -o "$D/a16.o" || exit 9
  gcc -std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT $WIDE -I"$D/include" -c "$D/src/acmp.c" -o "$D/a33.o" || exit 9
  g++ "$D/a16.o" "$W/t16.o" "$W/main.o" $GL -o "$D/acmp16" && g++ "$D/a33.o" "$W/t33.o" "$W/main.o" -fsanitize=shift,undefined $GL -o "$D/wide33" || exit 9
  "$D/acmp16" --gtest_filter='*InTheSlotOf*' > "$D/acmp16.out" 2>&1; r16=$?
  "$D/wide33" --gtest_filter='*InTheSlotOf*' > "$D/wide33.out" 2>&1; r33=$?
  echo "== $core: 16-sink rc=$r16, 33-sink rc=$r33"
  cat "$D/acmp16.out" "$D/wide33.out" | grep -E '^(A19|W[45]) |^\[  FAILED  \] [A-Z]|^\[  PASSED' | sort | uniq -c
done

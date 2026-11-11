#!/bin/bash
# Each round 2 plant against round 1's ACMP suites (acmp_tests, acmp_wide, acmp_walk at 9043b926), built the way the
# mutation driver builds its arms (scripts/mutation.py cflags, cppflags and WIDE). usage: escape_light.sh OUT
set -u
. <scratch>/scripts/env.sh
S=<scratch> O=$1 R1=9043b926532dc4ffb57218ee0eebca7564262289
mkdir -p $O/r1/tests $O/plants
for f in test_acmp.cpp test_acmp_wide.cpp test_acmp_walk.cpp acmp_fake.hpp main.cpp; do git -C $S/trees/head show $R1:tests/$f > $O/r1/tests/$f; done
WIDE="-DACMP_MAX_SINKS=33u -fsanitize=shift,undefined -fno-sanitize-recover=shift,undefined"
C="-std=c11 -O0 -g -Wall -Wextra -Werror -DNDEBUG -DCTRL_REENTRY_ASSERT -I$S/trees/head/include"
X="-std=c++20 -O0 -g -Wall -Wextra -Werror $(pkg-config --cflags gmock gtest) -I$S/trees/head/include -I$S/trees/head/examples -I$O/r1/tests"
L="$(pkg-config --libs gmock gtest)"
g++ $X -c $O/r1/tests/main.cpp -o $O/main.o || exit 2
g++ $X -c $O/r1/tests/test_acmp.cpp -o $O/acmp_tests.o || exit 2
g++ $X $WIDE -c $O/r1/tests/test_acmp_wide.cpp -o $O/acmp_wide.o || exit 2
g++ $X $WIDE -c $O/r1/tests/test_acmp_walk.cpp -o $O/acmp_walk.o || exit 2
python3 - "$O" <<'PY'
import json, sys
S='<scratch>'; O=sys.argv[1]
src=open(S+'/trees/head/src/acmp.c').read()
new=['walk-bind-second-word-unmarked','walk-unbind-second-word-unmarked','walk-release-second-word-unmarked','walk-probe-left-second-word-unmarked','walk-marks-never-cleared','walk-interface-marks-never-cleared','walk-clear-first-word-only']
open(O+'/plants/none.c','w').write(src)
for m in json.load(open(S+'/trees/head/tests/mutations.json')):
    if m['name'] in new:
        assert src.count(m['old'])==1
        open(O+'/plants/'+m['name']+'.c','w').write(src.replace(m['old'],m['new']))
PY
for p in $O/plants/none.c $O/plants/walk-*.c; do
  n=$(basename $p .c); d=$O/run-$n; mkdir -p $d
  gcc $C -c $p -o $d/acmp16.o && gcc $C $WIDE -c $p -o $d/acmp33.o || { echo "$n: build failed"; continue; }
  g++ $d/acmp16.o $O/acmp_tests.o $O/main.o $L -o $d/acmp_tests
  g++ $d/acmp33.o $O/acmp_wide.o $O/main.o -fsanitize=shift,undefined $L -o $d/acmp_wide
  g++ $d/acmp33.o $O/acmp_walk.o $O/main.o -fsanitize=shift,undefined $L -o $d/acmp_walk
  line="$n at round 1's suite:"
  for t in acmp_tests acmp_wide acmp_walk; do
    $d/$t --gtest_brief=1 > $d/$t.log 2>&1; rc=$?
    line="$line $t rc=$rc failed=$(grep -c '^\[  FAILED  \] [A-Za-z]*\.' $d/$t.log | head -1)"
  done
  echo "$line"
  grep -h "^\[  FAILED  \] [A-Za-z]*\." $d/*.log | sort -u | sed 's/^/    /' | head -8
  rm -f $d/acmp_tests $d/acmp_wide $d/acmp_walk $d/*.o
done

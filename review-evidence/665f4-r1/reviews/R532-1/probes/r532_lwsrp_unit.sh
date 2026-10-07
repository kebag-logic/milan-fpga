#!/bin/bash
# usage: r532_lwsrp_unit.sh CLONE SCRATCH NAME [FILE OLD NEW]  -- build lwSRP's cgreen suite in a copy, optionally mutated
set -u
CLONE=$1; S=$2; NAME=$3
W=$S/lwunit/$NAME; rm -rf $W; mkdir -p $W
git -C $CLONE/third_party/lwSRP archive HEAD | tar -x -C $W
if [ $# -ge 6 ]; then
  python3 - "$W/$4" "$5" "$6" <<'PY'
import sys; p,o,n=sys.argv[1:4]; t=open(p).read(); o=o.encode().decode('unicode_escape'); n=n.encode().decode('unicode_escape')
assert t.count(o)==1, f"{t.count(o)} sites"; open(p,'w').write(t.replace(o,n))
PY
  [ $? -eq 0 ] || { echo "[$NAME] PLANT-REFUSED"; exit 3; }
fi
cmake -S $W -B $W/b -DCMAKE_PREFIX_PATH=$S/cgreen-inst > $W/cmake.log 2>&1 || { echo "[$NAME] CMAKE-FAIL"; exit 4; }
make -C $W/b -j4 unit_tests > $W/make.log 2>&1 || { echo "[$NAME] BUILD-FAIL"; tail -5 $W/make.log; exit 5; }
LD_LIBRARY_PATH=$S/cgreen-inst/lib $W/b/unit_tests > $W/run.log 2>&1; rc=$?
echo "[$NAME] rc=$rc $(grep -E 'Completed|passes|failures' $W/run.log | tail -1)"
grep -E 'Failure|failed' $W/run.log | head -3

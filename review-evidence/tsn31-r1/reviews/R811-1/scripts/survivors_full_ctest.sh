#!/bin/sh
# usage: survivors_full_ctest.sh TREE WORK -- each review mutant that survived both ACMP binaries is planted into a copy
# of the tree and the whole CTest suite (GCC Debug, the CI's configuration without coverage) is built and run.
TREE=$1 W=$2
. "$(dirname "$0")/../env.sh"
mkdir -p "$W"
run() { name=$1; old=$2; new=$3
  d=$W/$name; rm -rf "$d"; mkdir -p "$d"; (cd "$TREE" && git archive HEAD) | tar -x -C "$d/"
  python3 -I -c "import sys;p=sys.argv[1];s=open(p).read();assert s.count(sys.argv[2])==1;open(p,'w').write(s.replace(sys.argv[2],sys.argv[3]))" "$d/src/acmp.c" "$old" "$new" || { echo "$name: plant did not apply"; return; }
  cmake -S "$d" -B "$d/b" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_C_COMPILER=gcc -DCMAKE_CXX_COMPILER=g++ > "$d/configure.log" 2>&1 &&
  cmake --build "$d/b" -j4 > "$d/build.log" 2>&1 &&
  ctest --test-dir "$d/b" -j4 --output-on-failure > "$d/ctest.log" 2>&1; rc=$?
  echo "$name: full ctest rc=$rc; $(grep -h 'tests passed' "$d/ctest.log")"; }
run review-transmit-word-off-by-one 'o->release[(release - 1u) / 32u] =' 'o->release[release / 32u] =' &
run review-owed-count-word-off-by-one 'change_owed + ((o->release[k / 32u]' 'change_owed + ((o->release[(k + 1u) / 32u]' &
run review-release-loop-word-off-by-one 'change_owed - ((o->release[k / 32u]' 'change_owed - ((o->release[(k + 1u) / 32u]' &
wait
run review-mask-not-cleared '	memset(o->release, 0, sizeof o->release);
' '' &
run review-mask-clears-one-word 'memset(o->release, 0, sizeof o->release);' 'memset(o->release, 0, sizeof o->release[0]);' &
run unplanted-control 'enum sent { SENT, OWED, LOST };' 'enum sent { SENT, OWED, LOST };' &
wait

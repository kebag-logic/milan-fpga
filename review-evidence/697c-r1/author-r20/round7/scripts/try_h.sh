#!/bin/bash
# What -H reports for forced includes and their own includes, with GCC and Clang (round 7 design probe).
set -u
W=$1
mkdir -p "$W/inc" "$W/sys"
cd "$W" || exit 1
printf '#include "h1.h"\n#include <stdbool.h>\nint a;\n' > a.c
printf '#include "h2.h"\n#define H1 1\n' > inc/h1.h
printf '#pragma once\n#define H2 2\n' > inc/h2.h
printf '#include "g.h"\nint x;\n' > f.h
printf '#define G 1\n' > g.h
printf '#define M 1\n' > m.h
printf '#pragma once\n#define bool _Bool\n' > sys/stdbool.h
for cc in gcc clang; do
  echo "== $cc: -include f.h -imacros m.h, -isystem sys"
  $cc -Iinc -isystem sys -include f.h -imacros m.h a.c -M -MF d.$cc -H; echo rc=$?; cat d.$cc
done
echo "== gcc -MG with a missing header"; printf '#include "nope.h"\n' > m.c; gcc m.c -M -MG -MF dm -H; echo rc=$?; cat dm
echo "== gcc missing header without -MG"; gcc m.c -M -MF dm2 -H; echo rc=$?; cat dm2
echo "== gcc #error"; printf '#include "h2.h"\n#error stop\n' > e.c; gcc -Iinc e.c -M -MF de -H; echo rc=$?; cat de

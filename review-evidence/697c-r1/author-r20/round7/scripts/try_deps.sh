#!/bin/bash
# How GCC answers a dependency pass added to a compile's own arguments (round 7 design probe).
set -u
W=$1
mkdir -p "$W/inc"
cd "$W" || exit 1
printf '#include "h1.h"\n#include <stdio.h>\nint a;\n' > a.c
printf '#include "h2.h"\nint b;\n' > b.c
printf '#include "h2.h"\n#define H1 1\n' > inc/h1.h
printf '#pragma once\n#define H2 2\n' > inc/h2.h
echo 'int x;' > f.h
echo "== 1 -c -o with -M -MF -H"; echo old > a.o; gcc -Iinc -c a.c -o a.o -M -MF d1 -H; echo rc=$?; cat d1; ls -la a.o; cat a.o
echo "== 2 multi with -M -MF, -o prog"; gcc -Iinc a.c b.c -o prog -M -MF d2 -H; echo rc=$?; cat d2
echo "== 3 multi with -M no -MF no -o"; gcc -Iinc a.c b.c -M -H; echo rc=$?
echo "== 4 existing -MMD -MF build.d + -M -MF ours"; gcc -Iinc -c a.c -o a2.o -MMD -MF build.d -MT a2.o -M -MF ours.d; echo rc=$?; echo ours:; cat ours.d; echo build:; cat build.d
echo "== 5 -include forced"; gcc -Iinc -include f.h -c a.c -o a3.o -M -MF d5 -H; cat d5
echo "== 6 two -o"; gcc -Iinc -c a.c -o a4.o -o /dev/null -M -MF d6; echo rc=$?; ls a4.o
echo "== 7 -MD on the real compile, multi-source, link"; gcc -Iinc a.c b.c -o prog7 -MD; echo rc=$?; ls *.d

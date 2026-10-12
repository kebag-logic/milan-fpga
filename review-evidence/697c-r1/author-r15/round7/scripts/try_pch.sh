#!/bin/bash
# Does a -M pass use a precompiled header read first, as the compile does? (round 7 design probe)
set -u
W=$1
mkdir -p "$W"
cd "$W" || exit 1
printf '#define CTRL_R6_PCH 1\n' > modes.h
gcc -x c-header modes.h -o modes.h.gch
printf '#error only the precompiled header defines the mode\n' > modes.h
printf '#ifdef CTRL_R6_PCH\n#include "reached.h"\n#endif\nint x;\n' > a.c
printf 'int reached;\n' > reached.h
echo "== compile"; gcc -include modes.h -c a.c -o a.o -H; echo rc=$?
echo "== -M pass"; gcc -include modes.h -c a.c -M -MF d -MT dependencies -H; echo rc=$?; cat d
echo "== -M pass with -Winvalid-pch"; gcc -include modes.h -Winvalid-pch -c a.c -M -MF d2 -MT dependencies -H; echo rc=$?; cat d2

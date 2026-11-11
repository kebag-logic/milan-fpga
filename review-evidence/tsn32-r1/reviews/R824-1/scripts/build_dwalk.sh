#!/bin/bash
# Build the reviewer's head-against-main differential probe. usage: build_dwalk.sh REPO HEAD MAIN OUT MAX_SINKS [SRC_OVERRIDE]
# SRC_OVERRIDE: an acmp.c to use for the head core instead of HEAD's (a planted copy).
set -eu
REPO=$1 HEAD=$2 MAIN=$3 O=$4 MAX=$5 OVR=${6:-}
D=$(cd "$(dirname "$0")" && pwd); S=$D/../scratch; . "$D/env.sh"
mkdir -p "$O"/{new/src,new/include,new/tests,old/src,old/include}
for p in src/acmp.c include/acmp.h include/wire.h tests/acmp_fake.hpp; do git -C "$REPO" show "$HEAD:$p" > "$O/new/$p"; done
for p in src/acmp.c include/acmp.h include/wire.h; do git -C "$REPO" show "$MAIN:$p" > "$O/old/$p"; done
[ -n "$OVR" ] && cp "$OVR" "$O/new/src/acmp.c"
R="$O/rename.h"; : > "$R"
for f in init rx adp_rx timer_expired tk_registered tk_kind_changed tk_unregistered set_started poll listener_registered \
         declaring restore_binding restore_rollback open binding_latch view change_pending rx_ready; do
  echo "#define acmp_$f old_acmp_$f" >> "$R"; done
F="-DACMP_MAX_SINKS=${MAX}u -fsanitize=shift,undefined,address -fno-sanitize-recover=all -g -O1"
gcc -std=c11 -Wall -Wextra $F -I"$O/old/include" -include "$R" -c "$O/old/src/acmp.c" -o "$O/old.o"
gcc -std=c11 -Wall -Wextra $F -I"$O/new/include" -c "$O/new/src/acmp.c" -o "$O/new.o"
g++ -std=c++17 $F -I"$O/new/include" -I"$O/new/tests" $(pkg-config --cflags gtest) -c "$D/dwalk.cpp" -o "$O/dwalk.o"
g++ $F "$O/dwalk.o" "$O/new.o" "$O/old.o" -o "$O/dwalk"
nm "$O/old.o" | grep -c " T old_acmp_" > "$O/old-symbols.count"

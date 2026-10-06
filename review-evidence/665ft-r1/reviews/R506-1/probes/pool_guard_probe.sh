#!/bin/sh
# Usage: pool_guard_probe.sh <repo checkout> <work dir>
# Builds the probe against the checkout's ctrl_pool.c twice: as shipped, and
# with the `&& bin->free_head != NULL` guard removed (a copy, never the
# checkout), and runs both. Prints gcov's view of line 115 for the shipped build.
set -u
REPO=$1; W=$2; HERE=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$W/ok" "$W/mut"
I="-I$REPO/sw/firmware/ctrl/port"
gcc -std=c11 -O0 --coverage $I -c "$REPO/sw/firmware/ctrl/port/ctrl_pool.c" -o "$W/ok/ctrl_pool.o" || exit 2
sed 's/ \&\& bin->free_head != NULL//' "$REPO/sw/firmware/ctrl/port/ctrl_pool.c" > "$W/mut/ctrl_pool.c"
grep -c 'free_head != NULL' "$W/mut/ctrl_pool.c"
gcc -std=c11 -O0 $I -c "$W/mut/ctrl_pool.c" -o "$W/mut/ctrl_pool.o" || exit 2
for v in ok mut; do
  g++ -std=c++20 -O0 $I -c "$HERE/pool_guard_probe.cpp" -o "$W/$v/probe.o" || exit 2
  g++ --coverage "$W/$v/probe.o" "$W/$v/ctrl_pool.o" -o "$W/$v/probe" -lgtest_main -lgtest -pthread || exit 2
  echo "== $v"; "$W/$v/probe"; echo "exit $?"
done
cd "$W/ok" && gcov -b -o . ctrl_pool.o >/dev/null 2>&1; grep -n -A3 'free_head != NULL' "$W/ok/ctrl_pool.c.gcov"

#!/bin/sh
# Usage: run_differential.sh BASE_TREE HEAD_TREE WORK   (checkouts of 69bac7c and e0b1449)
set -eu
here=$(cd "$(dirname "$0")" && pwd); base=$1; head=$2; work=$3; mkdir -p "$work"
for r in base head; do
  eval t=\$$r
  gcc -std=c11 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -shared -fPIC -Wl,-Bsymbolic -DNDEBUG -I"$t/include" "$t/src/adp.c" -o "$work/$r.so"
done
g++ -std=c++20 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -I"$head/include" "$here/differential.cpp" -ldl -o "$work/diffprobe"
"$work/diffprobe" "$work/base.so" "$work/head.so"

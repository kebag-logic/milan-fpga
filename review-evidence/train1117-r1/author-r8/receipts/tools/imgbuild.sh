#!/bin/bash
# imgbuild.sh CLONE OUT: the CPU budget harness's build (legs.py build, as run.py builds by default) of every arm at
# each point into OUT/<point>/<arm>, in parallel, for the images' hashes; then each ctrl_app.elf's sha256.
set -u
T=<scratch>; . $T/bin/env.sh
export MAKEFLAGS="-j4 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 O=$2
for P in 1x1 8x8-1if 8x8; do for V in none answering-every-port answering-ports valid-destinations; do
  mkdir -p $O/$P; python3 -B $T/tools/legs.py build $C $O/$P/$V $P $V 1 > $O/$P/$V.log 2>&1 &
done; done; wait
for P in 1x1 8x8-1if 8x8; do for V in none answering-every-port answering-ports valid-destinations; do
  echo "$P $V $(sha256sum $O/$P/$V/image/ctrl_app.elf 2>/dev/null | cut -c1-64)"
done; done > $O/hashes.txt
cat $O/hashes.txt

#!/bin/bash
# hbuild.sh CLONE OUT POINT: the CPU budget harness's build of every arm at POINT (legs.py build, as run.py builds by
# default) into OUT/<point>/<arm>, in parallel, each split into the train's part count for that arm (its parts.json),
# so the groups partition as the measured run's did; then each arm's ctrl_app.elf sha256.
set -u
S=<scratch>; . $S/bin/fwenv.sh
export MAKEFLAGS="-j3 --no-print-directory" PYTHONUNBUFFERED=1
C=$1 O=$2 P=$3
declare -A N=([none]=22 [answering-every-port]=6 [answering-ports]=22 [answering-later]=3 [declaring-outputs]=4 [shutdown-entry]=2 [talker-notices]=2 [valid-destinations]=3)
mkdir -p $O/$P
for V in "${!N[@]}"; do python3 -B $S/tools/legs.py build $C $O/$P/$V $P $V ${N[$V]} > $O/$P/$V.build.log 2>&1 & done; wait
for V in "${!N[@]}"; do echo "$P $V $(sha256sum $O/$P/$V/image/ctrl_app.elf 2>/dev/null | cut -c1-64) $(tail -1 $O/$P/$V.build.log | cut -c1-80)"; done | sort > $O/$P/hashes.txt
cat $O/$P/hashes.txt

#!/bin/bash
# mapbuild_full.sh CLONE OUT: the optimisation line's mapbuild.sh (opt-a808 tools/hot) over every arm at this head
# (variant none and each build.VARIANTS entry) and both images, without gPTP and with it (GPTP=1): the harness's build
# at each of its three points, as run.py builds by default, for the link maps the hot-list filter reads (each image as
# itself and as the SoC plan's stand-in and mapped images). Three builds at a time.
set -u
T=<scratch>; . $T/bin/env.sh
export HOME=$T/home MAKEFLAGS="-j2 --no-print-directory" PYTHONUNBUFFERED=1
C=$1; M=$2; mkdir -p $M
V="none $(cd $C/tb/verilator/ctrl_service_budget && python3 -B -c 'import build; print(" ".join(build.VARIANTS))')"
for G in 0 1; do for P in 1x1 8x8-1if 8x8; do for v in $V; do echo "$G $P $v"; done; done; done | \
  xargs -P 3 -L 1 bash -c 'G=$0; P=$1; v=$2; n=$P-$v-$([ $G = 1 ] && echo gptp || echo plain); GPTP=$G python3 -B '$T'/bin/legs_gptp.py build '$C' '$M'/$n $P $v 1 > '$M'/$n.log 2>&1; echo "$n rc=$? maps $(find '$M'/$n -name ctrl_app.map | wc -l)"'
echo "END $(date +%T)"

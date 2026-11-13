#!/bin/sh
# usage: run_arm.sh <clone> <out-prefix> <ccache-dir> <jobs> [OBJCACHE-mode]
# Runs <clone>'s engine mutation arm (python3 mutants.py --jobs <jobs>) from
# its engine directory, with the pinned Verilator first on PATH, CCACHE_DIR
# set to <ccache-dir> and TMPDIR under the packet's scratch. OBJCACHE is left
# unset (the arm's own default: ccache when on PATH) unless the fifth
# argument is "off", which sets OBJCACHE= (empty). Writes <out-prefix>.stdout,
# .stderr, .rc, .wall and .ccache-stats (ccache --print-stats afterwards).
set -u
clone=$1 out=$2 cdir=$3 jobs=$4 mode=${5:-default}
packet=$REVIEWS/gptp104-r839-1-packet
PATH=$packet/scratch/bin:$PATH
TMPDIR=$packet/scratch/tmp
CCACHE_DIR=$cdir
export PATH TMPDIR CCACHE_DIR
unset OBJCACHE CCACHE_BASEDIR CCACHE_NOHASHDIR
[ "$mode" = off ] && { OBJCACHE=; export OBJCACHE; }
ccache --zero-stats >/dev/null 2>&1
start=$(date +%s.%N)
( cd "$clone/tb/verilator/engine" && python3 mutants.py --jobs "$jobs" ) \
  >"$out.stdout" 2>"$out.stderr"
rc=$?
end=$(date +%s.%N)
echo "$rc" >"$out.rc"
echo "start $start end $end" >"$out.wall"
ccache --print-stats >"$out.ccache-stats" 2>&1
exit "$rc"

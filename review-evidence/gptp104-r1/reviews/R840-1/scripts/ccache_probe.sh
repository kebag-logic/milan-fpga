#!/bin/sh
# ccache behaviour of the engine arm's build(): cold, warm in a new temporary
# directory, warm from a checkout at another path, OBJCACHE= off, ccache
# absent from PATH, an unwritable cache, and the base for comparison.
. $REVIEWS/gptp104-r840-1-packet/scripts/env.sh
pb=$P/scripts/probe_build.py
H=$S/trees/head; B=$S/trees/base; M=$S/trees/head-moved-elsewhere
rm -rf $M; cp -a $H $M
W=$S/ccwork; rm -rf $W; mkdir -p $W
stats() { ccache --print-stats | awk -F'\t' '$1 ~ /^(direct_cache_hit|preprocessed_cache_hit|cache_miss|files_in_cache)$/ {printf "%s=%s ", $1, $2} END {print ""}'; }
step() { echo "== $1"; }
export CCACHE_DIR=$S/cc/probeA; rm -rf $CCACHE_DIR; mkdir -p $CCACHE_DIR
step "1 head cold, ccache on PATH, OBJCACHE unset"; python3 $pb $H $W/w1; ccache -z >/dev/null; stats_cold=1
ccache --print-stats >/dev/null
step "2 head warm, new temporary directory"; python3 $pb $H $W/w2; stats; ccache -z >/dev/null
step "3 head warm, a third temporary directory"; python3 $pb $H $W/w3; stats; ccache -z >/dev/null
step "4 checkout at another path, warm cache"; python3 $pb $M $W/w4; stats; ccache -z >/dev/null
step "5 same other path again"; python3 $pb $M $W/w5; stats; ccache -z >/dev/null
export CCACHE_DIR=$S/cc/probeOff; rm -rf $CCACHE_DIR; mkdir -p $CCACHE_DIR
step "6 OBJCACHE= (off), empty cache dir"; OBJCACHE= python3 $pb $H $W/w6; echo "files in cache dir: $(find $CCACHE_DIR -type f | wc -l)"
step "7 compiler_env with ccache absent from PATH"; mkdir -p $S/noccbin; PATH=$S/noccbin /usr/bin/python3 $pb $H $W/w7 --env
step "7b compiler_env defaults with ccache on PATH"; python3 $pb $H $W/w7 --env
step "7c caller's own settings win"; OBJCACHE=mycache CCACHE_NOHASHDIR=0 python3 $pb $H $W/w7 --env
mkdir -p $S/cc/readonly; chmod 555 $S/cc/readonly
step "8 unwritable cache dir (mode 555), OBJCACHE unset"; CCACHE_DIR=$S/cc/readonly python3 $pb $H $W/w8; echo "rc=$?"
step "8b uncreatable cache dir"; CCACHE_DIR=/proc/r840-no-such/cc python3 $pb $H $W/w8b; echo "rc=$?"
step "8c unwritable cache dir with OBJCACHE= (documented remedy)"; CCACHE_DIR=$S/cc/readonly OBJCACHE= python3 $pb $H $W/w8c; echo "rc=$?"
chmod 755 $S/cc/readonly
export CCACHE_DIR=$S/cc/probeBase; rm -rf $CCACHE_DIR; mkdir -p $CCACHE_DIR
step "9 base a64be73d, OBJCACHE=ccache forced, cold"; OBJCACHE=ccache CCACHE_NOHASHDIR=1 python3 $pb $B $W/w9; ccache -z >/dev/null
step "10 base a64be73d, warm, new temporary directory"; OBJCACHE=ccache CCACHE_NOHASHDIR=1 python3 $pb $B $W/w10; stats

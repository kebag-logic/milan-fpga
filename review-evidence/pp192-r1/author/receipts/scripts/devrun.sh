#!/usr/bin/env bash
# usage: devrun.sh <dev-root> <tag> <run-args...>   rebuild (incremental) and run the default bench
D="$1"; tag="$2"; shift 2
export PATH=<scratch>/bin:$PATH TMPDIR=<scratch>/tmpdir
cd "$D/tb/pp_top" || exit 1
s=$(date +%s); make gsi-build VERILATOR=verilator > "$D/$tag-build.log" 2>&1; echo "build rc=$? secs=$(( $(date +%s) - s ))" > "$D/$tag-build.rc"
s=$(date +%s); ./obj_dir/Vpp_top_sim "$@" > "$D/$tag-run.log" 2>&1; echo "run rc=$? secs=$(( $(date +%s) - s ))" > "$D/$tag-run.rc"

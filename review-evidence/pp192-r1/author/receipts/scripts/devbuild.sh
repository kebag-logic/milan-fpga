#!/usr/bin/env bash
# usage: devbuild.sh <dev-root> <tag> <run-args...>   build the pp_top default bench in a scratch copy and run it
D="$1"; tag="$2"; shift 2
export PATH=<scratch>/bin:$PATH TMPDIR=<scratch>/tmpdir
cd "$D/tb/pp_top" || exit 1
s=$(date +%s)
make gsi-build VERILATOR=verilator > "$D/$tag-build.log" 2>&1; echo "build rc=$? secs=$(( $(date +%s) - s ))" > "$D/$tag-build.rc"
s=$(date +%s)
./obj_dir/Vpp_top_sim "$@" > "$D/$tag-run.log" 2>&1; echo "run rc=$? secs=$(( $(date +%s) - s ))" > "$D/$tag-run.rc"

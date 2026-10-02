#!/bin/bash
# launch.sh NAME WORKDIR CMD... : run CMD detached in WORKDIR with the pinned
# toolchain first on PATH; log to receipts/campaigns/NAME.log, exit code to
# NAME.rc, wall seconds to NAME.time. Poll the .rc file to wait.
P=$REVIEWS/pp141-r431-2-packet
name=$1; wd=$2; shift 2
out=$P/receipts/campaigns; mkdir -p "$out" "$P/scratch/tmp/$name"
rm -f "$out/$name.rc" "$out/$name.log" "$out/$name.time"
( cd "$wd" && export PATH="$P/scratch/bin:$PATH" TMPDIR="$P/scratch/tmp/$name" VL_J="${VL_J:-2}";
  s=$(date +%s); "$@" > "$out/$name.log" 2>&1; rc=$?; e=$(date +%s)
  echo $((e-s)) > "$out/$name.time"; echo $rc > "$out/$name.rc" ) </dev/null >/dev/null 2>&1 &
disown
echo "launched $name"

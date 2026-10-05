#!/bin/sh
# Red/green of tb/aecp_notify section DR. Usage: bench_red_green.sh REPO SCRATCH OUT VERILATOR
# head:     git archive of the head
# red-main: the head tree with hdl/aecp/KL_aecp_notify.sv taken from main 054d01c7
# red-5343: git archive of 5343cd7 (the red-first commit: DR bench on main's RTL)
set -u
REPO=$1 S=$2 OUT=$3 V=$4
HEAD=79571006b803a4ab4af65358f0d87bc3af73180e MAIN=054d01c79e59c3f80454ad9cdefd8e914b540bb4
mkdir -p "$S" "$OUT"
for t in head red-main red-5343; do rm -rf "$S/$t"; mkdir -p "$S/$t"; done
git -C "$REPO" archive $HEAD | tar -x -C "$S/head"
git -C "$REPO" archive $HEAD | tar -x -C "$S/red-main"
git -C "$REPO" show $MAIN:hdl/aecp/KL_aecp_notify.sv > "$S/red-main/hdl/aecp/KL_aecp_notify.sv"
git -C "$REPO" archive 5343cd7 | tar -x -C "$S/red-5343"
for t in head red-main red-5343; do
  ( make -C "$S/$t/tb/aecp_notify" run VERILATOR="$V" > "$OUT/aecp_notify-$t.log" 2>&1; echo $? > "$OUT/aecp_notify-$t.rc" ) &
done
wait
for t in head red-main red-5343; do echo "$t rc=$(cat $OUT/aecp_notify-$t.rc)"; grep -E '^FAIL|\[i\] DR|checks' "$OUT/aecp_notify-$t.log"; done

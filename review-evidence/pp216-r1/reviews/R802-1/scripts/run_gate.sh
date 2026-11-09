#!/usr/bin/env bash
# run_gate.sh NAME WORKTREE CMD...  -> receipts/NAME.{cmd,log,rc,start,end}
# Puts the pinned Verilator 5.050 first on PATH. Portable: PKT and VPIN may be overridden.
PKT=${PKT:-$(cd "$(dirname "$0")/.." && pwd)}
VPIN=${VPIN:-$VALIDATION_TOOLS/pinned-verilator-5.050}
name=$1; wt=$2; shift 2
r=$PKT/receipts/$name
printf '%q ' "$@" > "$r.cmd"; echo >> "$r.cmd"
echo "cwd=$wt head=$(git -C "$wt" rev-parse HEAD) verilator=$(PATH=$VPIN:$PATH verilator --version)" >> "$r.cmd"
date -u +%FT%TZ > "$r.start"
( cd "$wt" && PATH=$VPIN:$PATH "$@" ) > "$r.log" 2>&1
echo $? > "$r.rc"
date -u +%FT%TZ > "$r.end"

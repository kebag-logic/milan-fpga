#!/bin/bash
# Copy round-1c logs into receipts/round1c with host paths replaced (collect.py).
R=<scratch>/round1c
C="<scratch>/venv/bin/python3 -I <scratch>/collect.py"
put() { for f in "$@"; do $C "$f" "round1c/$DEST/$(basename "$f")" > /dev/null; done; }
DEST=merge-7f84892a; put $R/merge-dp/*
DEST=lane-tree-75db4b57; put $R/fix-dp/*
DEST=dp762-mutants; put $R/dp762/*
for d in static builder yosys xvlog tsnfuzz unb; do [ -d $R/$d ] && { DEST=$d; put $R/$d/*; }; done
for d in sweep-s0 sweep-s1; do
  [ -d $R/$d ] || continue
  DEST=$d; put $R/$d/*.log $R/$d/*.txt
  DEST=$d/preflight; put $(ls $R/$d/preflight/* | grep -v check_merge_containment)
  $C $R/$d.out round1c/$d/runner.out > /dev/null
done
for a in $R/attempts/*; do DEST=attempts/$(basename $a); put $(find $a -maxdepth 1 -type f); done
DEST=scripts; put $R/scripts/* <scratch>/collect.py <scratch>/gen_index.py
echo collected

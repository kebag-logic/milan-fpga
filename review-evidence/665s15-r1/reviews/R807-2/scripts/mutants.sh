#!/bin/bash
# Usage: mutants.sh <probe-tree> <receipt-dir>: applies each mutant to a copy of the head tree, runs the
# generator's --check --crosscheck, the 32x32 --variant-shape build and --selftest, records rc, restores.
T=$1; R=$2; mkdir -p "$R"; cd "$T" || exit 2
mut() { # name file old new
  n=$1 f=$2 old=$3 new=$4
  cp "$f" "$f.orig"
  python3 - "$f" "$old" "$new" <<'PY' || { echo "$n: plant did not apply" >> "$R/summary.txt"; mv "$f.orig" "$f"; return; }
import sys; p, old, new = sys.argv[1:]; s = open(p).read()
assert s.count(old) == 1, s.count(old); open(p, "w").write(s.replace(old, new))
PY
  python3 -B sw/mailbox/gen_mailbox.py --check --crosscheck > "$R/$n.check.log" 2>&1; c=$?
  rm -rf "$R/$n.v32"; python3 -B sw/mailbox/gen_mailbox.py --variant-interfaces 2 \
     --variant-shape configs/endstation_ax7101_32x32.yaml --out "$R/$n.v32" > "$R/$n.variant.log" 2>&1; v=$?
  python3 -B sw/mailbox/gen_mailbox.py --selftest > "$R/$n.selftest.log" 2>&1; s=$?
  echo "$n: check rc $c, variant rc $v, selftest rc $s; selftest FAIL arms: $(grep -c '^\[FAIL\]' "$R/$n.selftest.log")" >> "$R/summary.txt"
  rm -rf "$R/$n.v32"; mv "$f.orig" "$f"
}
: > "$R/summary.txt"
mut M0-none sw/mailbox/gen_mailbox.py 'import os' 'import os'
mut MA-fix-reverted sw/mailbox/mailbox_skeleton.py 'if end == contract.window_bytes:' 'if False:'
mut MB-unbounded-everywhere sw/mailbox/mailbox_skeleton.py 'if end == contract.window_bytes:' 'if True:'
mut MC-ring-not-resized sw/mailbox/gen_mailbox.py 'return max(acmp.tx_words, 1 << max(0, need - 1).bit_length())' 'return acmp.tx_words'
mut MD-crosscheck-no-wrap sw/mailbox/gen_mailbox.py 'upper = (base + 4 * words) % width if decodes[name][2] else None' 'upper = (base + 4 * words) if decodes[name][2] else None'
mut ME-ring-short-by-one sw/mailbox/gen_mailbox.py 'need = sinks * (len(contract.tx_header) + (ACMP_FRAME_BYTES + 3) // 4)' 'need = (sinks - 1) * (len(contract.tx_header) + (ACMP_FRAME_BYTES + 3) // 4)'

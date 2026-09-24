#!/usr/bin/env bash
# hold_probe.sh PROOF OUTDIR REPEATS HOLD: run PROOF --selftest REPEATS times per mode
# (uid1000, uid0) inside sandbox.sh with FAKE_HOLD=HOLD in the environment, which the
# stand-in runner reads as its fixed hold (default 3 s). Shows which cases, if any,
# depend on that hold. The proof's bytes are not changed; only the environment is.
# Prints one line per run: mode rep rc failing-cases.
set -euo pipefail
here=$(cd "$(dirname "$0")" && pwd)
proof=$1 outdir=$2 repeats=$3 hold=$4
mkdir -p "$outdir/tmp"
for mode in uid1000 uid0; do
  for rep in $(seq 1 "$repeats"); do
    rc=0
    FAKE_HOLD=$hold TMPDIR=$outdir/tmp "$here/sandbox.sh" "$mode" bash "$proof" --selftest \
      >"$outdir/$mode.$rep.txt" 2>&1 || rc=$?
    failed=$(sed -n 's/^  FAIL \([^:]*\):.*/\1/p' "$outdir/$mode.$rep.txt" | paste -sd';' -)
    printf 'FAKE_HOLD=%s mode=%s rep=%s rc=%s | failing cases: %s\n' "$hold" "$mode" "$rep" "$rc" \
      "${failed:-none}"
  done
done

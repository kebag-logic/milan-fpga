#!/bin/sh
# Rerun the prior rounds' probes against the head.
#  - capacity_probe.sh (round-1 external reviewer), byte-identical, unmodified.
#  - debt_probe.py (round-1 internal reviewer): first unmodified, then with the
#    single adaptation the head's run.build() signature needs (a capacity line;
#    run.EXTRA, the round-1 128 geometry, so the probe's semantics are unchanged).
set -u; . "$(dirname "$0")/env.sh"
P="$SCRATCH/prior"; extract "$P/export"
rm -rf "$P/cap-out"
sh "$P/capacity_probe.sh" "$SRC" "$P/cap-out" "$VERILATOR" "$SCRATCH/images/1x1.img.bin" "$SCRATCH/images/8x8.img.bin" > "$RCPT/prior-capacity-probe.log" 2>&1
echo $? > "$RCPT/prior-capacity-probe.rc"
rm -rf "$P/debt-unmod"
python3 "$P/debt_probe.py" --root "$P/export" --output "$P/debt-unmod" --verilator "$VERILATOR" > "$RCPT/prior-debt-probe-unmodified.log" 2>&1
echo $? > "$RCPT/prior-debt-probe-unmodified.rc"
sed 's/binary = harness.build(tree, work, args.verilator)/binary = harness.build(tree, work, args.verilator, harness.EXTRA)/' "$P/debt_probe.py" > "$P/debt_probe_adapted.py"
diff "$P/debt_probe.py" "$P/debt_probe_adapted.py" > "$RCPT/prior-debt-probe-adaptation.diff"
rm -rf "$P/debt-adapted"
python3 "$P/debt_probe_adapted.py" --root "$P/export" --output "$P/debt-adapted" --verilator "$VERILATOR" > "$RCPT/prior-debt-probe-adapted.log" 2>&1
echo $? > "$RCPT/prior-debt-probe-adapted.rc"

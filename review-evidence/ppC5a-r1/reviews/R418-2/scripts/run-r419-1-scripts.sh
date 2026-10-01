#!/usr/bin/env bash
# Re-run the other reviewer's published round-1 scripts (read-only copies, sha256 checked against
# the evidence manifest) at the exact head, on scratch exports only.
# Usage: run-r419-1-scripts.sh <clone> <head-sha> <packet-dir> <dir holding the two scripts>
set -u
CLONE=$1; HEAD=$2; PKT=$3; SRC=$4
export PATH="$PKT/scratch/bin:$PATH" TMPDIR="$PKT/scratch/tmp"
mkdir -p "$TMPDIR" "$PKT/receipts"
sha256sum "$SRC/probe_hz_reachability.py" "$SRC/reviewer_mutants.py"
# the probe, with only its anchor moved from the HZ8 call to the HZ12 call (the run list grew)
EXP=$PKT/scratch/r419-probe; rm -rf "$EXP"; mkdir -p "$EXP"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP"
sed -i 's/--build -j 0/--build -j 8/' "$EXP/tb/pp_top/Makefile" "$EXP/tb/ucpu/Makefile"
sed 's/ANCHOR = "    hz8_the_other_classes_run_beside_a_stream_step();/ANCHOR = "    hz12_a_stream_named_by_another_class_conflicts_with_its_read();/; s/"    hz8_the_other_classes_run_beside_a_stream_step();\\n"$/"    hz12_a_stream_named_by_another_class_conflicts_with_its_read();\\n"/' \
  "$SRC/probe_hz_reachability.py" > "$PKT/scratch/probe_hz_reachability.anchored.py"
diff "$SRC/probe_hz_reachability.py" "$PKT/scratch/probe_hz_reachability.anchored.py"
python3 "$PKT/scratch/probe_hz_reachability.anchored.py" "$EXP" "$(command -v verilator)" > "$PKT/receipts/33-r419-1-probe-at-head.log" 2>&1
echo "probe rc=$?"
# the mutant script, unchanged, on a fresh export
EXP2=$PKT/scratch/r419-mut-src; rm -rf "$EXP2"; mkdir -p "$EXP2"
git -C "$CLONE" archive "$HEAD" | tar -x -C "$EXP2"
sed -i 's/--build -j 0/--build -j 8/' "$EXP2/tb/pp_top/Makefile" "$EXP2/tb/ucpu/Makefile"
python3 "$SRC/reviewer_mutants.py" "$EXP2" "$PKT/scratch/r419-mut-logs" > "$PKT/receipts/24-r419-1-mutants-at-head.log" 2>&1
echo "mutants rc=$?"

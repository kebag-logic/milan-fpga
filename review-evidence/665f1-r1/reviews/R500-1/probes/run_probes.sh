#!/bin/sh
# R500-1: reproduce every reviewer probe. Run from a checkout of the exact head
# 215c3c0be5d8db6d9a1ba5aca3827dfe969c042e (submodules initialised, PyYAML
# installed). Disposable trees and builds go under the packet's scratch/.
# Usage: sh /path/to/packet/probes/run_probes.sh
set -eu
here=$(cd "$(dirname "$0")" && pwd)
out="$here/../receipts"
export R500_CLONE="$PWD" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$out" "$here/../scratch/tmp"
export TMPDIR="$here/../scratch/tmp"
python3 "$here/probe_time_step.py" > "$out/probe_time_step_1x1.txt"
python3 "$here/probe_dr2c.py" > "$out/probe_dr2c_1x1.txt"
python3 "$here/probe_dr2a_rearm.py" > "$out/probe_dr2a_rearm_1x1.txt"
python3 "$here/probe_verify_tail.py" > "$out/probe_verify_tail_1x1.txt"
python3 "$here/probe_parity_fuzz.py" endstation_ax7101_1x1_tdm8 2000 12 > "$out/probe_parity_fuzz_1x1.txt"
python3 "$here/probe_parity_fuzz.py" endstation_ax7101_8x8 1500 10 > "$out/probe_parity_fuzz_8x8.txt"
for m in control_no_verify verify_skips_last_stretch blankcheck_first_stretch_only \
         tie_picks_b time_not_held fail_not_stale program_refusal_ignored; do
	python3 "$here/probe_mutants.py" "$m" > "$out/mutant_$m.txt"
done

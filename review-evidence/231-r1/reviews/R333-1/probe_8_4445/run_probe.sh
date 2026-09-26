#!/usr/bin/env bash
# Reproduce: VIVADO_BIN=<vivado bin dir> bash run_probe.sh
set -u
cd "$(dirname "$0")"
for arm in control promoted; do
  "${VIVADO_BIN:-}${VIVADO_BIN:+/}vivado" -mode batch -nojournal -log "probe_$arm.log" \
    -source probe.tcl -tclargs "$arm" > "stdout_$arm.txt" 2>&1
  echo "arm=$arm rc=$?" | tee -a probe_results.txt
  grep -c 'Synth 8-4445' "probe_$arm.log" | sed "s/^/arm=$arm synth_8_4445_lines=/" | tee -a probe_results.txt
done

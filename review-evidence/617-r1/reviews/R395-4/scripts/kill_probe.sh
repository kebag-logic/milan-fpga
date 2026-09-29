#!/usr/bin/env bash
# The sweep's kill, as scripts/run_all_suites.sh applies it (timeout(1) on
# `make -C <suite>`), landing mid-arm while parallel builds and harness runs are
# in flight: afterwards no arm process of THIS run (its TMPDIR) may survive and no arm temp dir may remain.
# Usage: kill_probe.sh <repo> <seconds>   (env.sh sourced; TMPDIR in scratch)
set -u
R=$1; S=$2
before=$(ls -d "$TMPDIR"/capture-coherence-mutants-* 2>/dev/null | wc -l)
timeout "$S" taskset -c 0-7 make -C "$R/tb/verilator/capture_coherence" mutants > "$TMPDIR/../kill_probe_arm.log" 2>&1
echo "timeout rc=$? (124 = the guard fired)"
for i in 1 2 3 4 5 6; do
  n=$(pgrep -fc "$TMPDIR/capture-coherence-mutants-|$R/tb/verilator/capture_coherence/mutants.py|python3 mutants.py" || true)
  [ "$n" = 0 ] && break; timeout 2 tail -f /dev/null
done
echo "arm processes alive after the kill: $(pgrep -fc "$TMPDIR/capture-coherence-mutants-|python3 mutants.py" || true)"
pgrep -fa "$TMPDIR/capture-coherence-mutants-|python3 mutants.py" | cut -c1-160
echo "arm temp dirs before: $before  after: $(ls -d "$TMPDIR"/capture-coherence-mutants-* 2>/dev/null | wc -l)"
echo "arm log at the kill (last lines):"; tail -4 "$TMPDIR/../kill_probe_arm.log" | cut -c1-200

#!/usr/bin/env bash
# The make 4.3 chain at the head: `make -C tb/verilator/capture_coherence <target>`
# (no -s, as scripts/run_all_suites.sh runs it), GNU make 4.3 first on PATH,
# pinned Verilator 5.050 with "-j 0" capped to JCAP, under taskset CPUS.
# Records untracked/ignored files in the four suite dirs before and after.
# Usage: make43_chain.sh <repo> <target> <cpus e.g. 0-7> <jcap> <log>
set -u
R=$1; T=$2; C=$3; J=$4; L=$5
P=${P:-$REVIEWS/617-r395-4-packet}
. "$P/scripts/env.sh"; export JCAP=$J
snap() { git -C "$R" status --short --ignored --untracked-files=all tb/verilator/capture_coherence tb/verilator/chmap_capture tb/verilator/media_nco tb/verilator/milan_dp 2>/dev/null; }
{
  echo "# make 4.3 chain at $(git -C "$R" rev-parse HEAD): make -C tb/verilator/capture_coherence $T; $(make --version | head -1); $(verilator --version); taskset -c $C; Verilator -j 0 capped to $J"
  echo "## untracked/ignored before:"; snap
  echo "## run:"
  s=$(date +%s.%N)
  taskset -c "$C" make -C "$R/tb/verilator/capture_coherence" "$T"
  rc=$?
  e=$(date +%s.%N)
  echo "rc=$rc"
  python3 -c "print(f'wall {$e-$s:.1f} s on a shared host (load avg at end $(cut -d' ' -f1 /proc/loadavg))')"
  echo "## untracked/ignored after:"; snap
  echo "## leftover arm temp dirs: $(ls -d "$TMPDIR"/capture-coherence-mutants-* 2>/dev/null | wc -l)"
} > "$L" 2>&1

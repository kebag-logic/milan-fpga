#!/bin/sh
# R394-4: the arm's kill path under the chain the sweep uses (`timeout T make -C <suite> mutants`):
# timeout signals its process group (make and the driver), and make forwards SIGTERM to its recipe.
# After the kill: the driver's exit, any temp dir it left in TMPDIR, and any surviving process.
#   sh r394_killpath.sh <suite-dir> <seconds> <cpus>
set -u
suite=$1; t=$2; cpus=$3
echo "## make: $(make --version | head -1); timeout $t s; taskset -c $cpus; TMPDIR=$TMPDIR"
before=$(ls "$TMPDIR" | sort)
env -u MAKEFLAGS -u MAKELEVEL timeout "$t" taskset -c "$cpus" make -C "$suite" mutants > "$TMPDIR/../killpath.out" 2>&1
echo "timeout rc=$?"
sleep 5
grep -E 'SystemExit|OSError|Traceback|Error [0-9]|^\[i\]' "$TMPDIR/../killpath.out" | head -12
echo "## SystemExit count: $(grep -c '^SystemExit' "$TMPDIR/../killpath.out")"
echo "## temp entries left in TMPDIR:"
for e in $(ls "$TMPDIR" | sort); do echo "$before" | grep -qx "$e" || { echo "  $e $(du -sh "$TMPDIR/$e" | cut -f1)"; ls -R "$TMPDIR/$e" 2>/dev/null | head -8 | sed 's/^/    /'; }; done
echo "## surviving processes under the suite path: $(ps -eo args | grep -F "$suite" | grep -v -e grep -e r394_killpath | wc -l)"
ps -eo pid,args | grep -E 'Vcoherence|Vchmap|Vmedia_nco|capture-coherence-mutants' | grep -v grep | head -5

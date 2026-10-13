#!/usr/bin/env bash
# R632-5: re-run the earlier rounds' unchanged mutation drivers and probes at the
# exact head, concurrently, each inside scripts/sandbox.sh (no network, no
# Docker socket, read-only system). Usage: run_campaigns.sh PACKET MODE
# PACKET/scratch/pristine must hold `git archive` of the exact head.
# MODE is "probes" or "mutants"; the two are run one after the other.
set -uo pipefail
packet=$(realpath "$1")
mode=$2
cd "$packet"
mkdir -p receipts scratch/probe scratch/tmp
run() {  # name, then command; log and rc land in receipts/
  local name=$1; shift
  ( "$@" > "receipts/$name.log" 2>&1; echo $? > "receipts/$name.rc" ) &
}
copy() {  # a real (not hard-linked) copy of the pristine tree for one probe
  local tree=scratch/probe/$1
  rm -rf "$tree"; cp -r scratch/pristine "$tree"; cp "scripts/$2" "$tree/.probe.py"; echo "$tree"
}
if [ "$mode" = mutants ]; then
  run mutants_r2-at-head python3 -I scripts/mutants_r2.py "$packet" scratch/pristine --jobs 8
  run mutants_r3-at-head python3 -I scripts/mutants_r3.py "$packet" scratch/pristine --jobs 8
  wait; cat receipts/mutants_r*-at-head.rc; exit 0
fi
t=$(copy cleanup_entry probe_cleanup_entry.py)
run probe_cleanup_entry-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy shutdown probe_shutdown.py)
run probe_shutdown-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy r3 probe_r3.py)
run probe_r3-at-head scripts/sandbox.sh "$t" python3 -I .probe.py . 300
t=$(copy r2 probe_r2.py)
run probe_r2-at-head scripts/sandbox.sh "$t" python3 -I .probe.py . 400
t=$(copy r6331 r633-1-probe_cpu_ranges.py)
run r633-1-probe_cpu_ranges-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy r6331a r632-2-r633-1-probe-adapted.py)
run r632-2-r633-1-probe-adapted-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy compat r633-2-probe_cpu_ranges_compat.py)
run r633-2-probe_cpu_ranges_compat-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy lifecycle r633-2-probe_lifecycle.py)
run r633-2-probe_lifecycle-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
t=$(copy monitor r633-2-probe_monitor.py)
run r633-2-probe_monitor-at-head scripts/sandbox.sh "$t" python3 -I .probe.py .
wait
for rc in receipts/*.rc; do printf '%s %s\n' "$(cat "$rc")" "$rc"; done

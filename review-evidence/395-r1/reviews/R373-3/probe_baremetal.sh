#!/bin/bash
# Planted-fault probe for scripts/check_baremetal_only.py --check over every
# file this PR changes. Usage: probe_baremetal.sh <disposable clone at head>
# Control: unmodified clone must pass. Faults: (a) the round-2 wording
# restored at its line; (b) a '/sys' path component appended to each changed
# file. Each fault must make --check exit non-zero. The clone is reset after
# every arm.
set -u
C="$1"; cd "$C" || exit 2
run() { python3 -B scripts/check_baremetal_only.py --check >/tmp/bm.$$ 2>&1; echo $?; }
echo "control rc=$(run)"
sed -i 's#^Ethernet-to-system crossings remain#Ethernet/sys crossings remain#' docs/findings/COMMERCIAL_TIMING_395.md
grep -c '^Ethernet/sys crossings remain' docs/findings/COMMERCIAL_TIMING_395.md | sed 's/^/restored-lines=/'
rc=$(run); echo "fault restore-r2-wording rc=$rc"; grep -m2 COMMERCIAL /tmp/bm.$$
git checkout -q -- .
for f in $(git diff --name-only 8bc97021f28fb7f729418d3a00851c84ea0b50fd HEAD); do
  case "$f" in *.py) printf '\n# planted Ethernet/sys crossings\n' >> "$f";;
               *.tcl) printf '\n# planted Ethernet/sys crossings\n' >> "$f";;
               *) printf '\nplanted Ethernet/sys crossings\n' >> "$f";; esac
  rc=$(run); echo "fault plant-in $f rc=$rc"
  git checkout -q -- .
done
echo "final-status: $(git status --porcelain | wc -l) dirty"
echo "head: $(git rev-parse HEAD)"
rm -f /tmp/bm.$$

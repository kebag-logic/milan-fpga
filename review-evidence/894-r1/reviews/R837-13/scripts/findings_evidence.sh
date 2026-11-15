#!/bin/sh
# Print the exact head lines each R837-13 finding cites, beside the head's grader or model figure.
# Usage: findings_evidence.sh <clean-clone-at-head>
set -eu
C=$1; D=$C/docs/design/SPLIT_CONTROL_MEMORY.md; F=$C/docs/reference/FR_NFR.md; T=$C/tb/verilator/ctrl_service_budget
line() { printf '%s:%s: %s\n' "$2" "$1" "$(sed -n "$1p" "$3")"; }
echo "# head: $(git -C "$C" rev-parse HEAD)"
echo "## F1: the retired search's verdict"
line 2194 SPLIT_CONTROL_MEMORY.md "$D"; line 2200 SPLIT_CONTROL_MEMORY.md "$D"
line 390 FR_NFR.md "$F"; line 392 FR_NFR.md "$F"; line 393 FR_NFR.md "$F"
sed -n '21,27p' "$C/sw/firmware/ctrl/aecp/aecp_mbx.h" | sed 's/^/aecp_mbx.h:21-27: /'
printf 'ctrl_retry_search.py at head: '; git -C "$C" ls-files | grep -c ctrl_retry_search || true
printf 'deleted by: '; git -C "$C" log --format='%h' --diff-filter=D -1 -- sw/firmware/ctrl/test/ctrl_retry_search.py
echo "## F2: the polls-by-source table against poll_grade.STATED_US"
sed -n '2215p;2217,2229p' "$D" | cut -c1-260
grep -n -A3 '^STATED_US = ' "$T/poll_grade.py"
echo "## F3: the save bounds"
line 2518 SPLIT_CONTROL_MEMORY.md "$D"; line 1624 SPLIT_CONTROL_MEMORY.md "$D"; line 1625 SPLIT_CONTROL_MEMORY.md "$D"
line 108 README.md "$T/README.md"; line 112 README.md "$T/README.md"
echo "## F4: the 32x32/2if load"
line 2525 SPLIT_CONTROL_MEMORY.md "$D"
echo "## F5: the flip check's bounds"
line 2244 SPLIT_CONTROL_MEMORY.md "$D" | cut -c1-900; line 2207 SPLIT_CONTROL_MEMORY.md "$D"
echo "## F6: the sweep patterns"
grep -n "0\\\\.\\\\d{3}\|HEAD_LOADS = \|A #define's bare number counts" "$C/../pkt/review-evidence/894-r1/author-r19/scripts/figure_sweep.py" || true

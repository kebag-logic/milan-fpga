#!/bin/sh
# R496-4 reviewer probes for PR #668 at e6420c0f (disposable; portable POSIX sh).
# Usage: run_probes.sh CLONE PACKET
#   CLONE  a checkout of the exact head (read only)
#   PACKET the output directory (receipts/ and scratch/ are written there)
set -eu
CLONE=$1
PACKET=$2
S=$PACKET/scratch/probes
R=$PACKET/receipts
mkdir -p "$S" "$R"
FW=$CLONE/sw/firmware/ctrl
CFLAGS="-std=c11 -O1 -Wall -Wextra -I$FW/adp -I$FW/wire"

# the reference: the head's adp.c with the round-3 unbounded queue restored
sed 's/a->departing_owed < ADP_DEPARTING_OWED_MAX/a->departing_owed != UINT32_MAX/' "$FW/adp/adp.c" > "$S/adp_ref.c"
grep -q 'departing_owed != UINT32_MAX' "$S/adp_ref.c"
cc $CFLAGS -o "$S/probe_head" "$PACKET/probes/probe_coalesce_diff.c" "$FW/adp/adp.c"
cc $CFLAGS -o "$S/probe_ref" "$PACKET/probes/probe_coalesce_diff.c" "$S/adp_ref.c"

rc=0
: > "$R/probe_diff.log"
for seed in $(seq 1 400); do
	"$S/probe_head" drain "$seed" 3000 > "$S/h.$seed" || { rc=1; echo "seed $seed: head invariant FAIL in drain mode" >> "$R/probe_diff.log"; }
	"$S/probe_ref" drain "$seed" 3000 > "$S/r.$seed" || true
	if ! python3 "$PACKET/probes/compare_traces.py" "$S/h.$seed" "$S/r.$seed" > "$S/c.$seed"; then
		rc=1
		echo "seed $seed: $(tr '\n' ' ' < "$S/c.$seed")" >> "$R/probe_diff.log"
	fi
	grep -h '^END' "$S/h.$seed" | sed "s/^/seed $seed head /" >> "$S/ends_head"
done
python3 - "$S" >> "$R/probe_diff.log" <<'EOF'
import glob, re, sys
tot_ref_only = tot_head = seeds = passes = 0
coal = 0
for c in glob.glob(sys.argv[1] + "/c.*"):
    t = open(c).read()
    seeds += 1
    passes += t.strip().endswith("PASS")
    m = re.search(r"head frames (\d+), reference frames (\d+), reference-only frames (-?\d+)", t)
    tot_head += int(m.group(1)); tot_ref_only += int(m.group(3))
for h in glob.glob(sys.argv[1] + "/h.*"):
    m = re.search(r"coalesced=(\d+)", open(h).read().splitlines()[-1])
    coal += int(m.group(1))
print(f"drain mode: {passes} of {seeds} seeds PASS (states equal, wires equal after collapsing back-to-back identical DEPARTINGs)")
print(f"head frames {tot_head}; reference-only frames {tot_ref_only}; head departing_coalesced total {coal}")
EOF

: > "$R/probe_free.log"
fr=0
for seed in $(seq 1 400); do
	if ! "$S/probe_head" free "$seed" 20000 > "$S/f.$seed"; then
		fr=1
		grep -m3 '^FAIL' "$S/f.$seed" | sed "s/^/seed $seed /" >> "$R/probe_free.log"
	fi
	tail -n 1 "$S/f.$seed" | sed "s/^/seed $seed /" >> "$S/free_ends"
done
python3 - "$S/free_ends" >> "$R/probe_free.log" <<'EOF'
import re, sys
n = cmax = s = 0
for ln in open(sys.argv[1]):
    m = re.search(r"shutdowns=(\d+) coalesced=(\d+) owed=(\d+) fails=(\d+)", ln)
    n += 1; s += int(m.group(1)); cmax = max(cmax, int(m.group(2)))
    assert int(m.group(4)) == 0, ln
print(f"free mode: {n} seeds x 20000 inputs, invariants I1-I5 held; SHUTDOWNs acted {s}; max coalesced in a seed {cmax}")
EOF
[ $fr -eq 0 ] || rc=1

# the reference must actually exceed the cap somewhere, or the comparison is vacuous
if grep -q 'reference-only frames 0,' "$S"/c.* && ! grep -q 'reference-only frames [1-9]' "$S"/c.*; then
	echo "VACUOUS: no seed made the reference send a frame the head did not" >> "$R/probe_diff.log"
	rc=1
fi
cat "$R/probe_diff.log" "$R/probe_free.log"
exit $rc

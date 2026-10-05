#!/bin/sh
# R496-4: the differential probe must fail on planted coalescing defects.
# Usage: probe_selfcheck.sh CLONE PACKET
set -eu
CLONE=$1
PACKET=$2
S=$PACKET/scratch/probe_selfcheck
mkdir -p "$S"
FW=$CLONE/sw/firmware/ctrl
CFLAGS="-std=c11 -O1 -Wall -Wextra -I$FW/adp -I$FW/wire"
sed 's/a->departing_owed < ADP_DEPARTING_OWED_MAX/a->departing_owed != UINT32_MAX/' "$FW/adp/adp.c" > "$S/adp_ref.c"
cc $CFLAGS -o "$S/probe_ref" "$PACKET/probes/probe_coalesce_diff.c" "$S/adp_ref.c"
plant() { # name, perl substitution
	perl -0pe "$2" "$FW/adp/adp.c" > "$S/adp_$1.c"
	if cmp -s "$FW/adp/adp.c" "$S/adp_$1.c"; then echo "$1: PLANT FAILED"; exit 2; fi
	cc $CFLAGS -o "$S/probe_$1" "$PACKET/probes/probe_coalesce_diff.c" "$S/adp_$1.c"
}
plant drops-queued 's/(\t\ta->departing_coalesced\+\+;)/$1\n\t\ta->departing_owed--;/'
plant overwrites-oldest 's/(\t\ta->departing_coalesced\+\+;)/$1\n\t\ta->departing_index = index;/'
plant cap-one 's/a->departing_owed < ADP_DEPARTING_OWED_MAX/a->departing_owed < 1u/'
plant uncounted 's/\t\ta->departing_coalesced\+\+;/\t\t(void)0;/'
bad=0
for m in drops-queued overwrites-oldest cap-one uncounted; do
	hit=0
	for seed in $(seq 1 60); do
		"$S/probe_$m" drain "$seed" 3000 > "$S/h.$m.$seed" || hit=$((hit + 1))
		"$S/probe_ref" drain "$seed" 3000 > "$S/r.$seed" || true
		python3 "$PACKET/probes/compare_traces.py" "$S/h.$m.$seed" "$S/r.$seed" > /dev/null || hit=$((hit + 1))
	done
	if [ "$hit" -gt 0 ]; then echo "[ok] $m: probe failed it ($hit failing seed-checks of 120)"; else echo "[ESCAPED] $m"; bad=1; fi
done
exit $bad

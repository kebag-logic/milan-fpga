#!/bin/sh
# run_probes.sh REPO PACKET: (REPO is the exact-head clone; PACKET/scratch/repo-prior and repo-tally are its
# tracked tree with test_aecp.cpp replaced by 4cca9569's, and by the head's with its >= 20 floors raised to 1,000,000)
# run the round's focused probes concurrently (2 build jobs each, 16 total), each with its
# own verdict file under PACKET/receipts/probes; wait for all, then print every verdict line.
set -u
R=$1; P=$2; O=$P/scratch/probes; V=$P/receipts/probes
mkdir -p "$O" "$V"
EDIT=Core.MapEditsAreTheirDefinitionRowForRow
STREAMS=Core.MapEditWorkObservesEachOutputStreamOnce
WORDS="the edit reads its port once for each output stream its definition reaches"
SITE_OLD='if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, observed, e.input, &e.rows[n].r) ||'
SITE_NEW='if (!idle(a, observed, e.input, &e.rows[n].r) || (e.flags[n] & ILLEGAL) != 0u ||'
B_OLD='r->channel >= format_channels(stream->value + 74)'
B_NEW='r->channel > format_channels(stream->value + 74)'
PRIOR=$P/scratch/repo-prior
TALLY=$P/scratch/repo-tally
go() { repo=$1; label=$2; shift 2; ( timeout 560 python3 -B "$P/probe.py" "$repo" "$O" "$label" --jobs 2 "$@" > "$V/$label.txt" 2>&1; echo "rc $?" >> "$V/$label.txt" ) & }
go "$R" head-control-app --tests "$EDIT:$STREAMS" --want pass
go "$R" head-control-work --arm work --tests "$STREAMS" --want pass
go "$R" head-plant-read-before-legal --plant aecp/aecp_maps.c "$SITE_OLD" "$SITE_NEW" --want caught --words "$WORDS"
go "$PRIOR" prior-test-control --want pass
go "$PRIOR" prior-test-plant-read-before-legal --plant aecp/aecp_maps.c "$SITE_OLD" "$SITE_NEW" --want escaped
go "$R" head-plant-channel-boundary --plant aecp/aecp_maps.c "$B_OLD" "$B_NEW" --want caught
go "$PRIOR" prior-test-plant-channel-boundary --plant aecp/aecp_maps.c "$B_OLD" "$B_NEW" --want escaped
go "$TALLY" head-tally-floors-raised --want caught --words "the seeded edits include"
wait
for f in "$V"/*.txt; do echo "== $(basename "$f")"; grep -E '^\[|^rc ' "$f"; done

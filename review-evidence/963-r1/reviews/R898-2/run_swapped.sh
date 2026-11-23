#!/bin/sh
# run_swapped.sh REPO PACKET: the probes that need another test_aecp.cpp. aecp_arms compiles the clone's own
# sw/firmware/ctrl/test/test_aecp.cpp, so each phase writes the probe's test there, runs its probes concurrently (2
# build jobs each), and restores the exact-head blob with `git checkout`, checking the file's hash against the head's.
# Phase prior: 4cca9569's test_aecp.cpp. Phase tally: the head's with its ">= 20" floors raised to 1,000,000, so the
# failure text prints every seeded tally.
set -u
R=$1; P=$2; O=$P/scratch/probes; V=$P/receipts/probes
F=sw/firmware/ctrl/test/test_aecp.cpp
mkdir -p "$O" "$V"
WORDS="the edit reads its port once for each output stream its definition reaches"
SITE_OLD='if ((e.flags[n] & ILLEGAL) != 0u || !idle(a, observed, e.input, &e.rows[n].r) ||'
SITE_NEW='if (!idle(a, observed, e.input, &e.rows[n].r) || (e.flags[n] & ILLEGAL) != 0u ||'
B_OLD='r->channel >= format_channels(stream->value + 74)'
B_NEW='r->channel > format_channels(stream->value + 74)'
HEAD_BLOB=$(git -C "$R" rev-parse "HEAD:$F")
go() { label=$1; shift; ( timeout 560 python3 -B "$P/probe.py" "$R" "$O" "$label" --jobs 2 "$@" > "$V/$label.txt" 2>&1; echo "rc $?" >> "$V/$label.txt" ) & }
restore() { git -C "$R" checkout -- "$F"; test "$(git -C "$R" hash-object "$R/$F")" = "$HEAD_BLOB" && echo "restored $F to $HEAD_BLOB"; }
trap restore EXIT
git -C "$R" show 4cca956932073b3f704f12f81c53f2934cfa215c:$F > "$R/$F"
echo "phase prior: $(git -C "$R" hash-object "$R/$F") (4cca9569's $(git -C "$R" rev-parse 4cca956932073b3f704f12f81c53f2934cfa215c:$F))"
go prior-test-control --want pass
go prior-test-plant-read-before-legal --plant aecp/aecp_maps.c "$SITE_OLD" "$SITE_NEW" --want escaped
go prior-test-plant-channel-boundary --plant aecp/aecp_maps.c "$B_OLD" "$B_NEW" --want escaped
wait
restore
python3 -I -c 'import sys;p=sys.argv[1];t=open(p).read();o="EXPECT_GE(seen[name],20u)<<\"the seeded edits include \"";assert t.count(o)==1;open(p,"w").write(t.replace(o,o.replace("20u","1000000u")))' "$R/$F"
echo "phase tally: $(git -C "$R" hash-object "$R/$F")"
go head-tally-floors-raised --want caught --words "the seeded edits include"
wait
for f in "$V"/prior-*.txt "$V"/head-tally-*.txt; do echo "== $(basename "$f")"; grep -E '^\[|^rc ' "$f"; done

#!/bin/sh
# run_carriers.sh REPO PACKET: count how many of the edit definition test's seeded edits carry each kind of illegal
# mapping. Writes into the clone's test_aecp.cpp (the arm compiles that file) a copy of the head's test with one
# counter per kind at the injection site and an always-failing EXPECT_EQ that prints the counts, runs the unplanted
# app arm, and restores the exact-head blob with `git checkout`, checking its hash.
set -u
R=$1; P=$2; O=$P/scratch/probes; V=$P/receipts/probes
F=sw/firmware/ctrl/test/test_aecp.cpp
mkdir -p "$O" "$V"
HEAD_BLOB=$(git -C "$R" rev-parse "HEAD:$F")
restore() { git -C "$R" checkout -- "$F"; test "$(git -C "$R" hash-object "$R/$F")" = "$HEAD_BLOB" && echo "restored $F to $HEAD_BLOB"; }
trap restore EXIT
python3 -I - "$R/$F" <<'EOF'
import sys
p = sys.argv[1]
t = open(p).read()
old = "            edit[at]=c<ABSENT?aecp_mapping{ILLEGAL,0,0,0}:aecp_mapping{uint16_t(next()%2),past[in],0,0};\n"
assert t.count(old) == 1
t = t.replace(old, old + "            ++carriers[c<ABSENT?0:1];\n")
old = "    constexpr unsigned ABSENT=4000;\n"
assert t.count(old) == 1
t = t.replace(old, old + "    unsigned carriers[2]={};\n")
old = "    streaming=false;\n    for(auto name:{\"ADD 0\""
assert t.count(old) == 1
t = t.replace(old, "    EXPECT_EQ(carriers[0]*100000u+carriers[1],0u)<<\"PROBE carriers: no-stream kind*100000 + existing-stream kind\";\n" + old)
open(p, "w").write(t)
EOF
echo "probe test: $(git -C "$R" hash-object "$R/$F")"
timeout 560 python3 -B "$P/probe.py" "$R" "$O" head-illegal-carriers --jobs 8 --want caught --words "PROBE carriers" > "$V/head-illegal-carriers.txt" 2>&1
echo "rc $?" >> "$V/head-illegal-carriers.txt"
grep -E '^\[|^rc ' "$V/head-illegal-carriers.txt"
grep -B4 'PROBE carriers' "$O/head-illegal-carriers.log" | head -8

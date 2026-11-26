#!/bin/bash
# claims.sh CLONE R2DIR PRBODY BASE: extract the evidence each prior finding's
# resolution rests on. R2DIR is the downloaded review-evidence/pins1125-r2.
set -u
C=$1; R=$2; B=$3; BASE=$4
g() { git -C "$C" "$@"; }
echo "# claims at $(g rev-parse HEAD)"
echo "== r2 packet: sha256 against MANIFEST.json"
python3 -I - "$R" <<'EOF'
import json, hashlib, sys, os
r = sys.argv[1]
for e in json.load(open(os.path.join(r, "MANIFEST.json"))):
    h = hashlib.sha256(open(os.path.join(r, e["file"]), "rb").read()).hexdigest()
    print("OK " if h == e["published_sha256"] else "BAD", e["file"], h[:16])
EOF
echo "== R938-2 F2: tolerance comment and the assertion it describes"
grep -n 'kOffsetNearNs\|kGradedOffsetNs' "$C/tb/verilator/gptp_shadow/sim_main.cpp"
sed -n '2983,2992p' "$C/tb/verilator/gptp_shadow/sim_main.cpp"
grep -n -A2 '^static bool near' "$C/tb/verilator/gptp_shadow/sim_main.cpp"
echo "-- the phase-6 claim: gptp_plane checks the used delay exactly"
grep -n 'the engine publishes the used delay\|its offset uses the delay exactly' -A1 "$C/tb/verilator/gptp_plane/sim_main.cpp"
echo "== R937-2 F2: #109 planted defects new since $BASE (base count, head count)"
for n in delay-below-80-refused no-floor used-delay-clamped-to-zero floor-at-zero floor-at-799 \
         published-before-the-floor 801-is-good 800-is-bad public_bank_publishes_a_negative_delay \
         public_bank_keeps_a_stale_offset graded_follow_up_not_sent; do
  b=$(g grep -c -- "$n" "$BASE" -- tb | awk -F: '{s+=$NF}END{print s+0}')
  h=$(g grep -c -- "$n" HEAD -- tb | awk -F: '{s+=$NF}END{print s+0}')
  echo "$n base=$b head=$h"
done
echo "-- receipts: gptp_plane link_delay planted lines, gptp_shadow #109 controls"
grep -c '^PASS planted defect' <(sed -n '/link_delay campaign/q;p' "$R/author/receipts/gptp_plane.log")
grep -E '^\[ ok \] public_bank_|^\[ ok \] graded_' "$R/author/receipts/gptp_shadow.log"
echo "-- CHANGELOG line"; grep -n 'planted defects each fail' "$C/CHANGELOG.md"
echo "-- PR table rows under 'Planted defects, each caught by name'"
awk '/^Planted defects, each caught by name/{f=1;next} f&&/^\|/{n++} f&&!/^\|/&&n{exit} END{print n-2, "defect rows"}' "$B"
echo "== R938-2 F1: old-generator shadow tally and the PR instruction"
grep -n 'checks:' "$R/author/receipts/old-generator-red.log"
grep -n 'To see the regression go red' "$B"
echo "== R937-2 F1: the phase-22 row's wording"
grep -o 'within 64 ns, [a-z ]*when the plane uses that pair' "$B"
grep -o 'within 64 ns, [a-z ]*when the plane [a-z]* [a-z ]*floored' "$C/tb/verilator/gptp_shadow/README.md"

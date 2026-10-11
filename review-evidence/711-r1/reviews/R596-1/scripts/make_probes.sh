#!/usr/bin/env bash
# Build the srp_latency walk-probe trees under scratch/probes from the review clone.
# Each probe is a shared clone at a named commit plus one textual edit of
# sw/firmware/ctrl/test/srp_latency.cpp; the edit is asserted to apply exactly once.
set -euo pipefail
SRC=${SRC:-$REVIEWS/r596-1-711}
P=$REVIEWS/711-r596-1-packet
S=$P/scratch/probes
HEAD_SHA=49b437f445e34b558106c8799c1ffc0a5dc844cf
BASE_SHA=e8454e2751d05b02ee8e5a571857589ab358ab86
PIN_SHA=55ef91b75   # first commit: pin moved, old walk, no assertion
mkdir -p "$S"
F=sw/firmware/ctrl/test/srp_latency.cpp

clone() { # name commit
  git clone -q --shared --no-checkout "$SRC" "$S/$1"
  git -C "$S/$1" -c advice.detachedHead=false checkout -q --detach "$2"
}
edit() { # name python-replacement-script-args...
  python3 -I "$P/scripts/edit_once.py" "$S/$1/$F" "$2" "$3"
}

OLD_WALK='                else { const unsigned n=wire_be16(f->bytes+off)&8191u;
                       off+=2+width+(n+2)/3+2; }'
NEW_WALK='                else { // 802.1Q-2018 10.8.1.2: a Message holds vectors up to its EndMark.
                       while(off+2<=f->len && (f->bytes[off] || f->bytes[off+1])) {
                           const unsigned n=wire_be16(f->bytes+off)&8191u;
                           off+=2+width+(n+2)/3;
                       }
                       off+=2; }'
ASSERT_LINES='            ASSERT_TRUE(off+2<=f->len && !f->bytes[off] && !f->bytes[off+1])
                <<"walk must end on the MRPDU EndMark";
'

# exact head and base, unmodified
clone head-exact "$HEAD_SHA"
clone base-exact "$BASE_SHA"
# E1: head, MVRP walk reverted to one vector per Message, end assertion kept (new pin)
clone e1-oldwalk-assert "$HEAD_SHA"; edit e1-oldwalk-assert "$NEW_WALK" "$OLD_WALK"
# E2: base (old pin check) with the head's srp_latency.cpp
clone e2-newwalk-base "$BASE_SHA"
git -C "$SRC" show "$HEAD_SHA:$F" > "$S/e2-newwalk-base/$F"
# E3: base, old walk plus only the end assertion (old pin)
clone e3-oldwalk-assert-base "$BASE_SHA"
python3 -I "$P/scripts/edit_once.py" "$S/e3-oldwalk-assert-base/$F" \
  '            if(la && !seen[i][p]) {' "${ASSERT_LINES}"'            if(la && !seen[i][p]) {'
# E4: first commit (pin moved, old walk, no assertion) at the new pin
clone e4-pinonly "$PIN_SHA"
# M1: head, VectorAttribute size drops the ThreePackedEvents rounding ((n+2)/3 -> n/3)
clone m1-vecsize "$HEAD_SHA"; edit m1-vecsize 'off+=2+width+(n+2)/3;' 'off+=2+width+n/3;'
# M2: head, the Message EndMark is not skipped after the vectors
clone m2-noendskip "$HEAD_SHA"; edit m2-noendskip '                       off+=2; }' '                       }'
# M3: head, the walk reads only the first vector of a Message (break after one)
clone m3-onevector "$HEAD_SHA"; edit m3-onevector 'off+=2+width+(n+2)/3;' 'off+=2+width+(n+2)/3; break;'
# M4: head, the end assertion removed (old walk kept new): proves the walk itself is exercised by seen[]
clone m4-noassert-oldwalk "$HEAD_SHA"; edit m4-noassert-oldwalk "$NEW_WALK" "$OLD_WALK"
python3 -I "$P/scripts/edit_once.py" "$S/m4-noassert-oldwalk/$F" "${ASSERT_LINES}" ''
for d in "$S"/*/; do echo "$(basename "$d") $(git -C "$d" rev-parse --short HEAD) $(git -C "$d" diff --stat | tail -1)"; done

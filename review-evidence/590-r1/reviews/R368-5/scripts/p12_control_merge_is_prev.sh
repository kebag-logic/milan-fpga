#!/usr/bin/env bash
# P12: for each file both sides edited, the merge's edit of the lane copy
# (PREV -> MERGE) must carry exactly dev's changed lines (BASE -> DEV), and the
# merge's edit of dev's copy (DEV -> MERGE) exactly the lane's (BASE -> PREV).
# Compares ordered +/- line sequences, ignoring hunk positions.
set -u
BASE=7a7582f03ce5ba7863a90ac342c21be18d90db0b; PREV=1f039cfe86d5337f5c9b7248696dba1c4bdda67e
DEV=b5c0f69d5d11f0ec4bc847a2cfdd13e89e199a8a; MERGE=1f039cfe86d5337f5c9b7248696dba1c4bdda67e
body() { git diff -U0 --no-color "$1" "$2" -- "$3" | grep -E '^[+-]' | grep -vE '^(\+\+\+|---) ' ; }
for f in docs/integration/BAREMETAL_FIRMWARE.md docs/reference/MILAN_COMPLIANCE_MATRIX.md \
         docs/reference/REGISTER_MAP.md sw/builder/test_builder.py docs/findings/README.md; do
  a=$(cmp -s <(body $BASE $DEV "$f") <(body $PREV $MERGE "$f") && echo EQUAL || echo DIFFERENT)
  b=$(cmp -s <(body $BASE $PREV "$f") <(body $DEV $MERGE "$f") && echo EQUAL || echo DIFFERENT)
  echo "$f: dev-edit-carried=$a lane-edit-carried=$b (dev +/-: $(body $BASE $DEV "$f" | wc -l), lane +/-: $(body $BASE $PREV "$f" | wc -l))"
done

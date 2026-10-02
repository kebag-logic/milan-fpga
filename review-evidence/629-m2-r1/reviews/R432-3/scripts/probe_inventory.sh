#!/bin/sh
# SPDX-FileCopyrightText: 2026 Kebag Logic
# SPDX-License-Identifier: CERN-OHL-W-2.0
# [R432] round-3 probes of the Entity shape gate fix (PR #634, head 0b066b6e).
# Usage: probe_inventory.sh <disposable copy of the head> <variant> <dir holding make 4.3 as `make`>
# Variants (each applied to the disposable copy only, then both makes run):
#   head        - unmodified head (control)
#   round2      - scripts/shape_consumer_inventory.py, entity_shape_selftest.py and
#                 tb/verilator/milan_dp_mclk/Makefile at round 2 (d81198c2): F1 reproduced
#   no_derive   - classified_frozen_targets() returns set() (the fix removed)
#   overbroad   - every frozen token of a makefile that has ANY classified $-reference
#                 is skipped (classification by file, not by path)
#   cross_file  - classified_frozen_targets() ignores which makefile a classified entry
#                 belongs to (another file's classification leaks)
#   no_makeflags- the root suite's nested derivations without `MAKEFLAGS=`
# For each make: plain gate rc, --self-test rc + tally + failing lines, and the frozen
# shape prerequisites make's database lists for the root suite's Makefile.
set -u
T=$(cd "$1" && pwd); V=$2; M43=$(cd "$3" && pwd)
cd "$T"
INV=scripts/shape_consumer_inventory.py
case "$V" in
  head) ;;
  round2)
    for f in $INV scripts/entity_shape_selftest.py tb/verilator/milan_dp_mclk/Makefile; do
      git show d81198c2001756fd84c353d93c312c133c5af66b:$f > $f; done ;;
  no_derive)
    python3 - "$INV" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a='    targets = set()\n    for consumer, reference in CLASSIFIED_CONSUMERS:\n'
assert s.count(a)==1; s=s.replace(a,'    targets = set()\n    return targets\n    for consumer, reference in CLASSIFIED_CONSUMERS:\n'); open(p,'w').write(s)
EOF
    ;;
  overbroad)
    python3 - "$INV" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a='        if target in classified:\n            continue\n'
assert s.count(a)==1
s=s.replace(a,'        if target in classified or any(c == name and "$" in r for c, r in CLASSIFIED_CONSUMERS):\n            continue\n'); open(p,'w').write(s)
EOF
    ;;
  cross_file)
    python3 - "$INV" <<'EOF'
import sys; p=sys.argv[1]; s=open(p).read()
a='        if consumer != name or "$" not in reference:\n'
assert s.count(a)==1; s=s.replace(a,'        if "$" not in reference:\n'); open(p,'w').write(s)
EOF
    ;;
  no_makeflags)
    sed -i 's/\$(shell MAKEFLAGS= \$(MAKE)/$(shell $(MAKE)/' tb/verilator/milan_dp_mclk/Makefile
    grep -c 'shell MAKEFLAGS=' tb/verilator/milan_dp_mclk/Makefile | sed 's/^/MAKEFLAGS= occurrences after edit: /' ;;
  *) echo "unknown variant $V"; exit 2 ;;
esac
echo "variant=$V changed: $(git status --porcelain | tr '\n' ' ')"
for which in 43 host; do
  if [ $which = 43 ]; then P="$M43:$PATH"; else P="$PATH"; fi
  echo "==== make: $(PATH=$P make --version | head -1)"
  PATH=$P python3 scripts/check_entity_shape.py > /tmp/r432p.$$ 2>&1; rc=$?
  echo "plain gate rc=$rc"; grep -E 'FAIL|RESULT' /tmp/r432p.$$ | head -n 8
  PATH=$P python3 scripts/check_entity_shape.py --self-test > /tmp/r432s.$$ 2>&1; rc=$?
  echo "self-test rc=$rc"; grep -E '\[FAIL\]|FAIL |RESULT|checks:' /tmp/r432s.$$ | head -n 12
  echo "frozen shape prerequisites in the root suite's database:"
  PATH=$P python3 -c "
import sys; sys.path.insert(0,'scripts')
import shape_consumer_inventory as i
print('  ', i.shape_prereqs_from_database(i.ROOT/'tb/verilator/milan_dp_mclk','Makefile'))
print('   classified_frozen_targets:', sorted(i.classified_frozen_targets('tb/verilator/milan_dp_mclk/Makefile')))"
done
rm -f /tmp/r432p.$$ /tmp/r432s.$$
git checkout -q -- .
echo "restored: $(git status --porcelain | wc -l) changed paths"

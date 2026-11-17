#!/bin/bash
# The cause, at the base: the reviewed head's unit test of every acknowledged name surviving the real store's power
# cycle, inserted into the base 659d7687's test_aecp.cpp (less its pending_count line, which the base lacks), run on
# the base's own aecp_nvm.c, then the same on the first fix commit 945a1217. Usage: base_cause_probe.sh REPO OUT
set -u
REPO=$1 OUT=$2
mkdir -p "$OUT"
for rev in 659d7687 945a1217; do
  t="$OUT/tree-$rev"; rm -rf "$t"
  git clone -q --no-checkout "$REPO" "$t" && git -C "$t" -c advice.detachedHead=false checkout -q "$rev"
  for sm in gptp-processor protocol-processor third_party/tsn-c-stack third_party/lwSRP; do
    git -C "$t" -c protocol.file.allow=always -c "submodule.$sm.url=$REPO/$sm" submodule update -q --init "$sm"
  done
  git -C "$REPO" show 945a1217:sw/firmware/ctrl/test/test_aecp.cpp \
    | sed -n '/^\/\/ #920: a SET_NAME of every user-settable name/,/^}/p' | grep -v 'pending_count' > "$OUT/test-$rev.inc"
  python3 -I - "$t/sw/firmware/ctrl/test/test_aecp.cpp" "$OUT/test-$rev.inc" <<'EOF'
import sys
path, inc = sys.argv[1], open(sys.argv[2]).read()
src = open(path).read()
if 'EveryAcknowledgedNameSurvivesTheRealStorePowerCycle' in src:
    sys.exit(0)  # the fix commit carries it already
anchor = '// #763: an emptied list in either direction'
assert anchor in src, 'anchor'
open(path, 'w').write(src.replace(anchor, inc + '\n' + anchor, 1))
EOF
  ( cd "$t" && python3 -B sw/firmware/ctrl/test/aecp_arms.py --output "$OUT/out-$rev" --nvm \
      --filter 'Nvm.EveryAcknowledgedNameSurvivesTheRealStorePowerCycle' \
      --stack "$REPO/third_party/tsn-c-stack" ) > "$OUT/run-$rev.log" 2>&1
  echo "$rev rc=$?" | tee "$OUT/rc-$rev.txt"
done

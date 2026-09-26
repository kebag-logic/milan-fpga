#!/usr/bin/env bash
# R327-2 probes 5-6. Usage: probes2.sh <checkout>
# P6 temporarily moves the protocol-processor checkout and restores it; it ends by
# verifying the checkout equals the superproject gitlink again.
set -u
REPO=${1:?checkout}
cd "$REPO" || exit 2
OLD=54b4c3bbbc8cdea5ced0be29c9226fdf82233b74; NEW=9143e21a57e6315c7678430cfc45b4a2b7e10c09

echo "## P5: every path outside the two changed documents is byte-identical between $OLD and $NEW"
git ls-tree -r "$OLD" | grep -v -P '\t(docs/reference/SUBMODULES\.md|tb/verilator/milan_dp/README\.md)$' > /tmp/r327_2_old.$$
git ls-tree -r "$NEW" | grep -v -P '\t(docs/reference/SUBMODULES\.md|tb/verilator/milan_dp/README\.md)$' > /tmp/r327_2_new.$$
echo "entries old=$(wc -l < /tmp/r327_2_old.$$) new=$(wc -l < /tmp/r327_2_new.$$)"
if cmp -s /tmp/r327_2_old.$$ /tmp/r327_2_new.$$; then echo "IDENTICAL (modes, blob/gitlink ids, paths)"; else echo DIFFERENT; diff /tmp/r327_2_old.$$ /tmp/r327_2_new.$$ | head; fi
grep -P '^160000' /tmp/r327_2_new.$$
rm -f /tmp/r327_2_old.$$ /tmp/r327_2_new.$$
echo "changed paths: $(git diff --name-only "$OLD" "$NEW" | tr '\n' ' ')"

echo "## P6: the README:468 restore step, 'restore the pin of record', executed"
PIN=$(git rev-parse :protocol-processor)
[ -z "$(git -C protocol-processor status --porcelain)" ] || { echo "processor checkout dirty; refusing"; exit 2; }
git -C protocol-processor checkout -q --detach 7a47f578
echo "repinned checkout=$(git -C protocol-processor rev-parse HEAD) gitlink=$PIN"
git submodule status protocol-processor
git submodule update -q protocol-processor
AFTER=$(git -C protocol-processor rev-parse HEAD)
echo "after 'git submodule update protocol-processor': checkout=$AFTER"
[ "$AFTER" = "$PIN" ] && echo "RESTORED to the pin of record" || { echo "NOT RESTORED"; exit 1; }
git submodule status protocol-processor

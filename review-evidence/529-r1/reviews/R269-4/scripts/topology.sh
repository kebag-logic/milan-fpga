#!/usr/bin/env bash
# Composition topology of the merge-train candidate: merge base, the dev-side
# commits the source head has not seen, the source-side commits, and the
# overlap of the two sides' net-changed paths.
# Usage: topology.sh <repo> <candidate> <dev> <source>
set -euo pipefail
repo=$1 cand=$2 dev=$3 src=$4
g() { git -C "$repo" "$@"; }
mb=$(g merge-base "$dev" "$src")
echo "candidate      $(g rev-parse "$cand") tree $(g rev-parse "$cand^{tree}")"
echo "parents        $(g log -1 --format=%P "$cand")"
echo "dev            $(g rev-parse "$dev") tree $(g rev-parse "$dev^{tree}")"
echo "source         $(g rev-parse "$src") tree $(g rev-parse "$src^{tree}")"
echo "merge-base     $mb"
echo "merge-bases    $(g merge-base --all "$dev" "$src" | tr '\n' ' ')"
echo
echo "## dev-side commits not in source ($mb..$dev), --format='%H %P | %s'"
g log --format='%H %P | %s' "$mb..$dev"
echo
echo "## dev-side first-parent chain ($mb..$dev)"
g log --first-parent --format='%H %P | %s' "$mb..$dev"
echo
echo "## source-side commits ($mb..$src)"
g log --format='%H %P | %s' "$mb..$src"
echo
echo "## commits in candidate not in dev (must be exactly source side + candidate)"
g log --format='%H' "$dev..$cand"
echo
echo "## net-changed paths, dev side ($mb..$dev)"
g diff --no-renames --name-status "$mb" "$dev" | sort -k2 > /tmp/topo_dev.$$
cat /tmp/topo_dev.$$
echo
echo "## net-changed paths, source side ($mb..$src)"
g diff --no-renames --name-status "$mb" "$src" | sort -k2 > /tmp/topo_src.$$
cat /tmp/topo_src.$$
echo
echo "## paths changed on BOTH sides"
join -1 2 -2 2 <(sort -k2 /tmp/topo_dev.$$) <(sort -k2 /tmp/topo_src.$$) || true
echo "## (end of overlap)"
echo
echo "## candidate tree == 3-way merge-tree of dev and source?"
mt=$(g merge-tree --write-tree "$dev" "$src" | head -1)
echo "merge-tree --write-tree: $mt"
[ "$mt" = "$(g rev-parse "$cand^{tree}")" ] && echo "MATCH candidate tree" || echo "MISMATCH candidate tree"
echo
echo "## candidate vs dev: paths changed (must equal source-side set)"
g diff --no-renames --name-status "$dev" "$cand" | sort -k2 > /tmp/topo_cd.$$
cat /tmp/topo_cd.$$
echo
echo "## candidate vs source: paths changed (must equal dev-side set)"
g diff --no-renames --name-status "$src" "$cand" | sort -k2 > /tmp/topo_cs.$$
cat /tmp/topo_cs.$$
echo
echo "## set equality checks"
diff <(awk '{print $2}' /tmp/topo_cd.$$) <(awk '{print $2}' /tmp/topo_src.$$) && echo "cand-vs-dev paths == source-side paths"
diff <(awk '{print $2}' /tmp/topo_cs.$$) <(awk '{print $2}' /tmp/topo_dev.$$) && echo "cand-vs-source paths == dev-side paths"
echo
echo "## per-path blob identity: candidate blob == source blob for every source-side path"
while read -r st p; do
  cb=$(g rev-parse -q --verify "$cand:$p" 2>/dev/null || echo ABSENT)
  sb=$(g rev-parse -q --verify "$src:$p" 2>/dev/null || echo ABSENT)
  [ "$cb" = "$sb" ] && r=SAME || r=DIFF
  echo "$r $st $p cand=$cb src=$sb"
done < /tmp/topo_src.$$
echo
echo "## per-path blob identity: candidate blob == dev blob for every dev-side path"
while read -r st p; do
  cb=$(g rev-parse -q --verify "$cand:$p" 2>/dev/null || echo ABSENT)
  db=$(g rev-parse -q --verify "$dev:$p" 2>/dev/null || echo ABSENT)
  [ "$cb" = "$db" ] && r=SAME || r=DIFF
  echo "$r $st $p cand=$cb dev=$db"
done < /tmp/topo_dev.$$
rm -f /tmp/topo_*.$$

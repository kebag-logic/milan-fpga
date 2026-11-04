#!/usr/bin/env bash
# command_table_probe.sh <scratch dir> <shfmt>: the image command-table checker (scripts/ci_tool_inventory.py --check)
# on fresh clean clones of the round 6 head, its two parents and the merge base, unmodified; then, in a disposable
# copy of the head only, the one digest dev left stale re-pinned to the file's bytes, to show what else refuses.
set -u
S=$1; export CI_IMAGE_SHFMT=$2; L=$LANES/797-d0-audit
H=$(git -C "$L" rev-parse HEAD)
# A fresh clean clone with its submodules (clone_at.sh), at the full SHA of <rev>.
clone() { rm -rf "$2"; bash "$(dirname "$0")/../receipts/gates/tools/clone_at.sh" "$(git -C "$L" rev-parse "$1")" "$2"; }
echo "shfmt: $("$CI_IMAGE_SHFMT" --version)"
for rev in HEAD HEAD^1 HEAD^1^1 HEAD^1^2 "$(git -C "$L" merge-base e8ec8d20 HEAD^1^2)"; do
  sha=$(git -C "$L" rev-parse --short=8 "$rev"); d=$S/ct-$sha
  clone "$rev" "$d" || { echo "clone $rev failed"; continue; }
  echo "== $sha ($rev): python3 scripts/ci_tool_inventory.py --check"
  ( cd "$d" && python3 scripts/ci_tool_inventory.py --check ); echo "rc=$?"
  echo "-- declared script digests against the bytes:"; python3 -I "$(dirname "$0")/table_digests.py" "$d"
done
echo "== $(git -C "$L" rev-parse --short=8 HEAD): docs workflow inventory step walked through the command-table walker"
( cd "$S/ct-$(git -C "$L" rev-parse --short=8 HEAD)" && python3 -I "$(dirname "$0")/walk_inventory_step.py" . ); echo "rc=$?"
d=$S/ct-repin; clone HEAD "$d" || exit 9
( cd "$d" && python3 - <<'PY'
import hashlib, json, pathlib
p = pathlib.Path('ci/image/command-table.json'); t = json.loads(p.read_text())
name = 'sw/builder/endstation_builder.py'
old = t['scripts'][name]['sha256']; new = hashlib.sha256(pathlib.Path(name).read_bytes()).hexdigest()
t['scripts'][name]['sha256'] = new
p.write_text(json.dumps(t, indent=2) + '\n')
print(f'disposable copy only: {name} {old[:12]} -> {new[:12]}')
PY
)
echo "== disposable copy, diff:"; git -C "$d" diff --stat
echo "== disposable copy: python3 scripts/ci_tool_inventory.py --check"
( cd "$d" && python3 scripts/ci_tool_inventory.py --check ); echo "rc=$?"

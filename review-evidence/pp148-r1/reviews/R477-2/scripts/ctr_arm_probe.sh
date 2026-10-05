#!/usr/bin/env bash
# Exercise tb/pp_top/ctr_mutants.py's own plant() for the arm
# ctr-notify-one-window at OLD and NEW (no build, no simulation), then show
# that a context-refreshed copy of the same patch plants at NEW and yields the
# same planted sv2v design as the committed patch at OLD.
# Usage: ctr_arm_probe.sh <repo> <old-rev> <new-rev> <scratch-dir>
set -uo pipefail
repo=$1 old=$2 new=$3 scr=$4
arm=ctr-notify-one-window
f=hdl/aecp/KL_aecp_notify.sv
rm -rf "$scr"; mkdir -p "$scr"
for r in "$old" "$new"; do
  mkdir -p "$scr/src-$r" "$scr/plant-$r"
  git -C "$repo" archive "$r" | tar -x -C "$scr/src-$r"
  cp -r "$scr/src-$r/hdl" "$scr/plant-$r/hdl"
  echo "== $r: ctr_mutants.plant(tree, '$arm') via the driver's own code"
  python3 - "$scr/src-$r" "$scr/plant-$r" "$arm" <<'PY'
import importlib.util, subprocess, sys
from pathlib import Path
src, tree, arm = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3]
sys.path.insert(0, str(src / "tb" / "common"))
spec = importlib.util.spec_from_file_location("ctr_mutants", src / "tb/pp_top/ctr_mutants.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
try:
    m.plant(tree, arm)
    print("PLANTED")
except subprocess.CalledProcessError as e:
    print(f"plant() raised CalledProcessError: {e}")
    sys.exit(3)
PY
  echo "plant rc=$?"
done
echo "== refreshed patch: the committed patch with its two context comment lines replaced by NEW's four"
python3 - "$scr/src-$new/tb/pp_top/ctr_mutations/$arm.patch" "$scr/src-$new/$f" > "$scr/$arm.refreshed.patch" <<'PY'
import sys
p = open(sys.argv[1]).read().split("\n")
src = open(sys.argv[2]).read().split("\n")
i = next(k for k, l in enumerate(src) if "Provisional stamp" in l)
new_ctx = [" " + l for l in src[i:i + 4]]
out, skip = [], 0
for l in p:
    if l.startswith(" ") and ("Measure the one-second limit" in l or "possibly much earlier" in l):
        if "Measure" in l: out += new_ctx
        continue
    if l.startswith("@@"):
        l = "@@ -1297,10 +1297,11 @@"
    out.append(l)
print("\n".join(out), end="")
PY
diff "$scr/src-$new/tb/pp_top/ctr_mutations/$arm.patch" "$scr/$arm.refreshed.patch"
mkdir -p "$scr/plant-refreshed"; cp -r "$scr/src-$new/hdl" "$scr/plant-refreshed/hdl"
( cd "$scr/plant-refreshed" && git apply --check "$scr/$arm.refreshed.patch" && git apply "$scr/$arm.refreshed.patch" ) && echo "refreshed patch PLANTED at $new"
pk() { ( cd "$1" && find hdl -name '*_pkg.sv' | sort ); }
( cd "$scr/plant-$old" && sv2v $(pk "$scr/plant-$old") "$f" > planted.v )
( cd "$scr/plant-refreshed" && sv2v $(pk "$scr/plant-refreshed") "$f" > planted.v )
( cd "$scr/src-$old" && sv2v $(pk "$scr/src-$old") "$f" > unplanted.v )
sha256sum "$scr/plant-$old/planted.v" "$scr/plant-refreshed/planted.v" "$scr/src-$old/unplanted.v" | sed "s#$scr/##"
cmp "$scr/plant-$old/planted.v" "$scr/plant-refreshed/planted.v" && echo "planted design at NEW (refreshed patch) == planted design at OLD (committed patch): IDENTICAL"
cmp -s "$scr/plant-$old/planted.v" "$scr/src-$old/unplanted.v" || echo "planted design differs from the unplanted design (the arm is a real edit)"

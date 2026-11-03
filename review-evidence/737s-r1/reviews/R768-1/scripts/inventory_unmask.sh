#!/usr/bin/env bash
# In a disposable clone at <rev>: repeatedly re-pin only the declared-script hash named by
# the refusal in ci/image/command-table.json (so the next refusal is revealed), up to N rounds, and print each refusal.
# usage: inventory_unmask.sh <clone> <rev> <shfmt> [rounds]
set -u
C="$1"; REV="$2"; export CI_IMAGE_SHFMT="$3"; N="${4:-8}"
cd "$C" || exit 2
git checkout -q --force --detach "$REV" && git submodule update -q || exit 2
for i in $(seq 1 "$N"); do
  out="$(python3 scripts/ci_tool_inventory.py --check 2>&1)"; rc=$?
  echo "round $i rc=$rc: $(printf '%s' "$out" | tail -n1 | cut -c1-200)"
  [ $rc -eq 0 ] && break
  f="$(printf '%s' "$out" | sed -n "s/^REFUSED: changed declared script '\(.*\)'$/\1/p" | tail -n1)"
  [ -n "$f" ] || break
  h="$(sha256sum "$f" | cut -d' ' -f1)"
  python3 - "$f" "$h" <<'PY'
import json, sys
p = "ci/image/command-table.json"; d = json.load(open(p)); f, h = sys.argv[1:3]
d["scripts"][f]["sha256"] = h
open(p, "w").write(json.dumps(d, indent=2) + "\n")
PY
done
git checkout -q --force --detach "$REV"

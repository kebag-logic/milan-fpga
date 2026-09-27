#!/bin/sh
# R363-1: compare planner outputs at base and head for every area and mode.
# Usage: plan_diff.sh <repo-root> <base-sha> <head-sha> <scratch-dir>
set -eu
repo=$1; base=$2; head=$3; out=$4
mkdir -p "$out/base" "$out/head"
git -C "$repo" show "$base:tb/tools/torture_campaign.py" > "$out/base/torture_campaign.py"
git -C "$repo" show "$head:tb/tools/torture_campaign.py" > "$out/head/torture_campaign.py"
for side in base head; do
  for mode in "--plan --json" "--plan" "--checklist" "--coverage" "--coverage-by-area"; do
    tag=$(printf '%s' "$mode" | tr -c 'a-z' '_')
    for area in audio churn matrix multi payload physical torture soak power "soak,power" \
                "audio,churn,matrix,multi,payload,physical,torture,soak,power"; do
      atag=$(printf '%s' "$area" | tr -c 'a-z' '_')
      # shellcheck disable=SC2086
      python3 -B "$out/$side/torture_campaign.py" $mode --areas "$area" \
        > "$out/$side/$tag$atag.txt" 2>&1 || echo "rc=$?" >> "$out/$side/$tag$atag.txt"
    done
  done
done
diff -r "$out/base" "$out/head" --exclude=torture_campaign.py --exclude=__pycache__ > "$out/plan.diff" || true
echo "files compared: $(ls "$out/head" | grep -c txt)"
echo "differing files:"
diff -rq "$out/base" "$out/head" --exclude=torture_campaign.py --exclude=__pycache__ | sed 's/^/  /' || true

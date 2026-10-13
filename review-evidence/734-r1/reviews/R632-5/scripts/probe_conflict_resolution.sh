#!/usr/bin/env bash
# Mutation probes on the single merge conflict (scripts/ci_events.py INHERITED_STEP_ENV).
# Each probe is a fresh `git archive` copy of the head; the gate is `ci_events.py --check`.
# Usage: probe_conflict_resolution.sh <repo> <head> <python> <work_dir> <out_dir>
set -u
repo=$1 head=$2 py=$3 work=$4 out=$5
mkdir -p "$work" "$out"
export PYTHONDONTWRITEBYTECODE=1
# old|new literal replacements on scripts/ci_events.py; "control" leaves the file unchanged.
probes=(
  "control||"
  "dev-side-changes-env|\"EVENT_NAME\", \"PR_BASE_REF\", \"PR_HEAD_SHA\", \"PUSH_BEFORE_SHA\"|\"EVENT_NAME\", \"PR_BASE_SHA\", \"PUSH_BEFORE_SHA\""
  "drop-head-sha-from-changes-env|\"EVENT_NAME\", \"PR_BASE_REF\", \"PR_HEAD_SHA\", \"PUSH_BEFORE_SHA\"|\"EVENT_NAME\", \"PR_BASE_REF\", \"PUSH_BEFORE_SHA\""
  "pr-side-aggregate-env|\"CHANGES_RESULT\", \"FIRMWARE_BOUNDARY_RESULT\",|\"CHANGES_RESULT\","
  "drop-verilator-result|\"FIRMWARE_UNIT_RESULT\", \"FIRMWARE_VERILATOR_RESULT\",|\"FIRMWARE_UNIT_RESULT\","
)
for p in "${probes[@]}"; do
  IFS='|' read -r name old new <<<"$p"
  (
    dir="$work/$name"
    rm -rf "$dir"; mkdir -p "$dir"
    git -C "$repo" archive "$head" | tar -x -C "$dir"
    if [ -n "$old" ]; then
      "$py" -I - "$dir/scripts/ci_events.py" "$old" "$new" <<'EOF'
import pathlib, sys
path, old, new = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
text = path.read_text(encoding="utf-8")
assert text.count(old) == 1, f"expected one occurrence, found {text.count(old)}"
path.write_text(text.replace(old, new), encoding="utf-8")
EOF
    fi
    (cd "$dir" && "$py" scripts/ci_events.py --check) >"$out/$name.log" 2>&1
    echo $? >"$out/$name.rc"
  ) &
done
# The unresolved conflict text itself, as git's own replay of the merge produces it.
(
  dir="$work/unresolved-markers"
  rm -rf "$dir"; mkdir -p "$dir"
  git -C "$repo" archive "$head" | tar -x -C "$dir"
  tree=$(git -C "$repo" merge-tree --write-tree "$head^1" "$head^2" | head -n 1)
  git -C "$repo" show "$tree:scripts/ci_events.py" >"$dir/scripts/ci_events.py"
  (cd "$dir" && "$py" scripts/ci_events.py --check) >"$out/unresolved-markers.log" 2>&1
  echo $? >"$out/unresolved-markers.rc"
) &
wait
for f in "$out"/*.rc; do printf '%s\t%s\n' "$(basename "$f" .rc)" "$(cat "$f")"; done

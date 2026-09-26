#!/usr/bin/env bash
# Re-verify R332-6 F1 closure at a fixed PR head. Read-only GitHub queries.
# Usage: check_pr_body.sh [repo] [pr] [expected_head] [expected_tree]
set -euo pipefail
repo=${1:-kebag-logic/milan-fpga}
pr=${2:-572}
head=${3:-ae729bbfd90934f4d56d3b02f1ffc652496b414d}
tree=${4:-c2c692fb14fe731e46ff03873c11a45a77adc4e8}
out=$(mktemp -d)
trap 'rm -rf "$out"' EXIT

gh pr view "$pr" -R "$repo" --json headRefOid,body > "$out/pr.json"
live=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["headRefOid"])' "$out/pr.json")
python3 -c 'import json,sys;sys.stdout.write(json.load(open(sys.argv[1]))["body"])' "$out/pr.json" > "$out/body.md"
rtree=$(gh api "repos/$repo/git/commits/$head" --jq .tree.sha)

fail=0
echo "headRefOid=$live expected=$head"; [ "$live" = "$head" ] || fail=1
echo "tree=$rtree expected=$tree"; [ "$rtree" = "$tree" ] || fail=1

# Head-state claims F1 forbids. "local gate" is a gate name, not a head claim.
if grep -niE 'local and|unpush|not (yet )?pushed|unedited|not been edited|prepared replacement|publication .* pending' "$out/body.md"; then
  echo "FORBIDDEN head-state claim present"; fail=1
else
  echo "no local/unpushed/unedited head-state claim"
fi

# Every full SHA the body names must be the head or a named historical commit.
for s in $(grep -oE '\b[0-9a-f]{40}\b' "$out/body.md" | sort -u); do
  case $s in
    "$head") echo "$s current head";;
    7eb3b0d4a6987fd2e93ffc3b5be125267df7f53a) echo "$s source base (em-dash reference)";;
    3a1477c528bdf71b7cecadf86383b7579c9197d6) echo "$s Round 3 head (round-scoped history)";;
    *) echo "$s UNEXPECTED"; fail=1;;
  esac
done

grep -nE '^`?'"$head"'`? is the published PR head' "$out/body.md" || { echo "status line missing"; fail=1; }
echo "result=$([ $fail = 0 ] && echo PASS || echo FAIL)"
exit $fail

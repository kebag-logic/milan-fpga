#!/usr/bin/env bash
# [R632] round 2: the hosted scope branch trusts that GITHUB_SHA is a two-parent
# merge whose first parent is the base. If the checked-out sha were the PR head
# itself (a fast-forward), only the last PR commit would be classified.
# Usage: ff_guard_demo_r632_2.sh <shipping> <empty-dir> <python-with-yaml>
set -euo pipefail
ship="$(cd "$1" && pwd)"; r="$2"; py="$3"; g(){ git -c user.name=p -c user.email=p@x.invalid -C "$r" "$@"; }
g init -q; mkdir -p "$r/scripts" "$r/hdl" "$r/docs"; git -C "$ship" show HEAD:scripts/ci_scope.py > "$r/scripts/ci_scope.py"
echo r > "$r/docs/a.md"; g add .; g commit -qm base; B=$(g rev-parse HEAD)
echo 'module m; endmodule' > "$r/hdl/m.sv"; g add .; g commit -qm "PR RTL"
echo more >> "$r/docs/a.md"; g commit -qam "PR docs"; H=$(g rev-parse HEAD)
body="$("$py" -I -c 'import sys,yaml
d=yaml.safe_load(open(sys.argv[1]))
[st]=[x for x in d["jobs"]["changes"]["steps"] if x.get("id")=="scope"]
print(st["run"].replace("python3 scripts/ci_scope.py --selftest", ":"))' "$ship/.github/workflows/rtl-fast.yml")"
M=$(g commit-tree "$(g merge-tree --write-tree $B $H | head -1)" -p $B -p $H -m merge)
for sha in $M $H; do t=$(mktemp -d "$r/../t.XXXX"); (cd "$r" && env -i PATH="$PATH" HOME="$t" EVENT_NAME=pull_request PR_BASE_REF=dev PR_HEAD_SHA=$H GITHUB_SHA=$sha RUNNER_TEMP="$t" GITHUB_OUTPUT="$t/out" bash -euo pipefail -c "$body" >/dev/null)
  echo "GITHUB_SHA=$( [ $sha = $M ] && echo two-parent-merge || echo pr-head-ff ) files=[$(tr '\n' ' ' < "$t/changed-files")] $(cat "$t/out")"; done

#!/bin/bash
# Usage: probes.sh <clone at the reviewed head> <receipts dir> <scratch dir>. Prints classifier, resource-gate and integrity results.
set -u
C=$1; R=$2; S=$3; BASE=1f29f189279f9fc0132f4918e47342b87d22f33a; R8=20933ef48a9b174e58a9d17ddd59078a072024af; H=d63b378d27c1c663034744a5b48a99c190271f58
export PYTHONDONTWRITEBYTECODE=1 TMPDIR=$S
cd "$C" || exit 2
{
  python3 scripts/ci_scope.py --selftest 2>&1 | tail -1
  echo "paths in PR: $(git diff --name-only $BASE $H | wc -l); non-Markdown: $(git diff --name-only $BASE $H | grep -vc '\.md$')"
  echo "paths in round 9 delta: $(git diff --name-only $R8 $H | wc -l); non-Markdown: $(git diff --name-only $R8 $H | grep -vc '\.md$')"
  echo "classifier, PR at $R8: $(git diff --name-only $BASE $R8 | python3 scripts/ci_scope.py)"
  echo "classifier, PR at $H: $(git diff --name-only $BASE $H | python3 scripts/ci_scope.py)"
  echo "classifier, PR at $H minus AREA_BUDGET: $(git diff --name-only $BASE $H | grep -v '^docs/design/AREA_BUDGET.md$' | python3 scripts/ci_scope.py)"
  echo "scripts, .github, syn, tests paths changed by the PR: $(git diff --name-only $BASE $H -- scripts .github syn tests | wc -l)"
} > "$R/ci_scope.txt" 2>&1
B=$S/probe; mkdir -p "$B"
git show $R8:docs/design/AREA_BUDGET.md > "$B/r8.md"; git show $H:docs/design/AREA_BUDGET.md > "$B/head.md"
grep -vE '38,?040|60 percent' "$B/head.md" > "$B/mut_figures.md"
sed 's/^| `route-1x1` | +500 |/| `route-1x1` | +501 |/' "$B/head.md" > "$B/mut_policy.md"
{
  echo "r8 = round 8 budget; head = reviewed budget; mut_figures = head without lines naming 38,040 or 60 percent; mut_policy = head with the route-1x1 LUT tolerance +500 changed to +501"
  echo "mut_figures removes $(diff "$B/head.md" "$B/mut_figures.md" | grep -c '^<') lines; mut_policy changes $(diff "$B/head.md" "$B/mut_policy.md" | grep -c '^>') line"
  for b in r8 head mut_figures mut_policy; do
    o=$(python3 syn/ooc/pp_resource_gate.py check-baseline --budget "$B/$b.md" 2>&1); rc=$?
    echo "$b rc=$rc: $(echo "$o" | tail -1 | cut -c1-170)"
  done
  echo "default budget: $(python3 syn/ooc/pp_resource_gate.py check-baseline 2>&1 | tail -1)"
  echo "baseline json blob at base, round 8, head: $(git rev-parse $BASE:syn/ooc/pp_resource_baseline.json $R8:syn/ooc/pp_resource_baseline.json $H:syn/ooc/pp_resource_baseline.json | tr '\n' ' ')"
  for h in $R8 $H; do echo "policy table digest at $h: $(git show $h:docs/design/AREA_BUDGET.md | awk '/^\| Endpoint \| LUT/{f=1} f{ if(!/^\|/) exit; print}' | sha256sum | cut -c1-64)"; done
  for h in $R8 $H; do echo "measured cells (resource, device, route, used) digest at $h: $(git show $h:docs/design/AREA_BUDGET.md | grep -E '^\| (Slice LUT|Slice register|Slice|Block RAM tile|DSP|WNS)' | cut -d'|' -f2-5 | sha256sum | cut -c1-64)"; done
} > "$R/gate_negative_control.txt" 2>&1
{
  echo "HEAD $(git rev-parse HEAD); tree $(git rev-parse 'HEAD^{tree}'); index tree $(git write-tree)"
  echo "tracked changes: $(git status --porcelain | wc -l); ignored paths present: $(git status --porcelain --ignored | grep -c '^!!')"
  git diff --quiet HEAD && echo "worktree and index equal HEAD"
  git diff --check $BASE $H; echo "git diff --check rc=$?"
  git ls-files -s | grep '^160000'
  echo "gitlink differences from base: $(git diff --raw $BASE $H | grep -c ' 160000 ')"
  echo "delta commits with a body: $(git log --format='%b' $R8..$H | grep -c .)"
  echo "added delta lines naming a lane, round or reviewer: $(git diff $R8 $H | grep '^+' | grep -cE '\b(R75[78]|A72[0-9]|B[0-9]{2})\b')"
} > "$R/integrity.txt" 2>&1

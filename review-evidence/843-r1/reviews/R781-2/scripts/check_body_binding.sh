#!/usr/bin/env bash
# Re-check that PR #846's body names the exact head and that each gate figure it
# states is bound to the commit its published receipt was measured at.
# Usage: check_body_binding.sh <milan-fpga clone at the head> <output dir>
set -u
REPO=${1:?clone}; OUT=${2:?outdir}
HEAD=1105f54546b2f19d9577b7fad902c908e34f88ee
EV=3b2b1ef2607c8250dcaa1c55b6dbe496c90588c3
R=repos/kebag-logic/milan-fpga/contents/review-evidence/843-r1/author/receipts
raw() { gh api -H 'Accept: application/vnd.github.raw' "$R/$1?ref=$EV"; }
mkdir -p "$OUT"
gh pr view 846 -R kebag-logic/milan-fpga --json body,headRefOid > "$OUT/view.json"
python3 -I - "$OUT/view.json" "$HEAD" <<'EOF'
import json, sys
d = json.load(open(sys.argv[1])); h = sys.argv[2]; b = d['body']
print('headRefOid ==', d['headRefOid'] == h)
print('Status names head:', f'head `{h}`' in b)
print('checkout names head:', f'git checkout --detach {h}' in b)
print('stale 4c4c5982 full SHA in body:', '4c4c598273904f6c994b75c860e74ac742ae49d2' in b)
EOF
echo "== measured-at commit of each receipt family"
for f in sweep-1105f545/shard-0/complete.json sweep-1105f545/shard-1/complete.json \
         sweep-1105f545/shard-2/complete.json sweep-1105f545/shard-2-rerun/complete.json \
         sweep-1105f545/shard-3/complete.json; do
  printf '%s: %s\n' "$f" "$(raw "$f" | tr -d '\n ' )"
done
printf 'final-gates builder: %s\n' "$(raw final-gates-1105f545/builder.log | sed -n 1p)"
printf 'final-gates fw_service_budget: %s\n' "$(raw final-gates-1105f545/fw_service_budget.log | sed -n 1p)"
printf 'docs-yml tree-after: %s\n' "$(raw docs-yml-1105f545/docs-check__tree-after.txt | sed -n 1p)"
printf 'docs-yml tally: %s\n' "$(raw docs-yml-1105f545/verify.md | grep 'steps ran')"
printf 'physical: %s\n' "$(raw physical-gptp-4c4c5982/milan_dp_gptp.log | sed -n 1p)"
printf 'route-head bank.out commit: %s\n' "$(raw route-head/bank.out | sed -n 2p)"
printf 'route-dev bank.out commit: %s\n' "$(raw route-dev/bank.out | sed -n 2p)"
echo "mutants: directory mutants-8210abaa; $(raw mutants-8210abaa/mutants.json | python3 -I -c 'import json,sys;r=json.load(sys.stdin)["rows"];print(len(r),"mutants",sum(len(x["checks"]) for x in r),"check runs, all caught:",all(c["caught"] for x in r for c in x["checks"]))')"
echo "== files changed since the route/mutant commit 8210abaa"
git -C "$REPO" diff --stat 8210abaa1f5664bc6f755043b19a34a4eb38ede2 "$HEAD"
echo "== files changed since the physical-suite commit 4c4c5982"
git -C "$REPO" diff --name-only 4c4c598273904f6c994b75c860e74ac742ae49d2 "$HEAD"
echo "== route figures, head receipt"
raw route-head/route-1x1-check-shipping.log | grep -E '^(LUT|FF|SLICE|RAMB|DSP|WNS|WHS)'
echo "== route figures, dev receipt"
raw route-dev/route-1x1-check-shipping.log | grep -E '^(LUT|FF|SLICE|RAMB|DSP|WNS|WHS)'

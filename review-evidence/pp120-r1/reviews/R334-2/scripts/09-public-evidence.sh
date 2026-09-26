#!/usr/bin/env bash
# Read-only public evidence check: fetch kebag-logic/milan-fpga@356583ef
# review-evidence/pp120-r1 (author folders + MANIFEST.json; reviews/ is fetched
# only after the verdict, by 11-reviews-fetch.sh), verify hashes, compare the
# published round-3 patch with the exact delta, summarise gate/consumer results,
# and record exact-head hosted CI jobs/steps. No GitHub write.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); C=${CLONE:-$REVIEWS/r334-2-pp120}; D=$PK/scratch/evidence; mkdir -p $D; cd $D
REF=356583ef6ba0d99eec2b7a8d006664a47497d8bc; H=83c84b19e09d397ed2eb6f5ace337686ce0ef86b; R=Mister-M-alt/protocol-processor-control-plane-avb-milan
if [ ! -f review-evidence/pp120-r1/author-r3/head.txt ]; then
  gh api "repos/kebag-logic/milan-fpga/git/trees/$REF?recursive=1" --jq '.tree[] | select(.type=="blob" and (.path|startswith("review-evidence/pp120-r1"))) | "\(.sha) \(.path)"' > list.txt
  grep -v '/reviews/' list.txt > list-author.txt
  while read -r sha p; do mkdir -p "$(dirname "$p")"; gh api -H 'Accept: application/vnd.github.raw' "repos/kebag-logic/milan-fpga/git/blobs/$sha" > "$p"; done < list-author.txt
fi
cd review-evidence/pp120-r1
python3 - "$C" <<'P'
import json, hashlib, os, subprocess, sys
m = json.load(open("MANIFEST.json")); mine = [e for e in m if not e["file"].startswith("reviews/")]
bad = [e["file"] for e in mine if hashlib.sha256(open(e["file"], "rb").read()).hexdigest() != e["published_sha256"]]
print(f"MANIFEST.json {len(m)} entries; author/author-r2/author-r3 {len(mine)} verified, {len(bad)} mismatches; reviews/ {len(m) - len(mine)} deferred")
print("author-r3/head.txt:", open("author-r3/head.txt").read().strip())
d = subprocess.run(["git", "-C", sys.argv[1], "diff", "a9b7874d415d935949becd7ccfd58799927efb08", "83c84b19e09d397ed2eb6f5ace337686ce0ef86b"], capture_output=True, text=True).stdout
body = lambda t: [l for l in t.splitlines() if l[:1] in "+-@ " and not l.startswith(("+++", "---"))]
p = open("author-r3/round3.patch").read()
print(f"author-r3/round3.patch hunks == git diff a9b7874d..83c84b19 hunks: {body(p) == body(d)}")
for f in ("author-r3/gates/results.json", "author-r3/consumer/results.json", "author-r3/consumer/setup-incomplete-results.json", "author-r3/gates/shared-tally-attempt.json"):
    r = json.load(open(f)); r = r if isinstance(r, list) else [r]
    print(f"{f}: {len(r)} command(s), rc {[x['rc'] for x in r]}")
fs = json.load(open("author-r3/consumer/final-state.json"))
print("consumer final-state:", {k: fs[k] for k in ("parent_head", "processor_head", "patch_sha256", "consumer_commands_match_supplied_argv")}, "| parent status:", fs["parent_status"].replace("\n", "; "))
P
grep -h -E 'pp_shadow: .* checks|port contract gate|TEST-EVIDENCE RATCHET|GATE ARM|ALL GATES|LINT GATE' author-r3/consumer/0[678].log author-r3/consumer/1[02].log | cut -c1-230
grep -h -E '^suites:|^[0-9]+ checks: |^NW:' author-r3/gates/run-suites.log author-r3/gates/pp-top.log author-r3/gates/name-writes.log
echo "== hosted CI at $H (read-only)"
for id in $(gh api "repos/$R/actions/runs?head_sha=$H" --jq '.workflow_runs[].id'); do
  gh api "repos/$R/actions/runs/$id" --jq '"run \(.id) \(.name) \(.event) \(.status) \(.conclusion) head=\(.head_sha)"'
  gh api "repos/$R/actions/runs/$id/jobs" --jq '.jobs[] | "  job \(.name) \(.conclusion): " + ([.steps[] | "\(.name)=\(.conclusion)"] | join("; "))'
done

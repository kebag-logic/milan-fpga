#!/usr/bin/env bash
# Read-only: fetch the public evidence tree (milan-fpga 27f87160, review-evidence/pp120-r1)
# into scratch, verify its MANIFEST.json hashes, summarise the gate results; then record
# exact-head hosted CI jobs/steps. No GitHub write.
set -uo pipefail
PK=$(cd "$(dirname "$0")/.." && pwd); D=$PK/scratch/evidence; mkdir -p $D; cd $D
REF=27f87160de652b3bfcbb166bd154653b13e28642; H=a9b7874d415d935949becd7ccfd58799927efb08
R=Mister-M-alt/protocol-processor-control-plane-avb-milan
if [ ! -f review-evidence/pp120-r1/MANIFEST.json ]; then
  gh api "repos/kebag-logic/milan-fpga/git/trees/$REF?recursive=1" --jq '.tree[] | select(.type=="blob" and (.path|startswith("review-evidence/pp120-r1"))) | "\(.sha) \(.path)"' > list.txt
  while read -r sha p; do mkdir -p "$(dirname "$p")"; gh api -H 'Accept: application/vnd.github.raw' "repos/kebag-logic/milan-fpga/git/blobs/$sha" > "$p"; done < list.txt
fi
cd review-evidence/pp120-r1
python3 - <<'P'
import json, hashlib
m = json.load(open("MANIFEST.json"))
bad = [e["file"] for e in m if hashlib.sha256(open(e["file"], "rb").read()).hexdigest() != e["published_sha256"]]
print(f"evidence MANIFEST.json: {len(m)} entries, {len(bad)} hash mismatches, "
      f"{sum(e['path_redacted'] for e in m)} path-redacted; producers: "
      f"{sorted({e['file'].split('/')[0] for e in m})}")
for f in ("author-r2/repository-results.json", "author-r2/consumer/results.json"):
    r = json.load(open(f)); print(f"{f}: {len(r)} commands, rc set {sorted({x['rc'] for x in r})}")
print("author/area.json head:", json.load(open("author/area-inputs.json"))["head"])
P
grep -h -E 'undocumented|TEST-EVIDENCE RATCHET|checks, 0 failures|not run|calibration' ../../../evidence/review-evidence/pp120-r1/author-r2/consumer/0[678].log ../../../evidence/review-evidence/pp120-r1/author-r2/consumer/10.log 2>/dev/null | cut -c1-240 | head -12
echo "== hosted CI at $H (read-only)"
for id in $(gh api "repos/$R/actions/runs?head_sha=$H" --jq '.workflow_runs[].id'); do
  gh api "repos/$R/actions/runs/$id" --jq '"run \(.id) \(.name) \(.event) \(.status) \(.conclusion) head=\(.head_sha)"'
  gh api "repos/$R/actions/runs/$id/jobs" --jq '.jobs[] | "  job \(.name) \(.conclusion): " + ([.steps[] | "\(.name)=\(.conclusion)"] | join("; "))'
done

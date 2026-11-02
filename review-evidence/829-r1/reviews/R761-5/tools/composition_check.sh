#!/usr/bin/env bash
# Reproduce the composition checks of round R761-5 for PR #831 (#829).
# Usage: composition_check.sh <clone> <signed-packet-dir>
#   <clone>: a checkout at candidate 4871df3f6eed1cbc5a399e18372b60a04cb32387
#   <signed-packet-dir>: holds manifest.json, manifest.json.sig, allowed_signers
set -euo pipefail
repo=$1 pkt=$2
cand=4871df3f6eed1cbc5a399e18372b60a04cb32387
dev=503bc97cd4f24ad07596c17e7188f2024617972d
head=b9628c8963d436af0dccebb205a5241ece5d9e93
cd "$repo"
base=$(git merge-base "$dev" "$head")
echo "merge-base $base"
echo "candidate tree      $(git rev-parse "$cand^{tree}")"
echo "recomputed merge    $(git merge-tree --write-tree "$dev" "$head")"
echo "predecessors on dev since the PR base:"
git log --oneline --first-parent "$base..$dev"
echo "files changed by both:"
comm -12 <(git diff --name-only "$base" "$head" | sort) \
         <(git diff --name-only "$base" "$dev" | sort)
cd "$pkt"
ssh-keygen -lf <(awk '{print $3" "$4}' allowed_signers)
ssh-keygen -Y verify -f allowed_signers -I milan-local-ci -n milan-local-ci \
  -s manifest.json.sig < manifest.json
python3 -I - manifest.json "$cand" "$head" <<'EOF'
import json, sys
m = json.load(open(sys.argv[1]))
s, e = m["subject"], m["execution"]
assert s["candidate"] == sys.argv[2] and s["head"] == sys.argv[3], s
assert m["result"] == "success" and e["act"]["exit_code"] == 0
cov = e["coverage"]
assert all(v.get("ok") is True for v in cov.values())
jobs = e["act"]["jobs"]
for k, v in cov.items():
    if v["by"] == "act":
        for j in v.get("act_jobs", [v.get("act_job")]):
            assert jobs[j] == "success", (k, j)
    else:
        print("not-run:", k, "-", v["reason"])
assert all(b["exit_code"] == 0 and all(c["exit_code"] == 0 for c in b["commands"])
           for b in e["banks"].values())
print(f"coverage {len(cov)} entries ok; act jobs {len(jobs)}; banks {list(e['banks'])}")
EOF

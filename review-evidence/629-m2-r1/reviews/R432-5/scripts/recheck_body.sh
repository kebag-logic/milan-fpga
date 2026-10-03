#!/usr/bin/env bash
# R432-5 body-only re-check of PR #634 at head 2bc5adc0. Read-only GitHub API
# calls; writes into the directory given as $1 (default: current directory).
# Needs: gh (authenticated for reads), python3, diff, grep, sort, uniq.
set -euo pipefail
OUT=${1:-.}
REPO=kebag-logic/milan-fpga
EVID=a1ae6104a6ad9a744831a0512b01034d39a6ce26   # 629-m2-review-evidence tip read
P=review-evidence/629-m2-r1/author-r4b
cd "$OUT"

gh pr view 634 -R "$REPO" --json body,headRefOid \
  | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d["headRefOid"], file=sys.stderr); open("live-PR-BODY.md","w").write(d["body"])'
gh api "repos/$REPO/contents/$P/PR-BODY.md?ref=$EVID" \
  -H 'Accept: application/vnd.github.raw' > author-r4b-PR-BODY.md
gh api "repos/$REPO/contents/$P/receipts/campaigns/restart_controls_probe.log?ref=$EVID" \
  -H 'Accept: application/vnd.github.raw' > restart_controls_probe.log

# The body version R432-4 reviewed (edit of 07:53:19Z) and the live one.
gh api graphql -f query='{repository(owner:"kebag-logic",name:"milan-fpga"){pullRequest(number:634){userContentEdits(first:6){nodes{editedAt diff}}}}}' \
  | python3 -c '
import json,sys
n=json.load(sys.stdin)["data"]["repository"]["pullRequest"]["userContentEdits"]["nodes"]
v={e["editedAt"]:e["diff"] for e in n}
open("body-as-reviewed-R432-4.md","w").write(v["2026-10-03T07:53:19Z"])'

echo "== author r4b body vs body R432-4 reviewed (expect identical)"
cmp author-r4b-PR-BODY.md body-as-reviewed-R432-4.md && echo identical
echo "== body R432-4 reviewed vs live body"
diff body-as-reviewed-R432-4.md live-PR-BODY.md > body-R432-4-to-live.diff || true
cat body-R432-4-to-live.diff
echo "== receipt per-campaign rows"
grep -oE '^\[[^]]+\]' restart_controls_probe.log | sort | uniq -c
echo "== gsi anchors by file"
grep -A1 '^\[gsi\]' restart_controls_probe.log | grep -oE 'at [A-Za-z_]+\.sv' | sort | uniq -c
tail -n 1 restart_controls_probe.log

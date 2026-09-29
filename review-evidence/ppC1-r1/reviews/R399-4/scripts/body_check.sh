#!/usr/bin/env bash
# Read-only: fetch PR #133's body, its edit history and its closing references, then diff the
# body revision current during round 3 (edited 2026-09-29T09:58:59Z) against the live body.
# Needs an authenticated `gh` (GraphQL query only, no mutation). Usage: body_check.sh <out-dir>
set -uo pipefail
out=${1:?out dir}; mkdir -p "$out"
gh api graphql -f query='query{repository(owner:"Mister-M-alt",name:"protocol-processor-control-plane-avb-milan"){pullRequest(number:133){headRefOid body lastEditedAt closingIssuesReferences(first:20){nodes{number}} userContentEdits(first:50){nodes{createdAt editedAt diff}}}}}' > "$out/g.json"
jq -r '.data.repository.pullRequest | "head \(.headRefOid) lastEdited \(.lastEditedAt) closing \([.closingIssuesReferences.nodes[].number]|sort)"' "$out/g.json"
jq -j '.data.repository.pullRequest.body' "$out/g.json" > "$out/body-now.md"
jq -j '[.data.repository.pullRequest.userContentEdits.nodes[] | select(.createdAt=="2026-09-29T09:58:59Z" and .editedAt=="2026-09-29T09:58:59Z")][0].diff' "$out/g.json" > "$out/body-r3.md"
sha256sum "$out/body-r3.md" "$out/body-now.md"
echo "Closes lines:"; grep -nE '^Closes #' "$out/body-now.md"
diff "$out/body-r3.md" "$out/body-now.md"; echo "diff rc=$? (1 = differs; expect a pure append after the last round-3 line)"

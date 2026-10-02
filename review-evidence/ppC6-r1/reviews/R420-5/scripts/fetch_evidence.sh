#!/usr/bin/env bash
# Fetch the public evidence files this review compares, each at the evidence
# commits that matter, plus the live PR #139 body. Read-only (GitHub API GETs).
# usage: fetch_evidence.sh OUTDIR
set -euo pipefail
out=${1:?outdir}; mkdir -p "$out"
E=kebag-logic/milan-fpga
R=Mister-M-alt/protocol-processor-control-plane-avb-milan
B=review-evidence/ppC6-r1
get() { # path ref -> $out/<ref>/<path with / -> __>
  local p=$1 ref=$2 f
  f="$out/$ref/$(echo "$p" | sed 's#/#__#g')"
  mkdir -p "$out/$ref"
  if ! gh api -H 'Accept: application/vnd.github.raw' "repos/$E/contents/$B/$p?ref=$ref" > "$f" 2>/dev/null; then
    rm -f "$f"; echo "ABSENT  $ref:$B/$p"; return 0; fi
  echo "$(sha256sum "$f" | cut -d' ' -f1)  git-blob=$(git hash-object "$f")  $ref:$B/$p"
}
for ref in 72483b72 7d8194b5 ca502628 a6ea796e 2a98e7d4; do
  get author-r4/PR-BODY.md $ref
  get author-r4b/PR-BODY.md $ref
  get author-r4b/HANDOFF.md $ref
done
for ref in 8d04013c ca502628 2a98e7d4; do get author-r3/PR-BODY.md $ref; done
for ref in 7d8194b5 ca502628 a6ea796e 5d9d643e 2a98e7d4; do get MANIFEST.json $ref; done
gh api "repos/$R/pulls/139" --jq .body > "$out/live-body.md"
gh api "repos/$R/pulls/139" --jq '"head=\(.head.sha) updated_at=\(.updated_at) body_chars=\(.body|length)"'
echo "$(sha256sum "$out/live-body.md" | cut -d' ' -f1)  live PR #139 body (gh --jq .body, adds one trailing newline)"

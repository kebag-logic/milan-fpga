#!/bin/bash
# hosted_fetch.sh SHA OUT: list the Actions runs for SHA; for the rtl-full run save every job (with its steps) from the
# jobs API as OUT/jobs.json, and download every suite-logs-* and suite-union-* artifact into OUT/art/.
set -euo pipefail
SHA=$1; OUT=$2; REPO=kebag-logic/milan-fpga
mkdir -p "$OUT"
gh api "repos/$REPO/actions/runs?head_sha=$SHA&per_page=50" \
  --jq '.workflow_runs[] | [.id, .name, .event, .status, (.conclusion // "-"), .created_at, .updated_at] | @tsv' \
  > "$OUT/runs.tsv"
cat "$OUT/runs.tsv"
RUN=$(awk -F'\t' '$2 == "rtl-full" && $3 == "pull_request" {print $1; exit}' "$OUT/runs.tsv")
[ -n "$RUN" ] || { echo "no rtl-full pull_request run for $SHA" >&2; exit 2; }
echo "$RUN" > "$OUT/run-id"
gh api --paginate "repos/$REPO/actions/runs/$RUN/jobs?per_page=100&filter=latest" --jq '.jobs[]' \
  | python3 -c 'import json,sys; print(json.dumps({"jobs":[json.loads(l) for l in sys.stdin if l.strip()]}))' \
  > "$OUT/jobs.json"
python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); print(len(d["jobs"]), "jobs")' "$OUT/jobs.json"
if [ "${3:-}" = artifacts ]; then
  mkdir -p "$OUT/art"
  gh run download "$RUN" -R "$REPO" -p 'suite-logs-*' -D "$OUT/art"
  gh run download "$RUN" -R "$REPO" -p 'suite-union-*' -D "$OUT/unions" || true
  ls "$OUT/art" | wc -l
fi

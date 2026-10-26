#!/usr/bin/env bash
# Read-only: for every completed, non-skipped job of the hosted runs of one head, fetch the
# job log and record its runner image lines ("Image:" / "Version:" in "Set up job").
# Usage: hosted_images.sh <head-sha> <out-tsv>
set -u
repo=kebag-logic/milan-fpga head=$1 out=$2
: > "$out"
for run in $(gh api "repos/$repo/actions/runs?head_sha=$head&per_page=50" --jq '.workflow_runs[].id'); do
  gh api --paginate "repos/$repo/actions/runs/$run/jobs?per_page=100" \
    --jq '.jobs[] | [.id, .name, .status, (.conclusion // "-"), (.labels | join(","))] | @tsv' |
  while IFS=$'\t' read -r job name status conclusion labels; do
    image=- version=-
    if [ "$status" = completed ] && [ "$conclusion" != skipped ]; then
      log=$(gh api --allow-escape-sequences "repos/$repo/actions/jobs/$job/logs" 2>/dev/null | tr -cd '[:print:]\n\t' | head -n 60)
      image=$(printf '%s\n' "$log" | grep -m1 -oE 'Image: [^[:space:]]+' || echo none)
      version=$(printf '%s\n' "$log" | awk '/Image: /{getline; sub(/^[^ ]* /, ""); print; exit}')
      version=${version:-none}
    fi
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$run" "$job" "$name" "$status" "$conclusion" "$labels" "$image" "$version" >> "$out"
  done
done

#!/bin/bash
# Run the consumer's Python-idiom and test-evidence ratchets with gptp-processor moved, in a local commit
# only, to each given pin; budgets are the consumer base's own. usage: consumer_ratchets.sh CONSUMER BASE OUTDIR PIN...
set -u
C=$1; B=$2; O=$3; shift 3
mkdir -p "$O"; cd "$C" || exit 2
git checkout -q --detach "$B" && git submodule update -q -- protocol-processor || exit 2
for pin in "$@"; do
  git -C gptp-processor checkout -q --detach "$pin" || exit 2
  git add gptp-processor
  git -c user.name=reviewer -c user.email=reviewer@invalid commit -q --allow-empty -m "probe: gptp-processor at $pin"
  tag=$(git rev-parse --short=7 "$B")-$(git -C gptp-processor rev-parse --short=7 HEAD)
  {
    echo "consumer base $(git rev-parse "$B"), probe commit $(git rev-parse HEAD)"
    git submodule status -- protocol-processor gptp-processor
    echo "budget files vs consumer base: $(git diff --stat "$B" HEAD -- scripts/py_idiom.budget scripts/test_evidence.budget | tail -1)"
    echo "probe commit changes: $(git diff --name-only "$B" HEAD | tr '\n' ' ')"
    echo "== python3 scripts/check_py_idiom.py"; python3 scripts/check_py_idiom.py; echo "rc $?"
    echo "== python3 scripts/measure_test_evidence.py --check"; python3 scripts/measure_test_evidence.py --check; echo "rc $?"
  } > "$O/ratchets-$tag.log" 2>&1
  grep -E '^rc |budget files' "$O/ratchets-$tag.log" | sed "s/^/$tag: /"
done

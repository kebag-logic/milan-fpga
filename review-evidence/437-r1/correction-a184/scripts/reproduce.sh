#!/usr/bin/env bash
# Reproduce every A184 measurement, in order, against the lane at
# 4741498f3b2b4f67f431037d327c96cf65691278 (clean). Renderer steps reuse the
# cached receipts under work/ and receipts/ unless deleted; step 5 always
# renders fresh. At most 8 jobs run at once (gates.sh), 4 inside render.py,
# mutate.py and replay_a172_mutants.py.
set -eu
OUT=$MANAGEMENT/2026-09-23/437-a184
LANE=$LANES/437-container-paragraph-scopes
S=$OUT/scripts
cd "$LANE"
test "$(git rev-parse HEAD)" = 4741498f3b2b4f67f431037d327c96cf65691278
test -z "$(git status --porcelain=v1 --untracked-files=all)"

# 0. public inputs: the immutable R237-r1, R238-r1, A168 and A172 packets
if [ ! -d "$OUT/public-inputs/review-evidence/437-r1/correction-a172" ]; then
  mkdir -p "$OUT/public-inputs"
  for spec in "2e5eae85be76510b5d40bfdb6260bd4e573aa037 review-evidence/437-r1/reviews/R237-1" \
              "f39bf814fc13b5741b57191777455401babec1bf review-evidence/437-r1/reviews/R238-1" \
              "1dc9d95bbc9cb6cf48bb30ce59d0dc2b587a8c92 review-evidence/437-r1/author" \
              "9f5e84cee18b20ed7cb0b2c8cc5cd620370adc0d review-evidence/437-r1/correction-a172"; do
    set -- $spec
    git fetch -q origin "$1"
    git archive "$1" "$2" | tar -x -C "$OUT/public-inputs"
  done
fi

# 1. live-dev integration proof (merge commit a09ff881)
python3 -B $S/integration_proof.py b5e6c23e1b9802b5cacbc62db212064d7e429862 \
  483a133ed08867ea0d300d2b4a027b5b48a4282f a09ff881d31850e91866e301c846579173d7aa61 \
  > "$OUT/receipts/integration-proof.json"

# 2. shape inputs, 3. renderer receipts (cached)
python3 -B $S/build_shapes.py
python3 -B $S/render.py "$OUT/work/family-one-in.json" "$OUT/receipts/family-one-render.json"
python3 -B $S/render.py "$OUT/work/comment-in.json" "$OUT/receipts/comment-render.json"
python3 -B $S/render.py "$OUT/work/contract-in.json" "$OUT/receipts/contract-probes-1.json"
python3 -B $S/render.py "$OUT/work/contract2-in.json" "$OUT/receipts/contract-probes-2.json"

# 4. the committed fixtures equal what make_fixture.py writes from those receipts
cp "$OUT/receipts/family-one-render.json" "$OUT/work/family-one-out.json"
cp "$OUT/receipts/comment-render.json" "$OUT/work/comment-out.json"
python3 -B $S/make_fixture.py
test -z "$(git status --porcelain=v1 --untracked-files=all)"

# 5. fresh rendering of every fixture shape at this head
$S/rec.sh fixture-at-head python3 -B $S/verify_fixture_at_head.py "$OUT/receipts/fixture-at-head.json"

# 6. focused gates
$S/gates.sh

# 7. comparisons and mutations
$S/rec.sh named-regressions python3 -B $S/named_regressions.py "$OUT/receipts/named-render.json" "$OUT/receipts/named-regressions.json"
$S/rec.sh three-way python3 -B $S/three_way.py "$OUT/receipts/three-way.json" \
  "$OUT/receipts/contract-probes-1.json" "$OUT/receipts/contract-probes-2.json" \
  "$OUT/receipts/family-one-render.json" "$OUT/receipts/comment-render.json"
$S/rec.sh corpus-compare python3 -B $S/corpus_compare.py "$OUT/receipts/corpus-compare.json"
$S/rec.sh prior-arms python3 -B $S/prior_arms.py "$OUT/receipts/prior-arms.json"
$S/rec.sh mutations python3 -B $S/mutate.py "$OUT/receipts/mutations.json"
$S/rec.sh a172-mutants python3 -B $S/replay_a172_mutants.py "$OUT/receipts/a172-mutants.json"

# 8. final integrity
$S/rec.sh integrity python3 -B $S/integrity.py "$OUT/receipts/integrity.json"

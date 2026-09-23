#!/usr/bin/env bash
# R238-2 reproduction, in the order the round ran it.
#   CLONE  : a clean checkout of e4906bfca65c61e7e109e3532ac1b2dd5b4c0096
#   PACKET : this packet's root
# Every renderer call posts a synthetic page to GitHub's Markdown API (gfm mode).
# Walk revisions are extracted with `git archive` into $PACKET/scratch, which
# is disposable and never published.
set -eu
: "${CLONE:?}" "${PACKET:?}"
S=$PACKET/scratch
mkdir -p "$S/tmp"
export TMPDIR=$S/tmp
for rev in 88e9276b2a220c716f64a843f7e1eb8f9265e896:base \
           4741498f3b2b4f67f431037d327c96cf65691278:prev \
           e4906bfca65c61e7e109e3532ac1b2dd5b4c0096:head; do
  sha=${rev%%:*}; name=${rev##*:}
  rm -rf "$S/walk_$name"; mkdir -p "$S/walk_$name"
  git -C "$CLONE" archive "$sha" scripts | tar -x -C "$S/walk_$name"
done
cd "$PACKET"
# 1. focused gates at the exact head
scripts/run_gates.sh "$CLONE" receipts
# 2. acceptance 4: tracked-page classification, base walk vs head walk, three trees
for rev in 88e9276b2a220c716f64a843f7e1eb8f9265e896 574c29fa111c74e5e5ed63e4670aff1f492e28e2 \
           e4906bfca65c61e7e109e3532ac1b2dd5b4c0096; do
  python3 -B scripts/corpus_compare.py "$CLONE" "$rev" "$S/walk_base" "$S/walk_head" \
    "receipts/ac4_${rev:0:8}_base_vs_head.json"
done
# 3. named probes (fresh renders) at base, previous head and this head
(cd probes && for b in batch1 batch2 batch4_prior batch5_family_two; do
  python3 -B ../scripts/probe.py $b.json $b.jsonl base=$S/walk_base prev=$S/walk_prev head=$S/walk_head
done)
# 4. seeded differential sweeps and the container matrix (render only where base and head differ)
python3 -B scripts/fuzz_diff.py 238 40000 1200 "$S/walk_base" "$S/walk_head" "$S/fuzz_seed238.jsonl" 3
python3 -B scripts/rerender_failed.py "$S/fuzz_seed238.jsonl" probes/fuzz_seed238_complete.jsonl
FUZZ_MODE=no35 python3 -B scripts/fuzz_diff.py 4372 60000 1500 "$S/walk_base" "$S/walk_head" \
  "$S/fuzz_seed4372_no35.jsonl" 3
python3 -B scripts/rerender_failed.py "$S/fuzz_seed4372_no35.jsonl" probes/fuzz_seed4372_no35_complete.jsonl
python3 -B scripts/matrix_diff.py "$S/walk_base" "$S/walk_head" probes/matrix_base_vs_head.jsonl 3
# 5. end-to-end em-dash provenance and navigation at base and head
for w in base head; do
  python3 -B scripts/emdash_probe.py "$S/walk_$w" probes/emdash_cases.json "$S/tmp" > receipts/emdash_probe_$w.jsonl
  python3 -B scripts/emdash_probe.py "$S/walk_$w" probes/emdash_cases2.json "$S/tmp"
  python3 -B scripts/emdash_probe.py "$S/walk_$w" probes/emdash_cases3.json "$S/tmp"
done
# 6. committed fixtures: exact recorded request bytes re-sent, walk against each recording
rm -f receipts/fixtures_rerender_head.jsonl
python3 -B scripts/rerender_fixtures.py "$CLONE" "$S/walk_head" receipts/fixtures_rerender_head.jsonl 0 81
python3 -B scripts/rerender_fixtures.py "$CLONE" "$S/walk_head" receipts/fixtures_rerender_head.jsonl 81 162
# 7. mutations (disposable copies only), then the surviving ones against fresh renders
python3 -B scripts/mutate.py "$S/walk_head" "$S" receipts/mutations_r238.json 8
python3 -B scripts/mutate_prior.py "$S/walk_head" "$S" receipts/mutations_prior_r238.json 8
for m in C17 H06 H10; do python3 -B scripts/make_mutant.py "$S/walk_head" "$S/mutant_$m" $m; done
(cd probes && python3 -B ../scripts/probe.py batch3.json batch3.jsonl base=$S/walk_base head=$S/walk_head \
   C17=$S/mutant_C17 H06=$S/mutant_H06 H10=$S/mutant_H10)
# 8. timing and final review-checkout integrity
python3 -B scripts/timing_probe.py "$S/walk_head"
python3 -B scripts/integrity.py "$CLONE" e4906bfca65c61e7e109e3532ac1b2dd5b4c0096 \
  f5d2e8c022d39684f458f7d2d0ee97b350533353 receipts/integrity_final.json
python3 -B scripts/fixture_base_check.py "$CLONE" "$S" > receipts/fixture_base_check.txt

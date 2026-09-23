#!/usr/bin/env bash
# reproduce.sh: every A190 measurement, in order, against the lane's clean HEAD.
# Renders only pages missing from work/render-cache.jsonl, and only synthetic
# pages; verify_fixtures.py always renders the 162 fixture shapes fresh.
set -euo pipefail
P=$REVIEWS/437-a190-packet
cd "$P"
scripts/fetch_inputs.sh                                   # public review evidence -> inputs/
python3 -B scripts/harvest.py inputs work/public-cache.json
python3 -B inputs/review-evidence/437-r1/reviews/R237-2/scripts/gen_corpus.py > work/r237-2-corpus.json
for n in containers comments prose fuzz fuzz2 tabs; do
    python3 -B scripts/gen_probes.py $n > work/probe-$n.json
done
for n in r237-2-corpus probe-containers probe-comments probe-prose probe-fuzz probe-fuzz2 probe-tabs probe-rules probe-residue; do
    CAND=prod:headings python3 -B scripts/sweep.py need work/$n.json > /tmp/a190-need.json
    python3 -B scripts/render.py work/render-cache.jsonl /tmp/a190-need.json
done
rm -f receipts/exits.tsv
scripts/gates.sh
R=scripts/rec.sh
$R ac4-corpus python3 -B $P/scripts/corpus_ac4.py $P/receipts/ac4-corpus.json \
    88e9276b2a220c716f64a843f7e1eb8f9265e896 574c29fa111c74e5e5ed63e4670aff1f492e28e2 HEAD
$R prior-arms python3 -B $P/scripts/prior_arms.py $P/receipts/prior-arms.json
$R r237-2-findings python3 -B $P/scripts/r237_2_findings.py $P/receipts/r237-2-findings.json
$R emdash-probe-base python3 -B $P/scripts/emdash_probe_walk.py --repo $LANES/437-container-paragraph-scopes --rev 483a133ed08867ea0d300d2b4a027b5b48a4282f
$R emdash-probe-head python3 -B $P/scripts/emdash_probe_walk.py --repo $LANES/437-container-paragraph-scopes --rev HEAD
$R final-sweep python3 -B $P/scripts/final_sweep.py $P/receipts/final-sweep.json
$R mutations python3 -B $P/scripts/mutate.py HEAD $P/receipts/mutations.json
$R fixtures-at-head python3 -B $P/scripts/verify_fixtures.py $P/receipts/fixtures-at-head.json
$R integrity python3 -B $P/scripts/integrity.py $P/receipts/integrity.json

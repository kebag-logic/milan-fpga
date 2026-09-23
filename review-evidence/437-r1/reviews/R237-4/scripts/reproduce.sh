#!/usr/bin/env bash
# Reproduce round R237-4 of #437 / PR #515 from this packet.
#
# Usage: scripts/reproduce.sh <clone>
#   <clone>  a clone of kebag-logic/milan-fpga holding commits 34f124f9,
#            e4906bfc and ede8d48e (and 88e9276b for acceptance 4), with the
#            three required submodules initialised for the integrity check.
# Renders are served from receipts/render-cache when present (exact request
# and response bytes, named by the request's SHA-256); a missing page is
# sent to GitHub's Markdown API (gfm mode) as synthetic text only.
set -euo pipefail
clone=$(cd "$1" && pwd)
packet=$(cd "$(dirname "$0")/.." && pwd)
head=34f124f9b0dabeb74c655052f0a0858620a09037
tree=bb9b3dbc70a81af453f47c4c72aeb8433d927d91
prev=e4906bfca65c61e7e109e3532ac1b2dd5b4c0096
base=ede8d48ecd7c7f589a14b957951f040d92c99c70
orig=88e9276b2a220c716f64a843f7e1eb8f9265e896
evidence=ccc7b2b199469035ccea5e534584e691b59c1234
s="$packet/scratch"
r="$packet/receipts"
mkdir -p "$s" "$r"/{gates,triage,probes,mutation,prior}
for rev in base prev head; do
  rm -rf "${s:?}/$rev" && mkdir -p "$s/$rev"
  git -C "$clone" archive "${!rev}" scripts | tar -x -C "$s/$rev"
done

# Focused gates, run in the clone at the exact head (python3 -B: no bytecode).
[ "$(git -C "$clone" rev-parse HEAD)" = "$head" ] || { echo "clone is not at $head" >&2; exit 2; }
(cd "$clone" && for c in "gen_toc.py --selftest" "gen_toc.py --check" "gen_toc.py --verify-anchors" \
    "gen_toc.py --sites" "check_em_dash.py --selftest" "check_em_dash.py --base $base" "docs_check.py" \
    "docs_check.py --selftest" "check_doc_style.py" "check_doc_style.py --selftest" "check_doc_paths.py" \
    "check_py_idiom.py" "check_py_idiom.py --selftest" "check_hygiene.py --check" "check_todo_ownership.py" \
    "measure_naming.py --check" "measure_fail_fast.py --check" "measure_test_evidence.py --check" \
    "measure_control_flow.py --selftest" "measure_cohesion.py --selftest" "check_feature_status.py"; do
  set +e; python3 -B scripts/$c > "$r/gates/$(echo "$c" | tr ' ./-' '____').out" 2>&1; echo "$c exit=$?"; set -e
done; git diff --check "$base" "$head" && echo "git diff --check exit=0")

cd "$packet"
python3 -B scripts/fixture_triage.py "$s/head/scripts" "$s/base/scripts" "$r/triage/fixture_triage.json"
python3 -B scripts/rerender_fixtures.py "$s/head/scripts" "$r/render-cache" "$r/triage/rerender_fixtures.json"
python3 -B scripts/ac4_compare.py "$clone" "$s/head/scripts" "$s/base/scripts" "$head" "$base" "$orig"
python3 -B scripts/probe_corpus.py > "$r/probes/corpus1.json"
python3 -B scripts/probe_corpus2.py > "$r/probes/corpus2.json"
python3 -B scripts/probe_corpus3.py > "$r/probes/corpus3.json"
python3 -B scripts/probe_run.py "$r/probes/corpus1.json" "$s/head/scripts" "$s/base/scripts" "$r/render-cache" "$r/probes/run1.json" 20
python3 -B scripts/probe_run.py "$r/probes/corpus2.json" "$s/head/scripts" "$s/base/scripts" "$r/render-cache" "$r/probes/run2.json" 1
python3 -B scripts/probe_run.py "$r/probes/corpus3.json" "$s/head/scripts" "$s/base/scripts" "$r/render-cache" "$r/probes/run3.json" 6
python3 -B scripts/emdash_e2e.py "$s/base/scripts"
python3 -B scripts/emdash_e2e.py "$s/head/scripts"
python3 -B scripts/mutate.py "$s/head/scripts" "$s/mut" "$r/mutation/mutants.json"
python3 -B scripts/mutate_rounds.py "$s/head/scripts" "$s" "$r/mutation" "$r/render-cache" \
  "$r/probes/corpus1.json" "$r/probes/corpus2.json" "$r/probes/corpus3.json"
python3 -B scripts/crash_fuzz.py "$s/head/scripts" 60000 437

# Prior rounds' public receipts, fetched read-only from the evidence commit.
ev="$s/evidence"
for f in reviews/R237-3/receipts/pages/minimal.json reviews/R237-3/receipts/pages/minimal2.json \
    reviews/R237-3/receipts/minimal.rendered.json reviews/R237-3/receipts/minimal2.rendered.json \
    reviews/R237-3/receipts/pages/fuzz_full_sample.json reviews/R237-3/receipts/pages/fuzz_core_sample.json \
    reviews/R237-3/receipts/fuzz1.json reviews/R237-3/receipts/fuzz_core.json \
    reviews/R238-2/probes/batch1.jsonl reviews/R238-2/probes/batch2.jsonl reviews/R238-2/probes/batch3.jsonl \
    reviews/R238-2/probes/batch4_prior.jsonl reviews/R238-2/probes/fuzz_seed238_complete.jsonl \
    reviews/R238-2/probes/matrix_base_vs_head.jsonl reviews/R238-2/probes/fuzz_seed4372_no35_complete.jsonl \
    reviews/R237-2/receipts/comment-rule-render.json reviews/R237-2/receipts/regression-seed-render.json \
    reviews/R237-2/receipts/combinatorial-render.json; do
  mkdir -p "$ev/$(dirname "$f")"
  gh api -H "Accept: application/vnd.github.raw" \
    "repos/kebag-logic/milan-fpga/contents/review-evidence/437-r1/$f?ref=$evidence" > "$ev/$f"
done
python3 -B scripts/replay_prior.py "$ev" "$s/base/scripts" "$s/prev/scripts" "$s/head/scripts" "$r/prior/replay_prior.json"
python3 -B scripts/integrity.py "$clone" "$head" "$tree" > "$r/integrity-final.json"

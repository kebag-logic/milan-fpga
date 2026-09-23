# [A184] Commands and exits

Every command below ran in the lane `$LANES/437-container-paragraph-scopes`.
Rows from `receipts/exits.tsv`: receipt name, exit code, HEAD at run time, UTC start, and argv.
Each log is `receipts/<name>.log`. `scripts/rec.sh` wrote every row, and `scripts/gates.sh` ran the 33 focused gates, at most 8 at once.

## Before the fix commit (no rec.sh row)

| Step | Command | Result |
|---|---|---|
| Integration proof, before merge | `scripts/integration_proof.py HEAD 483a133e <merge-tree>` | `receipts/integration-proof-pre.json`: intersection empty, patches identical |
| Merge | `git merge --no-ff 483a133e` | commit `a09ff881`, tree `0e9e503d` |
| Integration proof, after merge | `scripts/integration_proof.py b5e6c23e 483a133e HEAD` | `receipts/integration-proof.json`: same hashes |
| Contract probes | `scripts/render.py work/contract-in.json ...`, `work/contract2-in.json` | 26 + 16 renders, exit 0, request length = wire Content-Length for all |
| Shape inputs | `scripts/build_shapes.py` | 51 family-one shapes, 40 comment controls |
| Shape renders | `scripts/render.py work/family-one-in.json ...`, `work/comment-in.json` | 51 + 40 renders, exit 0, length checks pass |
| Fixtures | `scripts/make_fixture.py` | writes the two committed JSON fixtures from those receipts |

## At head 4741498f (rec.sh rows)

| Name | Exit | Head | UTC | Command |
|---|---:|---|---|---|
| fixture-at-head | 0 | `4741498f3b2b` | 2026-09-23T04:44:18Z | `python3 -B $OUT/scripts/verify_fixture_at_head.py $OUT/receipts/fixture-at-head.json` |
| toc-sites | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/gen_toc.py --sites` |
| toc-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/gen_toc.py --selftest` |
| docs-check-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/docs_check.py --selftest` |
| doc-style-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_doc_style.py --selftest` |
| doc-style | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_doc_style.py` |
| doc-paths | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_doc_paths.py` |
| toc-check | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/gen_toc.py --check` |
| toc-anchors | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/gen_toc.py --verify-anchors` |
| hygiene | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_hygiene.py --check` |
| hygiene-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_hygiene.py --selftest` |
| naming | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/measure_naming.py --check` |
| naming-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/measure_naming.py --selftest` |
| fail-fast | 0 | `4741498f3b2b` | 2026-09-23T04:45:01Z | `python3 -B scripts/measure_fail_fast.py --check` |
| fail-fast-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:01Z | `python3 -B scripts/measure_fail_fast.py --selftest` |
| py-idiom | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_py_idiom.py` |
| py-idiom-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_py_idiom.py --selftest` |
| emdash-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_em_dash.py --selftest` |
| control-flow-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/measure_control_flow.py --selftest` |
| emdash-base-mergebase | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| cohesion-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/measure_cohesion.py --selftest` |
| emdash-base-original | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896` |
| ci-events | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/ci_events.py --check` |
| solution-docs | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_solution_docs.py` |
| docs-check | 0 | `4741498f3b2b` | 2026-09-23T04:45:00Z | `python3 -B scripts/docs_check.py` |
| feature-status | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_feature_status.py` |
| gptp-docs | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_gptp_docs.py` |
| submodule-docs | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_submodule_docs.py` |
| archive | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_archive.py` |
| todo-ownership | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_todo_ownership.py` |
| todo-ownership-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/check_todo_ownership.py --selftest` |
| test-evidence | 0 | `4741498f3b2b` | 2026-09-23T04:45:02Z | `python3 -B scripts/measure_test_evidence.py --check` |
| test-evidence-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:02Z | `python3 -B scripts/measure_test_evidence.py --selftest` |
| ci-events-selftest | 0 | `4741498f3b2b` | 2026-09-23T04:45:03Z | `python3 -B scripts/ci_events.py --selftest` |
| named-regressions | 0 | `4741498f3b2b` | 2026-09-23T04:46:00Z | `python3 -B $OUT/scripts/named_regressions.py $OUT/receipts/named-render.json $OUT/receipts/named-regressions.json` |
| three-way | 0 | `4741498f3b2b` | 2026-09-23T04:46:22Z | `python3 -B $OUT/scripts/three_way.py $OUT/receipts/three-way.json $OUT/receipts/contract-probes-1.json $OUT/receipts/contract-probes-2.json $OUT/receipts/family-one-render.json $OUT/receipts/comment-render.json` |
| prior-arms | 0 | `4741498f3b2b` | 2026-09-23T04:46:22Z | `python3 -B $OUT/scripts/prior_arms.py $OUT/receipts/prior-arms.json` |
| corpus-compare | 0 | `4741498f3b2b` | 2026-09-23T04:46:22Z | `python3 -B $OUT/scripts/corpus_compare.py $OUT/receipts/corpus-compare.json` |
| mutations | 0 | `4741498f3b2b` | 2026-09-23T04:46:31Z | `python3 -B $OUT/scripts/mutate.py $OUT/receipts/mutations.json` |
| a172-mutants | 0 | `4741498f3b2b` | 2026-09-23T04:46:47Z | `python3 -B $OUT/scripts/replay_a172_mutants.py $OUT/receipts/a172-mutants.json` |
| integrity | 1 | `4741498f3b2b` | 2026-09-23T04:47:28Z | `python3 -B $OUT/scripts/integrity.py $OUT/receipts/integrity.json` |
| integrity | 0 | `4741498f3b2b` | 2026-09-23T04:47:34Z | `python3 -B $OUT/scripts/integrity.py $OUT/receipts/integrity.json` |

The first `integrity` row (exit 1) came from a harness bug: it counted merged dev commits as author commits.
The script was corrected, and the second row (exit 0) is the result. Its log replaced the first.

## Reproduce

`scripts/reproduce.sh` reruns every step in order against the clean head.
Renderer steps reuse cached receipts; `fixture-at-head` always renders fresh.

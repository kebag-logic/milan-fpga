# [A190] Commands and exits

Every command ran in the lane `$LANES/437-container-paragraph-scopes` at the head shown, through `scripts/rec.sh`,
which keeps `receipts/<name>.log` and one `receipts/exits.tsv` row (name, exit, HEAD, UTC start, argv).
`scripts/gates.sh` runs the focused gates in sequence; `scripts/reproduce.sh` reruns everything in order.
Scripts under `$PACKET/scripts` are this packet's; paths are shown relative to it.

## Before the fix commit

| Step | Command | Result |
|---|---|---|
| Integration proof | `git merge-tree --write-tree HEAD 574c29fa`, then `git diff --binary` before and after | `receipts/integration-proof.json`: intersection empty, patch SHA-256 `1bd01330…fb9b` identical |
| Merge | `git merge --no-ff 574c29fa` | commit `ef39ecc4`, tree `6fdccfce` (equal to the precomputed tree) |
| Public renderings | `scripts/harvest.py inputs work/public-cache.json` | 1,367 unique pages, no conflicting heading lists |
| Corpora | `gen_corpus.py` (R237-2's), `scripts/gen_probes.py containers/comments/prose/fuzz/fuzz2/tabs` | `work/*.json` |
| Renders | `scripts/render.py work/render-cache.jsonl <pages>` for every page where the walks differ | 4,205 rows, all exit 0 |
| Fixture | `scripts/make_walk_fixture.py scripts/gen_toc_container_walk.json receipts/walk-fixture-render.jsonl` | 71 shapes |

## At head `e4906bfc`

| Name | Exit | Head | UTC | Command |
|---|---:|---|---|---|
| toc-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:30:52Z | `python3 -B scripts/gen_toc.py --selftest` |
| toc-check | 0 | `e4906bfca65c` | 2026-09-23T08:30:52Z | `python3 -B scripts/gen_toc.py --check` |
| toc-anchors | 0 | `e4906bfca65c` | 2026-09-23T08:30:53Z | `python3 -B scripts/gen_toc.py --verify-anchors` |
| toc-sites | 0 | `e4906bfca65c` | 2026-09-23T08:30:54Z | `python3 -B scripts/gen_toc.py --sites` |
| emdash-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:30:54Z | `python3 -B scripts/check_em_dash.py --selftest` |
| emdash-base-mergebase | 0 | `e4906bfca65c` | 2026-09-23T08:30:58Z | `python3 -B scripts/check_em_dash.py --base 574c29fa111c74e5e5ed63e4670aff1f492e28e2` |
| emdash-base-483a133e | 0 | `e4906bfca65c` | 2026-09-23T08:31:01Z | `python3 -B scripts/check_em_dash.py --base 483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| emdash-base-88e9276b | 0 | `e4906bfca65c` | 2026-09-23T08:31:04Z | `python3 -B scripts/check_em_dash.py --base 88e9276b2a220c716f64a843f7e1eb8f9265e896` |
| docs-check | 0 | `e4906bfca65c` | 2026-09-23T08:31:08Z | `python3 -B scripts/docs_check.py` |
| docs-check-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:11Z | `python3 -B scripts/docs_check.py --selftest` |
| doc-style | 0 | `e4906bfca65c` | 2026-09-23T08:31:11Z | `python3 -B scripts/check_doc_style.py` |
| doc-style-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:12Z | `python3 -B scripts/check_doc_style.py --selftest` |
| doc-paths | 0 | `e4906bfca65c` | 2026-09-23T08:31:12Z | `python3 -B scripts/check_doc_paths.py` |
| py-idiom | 0 | `e4906bfca65c` | 2026-09-23T08:31:12Z | `python3 -B scripts/check_py_idiom.py` |
| py-idiom-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:15Z | `python3 -B scripts/check_py_idiom.py --selftest` |
| hygiene | 0 | `e4906bfca65c` | 2026-09-23T08:31:17Z | `python3 -B scripts/check_hygiene.py --check` |
| hygiene-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:18Z | `python3 -B scripts/check_hygiene.py --selftest` |
| naming | 0 | `e4906bfca65c` | 2026-09-23T08:31:18Z | `python3 -B scripts/measure_naming.py --check` |
| fail-fast | 0 | `e4906bfca65c` | 2026-09-23T08:31:18Z | `python3 -B scripts/measure_fail_fast.py --check` |
| test-evidence | 0 | `e4906bfca65c` | 2026-09-23T08:31:20Z | `python3 -B scripts/measure_test_evidence.py --check` |
| cohesion-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:24Z | `python3 -B scripts/measure_cohesion.py --selftest` |
| control-flow-selftest | 0 | `e4906bfca65c` | 2026-09-23T08:31:25Z | `python3 -B scripts/measure_control_flow.py --selftest` |
| todo-ownership | 0 | `e4906bfca65c` | 2026-09-23T08:31:25Z | `python3 -B scripts/check_todo_ownership.py` |
| feature-status | 0 | `e4906bfca65c` | 2026-09-23T08:31:26Z | `python3 -B scripts/check_feature_status.py` |
| diff-check-branch | 0 | `e4906bfca65c` | 2026-09-23T08:31:26Z | `git diff --check 574c29fa111c74e5e5ed63e4670aff1f492e28e2 HEAD` |
| diff-check-worktree | 0 | `e4906bfca65c` | 2026-09-23T08:31:26Z | `git diff --check` |
| status | 0 | `e4906bfca65c` | 2026-09-23T08:31:26Z | `git status --porcelain=v1 --untracked-files=all` |
| ac4-corpus | 0 | `e4906bfca65c` | 2026-09-23T08:31:34Z | `python3 -B scripts/corpus_ac4.py receipts/ac4-corpus.json 88e9276b2a220c716f64a843f7e1eb8f9265e896 574c29fa111c74e5e5ed63e4670aff1f492e28e2 HEAD` |
| prior-arms | 0 | `e4906bfca65c` | 2026-09-23T08:31:46Z | `python3 -B scripts/prior_arms.py receipts/prior-arms.json` |
| r237-2-findings | 0 | `e4906bfca65c` | 2026-09-23T08:31:46Z | `python3 -B scripts/r237_2_findings.py receipts/r237-2-findings.json` |
| emdash-probe-base | 0 | `e4906bfca65c` | 2026-09-23T08:31:46Z | `python3 -B scripts/emdash_probe_walk.py --repo $LANE --rev 483a133ed08867ea0d300d2b4a027b5b48a4282f` |
| emdash-probe-head | 0 | `e4906bfca65c` | 2026-09-23T08:31:47Z | `python3 -B scripts/emdash_probe_walk.py --repo $LANE --rev HEAD` |
| final-sweep | 0 | `e4906bfca65c` | 2026-09-23T08:31:47Z | `python3 -B scripts/final_sweep.py receipts/final-sweep.json` |
| fixtures-at-head | 0 | `e4906bfca65c` | 2026-09-23T08:33:52Z | `python3 -B scripts/verify_fixtures.py receipts/fixtures-at-head.json` |
| integrity | 0 | `e4906bfca65c` | 2026-09-23T08:35:15Z | `python3 -B scripts/integrity.py receipts/integrity.json` |
| mutations | 0 | `e4906bfca65c` | 2026-09-23T08:35:47Z | `python3 -B scripts/mutate.py HEAD receipts/mutations.json` |

36 commands, every exit 0.

[A552]

## Contents

- [Status](#status): local validation and branch.
- [Linked Issue / roles](#linked-issue--roles): assignment and reviewers.
- [Description](#description): limits and measured envelopes.
- [Authoritative references](#authoritative-references): governing contract.
- [How to get into the same state](#how-to-get-into-the-same-state): checkout and dependencies.
- [How to validate](#how-to-validate): commands and expected outcomes.
- [Known limitations / out of scope](#known-limitations--out-of-scope): follow-up and pending integration.
- [Definition of Done](#definition-of-done): completion ledger.

## Status

REVIEW READY: round-2 documentation corrections for R516-F1/F2 are committed. Documentation, contents, anchors, em-dash, path, style and archive gates all return rc 0 at the candidate head. R517-1 was POSITIVE at `26bd6334`; R516-1 requires Docs re-review after this correction. The round-1 builder declared one calibration arm NOT RUN because its report was absent.

`673-mclk-timeout` -> `dev`; candidate head `793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df`, base `bd884631684ccf5060339efa92263d5c3e5c262c`. Published as PR #681 for independent review.

## Linked Issue / roles

Closes #673

Executor: [A552]
Internal cleared-context reviewer: [R516]
External reviewer: [R517]

## Description

Slow hosted runners cut healthy suites at their wall-clock limit. Increase `capture_coherence` to 2400 s, `milan_dp_mclk` to 3600 s and `milan_dp` to 4800 s. Mirror the limits and their mutation cases in the evidence checker. Record the measured basis in the CI policy. The testing guides and suite READMEs now link to that policy table and the #673 ruling. The run guide records the current 60-suite default selection. Timeout results remain UNKNOWN with exit 92, and caller overrides retain their meaning.

| Suite | Measured maximum | Old limit | Usage | Applied / proposed limit | Maximum source |
|---|---|---|---|---|---|
| `capture_coherence` | 1642.280 s PASS | 1800 s | 91.24% | increase to 2400 s | [37429204551 / 112155955445](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955445) |
| `milan_dp` | 3509.562 s PASS | 3600 s | 97.49% | increase to 4800 s | [37424768281 / 112142195163](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195163) |
| `milan_dp_gptp` | 5400.003 s TIMEOUT | 5400 s | 100.00% | retain 5400 s; follow-up | [37430728685 / 112160880673](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880673) |
| `milan_dp_mclk` | 1800.008 s TIMEOUT | 1800 s | 100.00% | increase to 3600 s | [37430728685 / 112160880744](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880744) |
| `milan_dp_render` | 1285.710 s PASS | 1800 s | 71.43% | retain 1800 s | [37429204551 / 112155955318](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955318) |
| `mmcm_servo` | 1147.315 s PASS | 1800 s | 63.74% | retain 1800 s | [37430728685 / 112160880744](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685/job/112160880744) |
| `pp_shadow` | 1201.263 s PASS | 1800 s | 66.74% | retain 1800 s | [37424768281 / 112142195196](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195196) |

Latest-ten-run observations for every changed suite:

| Run | capture_coherence | milan_dp_mclk | milan_dp |
|---|---|---|---|
| [37457223191](https://github.com/kebag-logic/milan-fpga/actions/runs/37457223191) | no completed window available | no completed window available | no completed window available |
| [37455131093](https://github.com/kebag-logic/milan-fpga/actions/runs/37455131093) | no completed window available | 642.002 s PASS (job 112240922212) | 2282.219 s PASS (job 112240922168) |
| [37453634481](https://github.com/kebag-logic/milan-fpga/actions/runs/37453634481) | no completed window available | no completed window available | no completed window available |
| [37445962113](https://github.com/kebag-logic/milan-fpga/actions/runs/37445962113) | 1580.682 s PASS (job 112210929411) | 1012.424 s PASS (job 112210929579) | 3393.460 s PASS (job 112210929473) |
| [37439568024](https://github.com/kebag-logic/milan-fpga/actions/runs/37439568024) | 881.088 s PASS (job 112189866132) | 780.518 s PASS (job 112189866168) | 2324.670 s PASS (job 112189866083) |
| [37432004413](https://github.com/kebag-logic/milan-fpga/actions/runs/37432004413) | suite jobs skipped | suite jobs skipped | suite jobs skipped |
| [37430728685](https://github.com/kebag-logic/milan-fpga/actions/runs/37430728685) | 839.194 s PASS (job 112160880721) | 1800.008 s TIMEOUT (job 112160880744) | 2121.671 s PASS (job 112160880630) |
| [37429204551](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551) | 1642.280 s PASS (job 112155955445) | 1800.005 s TIMEOUT (job 112155955407) | 2340.774 s PASS (job 112155955400) |
| [37424768281](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281) | 1613.483 s PASS (job 112142195196) | 1084.530 s PASS (job 112142195210) | 3509.562 s PASS (job 112142195163) |
| [37420502040](https://github.com/kebag-logic/milan-fpga/actions/runs/37420502040) | 1606.127 s PASS (job 112128698286) | no completed window available | no completed window available |

The round-1 survey uses the ten latest `rtl.yml` run IDs when it was frozen; round 2 preserves that measurement window. Refreshing their available logs produced 39 downloaded job logs, 38 with suite verdict windows, and 425 completed verdict windows. Seven active-job requests returned HTTP 404; run 37432004413 skipped the suite jobs. Cancelled jobs contribute only completed windows, never invented completion times. Two cancelled jobs have partial suite inventories; only the 36 complete job inventories contribute overhead maxima.

For each log, the first window begins at `shard: INDEX/TOTAL`; later windows begin at the preceding PASS/FAIL/TIMEOUT line. Each ends at its suite verdict timestamp. This includes intervening tally/loop overhead. Raw timestamps are used before rounding to milliseconds. TIMEOUT means UNKNOWN and is a lower bound on required completion time, not a passing maximum.

For each shard, sum the new limits of changed suites, the independently largest observed windows of every other suite, and that shard's largest measured job overhead. Overhead is `completed_at - started_at - sum(suite windows)` for complete jobs; it includes setup, preflights, final tally, upload and cleanup. The acceptance ceiling is 6480 s (90% of 7200 s). Shards 1/5, 2/5 and 4/5 all fit; no requested limit is trimmed. Shards 0/5 and 3/5 are shown for completeness. These are measured envelopes, not guarantees about future runner slowdown or cache misses.

| Shard | Changed limits sum | Other suite maxima sum | Maximum job overhead | Envelope | Headroom / 7200 s | Overhead source |
|---|---|---|---|---|---|---|
| 0/5 | 0 s | 1453.974 s | 85.911 s | 1539.885 s | 5660.115 s / 78.61% | [37429204551 / 112155955318](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955318) |
| 1/5 | 2400 s | 3381.779 s | 117.580 s | 5899.359 s | 1300.641 s / 18.06% | [37424768281 / 112142195196](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195196) |
| 2/5 | 3600 s | 2517.453 s | 86.448 s | 6203.901 s | 996.099 s / 13.83% | [37429204551 / 112155955407](https://github.com/kebag-logic/milan-fpga/actions/runs/37429204551/job/112155955407) |
| 3/5 | 0 s | 552.155 s | 106.537 s | 658.692 s | 6541.308 s / 90.85% | [37439568024 / 112189866162](https://github.com/kebag-logic/milan-fpga/actions/runs/37439568024/job/112189866162) |
| 4/5 | 4800 s | 0.000 s | 89.438 s | 4889.438 s | 2310.562 s / 32.09% | [37424768281 / 112142195163](https://github.com/kebag-logic/milan-fpga/actions/runs/37424768281/job/112142195163) |

## Authoritative references

- [Issue #673](https://github.com/kebag-logic/milan-fpga/issues/673), [assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015580138), and [resume ruling](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6015726285).
- [Round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6016931581) and [R516-F1/F2](https://github.com/kebag-logic/milan-fpga/pull/681#issuecomment-6016896997).
- `CONTRIBUTING.md`, verification and one-line commit rules.
- `REQUIREMENTS.md`, REQ-VER-03 and REQ-VER-04.
- `docs/testing/CI_WORKFLOWS.md`, exhaustive validation and suite deadlines.

## How to get into the same state

```sh
git fetch origin 673-mclk-timeout
git switch --detach 793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
```

Use the repository's pinned Markdown renderer and configured integration environment. Supply an existing disk-backed scratch directory as `TMPDIR`. The builder command requires the selected RV32 SDK and patched integration dependencies.

## How to validate

Round-2 validation at `793dcd3f7867d85f8c1f5c9ef2b04dc9c2d9c5df`: the documentation commands below all passed. The exact R516 search returned no matches, and the live selector returned 60 default suites. `HANDOFF.md` records the exact commands, elapsed times and receipt hashes. The builder and implementation checks retain their round-1 evidence at `26bd6334a7b8b2a8582b36ae4729a71620546c14`; they were not rerun for the four Markdown corrections.

```sh
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration
python3 scripts/measure_test_evidence.py --check
python3 scripts/measure_test_evidence.py --selftest
bash -n scripts/run_all_suites.sh
python3 scripts/test_suite_cancellation.py
python3 scripts/suite_shards.py --selftest
python3 scripts/suite_tally.py --selftest
python3 scripts/ci_events.py --check
python3 scripts/ci_events.py --selftest
python3 scripts/ci_scope.py --selftest
python3 scripts/docs_check.py
python3 scripts/docs_check.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_doc_style.py
python3 scripts/check_archive.py
python3 scripts/gen_toc.py --selftest
python3 scripts/gen_toc.py --verify-anchors
python3 scripts/gen_toc.py --check
python3 scripts/check_em_dash.py --base bd884631684ccf5060339efa92263d5c3e5c262c
python3 scripts/check_py_idiom.py
python3 scripts/check_sh_idiom.py
python3 scripts/check_hygiene.py --check
git diff --check bd884631684ccf5060339efa92263d5c3e5c262c HEAD
```

Round-1 evidence at `26bd6334a7b8b2a8582b36ae4729a71620546c14`: the initial full builder attempt and its isolated firmware group each hit the local 540-second guard. The final builder evidence comes from the unchanged complete bank, run in a maintained foreground session with a longer deadline. The earlier attempts remain INCOMPLETE in the handoff. The complete command returned rc 0 in 1276.810 s, with one declared NOT RUN: gate 11 calibration needs an existing placement-utilization report that was absent. No elaboration arm was skipped for a toolchain reason.

Expected result: every completed gate exits 0; the evidence self-test reports 105 PASS and 0 FAIL. The builder must report no failed gates and must run all required elaboration arms. The recorded gate table and log hashes are in `HANDOFF.md`; round-1 self-test evidence is also recorded in the [issue handoff](https://github.com/kebag-logic/milan-fpga/issues/673#issuecomment-6016597101). This is executor evidence, not a review verdict.

## Known limitations / out of scope

Follow-up for the manager: move `milan_dp_gptp` into a job with a larger timeout or split its scheduling, then obtain a completed hosted sample and size its suite allowance. Run 37430728685, job 112160880673, reached 5400.003 s and returned UNKNOWN; no completed physical sample exists in the survey. The job lasted 5482 s, including 81.997 s outside that suite window. A proposed 7200 s allowance would need 7281.997 s, exceeding the current 7200 s job envelope. The resume ruling explicitly excludes this change. The manager opens and schedules the follow-up between merge rounds. No follow-up issue was created in this lane.

Suite checks, counts, campaigns, shard assignments, job timeouts, RTL and submodule pins are unchanged. Historical samples do not establish exact-head hosted results. Seven active-job logs were unavailable during the survey. No timeout sample establishes a successful completion bound. The local builder uses Verilator 5.052 and sv2v 0.0.13; the hosted pins are 5.050 and 0.0.12. Full local/hosted merge acceptance and Docs re-review remain pending; the manager schedules CI-affecting changes between merge rounds.

## Definition of Done

- [x] Linked Issue acceptance criteria, as ruled, are satisfied
- [x] Changed budgets have self-checking mutation cases
- [x] Assigned local builder, evidence and documentation gates pass
- [ ] Complete merge-stage local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per CONTRIBUTING.md
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


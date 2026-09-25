# [A306] Round 2 handoff

Issue: [#541](https://github.com/kebag-logic/milan-fpga/issues/541).
PR: [#562](https://github.com/kebag-logic/milan-fpga/pull/562).
Branch: `541-crf-unlock`.
Starting head: `2734b771bcf0b383ea62ef05744452827bafe9e4`.
Final local head: `fa1b5c364b39842d0f3d8e09acd7ca58a9532f0c`.
Source base remains `5b73d3f47dfed519eb988c13d6beb1db664ef1e0`.
Commit subject: `Test CRF timeout under continuous validation errors`.
One new commit, no body or trailers.

Status: assigned author work and local validation complete. Independent
re-review remains pending. No push, PR edit, merge, other checkout,
hardware activity or delegation was performed.

## Scope and decisions

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5828726541)
settles this change. It preserves the
[round-1 decision](https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5827373589)
and the published clause evidence. R322-1 F1 and R323-1 F1 retain their
reviewer-assigned Tests and Robustness lenses; the assigned R323-1 F2 is Docs.
This handoff records author evidence, not a review verdict or completion ledger.

All `hdl/` content and `docs/reference/REGISTER_MAP.md` are byte-identical
to the starting head. See [scope-integrity.log](scope-integrity.log).
No dev merge occurred. The round-2 delta is in [round-2.patch](round-2.patch).

## Changes

| File:line | Change |
| --- | --- |
| `tb/verilator/crf_rx/sim_discontinuity.cpp:29` | Enables the new default-gate check. |
| `tb/verilator/crf_rx/sim_discontinuity.cpp:183` | Corrects the silence-only comment: the timer measures time without a consumed accepted PDU. |
| `tb/verilator/crf_rx/sim_discontinuity.cpp:227` | Starts LOCKED, drives matched wrong-type PDUs every 400 clocks (2 ms), checks retention through clock 19,992 and unlock with one event by clock 20,012, then checks no relock/recount through clock 40,012. Only public outputs are graded. |
| `tb/verilator/crf_rx/mutants.py:23` | Adds `validation_error_refreshes_timeout`; the existing compiled-mutant protocol requires rc 1 and the named timeout-check failure. |
| `docs/testing/TESTING.md:463` | Names both validation-error mutants and the timeout coverage. |
| `scripts/measure_test_evidence.py:597` | Keeps the mutation-source-reader description aligned; no ratchet budget changed. |

At the harness's 200 kHz clock, the observation bracket is 99.96 to
100.06 ms after the final consumed accepted PDU. The stimulus supplies a
reject every 2 ms, including at 100 ms, so a reject-refresh defect stays
locked at the deadline. Malformed-only traffic continues through 200.06 ms.
The test also checks that validation errors are counted. Existing lock
retention, single-reject counting, silence timeout, discontinuity and
connected servo checks remain enabled.

## Check results

| Check | Result | Receipt |
| --- | --- | --- |
| Receiver unit | 13,836 checks, 0 failures | crf-rx.log |
| Receiver discontinuity, including new timeout check | 2,201 checks, 0 failures | crf-rx.log |
| Connected talker step | 69 checks, 0 failures | crf-rx.log |
| Default mutation campaign | 10 controls, 0 campaign failures | crf-rx.log |
| Servo unit / playback / PHC step | 85 / 8 / 113 checks, 0 failures | mmcm-servo.log |
| Reviewer clean controls | Both PASS; all legs built | r322-refresh.log, r323-refresh.log |

## Mutant verdicts

| Case | Verdict / executable rc | Required named failure |
| --- | --- | --- |
| `clean` | PASS / 0 | None |
| `validation_error_unlocks` | DETECTED / 1 | validation error preserves established lock |
| `validation_error_refreshes_timeout` | DETECTED / 1 | reject stream cannot refresh the 100 ms timeout |
| `tu_ignored` | DETECTED / 1 | tu edge invalidates before the sampling edge |
| `jump_removed` | DETECTED / 1 | unmarked timestamp jump invalidates the rate |
| `refill_short` | DETECTED / 1 | all 255 crossing intervals are withheld |
| `accept_edge_late` | DETECTED / 1 | tu edge invalidates before the sampling edge |
| `servo_clean` | PASS / 0 | None |
| `servo_ignores_valid` | DETECTED / 1 | [U13] invalid remote sample holds trim |
| `servo_never_resumes` | DETECTED / 1 | [U13] valid offset resumes PI trim |
| R322 `P2_error_refreshes_timeout` | DETECTED; discontinuity make rc 2, executable rc 1 | reject stream cannot refresh the 100 ms timeout |
| R323 `uf_refreshes_timeout` | DETECTED; discontinuity make rc 2, executable rc 1 | reject stream cannot refresh the 100 ms timeout |

The expected nonzero mutant executable exits are successful detection, not
failed gates. Both reviewer refresh mutants fail the same four checks:

- `reject stream cannot refresh the 100 ms timeout`
- `reject stream timeout counts one unlock` (got 0, expected 1)
- `continued reject stream stays unlocked`
- `continued reject stream never recounts the unlock` (got 0, expected 1)

R322's unit leg remains green. R323's unit and talker-step legs remain green.
Their discontinuity executables each return 1; the containing make returns 2.
Both reviewer scripts return 0, so the DETECTED verdicts and named failures
were checked explicitly, not inferred from their outer return codes.
Receipts: [r322-refresh.log](r322-refresh.log), [r322-results.json](r322-results.json),
[r323-refresh.log](r323-refresh.log), and the per-leg logs beside them.

## Reviewer artifact provenance and reproduction

Public evidence revision: `ad7d1c926eeaaaca2765c8325bcd30a2c941189c` on `541-review-evidence`.
The reports were verified identical to public comments 5827859729 and
5828724733. The scripts were executed unchanged; their bytes were checked
against that revision before and after execution.

| Script | SHA-256 |
| --- | --- |
| `review-evidence/541-r1/reviews/R322-1/scripts/probe_mutants.py` | `8f2137b5e050cd5907c51b3a968c8715d38c1bca5931747888d8ad3a64d809dc` |
| `review-evidence/541-r1/reviews/R323-1/scripts/reviewer_mutants.py` | `013eb10af2ff1d86e0029b378a83e3b63bd6201ecccb2cf32e1a7b0df8edf710` |

Reproduction, after extracting the candidate head and public evidence under
`$SCRATCH` and selecting the local compiler through `$VERILATOR`:

```sh
PROBES=clean,P2_error_refreshes_timeout python3 "$EVIDENCE/R322-1/scripts/probe_mutants.py" "$HEAD_EXPORT" "$SCRATCH/r322" "$VERILATOR" 1
python3 "$EVIDENCE/R323-1/scripts/reviewer_mutants.py" "$HEAD_EXPORT" "$SCRATCH/r323" clean uf_refreshes_timeout
```

The R322 script's existing job-count option was set to 1. The R323 script's
existing selection arguments chose its clean control and refresh mutant.
No mutation or script code was changed. Reviewer build products and tree exports
stayed in `/tmp`, outside the output directory. All scratch evidence,
exports, the scoped compiler wrapper and the temporary Markdown environment
were deleted after their receipts were retained.

## Required gates

All 16 required invocations returned 0. Each command ran in the foreground,
without a pipeline, with a 7,200-second execution timeout.

| Command | rc | Receipt |
| --- | --- | --- |
| `make -C tb/verilator/crf_rx` | 0 | [crf-rx.log](crf-rx.log) |
| `make -C tb/verilator/mmcm_servo` | 0 | [mmcm-servo.log](mmcm-servo.log) |
| `python3 scripts/docs_check.py` | 0 | [docs-git.log](docs-git.log) |
| `python3 scripts/docs_check.py (exact-head archive without Git metadata)` | 0 | [docs-no-git.log](docs-no-git.log) |
| `python3 scripts/check_em_dash.py --base 5b73d3f47dfed519eb988c13d6beb1db664ef1e0` | 0 | [em-dash.log](em-dash.log) |
| `python3 scripts/check_doc_style.py` | 0 | [doc-style.log](doc-style.log) |
| `python3 scripts/gen_toc.py --check` | 0 | [toc-check.log](toc-check.log) |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | [toc-anchors.log](toc-anchors.log) |
| `python3 scripts/check_doc_paths.py` | 0 | [doc-paths.log](doc-paths.log) |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | [module-matrix.log](module-matrix.log) |
| `python3 scripts/xvlog_gate.py --check` | 0 | [xvlog.log](xvlog.log) |
| `python3 scripts/check_sv_idiom.py` | 0 | [sv-idiom.log](sv-idiom.log) |
| `python3 scripts/check_cpp_idiom.py` | 0 | [cpp-idiom.log](cpp-idiom.log) |
| `python3 scripts/check_py_idiom.py` | 0 | [py-idiom.log](py-idiom.log) |
| `python3 scripts/measure_test_evidence.py --check` | 0 | [test-evidence.log](test-evidence.log) |
| `git diff --check` | 0 | [diff-check.log](diff-check.log) |

The no-Git documentation mode checked the exact committed tree archive,
with no Git metadata or submodule exports. Both documentation modes found
zero findings across 165 Markdown and 865 text files. Only the Git-dependent
inventory-parity arm is skipped in no-Git mode, as in CI.
Live HDL analysis examined 72 parent and 48 pinned-processor files: zero
parent findings, four existing processor findings, equal to the ratchet.
The evidence ratchet passes at 72 <= 77 suites without mutation arms,
10 <= 10 unseeded draws, zero unexplained readers and 3 <= 3 wall-clock users.
No budget was loosened or changed.

Simulation used the installed compiler version recorded in
[tool-identity.log](tool-identity.log), with only unlimited build parallelism
capped at eight jobs. Markdown dependencies came from the repository's
hash-locked requirements. The C++ idiom gate ran on the same candidate bytes
immediately before commit. Additional checks were the new harness precheck,
committed-diff whitespace check and protected-artifact identity check.
No required command failed. Compilation failures were never counted as kills.

## Delivery

[PR-BODY.md](PR-BODY.md) updates the complete current body retrieved with
`gh pr view 562 --json body`; its original is retained as PR-BODY.original.md.
The update starts with `[A306]`, includes Round 2, retains `Closes #541`,
and contains no home paths, tool/model attribution or attribution footer.
It is a local draft only; PR #562 was not edited.

[REVIEW-READY.md](REVIEW-READY.md) was posted as the final authorized action:
[Issue #541 review-ready comment](https://github.com/kebag-logic/milan-fpga/issues/541#issuecomment-5829021483).
Its posting receipt is REVIEW-READY.url.
No implementation risk or unresolved decision remains within this assignment.
Independent re-review, publication and subsequent merge gates remain outside
this author turn. This handoff does not claim the PR has cleared review.

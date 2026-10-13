[A607]

# Lane 730: handoff

## Round 5

Status: REVIEW READY at `ede700b00ef4d79566a6f108b11ce9bd4ad6beaa`.
The working tree is clean. No push, PR edit or live replay ran this round.
The Round 5 REVIEW READY is the new final comment on issue #730.

Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6134111240
Reviews: [R633-4](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6134026466)
and [R632-4](https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6134106828).
The earlier session ended externally, with one local commit and partial controls.
The retained commit was reviewed; the controls were completed here.

New commits, without rebase, amend or identity changes:

- `2d0fad22`: retained implementation of the monitor mask and deferred delivery.
- `20a534a9`: completed standing controls, restored the mask when act's boundary opens on
  a pending signal, and kept the live interruption probe interruptible inside the monitor.
- `ede700b0`: authoritative mask, delivery and control documentation.

### Changes at the final head

| File:line | Change and reason |
| --- | --- |
| `scripts/act_ci.py:269`, `:278` | `TerminationRequest.delivered_after` restores the incoming mask only after monitor cleanup. A previously propagating body failure wins; the delivered signal is printed beside it. Otherwise a held signal keeps its conventional status, with any cleanup failure printed beside it. |
| `scripts/act_ci.py:5650`, `:5712`, `:5729`, `:5742` | The monitor takes the signal mask before yielding its body. Its reader starts with the signals blocked. The mask stays held across generator/context-manager cleanup entry, stream containment, reader join and dead-thread proof, pipe finalization and cleanup reporting. Only then does `delivered_after` release it. No mask is exported when spawning the event-stream process. |
| `scripts/act_ci.py:5313` | The normal act boundary queries the held mask before its `try`, unblocks inside that `try`, and restores in `finally`. A signal already pending on entry therefore cannot bypass restoration. Act runs interruptibly. |
| `scripts/act_ci.py:15565` | The live interrupt probe opens the same temporary window inside its existing cleanup-bearing `try`. Its worker also starts through `start_cleanup_thread_or_refuse`. Without this additional call-site fix the monitor's mask would prevent the probe's expected SIGINT from interrupting act. The live probe was not run. |
| `scripts/act_ci.py:7696`, `:8203`, `:8309` | The standing harness observes containment, reader completion and pipe closure where outer teardown would start. Its trace sweeps every executed Python line from the body's final step through the native mask-release call, including context-manager and thread-join internals. It stops before code outside that critical section. Each run uses a busy reader; failure stops the sweep at the first counterexample. |
| `scripts/act_ci.py:12390`, `:12443` | Offline controls pin normal act's unblocked execution, restoration after return/raise, pending-signal delivery before spawn, and the live interrupt probe's immediate SIGINT and restored mask. |
| `docs/testing/CI_WORKFLOWS.md:1813`, `:1869` | The authoritative guarantee states the mask, thread inheritance, both act signal windows, release after all obligations, conventional status and first-failure precedence. The control inventory includes cleanup entry and the step sweep. |

### Controls and gates

CPython 3.12.3, PyYAML 6.0.3 and the pinned Markdown renderer.
All candidate self-tests and executable probes ran in disposable offline namespaces.
No network, Docker socket, host credential or privileged operation was exposed.
Temporary directories were backed by the assigned disk scratch, including the boundary's
private temporary mount. Foreground parents waited for all children; commands had bounded
execution times below ten minutes.

- `python3 -I scripts/act_ci.py --selftest`: 507 ok, 0 FAIL, rc 0; all earlier 498 arms remain.
- Cleanup-entry controls: real SIGINT, SIGTERM and SIGHUP at R633-4's exact AST-selected
  delivery point. Each contains the stream, finishes the move, joins the reader and closes
  the pipe before teardown, with statuses 130, 143 and 129.
- Step sweep: 198 line steps, each exercised once with main-thread delivery and once with
  process-wide delivery, cycling INT/TERM/HUP. All 396 injections complete containment,
  reader completion and pipe close before teardown, retain the conventional exit and
  diagnostic, and leave no cleanup signal newly blocked or pending.
- Held SIGTERM plus failed reap: 143, interrupt diagnostic and secondary reap diagnostic.
- Body failure plus held SIGTERM: original failure retained, signal reported beside it.
- R633-4's `probe_cleanup_entry.py`, unchanged: all six cases pass, including its three
  original body controls. Published sha256 `2bcf4697eaa587b0074d0dc75da77461ab5d673b4c3f37caf0b353405479b822`.
- Published unchanged probes: R632-2 shutdown S1-S4, R632-3 derivation/lifecycle P1-P5
  (300 seeds), R633-2 lifecycle (76,800 transitions), monitor, compatibility probe, and
  R632-2's published R633-1 adaptation all rc 0.
- R632-2's unchanged `mutants_r2.py`: 36/36 killed, no bad anchors.
  Sha256 `c78da78362d7e19e2f068d76d368201f111b5faa80110c24a7c934748f85ec0b`.
- R632-3's unchanged `mutants_r3.py`: 24/30 killed, Q24 killed; the exact prior survivors
  Q06, Q11, Q13, Q15, Q28 and Q29 remain. No bad anchors.
  Sha256 `2ef9496417f4adcbfca2b7c3b22341de36f85c7f3c5b64bb2975353db80cf8ec`.
- Eight Round 5 controls are killed: E01 removes the outer mask; E02 releases it before
  cleanup; E03 unblocks the reader; E04 never releases the mask; E05 lets a held signal
  replace an earlier body failure; E06 leaves normal act blocked; E07 moves normal act's
  unblocking before its restoration-bearing try; E08 leaves the live interrupt probe blocked.
  Each fails its targeted standing control (rc 1), not a timeout. E03 specifically fails
  the process-wide sweep. E08 refuses because fault injection never interrupted act.

Receipts are in `receipts/r5/`, with sizes and sha256 in `MANIFEST.json`.
The final source hashes are in `source-manifest.json`; no source export was copied.
`act_ci.py` is 670270 bytes, sha256
`1804dec90fb807c72d405f9d1f94e3b9f40b643b05ad872ead3ce4cb53138083`.
The step-sweep output and all 507 arms are in `act-ci-selftest.log`.
`mutations-r5-controls.json` contains each exact anchor/replacement and focused control name;
`run_masked_arms.py` runs that control against a scratch copy inside an offline boundary.
Every output file is below 200 KB; no toolchain, environment, package or tree export was copied.

Reviewer scripts were checked byte-for-byte against public evidence commit `677b2f0a`.
Reproduction commands, inside disposable offline boundaries:

```sh
python3 -I <review-r633-4>/scripts/probe_cleanup_entry.py <candidate>
python3 -I <review-r632-2>/scripts/mutants_r2.py <packet-r2> <candidate> --jobs 6
python3 -I <review-r632-3>/scripts/mutants_r3.py <packet-r3> <candidate> --jobs 6
python3 -I run_masked_arms.py <mutated-script> <control-name>
```

Each campaign packet supplies its offline `scripts/sandbox.sh`; its wrapper is validation
infrastructure, not candidate host orchestration. All children finish before the foreground
campaign exits. The mutation tree contains the final committed source bytes.

| Plain command | Result |
| --- | --- |
| `python3 scripts/ci_events.py --check` | rc 0, 2016 contract items; includes the act runner contract gate |
| `python3 scripts/ci_events.py --selftest` | rc 0, 2828 arms, including removal/disabling/swallowing of that gate |
| `scripts/act_slot_proof.sh --selftest` | rc 0, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | rc 0; ratchets unchanged, 54 checks pass |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | rc 0; no findings, 700 arms |
| `python3 scripts/docs_check.py` | rc 0, no findings |
| `python3 scripts/check_doc_style.py` | rc 0 |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` | rc 0; 480 anchors |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | rc 0; 157 added lines, 339 self-test arms |
| `python3 scripts/check_doc_paths.py` | rc 0; 964 paths |
| `git diff --check dc4d06cb HEAD` | rc 0 |

Validation corrections during the resume: four overlong test lines were wrapped. The
validation namespace initially lacked the clone's alternate Git object store; its read-only
mount was added and the Git check passed. The partial trace had extended beyond mask release
into weak-reference callbacks and the harness's teardown observation; its endpoint now names
the native mask release. These preliminary runs are not claimed as final gate evidence.

### CPU layout and disjointness, unchanged in Round 5

Every range below is four CPUs wide. Container j is numbered 1 through 4.

| Slot | Before: every concurrent container | After: staging | After: each concurrent container |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 1 | `4-7` | `20-23` | `24-27`, `28-31`, `32-35`, `36-39` |
| 2 | `8-11` | `40-43` | `44-47`, `48-51`, `52-55`, `56-59` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | j owns `20N+4j..20N+4j+3` |

The run derives the number used from the selected workflows' `max-parallel` and
`CONCURRENT_JOB_LIMIT`. A slot is spaced for four job ranges plus staging.
`selftest_cpu_layout_disjoint` at `scripts/act_ci.py:7243` covers all slots 0-63 at maximum
concurrency: 320 ranges, all width four, no shared CPU. It detects the planted pre-change
`4N` spacing across slots and every leg sharing one range within a slot. Staging planted on
a job range is refused. The per-container 16 GB bound and isolated-slot 24G cap are unchanged.

### Before/after measurement, unchanged obligation

No new replay was started. The manager's no-replay ruling still applies:
https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815

| Run | Job | Per-job wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- |
| Before, partial slot 3, dev `dc4d06cb`, PR #728 `2c2f3369` | full-ci-gate | 15 s, 20:02:42-20:02:57 UTC | 15.1 GiB sampled through the stop | succeeded |
| Same partial before | Verilator shards 0-3 | 20:02:57-20:10:36 UTC, interrupted | same sample | interrupted; replay rc 130 |
| Same partial before | Verilator 4, Yosys 0-3 | started during stop; no complete timing | same sample | interrupted |
| After, final lane head | all | not run, per ruling | not measured | not measured |

This partial run is not a completed before measurement or a verdict comparison.
The manager uses the retained slot-0 before logs (#721 at `42678ae2`, #715 at `c7d0ad63`)
and the first replay on merged code. The post-merge commands and exact plan, per-job,
CPU-range summary, verdict and memory lines to read remain in the measurement section below.
Acceptance 1 and 2 are proven offline; 3's same-head verdict comparison, 4 and optional 5
remain deferred. `Relates to #730` remains correct.

### Review and evidence disposition

R633-4-F1 is addressed by the implementation and controls, awaiting independent re-review.
No author verdict or reviewer-owned coverage ledger is supplied here. Earlier clean review
heads do not approve this new code. The former cleanup-entry limitation is superseded by
Round 5; historical round descriptions below describe their original heads only.
The other optional review suggestions remain outside this round.
Hosted acceptance, candidate-merge validation, merge authorization and post-merge containment
remain manager duties. No workflow, suite, testbench, RTL, firmware or gitlink changed.
The uninitialized dependency was not needed or initialized. No exclusive hardware lock was taken.

## Round 4

Status: REVIEW READY at `31e53e82a4a1604569ccacba8473f21e70b9cbc0` (not pushed; push is outside
this lane; the remote branch is still `5c6f489a`). Posted:
https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133776179
New commit on top of `5c6f489a`, no rebase or amend:

- `31e53e82` Make the replay concurrency arm fail unless every order of the selected workflows
  derives the most of any of them (#730)

`git diff --stat 5c6f489a 31e53e82`: `scripts/act_ci.py` +20/-0. Test-only: no runtime code,
doc, workflow, suite, testbench, RTL or firmware file touched. `scripts/act_ci.py` is blob
`ab097a5c`, sha256 `a9c135b0c94692590f24e4aca2bc60296a519794ea7814f166232713724facf2`.

Inputs:

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133645896
  (item 1 only; "No other change").
- R632-3 (NEGATIVE, one MINOR Tests, F1): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133640258
- R633-3 (POSITIVE): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133582228
- R632-3's `scripts/` from `review-evidence/730-r1/reviews/R632-3/` on `730-review-evidence`
  (`6c93fba4`); every file's sha256 matches its `MANIFEST.sha256`. `mutants_r3.py` is sha256
  `2ef9496417f4adcbfca2b7c3b22341de36f85c7f3c5b64bb2975353db80cf8ec`, run unchanged.

The ruling https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815 still
holds: no replay, no `act_ci.py` against a PR, no `--dry-run`, no live self-test. Only
`--selftest` ran, on the lane, on a `git archive` of the head, and on mutated scratch copies.

### Finding and fix (file:line at `31e53e82`)

| Item | Finding | Fix | Standing test |
| --- | --- | --- | --- |
| 1 | R632-3-F1: the arm at `scripts/act_ci.py:7143-7147` claims "the most of any selected workflow" but derived only `("docs", "rtl-full")`, widest last, so Q24 (`most = sum(...)`, the last workflow wins) passed all 497 arms | Test only. `import itertools` (`:51`). In `selftest_job_concurrency` (`:7085`): a third planted workflow `rtl-fast`, one matrix job with `max-parallel: 3` (`:7122`, `:7131`); `orders` (`:7123-7127`) is `(docs, rtl-full)`, `(rtl-full, docs)` and `itertools.permutations(("docs", "rtl-fast", "rtl-full"))`; for each `CONCURRENT_JOB_LIMIT` 1, 2, 3 the arm derives `rtl-fast` and `docs` alone (`:7139-7141`) and every order (`:7142`) | New arm `:7148-7153`: `alone == {1: (3, 1), 2: (3, 1), 3: (3, 1)}` and `ordered == {1: {4}, 2: {6}, 3: {7}}`, so every order gives exactly `rtl-full`'s value and the other two are shown narrower at each limit. The existing arm (`:7143-7147`) and the shipping arm are unchanged. Arms: 497 to 498. |

The orders put the widest workflow first, between and last, and before and after each narrower
one; the reversed order and "a wide workflow before a narrow one" (both named in the assignment)
are `("rtl-full", "docs")` and, among the six, `("rtl-full", "rtl-fast", "docs")`.

Docs not changed: `docs/testing/CI_WORKFLOWS.md:1827-1828` lists "the concurrency each job and
workflow derives, including the `CONCURRENT_JOB_LIMIT` sum", which stays true and names no order.
The assignment says no other change.

### Mutation evidence (on a `git archive` of `31e53e82`, through R632-3's `sandbox.sh`, CPython 3.14.7)

- R632-3's `mutants_r3.py`, unchanged: `mutants: 30, killed 24, survived ['Q06', 'Q11', 'Q13',
  'Q15', 'Q28', 'Q29'], bad anchors []`. Q24 is KILLED, failing exactly the new arm
  (`receipts/r4/r632-3-mutants-r3-at-head.txt`). At `5c6f489a` R632-3 recorded 23 killed with
  the same survivors plus Q24. Q15 is the one R632-3 judged equivalent; Q06, Q11, Q13, Q28 and
  Q29 are its optional S1, not taken (no other change).
- This round's order mutants (`receipts/r4/mutants-r4-order.txt`, driver
  `receipts/r4/mutants_r4_order.py`: R632-3's driver with only its mutant list replaced):

| Mutant | Arms failed |
| --- | --- |
| O01 the first selected workflow wins | the existing arm and the new arm |
| O02 the concurrencies are added | the existing arm, the new arm, and the monitor's handed ranges |
| O03 the least wins | the existing arm and the new arm |
| O04 only the first two selected workflows are read | the new arm |
| O05 only the last two selected workflows are read | the new arm |
| O06 the last wins (Q24) | the new arm |

- R632-2's `mutants_r2.py`, unchanged: `mutants: 36, killed 36, survived [], bad anchors []`
  (`receipts/r4/r632-2-mutants-r2-at-head.txt`).
- R632-3's `probe_r3.py` (300 seeds), unchanged: P1-P5 PASS
  (`receipts/r4/r632-3-probe-r3-at-head.txt`). R632-2's `probe_shutdown.py`, unchanged: S1-S4
  PASS (`receipts/r4/r632-2-probe-shutdown-at-head.txt`).

### Gates at `31e53e82` (all rc 0; CPython 3.12.3, PyYAML 6.0.3, pinned Markdown renderer)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | `selftest: PASS`, 498 ok, 0 FAIL; also 498/0 on CPython 3.14.7 in the sandbox on the archive |
| `python3 scripts/ci_events.py --check` / `--selftest` | OK, 2016 contract items / PASS, 2828 arms |
| `scripts/act_slot_proof.sh --selftest` | PASS, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | long function 9 <= 9, too many parameters 7 <= 7, over-long line 0 <= 0 / 54 PASS |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | 0 findings / 700 arms PASS |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_doc_style.py` | OK |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` | OK / 480 links |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | 0 findings over 133 added lines |
| `python3 scripts/check_doc_paths.py` | OK, 964 paths |
| `git diff --check dc4d06cb` | clean |

Receipts (`receipts/r4/`, hashed in `receipts/r4/SHA256SUMS`): `act-ci-selftest.log`,
`gates.txt`, `r632-3-mutants-r3-at-head.txt`, `r632-2-mutants-r2-at-head.txt`,
`mutants-r4-order.txt`, `r632-3-probe-r3-at-head.txt`, `r632-2-probe-shutdown-at-head.txt`,
and the scripts `mutants_r4_order.py` and `run_r4_evidence.sh`. The gate scripts are Round 3's
`receipts/r3/run_code_gates.sh` and `run_doc_gates.sh`, run unchanged. Not copied:
`ci-events-selftest.log` (184068 B, sha256
`c6b497eb75665fd129d7bdb0dbd39b65b62d3fce837704da7526626059658551`, the same bytes as Round 3).

### Unchanged from Round 3

The CPU sets per slot and per concurrent container, the disjointness proof and its planted
overlaps, the plan lines and dry run, and the replay table (no replay, per the ruling): no
layout, plan or runtime code changed. `Relates to #730`, not `Closes`: acceptance 3's same-head
verdict clause, 4 and 5 are post-merge. R632-3's S2 and S3 (R632-2-S2 and S3 retained) stay
optional and not taken, as in Round 3.

## Round 3

Status: REVIEW READY at `5c6f489ac65f51763a6ccc41f338dde0e5fc90b5` (not pushed; push is outside
this lane). Posted: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133409048
New commits on top of `5ba8313a`, no rebase or amend:

- `c915dc3f` Keep an interrupt or failure already propagating through a failed CPU-range monitor
  cleanup, printing the cleanup failure beside it, and make the join retry, hold, precedence and
  event-window arms able to fail (#730)
- `5c6f489a` Document that an interrupt or failure already unwinding keeps its exit status through
  a failed CPU-range monitor cleanup, and the new shutdown pins (#730)

`git diff --stat 5ba8313a 5c6f489a`: `scripts/act_ci.py` +282/-61, `docs/testing/CI_WORKFLOWS.md`
+21/-8. No workflow, suite, testbench, RTL or firmware file touched. `scripts/act_ci.py` is blob
`1f2fa87f` at both commits.

Inputs:

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6133149921
- R633-2 (NEGATIVE, one MINOR, F1): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133015754
- R632-2 (NEGATIVE, one MINOR, F1): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6133143865
- R632-2's `scripts/mutants_r2.py` (sha256
  `c78da78362d7e19e2f068d76d368201f111b5faa80110c24a7c934748f85ec0b`), `sandbox.sh`
  (`c1a5a236...`), `probe_r2.py` (`287f7cb6...`) and `probe_shutdown.py`
  (`30c10f643174b342fd390d4c4daebcc5e6194c3e38a75422f0d53e6839911485`), read from
  `review-evidence/730-r1/reviews/R632-2/` on `730-review-evidence` (`8a32fdc4`), run unchanged.
- R633-2's `probe_monitor.py` was read (at `52bc7cb8`) to see what it measures. It was not run:
  it extracts a fixed set of definitions and replaces collaborators, and its signal-preservation
  check is the case the new standing arms cover.

The ruling https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815 still
holds. No replay, no `act_ci.py` against a PR, no `--dry-run`, and no live self-test ran. Only
`--selftest` ran, on the lane, on archives of the head, and on mutated scratch copies.

### Findings and fixes (file:line at `5c6f489a`)

| Item | Finding | Fix | Standing test |
| --- | --- | --- | --- |
| 1 | R633-2-F1: a monitor cleanup failure replaced an interrupt or body failure already propagating. SIGTERM plus a reap failure exited 2 with the reap message, not 143 with `interrupted by SIGTERM after cleanup` | `job_cpu_range_monitor` records the propagating exception (`scripts/act_ci.py:5677-5679`, `except BaseException as exc: primary = exc; raise`) and passes it to `stop_job_cpu_range_monitor` (`:5681-5684`). `stop_job_cpu_range_monitor` takes `primary` (`:5535`); every step still runs first (unchanged). Then it prints each cleanup failure that is not the one raised, inside the signal mask (`:5576-5585`): all of them when a `primary` exists, `failures[1:]` otherwise. With a `primary` it returns (`:5586-5587`), so the caller's `raise` keeps the original. Without one, `raise failures[0]` as before (`:5588-5589`). Print line: `act-ci: CPU-range monitor cleanup also failed: <Type>: <message>`. A failing print cannot replace the first failure. Docstrings at `:5537-5546` and `:5602-5613`. | `selftest_job_cpu_monitor_busy` (`:7823`): body failure + reap failure gives outcome `raised act boundary failed`, stderr is exactly the reap line, and the reader is joined, the stream contained and the pipe closed before the monitor exits. A real SIGINT, SIGTERM and SIGHUP (`:7882`, delivered by `signal.raise_signal` to the runner's handler, `:7713`), each followed by a reap failure, give `exit 130/143/129`, stderr exactly the reap line then `act-ci: interrupted by SIG... after cleanup`, `joined_before_exit`, `moved == 1` and the pipe closed. A reap failure alone still raises it, with empty stderr. |
| 2 (K12) | R632-2-F1(a): the retry arm's reader died during the 0.25 s pause | `FlakyJoinReader` (`:7898`) now releases its thread only on the retried join; `held_reader` (`:7924`) bounds the wait at 10 s so a regression cannot hang the self-test | `selftest_job_cpu_monitor_shutdown` (`:7996`), first arm (`:8012`): the join failure is raised, the reader trail at that moment is `['reader ended']`, nothing else printed, the pipe closed. |
| 2 (K13) | R632-2-F1(b): no arm outlived the bounded wait | `DOCKER_COMMAND_TIMEOUT` patched to `0.05 - 10` (`:8044`), so the bounded wait is 0.05 s. The reader runs until the hold line is printed (`ReleaseOnHold`, `:7973`). No production change. | `:8038-8061`: `join_job_cpu_reader` returns `None` with the reader already ended, `problems == ['the CPU-range monitor survived its bounded shutdown']`, and stderr is exactly the hold line for process group 424242. |
| 2 (K36) | R632-2-F1(c): no arm had two cleanup failures | `stop_with_flaky_join` (`:7938`) runs stop with a containment, a `primary` and a reader whose first join fails | `:8021`: with no `primary`, a reap failure and a join failure raise `Refusal: cannot reap interrupted host process leader` after the reader ended, and print only the join line. `:8030`: with `primary=TerminationRequest(SIGTERM)`, nothing is raised and both lines are printed, reap first. |
| 2 (K32) | R632-2-F1(d): the `--since` value was not pinned | `time.time` stubbed to `1_700_000_000.75` around the first monitor arm (`:7740`) | `:7750`: `tail[:3] == ["events", "--since", "1699999999"]`. |
| 3 | R632-2 suggestions (optional) | S1 taken, test only: containment under the cleanup mask (`:8062-8078`, the arm unblocks INT/TERM/HUP around it so an inherited mask cannot hide a regression) and the reader-crash problem (`UnreadablePipe`, `:7988`; `:8079-8089`). S2 and S3 not taken (below). | K29 and K31 now killed. |

Harness changes: `drive_job_cpu_monitor` (`:7615`) runs the monitor inside
`run_with_cleanup_signals` (`:7680`), as `main` does, and keeps the captured stderr on the stream
(`FakeEventStream.stderr`, `:7598`). An interrupted body's outcome is `exit <128 + signum>`. The
earlier arm "a body that raises and a reap that fails together" expected the reap failure to
replace the body's. Item 1 reverses that requirement, so it now expects the body's failure, and
it checks more than before. The old SIGTERM arm raised `TerminationRequest` by hand; it now
delivers the real signal and checks exit 143 and its diagnostic. The old join-retry arm in
`selftest_job_cpu_monitor_failures` moved into `selftest_job_cpu_monitor_shutdown` with the fix
above. Arms: 490 to 497.

Exit status by case, before (`5ba8313a`) and after (`5c6f489a`), as `main` maps them:

| Case | Before | After |
| --- | --- | --- |
| body returns, cleanup OK | 0 path | unchanged |
| body returns, reap fails | Refusal, exit 2 | unchanged |
| body Refusal, reap fails | reap Refusal, exit 2 with the reap message | body Refusal, exit 2 with the body's message; reap printed beside it |
| body RuntimeError, reap fails | reap Refusal, exit 2 | RuntimeError propagates (as with no cleanup failure); reap printed beside it |
| SIGINT/SIGTERM/SIGHUP, cleanup OK | 130/143/129 | unchanged |
| SIGINT/SIGTERM/SIGHUP, reap fails | exit 2, no interrupt diagnostic | 130/143/129 with `interrupted by ... after cleanup`; reap printed beside it |
| reap and join both fail, no earlier failure | reap Refusal raised, join failure lost | reap Refusal raised; join failure printed |

Docs (`docs/testing/CI_WORKFLOWS.md` at `5c6f489a`):

- `:1807-1819`: the first failure wins: the 128 + signal status and diagnostic survive a failed
  monitor cleanup, cleanup failures are printed with their line, and with no earlier failure the
  first cleanup failure is raised.
- `:1844-1855`: the self-test pins: the `--since` second, the join retry, the hold, the mask,
  the reader crash, and which failure wins.

### Mutation evidence

R632-2's `mutants_r2.py`, unchanged, on a `git archive` of `c915dc3f` (the `act_ci.py` blob is
the head's), through its own `sandbox.sh` (no network, no Docker socket), CPython 3.14.7:
`mutants: 36, killed 36, survived [], bad anchors []` (`receipts/r3/r632-2-mutants-r2-at-head.txt`).
Every failing arm of the four required mutants (`receipts/r3/required-mutants-arms.txt`):

| Mutant | Arms failed |
| --- | --- |
| K12 failed join not retried | the retry arm; reap + join (no primary); reap + join (primary) |
| K13 bounded join gives up | the same three, and the hold arm |
| K32 `--since` an hour ahead | the event-filter arm |
| K36 last failure raised | reap + join (no primary) |

K29 (stop unmasked) and K31 (reader crash unrecorded), R632-2's S1, are killed by the mask and
reader-crash arm. Its `probe_shutdown.py`, unchanged, passes S1-S4 at the head
(`receipts/r3/r632-2-probe-shutdown-at-head.txt`).

This round's own mutants (`receipts/r3/mutants-r3.txt`, driver `receipts/r3/mutants_r3.py`):

| Mutant | Arms failed |
| --- | --- |
| N22 `primary` not passed to stop | 4 |
| N23 `primary` ignored by stop | 5 |
| N24 cleanup failures not printed | 6 |
| N25 the raised failure printed too | 3 |
| N26 only a signal kept | 1 |
| N27 a signal not kept (`except Exception`) | 3 |
| N28 hold not printed | 1 |
| N29 hold not recorded | 1 |

The 21 Round 2 mutants re-run at this head: 21 killed (`receipts/r3/mutants-r2-rerun.txt`).

### Gates at `5c6f489a` (all rc 0; CPython 3.12.3, PyYAML 6.0.3, pinned Markdown renderer)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | `selftest: PASS`, 497 ok, 0 FAIL; also 497/0 on CPython 3.14.7 |
| same, `os.cpu_count` stubbed to 1, 4, 8, 19, 20, 128 | 497/0 each (`receipts/r3/selftest-hosts.txt`) |
| same, 10 concurrent runs | 10 x 497/0 (`receipts/r3/selftest-stress.txt`) |
| `python3 scripts/ci_events.py --check` / `--selftest` | OK, 2016 contract items / PASS, 2828 arms |
| `scripts/act_slot_proof.sh --selftest` | PASS, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | long function 9 <= 9, too many parameters 7 <= 7, over-long line 0 <= 0 / 54 PASS |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | 0 findings / 700 arms PASS |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_doc_style.py` | OK |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` | OK / 480 links |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | 0 findings over 133 added lines |
| `python3 scripts/check_doc_paths.py` | OK, 964 paths |
| `git diff --check dc4d06cb` | clean |

Receipts (`receipts/r3/`, hashed in `receipts/r3/SHA256SUMS`): `act-ci-selftest.log` (44767 B,
sha256 `11b66dea7b67d15101d7c7ac9ae2486e539d4855dcdf1ed0c02ce36b9f64cd71`), `gates.txt`,
`selftest-hosts.txt`, `selftest-stress.txt`, `r632-2-mutants-r2-at-head.txt`,
`required-mutants-arms.txt`, `r632-2-probe-shutdown-at-head.txt`, `mutants-r3.txt`,
`mutants-r2-rerun.txt`, the drivers `mutants_r3.py` and `arms_for_required.py`, and the gate
scripts. Not copied: `ci-events-selftest.log` (184068 B, sha256
`c6b497eb75665fd129d7bdb0dbd39b65b62d3fce837704da7526626059658551`).

### Not taken, and why

- R632-2-S2 (optional): a first signal that lands in `job_cpu_range_monitor`'s `finally` before
  `stop_job_cpu_range_monitor` masks signals skips containment. Masking at the top of the
  `finally` would narrow the window but not close it, since the generator resumes a few bytecodes
  earlier. `replay_slot` and `run_act_process` share the pattern, so it belongs to its own Issue.
  Listed in the PR body's limitations.
- R632-2-S3 (optional): after a join that raised at once, a reader still running is reported as
  "survived its bounded shutdown" with a hold line, although no bounded wait elapsed. Kept: the
  hold is still true (teardown waits), and R632-2's own `probe_shutdown.py` S1 pins that text.
- Unchanged and still holding from Rounds 1 and 2: the CPU sets per slot and per concurrent
  container, the disjointness proof and its planted overlaps, the plan lines and the dry run
  (no layout or plan code changed), and the replay table (no replay, per the ruling).
  `Relates to #730`, not `Closes`: acceptance 3's same-head verdict clause, 4 and 5 are
  post-merge.
- Pre-existing, not touched: `import io` appears twice at `scripts/act_ci.py:47` and `:49`
  (present at `dc4d06cb`).

## Round 2

Status: REVIEW READY at `5ba8313a3f036f34aac1a6bfbfcec0e0efd8c646` (not pushed; push is outside
this lane). Posted: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132825823
New commits on top of `eb566634`, no rebase or amend:

- `93215f07` Keep each act job container's CPU range reserved until its destroy, read by docker
  inspect; refuse a small host on slot 0; join the monitor's reader on every exit (#730)
- `5ba8313a` Document range reservations until destroy, inspect-read placement, the slot-0
  refusal and the failure-safe monitor shutdown (#730)

Inputs:

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132404197
- R633-1 (NEGATIVE, four MAJOR): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6132335284
- R632-1 (NEGATIVE, two MINOR, two RESIDUE): https://github.com/kebag-logic/milan-fpga/pull/731#issuecomment-6132397037
- Reviewer probes read from `review-evidence/730-r1/reviews/` on `730-review-evidence`
  (`fc302f51`), extracted to scratch. R632-1's `mutants.py` was re-run against this head. R633-1's
  `probe_cpu_ranges.py` was not re-run, because it builds the record with the old three-argument
  signature. Its four sequences are now standing self-test arms, listed below.

The ruling https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815 still
holds. No replay, no `act_ci.py` against a PR, and no `--dry-run` against a daemon ran. Only
`--selftest` ran, plus the offline dry-run harness.

### Findings and fixes

| Item | Finding | Fix (file:line at `5ba8313a`) | Standing test |
| --- | --- | --- | --- |
| 1 | R633-1-F1: `die` freed a range that a stopped container keeps | A reservation lasts from placement to `destroy`, or until an inspect shows the container gone. `die` frees nothing (`scripts/act_ci.py:5443` `observe`, `:5366` `release`). Where a container runs comes from `docker container inspect --format {{.HostConfig.CpusetCpus}}` (`:5353` `effective_cpus`, `:5372` `check`, `:5607` `read_cpus`). The runner reads it after each move, at each `start`, at an `update` of a container not yet seen on its range, and for every holder when no range is free (`:5405` `place`). A `start` whose `create` was never read is placed. The summary changed (`:5471`), see below. | `selftest_job_cpu_record` (`:7371`) runs R633-1's sequence `create A, update A, start A, die A, create B, update B, start B, start A` through `ModelDaemon` (`:7263`). The model holds each container's real cpuset, and `disagreements` is checked after every event. A and B never share a range, A restarts on `4-7`, and B gets `8-11`. Further arms: destroy frees; with every range held, inspect frees a container removed without its event and keeps a stopped one's. |
| 2 | R633-1-F2: a failed or timed-out update freed its target | The target is reserved before the update runs (`:5405`). A Refusal (timeout) or non-zero exit keeps it reserved, then `check(moved_now=True, failure=...)` reads the effective cpuset. On target, it counts as moved, with a warning that the command failed but inspect shows it there. Off target, it is a warning and the range stays reserved until removal, because the request may still apply. An unreadable inspect is a warning and the range stays reserved. Only `No such container` from the daemon frees it. A late `update` event re-reads it (`:5443`). Warnings stay warnings, never a verdict. | `selftest_job_cpu_move_failures` (`:7460`) covers four cases, each with the next container created while the outcome is uncertain: applied then CLI timeout (R633-1's probe); lost then landing late; move and read both timing out; refused. In each, `found == []` after every event, and the warning text is pinned. |
| 3 | R633-1-F3: slot 0 fell back silently | `job_cpu_ranges` refuses on every slot (`:4672`). The fallback text in `describe_job_cpu_ranges` is gone (`:4710`). | `selftest_job_cpu_ranges` (`:7228`) checks slot 0 at 1, 3, 4, 7, 8, 19, 20 and 21 CPUs, for 1 and 4 containers. 19 refuses and 20 gives `4-7`..`16-19`; 7 refuses and 8 gives `4-7` for one container; below 4 refuses. |
| 4 | R633-1-F4 + R632-1-F1: a terminate failure skipped the join; no arm could see a missing join | `stop_job_cpu_range_monitor` (`:5528`) runs every step whatever an earlier one raised: poll (failure is a warning), containment, reader join, pipe close. It raises the first failure only after all of them. `join_job_cpu_reader` (`:5492`) waits until the reader is provably ended. A failed join is retried. A reader still alive after the bounded wait is a warning plus a printed containment hold, and the wait continues. | `selftest_job_cpu_monitor_busy` (`:7779`): the stream's only line arrives after the body returns, the move takes 0.2 s, and the stream ends only once contained (`HeldEventPipe`, `:7524`). The trail must show the move finished and the stream ended before "monitor exited". The arm runs for return, raise, SIGTERM, reap failure (R633-1's injection) and raise plus reap failure. `selftest_job_cpu_monitor_failures` (`:7840`) covers a stream or reader that cannot start, and a join that fails once (`FlakyJoinReader`, `:7820`). The poll-failure arm is in `selftest_job_cpu_monitor` (`:7692`). |
| 5 | R632-1-F2: verdict invariance not pinned at run level | No runtime change. The harness `run_workflow_control` (`:6339`) takes a `PlantedRun` (`:6331`): act's exit status, plus record outcomes and problems for `cpu_range_monitor_stand_in` (`:6201`). It now captures stderr with stdout. | `selftest_cpu_range_warnings` (`:6477`) uses a container left on staging and two planted problems. For act rc 0 the verdict is `PASS` for both workflows; for rc 3 it is `FAILED (3)` and the second workflow never runs. Each workflow prints its summary once and exactly one `WARNING ... CPU ranges:` line per problem. |
| 6 | R632-1-R1 / R2 residue | Mixed runner versions sentence added to the slot resource bounds (`docs/testing/CI_WORKFLOWS.md:2141-2143`). The PR body's slot-0 sentence is replaced (item 3 superseded R2's wording): every slot, slot 0 included, refuses a host without the derived ranges. | Docs gates. |

Also found and fixed in this round, by running the self-test under simulated host CPU counts.
`docs.yml` runs `act_ci.py --selftest` on a 4-vCPU hosted runner, but three self-test harnesses
called `run_validation` with the real CPU count. With item 3 they would have refused on that
runner. `run_workflow_control`, `selftest_validation_transcript` (`:6158`) and
`drive_validation_with_actions` (`:8194`) now pin 128 CPUs. Two expectations that read
`job_cpu_ranges`/`container_cpuset` outside the pin are now literals (`:6427`, `:6195`). The
self-test passes at 1, 2, 3, 4, 7, 8, 19, 20, 39, 40 and 128 simulated CPUs
(`receipts/r2/selftest-hosts.txt`). Mutant N19 (harness pinned to 4 CPUs) proves the pin is
needed.

Other code touched: `JOB_CPU_RANGE_EVENTS` comment (`:133-135`); `container_cpuset` docstring
(`:4633`); `job_cpu_range_monitor` docstring and `read_cpus` (`:5576`, `:5607`). The interrupt
probe's requirement (`:15078`) is unchanged and now reads the inspect-confirmed `moved`.

Docs (`docs/testing/CI_WORKFLOWS.md` at `5ba8313a`):

- `:1554-1558`: the interrupt gate's move is the one inspect shows.
- `:1746-1771`: reservation until `destroy`, `die` frees nothing, uncertain moves stay reserved,
  and inspect-read placement.
- `:1783-1786`: slot 0 refuses too.
- `:1794-1815`: the new summary line, and the failure-safe shutdown with its containment hold.
- `:1816-1847`: the self-test pins.
- `:2133-2143`: slot 0 refusal and mixed runner versions.

### Summary line (changed; the post-merge reading uses it)

```text
act-ci: <workflow>: CPU ranges: <n> job container(s) created: <m> seen on a range of their own by docker inspect, <g> removed before that, <s> never seen on one; at most <k> held a range at once
```

Post-merge expectation for a full `rtl-full` replay: `m == n` (12 when the gate selects the full
run), `g == 0`, `s == 0`, `k == 4`, and no `act-ci: WARNING: rtl-full: CPU ranges:` line. The plan
line, the CPU sets per slot and per concurrent container, and the disjointness proof with its
planted overlaps are unchanged from Round 1 (tables below).

### Dry run (unchanged lines, regenerated at `5ba8313a`)

The offline harness is the same driver as Round 1: the real `run_validation(..., dry_run=True)`
with GitHub, git, the slot daemon and the Docker boundary stood in. Its output is in
`receipts/r2/dryrun-offline.txt` (6865 B, sha256
`31dd3826c498da477b768708c6d147ac66de8ad6958bd1b8b099d84839a2fdf9`). Both slots return rc 0, and
the plan lines are byte-identical to Round 1:

```text
===== slot 0: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19
===== slot 3: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71 --cpuset-cpus=72-75 --cpuset-cpus=76-79
```

### Gates at `5ba8313a` (all rc 0; CPython 3.12.3, PyYAML 6.0.3, pinned Markdown renderer)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | `selftest: PASS`, 490 ok, 0 FAIL (was 477); also 490/0 on the host's CPython 3.14.7 |
| `python3 scripts/ci_events.py --check` / `--selftest` | OK, 2016 contract items / PASS, 2828 arms |
| `scripts/act_slot_proof.sh --selftest` | PASS, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | every ratchet holds (long function 9 <= 9, too many parameters 7 <= 7, over-long line 0 <= 0) / 54 PASS |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | 0 findings / 700 arms PASS |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_doc_style.py` | OK |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` | OK / 480 links |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | 0 findings over 120 added lines |
| `python3 scripts/check_doc_paths.py` | OK, 964 paths |
| `git diff --check dc4d06cb` | clean |

Receipts (`receipts/r2/`, hashed in `receipts/r2/SHA256SUMS`):

- `act-ci-selftest.log`: 43312 B, sha256
  `80b90c874668606c08e981242043adee150bd1c294cecb41d992bf5eace15c17`.
- `gates.txt`: every gate's rc and last line.
- `selftest-hosts.txt`: the CPU-count sweep.
- `mutants-r2.txt` and `mutants_r2.py`.
- `r632-mutants-rerun.txt`.
- `dryrun-offline.txt`.
- `run_code_gates.sh` and `run_doc_gates.sh`.

`ci-events-selftest.log` was not copied: 184068 B, sha256
`c6b497eb75665fd129d7bdb0dbd39b65b62d3fce837704da7526626059658551`.

### Mutation evidence (scratch copies of the head tree; each must fail `--selftest`)

Round 2 mutants (`receipts/r2/mutants-r2.txt`): 21 of 21 killed.

| Mutant | Arms failed |
| --- | --- |
| N01 `die` frees its range | 3 |
| N02 timed-out move released | 3 |
| N03 refused move released | 1 |
| N04 no inspect when every range is held | 1 |
| N05 move trusted without inspect | 4 |
| N06 `start` not inspected | 1 |
| N07 late `update` not inspected | 1 |
| N08 reap failure skips the join (R633-1-F4) | 2 |
| N09 join failure not retried | 1 |
| N10 slot-0 fallback restored (R633-1-F3) | 1 |
| N11 `start` without `create` ignored | 1 |
| N12 cleanup failure swallowed | 3 |
| N13 poll failure unguarded | 1 |
| N14 join before containment | 6 |
| N15 reserved counts as moved | 1 |
| N16 gone not counted | 1 |
| N17 off-target read not reported | 2 |
| N18 pipe left open after a failure | 2 |
| N19 harness host pinned to 4 CPUs | 1 |
| N20 planted act exit ignored | 1 |
| N21 held ranges ignored | 9 |

R632-1's own `mutants.py` re-run at this head (`receipts/r2/r632-mutants-rerun.txt`):

- 19 killed, including M13 (reader not joined), M16, M17 and M23, all four of which survived at
  `eb566634`.
- M18 (interrupt move not required) still survives. It is pinned only by the live
  `--interrupt-selftest`, which this lane may not run. R632-1 recorded this as a limit, not a
  finding.
- M08, M09, M20 and C24 are INVALID, because their anchors no longer exist. M08 (no free on
  `die`) and C24 (free on `destroy` only) describe what is now the intended behaviour. M20 hit the
  removed fallback, and N10 now covers it. M09's equivalent is N21.

### Material decisions (public in REVIEW READY)

- **Uncertain moves stay reserved until `destroy`.** This is stricter than "until an inspect shows
  the effective cpuset". An inspect showing the staging range after a timed-out update does not
  release the target, because the daemon may still apply that request (R633-1's
  delayed-completion case). Releasing there would let the late completion land on a range already
  given to the next container. The cost is one range idle for that container's life, which is a
  warning, never a verdict.
- **Summary semantics.** "moved" now means seen on its range by `docker container inspect`. The
  Round 1 count "started on the staging range before the move" is gone, because it was inferred
  from event order. It is replaced by `<g> removed before that` and `<s> never seen on one`
  (R632-1 S4).
- Each container now costs one extra `docker container inspect` after its move and one at each
  `start`. With four near-simultaneous creates, the fourth is moved about 3 CLI round trips
  later than in Round 1. Not measured (no live daemon in this lane).

### Not done, and why

- Acceptance 3's same-head verdict comparison, acceptance 4 and acceptance 5 are post-merge, per
  the ruling. `Relates to #730`, not `Closes`.
- No live `docker events`, `docker container update` or `docker container inspect` has run in
  this lane. The first live exercise is the post-merge replay, or `--interrupt-selftest` on slot
  0, if the manager allows it.
- Not touched: two runner directories under `/tmp` (`milan-act-ci-a004...`, from 2026-10-12
  22:02 local, written at 23:05; `milan-act-ci-b507...`, from 2026-10-11, about 830 MB each).
  They come from replays outside this lane. Every dry run and self-test of this lane cleaned up
  after itself.

---

# Round 1 (history)

Superseded by Round 2 where they differ:

- a `die` no longer frees a range;
- a failed move keeps its range;
- slot 0 refuses a small host instead of falling back;
- the summary line changed.

The CPU sets per slot and per container, the disjointness proof, the dry-run plan lines and the
replay table below still hold.

Status: REVIEW READY at `eb5666349fc20ed3b5437a4357ef097c1231e557` (not pushed; push and PR
creation are outside this lane). Issue #730. Posted:
https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6132134158

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131408752
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131500852
- Ruling (no replays in this lane; measurement after the merge):
  https://github.com/kebag-logic/milan-fpga/issues/730#issuecomment-6131815815
- Branch `730-act-cpusets` from dev `dc4d06cb`; origin
  `https://github.com/kebag-logic/milan-fpga.git` confirmed; committer identity unchanged.
- Commits (one-line, no body, no trailers):
  - `7bb36e09` Give each concurrent act job container its own CPU range, derived from
    max-parallel and CONCURRENT_JOB_LIMIT (#730)
  - `eb566634` Document the per-container CPU ranges of act replays and their derivation (#730)
- Files (`git diff --stat dc4d06cb HEAD`): `scripts/act_ci.py` and `docs/testing/CI_WORKFLOWS.md`,
  1062 insertions, 66 deletions.
  No workflow, suite, testbench, RTL or firmware file touched.
- `PR-BODY.md` beside this file; receipts in `receipts/`.

## Resume note

The 22:10 stop left uncommitted `scripts/act_ci.py` edits: the derivation, the range layout,
the event monitor and its wiring. They were reviewed against act 0.2.89's source and kept.
Missing at resume and added here: every new self-test arm, the update of the existing slot
arms to the new layout (`--selftest` crashed at resume: slot 1 was refused on the 8-CPU mock
host), two over-long lines (Rule 12), the dry-run arm, and the documentation.

## How it works

act 0.2.89 passes one `--container-options` word to every job container
(`pkg/runner/run_context.go` `rc.options`), so no act option gives two legs different CPUs.
The word's cpuset becomes a staging range. While act runs, the runner streams
`docker events` filtered to its own ownership label and moves each job container, at its
`create`, to the lowest free job range with `docker container update --cpuset-cpus`. A
`die`/`destroy` event frees the range. act runs with `--rm`, so each leg's container is removed
before its worker takes the next leg (`pkg/runner/job_executor.go`, stop container
executor), and `die` precedes the next `create` in the daemon's order. Service containers and
Docker actions also carry the options word, but the sandbox already refuses both
(`validate_workflow_sandbox`), so only job containers carry the label. The slot slice sets only
`MemoryMax` (no `AllowedCPUs`), so a move out of the staging range is permitted.

## Changes (file:line at `eb566634`)

| Where | What |
| --- | --- |
| `scripts/act_ci.py:122` | `ACT_DEFAULT_MAX_PARALLEL = 4`: act 0.2.89's own default (`pkg/model/workflow.go` `GetMaxParallel`) |
| `scripts/act_ci.py:129` | `SLOT_JOB_RANGES = CONCURRENT_JOB_LIMIT * ACT_DEFAULT_MAX_PARALLEL`: job ranges a slot is spaced for |
| `scripts/act_ci.py:134` | `JOB_CPU_RANGE_EVENTS`: the five container events the monitor reads |
| `scripts/act_ci.py:2041` | `job_container_width`: 1 without a matrix; else literal `max-parallel` (min 1) or 4; unreadable is a Refusal |
| `scripts/act_ci.py:2070` | `replay_container_concurrency`: per workflow, the `CONCURRENT_JOB_LIMIT` widest jobs summed; max over workflows |
| `scripts/act_ci.py:4602` | the slot banner says "staging CPUs" |
| `scripts/act_ci.py:4622` | `slot_cpu_base`: slot N's block starts at `N * 5 * 4 = 20N` |
| `scripts/act_ci.py:4631` | `container_cpuset`: the staging range (slot 0 unchanged; slot N `20N..20N+3`) |
| `scripts/act_ci.py:4655` | `cpu_range_overlaps`: the overlap finder used by the guard and the proof |
| `scripts/act_ci.py:4669` | `job_cpu_ranges`: the derived job ranges; >4 or <1 refused; isolated slot on a small host refused; slot 0 falls back to `()` |
| `scripts/act_ci.py:4711` | `describe_job_cpu_ranges`: the printed plan line |
| `scripts/act_ci.py:5306` | `JobCpuRanges`: event parsing, placement, freeing, counters, problems |
| `scripts/act_ci.py:5417-5533` | `read_job_cpu_events`, `stop_job_cpu_range_monitor`, `job_cpu_range_monitor`: own session, containment ladder and join before Docker teardown on every exit |
| `scripts/act_ci.py:5535` | `report_job_cpu_ranges`: summary line; problems as warnings, never a verdict |
| `scripts/act_ci.py:5563` | `WorkflowPlan.cpu_ranges` |
| `scripts/act_ci.py:5624` | `execute_workflows`: act runs inside the monitor |
| `scripts/act_ci.py:5682-5683, 5710` | `run_validation`: derive and allocate before the slot is entered; print the plan |
| `scripts/act_ci.py:14389-14398` | interrupt probe: runs under the monitor and requires its container moved |
| `scripts/act_ci.py:6846, 6905, 6924, 6975, 7035, 7123, 7165, 13376, 13433, 6074` | new self-test arms and helpers (below) |
| `scripts/act_ci.py` slot arms | `selftest_slot_selection`, `selftest_slot_act_command`, `selftest_slot_guards`, `selftest_slot_validation_path` moved to the new numbers |
| `docs/testing/CI_WORKFLOWS.md:1554-1557` | interrupt gate runs under the monitor |
| `docs/testing/CI_WORKFLOWS.md:1726-1812` | replica shape: staging range, monitor, derivation, plan line, self-test pins |
| `docs/testing/CI_WORKFLOWS.md:2098-2105` | slot resource bounds: slot N owns `20N..20N+19` |
| `docs/testing/CI_WORKFLOWS.md:2315` | slot self-test list: CPUs disjoint at the most concurrency |

## CPU sets, old and new (128-CPU host)

Old (`dc4d06cb`): every job container of a slot on one range, shared by all concurrent legs.

| Slot | Old: every container | New: staging (create) | New: concurrent containers 1, 2, 3, 4 |
| --- | --- | --- | --- |
| 0 | `0-3` | `0-3` | `4-7`, `8-11`, `12-15`, `16-19` |
| 1 | `4-7` | `20-23` | `24-27`, `28-31`, `32-35`, `36-39` |
| 2 | `8-11` | `40-43` | `44-47`, `48-51`, `52-55`, `56-59` |
| 3 | `12-15` | `60-63` | `64-67`, `68-71`, `72-75`, `76-79` |
| N | `4N..4N+3` | `20N..20N+3` | `20N+4..20N+19`, four ranges of 4 |

A run uses only the ranges it derives: shipping `rtl-full` 4; `docs`, `elaborate`, `rtl-fast` 1
(job range 1 only). Every range is 4 wide, so `nproc` stays 4. `--memory=16g
--memory-swap=16g` and `MemoryMax=24G` are unchanged. Slot 0 on a host under 20 CPUs keeps
all four `rtl-full` legs on `0-3` (pre-#730 behaviour, printed); an isolated slot refuses.
On 128 CPUs, slots 1-5 fit any shipping workflow and slot 6 fits one-container workflows
(before, CPU-wise, slots 1-31).

## Disjointness proof and planted overlaps

`max_concurrency_cpu_layout` (`scripts/act_ci.py:6905`) builds every slot 0-63 at
`SLOT_JOB_RANGES` containers on a host with exactly the CPUs slot 63 needs (1280);
`selftest_cpu_layout_disjoint` (`:6924`) checks 320 ranges, each 4 wide, with
`cpu_range_overlaps(...) == []`. Planted, and each must fail:

- across slots: `slot_cpu_base` patched to the pre-#730 `slot * 4` spacing; the proof reports
  `slot 0 job range 0 and slot 1 staging share CPU 4`;
- within a slot: `job_cpu_ranges` patched to the pre-#730 shape (every leg on the slot's one
  range); the proof reports `slot 0 staging and slot 0 job range 0 share CPU 0`, and leg
  against leg `slot 0 job range 0 and slot 0 job range 1 share CPU 0`;
- runtime guard: a staging range planted on the first job range makes `job_cpu_ranges` refuse.

Mutation checks (scratch copies of `act_ci.py`, each must FAIL the self-test; all did):

| Mutant | FAIL arms |
| --- | --- |
| old `slot * 4` spacing | 11 (incl. the max-concurrency proof) |
| every container moved to range 0 | 2 |
| `max-parallel` ignored | 2 |
| `CONCURRENT_JOB_LIMIT` ignored | 1 |
| `die` does not free | 2 |
| monitor not stopped when the body raises | 1 |
| act run outside the monitor | 4 |
| runtime overlap guard removed | 1 |
| plan line without the job ranges | 4 |
| event stream without the owner-label filter | 1 |

## Dry-run output (ruling item 2)

A live `--dry-run` is not daemon-free, so it was not run (see Conflicts). The output below is
the real `run_validation(..., dry_run=True)` with only GitHub, git, the slot daemon and the
Docker boundary stood in (`dry_run_transcript`, `scripts/act_ci.py:13376`; driver
the scratch `dryrun_offline.py`; full text `receipts/dryrun-offline.txt`,
6865 B, sha256 `b51c2215a080e81b69302f69ec2affdca2caed01f1b04146c82c71133380fbba`). The
shipping `rtl.yml` was read for real; 128-CPU host:

```text
===== slot 0: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19
act-ci: rtl-full: /trusted/act pull_request ... --concurrent-jobs 1 --container-options '--label=org.kebag-logic.milan-act-ci.owner=<token> --cpuset-cpus=0-3 --memory=16g --memory-swap=16g' ...
===== slot 3: rc=0
act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=60-63, then moved to a free one of --cpuset-cpus=64-67 --cpuset-cpus=68-71 --cpuset-cpus=72-75 --cpuset-cpus=76-79
act-ci: rtl-full: /usr/bin/sudo -n -- /usr/bin/nsenter --net=/run/netns/milan-act-slot-3 -- ... --cpuset-cpus=60-63 --memory=16g --memory-swap=16g' ...
```

The self-test arm `selftest_dry_run_cpu_ranges` (`:13433`) asserts the same two lines.

## Gates (all rc 0, at `eb566634` unless noted; interpreter CPython 3.12.3 + PyYAML 6.0.3 + `tools/markdown/requirements.txt`)

| Command | Result |
| --- | --- |
| `python3 scripts/act_ci.py --selftest` | `selftest: PASS`, 477 ok, 0 FAIL (also PASS on the host's 3.14) |
| `python3 scripts/ci_events.py --check` | OK, 2016 contract items |
| `python3 scripts/ci_events.py --selftest` | PASS, 2828 arms |
| `scripts/act_slot_proof.sh --selftest` | PASS, 44 cases |
| `python3 scripts/check_py_idiom.py` / `--selftest` | ratchets hold (over-long line 0) / 54 PASS |
| `python3 scripts/check_baremetal_only.py --check` / `--selftest` | 0 findings / 700 arms PASS |
| `python3 scripts/docs_check.py` | 0 findings |
| `python3 scripts/check_doc_style.py` / `--selftest` | OK / OK |
| `python3 scripts/gen_toc.py --check` / `--verify-anchors` / `--selftest` | OK / 480 links / 1501 arms |
| `python3 scripts/check_em_dash.py --base dc4d06cb` | 0 findings over 82 added lines |
| `python3 scripts/check_doc_paths.py` | OK, 964 paths |
| `git diff --check dc4d06cb HEAD` | clean |

Receipts (`receipts/`): `act-ci-selftest.log` 41117 B sha256
`779d7e60645e485aa94d73271d1e561a2e48c78f144611a78c71597ca348b07a`; `slot-proof-selftest.log`
4070 B `fc7d05d5...d92d9`; `py-idiom.log`, `py-idiom-selftest.log`; `dryrun-offline.txt`.
Not copied (size): `ci-events-selftest.log` 184068 B sha256
`c6b497eb75665fd129d7bdb0dbd39b65b62d3fce837704da7526626059658551` (scratch).

## Replays (acceptance 4): before and after

No complete replay exists in this lane. The slot-3 "before" replay of PR #728 at `2c2f3369`
(dev's runner) was stopped by the manager at 20:10 UTC (rc 130) for disk; slot 3's data-root
was deleted by the manager (the slot cache was removed). The lane's "after" replay was
never started (ruling).

| Run | Runner | Job | Wall clock | Slot memory peak | Verdict |
| --- | --- | --- | --- | --- | --- |
| before (partial, slot 3) | dev `dc4d06cb` | full-ci-gate | 20:02:42-20:02:57, 15 s | 15.1 GiB sampled `memory.peak` up to the stop | succeeded |
| before (partial, slot 3) | dev `dc4d06cb` | Verilator shards 0-3 | 20:02:57-20:10:36, cut by the stop | (same) | interrupted |
| before (partial, slot 3) | dev `dc4d06cb` | Verilator 4, Yosys 0-3 | started 20:10:36 inside the stop | (same) | interrupted |
| after | lane `eb566634` | all | not run (ruling) | n/a | n/a |

What the partial run does show is the defect's shape (`receipts/before-slot3-partial-samples.log`,
5846 B, sha256 `c68de136...efa4`; replay log 424948 B sha256
`d6c756d0a992fd09f951d82b7c0c34b00c777db5eb743b22ae487f1a268333aa`, scratch only). For 15
samples, four leg containers ran at once, every one with `cpuset.cpus` = `12-15`. Over the last
30 s interval they used 1.06, 0.94, 1.03 and 0.94 CPUs, about four CPUs in all, a quarter of a
hosted runner each.

### Post-merge measurement (ruling item 1): the command and the lines to read

The before replay is the manager's slot-0 record (#721 at `42678ae2`, #715 at `c7d0ad63`). The
after replay is the first manager replay on the merged runner, in the same form, from a clean
candidate worktree with the runner taken from a clean worktree at the merged dev tip:

```sh
python3 -I <trusted-dev>/scripts/act_ci.py --pr <number> --sudo --workflow rtl-full
```

Lines to read:

1. Plan, once per run:
   `act-ci: job container CPUs: up to 4 at once (max-parallel, CONCURRENT_JOB_LIMIT 1); each created on --cpuset-cpus=0-3, then moved to a free one of --cpuset-cpus=4-7 --cpuset-cpus=8-11 --cpuset-cpus=12-15 --cpuset-cpus=16-19`
2. Per job wall clock: from the job's first `[rtl-full/<job>] ⭐ Run Set up job` to its
   `[rtl-full/<job>] 🏁  Job succeeded` (or `Job failed`). act does not stamp these lines, so
   the log needs a per-line UTC stamp, as the recorded before logs have.
3. After the workflow: `act-ci: rtl-full: CPU ranges: <n> job container(s) created, <m> moved to a range of their own, at most <k> at once; <s> started on the staging range before the move`.
   Expect `m == n` (12 on a PR replay in which the gate selects the full run: gate,
   5 Verilator, verilator-suites, 4 Yosys, yosys-portability; physical-gptp runs only on
   schedule or dispatch) and `k == 4`. Also expect no `act-ci: WARNING: rtl-full: CPU ranges:` line.
4. Verdict: `act-ci: rtl-full: PASS at <sha>` or `act-ci: rtl-full: FAILED (<rc>)`, compared
   with the before replay's verdict at the same head (acceptance 3).
5. Memory: isolated slot only, `act-ci: slot N: memory peak <x> GiB of its 24G cap; the cap was hit <h> time(s), with no OOM at it`.
   Slot 0 has no slice, so its peak must be sampled on the host.
6. Optional host-side cross-check while four legs run (read-only):
   `docker ps -q --filter label=org.kebag-logic.milan-act-ci.owner | xargs docker inspect --format '{{.Name}} {{.HostConfig.CpusetCpus}}'`
   should list four different ranges.

Acceptance 5 (`CONCURRENT_JOB_LIMIT` 2) is deferred to the same post-merge measurement
(ruling item 3). With 2, `SLOT_JOB_RANGES` becomes 8, and each slot's block would be 36 CPUs.

## Acceptance status

| Item | Status |
| --- | --- |
| 1 own CPUs per concurrent container | Met in code. Proven offline by the self-test and the dry run; memory bounds unchanged; small host refused (isolated) or pre-#730 fallback (slot 0). Not yet exercised against a live daemon. |
| 2 derived, disjoint at max concurrency | Met: derivation from `max-parallel` and `CONCURRENT_JOB_LIMIT`; proof with planted overlaps. |
| 3 fidelity | No workflow, step or job change; every range 4 wide (`nproc` 4). Verdict unchanged on the same head: not shown in lane (no replay); post-merge. |
| 4 measured | Not in lane (ruling); command and lines above. |
| 5 optional | Deferred (ruling). |

Hence `Relates to #730`, not `Closes`.

## Conflicts and open risks

- **`--dry-run` is not daemon-free.** The ruling says "`--dry-run` and `--selftest` start no
  daemon", but `run_validation` enters `replay_slot` and `temporary_docker_boundary` under
  `--dry-run` too. In an isolated slot that starts the slot daemon and seeds the tool cache,
  which pulls the runner image (CI_WORKFLOWS.md, Parallel replay slots: "a `--dry-run` primes
  it", about 75 GB per slot). On slot 0 it creates the boundary and seeds on the default daemon,
  which the manager's live slot-0 replay was using. The ruling also says not to run `act_ci.py`
  against a live PR. So the dry-run output was produced offline, through the real dry-run code
  path. A daemon-free `--dry-run` would be a separate change (suggested new Issue).
- **Unexercised live.** No `docker events` stream or `docker container update` has run in this
  lane against a real daemon. The first live exercise is the post-merge replay, or
  `--interrupt-selftest` on slot 0 (default daemon, existing image), if the manager allows it
  before merge. That probe now also requires its container to have been moved.
- **Mixed runner versions overlap.** A slot run by a pre-#730 runner (`4N..4N+3`) can share CPUs
  with a slot run by this one (for example, old slot 1 `4-7` and new slot 0's job range 1). Run
  every slot from one runner version.
- **Transit on staging.** A container runs on the staging range between its `create` and its
  move; a start before the move is counted (`started on the staging range`). `nproc` is 4 either way.
- **New refusal.** A workflow deriving more than 4 concurrent containers (`max-parallel` over 4,
  or two wide jobs with `CONCURRENT_JOB_LIMIT` 2 and `SLOT_JOB_RANGES` unchanged) or an
  unreadable `max-parallel` is refused. No shipping workflow does this (self-test arm).
- **Fewer slots per host.** On 128 CPUs, slots 1-5 for any shipping workflow (manager uses 1-3).
- Scratch: the assigned disk directory (environment, act source, partial before log, mutation driver).
  `third_party/lwSRP` was not initialised (no gate needed it).

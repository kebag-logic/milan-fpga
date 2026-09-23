[R257] NEGATIVE - exact head b5ce20eca8b59709ec5bc6115e5e15bfc312f283

External independent review, round R257-1, of issue #523 / PR #526.

- Head `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`, tree `bfde1313250ae84105754af4b150325f55f5ef33`.
- Source base and live `dev` `483a133ed08867ea0d300d2b4a027b5b48a4282f` (a direct descendant, four commits).
- Cleared context. I rebuilt the task only from AGENTS/CONTRIBUTING, docs/README, the #523 body plus its manager/author comments (settled decision 5783211002), REQUIREMENTS REQ-VER-01/02/04, the diff and history, the public evidence at `6df2d51f`/`ad844b49`/`840fccb1`/`b9a05dc9`, and exact-head hosted check runs.
- No author private material and no other reviewer's report was read before this verdict and ledger were written.

Verdict: NEGATIVE. There is one open MAJOR and two open MINORs. Isolation of caller sources holds on every path I probed, including a hard KILL. The graceful INT/TERM cancellation of both drivers is correct. However, the new process-ownership layer makes a hard stop of the sweep *weaker* than at base: the real sweep keeps running detached, starts later suites and prints a completed PASS summary after its caller has seen the kill.

## Findings

### R257-1-F1 MAJOR - Conformance, RTL, Robustness, Tests, Docs

**Location:** `scripts/run_all_suites.sh:111`, `scripts/owned_process.py:207`, `scripts/owned_process.py:230-245`

**Title:** A hard stop of the launched sweep detaches the real sweep. It then starts later suites and emits a completed PASS summary.

**Authority:**
- The review bar for hard KILL: caller input unchanged and no completed success.
- #523 settled decision (issuecomment-5783211002): for the hard-kill path "no cleanup or completed-PASS claim may be made". Cancellation must "start no later suite".
- AGENTS section 6: Robustness ("reset during activity", invalid ordering); RTL/architecture ("existing module/interface contracts remain valid").

**Mechanism.** `run_all_suites.sh:111` `exec`s into `owned_process.py`. The PID the caller launched (and its process group) is therefore now a Python supervisor. That supervisor starts the real sweep shell with `start_new_session=True` (`owned_process.py:207`). Handled INT/TERM are forwarded correctly. Any signal the supervisor does not handle kills only the supervisor, and the sweep shell carries on as an orphan in its own session. That includes KILL, the terminal-hangup HUP and other default-fatal signals.

**Evidence.** I used `scripts/probe_sweep_hardstop.py`: the production fixture (real driver, selector and tally; synthetic make) with a signal at the published first-suite command handshake. The held command is released only after the caller has observed the death.

| Receipt | Caller status | Sweep shell survives | Later suite started | Completed summary after death |
|---|---|---|---|---|
| `receipts/hardstop-head-KILL.txt` | -9 | yes | yes | `PASS alpha`, `PASS omega`, `suites: 2 passed: 2 failed: 0`, `checks: 2 in-suite failures: 0` |
| `receipts/hardstop-head-HUP.txt` | -1 | yes | yes | same |
| `receipts/hardstop-base-KILL.txt` (base driver blob `2a02c7f3`) | -9 | no | no | nothing |
| `receipts/hardstop-base-HUP.txt` | -1 | no | no | nothing |

Raw results are in `receipts/raw/hardstop-*/result.json`.

**Impact:**
- `kill -9`, `timeout -s KILL ...`, a closed terminal, or Ctrl-\ aimed at the sweep no longer stops it. Nor does a process-group kill of the caller's job.
- The sweep keeps holding the tree lock, so the next sweep refuses with 91.
- It keeps writing the caller's `<outdir>` logs, so "partial" logs silently become complete ones.
- It appends a completed success summary to the caller's captured output after the caller already recorded a kill.
- Later suites also run. `tsn_fuzz`, for example, rewrites tracked `TEST_RESULTS.md` files (`tb/verilator/tsn_fuzz/cosim.py:141,201`), so caller files can change after the kill.
- Base did none of this.
- The committed tests cover INT/TERM only (`scripts/test_suite_cancellation.py:232-236`), so the regression passes them.
- `docs/testing/TESTING.md:210-222` documents INT/TERM semantics but not that the launched PID is now a supervisor whose death detaches the sweep.

**Why each lens:**
- Conformance: the hard-kill bar and the decision above.
- RTL: the driver's external process contract changed; there is no RTL in this PR.
- Robustness: the hard-stop path.
- Tests: no hard-stop arm.
- Docs: the changed process contract is undocumented.

**Required outcome:**
- A hard or default-fatal stop delivered to the launched PID, or to its process group, must not let the sweep start a later suite or emit a completed summary or verdict. Parity with base is the minimum.
- The resulting hard-stop behaviour is documented.

**Verification:**
- Rerun `scripts/probe_sweep_hardstop.py` for KILL and HUP at the fixed head. `later_suite_started` and `completed_summary_after_death` must both be false.
- A committed deterministic handshake arm covers this, and restoring the current behaviour in a disposable control turns it red.

### R257-1-F2 MINOR - Conformance, Robustness, Tests, Docs

**Location:** `tb/verilator/gptp_shadow/private_inputs.py:84-87`

**Title:** The Git-environment allowlist refuses presentation-only variables. The real campaign and the `gptp_shadow` suite therefore go red in common environments.

**Authority:**
- #523 acceptance 4: the original gPTP shadow controls still run and detect their defects.
- Commit `37e43cdc` intends to accept presentation-only Git settings.
- AGENTS section 6 Robustness: configuration-dependent behaviour.

**Evidence:**
- `receipts/real-gptp-shadow-refused-git-editor.log`: the real `make -C tb/verilator/gptp_shadow` ran with the verified Verilator 5.050 in an environment exporting `GIT_EDITOR`. It printed lifecycle PASS and baseline `309 checks: 309 PASS, 0 FAIL`, then `REFUSED: Git environment overrides are not accepted: GIT_EDITOR`, and make exited 2.
- `receipts/git-env-head.txt` vs `receipts/git-env-base.txt` (production lifecycle fixture, real Git):

| Variable | Head | Base |
|---|---|---|
| `GIT_EDITOR`, `GIT_ASKPASS`, `GIT_AUTHOR_NAME`, `GIT_SSH_COMMAND` | exit 2, zero controls run | all nine controls run, exit 0 |
| `GIT_PAGER` | accepted | accepted |
| `GIT_INDEX_FILE`, `GIT_DIR` (real redirects) | refused, correctly | ran |

None of the four refused variables can alter `ls-tree`/`ls-files`/`rev-parse` identity. The only positive control is `GIT_PAGER` (`test_mutant_lifecycle.py:88`). The README (`tb/verilator/gptp_shadow/README.md:94-96`) does not state this precondition.

**Impact:**
- The suite reports FAIL, and the nine controls do not run, for any developer whose shell or IDE terminal exports such a variable.
- This is fail-closed and diagnosable, with no false pass. It is still a manufactured red on a previously green suite, behind an undocumented environment precondition.

**Required outcome:**
- Variables that cannot redirect the repository, index, objects, configuration or captured output of the identity checks do not prevent the campaign.
- Redirecting variables stay refused, or are shown to be neutralised with caller input unchanged.
- The rule is documented and both sides of the boundary are controlled.

**Verification:**
- `scripts/probe_git_env.py` at the fixed head: presentation-only variables give exit 0 with nine controls, and redirects stay refused or neutralised.
- The real make passes with `GIT_EDITOR` exported.

### R257-1-F3 MINOR - Robustness, Tests, Docs

**Location:** `scripts/owned_process.py:58-69,243`, `tb/verilator/gptp_shadow/mutants.py:265`

**Title:** Missing process facilities produce a traceback and exit 1, not the documented refusal.

**Authority:**
- `docs/testing/TESTING.md:216-217`: "Unsupported process facilities are refused before commands start".
- `mutants.py` docstring: exit 2 means an input or cleanup refusal.
- The sweep's exit contract: `1..89` means that many suites FAILED.

**Evidence:** `scripts/probe_unsupported.py` gives:
- no `prctl` (a C library without it): `AttributeError` traceback, status 1 (`receipts/unsupported-no-prctl.txt`);
- no `os.pidfd_open`: `AttributeError`, status 1 (`receipts/unsupported-no-pidfd.txt`);
- a *failing* `prctl` call: the only case with the documented `REFUSED: process ownership ...`, exit 2 (`receipts/unsupported-prctl-fails.txt`).

No command started in any case. `main()` catches only `OSError`/`RuntimeError`.

**Impact:** On a host lacking these facilities (non-Linux, or an interpreter without pidfd support), the sweep exits 1, which its own contract reads as "one suite failed". The campaign exits 1, "a control was not caught". The documented refusal does not happen. The host population is narrow, and commands never start.

**Required outcome:** Absence of a required facility produces the documented refusal (a REFUSED diagnostic, exit 2) from both entry points, or the documentation states the actual behaviour. A control covers it.

**Verification:** `scripts/probe_unsupported.py` at the fixed head: all three modes exit 2 with REFUSED, and no command started.

### Suggestions (do not affect coverage)

- **R257-1-S1 (Docs, RTL):** `tb/verilator/gptp_shadow/Makefile:4` changes the default Verilator build parallelism from `-j 0` to `VERILATOR_JOBS ?= 4`. The repo convention elsewhere is `?= 0` (`tb/verilator/milan_dp/Makefile:14`, `tb/verilator/milan_dp_render/Makefile:35`). The PR description does not mention the new default. State the reason, or keep the convention.
- **R257-1-S2 (Docs):** On cancellation before log preparation, the shell says "logs were not prepared for this invocation", and the supervisor's next line (`scripts/owned_process.py:240`) says "partial logs retained" (`receipts/lock-wait-INT.txt`). Make the supervisor line conditional, or neutral.
- **R257-1-S3 (Tests):** 19 disposable mutation probes (`receipts/mutation-probes.txt`, `.json`) show where the refusal arms prove aggregate refusal rather than the named mechanism:
  - The linked-directory check, the Git-environment refusal, the pin comparison and the index-vs-HEAD comparison can each be removed with the lifecycle test still green (M04-M07). The corresponding arms are still refused, by an overlapping check.
  - The `^`/`$` anchors of both new bare-metal masks are not pinned by any arm (M17).
  - SIGSTOP-before-forward (M18) and a zombie-aware cleanup return (M15) are not pinned either.
  - Asserting the specific refusal reason per arm would make each mechanism load-bearing.

## What was verified and holds at this head

- **Private inputs** (`private_inputs.py`):
  - Only files named by HEAD's tree (and the pinned dependency trees) are copied. Index must equal HEAD, and nothing unknown may sit in scope.
  - Each file is `lstat`-checked as a regular, non-linked file, hashed as a Git blob over the exact copied bytes, and its executable bit is checked.
  - Copies are written as new files in a fresh private directory.
  - Refusal arms pass for dirty, staged, assume-unchanged, skip-worktree, mode-only, untracked, extra, symlink, parent-link, dependency-hidden, off-pin, removed pin index, dependency-link and Git-env; caller snapshots are unchanged.
  - A hard-link copy mutant (M01), a no-byte/mode-check mutant (M02) and a no-unknown-refusal mutant (M03) are each detected.
- **Mutation tables:** `MUTATIONS` (9), `NOT_SEPARATELY_OBSERVABLE` (6), `TALLY_RE`, `suite_failed`, `apply_control` and the alternate-failed-check fallback are AST-identical to base (`receipts/mutation-tables.txt`). Counting a build failure as detection is caught (M14).
- **Real campaign** (`receipts/real-gptp-shadow.log`; verified Verilator 5.050, `usr/bin/verilator_bin` sha256 `44898b22...` equal to the manager record, `receipts/verilator-identity.txt`):
  - lifecycle PASS, baseline 309/309;
  - six named detections plus three by the original alternate-failed-check path;
  - six notes, `controls: 9 failures: 0`, RESULT PASS, 261 s;
  - private scratch removed; caller clone unchanged.
- **Real driver interrupted at a live build boundary** (mutation present in the private copy and Verilator/compiler/simulator descendant running; `receipts/real-interrupt-*.txt`):

| Signal | Exit | Private tree | Owned descendants | Verdict printed | Caller clone |
|---|---|---|---|---|---|
| TERM | 143 | removed | gone | no | integrity PASS |
| INT | 130 | removed | gone | no | integrity PASS |
| KILL | -9 | left behind | survived (then stopped by the probe) | no | integrity PASS |

- **Sweep graceful cancellation:**
  - The committed test passes (selection, preflight, command and transition for INT and TERM; next-suite sentinel; reaped identities including zombies; foreign sibling; ordinary, masked and timeout continuation; the unsafe control).
  - Independent probe during a `--wait` lock wait behind a foreign holder (`receipts/lock-wait-*.txt`): 130/143, no preflight or suite started, foreign holder identity and its owner record untouched.
  - Mutants that drop the subreaper (M08), KILL escalation (M09), the cancel traps (M11), the stale-log clear (M13) or restore the original cleanup trap (M12) are detected.
  - Process signalling uses pidfds with a (ppid, start-time) recheck. The PID-reuse arm (M10) was checked by inspection only.
- **Bare-metal masks** (`check_baremetal_only.py:273-274`): exact-file, per-line, anchored to one declaration.
  - The selftest grows from 342 to 354 arms (+12: one positive and five refusals per file).
  - A broadened mask (M16) is caught.
  - The gate reports 0 findings over 830 files (`receipts/gates/`).
- **Focused gates at head** (`receipts/gates/*.status`, all exit 0): Python and shell idiom plus selftests, test-evidence check and selftest, fail-fast, bare-metal check and selftest, docs, doc style, em-dash vs base, doc paths, contents, `bash -n`. Both focused tests passed as well (`receipts/focused/`).
- **Readiness digests** (`scripts/reconcile_readiness.py`, `receipts/readiness-reconciliation-check.txt`):
  - At `b9a05dc9` the nested SHA256SUMS refuses exactly six files: `mutation-kill.json`, `mutation-term.json`, `reproduce.py`, `results.json`, `sweep-term.json`, `sweep-term.stdout`.
  - Each is `path_redacted` in the outer immutable MANIFEST, whose `original_sha256` equals the nested entry and whose `published_sha256` equals the bytes.
  - All 22 outer rows match the reconciliation file at `6df2d51f`.
  - The `523-r1` evidence MANIFEST verifies 1120/1120 entries with no unlisted files (`receipts/evidence-manifest-check.txt`).
- **Hosted checks at the exact head** (`receipts/hosted-check-runs.txt`):
  - Verilator shards 0-4 and Yosys shards 0-3 executed and succeeded, as did `verilator-suites` and `yosys-portability`, `rtl-fast`, `docs-check`, `docs-check-no-git`, `elaborate`, `wire-accountability`, `verilator-lint`, `yosys-elaboration` and `bdd-conformance`.
  - Earlier same-head attempts are cancelled, or failed closed at the aggregates, and were superseded.
  - `Physical gPTP` is a skipped context, not hardware evidence.
- **Review clone:** its integrity snapshot before and after all probes is identical: 860 records, HEAD tree equals the index, every blob and mode matches, and there are no index flags. The three required submodules sit at their gitlinks (`c1b61743`, `424c688f`, `48ff7a7e`) with clean trees; `external` is uninitialised and not required. See `receipts/integrity-before.json` and `receipts/integrity-after.json`.

## Reviewer-owned lens ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2) | #523 acceptance 1-4 and decision 5783211002 against `run_all_suites.sh:106-125,243-258,436-441`, `owned_process.py`, `private_inputs.py`, `mutants.py:237-313`; REQ-VER-01/02/04 against `receipts/real-gptp-shadow.log`, `receipts/gates/`; the `receipts/hardstop-*`, `real-interrupt-*`, `git-env-*` probes | R257-1 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| RTL | UNCLEAN (F1) | No `hdl/` or gitlink change in `git diff 483a133e..b5ce20ec` (`receipts/integrity-*.json` gitlinks); `tb/verilator/gptp_shadow/Makefile` SRCS/VFLAGS unchanged except `-j`; process-ownership architecture `owned_process.py:49-227` and the exec/session boundary `run_all_suites.sh:111`, `owned_process.py:207` | R257-1 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Robustness | UNCLEAN (F1, F2, F3) | Hard stop (`receipts/hardstop-*`), real INT/TERM/KILL (`receipts/real-interrupt-*`), lock wait (`receipts/lock-wait-*`), Git environment (`receipts/git-env-*`), missing facilities (`receipts/unsupported-*`), refusal arms in `receipts/focused/lifecycle.log` | R257-1 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Tests | UNCLEAN (F1, F2, F3) | `test_mutant_lifecycle.py`, `test_suite_cancellation.py`, `process_test_support.py` and the bare-metal arms `check_baremetal_only.py:902-920`; runs in `receipts/focused/`; 19 mutation probes `receipts/mutation-probes.json`; arm count 342->354 `receipts/baremetal-base-arms.txt` | R257-1 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Docs | UNCLEAN (F1, F2, F3) | `docs/testing/TESTING.md:210-241`, `tb/verilator/gptp_shadow/README.md:84-116`, `mutants.py:1-31` docstring, `run_all_suites.sh:17-30` exit contract, `measure_test_evidence.py:603-606`; docs gates in `receipts/gates/` | R257-1 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |

No lens is covered clean at this head.

## Real limits

- **Not run** (not permitted): the full parent, processor, Yosys or builder banks; act; Docker; hardware.
- **Hosted:** I read check-run conclusions only, not job logs.
- **PID reuse:** the identity recheck was verified by code inspection. It cannot be exercised deterministically (M10).
- **Unsupported hosts** were simulated inside Linux Python by removing the facilities. No non-Linux host was used.
- **Redacted originals:** the pre-normalisation bytes of the six redacted readiness files are not public. Their reconciliation rests on the outer immutable manifest pairs.
- **GitHub Actions** job-cancellation signalling and heavy-contention timing were not exercised.
- **Normalisation:** receipts and scripts had only literal host path prefixes replaced (`$PACKET`, `$REVIEW_CLONE`, `$PINNED_TOOLS`, `$HOME`). Raw originals remain in unpublished scratch.

## Pending manager duties

- Author fixes for F1-F3.
- A fresh review at the new head, with every lens re-covered wherever a later commit touches it.
- A second independent positive review.
- Exact-head hosted and trusted-replica evidence for the new head.
- Final current-dev candidate validation.
- Maintainer-authorized merge and post-merge containment.
- Physical calibration NOT RUN. Field skips are not hardware evidence.

## Prior public review findings at this head

I checked only after the verdict and ledger above were written. Neither the PR #526 thread (comments, reviews, inline comments) nor the #523 thread has any reviewer-published finding. The internal round R256-1 ended without a verdict or findings (manager comment 5788418380), and R256-2 had published nothing. There is therefore nothing to resolve or retain.

One implementation-stage defect was reported publicly by the author (#523 comment 5783610479): escalation could kill the sweep shell before its EXIT trap removed the lock owner file. It is resolved at this head. The committed transition and command controls assert that the lock owner file is removed after INT/TERM, and they pass in `receipts/focused/cancellation.log`.

R257-1 FINISHED

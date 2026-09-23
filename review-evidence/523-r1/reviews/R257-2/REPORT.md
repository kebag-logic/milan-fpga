[R257] NEGATIVE - exact head 26353960ae2763cc09741d0f7bcc720621bd5148

External independent review, round R257-2, of issue #523 / PR #526.

- Head `26353960ae2763cc09741d0f7bcc720621bd5148`, tree `b250c4b9445f6d6645d56941fbe388257f1d60e3`.
- Source base `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d`. The head descends from it through the conflict-free merge `86149f2b`, whose tree equals `git merge-tree --write-tree b5ce20ec 776bc77d` (`c0ad43e5`).
- Live `dev` is `574c29fa111c74e5e5ed63e4670aff1f492e28e2`. The current-dev candidate is manager-owned and was not reviewed here.
- Cleared context, in this order: AGENTS/CONTRIBUTING, docs/README, the #523 body (frozen acceptance 1-4), the settled decision 5783211002 and the manager comments, REQ-VER-01/02/04, `git diff 776bc77d..26353960` and its history, then the public evidence, including the correction-a189 packet at `6d033ff5`.
- Prior public findings (R256-2, R257-1) were read only after my own pass over the diff and my probes. I read no private author material and no report from the concurrent round.

## Verdict

NEGATIVE: one open MINOR finding (Tests). No BLOCKER or MAJOR is open.

Both shared MAJORs are fixed at their root, and my own process probes confirm it.

- Every command the owner launches is bound to it by a parent-death KILL plus an owner-still-parent check. A hard stop of the sweep entry, or of its process group, now kills the sweep shell. No later suite starts, no summary is printed, and the in-flight suite may finish.
- Git variables that cannot redirect the checkout are accepted. The identity commands run with no `GIT_*` variable at all.

All other R256-2 and R257-1 findings are also resolved. The remaining defect is a test gap: the sweep's cancellation report says whether this invocation prepared any logs, and no test can fail when that report is removed or inverted.

## Findings

### R257-2-F1

```text
[R257] MINOR Tests - scripts/test_suite_cancellation.py:135-189 (behaviour at scripts/run_all_suites.sh:122-133,262-266) - The cancellation report that attributes partial logs to this invocation has no test that can fail
Requirement/evidence: docs/testing/TESTING.md:239 documents "Cancellation before log preparation reports that boundary explicitly". run_all_suites.sh:123-131 prints "partial logs: $OUT" only after prepare_logs sets LOGS_READY=1 (run_all_suites.sh:262-266), and "logs were not prepared for this invocation" otherwise. That report was added for attribution (commit b5ce20ec, "Keep cancelled preflight logs attributable to the current invocation"), and acceptance 3 requires "attributable partial logs". The cancellation arms assert only "CANCELLED:" in the output (test_suite_cancellation.py:171), and the owner's own line satisfies that. Four disposable single-defect copies of the head leave the unmodified test_suite_cancellation.py green (receipts/50-test-mutations.json): logs-ready-early (LOGS_READY=1 from the start), logs-ready-never-set, no-partial-logs-message, and no-term-trap (the shell's TERM report is gone). receipts/51-attribution-demo.txt: with TERM during a lock wait and OUT holding only a previous invocation's log, production prints "logs were not prepared for this invocation", while the logs-ready-early copy prints "partial logs: <OUT>".
Impact: The line that tells an operator whether OUT holds this run's partial evidence can regress in two ways without any gate noticing. It can present a previous run's completed logs as this run's partial logs, which is the misattribution b5ce20ec corrected. Or it can deny partial logs that exist. Production behaviour at this head is correct: in receipts/10-sweep-stops.json the lock-wait arms print the not-prepared line, and the preflight and command arms print "partial logs:".
Required change: The committed cancellation controls assert the shell's report at both boundaries and for both signals. Before log preparation (selection, lock wait), the not-prepared line appears and no "partial logs:" line. After preparation (preflight, command, transition), "partial logs: <requested OUT>" appears. The shell's own "CANCELLED: INT|TERM" line is asserted, not only the owner's line.
Verification: At the fixed head, `python3 scripts/probe_mutations.py <clone> <scratch> <out.json> 4 logs-ready-early,logs-ready-never-set,no-partial-logs-message,no-term-trap` reports all four DETECTED, and the unmodified test stays green.
```

Lens attribution: Tests only. The behaviour itself is correct and documented accurately, so Conformance, Robustness and Docs carry no open item for it.

### Suggestions (do not affect coverage)

- **R257-2-S1 (Tests), retained from R256-2 S1 and R257-1 S3, plus one new observation.** Two process guards are not pinned by any test:
  - stopping the root before forwarding the signal (mutant `no-root-notify`, owned_process.py:140-143);
  - running the sweep shell in its own session (mutant `no-new-session`, owned_process.py:258).

  Both survive (receipts/50-test-mutations.json). My probes showed no documented outcome that depends on either guard, so this is optional. The PID-reuse identity recheck (owned_process.py:231-241) remains verified by inspection only.
- **R257-2-S2 (Tests), retained from both prior rounds.** Both anchors of the two exact-line bare-metal masks (check_baremetal_only.py:273-274) can be removed with the selftest still `PASS (354 arm(s))` (receipts/gates/mask-anchor-mutants.txt). The author declined this publicly. Impact is limited to two workstation files.
- **R257-2-S3 (Robustness), retained from R256-2 S3.** When INT/TERM arrives while the final tally runs, the output ends `suites: 3   passed: 3   failed: 0   timed out: 0` and then the CANCELLED lines, with no check total and no logs line. Exit is 130/143 (receipts/12-sweep-suspend-and-summary.json, `summary-*`). The author keeps the status and the CANCELLED lines authoritative. Consider printing the count line after the tally.
- **R257-2-S4 (Robustness, Docs): decision on the author-disclosed job-control risk.**
  - Evidence: an uncatchable STOP of the entry at the first-suite handshake suspends only the owner, and the later suites still run (receipts/12, `suspend-SIGSTOP`). An interactive Ctrl-Z behaves the same way. My TSTP arm was discarded by the kernel because the probe's entry sits in an orphaned process group, so that arm does not represent a terminal.
  - Before this change, a suspend held the loop, though not the in-flight suite.
  - No requirement or settled decision covers suspend. Integrity and verdicts are unaffected. Forwarding TSTP/CONT to the shell's session, or one sentence in TESTING.md, would close it. This is optional.
- **R257-2-S5 (Robustness, Docs).** In ordinary workflows, Git itself exports variables that the campaign refuses by name, even though they point at the same checkout (receipts/20-git-exported-env.txt, receipts/21-git-env-arms.json):
  - `git rebase --exec` in a linked worktree (the lane layout CONTRIBUTING prescribes) exports `GIT_DIR`;
  - commit hooks export `GIT_INDEX_FILE`, plus `GIT_DIR` in a worktree;
  - `git -c k=v <alias>` exports `GIT_CONFIG_PARAMETERS`;
  - `git submodule foreach` exports `GIT_DIR`.

  In each of these contexts the suite fails with a named `REFUSED` (fail-closed, no false pass). Both prior rounds asked for redirects to stay refused, and README:107-111 documents the rule. The identity commands already run with no `GIT_*` variable (private_inputs.py:55-58), and `scripts/xvlog_gate.py:395-410` strips rather than refuses. Consider accepting a value that names this checkout, or listing these contexts in the README.
- **R257-2-S6 (Docs).** The PR body's Status still names source `6674c278`, not the head under review. The issue's A192 REVIEW READY comment does cover `26353960`, so evidence for a cold reviewer exists.

## Prior public findings at this head

| Prior finding | State at 26353960 | Root cause and evidence |
|---|---|---|
| R256-2 F1 / R257-1 F1 MAJOR, hard stop left a detached sweep | **RESOLVED** | The fix is at the root: owned_process.py:127-133 sets a parent-death SIGKILL in the forked child, then checks that the owner is still its parent, before every owned command (owned_process.py:257-260). Sweep probe, 32 arms (receipts/10-sweep-stops.json): the command, preflight and lock-wait phases; entry or group; KILL, HUP, TERM, INT, ALRM, USR1. Results: no later-suite sentinel ever ran, no summary, the shell gone within 5 s, the foreign sibling preserved, the lock reusable by a second sweep. Graceful arms: every owned identity, including a TERM-, INT- and HUP-ignoring detached grandchild, was gone when the caller saw 130/143. Real nested builds: TERM reaped 16 descendants (bash, timeout, make, verilator_bin, cc1plus...) in 0.37 s and removed the private tree (receipts/41). With KILL, the in-flight real campaign finished orphaned (`RESULT: PASS` in its own log only), the caller saw -9 and only the `shard:` line, no sentinel suite ran, and the lock was free afterwards (receipts/42). Documented at run_all_suites.sh:31-35 and TESTING.md:225-233. The committed hard-stop arms plus my `no-pdeathsig` and `pdeathsig-term-not-kill` mutants are red. |
| R256-2 F2 / R257-1 F2, Git variables refused the campaign | **RESOLVED** | REDIRECTS (private_inputs.py:29-33) refuses only redirecting names. `_git` scrubs every `GIT_*` (private_inputs.py:55-58). Real Git in a plain clone and in a linked worktree with real submodules gave 25 accepted arms, each byte-exact against the committed blobs, including a GIT_TRACE=1 stderr flood, glob/icase/noglob pathspec flags, a bogus GIT_EXEC_PATH, trace2 and presentation variables (receipts/21). The real `make -C tb/verilator/gptp_shadow` passed with GIT_EDITOR, GIT_PAGER, GIT_AUTHOR_NAME, GIT_TERMINAL_PROMPT, GIT_OPTIONAL_LOCKS and GIT_TRACE2_EVENT exported (receipts/real-suite/make.log). The `git-env-passthrough` and `drop-index-file-refusal` mutants are red. Residual observation: S5. |
| R256-2 F3 MINOR, refusal covered non-build files | **RESOLVED** | The population is `make print-inputs` plus local quoted includes (private_inputs.py:92-114): 22 files. On a real clone (receipts/22), rewritten TEST_RESULTS.md files, an untracked hdl file, a dirty unrelated tb/common header, the suite README and an unrelated axis file are all accepted. A dirty target, build input, header, axis input, gPTP input, ucode generator, suite Makefile, or an assume-unchanged target each refuses with its own reason. |
| R256-2 F4 MINOR, CONTRIBUTING prescribed a copied third_party | **RESOLVED** | CONTRIBUTING.md:10 and 287-292 now require initialised pins. No current page still prescribes `cp -r` of a submodule (grep outside docs/history). The copied layout is refused as "not at its pin" (receipts/22). |
| R256-2 F5 MINOR, Git stderr parsed as records | **RESOLVED** | `_read` parses stdout only, with stderr in a separate file (private_inputs.py:44-52). GIT_TRACE=1 arms are accepted (receipts/21). The committed garbled-record arm exits 2, and my `garbage-records-skipped` mutant is red. |
| R257-1 F3 MINOR, missing facilities gave a traceback | **RESOLVED** | `_prctl` resolves every facility before any state change (owned_process.py:51-63). Six new modes, beyond the author's four, all exit 2 with `REFUSED:`, no traceback and nothing started, at both entry points: pidfd_open ENOSYS as in a filtered container, SUBREAPER EPERM, and PDEATHSIG EPERM in the forked child (receipts/13). |
| R257-1 S1 / R256-2 S4, Verilator job default | RESOLVED | `VERILATOR_JOBS ?= 0` (Makefile:4). The default `-j 0` is unchanged. |
| R257-1 S2, contradictory owner line | RESOLVED | The owner prints a neutral `CANCELLED: signal N; no completed sweep result` (owned_process.py:294). |
| R257-1 S3 / R256-2 S1, guards not load-bearing | PARTLY | Refusal arms now assert the specific reason. The directory-link, pin, index and env guards each turn red (receipts/50). Still unpinned: SIGSTOP-before-forward and the mask anchors, retained as S1 and S2. PID reuse is by inspection only. |
| R256-2 S2 | RESOLVED | Same fix as R257-1 F3. |
| R256-2 S3, final-tally signal | RETAINED | Retained as S3 (receipts/12). |

## What was verified at this head

- **Acceptance 1**
  - The committed lifecycle unsafe controls (`private = REPO`) show caller change after TERM and after KILL at the mutation-applied handshake, with no sleep oracle.
  - The author tests pass at the head (receipts/author-tests).
- **Acceptance 2**
  - Real Git, disposable clone, 12 campaign arms: entry or group, with KILL, HUP, TERM, INT, ALRM or USR1 at the handshake (receipts/30).
  - The caller's bytes, modes and index were unchanged in every arm, including the submodules.
  - No later mutation started and no RESULT was printed.
  - Graceful arms: the make and the detached grandchild were gone at status, and the private tree was removed.
  - Hard arms: the direct make died within 5 s. Only the detached grandchild and the private scratch remained, as documented at README:121-122.
  - Real Verilator builds (receipts/40a): TERM exited 143 with 0 of 12 descendants alive at status. KILL exited -9 and the caller was unchanged.
- **Acceptance 3**
  - See the F1 resolution row: 32 fixture arms plus 2 real nested builds.
  - Partial logs are kept under the requested OUT, with stale logs cleared only after locking.
  - The attribution report is correct in production. Its lack of a test is F1.
- **Acceptance 4**
  - Real `make -C tb/verilator/gptp_shadow` with the scoped Verilator 5.050 (wrapper and `verilator_bin` sha256 `44898b22...` in receipts/real-suite/verilator-version.txt), VERILATOR_JOBS=8 and ordinary Git variables exported. Exit 0 in 277 s.
  - Lifecycle PASS, `309 checks: 309 PASS, 0 FAIL`, and nine detections: six named, three through the unchanged alternate-failed-check path.
  - Six notes, `controls: 9   failures: 0`, `RESULT: PASS` (receipts/real-suite/make.log).
  - MUTATIONS (9), NOT_SEPARATELY_OBSERVABLE (6), TALLY_RE, PLANE/RET/OBS/TIC, suite_failed and apply_control are AST-identical to base (receipts/31).
  - The full banks, two reviews, hosted checks and containment remain manager duties.
- **Scope**
  - 13 files change: none under hdl/, no gitlink, no #517 pool file, no suite deadline change. `git diff --stat 776bc77d..26353960 -- hdl gptp-processor protocol-processor third_party external` is empty.
  - The Makefile SRCS/VFLAGS change only in `-j $(VERILATOR_JOBS)`.
- **Focused static gates at the head** (receipts/gates/SUMMARY.txt): all 17 exit 0.
  - docs_check, em-dash against base and its selftest, doc style, doc paths, TOC check and anchors;
  - bare-metal `--check` and `--selftest` (354 arms);
  - fail-fast, test-evidence and its selftest, Python and shell idiom, ci_scope selftest;
  - `bash -n`, `make -n`.
- **Test power** (receipts/50): 24 single-defect copies of the head, 17 detected.
  - Detected: subreaper, KILL escalation, transitive census, parent-death binding, TERM-as-death-signal, INT trap, stale preflight clearing, relative OUT, env scrub, redirect list, mode check, index check, hardlink copies, include closure, garbage records, directory links, pin check.
  - Survivors: `no-toplevel-check` is redundant with the pin comparison and is not a defect. The two in S1. The four in F1.
- **Evidence integrity**
  - correction-a189: all 318 published digests match the outer MANIFEST.json `published_sha256`.
  - The nested SHA256SUMS equals `original_sha256` for all 317 entries. It refuses exactly the 150 `path_redacted` files (receipts/61).
- **Hosted, inspected only**
  - At the exact head, 21 check runs completed with success, including `rtl-fast`, `docs-check`, `docs-check-no-git`, `wire-accountability`, `elaborate`, `verilator-suites` (shards 0-4) and `yosys-portability` (shards 0-3).
  - `Physical gPTP` is a skipped context, not hardware evidence (receipts/60). Acceptance belongs to the manager.
- **Review clone**
  - Byte, mode, index and gitlink integrity was EXACT before and after every probe (receipts/00 and receipts/99): 866 records.
  - gptp-processor `c1b61743`, protocol-processor `424c688f` and verilog-axis `48ff7a7e` are at their pins, each its own top level with every blob verified. No index flags.
  - Ignored build products from my real run were removed, so `git status --ignored` is empty.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #523 acceptance 1-4 and decision 5783211002 against run_all_suites.sh:111-133,262-266; owned_process.py:94-280; private_inputs.py:29-197; mutants.py:238-316; receipts/10, 12, 13, 21, 22, 30, 31, 40a, 41, 42, real-suite/make.log; the 13-file scope with no hdl/, gitlink, #517 or deadline change | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| RTL | CLEAN | No hdl/ or gitlink change (empty scoped diff stat); gptp_shadow/Makefile:1-69 SRCS/VFLAGS unchanged except `-j $(VERILATOR_JOBS)` default 0; the process-ownership state machine owned_process.py:94-280 (latch, root stop, TERM, leaf-first KILL, root resume, reap, bounded failure, parent-death binding), traced and exercised in receipts/10, 30, 40a, 41, 42; real build 309/309 | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Robustness | CLEAN | Hard and graceful stops across phase, target and six signals (receipts/10); campaign stops (30); real-build stops (40a, 41, 42); suspend and final tally (12); missing and refused facilities (13); Git environment in clone and worktree (21); refusal scope and pin layouts (22) | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Tests | UNCLEAN (R257-2-F1 MINOR) | scripts/test_suite_cancellation.py, tb/verilator/gptp_shadow/test_mutant_lifecycle.py, scripts/process_test_support.py, check_baremetal_only.py:902-921 arms; author runs at the head (receipts/author-tests); 24 production mutants (receipts/50); 2 mask mutants (receipts/gates/mask-*) | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Docs | CLEAN | docs/testing/TESTING.md:210-255; tb/verilator/gptp_shadow/README.md:84-135; CONTRIBUTING.md:10,287-307; run_all_suites.sh:17-35 exit contract; mutants.py:1-31; measure_test_evidence.py:603-606; each claim checked against the probe receipts; docs gates (receipts/gates); issue and PR evidence including correction-a189 integrity (receipts/61) | R257-2 | 26353960ae2763cc09741d0f7bcc720621bd5148 |

No finding was moved to another Issue.

## Real limits

- **Not run** (not permitted): the full parent, PP, gPTP, Yosys and builder banks; Docker/act; host act_ci; hardware.
  - The manager's static/builder and native banks for this head were still running. I neither claim nor infer their results.
- **Synthetic parts:**
  - Sweep probes use the production sweep, owner, selector and tally with a synthetic `make` and stubbed prerequisites.
  - Real-build nested probes ran in disposable clones: other suites were removed, four prerequisite self-tests were stubbed and a sentinel suite was added. The gptp_shadow suite, the lifecycle test, test_suite_cancellation.py and the sweep ran unmodified.
  - My first nested attempt also stubbed test_suite_cancellation.py. That broke the lifecycle test's import and is kept as a reviewer fixture error (receipts/40-real-build-stops.txt). It was rerun correctly (receipts/41, 42).
- **Inspection only:** PID reuse and the owner-still-parent race cannot be triggered deterministically.
  - Real TSTP from a terminal was not exercised. The STOP arm stands in for it.
  - GitHub Actions cancellation signalling was not exercised.
- **Hosted:** I read check-run conclusions only, not job logs.
- **Process-hygiene incident, disclosed.** At about 11:10 CEST, a reviewer cleanup command matched processes by command line (`python3 -c "import time; time.sleep(900)"`) and sent SIGTERM to two of them.
  - One was this round's own leaked probe sibling.
  - The other (pid 1013249) was created after my probe had exited. I cannot attribute it to this round, so it may have belonged to a concurrent review's fixture.
  - Every other containment in this round selected exact recorded identities through pidfds. That includes the two stubborn fixture children leaked by the deliberately broken `no-subreaper` and `no-sigkill-escalation` copies (receipts/98).
  - Processes from the concurrent round's scratch were observed in a process listing and not touched. None of its content was read.
- **Normalisation:** host path prefixes in receipts are replaced by `<packet>`, `<clone>`, `<scoped-tool-bin>`, `<scoped-verilator-root>`, `<concurrent-packet>`, `<tmp>` and `$HOME`. The scratch directory is unpublished.

## Pending manager duties

- Author correction of R257-2-F1 (test assertions only). Then a re-review of the Tests lens at the new head, and of any other lens whose scope that commit touches.
- The second independent review, whose round is in flight.
- The manager's full source static/builder and native banks at the final head.
- Trusted serial replica and exact-head hosted acceptance for the final head.
- Final current-dev candidate validation. The source base is `776bc77d`; live dev is `574c29fa`.
- Maintainer-authorized merge and post-merge containment.
- Physical calibration NOT RUN. Field skips are not hardware proof.
- Tell the concurrent round about the SIGTERM incident above (pid 1013249, about 11:10 CEST). If that process was one of its foreign-preservation sentinels, an arm observing it may have failed for a reason outside the code under review.

## Receipts and scripts

Every published file is listed with its sha256 in MANIFEST.sha256. Portable probes are in `scripts/`:
- `verify_head.py`: integrity;
- `probe_sweep_stops.py`, `probe_sweep_extra.py`: sweep;
- `probe_campaign_stops.py`, `probe_real_nested.py`: campaign and real builds;
- `probe_git_env.py`, `probe_refusal_scope.py`: Git and inputs;
- `probe_facilities.py`: facilities;
- `probe_mutations.py`: test power;
- `compare_mutation_tables.py`: population.

Each takes the clone path and a scratch path as arguments.

R257-2 FINISHED

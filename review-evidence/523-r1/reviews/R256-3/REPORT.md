[R256] POSITIVE - exact head 26353960ae2763cc09741d0f7bcc720621bd5148

Round R256-3. Cleared-context internal independent review of issue #523 / PR #526.

- Head `26353960ae2763cc09741d0f7bcc720621bd5148`, tree `b250c4b9445f6d6645d56941fbe388257f1d60e3`.
- Source base `776bc77d1b06bf57f9c64ac8ac08ea37cab06e7d` (an ancestor of the head). Live dev `574c29fa111c74e5e5ed63e4670aff1f492e28e2`.
- All five lenses applied to the whole PR diff (13 files; 10 non-merge commits plus the conflict-free dev merge 86149f2b since the source base), not only to the correction commits.

## Verdict in one paragraph

Every finding of R256-2 (F1 and F2 MAJOR; F3, F4 and F5 MINOR) and R257-1 (F1 MAJOR; F2 and F3 MINOR) is resolved at its root at this head. My own real-process probes and Git-environment arms confirm this, and none of them imports the lane's test helpers.

- **Hard stop of the sweep entry.** KILL, HUP, QUIT, USR1 and ALRM to the entry, and KILL or HUP to its process group, now kill the sweep shell within 5 s. This holds at the preflight, command and transition boundaries. No later suite starts, no summary is printed and nothing is written after the caller sees the stop. Only the in-flight command may finish, as documented.
- **Git environment.** Ordinary variables, including what `git bisect run` and `git rebase -x` actually export, run all nine controls. Identity commands run with every `GIT_*` removed. Only the documented redirect/injection names are refused, each by name.
- **Graceful cancellation.** INT/TERM cancellation of the sweep and of the campaign returns 130/143 in 0.2-2.3 s. Every owned identity is gone and private scratch is removed. Foreign processes are untouched and caller sources are unchanged.
- **Hard stops and the campaign.** Caller sources also stay unchanged under KILL, HUP and QUIT of the campaign and of the sweep around a real compile.
- **Detections.** The real campaign under scoped Verilator 5.050 gives 309/309 checks and detects all nine mutations. Its detection lines are byte-identical to the base driver's in a disposable base checkout.

No BLOCKER, MAJOR or MINOR finding is open. Seven SUGGESTIONS follow; they do not affect coverage.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md sections 2, 3 and 6, docs/README.md authority order.
2. Issue #523 body (frozen acceptance 1-4), the settled decision (issuecomment-5783211002), READY TAKEOVER, and the executor TAKEN, implementation-detail and validation comments.
3. REQUIREMENTS.md REQ-VER-01/02/04.
4. `git diff 776bc77d..26353960` and its history.
5. The exact-head hosted check runs.
6. After my own pass: the R256-2 and R257-1 findings, the correction assignment, the A189 and A192 REVIEW READY comments, and `review-evidence/523-r1/correction-a189/HANDOFF.md` at `6d033ff5`.

I did not read private author material, lane scratchpads or management files. I did not read any other reviewer's report for this head, including anything under the evidence tree's `reviews/` directory. The prior findings were read only after my independent pass over the diff and my probes.

## Findings (all SUGGESTION; no coverage effect)

```text
[R256] SUGGESTION Robustness, Docs - scripts/run_all_suites.sh:111-120, docs/testing/TESTING.md:225-233 - A job-control stop (TSTP) of the entry pauses only the supervisor
Authority/evidence: receipts/probe-tstp.json. With the entry stopped (state T), the held suite completed and the later suites a2 and a3 ran; after SIGCONT the sweep exited 0 with its summary. At base, the launched shell itself stopped. The author disclosed this as an open risk needing a decision. It is outside acceptance 1-4 and the settled decision, and it produces no false verdict, no source change and no lock change.
Impact: an interactive user who suspends a sweep to relieve contention finds it still consuming CPU.
Required outcome (optional): forward TSTP/CONT to the shell's session, or state in TESTING.md that job-control suspension reaches only the supervisor.
Verification: a TSTP arm at the command handshake records whether a later suite runs while the entry is stopped.

[R256] SUGGESTION Robustness, Docs - scripts/run_all_suites.sh:234-235 - The lock record names the inner sweep shell, not the launched entry
Authority/evidence: `pid $$` is written by the shell running under the owner, so the REFUSING message prints the inner shell's PID. receipts/probe-sweep.json arm o-command-TERM-inner-shell: TERM to that PID left the entry and the held suite running 3 s later. The run then ended 143 only after the in-flight suite completed, with no later suite. The contract documents the launched process as the one to signal.
Impact: an operator who stops "the holder" by the printed PID gets a cancellation delayed by up to one suite deadline.
Required outcome (optional): record the entry's PID (or both) in the lock record, or say in the REFUSING text which PID to signal.
Verification: the refusal text names the PID whose TERM yields prompt 143.

[R256] SUGGESTION Tests - scripts/owned_process.py:141,236; tb/verilator/gptp_shadow/private_inputs.py:194-195 - Three guards have no independent control
Authority/evidence: receipts/probe-mutations.json. Removing the root SIGSTOP on cancellation (M05), the start-time recheck before signalling (M17) or the show-toplevel check (M19) leaves the owning test green. M05 and M17 are disclosed as inspection-only. M19 is redundant with the pin-revision check (M18 turns the test red), because a checkout without its own .git resolves the superproject's HEAD. The other 17 plants turn the owning test red.
Impact: none observed; the guards are defence in depth.
Required outcome (optional): an arm that isolates each guard, or a comment that marks it inspection-only.
Verification: removing each guard in a disposable copy turns its arm red.

[R256] SUGGESTION Robustness, Docs - tb/verilator/gptp_shadow/private_inputs.py:24-33 - Configuration-injection names are refused although the identity commands already scrub every GIT_* variable
Authority/evidence: receipts/probe-gitenv.json, where GIT_CONFIG_GLOBAL=/dev/null and a harmless GIT_CONFIG_PARAMETERS both refuse with exit 2. My empirical check with the local Git showed that a pre-commit hook exports GIT_INDEX_FILE, a linked worktree's hook also exports GIT_DIR, and any `git -c ...` wrapper exports GIT_CONFIG_PARAMETERS. In all three contexts the campaign refuses by name. The refusal is documented (README.md:107-113), fail-closed and consistent with both prior rounds' required outcome. The code comment's rationale, "its bytes could not be attributed", overstates the risk, because `_git` (lines 55-58) already runs without any GIT_* variable.
Impact: a named, loud refusal in hook or `git -c` contexts where attribution would in fact be sound.
Required outcome (optional): keep the policy and reword the rationale, or accept and scrub these names by a recorded decision.
Verification: the documented list and the code agree with the stated reason.

[R256] SUGGESTION Robustness, Docs - tb/verilator/gptp_shadow/mutants.py:258,298-301, Makefile:41-43 - The private build now runs under TMPDIR
Authority/evidence: by inspection, the private suite executes `./obj_dir/Vgptp_shadow_sim` inside TMPDIR. A TMPDIR mounted noexec, or too small, would fail every control closed as "no completed suite tally (make exit N)", without the build's own diagnostic. Not exercised: this host has no writable noexec mount.
Impact: a fail-closed but poorly explained red suite on hardened hosts.
Required outcome (optional): state the TMPDIR requirement in the README, and print the tail of a private build that produced no tally.
Verification: a TMPDIR without exec permission yields a message naming the cause.

[R256] SUGGESTION Docs - PR #526 description, "Status" - The PR body names source 6674c278 rather than the current head
Authority/evidence: the body gives `6674c278` and tree `8d634f12`. The head is 26353960 (A192's one-file follow-up, publicly recorded on the issue).
Impact: a cold reader of the PR alone sees a stale head.
Required outcome (optional): refresh the Status line at publication.
Verification: the PR body names 26353960 / b250c4b9.

[R256] SUGGESTION Robustness - scripts/run_all_suites.sh:419-425 (carried from R256-2 S3, declined by the author) - A signal during the final tally can leave the counts line printed before the CANCELLED lines
Authority/evidence: R256-2 receipts; not re-probed this round. Status 130/143 and the CANCELLED lines remain authoritative.
Required outcome (optional): unchanged from R256-2.
```

Observation, not a finding: the supervisor is a Python process, which ignores SIGPIPE, so a SIGPIPE sent to the entry neither cancels nor stops the sweep. In receipts/probe-sweep.json arm o-command-PIPE-entry the sweep ran to completion (exit 0). This is consistent with the header's "fatal signal it does not handle" wording. At base, SIGPIPE killed the launched shell.

## Prior public review findings: resolved or retained at this head

| Finding | State at 26353960 | Root-cause evidence (reviewer-owned) |
|---|---|---|
| R256-2 F1 / R257-1 F1 MAJOR, hard stop leaves a detached sweep | RESOLVED | Commands start with a parent-death KILL binding and an owner-still-parent check (owned_process.py:127-133,257-260), so the shell dies with its owner. Evidence and controls: <ul><li>receipts/probe-sweep.json, 11 hard arms (KILL/HUP/QUIT/USR1/ALRM to the entry at command; KILL/HUP to the group; KILL/HUP at preflight and transition): shell gone within 5 s, no later-suite sentinel after the held command was released and the lock freed, no summary, empty output after the stop.</li><li>receipts/probe-nested.json KILL and HUP, a real sweep around the real campaign's compile: the in-flight campaign finished detached and removed its own scratch; no later suite, no summary, caller unchanged.</li><li>Documented at run_all_suites.sh:30-35 and TESTING.md:225-233.</li><li>Removing the binding (M01) turns both focused tests red.</li></ul> |
| R256-2 F2 / R257-1 F2, ordinary Git variables refuse the campaign | RESOLVED | `_git` scrubs every GIT_* (private_inputs.py:55-58); only the REDIRECTS names refuse (29-33). Evidence and controls: <ul><li>receipts/probe-gitenv.json: 16 ordinary-variable arms and a no-variable baseline each run nine controls, exit 0, caller unchanged. They include the variable sets `git bisect run` and `git rebase -x` really export (GIT_EXEC_PATH, GIT_PREFIX, editors), GIT_TRACE to stderr, GIT_CEILING_DIRECTORIES above the repo and the pathspec modes.</li><li>GIT_DIR, GIT_INDEX_FILE, GIT_WORK_TREE, GIT_CONFIG_PARAMETERS and GIT_CONFIG_GLOBAL refuse by name, exit 2.</li><li>The M10 plant (no scrub) and the corrected M11 plant (GIT_INDEX_FILE dropped) each turn the lifecycle test red.</li><li>The hosted shard running gptp_shadow at this head reports `PASS gptp_shadow` (receipts/hosted-shard1-excerpt.txt).</li></ul> |
| R256-2 F3 MINOR, refusal covers non-build files | RESOLVED | The population is `make print-inputs` plus local includes (private_inputs.py:92-114). receipts/probe-scope.json on the real tree: <ul><li>A rewritten gptp_plane TEST_RESULTS.md, a dirty aaf TEST_RESULTS.md, an untracked hdl/common file and a staged suite README proceed with nine controls.</li><li>The private tree is exactly the 20 declared inputs plus the 2 included headers.</li><li>Dirty cdc_pulse.sv, sim_main.cpp and a gptp-processor input each refuse by name.</li></ul> |
| R256-2 F4 MINOR, CONTRIBUTING prescribes a copied third_party/ | RESOLVED | CONTRIBUTING.md:10 and 287-306 now say never symlink or copy a submodule; initialise it at its pin. A search of current docs finds no remaining copy instruction. receipts/probe-scope.json: a dependency without its `.git` refuses "not at its pin". |
| R256-2 F5 MINOR, Git stderr parsed as records | RESOLVED | Standard error goes to a separate file (private_inputs.py:44-52, owned_process.py:244-260); a malformed record raises InputRefused. The GIT_TRACE and GIT_TRACE_SETUP arms put trace text on stderr and still run nine controls (receipts/probe-gitenv.json). The lifecycle `git-stderr` and `git-garbage` arms pass. |
| R257-1 F3 MINOR, missing facility traces back with exit 1 | RESOLVED | `_prctl()` resolves all three facilities before any state change (owned_process.py:51-63). receipts/probe-scope.json, using my own site hook: no prctl, no pidfd_open or no pidfd_send_signal gives `REFUSED:` exit 2 with no traceback, and nothing starts at either entry point. |
| R256-2 S4 / R257-1 S1, VERILATOR_JOBS default | TAKEN | Makefile:4 `?= 0`, equal to base `-j 0`. |
| R257-1 S2, owner line contradicts "logs were not prepared" | TAKEN | The owner now prints a neutral CANCELLED line; lock-wait arms show "logs were not prepared for this invocation". |
| R256-2 S1 / R257-1 S3, test power | PARTLY TAKEN | The directory-link and index-vs-HEAD plants (M15, M08) are now red. The remaining inspection-only guards are carried as a SUGGESTION above. |
| R256-2 S3, final-tally signal ordering | DECLINED by the author | Carried as a SUGGESTION above. |

The items the prior rounds found clean still hold at this head:

- **Isolation.** The hardlink plant (M09) is red; the handshake proves a private mutation with a distinct inode.
- **Caller state.** Caller bytes, modes, index and pins are unchanged across every campaign probe.
- **Graceful paths.** 130/143 with reaped identities, including under a lock wait.
- **Mutation population.** MUTATIONS, NOT_SEPARATELY_OBSERVABLE, PLANE/RET/OBS, TALLY_RE, suite_failed and apply_control are AST-identical to base.
- **Real campaign.** 9/9 detections, with the three alternate-failed-check lines unchanged.
- **Bare-metal masks.** `check_baremetal_only.py --check` and `--selftest` exit 0.

## Coverage evidence (clean lenses, with artifacts)

```text
[R256] PASS Conformance - issue #523 AC1-4 and decision 5783211002 against scripts/run_all_suites.sh:111-133,251-266,443-451, scripts/owned_process.py:94-143,184-298, tb/verilator/gptp_shadow/mutants.py:238-313, private_inputs.py:163-197 - AC1: receipts/probe-campaign-hold.json handshake proves the first mutation applied only in the private copy (hash differs, distinct inode) before the signal; the lifecycle unsafe arm restores caller mutation and goes red (M06 plant red). AC2: caller integrity unchanged after normal completion, named detection, build failure (lifecycle), INT/TERM/second-signal and KILL/HUP/QUIT at the hold point and during a real compile (receipts/probe-campaign-*.json). AC3: 16 graceful sweep arms at selection, lock wait, preflight, command and transition, entry and group (receipts/probe-sweep.json); the next-suite sentinel stays unexecuted, no summary, identities gone (not zombies), attributable partial logs, stale logs cleared only after locking; nested real sweep plus real campaign TERM/INT/TERM-group (receipts/probe-nested.json) and during the cancellation preflight and the lifecycle test (receipts/probe-nested-phase.json) leave nothing alive and no scratch. AC4: receipts/real-campaign-make.txt 309/309, nine detections, six notes, RESULT PASS; detection lines identical to receipts/base-campaign-make.txt. Hard-stop and Git-environment contracts per the prior-findings table. Scope: no hdl/, gitlink, workflow or #517 pool file.
[R256] PASS RTL - git diff 776bc77d..26353960 (no hdl/, gitlink or .github change); tb/verilator/gptp_shadow/Makefile:4-43 (SRCS/VFLAGS unchanged except -j $(VERILATOR_JOBS), default 0 = base); scripts/owned_process.py:94-280 and run_all_suites.sh:111-133 process architecture - traced subreaper enable/restore, INT/TERM latch, root STOP+forward, TERM then leaf-first KILL with bounded 2 s + 2 s deadlines, pidfd plus (ppid, start) recheck before every signal, PDEATHSIG + owner-still-parent before exec, reap of adopted children; the external contract (entry = supervisor, shell in its own session) is documented at run_all_suites.sh:30-35,111-117 and TESTING.md:210-233 and its error paths (hard stop, facility refusal, cleanup failure -> REFUSED exit 2) behave as documented in the probes; scoped Verilator 5.050 identity in receipts/verilator-identity.txt (verilator_bin sha256 44898b22...).
[R256] PASS Robustness - receipts/probe-sweep.json (27 graded arms + 2 observation arms), probe-nested.json (5), probe-nested-phase.json (4), probe-campaign-hold.json (9), probe-campaign-real.json (3), probe-gitenv.json (22), probe-scope.json (11), probe-tstp.json, contention-*.txt - graceful and hard stops at every boundary, stubborn detached descendants, foreign siblings in the entry's group and in their own session untouched (graceful arms), repeat execution (lifecycle repeat arm), dirty/untracked/staged/linked/off-pin/copied inputs, stderr noise, missing facilities, --list/--shard/--physical-gptp output identical to base (55 suites; 3-shard union = full list); both focused tests pass pinned to 2 CPUs beside six busy loops (63 s, 134 s).
[R256] PASS Tests - tb/verilator/gptp_shadow/test_mutant_lifecycle.py, scripts/test_suite_cancellation.py, scripts/process_test_support.py, check_baremetal_only.py:271-274,902-920 - both focused tests exit 0 at head (receipts/focused-*.txt); 20 reviewer plants in disposable copies (receipts/probe-mutations.json): 17 turn the owning test red (owner binding, owner re-exec, trap exit, KILL escalation, caller-path mutation, mode check, index-vs-HEAD, hardlink copy, Git scrub, GIT_INDEX_FILE refusal, build-failure-as-detection, lifecycle not default, cancellation preflight removed, linked-directory check, stale-log ordering, pin revision, context cleanup); 3 green are inspection-only or redundant guards (SUGGESTION above); the Makefile default target owns the lifecycle test and the sweep preflight owns the cancellation test (M13, M14 red).
[R256] PASS Docs - docs/testing/TESTING.md:210-255, tb/verilator/gptp_shadow/README.md:84-135, run_all_suites.sh:27-35,111-117, mutants.py:1-31, CONTRIBUTING.md:10,287-306, measure_test_evidence.py:603-606 - every stated behaviour matched a probe (130/143, 2 s + 2 s cleanup, hard-stop allowance and lock record, partial logs, "logs were not prepared", refusal list, private population, KILL leaves scratch and deeper build steps); focused doc/policy checks exit 0 at head (receipts/static-focused.txt: docs_check, em-dash vs base, doc style, gen_toc --check/--verify-anchors, py/sh idiom, bare-metal --check/--selftest, test-evidence, fail-fast, naming, hygiene, todo ownership, ci_scope --selftest, sweep shape, ci_events --check); issue comments carry the evidence a cold reviewer needs; the stale PR-body head is a SUGGESTION.
```

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #523 AC1-4, decision 5783211002, REQ-VER-01/02/04 against run_all_suites.sh, owned_process.py, mutants.py, private_inputs.py; receipts probe-sweep, probe-nested, probe-nested-phase, probe-campaign-hold/real, real-campaign-make vs base-campaign-make | R256-3 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| RTL | CLEAN | diff scope (no hdl/, gitlink or workflow); gptp_shadow Makefile SRCS/VFLAGS/-j; owned_process.py state machine and process contract; run_all_suites.sh exec/session/lock/trap boundary; verilator-identity | R256-3 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Robustness | CLEAN (SUGGESTIONS only) | 80+ signal, Git-environment, scope, facility, contention and selection arms listed above; TSTP and inner-shell observations | R256-3 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Tests | CLEAN (SUGGESTION only) | test_mutant_lifecycle.py, test_suite_cancellation.py, process_test_support.py, bare-metal arms; 20 reviewer plants; focused and contention runs | R256-3 | 26353960ae2763cc09741d0f7bcc720621bd5148 |
| Docs | CLEAN (SUGGESTIONS only) | TESTING.md, gptp_shadow README, sweep header, mutants.py docstring, CONTRIBUTING 2.2 and Contents, test-evidence disposition; 17 focused doc/policy checks; PR body and issue comments | R256-3 | 26353960ae2763cc09741d0f7bcc720621bd5148 |

Every lens is covered at the exact head under review, so no ancestor argument is needed. No finding was moved to another Issue.

## Hosted evidence at the exact head (read only, not accepted here)

- **Executed.** receipts/hosted-check-runs-26353960.tsv lists 21 contexts that executed and concluded success: Verilator shards 0-4, Yosys shards 0-3, verilator-suites, yosys-portability, rtl-fast, docs-check, docs-check-no-git, elaborate, wire-accountability, verilator-lint, yosys-elaboration, bdd-conformance, changes and full-ci-gate.
- **Skipped.** "Physical gPTP (nightly and manual)" is a skipped context, not hardware evidence.
- **gptp_shadow on the hosted runner.** The Verilator shard 1/5 job log (receipts/hosted-shard1-excerpt.txt) shows `PASS     gptp_shadow`, 21/21 suites and 171619 checks. That shard owns gptp_shadow, so the lifecycle test, the new cancellation preflight and the real campaign all ran there without a Git-environment refusal.
- **Yosys shard durations.** They were 28-39 s. Whether that is expected for this change is part of the manager's hosted acceptance.

## Real limits

- **Sweep probes.** They used the real driver, owner, selector and tally with synthetic suites and stubbed unrelated prerequisites.
- **Nested probes.** They used a disposable copy reduced to the real gptp_shadow suite plus a sentinel suite, with four unrelated preflight self-tests stubbed. No full real sweep was run (not permitted).
- **Base comparison.** The base driver ran in a disposable base checkout, where it mutates tracked source by design.
- **One unexplained nested HUP attempt.** The foreign sibling was found exited when checked; its exit status was not captured, and the rerun overwrote that attempt's receipt. The supervisor's census never contained that sibling, and every signal it sends is identity-gated to its own census. The diagnostic rerun kept the sibling alive for the whole 214 s arm, and every other foreign-sibling check in this round held. Other drivers on this shared host signal numeric process groups after `getpgid`, which is a candidate outside this PR. It is unverified, so the death is recorded as unattributed rather than as evidence either way.
- **Reviewer probe defects, disclosed.**
  - Two early sweep-probe attempts crashed.
  - One of them orphaned a fixture sweep whose handshake file then contaminated the next attempt's g-transition-SIGINT arm.
  - The first nested attempt stubbed a script the lifecycle test imports.
  - The first M11 plant left GIT_INDEX_FILE in the refused set; receipts/probe-mutations-2.txt shows that erroneous line, and batch 3 is the corrected plant.
  - All were superseded: receipts/probe-sweep.json is a clean rerun into a fresh directory with a per-arm attribution check and an empty leftover scan.
  - The orphan and seven fixture children leaked by the M04/M20 plants were stopped by pidfd after start-time checks. Those plants disable the reaping the fixtures rely on, as R256-2 also observed. No reviewer process remains.
- **Script edits after runs.** After their runs, probe_campaign.py was changed only to read the scoped tool path from REVIEW_VERILATOR (the runs used `$PINNED_TOOLS/verilator`) and to parse arguments only when run as a script. probe_nested.py gained foreign-exit diagnostics before the final HUP arm. Receipts were normalised to `$PACKET`, `$REVIEW_CLONE`, `$PINNED_TOOLS`, `$VERILATOR_IMAGE_ROOT` and `$HOME` by scripts/normalise.py; raw originals stay in unpublished scratch.
- **Not exercisable here.** PID reuse and the owner-exited-before-exec race were checked by inspection only. Missing facilities and non-Linux hosts were emulated inside Linux Python. The noexec TMPDIR case was not exercised.
- **Timing.** One shared 16-CPU host; contention was emulated by pinning.
- **Not re-verified.** I did not re-verify the readiness-digest reconciliation, which lies outside this diff and is unchanged. I did not read the manager's source banks for this head, which are still running; this report makes no claim about them.
- **Hardware.** Physical calibration NOT RUN; field skips are not hardware evidence.
- **Review clone.** It is byte-, mode-, index- and gitlink-identical to its pre-probe state (receipts/integrity-before.json equals receipts/integrity-after.json, including no untracked or ignored files). The generated ignored files my runs created were inspected and removed.

## Pending manager duties

- Publication of this report and packet.
- The independent external review (R257-2); two positive reviews are required.
- The manager's full source static/builder and native banks for this head.
- The trusted serial act replica at this head, including confirmation that gptp_shadow runs rather than refuses under the replica's job environment.
- Exact-head hosted acceptance.
- The final current-dev candidate at the merge turn. Live dev 574c29fa is 2 commits ahead of the source base and touches docs/testing/CI_WORKFLOWS.md and scripts/ci_events.py, neither of which is in this PR.
- An optional PR-body refresh to the current head.
- Maintainer-authorized merge, post-merge containment, and moving the card to Done.

R256-3 FINISHED

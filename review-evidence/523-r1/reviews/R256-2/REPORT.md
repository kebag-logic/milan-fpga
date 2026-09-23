[R256] NEGATIVE - exact head b5ce20eca8b59709ec5bc6115e5e15bfc312f283

Round R256-2, cleared-context internal independent review of issue #523 / PR #526.
Head `b5ce20eca8b59709ec5bc6115e5e15bfc312f283`, tree `bfde1313250ae84105754af4b150325f55f5ef33`,
source base and live `dev` `483a133ed08867ea0d300d2b4a027b5b48a4282f`. All five lenses applied.

## Verdict in one paragraph

The isolation core is sound and independently confirmed: the real mutation driver builds
in a private copy (192 regular, single-link, blob-exact files), the caller checkout stays
byte/mode/index/pin identical through normal completion, INT, TERM and KILL, graceful
INT/TERM exits 130/143 in about 0.2 s with every owned identity gone, the nine original
mutations, six unobservable reasons and the alternate-failed-check fallback are unchanged
(AST-identical) and the real campaign still catches all nine (309/309 baseline). The round
is NEGATIVE for two MAJOR and three MINOR findings: a hard stop (KILL or HUP) of the
sweep entry now leaves a detached sweep that starts later suites and prints a completed
summary, a regression against the base driver; ordinary Git environment variables
(GIT_EDITOR, author/committer identity, SSH, trace) refuse the whole campaign so zero
controls run; the clean-input refusal covers non-build files, including a TEST_RESULTS.md
the sweep itself rewrites; CONTRIBUTING still prescribes a lane layout the campaign now
refuses; and a harmless Git warning on stderr crashes the driver with the "not caught"
exit status.

## Reconstruction order

1. AGENTS.md, CONTRIBUTING.md sections 2 and 3, docs/README.md authority order.
2. Issue #523 body (frozen acceptance 1-4), the manager's settled decision
   (issuecomment-5783211002) and READY TAKEOVER; the executor's public TAKEN,
   implementation-detail, validation, provenance and REVIEW READY comments; the manager's
   source-validation comments on the issue and PR.
3. REQUIREMENTS.md REQ-VER-01/02/04.
4. `git diff 483a133e..b5ce20ec` (12 files, no hdl/ file, no gitlink) and the four commits.
5. Public evidence: readiness bundle at `b9a05dc9`, author archive and digest reconciliation
   at `ad844b49`, manager source evidence at `6df2d51f`, trusted replica at `840fccb1`;
   exact-head hosted check-run metadata.

No private author material, lane scratchpad, management directory or other reviewer
report was read before this verdict and ledger were written.

## Findings

### F1

```text
[R256] MAJOR Robustness, Conformance, RTL, Tests, Docs - scripts/run_all_suites.sh:110-112, scripts/owned_process.py:70,206-209 - A hard stop of the sweep entry leaves a detached sweep that runs later suites and prints a completed summary
Requirement/evidence: The round's bar for hard KILL is no cleanup and no completed success; the settled decision allows a hard kill to leave children but "no cleanup or completed-PASS claim may be made for that path". At head the entry PID becomes the Python owner (exec at run_all_suites.sh:111), the loop shell runs in a new session (owned_process.py:207 start_new_session=True) and only INT/TERM are handled (owned_process.py:70). receipts/probe-sweep-hardstop.json, same fixture, KILL or HUP delivered only to the entry at the command handshake, then the in-flight command released: head KILL and head HUP both start the next suite (omega), print "PASS     omega" and the "suites:" summary into the caller's output; base 483a133 KILL and HUP start no later suite and print no summary. Group-directed stops (terminal hangup, quit key, kill of the process group) now reach only the owner, because the loop is in another session.
Impact: A caller that hard-stops the sweep, or loses its terminal, sees the entry die while a detached shell keeps fd 9 (the tree lock, run_all_suites.sh:204-208) and runs the rest of the population for up to the full sweep time, writes logs into OUT, rewrites tracked TEST_RESULTS.md files, and appends PASS verdicts and a suites/passed summary to the caller's log; the next sweep in that tree refuses 91 or queues behind it. This is the uncontrolled continuation #523 set out to stop, reintroduced for non-graceful stops, and the base driver did not have it.
Required change: After the owning entry process is killed without cleanup, or receives a terminal hangup, the sweep shell starts no later suite and produces no completed summary; the in-flight command may finish (the settled hard-kill allowance). The session/process-group contract change is documented next to the 130/143 contract.
Verification: A deterministic probe at the command handshake that KILLs and HUPs only the entry, releases the command and requires the next-suite sentinel absent, no "suites:" line and the lock free once the in-flight command ends. It must fail at b5ce20e (it does, receipts/probe-sweep-hardstop.json) and pass after the fix.
```

RTL-lens attribution: the lens covers architecture and interface contracts. The sweep's
process contract (signalling the entry process or its group controls the run) changed, and
the entry-loss error path of the new owner/shell architecture is incomplete.

### F2

```text
[R256] MAJOR Robustness, Conformance, Tests, Docs - tb/verilator/gptp_shadow/private_inputs.py:84-87 - Ordinary Git environment variables refuse the whole mutation campaign
Requirement/evidence: Only four GIT_* names are accepted; any other refuses before copying. receipts/with-GIT_EDITOR-real-shadow-make.log (the reviewer's normal environment exports GIT_EDITOR): lifecycle PASS, baseline 309/309, then "REFUSED: Git environment overrides are not accepted: GIT_EDITOR", make exit 2, so the sweep would count gptp_shadow as a FAILED suite and none of the nine controls runs. receipts/probe-refusal-scope.tsv: GIT_EDITOR, GIT_SEQUENCE_EDITOR, GIT_AUTHOR_NAME, GIT_COMMITTER_EMAIL, GIT_SSH_COMMAND, GIT_ASKPASS, GIT_TRACE=0 and GIT_MERGE_AUTOEDIT each refuse (exit 2). The base driver (483a133 mutants.py:270-271) read no environment and ran all nine. Acceptance 4 requires the original controls to still run; the code's own rationale (private_inputs.py:83) is redirection of identity checks, which none of these variables can do. Tests: scripts/process_test_support.py:59,124-125 strip every GIT_* from each probe, the only accepted-variable arm is GIT_PAGER (test_mutant_lifecycle.py:88), and the only redirect arm (GIT_INDEX_FILE, :193) still refuses with the guard deleted (receipts/probe-test-power.json, no-git-env-check, test exit 0) because the dependency index comparison refuses first. Docs: neither tb/verilator/gptp_shadow/README.md nor docs/testing/TESTING.md mentions a Git environment refusal.
Impact: In any shell or agent environment that exports an ordinary Git setting (editor, identity, transport, trace), the required local sweep reports a red gptp_shadow and zero of nine controls run, although nothing is defective. The test population cannot observe this configuration and does not isolate the guard it names.
Required change: A variable that cannot change which repository, work tree, index, object store, configuration or pathspec the identity commands read neither refuses nor silences the campaign. Variables that can redirect identity remain refused, or are removed from the identity commands' environment, and each such rule has an arm that goes red when the rule is deleted. The rule is documented.
Verification: mutants.py (or new lifecycle arms) with each of the eight variables above runs the campaign; GIT_DIR, GIT_WORK_TREE, GIT_INDEX_FILE, GIT_OBJECT_DIRECTORY and GIT_CONFIG_PARAMETERS (or the published equivalent set) refuse; deleting the guard in a disposable copy turns the lifecycle test red.
```

### F3

```text
[R256] MINOR Robustness, Conformance, Docs - tb/verilator/gptp_shadow/private_inputs.py:11,88 - The clean-input refusal covers every file under hdl/, tb/common and the suite directory, not the campaign's inputs
Requirement/evidence: FIRST_PARTY verifies and copies 138 first-party files (receipts/probe-private-copy.json), including documentation and generated evidence the build never reads; the dependency scopes were narrowed to build inputs (private_inputs.py:12-14) but first-party was not. receipts/probe-refusal-scope.tsv: a timestamp-only rewrite of hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md, an untracked unrelated hdl/common file, and a dirty hdl/ieee1722/aaf/doc/TEST_RESULTS.md each refuse the campaign (exit 2). tsn_fuzz rewrites hdl/ieee8021as/gptp_plane/doc/TEST_RESULTS.md with a new timestamp whenever the field oracle is present (tb/verilator/tsn_fuzz/Makefile:207-219; the NOTE at scripts/run_all_suites.sh:79-83) and runs after gptp_shadow, so a second local sweep in the same tree reports gptp_shadow FAILED. The base driver refused only an untracked or modified mutation target (483a133 mutants.py:270-275); the settled decision says to preserve that refusal and to copy the required inputs.
Impact: False-red suite verdicts in ordinary local flows (a repeat sweep with the oracle installed; a sweep over uncommitted, unrelated hdl/ work) for files the campaign never builds.
Required change: Files the private build and the campaign do not read do not refuse the campaign; build inputs, mutation targets and unobservable-reason anchors remain verified. If the wider rule is intended, that decision is published and the repeat-sweep interaction is documented where the NOTE and the README describe the refusal.
Verification: a timestamp-only TEST_RESULTS.md rewrite and an untracked unrelated hdl/ file let the campaign run; a dirty build input or anchor file is refused.
```

### F4

```text
[R256] MINOR Docs - CONTRIBUTING.md:10,287-290 - The lane rule still prescribes a copied third_party/ layout that the campaign now refuses
Requirement/evidence: CONTRIBUTING section 2.2 (and its Contents entry) tells a worktree to cp -r third_party/ and delete the copied submodule's .git file. receipts/probe-dependency-pins.tsv: exactly that layout gives "REFUSED: required dependency is not at its pin: third_party/verilog-axis" (exit 2), so gptp_shadow fails; the base driver ran in that layout. The next bullet (CONTRIBUTING.md:291-294) separately requires submodule initialisation. The change's documentation does not reconcile the two.
Impact: A developer following the authoritative lane rule gets a red required suite with a pin message.
Required change: The authoritative documentation names one supported dependency layout consistent with the campaign's pin refusal, or the refusal accepts the documented layout by a published decision.
Verification: documentation diff, and the probe's cp -r case either documented as refused or accepted.
```

### F5

```text
[R256] MINOR Robustness, Conformance, Tests - tb/verilator/gptp_shadow/private_inputs.py:21-41, scripts/owned_process.py:206-209 - Git diagnostics on stderr are parsed as identity records
Requirement/evidence: owner.run merges stderr into the captured stream and _records splits that stream as NUL-separated records. receipts/probe-git-stderr-warning.txt: a deprecated core.fsyncObjectFiles setting makes Git print one warning line; the driver raises ValueError at private_inputs.py:35 and exits 1, which mutants.py:28-29 defines as "a control was not caught"; no control runs. The base driver used exit statuses only. No lifecycle arm covers Git diagnostics.
Impact: A benign Git configuration turns into an uncaught traceback whose exit status misreports an input problem as an uncaught mutation, and the campaign does not run.
Required change: Identity parsing reads only Git's standard output (or otherwise tolerates diagnostics), and any unparseable identity output is a refusal with exit 2, not a crash with exit 1.
Verification: the same probe runs the campaign or refuses with exit 2; an arm covers it.
```

### Suggestions (optional, no coverage effect)

```text
[R256] SUGGESTION Tests - receipts/probe-test-power.json - Four guards survive deletion under their focused tests
Evidence: deleting the directory-link refusal (private_inputs.py:44-49; the parent-link and dependency-link arms are refused first by the untracked and top-level checks), the identity recheck before signalling (owned_process.py:191; PID reuse not exercised), the root SIGSTOP on cancellation (owned_process.py:96; the transition fork race not exercised) or the mask's start anchor (check_baremetal_only.py:273-274; no arm plants a longer name ending in PROC) leaves the owning test green. Bytes stay blob-verified and pidfds bound the reuse risk, so impact is limited; arms that isolate each guard would make the tests prove what they name.

[R256] SUGGESTION Robustness, Docs - scripts/owned_process.py:62-66,243, docs/testing/TESTING.md:216-217 - A host without the prctl/pidfd facilities raises AttributeError (traceback, exit 1) instead of the documented refusal
Evidence: receipts/probe-unsupported-platform.txt. For the sweep, exit 1 reads as one failed suite. Catching AttributeError at the boundary and returning 2 with REFUSED would match the text.

[R256] SUGGESTION Robustness - scripts/run_all_suites.sh:411-418 - A signal during the final tally leaves "suites: 2   passed: 2   failed: 0" printed before the CANCELLED lines
Evidence: receipts/probe-summary-signal.json (exit 130/143, CANCELLED lines present, no check total or logs line). Printing the count line after the tally, or stating that the status and CANCELLED line are authoritative, removes the partial-summary shape.

[R256] SUGGESTION Conformance, Docs - tb/verilator/gptp_shadow/Makefile:4,9 - The suite's Verilator build parallelism default changed from all CPUs (-j 0) to 4 without a public rationale
Evidence: hosted runners with four or fewer vCPUs are unaffected; the README example uses VERILATOR_JOBS=4. Record the reason in the PR or README.
```

## Coverage evidence per lens (what was applied and held)

These rows record the artifacts each lens examined. They are coverage evidence, not
per-lens PASS verdicts: every lens below carries at least one open finding above.

| Lens | Checked and held at this head | Artifact |
|---|---|---|
| Conformance | Acceptance 1: the lifecycle unsafe control (private = REPO) detects caller change after interruption, at an explicit handshake, no sleep oracle | test_mutant_lifecycle.py:110-147; receipts/real-shadow-make.log line 29 |
| Conformance | Acceptance 2: caller bytes/modes/index/pins identical after normal completion, named detection, build failure, INT, TERM and KILL, including the real driver at a mutation-applied boundary | receipts/probe-real-driver-signals.json; receipts/real-shadow-integrity-before.txt, real-shadow-integrity-after.txt |
| Conformance | Acceptance 3 (graceful): 130/143, no later suite, reaped identities, partial logs, foreign holder untouched, also for a sweep queued on the lock | receipts/test_suite_cancellation.log; receipts/probe-lock-wait-cancel.json |
| Conformance | Acceptance 4 in a clean environment: 309/309, nine detections (six named, three via the unchanged alternate-failed-check fallback), six notes, RESULT PASS | receipts/real-shadow-make.log; receipts/real-shadow-exit.txt (exit 0, 264 s) |
| Conformance | Population: MUTATIONS, NOT_SEPARATELY_OBSERVABLE, TALLY_RE, PLANE/RET/OBS/TIC, suite_failed, apply_control, named and alternate arms AST-identical; the survivor arm changes only its message | receipts/mutation-population-compare.json |
| Conformance | Scope: 12 files, no hdl/ file, no gitlink change; #517 pool files untouched | `git diff --name-only 483a133e..b5ce20ec` |
| RTL | No RTL, processor or axis pin change; owner cancellation state machine (latch, root stop, TERM, leaf-first KILL, root resume, reap, bounded failure) traced line by line; pidfd plus start-time recheck before every signal | scripts/owned_process.py:90-199 |
| Robustness | Pinned dependency refusals on the real tree: off-pin, uninitialised, dirty dependency input | receipts/probe-dependency-pins.tsv |
| Robustness | Private copy: 192 files, regular, nlink 1, distinct inodes, blob-exact bytes, mode = caller mode plus owner write, no symlinks | receipts/probe-private-copy.json |
| Robustness | Stubborn detached descendants reaped on normal completion and cancellation; KILL leaves only private scratch and a build child, caller unchanged, no verdict | receipts/probe-real-driver-signals.json; receipts/test_suite_cancellation.log |
| Tests | 10 of 15 production mutants turn the owning test red: no-subreaper and no-kill-escalation (both suites), hardlink-copy, no-byte-hash, no-mode-check, no-untracked-check, no-private-restore, no-shell-cancel-traps, no-sweep-owner, mask-any-proc; the five survivors are F2 and the first suggestion | receipts/probe-test-power.json |
| Tests | Both focused tests pass at head; the normal make owns the lifecycle test; bare-metal selftest arms 342 -> 354, exactly the twelve new mask arms, all passing; --check 0 findings | receipts/test_suite_cancellation.exit; receipts/focused-static-gates.txt |
| Docs | Changed pages pass the em-dash gate (67 added lines) and docs_check; TESTING.md and the README match the implemented 130/143, cleanup bounds, private copies and KILL allowance; SHA256SUMS/MANIFEST reconciliation independently reproduced | receipts/focused-static-gates.txt; receipts/readiness-nested-SHA256SUMS-check.txt; receipts/readiness-reconciliation.json |

## Focus items

- Private-input selection and copy: whole first-party scopes plus gptp-processor/hdl (7) and
  verilog-axis/rtl (47); fresh writes only, no hardlink or write-through
  (receipts/probe-private-copy.json; hardlink mutant caught). Selection breadth is F3.
- Pinned dependency checks and refusals: dirty, staged, assume-unchanged, skip-worktree, mode,
  untracked, extra, symlink, parent-link, dependency, off-pin, pin-index, dependency-link and
  Git-override arms pass; real-tree pin probes refuse. Over-refusal is F2, F3, F4 and F5.
- Process boundaries: normal completion, named failure, build failure, INT, TERM (130/143 in
  about 0.21 s, identities gone, private removed), KILL (caller unchanged, no completed
  verdict). Sweep-entry hard stop is F1.
- Host-process masks: two exact-line masks keyed to two files; twelve new arms (two positive,
  ten refusal) pass; broadening to any /proc is caught, the start anchor is not (suggestion).
- Readiness digests: the nested SHA256SUMS refuses exactly six files (mutation-kill.json,
  mutation-term.json, reproduce.py, results.json, sweep-term.json, sweep-term.stdout); each
  nested digest equals the outer MANIFEST original_sha256, each is marked path_redacted, all
  22 public files equal their published_sha256, and every unrefused file has original equal
  to public. The recorded refusal is correctly retained, not rewritten.
- Issue #517's own pool cancellation is out of scope and untouched here.

## Prior public review findings

None to resolve or retain: before this round the PR and issue carried no review verdict or
finding (R256-1 ended without a report and provides no coverage). Checked after this
verdict and ledger were written.

## Reviewer-owned completion ledger

| Lens | State | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1 MAJOR, F2 MAJOR, F3 MINOR, F5 MINOR) | issue #523 acceptance 1-4 and settled decision; mutants.py, private_inputs.py, run_all_suites.sh; real campaign; population AST compare | R256-2 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| RTL | UNCLEAN (F1 MAJOR) | owned_process.py state machine and process contract; run_all_suites.sh session/lock/trap architecture; no hdl/ or gitlink change | R256-2 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Robustness | UNCLEAN (F1 MAJOR, F2 MAJOR, F3 MINOR, F5 MINOR) | signal, lock-wait, summary, hard-stop, refusal-scope, pin, stderr and private-copy probes; real driver INT/TERM/KILL | R256-2 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Tests | UNCLEAN (F1 MAJOR, F2 MAJOR, F5 MINOR) | test_mutant_lifecycle.py, test_suite_cancellation.py, process_test_support.py, bare-metal arms; 15 production mutants | R256-2 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |
| Docs | UNCLEAN (F1 MAJOR, F2 MAJOR, F3 MINOR, F4 MINOR) | docs/testing/TESTING.md, gptp_shadow README, run_all_suites.sh header, mutants.py docstring, CONTRIBUTING 2.2; evidence manifests | R256-2 | b5ce20eca8b59709ec5bc6115e5e15bfc312f283 |

No lens is covered clean by this round. No finding was moved to another Issue.

## Real limits

- The sweep was exercised through the production driver with the fixture's synthetic
  suites and selector/tally shims; no full real sweep was run (not permitted). The real
  campaign ran standalone in a disposable copy, not inside a real sweep.
- The first real campaign run was refused by the reviewer environment's GIT_EDITOR (kept as
  F2 evidence); the passing run unset only that variable.
- Cleanup timings were measured on one Linux host shared with unrelated lanes' jobs, which
  were not touched. PID reuse and non-Linux hosts were not exercised (the missing-prctl case
  was emulated only).
- Hosted results were read as check-run metadata only: the latest exact-head runs executed
  all five Verilator shards, four Yosys shards and the other required jobs successfully;
  earlier cancelled or failed contexts belong to superseded runs; the physical gPTP job is
  skipped (nightly/manual) and is not hardware evidence. The trusted replica was not run by
  this reviewer. Physical calibration NOT RUN.
- The final current-dev candidate was not reviewed; source base and live dev were both
  483a133 for this round.
- The no-subreaper and no-kill-escalation mutant runs (expected red) leaked four of the
  fixture's stubborn children from disposable scratch, because the mutated owner also
  contains the tests. The reviewer stopped them by pidfd after rechecking start time and
  command line; no probe process remained at the end of the round.

## Pending manager duties

Publication of this report; executor response to F1-F5; a fresh cleared-context re-review
at the corrected head covering all five lenses; the separate external review; trusted
replica and exact-head hosted acceptance at the final head; current-dev candidate
validation; maintainer-authorized merge; post-merge containment.

## Receipts and scripts

Receipts under `receipts/` and portable probe scripts under `scripts/`, all listed with
their digests in MANIFEST.sha256. Host paths are normalised to `<packet>`, `<clone>`,
`<scoped-tool-bin>` and `$HOME`. The scoped Verilator identity is in
receipts/verilator-identity.txt (Verilator 5.050 rev v5.050). The review clone's tracked
bytes, modes, index and the three required gitlinks were verified before and after the
round (receipts/integrity-before.txt, receipts/integrity-after.txt).

R256-2 FINISHED

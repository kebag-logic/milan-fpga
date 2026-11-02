[R764] NEGATIVE - exact head d4d8cff92658e57b11090c97daf7b44edb31b3b6

# R764-1 external review: issue #833 / PR #834

- Head under review: `d4d8cff92658e57b11090c97daf7b44edb31b3b6`, tree `7cf0eb4fdbcafbb8ea82c89fdefbaf94c013ac91`, 14 one-line commits on source base `1f29f189279f9fc0132f4918e47342b87d22f33a` (live `dev` is the same commit).
- Role: external, cleared-context reviewer. Sources: AGENTS.md, CONTRIBUTING.md, docs/README.md, the #833 body and comments, the PR body, `git diff 1f29f189..d4d8cff`, and the public evidence tree at `1ca64e40:review-evidence/833-r1`.
- Prior public review findings on #834: none existed when this round read the PR. The only PR comments are the two review-start notices, so there was nothing to resolve or retain.
- No manager source bank ran at this head, and this report claims none. Source-head execution evidence is the author's published receipts, plus the focused probes listed below.

## Verdict basis

The engineering is sound. All 12 captured failures reclassify exactly as the PR says. Every claimed fix in `scripts/owned_process.py` is a real fix, and I found no defect in its state machine. A true survivor still fails the run. The verdict is NEGATIVE for four open MINOR findings:

- one changed behaviour has no control (F2);
- the authoritative testing guide states a cleanup timing that this head no longer has (F1);
- two stated figures are wrong (F3, F4).

None of the four is a code defect in cleanup.

## Checks requested

### (1) Cause table: confirmed, 8 Z / 1 T / 3 D

`scripts/classify_evidence.py` re-derives each message from the raw jsonl and log sources, not from the author's summary. It skips the survivor control's own deliberate prints. The result is 12 messages: 8 state Z, 1 shell in state T holding a state-Z child, and 3 with a process in state D. Receipt: `receipts/cause-classification.txt`.

- Every one of the 12 messages has exactly one listed parent that is outside the listing. A listed descendant's parent is either the owner or another listed process, so that parent is the owner. For the 8 single-entry Z messages, the zombie's parent is therefore the owner that raised.
- The three D messages are at `round0-at-f6b776e7/fullsuite-round0-1/before/00{1,2,4}.log`. Their tree is `63044c82`, the message-only first commit, at load average 247.7 with 10 concurrent builds. The wait channels are `__mmap_region` (2.07 s after SIGKILL), `unlink_file_vma_batch_process` (1.36 s) and `dup_mmap` (1.91 s).
- All 12 report about 4.0 to 5.2 s of cleanup, which matches the pre-fix 2 + 2 s wall deadline.

### (2) Each fix is real and has a red mutation, with one gap

Each mutation ran in its own fresh clone at the head, in its own user and PID namespace. Driver: `scripts/mutate.py`. Receipts: `receipts/mutations/`, `receipts/mutations-identity/`.

| Fix | My mutation | Result at head |
|---|---|---|
| Identity by start time | M01: parent back in the initial key only | green: equivalent, see below |
| | M01b: parent back in the send-time recheck only | green: only delays SIGTERM by one pass |
| | M01c: both halves, the pre-fix identity | **red**: `re-parented descendant was treated as new and never got SIGTERM` |
| Reap after census | M02: no second reap | **red**: `CLEANUP FAILED ... state Z` in 0.47 s |
| Pass-advanced clock | M03: wall clock; M04: clamp 0.5 → 5.0 s | **red**, **red** (`CLEANUP FAILED` on a process never killed) |
| Resumed shell's own window | M05: resume does not extend the kill time; M06: pre-fix rule, shell killed at the kill time even if never resumed | **red**, **red** (`the shell was killed in the pass that resumed it`) |
| Trap-started command shares the window | M07: skip removed | **green**: F2 |
| SIGKILL before raising | M08: removed; M09: kept but sparing the stopped shell | **red**, **red** (`stopped shell left behind`) |
| Bounded endless listing | M10: unbounded | **red** (`cleanup never reached a verdict`) |
| A true survivor fails | M11: a process sent SIGKILL is trusted dead | **red** (`a survivor never failed the run`) |
| Report names the state | M12: state and wchan removed | **red** |
| Cleanup does nothing (suite / lifecycle) | M13 | **red** / **red** |
| None (3 controls) | | green, green, green |

Two of the green rows are not gaps:

- **M01 and M01b.** Each half of the identity fix covers the other. With the start-only send recheck, every initial descendant gets SIGTERM in pass 1, whatever the initial key holds. Reverting the whole fix (M01c) goes red.
- **M14 and M15.** M14 (no start-time recheck) is pre-existing safety outside this delta. M15 (windows back to 2 s) is a derived constant, which no stall-free control can see.

M07 is a real defect mutant: `scripts/probe_owner.py trap-child` shows the trap's leaf command SIGKILLed under M07 and completing at the head. See F2.

### (3) A true survivor still fails the run, and the 10 s window is derived

- The survivor controls (M08 to M11) are red when mutated, and the unmutated control prints the state of every listed process. At production constants, `receipts/probe-late-survivor-head.log` fails the run after 32.55 s of owner clock, naming the survivor as `state S` and `sent SIGKILL 10.00 s ago`.
- The 10 s windows are justified at `scripts/owned_process.py:30-40` from receipts I checked:
  - 121,660 = 50,139 + 50,138 + 10,692 + 10,691 kills, the longest 0.2269 s, load at most 111.5 (`deadline/killlat-summary.txt`);
  - a 7.958 s spawn stall;
  - a 3.042 s pass (`cause/slowest-cleanups.txt`);
  - 1.91 s and 2.07 s spent in state D.
- 10 s is the round value above the longest measured stall (7.96 s), which is what the comment claims. I accept it as derived.

### (4) Before and after at equal load

The author's raw receipts reproduce the counts in the PR table (`receipts/cause-classification.txt`, final section). However, every before-tree failure in the first two rows is the fixture's 12 s `Probe.finish` hang bound, not `CLEANUP FAILED`: 10 of 10 in the full suite and 18 of 18 in lifecycle. Those rows measure the `FINISH_SECONDS` change. The equal-load evidence for the cleanup fixes is:

- the suite row: 1 `CLEANUP FAILED` before, 0 after;
- the focused row: 4 before, 0 after;
- the mutations above.

That is adequate, but the table should say so (R1).

My own run had both trees at the same moment on the same 16 CPUs: 6 + 6 suite runs and 2 + 2 lifecycle runs, in PID namespaces, at load average 78 during the run. It gave 8 of 8 on each tree, so it does not separate them at this lower load (`receipts/compare/`). The host-level runs at the head, outside any namespace, are both rc 0 (`receipts/gates/host_suite.*`, `host_lifecycle.*`).

### (5) No host-wide signal or process match in committed code

I read every added line that signals or matches processes:

- `scripts/owned_process.py` signals only through a pidfd that it opens and rechecks by start time.
- The test file signals:
  - its own children (`.kill()`);
  - its own PID (`os.kill(os.getpid(), ...)`);
  - one survivor that it reaps itself (`scripts/test_suite_cancellation.py:405-410`).

There is no pkill, killall, killpg or command-line match. The load tools in the archive (`receipts/load-tools/`) are lane receipts, not product. The line 36 redaction in their `stoptests.py` is an archive privacy redaction, as stated.

### (6) Stale `ci/image/command-table.json`

I accept the decision to leave it. Reasons:

- It was already stale on `dev`. `scripts/command_table_staleness.py` counts **34 of 149** pins stale at `1f29f189`, plus 1 absent; at the head the count is 38, the 4 new ones being this delta's files.
- No workflow runs a reader of the table.

The PR's rationale misstates both facts (F4).

### (7) Relates-to vs Closes

`Relates to #833` is correct. Acceptance item 2 asks for "no suite left to fail by chance". `Probe.ready`'s fixed 15 s handshake (`scripts/process_test_support.py:196`) still trips in 4 of 10 focused runs at host load 250 to 314 after the change, with no ownership failure among them. Closing the issue, or splitting that bound into its own Issue, is the manager's call (see pending duties).

### Comment rule

The added comments and docstrings carry issue IDs only, with no lane labels, lane names, review rounds, reviewer IDs or comment IDs. I searched every added line and found no RESIDUE instance. Commits are one-line with no trailers (14 commits, 14 message lines).

## Findings

**F1 - MINOR - Docs - `docs/testing/TESTING.md:223-224` - the guide still states the pre-fix cleanup timing**
- Evidence: line 224 reads "Another two seconds bound reaping and terminal trap cleanup." At this head:
  - SIGKILL reaches every descendant 2 s after grace (`KILL_ALL_SECONDS`);
  - a remaining descendant fails the run only 10 s after that (`REAP_SECONDS`);
  - a late-resumed shell's trap has 10 s (`TRAP_SECONDS`) (`scripts/owned_process.py:37-40`).
- The PR edits the same paragraph block (lines 258-264) but leaves line 224. AGENTS §6 Docs requires: "Changed contracts are reflected in authoritative docs."
- Impact: the authoritative contract understates cleanup by a factor of five. A reader sizing a cancellation timeout from it is wrong.
- Required outcome: lines 223-224 state the stages this head enforces: 2 s grace, then 2 s to SIGKILL everything, then 10 s before a remaining descendant fails the run, and 10 s for a late-resumed shell's trap.
- Verification: read the lines against `scripts/owned_process.py:37-45`; `scripts/check_doc_style.py` and `scripts/docs_check.py` stay rc 0.

**F2 - MINOR - Tests, Docs - `scripts/owned_process.py:329-331`, `scripts/test_suite_cancellation.py:530-565`, PR body "Each fix reverted alone turns its control red" - no control for a trap-started command sharing the resumed shell's window**
- Evidence: this PR changes the rule from `now < resumed + 1.0` to the shell's whole window. The change is stated at `owned_process.py:329` ("A command the resumed shell's trap started shares its window") and in `TESTING.md:262`.
- Removing the skip (M07) leaves `scripts/test_suite_cancellation.py` green (`receipts/mutations/M07-trap-child-no-window.*`). Its only late-resume control uses a builtin `echo` trap, which starts no process.
- M07 is not equivalent. In `receipts/probe-trap-child-M07.log` a 1 s leaf command run by a late-resumed shell's trap is SIGKILLed and never writes its marker; at the head it does (`receipts/probe-trap-child-head.log`).
- Impact: a regression that kills a sweep's terminal-trap cleanup command on a late resume would pass the sweep preflight. The PR body's claim that each fix has a red control is not true for this part.
- Required outcome: a control in which a late-resumed shell's trap runs one external leaf command. It must pass at the head and go red when that skip is removed. Alternatively, the PR states publicly that this behaviour has no control.
- Verification: the M07 mutation goes red under `python3 scripts/test_suite_cancellation.py`.

**F3 - MINOR - Docs, Robustness - `scripts/process_test_support.py:19-21`, PR body ("14 to 24 s", "up to 24 s, not 4") - the time for a true survivor to fail the run is understated**
- Evidence: the failure fires at `kill_all + REAP_SECONDS`, where `kill_all = max(4, resumed + TRAP_SECONDS)` and a resume can happen up to clock 14. That gives under 34 s of owner clock, and under 44 s on the never-emptying-listing branch (`owned_process.py:289-290`).
- Measured at production constants: a late resume at about 12.5 s, then a survivor started by the trap, fails after **32.55 s** (`receipts/probe-late-survivor-head.log`).
- The comment uses the 24 s figure to justify `FINISH_SECONDS = 60`. The hang bound still exceeds the true maximum on an unloaded owner. With passes slower than 0.5 s it can fire first, but then the run still fails, only without the state report.
- Impact: a stated bound on the cancellation timeout path is wrong in a source comment and in the PR body.
- Required outcome: the comment and PR text state the derived maximum, under 34 s of owner clock (44 s for the empty-listing branch), and that wall time exceeds owner clock when a pass takes more than 0.5 s. Alternatively, the code is changed to match "24 s".
- Verification: rerun `scripts/probe_owner.py <clone> late-survivor`. Its reported seconds must lie within the stated bound.

**F4 - MINOR - Docs - PR body, Known limitations: "already stale on `dev` for 33 of 143 pinned files, and nothing reads it"**
- Evidence: `receipts/command-table-staleness.txt` reads git objects at `1f29f189` and finds 34 of 149 pins stale and 1 absent. Readers exist: `scripts/ci_command_table.py:217-220` refuses a "changed declared script", and `ci/image/build.py:151` reads the table. No workflow in `.github/workflows` runs either.
- Impact: the figures and the reason given for a deliberate non-change are wrong. The decision itself stands.
- Required outcome: the PR text gives the measured counts, or names the counting method behind 33/143. It says "no workflow runs a reader" rather than "nothing reads it", and notes the 4 pins this PR makes stale.
- Verification: `python3 -I scripts/command_table_staleness.py <checkout> 1f29f189… d4d8cff…`.

**R1 - RESIDUE - Docs - PR body, the "Before and after" table, rows 1 and 2**
The before failures (0 of 10, 0 of 18) are all the fixture's 12 s hang bound, with no `CLEANUP FAILED`, but the table does not say so. The published handoff does. Exact fix: append ", all at the fixture's 12 s hang bound" to both before cells, as `HANDOFF.md` has it.

**R2 - RESIDUE - Docs - `docs/testing/TESTING.md:259`**
"A stalled or starved owner therefore never fails a descendant it has not yet killed." The survivor control's own print lists the stopped shell as `not sent SIGKILL` (`receipts/compare/after-suite-1.log`). Exact fix: "A stalled or starved owner therefore never fails the run before its windows after SIGKILL have elapsed on its own clock."

**S1 - SUGGESTION - Tests**
No control exercises the 10 s values themselves: M15 (windows back to 2 s) stays green. A planted descendant that dies about 3 s after its SIGKILL, at production constants, would pin "a stall shorter than the window is not judged" for about 4 s of preflight.

**S2 - SUGGESTION - Docs**
The 13 ms against 30 ms census figure at `scripts/owned_process.py:84` has no published receipt.

## Clean-lens evidence

```text
[R764] PASS Conformance - #833 acceptance 1 and 2; scripts/owned_process.py:109-130,256-337; receipts/cause-classification.txt; receipts/mutations/M12-report-without-state.* - the message prints state, wchan, parent and age (M12 red); each of the 12 captured messages is classified 8 Z / 1 T / 3 D from raw receipts; acceptance 2 is met as a real fix with derived windows, and Relates-to is correct because Probe.ready's 15 s bound is still load-sensitive
[R764] PASS RTL - scripts/owned_process.py:256-337 (cleanup state machine; the delta has no HDL): grace → kill_all → limit stages, the single resume, the root skip, the new-descendant rules, failure-path SIGKILL and the bounded empty-listing branch; every transition is reachable and terminating (M03-M11, probes); the pidfd plus start-time recheck is unchanged in safety
```

## Lens ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #833 body and acceptance, A726 comments, PR body; `scripts/owned_process.py:109-130,256-337`; `receipts/cause-classification.txt`; author `final-*`, `round0-*`, `cause/*` receipts | R764-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| RTL | CLEAN | `scripts/owned_process.py:29-337` (no HDL in the delta; architecture of the cleanup state machine); mutations M01-M15; `receipts/probe-*` | R764-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Robustness | UNCLEAN (F3) | late resume, stall, re-parent, late exit, survivor and endless-listing paths; `scripts/process_test_support.py:19-22,196,219`; `scripts/test_suite_cancellation.py:142,329`; `tb/verilator/gptp_shadow/test_mutant_lifecycle.py:232`; `receipts/probe-late-survivor-head.log`; `receipts/compare/` | R764-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Tests | UNCLEAN (F2) | `scripts/test_suite_cancellation.py:372-653`; `receipts/mutations/` (19 runs), `receipts/mutations-identity/`, `receipts/probe-trap-child-*`; host and namespace runs at head | R764-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Docs | UNCLEAN (F1, F2, F3, F4; R1, R2 residue) | `docs/testing/TESTING.md:214-266`; `tb/verilator/gptp_shadow/README.md:117-124`; added source comments; PR body; `ci/image/command-table.json`; `receipts/command-table-staleness.txt`; focused doc gates rc 0 | R764-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |

## Executed here (each with its own log and rc)

- Mutations: 19 runs plus 2 identity-half runs, each in a fresh shared clone at the head, in its own user and PID namespace. The 3 unmutated controls are green.
- Probes at production constants: trap-child at the head and under M07; late-survivor at the head.
- Equal-load comparison of `63044c82` against the head (`receipts/compare/`).
- Host-level `scripts/test_suite_cancellation.py` and `test_mutant_lifecycle.py` at the head: rc 0, rc 0.
- Focused gates at the head, all rc 0: `check_py_idiom.py` and its `--selftest` (54 of 54), `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check`, `check_hygiene.py --check`, `check_doc_paths.py`, and `git diff --check 1f29f189 d4d8cff`.
- `check_em_dash.py` **NOT RUN**: its pinned renderer dependency is absent and installing it is not allowed. A byte search of the added lines found 0 em dashes (`receipts/gates/em_dash_manual.txt`).
- Restore check: the review clone is at the exact head, tree, index, blobs and modes, with all six gitlinks unchanged and no untracked or ignored files in the touched directories (`receipts/restore-verification.txt`). Every probe used separate clones under `scratch/`.

## Real limits

- I did not reproduce the failure classes myself. My comparison at load average 78 does not separate the trees, and I ran no load of 16 runnable per CPU or a host load of 250. The cause table and the CLEANUP FAILED counts rest on the published raw receipts.
- I did not re-execute the author's sweep shards, builder legs, `behave` or the `docs.yml` replay; those are author receipts only. No full parent, PP, gPTP or Yosys bank and no Docker or act runs were made, as instructed.
- Hosted evidence at the exact head (`receipts/hosted-checks-snapshot.txt`): 20 success, 1 skipped (`Physical gPTP (nightly and manual)`, a skipped context, not an executed one), and 29 queued or in progress. No failure yet. Physical calibration was NOT RUN, and field skips are not hardware proof.
- The 10 s windows cannot be checked by a stall-free control (M15 green). Their adequacy rests on the stalls measured on one host.

## Pending manager duties

- Hosted and act acceptance on the exact head, and the current-`dev` merge-candidate builder and native banks at the merge turn.
- Re-review after F1 to F4 are answered. F1 and F3 touch Docs and Robustness artifacts, and F2 touches Tests, so those lenses must be covered again at the new head.
- Decide whether #833 closes after this lands, or whether the `Probe.ready` 15 s handshake (`scripts/process_test_support.py:196`) gets its own Issue (AGENTS §4, newly discovered work).
- Carry R1 and R2 to the residue checklist.

R764-1 FINISHED

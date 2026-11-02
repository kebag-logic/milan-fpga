[R763] NEGATIVE - exact head d4d8cff92658e57b11090c97daf7b44edb31b3b6

# R763-1: internal cleared-context review of PR #834 (issue #833)

- Head `d4d8cff92658e57b11090c97daf7b44edb31b3b6`, tree `7cf0eb4fdbcafbb8ea82c89fdefbaf94c013ac91`, 14 commits on `dev` `1f29f189279f9fc0132f4918e47342b87d22f33a`.
- Changed files: `scripts/owned_process.py`, `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py`, `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`, `docs/testing/TESTING.md`.
- Sources, in order: AGENTS.md, CONTRIBUTING.md (via AGENTS), docs/README map, the #833 body and its three comments (priority raise, TAKEN, REVIEW READY), the PR #834 body, the diff and its history, then the public evidence tree `review-evidence/833-r1` at `1ca64e404244f88d2dcd679c677541b199ca5c06`.
- The review used no private author material and no other reviewer's report.

**Verdict: NEGATIVE.** Four MINOR findings are open, two RESIDUE items and two SUGGESTIONs are recorded, and two lenses (Conformance, RTL) are clean.

The fixes are real. Each of the six named fixes has a control that goes red when that fix alone is reverted at this head. The cause table matches the raw receipts, and a survivor still fails the run. The open findings are about the PR's tests and contract text:
- A stale "two seconds" contract line.
- A false "up to 24 s" bound.
- A new sweep-preflight control whose death window is shorter than the PR's own measured tail.
- One behaviour change with no control that detects its reversal.

## Prior public findings

PR #834 has no review, no review comment and no finding (0 reviews and 0 inline comments; the only PR comment is the review-start notice). #833 has no reviewer findings. So nothing needed to be resolved or retained.

## Focus checks

### (1) The cause table: CONFIRMED

All 12 `CLEANUP FAILED` messages captured on the before tree (`63044c82`, which is `dev` plus only the new message) appear verbatim in their raw receipts: 12 of 12 (`receipts/cause-messages-in-raw.txt`). My own classification (`scripts/classify_messages.py` → `receipts/cause-classification.txt`):

| Count | Class | Raw receipts |
|---:|---|---|
| 8 | `Z`, and the parent is the owner | `cause/f-s256.jsonl` ×4, `final-focus-L192/before.jsonl` ×3, `final-suite-L48-M6/before/001.log` |
| 1 | `bash` `T` in `do_signal_stop`, not sent SIGKILL, holding a `Z` child | `final-focus-L192/before.jsonl` n=1 |
| 3 | `D` after SIGKILL: `__mmap_region` 2.07 s (beside an owner zombie and a re-parented `git`), `unlink_file_vma_batch_process` 1.36 s, `dup_mmap` 1.91 s | `round0-at-f6b776e7/fullsuite-round0-1/before/00{1,2,4}.log` |

Why "parent = owner" can be read from the message alone: the census lists every descendant. A listed process whose parent is not also listed therefore has the owner as its parent, because a child whose parent died is re-parented to the owner, which is the subreaper.

The 3.04 s owner stall (`slowest-cleanups.txt`, `pass@0.513 took 3.042`) is in the receipts. So are the 0.23 s maximum over 121,660 kills and the 7.958 s spawn stall (`deadline/killlat-summary.txt`). One caveat: 7.96 s is a process-start latency. It is not a kill-to-death latency.

### (2) Each fix is real and has a red mutation at this head: CONFIRMED

I wrote my own mutation builder and ran each mutant in its own unprivileged PID namespace, one control per run (`scripts/mutate.py`, `scripts/run_control.py`, `receipts/mutants/`, `receipts/mutation-matrix.txt`):

| Mutant (applied alone to head `owned_process.py`) | Red controls |
|---|---|
| none | 0 of 7 (all pass) |
| identity includes the parent | `owner_reparented`: "re-parented descendant was treated as new and never got SIGTERM" |
| no reap after the census | `owner_late_exit`: `CLEANUP FAILED ... state Z ... not sent SIGKILL` |
| deadline on the wall clock | `owner_stall`: `CLEANUP FAILED ... not sent SIGKILL` |
| pass cap 5 s, not 0.5 s | `owner_stall` |
| no resumed-shell window | `owner_shell_window` |
| no SIGKILL before raising | `owner_survivor`: "stopped shell left behind" |
| endless listing unbounded | `owner_vanishing`: "cleanup never reached a verdict" |
| survivor never fails (verdict removed) | `owner_survivor`: "a survivor never failed the run"; `owner_vanishing` |
| report without state; report without wchan | `owner_report`, `owner_survivor` |
| cleanup does nothing | 6 of 7 |
| a SIGKILLed process counts as gone | 0 of 7. The run still fails, through the empty-owned verdict path, with the survivor named. This is not a test gap. |
| trap-started commands get the pre-change 1 s | **0 of 7: see F4** |

### (3) The survivor control and the 10 s window

A true survivor still fails the run. The `owner_survivor` control is red under the "verdict removed" mutant.

The 10 s window is evidence-based. It comes from:
- the measured D tail: 1.36, 1.91 and 2.07 s, all lower bounds;
- per-process kill latency: at most 0.23 s over 121,660 kills at load up to 111;
- episode stalls of 3.04 s and 7.96 s.

10 s outlasts the largest of these, and the owner clock's 0.5 s cap means a host stall that also stalls the owner cannot use up the window. The specific value is a round-up above the largest measured episode, not a computed quantile. I accept this under acceptance item 2's "deadline ... from that evidence".

The stated report time is wrong, though: see F2.

### (4) Before and after at equal load: COUNTS CONFIRMED, one attribution is missing from the PR body

I recounted every row from the raw rc and log files:

| Row | Before | After |
|---|---:|---:|
| Full suite | 0/10 | 10/10 |
| Lifecycle | 0/18 | 18/18 |
| Sweep test | 11/12 (1 `CLEANUP FAILED`) | 12/12 |
| Focus at load 230–311 | 4/10 (4 `CLEANUP FAILED`, 2 boundary) | 6/10 (0 `CLEANUP FAILED`, 4 `missing boundary` from the 15 s `Probe.ready`) |

All 12 after-tree sweep logs contain `CLEANUP FAILED` only in the `owner-survivor:` line, which is the control's own print.

Every one of the 28 before failures in the first two rows is the 12 s `Probe.finish` bound (`TimeoutExpired`), and none is `CLEANUP FAILED` (`receipts/before-failure-modes.txt`). So those two rows measure the `FINISH_SECONDS` change, not the ownership fixes. HANDOFF.md says so; the PR body does not (RESIDUE X1).

### (5) No host-wide signal or process match in committed code: CONFIRMED

Every signal call added in the delta goes to one of these, and to nothing else:
- a `Popen` child (`sleeper`, `middle`, `child`);
- the test process itself;
- one known re-parented child, rechecked by start time in `really_kill` (`test_suite_cancellation.py:425-429`). It is held as an unreaped zombie of the test, so its PID cannot be reused before the kill.

The product's census reads `/proc` host-wide, but it signals only descendants, through a pidfd plus a start-time recheck (`owned_process.py:240-254`).

The lane's load tools (`receipts/load-tools/`, including `stoptests.py` with its archive-only redaction at line 36) are not in the tree: `git ls-files` finds none of them.

### (6) The stale `ci/image/command-table.json`: DECISION ACCEPTED

`scripts/command_table_staleness.py` gives (`receipts/command-table-*.txt`):

| | Script pins checked | Hash differs | Absent from the tree |
|---|---:|---:|---:|
| `dev` `1f29f189` | 149 | 32 | 5 (4 of them are in submodules, so my superproject-only method cannot check them) |
| This head | 149 | 36 (the 4 files this PR changes are added) | 5 |

The author's "33 of 143" matches 32 + 1 on the numerator; the denominator method is unstated. No workflow and no sweep step validates the table's script pins:
- the four workflows do not reference `ci/image`;
- `run_all_suites.sh` does not either.

Regenerating the table would sweep in about 33 unrelated pins, so leaving it unregenerated is the proportionate choice. "Nothing reads it" is inaccurate wording (RESIDUE X2). A tracking Issue would help (SUGGESTION S1).

### (7) `Relates to` or `Closes` #833: `Relates to` IS CORRECT

Acceptance item 2 asks for "no suite left to fail by chance". After the change, 4 of 10 focus runs at load 250–314 still fail at `Probe.ready`'s 15 s handshake (`final-focus-L192/after.jsonl`), and F3 adds a new short window to the preflight. Closing the issue, or splitting the handshake into its own Issue and closing #833 by hand, is the maintainer's decision (SUGGESTION S2).

### Hosted contexts at this head

This is a read-only snapshot (`receipts/hosted-check-runs-snapshot.txt`). Many contexts were still queued or in progress at the time, and those completed had succeeded, including:
- `changes`
- `full-ci-gate`
- `verilator-lint`
- `elaborate-gates-0`
- `docs-gates-1`
- Verilator shard 8/19
- the firmware jobs

`Physical gPTP (nightly and manual)` is skipped, which is not execution. I make no hosted acceptance claim.

## Findings

**F1: MINOR. Lenses: Docs.** `docs/testing/TESTING.md:223-224`: the authoritative cleanup contract still states the old stages.
- Authority/evidence: the lines read "Cleanup allows two seconds before escalating stubborn descendants. Another two seconds bound reaping and terminal trap cleanup." At this head:
  - 2 s of grace, then a further 2 s until SIGKILL reaches every descendant (`scripts/owned_process.py:37-38`);
  - then 10 s from the last SIGKILL to the verdict (`:40`);
  - and 10 s for a resumed shell's trap (`:39`);
  - all on a clock that one census pass advances by at most 0.5 s (`:45`, `:284`).
  The PR added the new contract at `TESTING.md:258-264` but left 223-224, so the page contradicts itself and the code. AGENTS.md §6 Docs: "Changed contracts are reflected in authoritative docs."
- Impact: a reader of the authoritative page gets a 4 s cleanup bound that no longer exists, and a 2 s trap window that is now 10 s.
- Required outcome: lines 223-224 state the head's stages and clock, or are replaced by the new lines, with no contradiction left.
- Verification: read `TESTING.md` against `owned_process.py:37-45,284-310`.

**F2: MINOR. Lenses: Docs.** `scripts/process_test_support.py:20-21` ("a true survivor takes up to 24 s of owner cleanup to report") and the PR body's "reported after 14 to 24 s of owner clock". The stated bound is false.
- Authority/evidence: a shell can be resumed at any owner clock below 14 s, so `kill_all` can reach just under 24 s and the verdict just under 34 s. On the empty-owned path (`:290`) it can take a further 10 s.
- Probe with the shipped constants (`scripts/probe_bounds.py`, `receipts/bounds/`): a slow death delivered 6.5 s after the first signal, plus a survivor started by the shell's trap, was reported at **26.52 s**. At 13.5 s it was reported at **33.51 s**. Controls: no slow death, 22.04 s; slow death without a trap survivor, clean at 13.5 s and 13.9 s.
- Impact: the stated input to the `FINISH_SECONDS` derivation understates the worst case by about 10 s. 60 s still covers 34 s plus the 15.1 s driver, so no test changes today. But the figure is wrong, and it is a figure, so this is not RESIDUE.
- Required outcome: the comment and the PR text state the real bound (just under 34 s of owner clock for a survivor) and confirm that `FINISH_SECONDS` covers it together with the measured driver time.
- Verification: rerun `probe_bounds.py SCRIPTS 13.5 1` and compare the reported time with the stated bound.

**F3: MINOR. Lenses: Tests, Robustness.** `scripts/test_suite_cancellation.py:505-527` (`owner_stall`) with `:405-415` (`stages`). A new control in every sweep's preflight requires the planted child to die within about 2.5 s of its SIGKILL. That is shorter than the PR's own measured death tail.
- Authority/evidence: `owner_stall` sets `GRACE_SECONDS=0.5`, `KILL_ALL_SECONDS=0.5`, `REAP_SECONDS=2.0`. The SIGKILL lands at about 0.5 s of owner clock and the verdict comes at 3.0 s. The `stages` docstring says it is for "a control whose result does not depend on them"; this control's result does.
- Probe (`scripts/probe_stall_window.py`, `receipts/stall-window/`) with the shipped control and its SIGKILL delivered late, as in state D:

  | Delay | Result |
  |---|---|
  | 0, 1.0, 2.0, 2.3 s | PASS |
  | 2.7, 3.0 s | **FAIL**: `CLEANUP FAILED ... sent SIGKILL 2.51 s ago` |

- The PR measured D deaths of 1.36, 1.91 and 2.07 s, as lower bounds, at load about 250 (`owned_process.py:30-36`; the cause table above). It set the product window to 10 s precisely because "the tail comes in episodes".
- The control runs in the sweep preflight (`scripts/run_all_suites.sh:288`), the very place #833's #828 replay failed. Acceptance item 2: "no suite left to fail by chance".
- Impact: this adds a new chance failure to every sweep at the loads #833 is about. The control would fail at the same tail the product now tolerates.
- Required outcome: `owner_stall`'s verdict does not depend on a death window shorter than the measured tail, or that dependence is stated and justified. The wall-clock and pass-cap mutants must still go red.
- Verification: `probe_stall_window.py` passes at head for delays up to the chosen window; the `deadline-wall-clock` and `pass-cap-5s` mutants stay red.

**F4: MINOR. Lenses: Tests.** `scripts/owned_process.py:329-331`: no control detects reversal of the changed window for commands that a resumed shell's trap starts.
- Authority/evidence: this changed behaviour (the old code gave trap-started commands `now < resumed + 1.0`; now they share the shell's 10 s window) has no control that fails when it is reverted. The `trap-commands-1s` mutant passes all 7 owner controls (`receipts/mutation-matrix.txt`), because the trap in `owner_shell_window` only runs the builtin `echo`.
- It matters in production: the sweep's EXIT trap runs an external `rm` on both lock paths (`scripts/run_all_suites.sh:223` `cleanup() { rm -f "$LOCK_OWNER"; }` and `:236`, installed at `:238`).
- Demonstration (`scripts/trapcmd_variant.py`, `receipts/trapcmd/`): a variant of `owner_shell_window` whose trap runs `sleep 1.5 && echo ...` passes 3 of 3 at head and is red 3 of 3 under the mutant.
- AGENTS.md §5: "add or update self-checking tests for changed behavior"; §6 Tests: "Each new test can fail for the defect it claims to detect".
- Impact: a regression back to 1 s would SIGKILL the trap's lock-record removal under load, and no gate would notice.
- Required outcome: a control in which the resumed shell's trap starts an external command that needs more than 1 s goes red when the clause is reverted.
- Verification: the `trap-commands-1s` mutant is red; head is green.

**X1: RESIDUE. Lenses: Docs.** PR #834 body, "Before and after" table, rows `make -C tb/verilator/gptp_shadow` and `... lifecycle`.
- Every before failure (10 of 10 and 18 of 18) is the 12 s `Probe.finish` bound, and none is `CLEANUP FAILED` (`receipts/before-failure-modes.txt`). HANDOFF.md states this; the PR body does not.
- Exact fix: add "all before failures at the fixture's 12 s hang bound, none `CLEANUP FAILED`" to those two rows.

**X2: RESIDUE. Lenses: Docs.** PR #834 body, "Known limitations", last bullet: "and nothing reads it".
- `ci/image/build.py:151` hashes the table as an image recipe input, and `scripts/ci_command_table.py:17` and three self-tests read it. What is true is that no workflow or sweep step validates its script pins.
- Exact fix: replace "and nothing reads it" with "and no workflow or sweep step checks its script pins".

**S1: SUGGESTION.** File an Issue for `ci/image/command-table.json` script-pin staleness: 32 differ on `dev`, 36 at this head (`receipts/command-table-*.txt`).

**S2: SUGGESTION.** At merge, record on #833 whether `Probe.ready`'s 15 s handshake (and the five new `published()` 15 s handshakes the new controls add to the preflight, `test_suite_cancellation.py:418-422`) stays under #833 or moves to its own Issue.

## Comment rule

I scanned all 445 added lines (`git diff -U0`):
- no bench lane labels, lane names, review rounds, reviewer IDs or issue-comment IDs;
- the only issue ID is `#833` (14 occurrences).

No RESIDUE under the comment rule.

## Commits and hygiene

- All 14 commits are one-line with no trailers.
- `git diff --check 1f29f189 d4d8cff9` gives rc 0.
- The file modes of all five changed files are 100644.

## Executed at this head (my runs, in PID namespaces, at most 14 parallel jobs)

| Run | rc | Result |
|---|---:|---|
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`, including the seven new owner controls (`receipts/head/test_suite_cancellation.log`) |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` (`receipts/head/lifecycle.log`) |
| Mutation matrix | — | 14 mutants × 7 controls (`receipts/mutation-matrix.txt`) |
| Bound, trap-command and stall-window probes | — | as cited in F2, F3 and F4 |

## Clone integrity

After the probes:
- the index sha256 is unchanged (`b10052e7…`);
- the blob hashes and modes of all changed files match `HEAD`;
- there are 0 status entries, including ignored files: I removed the bytecode caches my runs created;
- the six submodule gitlinks are unchanged.

See `receipts/clone-integrity.txt`. No source edit, commit or push was made.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #833 acceptance 1–2 against: the `owned_process.py:109-130` message; `receipts/cause-classification.txt` (12 of 12 classified from raw); fix-to-cause mapping `owned_process.py:226-337`; before/after recount; the `Relates to` reasoning against `final-focus-L192/after.jsonl` | R763-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| RTL (architecture of the cleanup state machine; no HDL changed) | CLEAN | `owned_process.py:80-130,209-337`: census, identity, pidfd plus start-time send, reap order, clock cap, verdict and pre-raise SIGKILL, root-shell stop/resume transitions, empty-owned path, `__exit__` restore; probes `receipts/bounds/`; mutation matrix | R763-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Robustness | UNCLEAN (F3) | `test_suite_cancellation.py:405-640` windows and handshakes; `receipts/stall-window/`; `process_test_support.py:20-22,219`; the D and stall receipts | R763-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Tests | UNCLEAN (F3, F4) | `receipts/mutation-matrix.txt` (14 mutants × 7 controls); `receipts/trapcmd/`; head runs `receipts/head/`; author gate receipts (`gates/sweep/shard-0..3/spec/complete.json` rc 0 at this head, 64 `docs.yml` step rcs 0, behave 2330 steps, builder legs rc 0) | R763-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |
| Docs | UNCLEAN (F1, F2; RESIDUE X1, X2) | `docs/testing/TESTING.md:215-266`; `tb/verilator/gptp_shadow/README.md` cancellation section; source comments in the delta; PR body; HANDOFF.md | R763-1 | d4d8cff92658e57b11090c97daf7b44edb31b3b6 |

## Real limits

- I did not reproduce the D-state or host-stall classes under real compile load. F3's window comparison uses the PR's own measured tail together with a simulated late SIGKILL, not a live D state.
- My mutants ran in PID namespaces, where a census is cheap. Load-dependent behaviour was judged from the author's receipts.
- I did not rerun the full sweep, the builder legs, `behave` or `docs.yml`. I read the author's published receipts for these and did not re-execute them.
- I did not verify the 4 command-table pins inside submodules.
- Physical calibration: NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Hosted and `act` acceptance on the exact head: several hosted contexts were still in progress at my snapshot.
- Current-dev merge-candidate validation (builder and native banks) at the merge turn.
- Carry X1 and X2 to the residue checklist.
- The `Relates to`/`Closes` decision for #833 (S2).
- An Issue for the stale command table (S1).

R763-1 FINISHED

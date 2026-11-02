[R764] NEGATIVE - exact head c1b2961777809403bd2de833ec1fa00c75394d6c

# R764-4 external review: issue #833 / PR #834, round 4

- Head under review: `c1b2961777809403bd2de833ec1fa00c75394d6c`, tree `28a722419d061920d79833cd95c6c9fabe4a4953`. This matches the PR's live `headRefOid`. The PR is not a draft, base `dev`.
- Source base: `1f29f189279f9fc0132f4918e47342b87d22f33a`. Previously reviewed head: `3740565f4315cccc4e6dfb8d0b37ec9b55b65ec2` (R764-3 POSITIVE, R763-3 NEGATIVE).
- Round 4 delta `3740565f..c1b29617`: 2 one-line commits with no trailers. 3 files change, +13/-11:
  - `scripts/test_suite_cancellation.py:563-565` (control timing);
  - `scripts/process_test_support.py:22-29` (comment);
  - `docs/testing/TESTING.md:224,230` (guide).
- `scripts/owned_process.py` is byte-identical to `3740565f` (`git diff --quiet 3740565f c1b29617 -- scripts/owned_process.py`).
- No file in the whole PR is HDL (`receipts/pr-files.txt`: five Python/Markdown files, 0 `.sv/.v/.svh/.vh/.xdc/.tcl`).

## Verdict basis

- **R763-3-F1 is resolved at its cause, as its required outcome states.** I reproduced this independently, each run in its own user+PID namespace, at host load 44 to 90 on 16 CPUs.
  - `owner_shell_window` now goes red when the `clock < kill_all` term is removed from `owned_process.py:317`: 16 of 16 runs, plus 3 of 3 in the matrix, plus the whole suite (rc 1, 5.4 s).
  - M05, M06, `no-trap-window`, `trap-commands-no-window` and `trap-commands-1s` stay red, 3 of 3 each.
  - The control is green unmutated: 16 of 16 at 3.2 s, plus 3 of 3 in the matrix.
  - The author's re-run of R763-3's matrix differs from R763-3's table in exactly that one row.
- **The three retained residue items are taken with their exact fixes**: R763-2-X1, R763-2-X2 = R764-2-R2, and R764-2-R1. See [Prior findings](#prior-findings-at-this-head).
- **The verdict is NEGATIVE for one new MINOR, R764-4-F1 (Tests, Docs), found by falsifying the strengthened control.**
  - The control now pins one half of the guard: "never in the pass that resumes it". It does not pin the other half: "only after its own window".
  - A mutant that spares the resumed shell for the resume pass only stays green on every owner control (16 of 16) and on the whole suite (rc 0). That is a regression the guide's claim says the controls catch.
  - Under that mutant, a trap with 0.1 s of builtin work is cut short. The head lets that trap finish.
  - The product at this head is correct. Only the test cannot see this regression.

## Findings

**R764-4-F1 - MINOR - Tests, Docs - `scripts/test_suite_cancellation.py:542-581` (`owner_shell_window`) vs `scripts/owned_process.py:315-318`; `docs/testing/TESTING.md:273`**

- **Requirement/evidence.**
  - The guard at `owned_process.py:315-317` says: "A notified shell is SIGKILLed only after its own window: never in the pass that resumes it". It reads `(resumed is None or clock < kill_all)`, and `kill_all` is the resume plus `TRAP_SECONDS` (`:312`).
  - `TESTING.md:273` lists, among what the preflight controls establish: "A shell resumed late keeps its whole window to run its terminal trap and the commands it starts."
  - AGENTS.md section 6, Tests: "Each new test can fail for the defect it claims to detect."
- **Mutants (my `scripts/mutants.py`):**
  - `shell-window-one-pass`: `(resumed is None or clock <= resumed)`. The shell is spared in the resume pass only.
  - `shell-window-1s`: `(resumed is None or clock < resumed + 1.0)`.
- **Results for those mutants:**
  - Both are green on all 8 owner controls (`receipts/matrix-table.md`, 3 runs each).
  - On `owner_shell_window` alone both are green 16 of 16, at the head's 3.2 s (`receipts/repeat.txt`).
  - With `shell-window-one-pass`, the whole `scripts/test_suite_cancellation.py` is rc 0 in 57.2 s, the same as the head (`receipts/whole/`).
- **Why the control misses them.** After the resume pass, `owned_process.py:329` also spares the shell, because it is the parent of a live child: the trap's `sleep 1.5`. The control's trap is never without a live child for longer than a builtin `echo`. So only the resume-pass half of the guard is load-bearing in the control.
- **Impact.** `receipts/impact/summary.txt` uses `scripts/builtin_phase_probe.py`, the control's own set-up with the trap's last step after a builtin-only interval.
  - The head finishes the trap after 0.1, 0.5 and 2.0 s of builtin work.
  - `shell-window-one-pass` cuts all three short: `trap_finished=False`.
  - `shell-window-1s` cuts the 2.0 s one short.
  - The sweep's real trap starts with builtins: `cancelled` runs two `echo`s, then `exit`, then the EXIT trap's `rm` (`scripts/run_all_suites.sh:125-135,223,236-238`). Under load, a resumed shell that is not scheduled within one census pass would lose its lock-record cleanup.
  - A regression to a one-pass window would pass every control, while `TESTING.md:273` says the controls show the whole window is kept. This is the same class of gap as R763-3-F1, on the same guard.
- **Required outcome.** Either of these, without prescribing a design:
  - a control in which a resumed shell, past grace + 1 s, spends at least one census pass inside its trap with no live child, and whose last trap step is observable. It must go red under `shell-window-one-pass` and stay green unmutated. M05, M06, `no-trap-window`, `shell-killed-when-resumed` and `trap-commands-*` must stay red. One cheap shape, not prescribed: a builtin-only wait of about 0.2 s between the trap's `sleep` and its marker write.
  - or `TESTING.md:273` and the control's docstring state only what the control pins.
  - `shell-window-1s` going red is optional, because it costs about 1 s more of preflight.
- **Verification.** Re-run `scripts/matrix.py` and `scripts/repeat_control.py` from this packet with `scripts/mutants.py`. `shell-window-one-pass` must be red on at least one owner control. No other row may change from `receipts/matrix-table.md`, apart from optionally `shell-window-1s`. `none` must stay green.

**R764-4-S1 - SUGGESTION - Tests, Robustness - `scripts/test_suite_cancellation.py:565`**

- The control has a 0.3 s margin on the owner's clock. Its detection of `shell-killed-when-resumed` depends on the resume landing after `deadline + 1.0` = 1.2 s of owner clock (`owned_process.py:327`). The child dies 1.5 s of wall time after the first signal.
- The owner's clock falls behind wall time only while a pass takes longer than 0.5 s (`:284`). So under a heavily stalled owner the resume could land before 1.2 s, and the mutant would go green again. A false red is not possible; only detection is lost.
- I saw no such loss at load 44 to 90 (16 of 16 red). Optional: assert, or print, the owner clock at the resume, so a lost margin is visible rather than silent.

**R764-4-S2 - SUGGESTION - Tests - PR body, Round 4, "R763-3-S1 ... is not taken"**

- The reason given is that a control for S1 "would change a row in the same round", against F1's "no other row may change".
- That verification clause guards against collateral changes. It does not forbid a suggested mutant turning red on purpose.
- S1 stays an optional SUGGESTION, and the PR body could say so on its merits rather than through F1's clause.

**R764-3-R1 - RESIDUE (retained, not taken, not listed in the PR body) - Docs, Tests - `scripts/test_suite_cancellation.py:661`**

- The comment still reads "A re-armed window would hold the verdict past this bound: TRAP_SECONDS is longer." The line moved from `:659` to `:661` with the round 4 insert.
- Exact fix, as in round 3: "A re-armed window would hold the verdict past the 15 s bound below: TRAP_SECONDS is 30 s."
- The PR body's Round 4 section does not mention it. The manager should carry it to the residue checklist.

## Comment rule

The new comment lines at `scripts/test_suite_cancellation.py:563-564` and `scripts/process_test_support.py:22-29` state behaviour and reason only. They contain no bench lane label, lane name, review round, reviewer ID or issue-comment ID (grep over the added lines). There is no new instance.

## Prior findings at this head

| Finding | Severity | Status at `c1b29617` | Evidence |
|---|---|---|---|
| R763-3-F1 (in-window guard `owned_process.py:317` not pinned) | MINOR | **RESOLVED** (required outcome met) | `test_suite_cancellation.py:565`: the child dies 1.5 s after the first signal. With the term removed: red 16/16, 3/3, and whole suite rc 1. Unmutated: green 16/16 and 3/3. M05, M06, `no-trap-window`, `trap-commands-no-window` and `trap-commands-1s` red 3/3. The author's `matrix-r763-3/matrix-table.md` against R763-3's table: one row differs, `shell-killed-when-resumed` ok → RED(1). The guard's other half is still not pinned: new R764-4-F1 |
| R763-2-X1 (deadline after a resume applies to every descendant) | RESIDUE | **TAKEN, exact fix** | `TESTING.md:230`, `process_test_support.py:22-24` and the PR body's "The deadline's derivation" all read "After a resume, every remaining descendant's deadline is 20 s after the resume, including one the trap started." This is true by `owned_process.py:289,312`: once the resume extends `kill_all`, `limit = kill_all + REAP` is the resume plus 20 s |
| R763-2-X2 = R764-2-R2 (`TESTING.md:224`) | RESIDUE | **TAKEN, R764-2-R2's wording** | It reads "... except a cancelled shell, which keeps its own window." "Cancelled" is the better of the two fixes: `:317` spares a notified shell both before its resume and inside its window. The PR body states this reason |
| R764-2-R1 (PR body survivor sentence) | RESIDUE | **TAKEN, exact fix** | PR body line 49: "A true survivor still fails the run, as it did at 4 s before this change. Its deadline is now 14 s into cleanup on the owner's clock." |
| R764-3-R1 (`:659` "this bound") | RESIDUE | Retained, not taken | see above |
| R763-3-S1 ("listed" half of the resume condition) | SUGGESTION | Retained, optional | see R764-4-S2 |
| R764-2-S1, R763-2-S1/S2/S3 | SUGGESTION | Retained, optional | unchanged by the delta |

## Lens results

```text
[R764] PASS Conformance - scripts/owned_process.py:284-336 (unchanged since 3740565f); docs/testing/TESTING.md:223-236; scripts/process_test_support.py:19-30; PR body "The deadline's derivation" (receipts/pr-body-at-review.md); issue #833 acceptance 1-2 - every changed timing statement read against the code: 2 s SIGTERM, SIGKILL to all but a notified shell by 4 s (:313-333, :317), 14 s survivor limit (:289), resume only before 14 s (:290 precedes :304), resume + 20 s for every remaining descendant (:312, :289), +10 s for a listing (:290), 0.5 s pass cap (:284); FINISH_SECONDS 49.6/59.6 s arithmetic unchanged; acceptance unchanged from the prior verdict because the product file is byte-identical
[R764] PASS RTL - receipts/pr-files.txt - the PR touches 5 Python/Markdown files and no HDL, constraint or synthesis file, so no clock, reset, CDC, FSM or width contract is in scope; the cleanup state machine (owned_process.py:270-339) is unchanged since 3740565f
[R764] PASS Robustness - scripts/owned_process.py:315-333; receipts/repeat.txt; receipts/matrix-table.md; receipts/whole/none.* - product code unchanged; the strengthened control is deterministic at host load 44-90 (green 16/16 at 3.2 s, red 16/16 at 1.7 s under its target mutant) and the whole suite is rc 0 at head; margin note only (S1)
[R764] MINOR Tests - scripts/test_suite_cancellation.py:542-581 vs scripts/owned_process.py:315-318 - R764-4-F1 (R763-3-F1 itself resolved: receipts/matrix-table.md, receipts/repeat.txt, receipts/whole/)
[R764] MINOR Docs - docs/testing/TESTING.md:273 - R764-4-F1 (the guide's control claim is wider than what the control pins); TESTING.md:224,230 and process_test_support.py:22-29 otherwise exact; residue R764-3-R1 retained
```

## Evidence

| Receipt | Content | Result |
|---|---|---|
| `receipts/manifest-all.txt` (`scripts/verify_manifest.py`) | Evidence commit `ff8233016a903703c4899acc56aad485889887dc`, `review-evidence/833-r1/MANIFEST.json` (sha256 `d697e62a6ac367f7facf32161712818d58eff3af9fd7b6e743a0cdc36ac8a168`) | 4965 files ok, 0 bad, 0 missing, 0 unlisted; `author-r4/` alone has 1082 ok. GitHub reports the commit as unsigned, and there is no detached signature to verify, so integrity rests on the manifest digests |
| `scripts/mutants.py`, `scripts/matrix.py`, `scripts/run_control.py` → `receipts/matrix-table.md`, `receipts/matrix/` | 9 mutants × 8 owner controls × 3 runs, 16 jobs, each run in its own user+PID namespace | table in the receipt; only `owner_shell_window` discriminates, as intended |
| `scripts/repeat_control.py` → `receipts/repeat.txt`, `receipts/repeat/` | `owner_shell_window` × 16 for 4 variants | `none` 0/16 red; `shell-killed-when-resumed` 16/16 red; `shell-window-one-pass` 0/16; `shell-window-1s` 0/16 |
| `receipts/whole/` | whole `scripts/test_suite_cancellation.py` on 3 disposable head trees, in namespaces | `none` rc 0 in 57.1 s; `shell-window-one-pass` rc 0 in 57.2 s; `shell-killed-when-resumed` rc 1 in 5.4 s |
| `scripts/builtin_phase_probe.py` → `receipts/impact/` | trap with a 0.1/0.5/2.0 s builtin phase after a late resume | head finishes all three; one-pass cuts all three; 1 s cuts 2.0 |
| `receipts/gates/` | `check_doc_style.py` rc 0 (23 documents); `docs_check.py` rc 0 (0 findings, 1 git-only check skipped on the archive tree); `check_py_idiom.py` rc 0 (in the clone) | green |
| `receipts/clone-integrity.txt` | `git diff --check 1f29f189 HEAD` rc 0; head and tree match; index = HEAD tree (mode, blob, path); clean status including ignored files; gitlinks `external` efeb541a, `gptp-processor` 135afd04, `protocol-processor` a9e84b66 | restored and verified |
| `receipts/hosted-check-runs-at-head.tsv` | 23 check runs at the exact head, snapshot during review | 8 completed success (`bdd-conformance`, `changes`, `docs-check-no-git`, `docs-gates-0/1/2`, `Prepare pinned Yosys`, `wire-accountability`), 8 in progress, 7 queued; none failed; no long gate had concluded. Hosted acceptance is the manager's |
| Author receipts spot-checked (`author-r4/receipts/`) | `gates/lane/*.rc`: suite, lifecycle, behave and diffcheck all 0 at this head; `docsyml-verify.rc` 0; `control-quick/` matches my results; `matrix-r763-3` has the one-row diff | consistent |

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `owned_process.py:284-336`; `TESTING.md:223-236`; `process_test_support.py:19-30`; PR body derivation; #833 acceptance | R764-4 | `c1b2961777809403bd2de833ec1fa00c75394d6c` |
| RTL | CLEAN (inapplicable: no HDL in PR) | `receipts/pr-files.txt`; `owned_process.py:270-339` unchanged | R764-4 | `c1b2961777809403bd2de833ec1fa00c75394d6c` |
| Robustness | CLEAN | `owned_process.py:315-333`; `receipts/repeat.txt`, `matrix-table.md`, `whole/none.*` | R764-4 | `c1b2961777809403bd2de833ec1fa00c75394d6c` |
| Tests | UNCLEAN (R764-4-F1 open) | `test_suite_cancellation.py:542-581,661`; `receipts/matrix*`, `repeat*`, `whole/`, `impact/` | R764-4 | `c1b2961777809403bd2de833ec1fa00c75394d6c` |
| Docs | UNCLEAN (R764-4-F1 open; R764-3-R1 residue) | `TESTING.md:224,230,273`; `process_test_support.py:19-30`; PR body (`receipts/pr-body-at-review.md`) | R764-4 | `c1b2961777809403bd2de833ec1fa00c75394d6c` |

## Limits

- No manager source bank exists at this head, and none is claimed or inferred. Source-head execution evidence is the author's published gate receipts, which I spot-checked; my own runs are the focused probes above.
- The current-dev merge candidate (source base `1f29f189`, live dev `503bc97c`) is not validated here.
- I ran no full parent, PP, gPTP, Yosys or builder bank, and no lifecycle `make` target, Docker/act or hardware. Physical calibration was NOT RUN. A field skip is not hardware proof.
- The hosted contexts were mostly still queued or running when snapshotted. Executed jobs are distinguished from pending ones in `receipts/hosted-check-runs-at-head.tsv`.
- All load figures are host load averages at run time (44 to 90 on 16 CPUs). They are not booked-CPU measurements.
- Receipt logs contain disposable scratch and temporary-directory paths of this host, with no user names.
- Disclosure: while searching the public comments for a published packet digest, a keyword search matched one line of the other reviewer's round 4 report. That line was about evidence-manifest verification and contained no finding. I read nothing further of that report, and it did not inform this review.

## Pending manager duties

- Carry R764-4-F1 to the author. The Tests and Docs lenses re-cover at the corrected head. A text-only answer, narrowing `TESTING.md:273` and the control docstring, re-covers both only if the claim then matches what the control pins.
- Residue checklist: R764-3-R1 (exact fix above). The round 2 residue is now taken.
- Optional suggestions: R764-4-S1, R764-4-S2, R763-3-S1, R764-2-S1, R763-2-S1/S2/S3.
- Validate the current-dev merge candidate (builder and native banks), confirm hosted exact-head `verilator-suites`/`yosys-portability` and `rtl-fast` conclusions, and link those receipts on the PR.

R764-4 FINISHED

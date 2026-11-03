[R763] NEGATIVE - exact head fce77f0efc1425ef7732a8d70c02addc108f7afe

# R763-10: internal cleared-context review of PR #834 (issue #833)

Head `fce77f0efc1425ef7732a8d70c02addc108f7afe`, tree `5c37f78dadab8c4624d1b84d966d44accda975f1` (`receipts/env.txt`). The round 10 delta is `e803d94b..fce77f0e`, six commits, one per ruling item. It touches `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`. `scripts/owned_process.py` is byte-identical to round 9 (blob `6495a47b` at both heads). Authority: the round 10 ruling on #833 (issuecomment-6592794168).

## Summary

- **Ruling items 1 to 6 are met as written.** Each is checked below with its receipt.
- **`owner_report` is fixed.** At this head, 0 of 3000 runs were red, 8 at once, with the 1-minute load at 40.6 to 56.9 throughout. The prior head ran alongside under the same load, as a sensitivity control, and 5 of 1500 were red (one-sided Fisher p = 0.0041). All six `owner_report` mutants are red with their words.
- **The early, never-resumed and 1 s listings work as claimed.** Each new mutant is red on a named control with its words, and only on its own listings (46 listings).
- **The module moves change no behaviour.** `BLOCKING` moved byte for byte. All 143 prior `MUTANTS` entries are unchanged in value and order.
- **My round 9 sweep at this head: 4224 mutants, 400 survivors** (440 at round 9), in 82 classes. Each class acts only outside a stated domain as item 5 defines it, so all are RESIDUE, listed once below.
- **One finding makes the verdict NEGATIVE: R763-10-F1 (MINOR).** This round's wording of row 3 claims a cell that no listing has: a parent from the first census whose live first-census child outlives its own `SIGKILL`, beside or under a cancelled shell that is never resumed. A natural mutant kills that parent at 3 s instead of 4 s. It survives every owner control and the whole test, and is red on a reviewer listing written from the row. The product is correct in that cell.
- **My own miss, disclosed:** my round 9 sweep could not see this cell. Its probe has no first-census parent beside a shell, so the sweep scored that perturbation as equivalent. My round 9 F2 named only the live *new* child. The cell was already claimed by the unqualified round 9 text, and this round's text makes the claim explicit.

## Ruling items

### 1. `owner_report` (R763-9-F3 = R764-9-F1): MET

- **The fix.** `test_suite_cancellation.py:441-442` is R763-9-F3's exact fix: the child writes its PID, then waits in `signal.pause()` with no timer of its own. `STUBBORN` (`:376-384`) is unchanged, and so is every other use of it; the only changed line is in `owner_report`.
- **The report it checks now shows the pause.** The report reads `state S wchan __do_sys_pause` (`receipts/repo-mutants.log`, the `report-*` lines).
- **My stress run** (`scripts/stress_owner_report.py`, my unchanged round 9 driver; `scripts/burner.py`; `receipts/stress-*`):

  | Tree | Runs | Red | Load (1-minute) |
  |---|---|---|---|
  | Head `fce77f0e` | 3000, 8 at once | **0** | 40.6 to 56.9 for all 13 samples during the runs |
  | Prior head `e803d94b` (sensitivity control, same window) | 1500, 4 at once | 5 | the same |

  - The host's own load was about 8, so I raised it myself: one process held 36 threads runnable (hashing in threads that release the GIL), beside the 12 control runs, on 16 CPUs.
  - The prior head's reds are the round 9 race: `state R` with wchan `0` or `hrtimer_nanosleep`. They show the load was high enough to expose it.
  - The head's 0 against the prior head's 5 is significant at one-sided Fisher p = 0.0041 (`receipts/stress-stats.txt`).
- **The author's published receipts agree** (`author-r10/receipts/final/`):
  - `r763-9-stress-final-head.log`: 3000 runs, 0 red, load at end 42.3;
  - `r764-9-repeat-final-head.log`: 3200 runs, 0 red, mean load 44.2.
- **All six `owner_report` mutants are red with their words** (`receipts/repo-mutants.log`): `report-without-state`, `-wchan`, `-state-or-wchan`, `-current-parent`, `report-age-in-ticks` and `report-parent-is-first-parent`. `none` is green.

### 2. The early-in-grace edge (R763-9-F1): MET

- **The mechanism.**
  - `kept` (`test_suite_cancellation.py:776-787`) runs a listing again, early, when its census grows by `TICK`. The early run inserts `(TICK, "census")` after the first event.
  - `starved_cleanup` notes a stated census at its own time (`process_test_support.py:307`). The step rule then lands one pass exactly at `TICK`: the step is `max(TICK - TICK - 0, TICK)`.
  - Every one of the 8 early listings has a single event at 0, so the insertion keeps the order. A misordered list would turn the strict equality red; it would not pass silently.
- **The 8 early listings** are exactly the 8 rows of the early table (`TESTING.md:299-308`), and I derived them from each listing's lambda:
  - the trap's command after a first-pass resume, live and not;
  - with no shell, live and not;
  - beside a stopped shell, live and not;
  - beside a shell never resumed, under it and beside it.
- **Byte for byte:** all four `early-*` mutants match my round 9 `natural.py` exactly (`scripts/natcheck.py`, `receipts/natural-byte-mapping.txt`).
- **Red on a named control with their words** (`receipts/repo-mutants.log`):
  - `early-new-sigtermed-0.25`, `early-new-sigtermed-0.5` and `early-trap-command-sigtermed` print "an early first-pass resume's stated seconds were not kept";
  - `early-live-new-sigtermed` prints "an early first-pass resume and its live trap command's ...".
- **Red only on their own listings, out of 46** (`receipts/per-listing.log`):
  - `-0.25` and `-0.5`: on all 8 early listings and no other;
  - `early-trap-command-sigtermed`: on the 2 early first-pass resume listings;
  - `early-live-new-sigtermed`: on the 5 early live listings.
- **Named in rows 2 and 6:** `TESTING.md:314,318`. `receipts/table-check.txt` finds all four in exactly two rows, each row carrying its control.

### 3. A live new descendant beside a shell never resumed (R763-9-F2): MET

- **The listing.** `test_suite_cancellation.py:866-872` is the preferred listing with its stated event list, verbatim from R763-9-F2: `SIGTERM` to the child at 0; `SIGKILL` to the trap command at 2 and to the child at 4; at 14 `SIGKILL` to the shell, the child and the trap command, then the verdict.
- **Where it is named:**
  - rows 3 and 4 (`TESTING.md:315-316`);
  - the liveness table (`:291`).
- **Both F2 mutants:** `parent-of-live-new-unspared-beside-shell` and `verdict-early-live-new-beside-stopped-shell` match round 9 byte for byte. Each is red with "a live new descendant beside a shell never resumed's stated seconds were not kept".
- **The edge mutant:** `parent-under-unresumed-shell-unspared` is red on that listing and its early copy alone, 2 of 46.

### 4. R764-9-S1's three listings: MET

- **The live trap command after the 1 s resume.** `("one-second", 1)` is added to the live loop (`:847`); the command is first listed at 1.5 s (`TESTING.md:293`).
  - At this head the sweep kills the `|one|live|` classes that survived at round 9, for example `r2-sigterm-new|one|live|shell` and `r8-trap-no-window|one|live|shell` (`receipts/sweep-full.log`).
- **The never-resumed listing** is shared with item 3.
- **The non-shell parent with a live child beside a stopped shell:** "a parent beside a stopped shell and its live new descendant" (`:868`, `TESTING.md:292`).
- **Rows 2, 6 and 8 drop "not live" at 1 s** (`TESTING.md:314,318,320`). Row 8 keeps "not live" only for 3 s, 5.5 s and a tick before 14 s, which are not live.

### 5. The listing-time domain: MET, and it changes no row's claim

- **The statement.** `TESTING.md:261-262` states it once. It matches `starved_cleanup`:
  - with no stated time within half a second, the step is the cap, `min(step, 0.5)` (`process_test_support.py:303-306`);
  - otherwise the clock lands a tick short of the next stated time, then on it.
- **No row changes because of it.** Every row text this round changes is accounted for by items 2 to 4: the early listings, "at 1 s" and the never-resumed cells. Nothing is removed from any row except "not live" at 1 s, which widens the row.
- **It is the standard I applied at round 9.** That round's six interior-window classes were classified by this same rule.

### 6. R763-9-R1: MET verbatim

- `test_suite_cancellation.py:831-832` adds `next_to_last=2 - 2 * TICK, lone=[1, 10], live_new_descendant=True`.

### Module moves: no behaviour change

- `BLOCKING` now lives in `process_test_support.py:265-271`. It is byte-identical to round 9's, is no longer defined in `test_suite_cancellation.py`, and is imported there (`:25`) for its one use (`:886`).
- The 143 prior `MUTANTS` entries are unchanged in value and in order. The 7 new entries are listed in item 2 and item 3 (`receipts/module-moves.txt`, `scripts/modcheck.py`).
- `check_py_idiom.py` reports `long module: 10 <= 10`, rc 0: the ratchet the move answers holds. `check_hygiene.py` and `check_baremetal_only.py --check` are rc 0 (`receipts/check_*.log`).
- **Comment rule:** no line added in the delta carries a lane label, review round, reviewer ID or comment ID. `git diff --check 1f29f189 HEAD` is silent.

## The sweep at this head (ruling: re-run the round 9 sweep)

- **Method:** unchanged from round 9 (`scripts/sweep.py`, `probe_cells.py`; `classify10.py` = `classify.py` plus the two cells that round 10 lists). The probe passes 65 of 65 cells on the head product (`receipts/probe-cells-head.log`).
- **Totals:** 4224 mutants. 2716 are equivalent, 1108 are killed and 400 survive (`receipts/sweep-full.log`). At round 9 the counts were 1068 killed and 440 survivors.
  - **41 classes that survived at round 9 are now killed.** All are the live 1 s cell, the never-resumed live cell and `r2-sigterm-new|second`, round 9's early edge.
  - **One class that was killed at round 9 now survives:** `r8-trap-no-window|two-half|any|either`. The unlisted cell is a 2.5 s resume. Only `owner_shell_window` reaches it, a real-process control whose own timing decides which class its resume falls in. At round 9 it happened to kill this class.
- **Classification of the 82 survivor classes** (`receipts/sweep-classified.txt`):
  - **70 classes are red only on cells no listing lists.** These are resumes at 0.5 s, 1.5 s, 2.5 s, 4 s less a tick and 4 s, live commands after 3 s, 5.5 s and 10 s, survivors that are themselves live, and the like.
  - **6 `five-half` classes** reach the 5.5 s cell only through my probe's shape. The probe lists the command from the pass after the resume; the guide lists it "from the resume pass" (`TESTING.md:277`).
  - **6 interior-window classes act only at pass times strictly between a listing's passes:**
    - `r2-grace-early` and `r2-sigterm-new`, at [1.9 s, 2 s - 1.4 µs);
    - `r3-parent-unspared` and `r5-resume-early`, at (2 s, 2.25 s);
    - `r5-resume-early`, at [1.9 s, 2 s - 1.4 µs);
    - `r4-verdict-early`, at [7.5 s, 13.9 s).

    The one listed pass inside a window, 2 - 2 ticks in the next-to-last listings, does not meet that class's liveness condition, since nothing new is listed there yet. All six are outside the domain under item 5.
  - **None acts inside a stated domain, so all 82 are RESIDUE (R763-10-R2).**
- **The limit that led to F1:** my probe has no cell for a first-census parent beside a shell. So no perturbation of that cell can show up as a survivor; it is scored as equivalent. I tested it separately (`scripts/natural10.py`). That is F1.

## Findings

### R763-10-F1 - MINOR - Conformance, Tests, Docs - row 3 claims a first-census parent beside or under a shell never resumed, and no listing has one

- **Locations:**
  - `docs/testing/TESTING.md:315` (row 3, "Pinned by");
  - `scripts/test_suite_cancellation.py:788-873` (`owner_stated_seconds`, `stated_liveness`);
  - product `scripts/owned_process.py:325-328`.
- **Authority:**
  - Row 3's domain at this head: "over a parent whose live child, from the first census or new since it, outlives its own `SIGKILL`, with no cancelled shell, and under or beside one never resumed, killed at 4 s and not a tick before".
  - The child's origin and the shell condition are listed independently, so the domain is their product. Three of the four cells are listed:

    | Child | Shell condition | Listing |
    |---|---|---|
    | first census | no cancelled shell | "a stubborn parent" |
    | new | no cancelled shell | "a live new descendant" |
    | new | under or beside a shell never resumed | `:866-872` |
    | first census | under or beside a shell never resumed | **none** |

  - The round 10 ruling: "Any survivor inside a stated domain, as item 5 defines it, is a finding."
- **Evidence** (`scripts/natural10.py`, `receipts/natural10.log`, `receipts/natural10-under.log`):
  - **The reviewer listing.** It adds two listings to a copy of `owner_stated_seconds`: a first-census parent whose live first-census child outlives its `SIGKILL`, beside and under a cancelled shell. Stated: `SIGTERM` parent and child at 0; `SIGKILL` child at 2 and parent at 4; at 14 `SIGKILL` shell, parent and child, then the verdict. At this head (`none`) it passes, and so do all ten owner controls and the whole test.
  - **The mutant.** `first-census-parent-unspared-beside-shell` stops sparing a parent for a live child from the first census whenever a shell is cancelled. It changes `:327` to:

    ```python
    if any(parent == pid and child in live and not (self.root_notified and (child, _start) in initial) for child, (parent, _start) in owned.items()):
    ```

    It is red on both reviewer listings: the parent gets `SIGKILL` at 3.0 s, not 4 s. It is **green on all ten owner controls and on the whole test** (`suite cancellation: PASS`).
  - **The control mutant.** `parent-unspared-beside-stopped-shell` stops sparing any parent beside an unresumed shell. It is killed by `owner_stated_seconds` on "a live new descendant beside a shell never resumed", so the harness is sensitive there for a new child only.
- **Impact:**
  - A recipe can leave a process tree beside the sweep shell: a parent and a child that outlives `SIGKILL`, for example in state D.
  - The row states that the parent is spared while its child lives, to 4 s, "so its stubborn leaves are killed first". A regression that kills such a parent at 3 s whenever a shell is cancelled is invisible to every committed test, though row 3 claims the cell in so many words.
  - The product is correct today. The gap is in the evidence for a stated behaviour.
- **Required outcome, preferred (pin, as the round 9 and 10 rulings prefer):**
  - A listing of a first-census parent whose live first-census child outlives its own `SIGKILL`, beside a cancelled shell never resumed, with the stated events above. Preferably under one as well.
  - `first-census-parent-unspared-beside-shell`, or an equivalent, joins `MUTANTS`, red on a named control with its words, and is named in row 3.
  - The reviewer listing in `scripts/natural10.py` (`EXTRA`) shows this is feasible as one `kept` call on the existing helpers.
- **Required outcome, otherwise:** qualify row 3 so that the shell conditions apply only to a new child. This narrows the row, which the rulings disfavour, so it needs the manager.
- **Verification:**
  - the new listing is green at the head;
  - the mutant is red on it with its words, and only on it and its early copy if it has one;
  - `--mutants` stays PASS;
  - `python3 -I natural10.py <tree> <scratch> 7` shows the mutant killed.

### RESIDUE (wording only; non-blocking; for the residue checklist)

**R763-10-R1 - RESIDUE - Docs, Tests (docstring) - `docs/testing/TESTING.md:297`; `scripts/test_suite_cancellation.py:778-779`**

- **The wording.** The guide says "Each listing whose census grows after the first pass is kept again, early". The docstring says "one whose census grows after the first pass does so again early".
- **The code.** It keeps a listing early only when its census has grown by `TICK`: `set(listing(TICK)) - set(listing(0))` (`:786`). The listings whose census first grows later are not kept early: the 1 s, 3 s and 5.5 s resumes, the pass-2 and later matrix cells, and next-to-last. Read literally, the sentence covers them too.
- **What is unaffected.** No row, table or mutant changes. The early table (`:299-308`) and rows 2 and 6 name exactly the 8 early listings, and an early census in the others would list nothing new.
- **Exact fix:**
  - `TESTING.md:297`: "Each listing whose census has grown by the second pass is kept again, early: ...";
  - docstring: "one whose census has grown by the second pass does so again early, with a census stated a tick after the first pass."

**R763-10-R2 - RESIDUE - Tests - `receipts/sweep-classified.txt` - the 82 out-of-domain survivor classes (400 mutants)**

- These are residue for #495 under the round 6 and round 10 rulings: 70 unlisted cells, 6 from the probe's shape at 5.5 s, and 6 between listed passes.
- Also listed once: `r8-trap-no-window|two-half|any|either`, which survives at this head and was killed at round 9, only by `owner_shell_window`'s real-process timing. Its cell, a 2.5 s resume, is unlisted.
- No action is required for this PR.

### SUGGESTION

**R764-6-S1 - SUGGESTION - retained, not taken** (outside #833, as before).

## Prior findings at this head

I read the other reviewer's published round 9 findings (PR comment 6592718423) only after the verdict and ledger above were written.

| ID | Severity | Status at fce77f0e | Evidence |
|---|---|---|---|
| R763-9-F1 | MINOR | RESOLVED at its cause | Item 2: 8 early listings; the four `early-*` mutants are byte-exact and red with their words, only on early listings; named in rows 2 and 6 |
| R763-9-F2 | MINOR | RESOLVED for the cell it named (a live *new* child) | Item 3: listing `:866-872`, both mutants red, edge mutant red on its own listing. The first-census child in the same row is F1 |
| R763-9-F3 = R764-9-F1 | MAJOR (mine), MINOR (other reviewer) | RESOLVED | Item 1: `signal.pause()` child; 0 of 3000 at load ≥ 40.6 against the prior head's 5 of 1500; six mutants red. The other reviewer's alternative fix (a one-hour sleep) was not needed; the ruling chose `signal.pause()` |
| R763-9-R1 = R764-9-S2 | RESIDUE / SUGGESTION | RESOLVED verbatim | `test_suite_cancellation.py:831-832` |
| R763-9-S1 | SUGGESTION | TAKEN | `TESTING.md:261-262` (item 5) |
| R764-9-S1 | SUGGESTION | TAKEN, all three listings | Item 4. Its third listing is "parent sparing by a new child", its class `D`, and is implemented as such at `:868`. The first-census child is not in that suggestion's scope and is F1 |
| R763-8-*, R764-8-* | — | Still RESOLVED | The round 8 listings and mutants are unchanged, and `--mutants` is PASS at this head |
| R764-6-S1 | SUGGESTION | Retained, not taken | Outside #833 |

## Lens results

- [R763] MINOR Conformance - `TESTING.md:315` vs `receipts/natural10.log` - R763-10-F1. Everything else in the delta is checked against the round 10 ruling items 1 to 6 and #833 acceptance 1 and 2: `receipts/repo-mutants.log`, `per-listing.log`, `natural-byte-mapping.txt`, `table-check.txt`, `stress-*`.
- [R763] PASS RTL - `scripts/owned_process.py` blob `6495a47b`, byte-identical to round 9 (`receipts/env.txt`); `receipts/probe-cells-head.log` - the 65-cell probe written from rows 2 to 8 passes on the head product. The product is also correct in F1's cell: the reviewer listing is green under `none`. No HDL is in the delta, and the module moves change no `MUTANTS` value or `BLOCKING` byte (`receipts/module-moves.txt`).
- [R763] PASS Robustness - `test_suite_cancellation.py:435-468`; `receipts/stress-owner-report-head.log`, `-prev.log`, `stress-stats.txt` - the load-dependent chance failure (round 9 F3) is gone: 0 of 3000 at load 40.6 to 56.9, against 5 of 1500 on the prior head in the same window. `owner_report` still checks state, wchan, parents, age and the zombie, and its six mutants are red. The product's malformed, ordering and timeout paths are unchanged.
- [R763] MINOR Tests - `test_suite_cancellation.py:788-873`, `receipts/natural10.log` - R763-10-F1. Everything else in the test delta checks out: the 7 new mutants are byte-exact where they were round 9's, each is red with its words and only on its own listings (46 listings), the early mechanism, the never-resumed and 1 s listings, the `owner_report` fix and the module moves.
- [R763] MINOR Docs - `TESTING.md:315` - F1: row 3 claims a cell no listing exercises. Residue R1 and R2 are non-blocking. Items 4 to 6 wording is verified at `TESTING.md:261-262,291-308,314-320` and `test_suite_cancellation.py:831-832`.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | round 10 ruling items 1-6; #833 acceptance; `TESTING.md:253-325`; `test_suite_cancellation.py:435-468,742-873`; `natural10.py`, `sweep.py` | R763-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| RTL | CLEAN | `scripts/owned_process.py:256-339` (blob `6495a47b`, unchanged); `probe_cells.py` 65 of 65; `receipts/module-moves.txt` | R763-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Robustness | CLEAN | `test_suite_cancellation.py:435-468`; stress: head 3000 (0 red) and prior head 1500 (5 red) at load 40.6-56.9; `run_all_suites.sh` preflight unchanged | R763-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Tests | UNCLEAN (F1) | `test_suite_cancellation.py:742-873`; `process_test_support.py:263-308,343-913`; `receipts/repo-mutants.log` (149/146 PASS), `per-listing.log`, `natural-byte-mapping.txt`, `table-check.txt`, `sweep-full.log`, `natural10.log` | R763-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |
| Docs | UNCLEAN (F1; R1, R2 non-blocking) | `TESTING.md:253-325`; docstrings `:743-755,778-779,836-841`; author `PR-BODY.md` and `HANDOFF.md` (round 10) | R763-10 | fce77f0efc1425ef7732a8d70c02addc108f7afe |

## Execution receipts

| What | Result | Receipt |
|---|---|---|
| `owner_report` stress | head 0 of 3000 (8 at once); prior head 5 of 1500; load 40.6-56.9; p = 0.0041 | `receipts/stress-owner-report-head.{log,rc}`, `-prev.{log,rc}`, `stress-stats.txt`, `stress-loadavg-samples.txt`, `stress-load-{start,end}.txt` |
| Repository `--mutants --jobs 8` | PASS, 149 mutants, 146 with a control; rc 0 | `receipts/repo-mutants.{log,rc}` |
| New mutants on every listing | `none` 0 of 46; each new mutant red only on its own listings | `receipts/per-listing.log` |
| Byte mapping, round 9 mutants | 6 of 6 SAME (the seventh was a control mutant, not proposed) | `receipts/natural-byte-mapping.txt` |
| Table check | 146 controlled mutants all named with their controls; `early-*` in rows 2 and 6 | `receipts/table-check.txt` |
| Module moves | `BLOCKING` identical; 143 prior entries unchanged | `receipts/module-moves.txt` |
| Cell probe | PASS, 65 of 65 | `receipts/probe-cells-head.log` |
| Sweep | 4224: 2716 equivalent, 1108 killed, 400 survivors in 82 classes, none in a stated domain | `receipts/sweep-full.{log,rc}`, `sweep-classified.txt` |
| F1 mutants | reviewer listing green at the head; `first-census-parent-unspared-beside-shell` survives all ten controls and the whole test | `receipts/natural10.{log,rc}`, `natural10-under.log` |
| Whole test at the head | `suite cancellation: PASS` (the `none` tree in `natural10.log`) | `receipts/natural10.log` |
| Static checks | `check_py_idiom` rc 0 (long module 10 <= 10), `check_hygiene` rc 0, `check_baremetal_only --check` rc 0 | `receipts/check_*.log` |
| Hosted snapshot | 18 success, 27 queued or in progress, 1 skipped (physical gPTP) | `receipts/hosted-checks-snapshot.txt` |
| Restore | HEAD, tree, index equal to `ls-tree`, clean with `--ignored`, six gitlinks unchanged | `receipts/restore-check.txt` |

## Real limits

- I ran no whole-suite bank, gPTP, PP, Yosys or builder bank, no Docker or act, and no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank runs at this head. I claim none. Source-head gate evidence is the author's published receipts (`author-r10`), which I spot-checked: the stress logs, and the lane-gate table in `HANDOFF.md`.
- I raised the stress load with a thread load generator, because the host's own load was about 8. The prior head's 5 reds under the same load show the condition is real, but it is not load 105.
- My sweep is my own perturbation x condition grid on my own probe. As F1 shows, a cell missing from the probe hides its perturbations as equivalent. There may be other such cells. I checked only row 3's child-origin x shell product by hand.
- Hosted checks were mostly queued or in progress when I looked. The manager owns hosted and act acceptance.

## Pending manager duties

- Rule on R763-10-F1, pin or narrow. Carry R763-10-R1 and R2 to the residue checklist.
- Validate the current-dev merge candidate (source base `1f29f189279f9fc0132f4918e47342b87d22f33a`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`) with builder and native banks at the merge turn, and link the receipts.
- Hosted and act acceptance at the final head.

R763-10 FINISHED

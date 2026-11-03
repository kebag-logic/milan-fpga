[R763] NEGATIVE - exact head e803d94b3a11921a293cf036a8eda333d23828f9

# R763-9: internal cleared-context review of PR #834 (issue #833)

Head `e803d94b3a11921a293cf036a8eda333d23828f9`, tree `e10d752b67f6b8a1b726c60f1889e61ff60bbb1b` (`receipts/env.txt`). Round 9 delta `5b6d38a3..e803d94b`: `docs/testing/TESTING.md`, `scripts/process_test_support.py` and `scripts/test_suite_cancellation.py`. `scripts/owned_process.py` is byte-identical to round 8.

## Summary

- **The product is correct in every cell I probed.** My explicit-schedule cell probe covers 16 resume times, never, and no shell, each with no new descendant, one that is not live and one that is live. That is 65 cells, written from the table's rows, and `owned_process.py` passes all 65 (`probe_cells.py`).
- **Ruling items 1 to 4 are met as written:**
  - each liveness listing is present;
  - all 13 round 8 reviewer mutants match their published edits byte for byte and are red with their words;
  - every mutant is named in its row;
  - each of the ten edge mutants is red on its own cell alone, 1 of 35 listings;
  - the three residue fixes are verbatim.
- **The author's reading of "late in grace" is consistent with the product.**
- **My one sweep: 4224 mutants, 440 survivors** (`receipts/sweep-full.log`). The mutants cover 22 perturbations of rows 2 to 8, over 15 time classes, 4 liveness conditions and 3 shell conditions. The survivors group into 101 classes (`receipts/sweep-classified.txt`):
  - 88 hit only cells no listing claims;
  - 6 hit listed cells only through cells whose listing differs from the guide's (the trap's command listed from the pass after the resume instead of from the resume pass);
  - 6 hit listed cells only at pass times strictly inside a class, between the passes the harness samples;
  - 1 hits a claimed edge, F1.
- **Three findings make the verdict NEGATIVE:**
  - **R763-9-F1 (MINOR):** no listing lists a descendant new since the first census before 0.5 s into cleanup. A natural mutant that sends `SIGTERM` to any descendant first seen in the first half second survives every owner control and the whole test.
  - **R763-9-F2 (MINOR):** rows 3 and 4 claim a live new descendant beside a cancelled shell that is never resumed, and no listing has one. Two mutants survive every control and the whole test.
  - **R763-9-F3 (MAJOR), item 5 ruled:** the `owner_report` red rate is a defect in a file this PR adds. It is the control's own race. I measured 28 red of 3000 at load 43 to 50; with a one-line fix it is 0 of 3000 under the same interleaved load (Fisher one-sided p = 3.5e-9). That puts a chance failure in the preflight of every suite run, which acceptance 2 of #833 rules out.

## Scope reconstructed

- **Issue #833 acceptance:**
  1. the failure message prints each descendant's `/proc/<pid>/stat` state;
  2. a fixed deadline or a real fix, "with no suite left to fail by chance". A sweep failure is not accepted as a flake by default.
- **Round 9 ruling (issuecomment-6590477473):**
  1. a liveness axis for new descendants: beside a stopped shell before any resume, with no cancelled shell, and as the trap's command after an in-grace resume, early (pass 1 and pass 2) and late (the last in-grace pass);
  2. every round 8 reviewer mutant red on a named control with its words, and named in its row;
  3. domain notes name the liveness cells, with one edge mutant per new cell, all red;
  4. the residue exact fixes;
  5. one sweep by each reviewer over every cell (resume class x liveness x shell), reporting every survivor. The bar is unchanged.
- **Standing rulings:**
  - round 6 item 4: a mutant against unstated behaviour is residue for #495;
  - round 8: edges of each class;
  - R764-8-S1, taken: "A cell's domain is its listed resume, not the whole of its class" (`TESTING.md:262`).

## Focus checks

### 1. Liveness listings (ruling item 1): MET as listed; see F1 for the early edge

- **Beside a stopped shell before any resume (R763-8-F1).** `test_suite_cancellation.py:845-848`: the child exits after pass 1, and a real `cat` stands for a live new descendant under the shell from pass 2 to 3 s. The product holds the resume until it is gone (`owned_process.py:303-304`). `resume-beside-new-live` and the edge mutant `resume-beside-live-new-past-grace` are each red on this listing alone (`receipts/per-listing.log`).
- **With no cancelled shell (R764-8-F1).** `:850-853`: the survivor is spared to 4 s while its live child lives (`owned_process.py:329`). `live-new-sigtermed-with-no-shell` is red on it alone.
- **As the trap's command after an in-grace resume (R763-8-F2, R764-8-F1).** The live column covers all six matrix classes (`:838-839`), plus both next-to-last cells (`:857-860`). Each edge mutant is red on exactly its own cell (`receipts/per-listing.log`).
- **The author's reading of "late in grace" holds against the product:**
  - a trap's command cannot exist before the resume, since the shell is stopped;
  - `SIGCONT` is sent after the census of the resume pass (`owned_process.py:303-311`), so the command is first listed one pass later;
  - so the latest in-grace listing is the last pass before 2 s, after a resume one pass earlier;
  - a live command listed earlier would hold the resume (`:304`);
  - the zombie is not live, so it does not hold the resume, and its `SIGKILL` at 2 s is a stated event. That event makes the harness land a pass at 2 s less a tick (`process_test_support.py:291-293`). This is legitimate product behaviour, and the guide states it (`TESTING.md:288`).
- **The early side is pinned for the resume, not for the command's listing.** In every listing the command, and every other new descendant, is first listed at clock 0.5 s or later (`receipts/new-in-grace-audit.txt`: 11 listings, earliest 0.5). The cause is the harness: with no stated event due within half a second, it steps half a second (`process_test_support.py:292-293`). This is F1.

### 2. The 13 round 8 reviewer mutants (ruling item 2): MET

- **Byte for byte:** all 13 match `MUTANTS` (`receipts/r8-byte-mapping.txt`, `bytecheck.py`, `bytecheck_exec.py`). The published scripts are hash-checked against their reviewers' public manifests:
  - `r8_mutants.py` is `30fe7772…`, matching R763-8's `MANIFEST.sha256`;
  - `r764_8_probes.py` is `07802fca…` and `r764_8_live_probes.py` is `32c47359…`, matching R764-8's.
- **Red with their words:** my run of the repository's `--mutants --jobs 6` passes: `owned-process mutants: PASS (142 mutants, 139 with a control that must fail)`, rc 0 (`receipts/repo-mutants.log`).
- **Named in their rows:** every one of the 139 controlled mutants is named in a row whose control column carries its control. The 3 with no control are in no row, and only `windows-2s` is in two rows, as accepted at R763-6 (`receipts/table-check.txt`, `table_check.py`).
- **Per listing:** both interior mutants are each red on their new lone resume alone (`receipts/per-listing.log`).

### 3. Domain notes and edge mutants (ruling item 3): MET for the cells named; F1 and F2 for two claims

- Rows 2 to 8 (`TESTING.md:295-301`) and the liveness table (`:284-290`) name the liveness cells.
- The ten edge mutants are each red on 1 of 35 listings, their own:
  - `first-pass-`, `second-pass-` and `next-to-last-in-grace-live-trap-command-sigtermed`;
  - `next-to-last-in-grace-trap-command-sigtermed`;
  - `last-in-grace-`, `first-past-grace-`, `second-past-grace-` and `last-pass-live-trap-command-unspared`;
  - `resume-beside-live-new-past-grace`;
  - `live-new-sigtermed-with-no-shell`.
- `TESTING.md:258` still says the domains "Together ... cover all that the row states". F1 and F2 falsify that.

### 4. Residues: all applied verbatim

- R763-8-R1 is at `TESTING.md:263`.
- R763-8-R2 (= R764-8-R1) is at `test_suite_cancellation.py:752-754`.
- R763-8-R3 is at `:814-815`.
- R764-8-S1 is at `TESTING.md:262`.
- The comment rule holds: no line the delta adds carries a lane label, review round, reviewer ID or comment ID. `git diff --check 1f29f189 HEAD` is silent.

### 5. The `owner_report` rate (item 5): a defect in this PR. F3

See F3.

## The sweep (ruling item 5)

- **Method** (`sweep.py`, `probe_cells.py`, `classify.py`):
  - **Perturbations:** each of 22 perturbations breaks one stated behaviour of rows 2 to 8:
    - `SIGTERM` to a new descendant, or to the resumed shell;
    - no `SIGTERM` to a first-census one;
    - grace ended early;
    - a parent of a live child unspared;
    - kill-all late;
    - the verdict a pass late or early;
    - the resume held, or taken while another lives;
    - the window short, long or cut later;
    - the shell or the trap's command killed inside the window, or the command given no window.
  - **Conditions:** each perturbation is applied only under one cell condition. That condition is the product of three parts:
    - a time class of the resume or of the event: 15 classes, each matrix edge, the interior points and the gaps between them;
    - the liveness of a listed descendant new since the first census: none, not live, live or any;
    - with a cancelled shell, without one, or either.
  - **Verdict per mutant:** the mutant first runs on my probe, which shows whether it changes a stated behaviour in any cell. If it does, it then runs on every owner control. **A survivor is red on the probe and green on all ten controls.**
  - **Totals:** 4224 mutants. 2716 are equivalent (no cell changes), 1068 are killed and 440 survive.
- **Classification of the 101 survivor classes** (`receipts/sweep-classified.txt`):
  - **88 classes are red only on cells no listing claims.** They are outside the listed domain, residue for #495 under the round 6 ruling. The cells are:
    - resumes at 0.5 s, 1.5 s, 2.5 s, 4 s less a tick and 4 s;
    - a live command after resumes at 1 s, 3 s, 5.5 s and 10 s, which the rows exclude in so many words ("not live, after resumes at 1 s, 3 s, 5.5 s");
    - lone resumes at 5.5 s and next-to-last;
    - a live new descendant holding the shell to a time other than 3 s, which row 5 limits to "at 3 s";
    - a survivor that is itself live.

    The one exception is the never-resumed shell with a live new descendant, which F2 shows is claimed.
  - **6 classes (the `five-half` ones) touch the listed 5.5 s cell only through my probe's shape.** My probe lists the trap's command from the pass after the resume; the guide says that listing has it "from the resume pass" (`TESTING.md:278`). They are outside the domain.
  - **6 classes hit listed cells only at pass times strictly inside a class, between two passes the harness samples.** Each is a window narrower than the half-second step that excludes the sampled tick-before pass:
    - `r2-grace-early` and `r2-sigterm-new` at [1.9 s, 2 s - 1.4 µs);
    - `r3-parent-unspared` and `r5-resume-early` at (2 s, 2.25 s);
    - `r5-resume-early` at [1.9 s, 2 s - 1.4 µs);
    - `r4-verdict-early` at [7.5 s, 13.9 s).

    The rows' domains for these name the tick before ("at 2 s and not a tick before", "killed at 4 s and not a tick before", "its verdict at 14 s and not a tick before"), or name a class sampled at both its ends. I record them as outside the listed domain, the same standard the round 8 and 9 rulings apply to classes of resume. See S1.
  - **1 class hits a claimed edge: `r2-sigterm-new|second`** (`SIGTERM` to a new descendant listed at 5e-7 s ≤ clock < 0.25 s). Its natural forms survive the whole test too: F1.
  - **F2's cell** is the one claimed cell among the 88: a never-resumed shell beside a live new descendant (`r3-parent-unspared|*|live|shell`, `r3-kill-all-late|four|live|shell`, `r4-verdict-early|last-pass|live|shell`).
- **Natural forms** (`natural.py`, `receipts/natural.log`): each was run on the probe, all ten owner controls and the whole test.

  | Mutant | Probe | Owner controls | Whole test |
  |---|---|---|---|
  | `early-new-sigtermed-0.25` | red | green | green |
  | `early-new-sigtermed-0.5` | red | green | green |
  | `early-trap-command-sigtermed` | red | green | green |
  | `early-live-new-sigtermed` | red | green | green |
  | `parent-of-live-new-unspared-beside-shell` | red | green | green |
  | `verdict-early-live-new-beside-stopped-shell` | red | green | green |
  | `trap-command-next-pass-sigtermed` (the same idea keyed on the pass, not the clock) | red | red | red |

  The last row is the control against the others: keyed on the pass, the same idea is caught.

## Findings

### R763-9-F1 - MINOR - Conformance, Tests, Docs - no listing lists a new descendant before 0.5 s into cleanup

- **Locations:**
  - `docs/testing/TESTING.md:295` (row 2) and `:299` (row 6);
  - `TESTING.md:258,260`;
  - `scripts/test_suite_cancellation.py:785-860`;
  - `scripts/process_test_support.py:289-295`;
  - `scripts/owned_process.py:319-323`.
- **Authority:**
  - Row 2: "A descendant new since that census gets none". Its domain: "over descendants new since then and listed inside grace, live or not: before any resume, with no shell and beside a stopped one, and after a resume in the matrix's first-pass and pass-2 cells".
  - Row 6: the trap's command "gets no `SIGTERM` either, even when the resume comes inside grace".
  - Ruling item 1: the trap's command "early in grace, in pass 1 and pass 2". The author reads "late" as an edge (first listed in the last in-grace pass), so the matching early edge is the command first listed in the pass right after a pass-1 or pass-2 resume.
  - Round 8's method asks for each class at its earliest pass.
- **Evidence:**
  - **The audit.** Of 11 listings with a new descendant inside grace, the earliest pass that lists one is at clock 0.5 s (`receipts/new-in-grace-audit.txt`, `audit_new_in_grace.py`). With no stated event due within half a second, the starved harness steps half a second (`process_test_support.py:292-293`). So no listing ever lists a new descendant between the first pass and 0.5 s.
  - **The survivor.** `early-new-sigtermed-0.5` changes `owned_process.py:322` to `if (pid, start) not in initial and clock >= 0.5:`. It sends `SIGTERM` to every descendant new since the first census that is listed in the first half second. It is green on all ten owner controls and on the whole test (`receipts/natural.log`).
  - **Where it is red.** It is red on my probe in these claimed cells:
    - the first-pass and pass-2 resumes with a trap command, live and not;
    - the live new descendant beside a stopped shell;
    - with no shell, a new descendant, live and not.
  - **The variants.** The `0.25` form, the trap-command-only form and the live-only form survive the same way.
- **Impact:**
  - Real census passes take about 10 to 20 ms (the READY post's 29-40 ms whole control; the guide's own statement that a pass is short). So a terminal trap's cleanup command, started right after a first-pass resume, is typically first listed at tens of milliseconds. That is inside the unsampled half second.
  - That is the most common real case of row 6: a shell alone at the first pass.
  - A regression that sends `SIGTERM` to it would kill the cleanup row 2 exists to protect ("so a terminal trap's cleanup command can run"), and nothing committed would notice.
- **Required outcome** (pin, not narrow, per the round 9 ruling):
  - A listing in which a new descendant is first listed at a pass early in grace. The earliest pass after the first, a tick in, is the edge. It should cover at least the trap's command after a first-pass resume, live and not, and preferably also the new descendant with no shell and beside a stopped shell.
  - `early-new-sigtermed-0.5`, or an equivalent, joins `MUTANTS` as that cell's edge mutant, red on a named control with its words, and is named in rows 2 and 6.
  - The domain notes name the early listing.
  - **Feasibility, not prescribed:** in the current harness a pass lands early only a tick before a stated time. An optional extra pass time for `starved_cleanup`, or a stated event a couple of ticks after the first pass, would place one. `probe_cells.py` shows that an explicit schedule turns all four natural forms red.
- **Verification:**
  - `python3 -I natural.py <clone> <scratch> 10`: the four `early-*` mutants are red on a named control.
  - `--mutants` stays PASS, with `none` green.
  - `audit_new_in_grace.py` shows a new descendant listed below 0.5 s.

### R763-9-F2 - MINOR - Conformance, Tests, Docs - no listing has a live new descendant beside a shell that is never resumed

- **Locations:**
  - `docs/testing/TESTING.md:296` (row 3) and `:297` (row 4);
  - the liveness table `:284-290`;
  - `scripts/test_suite_cancellation.py:830-860`;
  - `owned_process.py:289,329`.
- **Authority:**
  - Row 3's domain: "a parent whose live child, from the first census or new since it, outlives its own `SIGKILL`, killed at 4 s and not a tick before". It does not qualify the cancelled shell.
  - Row 4's domain: "beside a new descendant, live or not, and beside a shell never resumed, with or without a new descendant". The second clause does not qualify liveness, though the same row qualifies the first. Elsewhere this round writes "not live" wherever only an entry that is not live is listed (rows 2, 6, 8).
  - The ruling's sweep axes: liveness x with or without the shell.
- **Evidence:**
  - Every listing with a live new descendant has either no cancelled shell (`:850`) or a shell resumed at 3 s (`:845`).
  - The never-resumed shell's new descendant (`:809-812`) is a PID above the PID range, so the product sees it as not live.
  - `parent-of-live-new-unspared-beside-shell` does not spare a parent of a live new descendant when a shell is cancelled. `verdict-early-live-new-beside-stopped-shell` brings the verdict a pass early beside a stopped shell with a live new descendant. Both are green on all ten owner controls and the whole test (`receipts/natural.log`).
  - The sweep's `r3-parent-unspared|{all,first-past,two-half,three,four}|live|shell`, `r3-kill-all-late|four|live|shell` and `r4-verdict-early|last-pass|live|shell` survive the same way. Their only red cell is `shell never new=live`.
- **Impact:**
  - On a cancel, a recipe's terminal trap may start a cleanup process that hangs, for example in state D. Its parent then sits beside the stopped sweep shell.
  - The product spares the parent until 4 s and fails the run at 14 s, as stated.
  - A regression of either behaviour in that cell is invisible, though rows 3 and 4 read as claiming it.
- **Required outcome, preferred:**
  - One listing: a cancelled shell never resumed, its first-census child outliving its `SIGKILL`, and from pass 2 that child's trap starting a live new descendant that outlives 14 s.
  - Stated: `SIGTERM` child at 0; `SIGKILL` trap command at 2; `SIGKILL` child at 4; at 14, `SIGKILL` shell, child and trap command, then the verdict.
  - It is named in rows 3 and 4 and in the liveness table, with an edge mutant.
  - **Feasibility, not prescribed** (`f2_feasibility.py`, `receipts/f2-feasibility.log`): this listing, added to a copy of `stated_liveness`, is green at the head and red under both F2 mutants. Without it, both are green.
- **Required outcome, otherwise:** qualify row 3 ("with no cancelled shell") and row 4 ("with or without a new descendant that is not live"). That narrows the rows, which the round 9 ruling disfavours, so it needs the manager.
- **Verification:** both F2 mutants are red on a named control with their words, and `--mutants` stays PASS.

### R763-9-F3 - MAJOR - Conformance, Robustness, Tests - `owner_report` fails by chance under load: the preflight of every suite run

- **Locations:**
  - `scripts/test_suite_cancellation.py:441` (the child is `STUBBORN`, which wakes every 20 ms) and `:446-450` (waits for state `S`, then describes it and asserts `"state S"`);
  - `scripts/run_all_suites.sh:288` (the preflight runs this test).
- **Authority:**
  - #833 acceptance 2: "with no suite left to fail by chance".
  - The issue body: "A sweep failure here is not accepted as a flake by default."
  - The control is added by this PR (`58c8a367d7`, `151adbea64`, `a25ee52d1b` in `1f29f189..HEAD`), in a file this PR changes.
- **Evidence:**
  - **The race.** Between the `eventually` that sees state `S` (`:446`) and the `_describe` read (`:448`), the child's 20 ms timer can fire. It is then runnable, state `R` with wchan `hrtimer_nanosleep`, and under load it stays runnable while it waits for a CPU.
  - **My measurement, interleaved under the same load** (`stress_owner_report.py`; `receipts/stress-owner-report-head.log`, `-fix.log`, `stress-loadavg-samples.txt`, `stress-stats.txt`):

    | Tree | Runs | Red | Load |
    |---|---|---|---|
    | Head | 3000 (8 at once) | 28 (0.93%) | 43 to 50 |
    | Head with the fix below | 3000 (8 at once) | 0 | the same |

    Every red is `AssertionError: ('state S', '... state R wchan hrtimer_nanosleep ...')`. The difference has one-sided Fisher p = 3.5e-9.
  - The author's own receipts show the same failure, 4 of 1152 at load about 42 (`author-r9/receipts/final/stress-owner_report*.log`).
  - At 0.93% per run, a 20-shard replay has about a 17% chance that at least one preflight goes red.
- **Impact:**
  - The PR closing a load-dependent chance failure adds another to the preflight of every suite run, at about 1% per run at load 45. It will be higher at the loads #833 records (105 to 112).
  - The report it checks is right. The defect is the control's own timing.
- **Required outcome (exact fix):** the child described in `owner_report` must stay asleep from the handshake to its `SIGKILL`, with no timer of its own. For example, replace `:441` with:

  ```python
  sleeper = subprocess.Popen([sys.executable, "-c", "import os, signal, sys; from pathlib import Path; "
                              "Path(sys.argv[1]).write_text(str(os.getpid())); signal.pause()", str(ready)])
  ```

  This is `receipts/owner-report-fix.diff`. It passes every assertion of the control: state `S`, a non-empty wchan, the parent, the age and the zombie. Other controls that need a child ignoring `SIGTERM` keep `STUBBORN`.
- **Verification:** `python3 -I stress_owner_report.py <tree> 3000 8` at load 40 or more gives 0 red, and so does the author's own stress driver.

### RESIDUE (wording only; non-blocking; for the residue checklist)

**R763-9-R1 - RESIDUE - Tests (printed summary) - `scripts/test_suite_cancellation.py:824-827`**

- The control's printed summary lists `resumes=[0, 1, 3, 5.5, last]` and `matrix=[...]`. It leaves out the next-to-last in-grace resume, the lone resumes at 1 s and 10 s, and the liveness axis this round adds. It changes no assertion.
- **Exact fix:** add `next_to_last=2 - 2 * TICK, lone=[1, 10], live_new_descendant=True` to that dict.

### SUGGESTION

**R763-9-S1 - SUGGESTION - Docs - `docs/testing/TESTING.md:260-262`**

- Six sweep survivor classes act only at pass times strictly inside a class, in windows narrower than the harness's half-second step that exclude its tick-before pass. I classified them outside the listed domain, by the same standard as "A cell's domain is its listed resume".
- The guide could say so once for listing times: "Between stated times the starved owner's passes are half a second apart; a listing's domain is its listed passes." Then no reader takes "listed inside grace" or "not a tick before" as a claim about every pass time in between.
- This does not replace F1, which is an unlisted edge.

**R764-6-S1 - SUGGESTION - retained, not taken** (outside #833, as before).

## Prior findings at this head

| ID | Severity | Status at e803d94b | Evidence |
|---|---|---|---|
| R763-8-F1 | MINOR | RESOLVED at its cause: a live new descendant holds the stopped shell | `:845-848`; `resume-beside-new-live`, `resume-beside-live-new-past-grace` red on it alone (`receipts/per-listing.log`) |
| R763-8-F2 | MINOR | RESOLVED: the command is first listed at the last in-grace pass after a resume a pass earlier, live and not | `:854-860`; `sigterm-trap-command-after-resume-from-1.5s` red on both next-to-last cells. Its early counterpart is F1 |
| R764-8-F1 | MINOR | RESOLVED for every cell named: live new descendants with no shell, beside a stopped shell, and in all six matrix classes plus next-to-last | `sigterm-to-live-new` red on 5 listings, `live-trap-command-unspared-after-in-grace-resume` on 4. The cases not named are F1 and F2 |
| R763-8-R1, R2, R3; R764-8-R1 | RESIDUE | RESOLVED, exact fixes verbatim | `TESTING.md:263`; `test_suite_cancellation.py:752-754,814-815` |
| R764-8-S1 | SUGGESTION | TAKEN | `TESTING.md:262` |
| R764-6-S1 | SUGGESTION | Retained, not taken | PR body |

## Lens results

- [R763] MINOR Conformance - `TESTING.md:295,299`; `receipts/natural.log` - R763-9-F1.
- [R763] MINOR Conformance - `TESTING.md:296-297`; `receipts/f2-feasibility.log` - R763-9-F2.
- [R763] MAJOR Conformance - #833 acceptance 2 vs `test_suite_cancellation.py:441-450` - R763-9-F3.
- [R763] PASS RTL - `scripts/owned_process.py:256-339` (byte-identical to round 8), `probe_cells.py` - I read the cleanup loop against rows 2 to 8 and wrote a 65-cell expectation from the rows. The product passes every cell: grace `>=` at `:313`, the resume at `:304`, the window at `:312,317,332`, parent sparing at `:327-329`, the verdict at `:289-290`. There is no HDL in the delta.
- [R763] MAJOR Robustness - `test_suite_cancellation.py:441-450`, `receipts/stress-owner-report-head.log` - R763-9-F3: a load-dependent chance failure. The product's own handling of malformed, ordering and timeout paths is unchanged, and is correct in every probe cell.
- [R763] MINOR Tests - F1, F2; MAJOR Tests - F3. Everything else in the test delta checks out: the liveness listings, 23 new mutants red with words, ten edge mutants each alone, byte mapping, and the table check.
- [R763] MINOR Docs - `TESTING.md:258,295-299` - F1 and F2: row domains and line 258 claim cases no listing exercises. Residue R1 and suggestion S1 are non-blocking.

## Reviewer-owned completion ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1, F2, F3) | #833 acceptance; round 6, 8 and 9 rulings; `TESTING.md:253-315`; `test_suite_cancellation.py:436-470,741-860`; `natural.py`, `sweep.py` | R763-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| RTL | CLEAN | `scripts/owned_process.py:30-45,100-131,256-339`; `probe_cells.py` (65 cells, PASS) | R763-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Robustness | UNCLEAN (F3) | `test_suite_cancellation.py:441-450`; `run_all_suites.sh:288`; stress 3000 + 3000 at load 43-50 | R763-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Tests | UNCLEAN (F1, F2, F3) | `test_suite_cancellation.py:741-860`; `process_test_support.py:263-323,760-886`; `receipts/repo-mutants.log`, `per-listing.log`, `table-check.txt`, `r8-byte-mapping.txt`, `sweep-full.log`, `natural.log` | R763-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |
| Docs | UNCLEAN (F1, F2; R1 and S1 non-blocking) | `TESTING.md:253-315`; PR body Round 9; docstring `:742-755`, `:831-836` | R763-9 | e803d94b3a11921a293cf036a8eda333d23828f9 |

## Execution receipts

| What | Result | Receipt |
|---|---|---|
| Cell probe on the product | PASS, 65 of 65 | `probe_cells.py` (rerun by `sweep.py` per mutant) |
| One sweep over every cell | 4224 mutants: 2716 equivalent, 1068 killed, 440 survivors in 101 classes | `receipts/sweep-full.log`, `receipts/sweep-classified.txt` |
| Natural forms | 6 survivors on all controls and the whole test; 1 control mutant red | `receipts/natural.log` |
| Repository `--mutants --jobs 6` | PASS, 142 mutants / 139 controlled, rc 0 | `receipts/repo-mutants.log`, `.rc` |
| Every round 9 mutant on every listing | `none` 0 of 35; each edge mutant 1 of 35, its own | `receipts/per-listing.log` |
| Round 8 byte mapping | 13 of 13 SAME, sources hash-checked against reviewer manifests | `receipts/r8-byte-mapping.txt` |
| Table check | all controlled mutants named, with their controls | `receipts/table-check.txt` |
| New-descendant audit | earliest in-grace listing at 0.5 s | `receipts/new-in-grace-audit.txt` |
| F2 feasibility | green at head; red under both F2 mutants | `receipts/f2-feasibility.log` |
| `owner_report` stress | head 28 of 3000; fix 0 of 3000; p = 3.5e-9 | `receipts/stress-*.{log,txt}`, `receipts/owner-report-fix.diff` |
| Restore | HEAD, tree, index (`ls-files -s` = `ls-tree` hash), six gitlinks unchanged; reviewer-made ignored `scripts/__pycache__` removed | `receipts/restore-check.txt` |

## Real limits

- I ran no whole-suite bank, gPTP, PP, Yosys or builder bank, no Docker or act, and no hardware. Physical calibration was NOT RUN, and field skips are not hardware proof.
- No manager source bank runs at this head. I claim none, and source-head gate evidence is the author's.
- The whole test ran only from mutant trees in `natural.py`, 7 runs. The six survivors were each rc 0 with `suite cancellation: PASS`. The pass-keyed control mutant was rc 1, red at "a first-pass resume". I did not run the whole test separately from the clean head.
- My sweep's mutants are my own perturbation x condition grid. Survivors outside it may exist. Classifying the six interior-window classes as outside the domain is my reading of the standing domain rule (S1), recorded for the manager to rule on.
- Load during the stress was set by the host's other work plus my 16 jobs, 43 to 50. I did not reproduce load 105.
- Hosted checks at this head were partly in progress when I looked: some completed successfully, many were still running, and the physical gPTP job was skipped. The manager owns hosted and act acceptance.

## Pending manager duties

- Rule on F1, F2 and F3, and carry R763-9-R1 to the residue checklist.
- Rule on S1, the interior-window classification.
- Validate the current-dev merge candidate (source base `1f29f189279f9fc0132f4918e47342b87d22f33a`, live dev `e61a4afaa54a598ceec08b7b5879285256cc60b6`) with builder and native banks at the merge turn, and link the receipts.
- Hosted and act acceptance at the final head.

R763-9 FINISHED

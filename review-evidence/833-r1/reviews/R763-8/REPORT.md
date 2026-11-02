[R763] NEGATIVE - exact head 5b6d38a3542119ad77d352ea992e3cc41d121620

Round R763-8, internal independent review of PR #834 (issue #833), tree `bc7cb27fe2b8df97fb30a47a48c304ff34faf85f`. Delta reviewed: `887fdd53..5b6d38a3` (five one-line commits; tests and docs only). `scripts/owned_process.py` is byte-identical to round 7 (`git diff --quiet 887fdd53 HEAD -- scripts/owned_process.py`).

## Summary

- **The round 8 ruling's four items are met as specified, and all prior findings are resolved.**
  - **Item 1, the matrix:** every cell of the resume-timing matrix exists. An audit of each listing's passes puts each resume in the class it claims.
  - **Item 2, round 7 mutants:** all nine round 7 reviewer mutants are in `MUTANTS` byte for byte, as eight edits, each red with its words.
  - **Item 3, domain notes:** the notes name the cells they cover.
  - **Item 4, edge mutants:** each of the twelve is red on its own cell's listing and on no other.
  - **Preflight cost:** about 10 ms.
- **Two open MINOR findings make this round NEGATIVE.** Two new reviewer mutants survive every owner control, each against a row the testing guide says is fully covered. Line 258 says: "Together they cover all that the row states."
  - **R763-8-F1:** row 5, "stays stopped while any other descendant lives". No listing has a live descendant that is new since the first census.
  - **R763-8-F2:** rows 2 and 6. No listing has a trap command listed inside grace after a resume later than 1 s.
  - Both can be pinned. A one-line feasibility listing for each is green at the head and red under its mutant alone.
- **The product is correct in every probe.** Both findings are coverage gaps, of the same class the ruling set out to close.
- **Also recorded:** three wording RESIDUE items and one retained SUGGESTION.

## Scope reconstructed

- **Issue #833 acceptance:**
  1. the failure message prints each descendant's `/proc/<pid>/stat` state;
  2. a fixed deadline or a real fix, from that evidence, with no suite left to fail by chance.
- **Manager's round 8 ruling (issuecomment-6588568293):**
  1. a resume-timing matrix {first pass in grace, later pass in grace, first pass past grace, later pass past grace} x {nothing else live, a trap command started after the resume}, plus the R763-7-F2 listing (a new descendant while the shell is stopped). Each cell asserts the row 2, 3, 5, 6, 7 and 8 behaviour that applies to it.
  2. every round 7 reviewer mutant is red on a named control with its words, and is in `MUTANTS`.
  3. each domain note names the cells it covers, and no row claims a cell no listing exercises.
  4. one edge mutant per cell, all red.
- **The bar is unchanged:** a survivor against a listed row within its stated domain is a finding.
- **Authority read:** AGENTS.md, CONTRIBUTING.md (by reference), issue body and comments, the author's TAKEN and REVIEW READY comments, the PR body's Round 8 section, the delta, and published author receipts (`review-evidence/833-r1/author-r8` at `7aba003d`).
- **Prior findings** (R763-7 and R764-7 published reports) were read only after my own pass over the diff.

## Focus checks

### 1. The matrix (ruling item 1): MET

- **Listings.** `scripts/test_suite_cancellation.py:820-825` adds eleven listings. With round 7's "a first-pass resume" (`:798`) as the twelfth, every cell is covered. The R763-7-F2 listing is at `:814-817`, and R764-7's 1 s listing at `:812`.
- **Pass audit.** `receipts/classify_none.txt` was made by `probe_all_listings.py --classify`, which records every census clock. Each resume falls where the guide says:

  | Cell | Resume clock | Pass | Past-grace ordinal | Trap command first listed |
  |---|---|---|---|---|
  | First pass | 0 | 1 | 0 | 0.5, inside grace |
  | Pass 2 | a tick | 2 | 0 | 0.5 + a tick, inside grace |
  | Last pass before 2 s | 2 - a tick | 6 | 0 | 2.5 - a tick, past grace (the next pass is 2.5 - a tick) |
  | First at or past 2 s | 2 | 6 | 1 | past grace |
  | Next pass after that | 2 + a tick | 7 | 2 | past grace |
  | Last pass before 14 s | 14 - a tick | 31 | 26 | 14.5 - a tick |

- **Each cell asserts its rows.** Each listing compares its whole event list to a tick (`assert events == stated`). Where they apply, that covers:
  - the child's `SIGTERM` at 0 and `SIGKILL` at 2;
  - the exact resume pass;
  - no `SIGTERM` to an in-grace trap command;
  - the shell and command spared past 4 s, and `SIGKILL` 10 s after the resume;
  - the verdict 20 s after the resume.
- **All 23 listings are green at the head** (`receipts/classify_none.txt`).
- **"First pass past grace" read as the first pass at or past 2 s: CORRECT against the product.**
  - `owned_process.py:260-285` sets `clock` to 0 at start. The first pass adds `min(now - last, MAX_PASS_SECONDS)`, with `MAX_PASS_SECONDS = 0.5` (`:45`). So the first pass's clock is at most 0.5 s, below `GRACE_SECONDS = 2.0`.
  - `:313` switches to `SIGKILL` at `clock >= deadline`. So the first past-grace pass is the first pass with clock >= 2 s, and the matrix puts it at exactly 2 s.
  - The latest resume is 14 - a tick. At 14 s, `:290` raises the verdict before `:304` can resume.

### 2. Round 7 reviewer mutants (ruling item 2): MET

- **Byte for byte.** `receipts/r7_mutant_byte_mapping.txt` comes from `probe_byte_mapping.py`. It runs only the constants and the `MINE` dicts of the published R763-7 `r7_mutants.py` and R764-7 `rv7_mutants.py` (sha256 in `receipts/published_r7_scripts.sha256`), and compares them to `MUTANTS` at the head.
  - 9 published names map to 8 edits, all SAME.
  - `r7-no-resume-in-grace-after-pass-1` and `rv7-no-resume-later-in-grace` are the one edit `no-resume-later-in-grace`.
  - The PR body's mapping table is accurate.
  - The `rv6-*` renames are complete: no `rv6-`, `rv7-` or `r7-` name remains in `scripts/` or `docs/testing/TESTING.md`.
- **Red with words.** `receipts/mutants.log` is my own `--mutants --jobs 12` run at the head: `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`. `none` is green on all 10 controls, and each of the 8 is red on its control with its words.
- **Every listing checked** (`receipts/edge_and_r8_mutants_all_listings.txt`). The F1 mutants are red on the in-grace cells as the PR body states:
  - `no-resume-later-in-grace` and `no-window-later-in-grace`: all four later in-grace cells and the 1 s listing;
  - `trap-window-not-later-in-grace`: both later in-grace trap-command cells and the 1 s listing;
  - both `SIGTERM` mutants: the pass-2 trap-command cell and the 1 s listing.
- **Feasibility listings are as published.**
  - The R763-7-F2 listing at `:814-817` matches the published `pin_feasibility_row2.sh` event for event, and `sigterm-to-new-while-shell-stopped` is red on it alone.
  - R764-7's listing at `:812` is the published `kept("an in-grace resume", resumed_at(1), window(1), shell)`.

### 3. Domain notes (ruling item 3): MET for cells; see F1 and F2 for the rows

- `docs/testing/TESTING.md:259-277` tables the cells with each listing's words. These match the `kept` words in the code.
- **Rows 2, 3, 5, 6, 7 and 8** (`:282-288`): each names only cells and listings that exist, and none claims a cell that no listing exercises.
  - Row 2's new-descendant clause names exactly the cells whose command is listed inside grace (first pass, pass 2, 1 s). The audit above confirms those are the only ones.
- **Table check** (`receipts/table_check.txt`):
  - all 116 mutants with a control are named;
  - each named mutant's control appears in its row;
  - the 3 mutants with no control are in no row;
  - only `windows-2s` is in two rows, as R763-6 accepted.
- **What item 3 does not close.** Line 258 still says the domains "Together ... cover all that the row states". Two row statements outside every listing survive mutation (F1, F2).

### 4. Edge mutants (ruling item 4): MET

- `receipts/edge_and_r8_mutants_all_listings.txt` runs all 23 listings under each of the twelve edge mutants (`process_test_support.py:676-752`).
- Each is red on exactly its own cell's listing, 1 of 23, and each is red with its words in `receipts/mutants.log`.
- `last-pass-trap-command-spared-only-if-listed-at-resume` leaves round 7's "a last-pass resume" green and turns the matrix cell red, as the PR body says.

### 5. Residues and preflight cost

- **Round 7 residues: all RESOLVED, with their exact fixes:**
  - R763-7-R1 is at `TESTING.md:300`;
  - R763-7-R2 is at `:259`;
  - R764-7-R1 is in row 13;
  - R763-7-R3 and R764-7-R2 are superseded by the matrix wording.
- **Preflight cost** (`receipts/preflight_cost.txt`): `owner_stated_seconds` takes 0.13 to 0.19 s here against 0.12 to 0.13 s at round 7, interleaved, 3 runs each.
- **Whole test** (`receipts/whole_test.log`): rc 0, 60.9 s, SIGHUP at its default (`receipts/whole_test_sighup.txt`). That is in line with the author's 60.4 s.
- **Comment rule:** every comment and docstring line the delta adds was scanned. None shows a lane label, lane name, review round, reviewer ID or comment ID.

## Findings

### R763-8-F1 - MINOR - Conformance, Tests, Docs - no listing has a live new descendant while the cancelled shell is stopped

- **Locations:**
  - `docs/testing/TESTING.md:285` (row 5: "A cancelled shell stays stopped while any other descendant lives"; its domain is "over a shell stopped while its child lives");
  - `docs/testing/TESTING.md:258`;
  - `scripts/test_suite_cancellation.py:741-830`;
  - `scripts/owned_process.py:303-304`.
- **Authority:**
  - Row 5 states "any other descendant". Line 258 says the domains together "cover all that the row states".
  - The ruling requires each cell to assert the row 5 behaviour that applies to it, and its listing with a new descendant while the shell is stopped.
  - The bar: a survivor against a listed row is a finding.
- **Evidence:**
  - Every new descendant in `owner_stated_seconds` is a PID above the PID range (`:756`), so `_live()` (`owned_process.py:104-106`) never counts it as live. The only live process the control lists is the first-census child `os.getpid()`.
  - In "a new descendant beside a stopped shell" (`:814`), the first-census child keeps the shell stopped by itself. So no listing tests that a live new descendant keeps it stopped.
  - Reviewer mutant `r8-resume-beside-new-live` changes `owned_process.py:304` to count only first-census descendants as live: `not ({p for p in live if (p, owned[p][1]) in initial} - {root_pid})`.
  - It is green on all ten owner controls (`receipts/r8_mutants.log`, `r8_mutants.py`, which uses the repository's own `mutant_tree` and `run_mutant`).
- **Impact:**
  - On a cancel, a command's own terminal trap may start a cleanup process and exit.
  - Under the mutant, the stopped sweep shell is resumed while that cleanup still runs, so its terminal trap runs alongside it. Row 5 says this cannot happen.
  - Nothing committed would see the regression.
- **Required outcome, preferred** (pin, never narrow):
  - A listing in which a descendant new since the first census is live while the cancelled shell is stopped, and the shell is resumed only once it is gone.
  - This mutant, or an equivalent, joins `MUTANTS`, red on a named control with its words, and is named in row 5. Row 5's domain note names the case.
  - **Feasibility, not prescribed:** `r8_feasibility.py` adds one listing to a copy:
    - first census {shell, child = `os.getpid()`};
    - from pass 2, a live new descendant `os.getppid()` under the shell, until 3 s;
    - stated `SIGTERM` child at 0, `SIGKILL` new at 2, `SIGCONT` at 3, shell `SIGKILL` at 13 and 23, verdict at 23.
  - It is green at the head and red under the mutant alone, 1 of 25 listings (`receipts/r8_feasibility.log`).
- **Required outcome, otherwise:** narrow row 5 to first-census descendants and put the rest on the not-pinned list with a true reason. That contradicts "pin, never narrow", so it needs the manager.
- **Verification:**
  - `python3 -B r8_mutants.py <clone> 12 r8-resume-beside-new-live` is red on a named control.
  - `--mutants` stays PASS, with `none` green.

### R763-8-F2 - MINOR - Conformance, Tests, Docs - no trap command is listed inside grace after a resume later than 1 s

- **Locations:**
  - `docs/testing/TESTING.md:282` (row 2: "A descendant new since that census gets none");
  - `docs/testing/TESTING.md:286` (row 6: the trap's command "gets no `SIGTERM` either, even when the resume comes inside grace");
  - `docs/testing/TESTING.md:258`;
  - `scripts/test_suite_cancellation.py:812,820-825`;
  - `scripts/owned_process.py:319-323`.
- **Authority:**
  - Rows 2 and 6 state the clause for any resume inside grace. Line 258 says the domains together cover all of it.
  - Ruling item 4 asks for the earliest and the latest edge of each class.
- **Evidence:**
  - The audit (`receipts/classify_none.txt`) shows a trap command listed inside grace only after resumes at 0, a tick and 1 s.
  - In the matrix's latest in-grace cell, the command is first listed at 2.5 s less a tick. That is past grace by construction, because its pass is the last in grace. So that cell pins row 8, not this clause.
  - The latest edge of the clause is a resume one pass before the last in-grace pass, with the command listed in the last one. No listing has it.
  - Reviewer mutant `r8-sigterm-trap-command-after-late-grace-resume` changes `:322` to `if (pid, start) not in initial and not (resumed is not None and resumed >= 1.5):`. It is green on all ten owner controls (`receipts/r8_mutants.log`). Any threshold above 1 s survives the same way.
- **Impact:**
  - A command whose own `SIGTERM` trap takes most of grace is realistic. When it exits, the shell is resumed near the end of grace. Its trap's cleanup command, listed one pass (about 20 ms) later and still inside grace, would get `SIGTERM` under the mutant.
  - Row 2 says that cannot happen ("so a terminal trap's cleanup command can run").
  - The domain notes are honest about which cells they cover. Line 258's claim, and the rows' unconditional wording, are not.
- **Required outcome, preferred:**
  - A listing in which a trap command is listed inside grace after a resume in the latter part of grace, ideally at the last in-grace pass, and gets no `SIGTERM`.
  - This mutant, or an equivalent, joins `MUTANTS`, red with its words, and is named in rows 2 and 6, whose domain notes name the case.
  - **Feasibility, not prescribed:** `kept("...", resumed_at(2 - TICK), window(2 - TICK), shell)` lists the command at the 2 s less a tick pass. It is green at the head and red under the mutant alone, 1 of 25 (`receipts/r8_feasibility.log`).
  - **A more faithful shape:** the command listed one pass after a resume, both inside grace. That needs a stated event at 2 s to put a pass at 2 s less a tick.
- **Required outcome, otherwise:** narrow rows 2 and 6 to the resumes pinned and record the rest as not pinned. That needs the manager.
- **Verification:**
  - `python3 -B r8_mutants.py <clone> 12 r8-sigterm-trap-command-after-late-grace-resume` is red on a named control.
  - `--mutants` stays PASS.

### RESIDUE (wording only; non-blocking; for the residue checklist)

**R763-8-R1 - RESIDUE - Docs - `docs/testing/TESTING.md:262`**

- "since its clock is its own length" gives the wrong reason. A first pass that takes an hour still counts only half a second (`owned_process.py:284`). The PR body has it right.
- **Exact fix:** "The first pass of cleanup is always inside grace, since its clock is its own length, at most half a second, so the first pass past grace is the first at or past 2 s."

**R763-8-R2 - RESIDUE - Tests (docstring) - `scripts/test_suite_cancellation.py:752-753`**

- "Other listings resume it at 1 s, 3 s and 5.5 s, with that command listed from the resume, and never" leaves out "a last-pass resume" and "a resumed vanishing listing". Both resume at 14 s less a tick, with the command from the resume. The guide's line 276 includes them.
- **Exact fix:** "Other listings resume it at 1 s, 3 s, 5.5 s and a tick before 14 s, with that command listed from the resume, and never."

**R763-8-R3 - RESIDUE - Tests (comment) - `scripts/test_suite_cancellation.py:819`**

- "That command after a first-pass resume is the listing above." The listing directly above is "a new descendant beside a stopped shell". The one meant is seven listings up.
- **Exact fix:** "That command after a first-pass resume is the listing "a first-pass resume" above."

### SUGGESTION

**R764-6-S1 - SUGGESTION - retained, not taken (outside #833, as the author states)**

- My first whole-test run was started under a launcher that ignores SIGHUP. It failed only at `hard-HUP` with `TimeoutExpired` after 60 s, rc 1 (`receipts/whole_test_nohup_sighup_ignored.log`).
- With SIGHUP at its default, the same head passes, rc 0 (`receipts/whole_test.log`).
- This predates the PR and is not a defect of this delta. A new Issue remains the right home.

## Prior findings at this head

| ID | Severity | Status | Evidence |
|---|---|---|---|
| R763-7-F1 = R764-7-F1 | MINOR | RESOLVED | Later in-grace cells at `:820-825` and the 1 s listing at `:812`. All three mutants of each reviewer are red with words (`receipts/mutants.log`) and red on those cells (`receipts/edge_and_r8_mutants_all_listings.txt`). Byte mapping SAME |
| R763-7-F2 | MINOR | RESOLVED | Listing at `:814-817`. `sigterm-to-new-while-shell-stopped` is red on it alone. Row 2 names it |
| R763-7-R1, R2, R3 | RESIDUE | RESOLVED | `TESTING.md:300`, `:259`, rows 6 to 8 |
| R764-7-R1, R2 | RESIDUE | RESOLVED | Row 13's note; the docstring (see R763-8-R2 for a residual omission) |
| R763-7-S1 = R764-7-S1 | SUGGESTION | TAKEN | No round-prefixed mutant names remain |
| R763-7-S2 | SUGGESTION | TAKEN | The author's receipts quote `grace_resume_probe2.py` (`author-r8/receipts/final/grace2-*`) |
| R764-7-S2 | SUGGESTION | TAKEN | `shell-window-one-pass` and `trap-commands-1s` are red on `owner_stated_seconds` with "a late resume's stated seconds were not kept" (`receipts/mutants.log`), and red on 16 and 10 listings with every listing checked |
| R764-6-S1 | SUGGESTION | Retained | See above |
| Rounds 1 to 6 findings | - | Resolved at earlier heads, per both round 7 reports | The delta touches only `owner_stated_seconds`, `MUTANTS` and the cleanup table. The campaign and the table check stay PASS |

## Lens results

- [R763] MINOR Conformance - `docs/testing/TESTING.md:258,282,285,286` vs the round 8 ruling and the bar - R763-8-F1 and F2: rows 2, 5 and 6 state behaviour that line 258 says is covered and that a surviving mutant breaks. Ruling items 1 to 4 are met (`receipts/classify_none.txt`, `edge_and_r8_mutants_all_listings.txt`, `r7_mutant_byte_mapping.txt`). The "first pass past grace" reading is correct against `owned_process.py:260-313`. The product is correct in every probe.
- [R763] PASS RTL - PR file list `1f29f189..5b6d38a3` (`docs/testing/TESTING.md`, `scripts/owned_process.py`, `scripts/process_test_support.py`, `scripts/test_suite_cancellation.py`, `tb/verilator/gptp_shadow/test_mutant_lifecycle.py`) - no HDL, CDC, FSM or interface artifact in the PR or the delta, so the lens is inapplicable by the diff. The delta changes nothing the prior RTL verdict depends on.
- [R763] PASS Robustness - `scripts/process_test_support.py:268-313`, `scripts/owned_process.py` (byte-identical to round 7) - `starved_cleanup` restores `owned_process.time` and the owner hooks in `finally`, and its clock is bounded (`clock < 100`) and exact in binary.
  - The campaign at 12 jobs is PASS (`receipts/mutants.log`).
  - The whole test is rc 0 with SIGHUP at its default (`receipts/whole_test.log`).
  - The one red run is the pre-existing SIGHUP-ignored launcher case (R764-6-S1), not this delta.
- [R763] MINOR Tests - `scripts/test_suite_cancellation.py:741-830`, `scripts/process_test_support.py:321-752` - R763-8-F1 and F2: two reviewer mutants are green on all ten owner controls (`receipts/r8_mutants.log`).
  - Everything else checks: the campaign is PASS, 119/116; the edge mutants are red on their own cell alone; and all nine round 7 mutants are byte for byte and red with words.
  - The author's published `--matrix` (4 parts, 1353 runs) checks mutant by mutant: `none` green on all 11; each of the 116 red on its control and on the whole test; the 3 with no control green on all 11 (`receipts/author_matrix_check.txt`).
- [R763] MINOR Docs - `docs/testing/TESTING.md:258-301`, PR body Round 8 - R763-8-F1 and F2: line 258 overstates coverage for rows 2, 5 and 6. RESIDUE R763-8-R1 to R3. The PR body's mapping, edge table and claims checked accurate. No comment-rule instance in the delta.

## Reviewer ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R763-8-F1, F2 open) | `TESTING.md:255-301`; `owned_process.py:37-45,104-106,256-339`; issue #833 acceptance; round 8 ruling | R763-8 | `5b6d38a3542119ad77d352ea992e3cc41d121620` |
| RTL | CLEAN | PR file list `1f29f189..5b6d38a3`: no HDL or interface artifact | R763-8 | `5b6d38a3542119ad77d352ea992e3cc41d121620` |
| Robustness | CLEAN | `process_test_support.py:265-313`; `owned_process.py` unchanged since `887fdd53`; `receipts/mutants.log`, `receipts/whole_test.log` | R763-8 | `5b6d38a3542119ad77d352ea992e3cc41d121620` |
| Tests | UNCLEAN (R763-8-F1, F2 open) | `test_suite_cancellation.py:741-830`; `process_test_support.py:321-753`; all `receipts/*` | R763-8 | `5b6d38a3542119ad77d352ea992e3cc41d121620` |
| Docs | UNCLEAN (R763-8-F1, F2 open; RESIDUE R1 to R3) | `TESTING.md:255-301`; PR body Round 8 section; delta comments and docstrings | R763-8 | `5b6d38a3542119ad77d352ea992e3cc41d121620` |

## Executed (all foreground or polled to completion; logs in `receipts/`)

- `python3 -B scripts/test_suite_cancellation.py --mutants --jobs 12`: rc 0, PASS (119 mutants, 116 with a control).
- `python3 -B scripts/test_suite_cancellation.py` with SIGHUP at its default: rc 0, 60.9 s. Under `nohup`, rc 1 at hard-HUP (R764-6-S1).
- `probe_all_listings.py --classify` (head) and `probe_mutants_all_listings.sh` (24 mutants, every listing checked).
- `probe_table.py`, `probe_byte_mapping.py`, `r8_mutants.py` (2 mutants x 10 controls) and `r8_feasibility.py` (3 copies x 25 listings).
- Preflight timing at both heads, and the author's `--matrix` receipts checked mutant by mutant.
- Clone integrity after the probes (`receipts/clone_integrity.txt`):
  - HEAD and `write-tree` match the exact head and tree;
  - index and worktree are clean;
  - the six gitlinks are unchanged;
  - the `scripts/__pycache__/` my runs created was removed, leaving no ignored or untracked file.

## Real limits

- **No real-process probe of F1 or F2.** The surviving mutants are shown on the starved owner's clock and on every owner control. A production-stage reproduction (as in `grace_resume_probe2.py`) was not run for either.
- **No source bank was run by the manager or by me at this head.** Source-head gates are the author's published receipts; I re-ran only the cancellation test, its campaign and my probes.
- **Not run here:** the docs workflow steps, `make -C tb/verilator/gptp_shadow lifecycle` and `behave`. The delta does not touch them, and I relied on the author's receipts.
- **Hosted checks were mostly in progress** at the time of reading (`receipts/hosted_checks.txt`). Hosted and act acceptance are the manager's.
- Physical calibration NOT RUN, and field skips are not hardware proof.

## Pending manager duties

- Rule on R763-8-F1 and F2: pin (preferred; feasibility shown) or narrow (needs the manager).
- Carry RESIDUE R763-8-R1, R2 and R3 to the residue checklist.
- Validate the current-dev merge candidate (source base `1f29f189`, live dev `e61a4afa`) with builder and native banks at the merge turn, and link its receipts on the PR.
- Hosted and act acceptance at the exact head.

R763-8 FINISHED

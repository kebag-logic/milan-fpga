[R764] NEGATIVE - exact head 5b6d38a3542119ad77d352ea992e3cc41d121620

External review of issue #833 / PR #834, round 8 (R764-8). Tree `bc7cb27fe2b8df97fb30a47a48c304ff34faf85f`, reviewed against source base `1f29f189279f9fc0132f4918e47342b87d22f33a`. The round 8 delta is `887fdd53..5b6d38a3`: five commits that change only tests and text. `scripts/owned_process.py` is unchanged in it (`git diff --quiet 887fdd53..HEAD -- scripts/owned_process.py`).

## Summary

- **One open MINOR, R764-8-F1 (Conformance, Tests, Docs).** Every descendant new since the first census that `owner_stated_seconds` lists inside grace is a fake PID above the PID limit. The product's liveness check (`owned_process.py:104-106,303`) never sees it as live. So rows 2, 6 and 8 are pinned only for new descendants that the product treats as dead.
  - The reviewer mutant `sigterm-to-live-new` sends `SIGTERM` to a live new descendant during grace. It is **green on the whole test**.
  - The reviewer mutant `live-trap-command-unspared-after-in-grace-resume` takes a live trap command out of the shell's window after an in-grace resume. It is also **green on the whole test**.
  - Both break a listed row inside its stated domain. Two listings with a real, live new descendant turn both red and stay green at the head, so the gap can be closed.
- **The round 8 ruling's four items are met as specified:**
  - the matrix, one listing per cell;
  - every round 7 reviewer mutant, each byte for byte and red with its words;
  - domain notes that name their cells;
  - twelve edge mutants, each red on its own cell's listing alone.
- **Every round 7 finding (R763-7 and R764-7) is resolved or taken** (table below). The suggestion R764-6-S1 is still not taken, as before.
- **The product's reading of "first pass past grace" is confirmed.** It is the first census pass at or past 2 s (`owned_process.py:284,313`).
- **One RESIDUE (docstring) and one SUGGESTION.** No new instance of the comment rule.

## Scope reconstructed

- The manager's round 8 ruling (issue #833, issuecomment-6588568293) asks for four things:
  - a resume-timing matrix: {first pass in grace, later pass in grace, first past grace, later past grace} x {nothing else live, a trap command started after the resume};
  - a new descendant while the shell is stopped (R763-7-F2);
  - every round 7 reviewer mutant red on a named control with its words;
  - domain notes that name their cells, and one edge mutant per cell.
- The bar is unchanged. A survivor against a listed row inside its stated domain is a finding. A survivor against unlisted behaviour is residue.
- Authorities read:
  - `docs/testing/TESTING.md:253-305`: the preamble, the matrix, the cleanup table and the not-pinned list;
  - `scripts/owned_process.py:104-106,256-339`: the product, unchanged;
  - `scripts/test_suite_cancellation.py:741-829`: `owner_stated_seconds`;
  - `scripts/process_test_support.py:264-313`: `starved_cleanup` and `TICK`;
  - `scripts/process_test_support.py:315-753,756-836`: `MUTANTS` and the campaign;
  - PR body sections "Round 8" through "Round 8 gates".
- I did my own pass over the diff before reading the published R763-7 and R764-7 reports.

## Focus checks

### 1. The matrix (`test_suite_cancellation.py:769-778,812-824`; `TESTING.md:261-276`)

- **Cells.** `cell(resume, *started)` lists the child while `clock < resume`. It lists what the trap starts only when `clock > resume`, from the pass after the resume. That is correct, because a census taken before the `SIGCONT` cannot list a command the trap starts.
- **Cell clocks.** On the starved clock the cells resume at:
  - 0 (pass 1);
  - `TICK` (pass 2);
  - `2-TICK` (the last pass before 2 s, pass 6);
  - 2 (the first pass at or past 2 s);
  - `2+TICK`;
  - `14-TICK` (the last pass before the verdict).
- The author's signed `matrix-audit.log` confirms each pass, each clock, and when each command is first listed. I checked its hash, below. The command is listed inside grace only after the pass-1 and pass-2 resumes, at 0.5 s and 0.5 s + tick. That matches `TESTING.md:275`.
- **Assertions.** Each cell asserts its whole event list, to a tick:
  - `SIGTERM` and `SIGKILL` to the child where it is listed;
  - no `SIGTERM` to the shell or to the command;
  - `SIGCONT` in exactly the resume pass;
  - `SIGKILL` 10 s after the resume, and the verdict 20 s after.
  - Together these assert rows 2, 3, 5, 6, 7 and 8 for that cell.
- **New descendant beside a stopped shell (`:814-817`).** This is R763-7's feasibility listing as published. It is pinned by `sigterm-to-new-while-shell-stopped`.
- **The author's reading "first pass past grace = first census pass at or past 2 s" is correct against the product:**
  - `signum = SIGKILL if clock >= deadline` (`owned_process.py:313`).
  - The first pass's clock is its own length, capped at 0.5 s (`:260,284`), so pass 1 is always inside grace.
  - Reviewer probes pin the edge (`receipts/probes.log`):
    - `grace-strictly-past` (`>` for `>=`) is red;
    - `resume-held-at-grace-edge` is red on "a lone first past-grace resume";
    - `no-window-at-grace-edge` is red on the same listing.
- **Limit (see S1).** Each class is sampled at its earliest and latest pass, as the ruling specifies. Mutants with a magic threshold inside a class survive:
  - `interior-past-grace-no-window` (7 s to 13 s) is green;
  - `interior-in-grace-lone-shell-killed` (0.5 s to 1.5 s) is green.
  - No row claims those interior points, so neither is a finding.

### 2. Round 7 reviewer mutants and the rv6 renames

- **All nine published round 7 edits match `MUTANTS` byte for byte** under their behaviour names (`receipts/rename-check.log`). There are nine because R763-7's and R764-7's no-resume mutants are one edit. The PR body's mapping table is exact:
  - `r7-check-before-open-sigkill` → `check-before-open-for-sigkill` (control `owner_reused_identity`);
  - `r7-no-resume-in-grace-after-pass-1` and `rv7-no-resume-later-in-grace` → `no-resume-later-in-grace`;
  - `r7-sigterm-trap-command-later-grace-resume` → `sigterm-trap-command-unless-first-pass-resume`;
  - `rv7-sigterm-trap-command-later-grace-resume` → `sigterm-trap-command-after-later-grace-resume`;
  - `r7-trap-window-not-later-grace` → `trap-window-not-later-in-grace`;
  - `rv7-no-window-later-in-grace` → `no-window-later-in-grace`;
  - `r7-sigterm-new-while-shell-stopped` → `sigterm-to-new-while-shell-stopped`;
  - `rv7-sigterm-to-new-after-1s` → `sigterm-to-new-after-1s`.
- **The six `rv6-*` renames change only the key.** The edit, control and words are the same context lines in the diff. TESTING rows 1, 5, 6 and 12 use the new names.
- **`trap-commands-1s` and `shell-window-one-pass` are rebound to `owner_stated_seconds`.** Their words are "a late resume's stated seconds were not kept". Both are red with no timing in my campaign (R764-7-S2 taken).
- **Default campaign at this head:** `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)`, `--jobs 8`, rc 0 (`receipts/mutants-default.log`).

### 3. Domain notes (`TESTING.md:282-288`)

- Rows 2, 3, 5, 6, 7 and 8 name the matrix cells they cover.
- Row 2's new-descendant clause names only the cells whose command is listed inside grace: pass 1, pass 2 and the 1 s listing. Its "beside a stopped one" names the new listing.
- I checked each cell claim against the listings and the audit. No row claims a **cell** that no listing exercises.
- The claim that over-reaches is about **liveness**, not timing: see F1.
- Row 5's "from the first pass ... to the last before 14 s" could read as a span. The preamble (`:261`) and the "At" column (`:268-273`) say the cells are edge samples. See S1.

### 4. Edge mutants

- All twelve are red on `owner_stated_seconds` with their cell's words (`receipts/mutants-default.log`).
- The author's signed `per-listing.log` shows each one missing on its own cell's listing only, and on none of the other 22.
- The edge conditions match the cell clocks:
  - `passes == 1`, `passes == 2`;
  - `deadline - MAX_PASS_SECONDS <= clock < deadline`;
  - `late == 1`, `late == 2`;
  - `clock + MAX_PASS_SECONDS >= kill_all + REAP_SECONDS`, taken before `kill_all` is extended.
- `last-pass-trap-command-spared-only-if-listed-at-resume` is correctly green on round 7's last-pass listing, whose command is listed at the resume, and red on the matrix cell.

### 5. Residues and preflight cost

- **R763-7-R1, R763-7-R2 and R764-7-R1 are applied as their exact fixes** (`TESTING.md:300`, `:259`, `:293`).
- **R763-7-R3 is resolved:** the rows now name the cells and the resumes at 1 s, 3 s and 5.5 s.
- **R764-7-R2 is resolved as published.** The docstring has a new omission, recorded as RESIDUE R764-8-R1.
- **Cost.**
  - The author's signed `cost.txt`:
    - `owner_stated_seconds` takes 0.16 to 0.21 s before and after;
    - the whole test has a mean of 60.6 s at round 7 and 60.4 s at round 8.
  - My runs at load 35 to 41 (`receipts/stated-seconds-timing.txt`): 0.22, 0.19 and 0.18 s, each rc 0. The whole test is rc 0, `suite cancellation: PASS` (`receipts/whole-head.log`).
  - The preflight cost is unchanged.
- **Module ratchet:** `test_suite_cancellation.py` has 965 lines.
- **Comment rule:** the added source lines carry no lane label, round, reviewer ID or comment ID. A grep of the delta's added lines returns rc 1.

## Findings

### R764-8-F1 - MINOR - Conformance, Tests, Docs - new descendants in grace are pinned only when not live

- **Locations:**
  - `scripts/test_suite_cancellation.py:755-756`: every new descendant is a fake PID, "never ... a real process";
  - the listings with a new descendant inside grace:
    - `:798` "a first-pass resume";
    - `:800-803` "a new descendant";
    - `:812` "an in-grace resume";
    - `:814-817` "a new descendant beside a stopped shell";
    - `:824`, the pass-2 cell "a second-pass resume and its trap command";
  - `docs/testing/TESTING.md:282` (row 2), `:286` (row 6) and `:288` (row 8), with their domain notes;
  - `docs/testing/TESTING.md:257-258`: "Together they cover all that the row states";
  - product: `scripts/owned_process.py:104-106` (`_live`), `:303` (`live`), `:319-323` (no `SIGTERM` to new descendants) and `:332` (the trap command's window).
- **Authority:**
  - Row 2: "A descendant new since that census gets none [`SIGTERM`], so a terminal trap's cleanup command can run". Its domain: "over descendants new since then and listed inside grace: before any resume, with no shell and beside a stopped one, and after a resume in the matrix's first-pass and pass-2 cells and at 1 s".
  - Row 6: the trap's command "gets no `SIGTERM`", pinned "listed inside grace after a resume in the matrix's first-pass and pass-2 cells and at 1 s".
  - Row 8: the trap's command gets no `SIGKILL` inside the window, pinned "in every matrix cell with one".
  - The bar: a survivor against a listed row inside its stated domain is a finding.
  - The round 8 ruling closes the class "a domain note claims a case that no listing exercises".
- **Evidence:**
  - `_live(pid)` reads `/proc/<pid>/stat`, so to the product every fake PID is not live. A real cleanup or trap command is a live process.
  - The only real PID in the control is `child`, which is never new.
  - So every in-grace new descendant in the pinning control is, to the product, the same as a zombie.
  - Two reviewer mutants that depend on the product's own `live` set survive **the whole test** (`receipts/live-probes.log`, `probes/r764_8_live_probes.py`):
    - **`sigterm-to-live-new`** changes the grace skip `if (pid, start) not in initial:` to `... not in initial and pid not in live:`. A live descendant new since the first census then gets `SIGTERM` during grace. That is exactly what row 2 says cannot happen, and what row 6 says of the trap's command. Whole test: rc 0, `suite cancellation: PASS`.
    - **`live-trap-command-unspared-after-in-grace-resume`** adds `and (pid not in live or resumed >= deadline)` to the window line `:332`. After an in-grace resume, a live trap command is then `SIGKILL`ed at 2 s, inside the shell's window. Whole test: rc 0.
  - Control: `live-trap-command-unspared` (no time condition) is red on `owner_shell_window`, a real trap command after a resume past 4 s. So liveness is pinned for a resume past 4 s, but not inside grace.
- **Impact:**
  - This is R763-7-F2's own scenario. A cancel stops the top shell. A nested recipe shell runs its terminal trap after its first-pass `SIGTERM`, and that trap's cleanup command is live.
  - Under `sigterm-to-live-new`, that command is `SIGTERM`ed during grace, and the control stays green.
  - The same holds for a trap command after a first-pass, pass-2 or 1 s resume (rows 6 and 8).
  - Rows 2, 6 and 8 claim these cases, but every listing exercises them only with entries the product sees as dead.
- **Feasibility (not prescribed)** (`probes/r764_8_live_feasibility.py`, `receipts/live-feasibility.log`). Two listings use a real sleeping process as the new descendant:
  - "a live new descendant beside a stopped shell": the command is listed from pass 2 as a child of the stopped shell;
  - "a second-pass resume and its live trap command": the matrix's pass-2 cell with a live command.
  - Results:
    - green at the head (rc 0);
    - `sigterm-to-live-new` red, with `(0.5, 'SIGTERM', 'trap command')`;
    - `live-trap-command-unspared-after-in-grace-resume` red, with `(2.0000009536743164, 'SIGKILL', 'trap command')`.
  - Note: a live descendant of `child` would also spare `child` until 4 s (row 3, `owned_process.py:329`). So R763-7's shape, with the command under `child`, needs its expected list changed if it is made live.
- **Required outcome:**
  - Rows 2, 6 and 8 are pinned for live new descendants inside their stated domains:
    - before any resume, beside a stopped shell;
    - with no shell;
    - the trap's command after an in-grace resume, the matrix's pass-1 and pass-2 cells and 1 s.
  - Both reviewer mutants, or equivalents, are in `MUTANTS`, red on a named control with their words, and named in their rows.
  - Otherwise: narrow those domain notes to entries the product does not see as live, and put the live case on the not-pinned list with a true reason. This needs the manager, since the ruling says pin, never narrow.
- **Verification:**
  - `python3 -I probes/r764_8_live_probes.py <clone> <scratch>`: both survivors red.
  - `python3 scripts/test_suite_cancellation.py --mutants`: PASS.
  - Every check in Focus checks 1 to 4 still passes.

### R764-8-R1 - RESIDUE - Tests (docstring wording) - `scripts/test_suite_cancellation.py:752-753`

- "Other listings resume it at 1 s, 3 s and 5.5 s, with that command listed from the resume, and never" leaves out the two round 7 listings that resume at a tick before 14 s (`:805`, `:810`). `TESTING.md:276` names them.
- **Exact fix:** "Other listings resume it at 1 s, 3 s, 5.5 s and a tick before 14 s, with that command listed from the resume, and never."

### R764-8-S1 - SUGGESTION - Docs, Tests - `docs/testing/TESTING.md:285` (row 5 domain), `:261`

- Each class is sampled at its earliest and latest pass, as ruled. Interior-threshold mutants survive (`receipts/probes.log`: `interior-past-grace-no-window`, `interior-in-grace-lone-shell-killed`).
- Row 5's "in every matrix cell, from the first pass, with nothing else ever live, to the last before 14 s" can be read as a continuous span.
- Optional: say "at each cell's listed resume" in row 5, or state once in `:261` that a cell's domain is its listed resume, not the whole class.
- No row is overstated as the preamble reads, so this is not a finding.

## Prior findings at this head

| ID | Severity | Status at this head | Evidence |
|---|---|---|---|
| R763-7-F1 = R764-7-F1 | MINOR | **RESOLVED** | Matrix later-in-grace cells `test_suite_cancellation.py:820-824`. All four F1 mutants are red with words; per the PR body, they are also red on those cells. Campaign PASS |
| R763-7-F2 | MINOR | **RESOLVED as specified** (listing `:814-817`, `sigterm-to-new-while-shell-stopped` red). Its cause is not fully closed: the listing's new descendant is not live. See R764-8-F1 | `receipts/mutants-default.log`, `receipts/live-probes.log` |
| R763-7-R1, R2 | RESIDUE | **RESOLVED**, exact fixes | `TESTING.md:300`, `:259` |
| R763-7-R3 | RESIDUE | **RESOLVED** | `TESTING.md:286-288` |
| R764-7-R1 | RESIDUE | **RESOLVED**, exact fix | `TESTING.md:293` |
| R764-7-R2 | RESIDUE | **RESOLVED**. A new omission is R764-8-R1 | `test_suite_cancellation.py:749-753` |
| R763-7-S1, R764-7-S1 | SUGGESTION | **TAKEN** | `receipts/rename-check.log`; diff of `process_test_support.py` |
| R763-7-S2 | SUGGESTION | **TAKEN** | PR body, Round 8 mutation table |
| R764-7-S2 | SUGGESTION | **TAKEN** | `MUTANTS` `shell-window-one-pass`, `trap-commands-1s` → `owner_stated_seconds`, red |
| R764-6-S1 | SUGGESTION | Retained, not taken. It is outside #833 | PR body |

## Evidence verified

- **Signed packet.** The published evidence is at `7aba003d12dbb80a2826d847e4d2a625c9303e28:review-evidence/833-r1`. I hashed 10 round 8 receipts against `MANIFEST.json` `published_sha256`, and all 10 are OK:
  - `cost.txt`;
  - `matrix-audit.log`;
  - `per-listing.log`;
  - `matrix-part1..4.log`, each ending PASS;
  - `matrix-table.md`;
  - `rv7-mutants.log`;
  - `r7-mutants.log`.
  - R763-7 and R764-7 `REPORT.md` are also OK.
  - I fetched `probe-tree-head.txt` from the wrong path (404), so it was not checked.
- **My runs at the exact head.** Load was 33 to 47 on 16 CPUs.

| Run | Result | Receipt |
|---|---|---|
| Whole test | rc 0, `suite cancellation: PASS` | `receipts/whole-head.log` |
| Default mutant campaign | rc 0, PASS, 119 mutants / 116 controlled | `receipts/mutants-default.log` |
| Boundary probes | `none` green; 6 red; 2 interior-threshold green (S1) | `receipts/probes.log` |
| Liveness probes | 2 green on the whole test (F1); 1 red | `receipts/live-probes.log` |
| Feasibility | head green; both survivors red | `receipts/live-feasibility.log` |

- **Hosted, at the exact head:** the PR is ready. Contexts were in progress or queued when this review ran. Physical gPTP was skipped, which is not hardware evidence. I claim no hosted verdict.
- **Restore** (`receipts/restore-check.txt`):
  - `diff-index` is clean, and the index matches the HEAD tree in mode, blob and path;
  - 0 worktree blobs differ when rehashed;
  - the six gitlinks are unchanged;
  - no untracked or ignored files remain (one probe's `scripts/__pycache__` was removed).

## Lens results

- [R764] MINOR Conformance - `docs/testing/TESTING.md:282,286,288` vs `scripts/test_suite_cancellation.py:755-824` - R764-8-F1: rows 2, 6 and 8 claim new descendants in grace that are pinned only when not live.
- [R764] PASS RTL - `scripts/owned_process.py:256-339` (unchanged in the delta) - I read the cleanup FSM against the matrix's edges. `>=` grace (`:313`), pass-1 clock (`:284`), resume (`:304-312`) and window (`:317,324-333`) are consistent. Boundary probes are red (`receipts/probes.log`). There is no HDL in the delta.
- [R764] PASS Robustness - `scripts/owned_process.py:256-339`, `receipts/probes.log` - The edge timings (2-TICK, 2, 2+TICK, 14-TICK), the stopped shell beside a new descendant, and the verdict timing are handled correctly. The product is unchanged and no probe shows it wrong.
- [R764] MINOR Tests - `scripts/test_suite_cancellation.py:755-824`, `scripts/process_test_support.py:315-753` - R764-8-F1: two reviewer mutants survive the whole test. Everything else in the round 8 test delta checks out: the matrix, 21 new mutants, renames and edge mutants. RESIDUE R764-8-R1.
- [R764] MINOR Docs - `docs/testing/TESTING.md:253-305`, PR body Round 8 - R764-8-F1: the domain notes of rows 2, 6 and 8 over-claim liveness. Cell claims are exact, and the PR body's mapping and tables are exact. SUGGESTION R764-8-S1.

## Reviewer ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (R764-8-F1) | `TESTING.md:253-305`; round 8 ruling; `owned_process.py:256-339` | R764-8 | 5b6d38a3542119ad77d352ea992e3cc41d121620 |
| RTL | CLEAN | `owned_process.py:104-106,256-339` (unchanged since `c1b29617`); no HDL in delta | R764-8 | 5b6d38a3542119ad77d352ea992e3cc41d121620 |
| Robustness | CLEAN | `owned_process.py:256-339`; `receipts/probes.log` | R764-8 | 5b6d38a3542119ad77d352ea992e3cc41d121620 |
| Tests | UNCLEAN (R764-8-F1) | `test_suite_cancellation.py:741-829`; `process_test_support.py:264-313,315-836`; campaign, probes, feasibility | R764-8 | 5b6d38a3542119ad77d352ea992e3cc41d121620 |
| Docs | UNCLEAN (R764-8-F1; RESIDUE R1 is non-blocking) | `TESTING.md:253-305`; PR body Round 8; docstring `:742-754` | R764-8 | 5b6d38a3542119ad77d352ea992e3cc41d121620 |

## Real limits

- I ran no full parent, PP, gPTP, Yosys or builder bank, and no `docs.yml` replay. Source-head gate evidence is the author's published receipts, which I spot-checked by hash, not re-executed.
- I ran no `--matrix` campaign. The per-listing and per-control claims rest on the author's signed `per-listing.log` and `matrix-part*.log`.
- The interior points of each matrix class are not sampled (S1). This is by design under the ruling.
- Physical calibration was NOT RUN. Field skips are not hardware proof.

## Pending manager duties

- Rule on R764-8-F1: pin live new descendants, or narrow the domain notes with a not-pinned entry.
- Carry R764-8-R1 to the residue checklist.
- Hosted and act acceptance at the exact head. The hosted contexts were still running.
- The current-dev merge candidate (source base `1f29f189`, live dev `e61a4afa`): builder and native banks at the merge turn, with receipts linked on the PR.

R764-8 FINISHED

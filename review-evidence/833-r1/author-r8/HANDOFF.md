# #833 round 8 HANDOFF ([A726h])

Status: REVIEW READY, posted on #833 as issuecomment-6590173384 (`receipts/ready.md`, `ready-url.txt`).

Base: round 7 head `887fdd53`. Head `5b6d38a3542119ad77d352ea992e3cc41d121620`, 5 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6588718478 (`receipts/taken.md`, `taken-url.txt`).

Sources, in this order:
- The manager's round 8 ruling: issue #833 issuecomment-6588568293. It is the authority for this round.
- R763-7: PR #834 issuecomment-6588338480, NEGATIVE: MINOR F1 and F2, RESIDUE R1 to R3, SUGGESTION S1 and S2.
- R764-7: PR #834 issuecomment-6588537339, NEGATIVE: MINOR F1 (= R763-7-F1), RESIDUE R1 and R2, SUGGESTION S1 and S2; R764-6-S1 retained.
- Both packets' scripts, run unchanged from copies of their published files.

`scripts/owned_process.py` is byte-identical to `887fdd53` (and to `c1b29617`). No probe or mutant showed the product wrong.

## The findings, each with its change and control

| Finding | IDs | Change at the head | Control: words | Evidence |
|---|---|---|---|---|
| No listing resumed the shell in a later pass inside grace | R763-7-F1, R764-7-F1; ruling item 1 | `scripts/test_suite_cancellation.py:818-824`: the resume-timing matrix (below), `cell()` at `:769`, `window(resume, windowed)` at `:774`. R764-7's feasibility listing, `kept("an in-grace resume", resumed_at(1), window(1), shell)`, as published, at `:812`. Docstring `:742-754` | The 8 round 7 reviewer mutants (item 2 table) | `receipts/item1/matrix-audit.log`, `final/matrix-audit.log`: each listing's resume pass, clock, class and when its command is first listed. `final/per-listing.log` |
| No listing had a new descendant while a cancelled shell is stopped | R763-7-F2; ruling item 1 | `:813-817`: R763-7's feasibility listing as published, "a new descendant beside a stopped shell" | `sigterm-to-new-while-shell-stopped`: "a new descendant beside a stopped shell's stated seconds were not kept" | `final/pin-feasibility-row2-r763-7.log` |
| Every reviewer mutant published at round 7 joins `MUTANTS` | ruling item 2 | `scripts/process_test_support.py:640-675`, named in rows 1, 2, 5, 6, 7, 8 | Item 2 table | `receipts/item2/same-edits-r763.log`, `same-edits-r764.log`: each `MUTANTS` edit is the published edit, byte for byte |
| Each domain note names its matrix cells | ruling item 3; R763-7-R3 | `docs/testing/TESTING.md:261-277`: the matrix described and tabled with each cell's words; rows 2-8 (`:282-288`) name the cells they cover. Row 2's new-descendant clause names only cells whose command is listed inside grace | | `final/per-listing.log`: each cell is exercised; `final/table-check-*.log` |
| An edge mutant per cell | ruling item 4 | `scripts/process_test_support.py:676-752`, named in rows 6, 7, 8 | Item 4 table | `final/per-listing.log`: each red on its own cell and no other listing |
| Not-pinned item 1 | R763-7-R1 | `TESTING.md:300`, the exact fix | | |
| The times preamble | R763-7-R2 | `TESTING.md:259`, the exact fix | | |
| Row 13's note | R764-7-R1 | `TESTING.md:293`, the exact fix | | |
| The docstring's resume list | R764-7-R2 | `test_suite_cancellation.py:742-754`: it now names the resumes the control makes (the matrix's, 1 s, 3 s, 5.5 s, never) | | |
| Round prefixes in `MUTANTS` names | R763-7-S1, R764-7-S1: taken | The six `rv6-*` renamed (item 5); the round 7 ones added under behaviour names. Reason: both reviewers asked; round 8 touches the table; the published names stay traceable here and in the PR body | Unchanged edits, controls, words | `receipts/item5/mutants.log` |
| Quote the corrected grace probe | R763-7-S2: taken | `grace_resume_probe2.py` is the one quoted | | `final/grace2-*.log` |
| `trap-commands-1s`, `shell-window-one-pass` depend on load | R764-7-S2: taken | `process_test_support.py:404,417`: both now name `owner_stated_seconds`. Reason: the brief puts SUGGESTIONs at the author's judgement. Both are red there with no timing, and rows 7 and 8 already list that control. `owner_shell_window` keeps its other 11 mutants for its real-process domain, and `--matrix` still runs both mutants on it | "a late resume's stated seconds were not kept" | `final/stated-seconds-check.log`; `final/matrix-table.md`: both still red on `owner_shell_window` at this load |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1: retained, not taken | None. Reason: as in round 7, it predates this PR and is outside #833 | | |

### Interpretation made public

"First pass past grace" is read as the first census pass at or past 2 s. The first pass of cleanup is always inside grace: its clock is its own length, at most 0.5 s. The PR body and `TESTING.md:262` say so.

## Item 1: the resume-timing matrix

`owner_stated_seconds`, `scripts/test_suite_cancellation.py:818-824`. Every cell's whole event list is asserted to a tick. That covers:
- the child's `SIGTERM` at 0 and `SIGKILL` at 2 where it is listed (row 2, row 3);
- no `SIGTERM` to the shell or its command (rows 2, 6);
- the resume in exactly that pass (row 5);
- `SIGKILL` to the shell and its command at resume + 10 and none before (rows 3, 6, 7, 8);
- the verdict at resume + 20.

| Class | Resume (pass, clock) | Alone | With a trap command | Command first listed |
|---|---|---|---|---|
| first pass, inside grace | 1, 0 s | "a lone first-pass resume" | "a first-pass resume" (round 7's listing, the same cell) | 0.5 s, a `SIGTERM` pass |
| later pass inside grace, earliest | 2, 2^-20 s | "a lone second-pass resume" | "a second-pass resume and its trap command" | 0.5 s + a tick, a `SIGTERM` pass |
| later pass inside grace, latest | 6, 2 s - a tick (next pass 2.5 s - a tick) | "a lone last in-grace resume" | "a last in-grace resume and its trap command" | 2.5 s - a tick, a `SIGKILL` pass |
| first pass past grace | 6, 2 s (pass before: 2 s - a tick) | "a lone first past-grace resume" | "a first past-grace resume and its trap command" | 2.5 s |
| later pass past grace, earliest | 7, 2 s + a tick (pass before: 2 s) | "a lone second past-grace resume" | "a second past-grace resume and its trap command" | 2.5 s + a tick |
| later pass past grace, latest | 31, 14 s - a tick | "a lone last-pass resume" | "a last-pass resume and its trap command" | 14.5 s - a tick |

All of the pass numbers and clocks above are from `final/matrix-audit.log`. The listings beside the matrix:
- resumes at 1 s (R764-7's), 3 s, 5.5 s and 14 s - a tick, with the command listed from the resume pass;
- a stopped shell never resumed;
- "a new descendant beside a stopped shell" (R763-7's).

The new listings run after round 7's, so every earlier mutant keeps its words (`receipts/item1/mutants.log`: PASS 99/96).

`starved_cleanup` and `TICK` moved unchanged to `scripts/process_test_support.py:264-313` (with `import owned_process`, `from types import SimpleNamespace`). That keeps `scripts/test_suite_cancellation.py` at 965 lines, under the 1000-line ratchet. `owner_stated_seconds` is under the 100-line function limit (`check_py_idiom` rc 0).

## Item 2: every reviewer mutant published at round 7

| `MUTANTS` name | R763-7 name | R764-7 name | Finding | Row | Control: words | Also red, every listing checked |
|---|---|---|---|---|---|---|
| `check-before-open-for-sigkill` | `r7-check-before-open-sigkill` | | R763-7 (row 1 edge) | 1 | `owner_reused_identity`: "a census entry was signalled by its number" | |
| `no-resume-later-in-grace` | `r7-no-resume-in-grace-after-pass-1` | `rv7-no-resume-later-in-grace` (same edit) | R763-7-F1, R764-7-F1 | 5 | `owner_stated_seconds`: "an in-grace resume's ..." | all four later in-grace cells |
| `sigterm-trap-command-unless-first-pass-resume` | `r7-sigterm-trap-command-later-grace-resume` | | R763-7-F1 | 6 | "an in-grace resume's ..." | the pass-2 trap-command cell |
| `sigterm-trap-command-after-later-grace-resume` | | `rv7-sigterm-trap-command-later-grace-resume` | R764-7-F1 | 6 | "an in-grace resume's ..." | the pass-2 trap-command cell |
| `trap-window-not-later-in-grace` | `r7-trap-window-not-later-grace` | | R763-7-F1 | 8 | "an in-grace resume's ..." | both later in-grace trap-command cells |
| `no-window-later-in-grace` | | `rv7-no-window-later-in-grace` | R764-7-F1 | 7 | "an in-grace resume's ..." | all four later in-grace cells |
| `sigterm-to-new-while-shell-stopped` | `r7-sigterm-new-while-shell-stopped` | | R763-7-F2 | 2 | "a new descendant beside a stopped shell's ..." | |
| `sigterm-to-new-after-1s` | | `rv7-sigterm-to-new-after-1s` (its control) | R764-7-F1 | 2 | "a first-pass resume's ..." | 4 more listings |

Nine published names, eight edits: two are the same edit (`receipts/item2/same-edits-*.log`).

## Item 4: an edge mutant per cell

Each records at the resume whether that pass is its cell's edge (the `edge` it adds), then breaks that cell's behaviour only there. Run with every listing checked (`final/per-listing.log`), each is red on its own cell's listing and on no other.

| Cell | Edge | Mutant | Row | Words |
|---|---|---|---|---|
| first pass, alone | `passes == 1` | `lone-first-pass-shell-needs-a-child` | 7 | "a lone first-pass resume's ..." |
| first pass, trap command | `passes == 1` | `first-pass-trap-command-sigtermed` | 6 | "a first-pass resume's ..." |
| later in grace, alone, earliest | `passes == 2` | `lone-second-pass-shell-needs-a-child` | 7 | "a lone second-pass resume's ..." |
| later in grace, trap command, earliest | `passes == 2` | `second-pass-trap-command-sigtermed` | 6 | "a second-pass resume and its trap command's ..." |
| later in grace, alone, latest | within a pass of 2 s | `lone-last-in-grace-shell-needs-a-child` | 7 | "a lone last in-grace resume's ..." |
| later in grace, trap command, latest | within a pass of 2 s | `last-in-grace-trap-command-unspared` | 8 | "a last in-grace resume and its trap command's ..." |
| first past grace, alone | first pass at or past 2 s | `lone-first-past-grace-shell-needs-a-child` | 7 | "a lone first past-grace resume's ..." |
| first past grace, trap command | first pass at or past 2 s | `first-past-grace-trap-command-unspared` | 8 | "a first past-grace resume and its trap command's ..." |
| later past grace, alone, earliest | second pass past grace | `lone-second-past-grace-shell-needs-a-child` | 7 | "a lone second past-grace resume's ..." |
| later past grace, trap command, earliest | second pass past grace | `second-past-grace-trap-command-unspared` | 8 | "a second past-grace resume and its trap command's ..." |
| later past grace, alone, latest | within a pass of the verdict | `lone-last-pass-shell-needs-a-child` | 7 | "a lone last-pass resume's ..." |
| later past grace, trap command, latest | within a pass of the verdict | `last-pass-trap-command-spared-only-if-listed-at-resume` | 8 | "a last-pass resume and its trap command's ..." |

The defects:
- the lone cells' shell is spared after its resume pass only while it has a listed child;
- the in-grace trap-command cells' command gets `SIGTERM`;
- the past-grace trap-command cells' command loses its window.

The last-pass one spares only a command listed at the resume. Round 7's last-pass listing, which lists the command from the resume pass, stays green under it, and the matrix's cell turns red.

## Item 5: renames

| Old | New |
|---|---|
| `rv6-sigkill-by-number` | `sigkill-by-number` |
| `rv6-sigcont-by-number` | `sigcont-by-number` |
| `rv6-resume-not-before-grace` | `resume-not-before-grace` |
| `rv6-resume-not-first-pass` | `resume-not-first-pass` |
| `rv6-sigterm-trap-commands` | `sigterm-trap-commands` |
| `rv6-return-before-confirm` | `return-before-confirm` |

## Commits

| Commit | Item | Subject |
|---|---|---|
| `100915d0` | 1 | Resume the cancelled shell in every class of pass in the stated-seconds control, each at its earliest and its latest, alone or with a trap command started after the resume, and list a new descendant beside a stopped shell |
| `03a76583` | 2 | Add every reviewer mutant published at round 7 to MUTANTS, each red on the stated-seconds or reused-identity control with its words and named in the row it breaks |
| `787b727d` | 3 | Table the resume-timing matrix's cells and their words in the testing guide, and name in each cleanup table row the cells its stated-seconds domain covers |
| `9d8ca1ab` | 4 | Add a mutant at the edge of each resume-timing matrix cell, each red on that cell's listing alone, and name each in the row it breaks |
| `5b6d38a3` | 5 | Word the not-pinned SIGCONT item, the times preamble and the re-parented row's domain exactly, name the round's reviewer mutants by behaviour, and pin two shell-window mutants on the stated-seconds control |

One per item, one-line subjects, empty bodies, no trailers. Before each commit (`receipts/item1/` to `item5/`):
- the quick gates: idiom, doc style, docs check, bare-metal scope, diff check;
- the table check;
- per listing at `none`;
- the full `--mutants` campaign: 99/96, 107/104, 107/104, 119/116 and 119/116, each PASS.

## Cost

`final/cost.txt`: each control 3 times at `887fdd53` and at the head, interleaved, host load 6 to 10.
- `owner_stated_seconds` takes 0.16 to 0.21 s at both, and every control is within 0.2 s.
- The whole test, 4 runs each, 8 at once: mean 60.6 s at round 7, 60.4 s here.

**Round 8 adds no measurable time to the preflight** (well under the 2 s allowed).

## Gates

All at head `5b6d38a3542119ad77d352ea992e3cc41d121620`, one log and rc each, never piped.
- The lane gates ran on a fresh clean clone with `TMPDIR` in scratch (`receipts/gates/lane.sh`); `tree-after.txt` is empty with `--ignored`.
- SIGHUP was at its default in every launcher: `SigIgn 0` for the lane gates, campaigns and probes, and `0x4` (SIGQUIT only) for the detached docs.yml launcher, as in round 7 (`gates/sigign.txt`).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's runner and verifier, as copied in round 7; only the venv and HOME paths point at this round's scratch (`gates/runner-vs-round7.diff`), `not_run.json` unchanged. Fresh venv, identical to round 7's freeze (`gates/venv-freeze-new.txt`), fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job (the no-git job has no `.git` to check, as in round 7). Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | `gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/`. `gate_41`'s log is over 200 KB: sha256 and size in `gates/LARGE-LOGS.txt`, tail in `docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `owner-stated-seconds` prints resumes `[0, 1, 3, 5.5, 14 - 2^-20]` and the matrix `[0, 2^-20, 2 - 2^-20, 2, 2 + 2^-20, 14 - 2^-20]` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants --jobs 4` | 0 | `owned-process mutants: PASS (119 mutants, 116 with a control that must fail)` | `gates/lane/mutants.*` |
| `--matrix` (every mutant on every control and the whole test), 4 parts, `--jobs 10` | 0 each | 1353 runs, no run cut. `none` green on all 11; each of the 116 red on its control with its words and on the whole test; the 3 with no control green on all 11 | `final/matrix-part1..4.*`, `final/matrix-table.md` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`; the log is 235,305 bytes, sha256 in `gates/LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` (also inside docs.yml) | 0 each | before each commit | `item*/quick/` |
| Full sweep | not run | Round 8 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

### Reviewers' probes at the head, unchanged

| Probe | Result | Receipt |
|---|---|---|
| `row_mutants.py` (round 6; identical in all three packets) | no survivor among its 10 | `final/row-mutants.*` |
| `r7_mutants.py` (R763-7) | no survivor among its 5 | `final/r7-mutants.*` |
| `rv7_mutants.py` (R764-7) | no survivor among its 4. Its `RV7_WHOLE=1` mode stops at its own report line on the first red result (it joins `None`); that run was red; `--matrix` gives the whole-test column for all four | `final/rv7-mutants*.*` |
| `grace_resume_probe.py` (round 6) | PASS 5 of 5 | `final/grace-resume-head.*` |
| `grace_resume_probe2.py` (R763-7, trees by its `grace_trees.py`) | PASS 3 of 3 at the head; FAIL 3 of 3 on `sigterm-to-new`, `sigterm-trap-commands` (was `rv6-sigterm-trap-commands`), `r7-sigterm-trap-command-later-grace-resume` and `sigterm-trap-command-after-later-grace-resume` | `final/grace2-*` |
| `pin_feasibility.sh`, `pin_feasibility_row2.sh` (R763-7), on their published sets | `none` green; every mutant red with the listing's words | `final/pin-feasibility*-r763-7.log` |
| `rv7_pin_feasibility.py` (R764-7) | PASS | `final/rv7-pin-feasibility.*` |
| `slow_shell_window.py campaign . 8 4 0.15,0.3,0.5` (R764-6) | PASS, 45 runs | `final/slow-shell-window.*` |
| `sigcont_pending.py` (R764-6) | rc 0 | `final/sigcont-pending.*` |
| `stated_seconds_check.py` (R764-7) | both S2 mutants red on `owner_stated_seconds` | `final/stated-seconds-check.*` |
| Table checks: R763-7 `table_check.py`, R764-7 and R764-6 `table_vs_mutants.py`, the lane's | rc 0 each | `final/table-*` |
| R763-6 `table_vs_mutants.py` | rc 1 for `windows-2s` only, named in two rows, which R763-6 accepted at round 6 (as at round 7) | `final/table-vs-mutants-r763-6.*` |

## Incidents, no harm

- One command (a clone into scratch whose script began with an `rm -rf` of a variable path) was refused by the session's permission policy. It was re-run without the removal, since the directories did not exist yet.
- Every run set `TMPDIR` to scratch and ran with `-B` or `PYTHONDONTWRITEBYTECODE=1`. The lane's ignored `scripts/__pycache__` and `tb/verilator/gptp_shadow/__pycache__` predate this session (mtimes 2026-11-02 20:41 and 2026-11-01 23:23); nothing tracked changed.
- The unit's memory peak was 7.2 GB, page cache included, under the 12 GB asked.
- Nothing was signalled by name.

## Files

- `PR-BODY.md`: round 7's body with a Round 8 section; the shared sections (status, roles, expected result, cost note) brought to this head.
- `receipts/`: `taken.md`; `item1/` to `item5/`; `final/` (probes, matrix, per listing, cost at the head); `gates/` (lane gates, docs.yml); `tools/` (this round's probes and checks).

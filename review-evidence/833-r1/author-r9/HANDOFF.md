# #833 round 9 HANDOFF ([A726i])

Status: REVIEW READY, posted on #833 as issuecomment-6592237814 (`receipts/ready.md`, `ready-url.txt`).

Base: round 8 head `5b6d38a3`. Head `e803d94b3a11921a293cf036a8eda333d23828f9`, 4 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6590733082 (`receipts/taken.md`, `taken-url.txt`).

Sources, in this order:
- The manager's round 9 ruling: issue #833 issuecomment-6590477473. It is the authority for this round.
- R763-8: PR #834 issuecomment-6590465323, NEGATIVE: MINOR F1 and F2, RESIDUE R1 to R3; R764-6-S1 retained.
- R764-8: PR #834 issuecomment-6590467902, NEGATIVE: MINOR F1, RESIDUE R1, SUGGESTION S1.
- Both packets' scripts, run unchanged from copies of their published files. Every packet's `MANIFEST.sha256` checks OK (rounds 6, 7 and 8).

`scripts/owned_process.py` is byte-identical to `5b6d38a3` (and to `c1b29617`). No probe or mutant showed the product wrong.

## The findings, each with its change and control

Line numbers are at the head.

| Finding | IDs | Change at the head | Control: words | Evidence |
|---|---|---|---|---|
| No live new descendant beside a stopped shell; a resume beside one survived | R763-8-F1; ruling item 1(a) | `scripts/test_suite_cancellation.py:844-848`, "a live new descendant beside a stopped shell": the child's trap starts it as the child exits (from pass 2), it alone holds the shell, which is resumed at 3 s once it is gone | `resume-beside-new-live` (R763-8's edit): "a live new descendant beside a stopped shell's stated seconds were not kept" | `receipts/final/per-listing-reviewer.log`: red on that listing alone |
| No live new descendant with no cancelled shell | R764-8-F1; ruling item 1(b) | `:849-853`, "a live new descendant": a survivor's trap starts it; the survivor is spared to 4 s while it lives | `sigterm-to-live-new` (R764-8's edit) red on it; edge `live-new-sigtermed-with-no-shell` | `per-listing-reviewer.log`, `per-listing-edges.log` |
| No trap command listed inside grace after a resume later than 1 s | R763-8-F2; ruling item 1(c), late | `:854-860`: a zombie the stopped shell has not collected puts a pass a tick before 2 s; the resume is a pass before that (2 s less two ticks, pass 6), the trap's command, live or not, first listed in the last pass in grace (pass 7) | `sigterm-trap-command-after-resume-from-1.5s` (R763-8's edit): "a next-to-last in-grace resume and its trap command's ..." | `final/matrix-audit.log` runs 32, 33; `per-listing-reviewer.log` |
| Every in-grace new descendant was one the product sees as not live; two liveness mutants survived the whole test | R764-8-F1; ruling item 1(c), early | `:842-843`: every matrix cell with a trap command also has it live (pass 1, pass 2, and beyond the ruling every later class) | `sigterm-to-live-new`, `live-trap-command-unspared-after-in-grace-resume`: "a first-pass resume and its live trap command's ..." | `final/r764-8-live-probes.log`: both red on the whole test |
| Every round 8 reviewer mutant joins `MUTANTS` | ruling item 2 | `scripts/process_test_support.py:763-820`, named in rows 2, 5, 6, 7, 8 | item 2 table below | `final/same-edits-r8.log`: 13 of 13 byte for byte |
| The two interior reviewer mutants (green at round 8) | R764-8-S1 probes; ruling item 2 | `test_suite_cancellation.py:821-823`: a lone resume at 1 s and one at 10 s | "a lone one-second resume's ...", "a lone ten-second resume's ..." | `final/r764-8-probes.log`: all 8 red |
| Domain notes name the liveness cells | ruling item 3 | `docs/testing/TESTING.md:264-265` (the live column's preamble), `:268-275` (the matrix with a live column), `:280-290` (the lone resumes; the liveness cells tabled); rows 2-8 at `:295-301` | | `final/table-*.log` |
| An edge mutant per new cell | ruling item 3 | `process_test_support.py:821-886` | item 3 table below | `final/per-listing-edges.log`: each red on its own cell alone |
| The first pass's clock | R763-8-R1 | `TESTING.md:263`, the exact fix | | |
| The docstring's resume list | R763-8-R2 = R764-8-R1 | `test_suite_cancellation.py:752-753`, the exact fix, then "Alone, it is also resumed at 1 s and 10 s." | | |
| "the listing above" | R763-8-R3 | `test_suite_cancellation.py:813-815`, the exact fix | | |
| A cell read as a span | R764-8-S1: taken | `TESTING.md:262`, after the matrix's line 261: "A cell's domain is its listed resume, not the whole of its class." Reason: both the ruling and R764-8 read the matrix so; no row's claim changes | | |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1: retained, not taken | None. Reason: as in rounds 7 and 8, it predates this PR and is outside #833 | | |

### Interpretations made public

- **"late in grace, at the last in-grace pass"** (ruling item 1(c)) is read as the trap's command first listed in the last pass before 2 s, after a resume one pass earlier. A live command is listed only from the pass after the resume: a census before the `SIGCONT` cannot list it, and a live one listed in the resume pass would hold the resume. It is R763-8-F2's "latest edge" and its "more faithful shape". The pass a tick before 2 s needs a stated event at 2 s. A zombie the stopped shell has not collected is the one used: it holds nothing (the product's `live` excludes it), and its `SIGKILL` at 2 s is that event.
- **Beyond the ruling's three places,** every matrix cell with a trap command also has it live. So liveness crosses every class of resume, for the round 9 sweep the ruling announces.
- **"Every round 8 reviewer mutant"** includes R764-8's eight boundary probes, the two interior ones among them. They were green only for want of an interior listing. A lone resume at 1 s and one at 10 s turn them red. No other interior point is claimed; S1's sentence says a cell's domain is its listed resume.

## Item 1: the liveness axis

A live new descendant is a real process, `cat` reading a pipe the control holds open: `stated_liveness` at `test_suite_cancellation.py:830-860`. It is live until that pipe closes, at the `with`'s end (no signal), and never really signalled, as the starved owner's send only records. Every other new descendant is a number above the largest PID, which the product's `_live` sees as not live.

| Cell | Resume (pass, clock) | Live new descendant first listed | Words | Rows asserted |
|---|---|---|---|---|
| no cancelled shell | none | pass 2, 0.5 s | "a live new descendant" | 2 (no `SIGTERM`, `SIGKILL` at 2 s), 3 (survivor spared to 4 s), 4 (verdict at 14 s) |
| beside a stopped shell, before any resume | pass 9, 3 s | pass 2, 0.5 s, gone at 3 s | "a live new descendant beside a stopped shell" | 2, 5 (stopped while it lives, resumed in the first pass without it), 6, 7 |
| trap command, resume in pass 1 | 1, 0 s | 0.5 s, inside grace | "a first-pass resume and its live trap command" | 2, 3, 6, 8 |
| trap command, resume in pass 2 | 2, a tick | 0.5 s and a tick, inside grace | "a second-pass resume and its live trap command" | 2, 3, 6, 8 |
| trap command, resume a pass before the last in grace | 6, 2 s less two ticks | a tick before 2 s, inside grace, the last pass in grace | "a next-to-last in-grace resume and its live trap command" | 2, 3, 6, 8 |
| the same, not live | 6, 2 s less two ticks | a tick before 2 s | "a next-to-last in-grace resume and its trap command" | 2, 3, 6, 8 |
| trap command, resume in the last pass in grace | 6, a tick before 2 s | 2.5 s less a tick, past grace | "a last in-grace resume and its live trap command" | 3, 6, 8 |
| trap command, resume in the first pass past grace | 6, 2 s | 2.5 s | "a first past-grace resume and its live trap command" | 3, 6, 8 |
| trap command, the next pass | 7, a tick after 2 s | 2.5 s and a tick | "a second past-grace resume and its live trap command" | 3, 6, 8 |
| trap command, the last pass before 14 s | 31, a tick before 14 s | 14.5 s less a tick | "a last-pass resume and its live trap command" | 3, 6, 8 |

Every pass and clock above is from `receipts/final/matrix-audit.log` (runs 24 to 33). The new listings run after round 8's, so every earlier mutant keeps its words (`receipts/item1/mutants.log`: PASS 119/116).

Line budgets: `window` and the matrix's classes (`RESUME_MATRIX`) moved unchanged to `scripts/process_test_support.py:266-275`. `owner_stated_seconds` is 87 lines (limit 100) and `scripts/test_suite_cancellation.py` 997 lines (ratchet 1000); `process_test_support.py` is 970. `check_py_idiom` rc 0 at each commit.

## Item 2: every reviewer mutant published at round 8

| `MUTANTS` name | R763-8 name | R764-8 name | Finding | Row | Control: words | Red on, every listing checked |
|---|---|---|---|---|---|---|
| `resume-beside-new-live` | `r8-resume-beside-new-live` | | R763-8-F1 | 5 | `owner_stated_seconds`: "a live new descendant beside a stopped shell's ..." | that listing alone |
| `sigterm-trap-command-after-resume-from-1.5s` | `r8-sigterm-trap-command-after-late-grace-resume` | | R763-8-F2 | 6 | "a next-to-last in-grace resume and its trap command's ..." | both next-to-last cells |
| `sigterm-to-live-new` | | `sigterm-to-live-new` | R764-8-F1 | 2 | "a first-pass resume and its live trap command's ..." | 5 live listings |
| `live-trap-command-unspared-after-in-grace-resume` | | same | R764-8-F1 | 8 | the same | the 4 in-grace live cells |
| `live-trap-command-unspared` | | same (its control mutant) | R764-8-F1 | 8 | the same | the 7 live trap-command cells; also `owner_shell_window` |
| `interior-past-grace-no-window` | | same | R764-8-S1 | 7 | "a lone ten-second resume's ..." | that listing alone |
| `interior-in-grace-lone-shell-killed` | | same | R764-8-S1 | 7 | "a lone one-second resume's ..." | that listing alone |
| `grace-strictly-past` | | same | R764-8 probe | 2 | "a survivor's ..." | 19 listings |
| `no-window-at-grace-edge` | | same | R764-8 probe | 7 | "a lone first past-grace resume's ..." | the 3 first past-grace cells |
| `trap-command-spared-only-in-resume-pass-past-grace` | | same | R764-8 probe | 8 | "a late resume's ..." | 9 listings |
| `sigterm-new-beside-stopped-shell-late` | | same | R764-8 probe | 2 | "a new descendant's ..." | 4 listings |
| `resume-held-at-grace-edge` | | same | R764-8 probe | 5 | "a lone first past-grace resume's ..." | the 3 first past-grace cells |
| `verdict-from-grace-after-in-grace-resume` | | same | R764-8 probe | 6 | "a first-pass resume's ..." | 12 listings |

R763-8's two names drop the round prefix, as round 8 did for round 7's; `sigterm-trap-command-after-late-grace-resume` would sit beside round 7's `sigterm-trap-command-after-later-grace-resume`, so its edit's threshold names it. Each mutant is named in exactly one row, so R763-6's one-row check still reports only `windows-2s`.

## Item 3: domain notes and an edge mutant per liveness cell

| Cell | Mutant | Row | Breaks, only there | Words |
|---|---|---|---|---|
| live, no cancelled shell | `live-new-sigtermed-with-no-shell` | 2 | `SIGTERM` to a live new descendant when no shell is cancelled | "a live new descendant's ..." |
| live, beside a stopped shell | `resume-beside-live-new-past-grace` | 5 | a live new descendant no longer holds the stopped shell once grace is over | "a live new descendant beside a stopped shell's ..." |
| live trap command, pass 1 | `first-pass-live-trap-command-sigtermed` | 6 | `SIGTERM` to it, at the pass-1 edge | "a first-pass resume and its live trap command's ..." |
| live trap command, pass 2 | `second-pass-live-trap-command-sigtermed` | 6 | the same at pass 2 | "a second-pass resume and its live trap command's ..." |
| live trap command, a pass before the last in grace | `next-to-last-in-grace-live-trap-command-sigtermed` | 6 | `SIGTERM` to a live one after a resume in the last half-second of grace | "a next-to-last in-grace resume and its live trap command's ..." |
| the same, not live | `next-to-last-in-grace-trap-command-sigtermed` | 6 | the same for one not live | "a next-to-last in-grace resume and its trap command's ..." |
| live trap command, last pass in grace | `last-in-grace-live-trap-command-unspared` | 8 | the window of a live one first listed past grace after an in-grace resume | "a last in-grace resume and its live trap command's ..." |
| live trap command, first past grace | `first-past-grace-live-trap-command-unspared` | 8 | its window at the first past-grace edge | "a first past-grace resume and its live trap command's ..." |
| live trap command, next past grace | `second-past-grace-live-trap-command-unspared` | 8 | the same at the second | "a second past-grace resume and its live trap command's ..." |
| live trap command, last pass | `last-pass-live-trap-command-unspared` | 8 | the same within a pass of the verdict | "a last-pass resume and its live trap command's ..." |

`receipts/item3/per-listing-edges.log` (also `final/`): each new one is red on its own cell's listing and no other. Round 8's twelve are red on their class's cells, live or not; `last-in-grace-trap-command-unspared` (edge: any resume in the last half-second of grace) is also red on both next-to-last cells.

## Item 4: the RESIDUE, S1, and every reviewer probe at the head

The RESIDUE and S1 are in the findings table. The probes, each from its published copy, at a clean clone of the head (`$VALIDATION_STORAGE/833-a726i/wt-head`):

| Probe | Result | Receipt (`receipts/final/`) |
|---|---|---|
| R763-8 `r8_mutants.py` | both red on `owner_stated_seconds`; no survivor | `r8-mutants.*` |
| R763-8 `r8_feasibility.py` | `none` 37 listings green; each mutant red on its own listing and on this head's | `r8-feasibility.*` |
| R763-8 `probe_all_listings.py --classify` | 35 listings green | `r763-8-classify.*` |
| R763-8 `probe_mutants_all_listings.sh` | 47 mutants (its 24 and the 23 new), each red on at least one listing | `r763-8-mutants-all-listings.*` |
| R763-8 `probe_table.py`, `probe_byte_mapping.py` | no problems; 9 of 9 round 7 edits SAME | `r763-8-probe-table.*`, `r763-8-byte-mapping.*` |
| R764-8 `r764_8_probes.py` | `none` green; all 8 red, both interior ones included | `r764-8-probes.*` |
| R764-8 `r764_8_live_probes.py` | all 3 red on the whole test | `r764-8-live-probes.*` |
| R764-8 `r764_8_live_feasibility.py` | `none` green; both mutants red | `r764-8-live-feasibility.*` |
| R764-8 `r764_8_rename_check.py` | PASS, 9 published | `r764-8-rename-check.*` |
| R763-7 `r7_mutants.py`, R764-7 `rv7_mutants.py`, `row_mutants.py` | no survivor among 5, 4, 10 | `r7-mutants.*`, `rv7-mutants.*`, `row-mutants.*` |
| R764-7 `RV7_WHOLE=1` | stops at its own report line on the first red result (joins `None`), as in round 8; that run was red; `--matrix` has every whole-test column | `rv7-mutants-whole.*` |
| R763-6 `matrix.py` over its 8 `mktree.py` mutants | each red on a control and on the whole test | `r763-6-matrix.*` |
| R763-7 `pin_feasibility.sh`, `pin_feasibility_row2.sh` (trees by `grace_trees.py`) | as published: `none` green, each mutant red with its listing's words | `pin-feasibility*-r763-7.*`, `grace-trees.*` |
| R764-7 `rv7_pin_feasibility.py`, `stated_seconds_check.py` | PASS; both S2 mutants red | `rv7-pin-feasibility.*`, `stated-seconds-check.*` |
| `grace_resume_probe.py` (round 6) | PASS 5 of 5 | `grace-resume-head.*` |
| R763-7 `grace_resume_probe2.py` | PASS 3 of 3 at the head; FAIL 3 of 3 on `sigterm-to-new`, `sigterm-trap-commands`, `r7-sigterm-trap-command-later-grace-resume`, `sigterm-trap-command-after-later-grace-resume`, `sigterm-to-live-new`; PASS on `live-trap-command-unspared-after-in-grace-resume`, whose `SIGKILL` at 2 s comes after this probe's command has finished | `grace2-*` |
| R763-6 `slow_census.py` on `owner_shell_window` | `none` green at 0.15, 0.3, 0.5, 0.75 s a pass; its 8 mutants red at 0.15 and 0.5 | `slow-census/` |
| R764-6 `slow_shell_window.py campaign <head> 8 4 0.15,0.3,0.5` | PASS, 45 runs | `slow-shell-window.*` |
| R764-6 `sigcont_pending.py` | rc 0 | `sigcont-pending.*` |
| R763-6 `hup_ignored.py ... --mutants none --matrix` | rc 0, `none` green on all 11 | `hupign-head.*` |
| R763-6 `repeat.py`, R764-6 `repeat_controls.sh` | all green except `owner_report`, below | `stress-*`, `repeat-controls.*` |
| Table checks: R763-7 `table_check.py`, R764-7 and R764-6 `table_vs_mutants.py`, the lane's | rc 0 each | `table-*`, `item*/table_check.*` |
| R763-6 `table_vs_mutants.py` | rc 1 for `windows-2s` only, named in two rows, as R763-6 accepted at round 6 | `table-r763-6.*` |

Two probes needed a `scratch` directory beside their packet that the published packets do not ship (`rv7_mutants.py`, `slow_shell_window.py`). The first run of each stopped with `FileNotFoundError`; the rerun after `mkdir` is the receipt.

## An observation outside this round: `owner_report` under repetition

R763-6's `repeat.py` at the head: `owner_report` 63 of 64 green. The red: `AssertionError: ('state S', 'pid ... (python3) state R wchan hrtimer_nanosleep ...')`. Repeated 256 at a time, 16 at once, load about 42:

| Tree | Runs | Red |
|---|---:|---:|
| round 8 head `5b6d38a3` | 512 | 1 |
| this head | 512 + 64 (R763-6) + 64 (R764-6) | 3 |

The report is right each time: the child (`STUBBORN`, `time.sleep(0.02)` in a loop) was runnable when `_describe` read it, after the control's `eventually(... == "S")`. So it is the control's own race between that wait and the report, not the product. `owner_report` (`test_suite_cancellation.py:435-467`, last changed in `a25ee52d`) and `_describe` are unchanged in round 9. Every gate's run of it was green. It is disclosed in the PR body and REVIEW READY for a ruling, and not changed (touch nothing else). Receipts: `final/stress-owner_report*.log`.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `febf8b4b` | 1 | Add a liveness axis to the stated-seconds control: a live new descendant as the trap's command in every matrix cell, beside a stopped shell resumed only once it is gone and with no cancelled shell, and a trap command, live or not, listed in the last pass inside grace after a resume a pass earlier |
| `ba8019bd` | 2 | Add every reviewer mutant published at round 8 to MUTANTS with its published edit, each red on the stated-seconds control with its words and named in the row it breaks, and resume a lone shell at 1 s and at 10 s, where the two interior ones turn red |
| `58ba5b33` | 3 | Table the liveness cells in the testing guide and name them in each cleanup row's domain, and add an edge mutant per liveness cell, each red on that cell's listing alone and named in the row it breaks |
| `e803d94b` | 4 | Word the first pass's clock, the docstring's resumes and the matrix comment's listing exactly, and say once that a matrix cell's domain is its listed resume |

One per item, one-line subjects, empty bodies, no trailers. Before each commit (`receipts/item1/` to `item4/`): the quick gates (idiom, doc style, docs check, bare-metal scope, diff check), the table check, per listing at `none`, and the full `--mutants` campaign: 119/116, 132/129, 142/139, 142/139, each PASS.

## Cost

`final/cost.txt`, `final/inproc-cost.txt`, host load about 42 on 16 CPUs, round 8 head against this one, interleaved:
- `owner_stated_seconds` in one process, 20 calls a tree, 3 times: median 28.7 to 29.2 ms at round 8, 40.4 to 40.5 ms here;
- as its own process: 0.16 s at both; every other control within 0.1 s;
- the whole test, 4 runs each, 8 at once: mean 60.9 s at both.

**Round 9 adds about 11 ms to the preflight**, well under the 2 s allowed.

## Gates

All at head `e803d94b3a11921a293cf036a8eda333d23828f9`, one log and rc each, never piped.
- The lane gates ran on a fresh clean clone with `TMPDIR` in scratch (`receipts/gates/lane.sh`, round 8's with this head and this round's scratch); `tree-after.txt` is empty with `--ignored`.
- SIGHUP was at its default in every launcher: `SigIgn 0` for the lane gates, item checks, campaigns and probes; `0x4` (SIGQUIT only) for the docs.yml launcher, as in rounds 7 and 8 (`gates/sigign-docsyml.txt`, `final/matrix-part*.sigign`, each lane log's own `SigIgn` line).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's runner and verifier; only the venv and HOME paths point at this round's scratch (`gates/runner-vs-round1.diff`); `not_run.json` is round 1's, unchanged. Fresh venv, identical to round 8's freeze (`gates/venv-freeze-new.txt` = `requirements-round8.txt`), fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job (the no-git job has no `.git` to check, as before). Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. Jobs 00:51 to 01:37 | `gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml-jobs.txt`, `docsyml/`. `gate_41`'s log is over 200 KB: sha256 and size in `gates/LARGE-LOGS.txt`, tail in `docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `owner-stated-seconds` prints resumes `[0, 1, 3, 5.5, 14 - 2^-20]` and the matrix `[0, 2^-20, 2 - 2^-20, 2, 2 + 2^-20, 14 - 2^-20]` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants --jobs 4` | 0 | `owned-process mutants: PASS (142 mutants, 139 with a control that must fail)` | `gates/lane/mutants.*` |
| `--matrix` (every mutant on every control and the whole test), 4 parts, `--jobs 10` | 0 each | 1606 runs, no run cut. `none` green on all 11; each of the 139 red on its control with its words and on the whole test; the 3 with no control green on all 11 | `final/matrix-part1..4.*`, `final/matrix-table.md` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`; the log is 235,305 bytes, sha256 in `gates/LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` (also inside docs.yml) | 0 each | before each commit | `item*/quick/` |
| Full sweep | not run | Round 9 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

The PR body's command-table note still holds at this head: R764-1's `command_table_staleness.py` on the lane prints `pins 149 stale 34 absent 1` for `1f29f189` and `stale 38` for `d4d8cff9` and for this head (`final/command-table-staleness.log`).

## Incidents, no harm

- Every run set `TMPDIR` to scratch and ran with `-B` or `PYTHONDONTWRITEBYTECODE=1`. Nothing was signalled by name: the live process of the control ends when its pipe closes, and the probes' own children by their handles.
- The unit's memory peak was 8.0 GB, page cache included, under the 12 GB asked (during docs-gates-0).
- The probes' scratch snapshot of the head (`wt-head`, not the lane) gained an ignored `scripts/__pycache__` from one probe run; the lane's ignored `scripts/__pycache__`, `tb/verilator/gptp_shadow/__pycache__` and `sw/builder/out` predate this session (2026-11-02); nothing tracked changed.
- Nothing was pushed; no PR or issue text was edited.

## Files

- `PR-BODY.md`: round 8's published body with rounds 6 and 7 replaced by links to their archived bodies, as rounds 2 to 5 were, and a Round 9 section; the shared sections (status, roles, touched files, expected result, cost note) brought to this head.
- `receipts/`: `taken.md`; `item1/` to `item4/`; `final/` (probes, matrix, per listing, audit, cost at the head); `gates/` (lane gates, docs.yml); `tools/` (this round's probes and checks).

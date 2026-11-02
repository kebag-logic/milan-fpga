# #833 round 6 HANDOFF ([A726f])

Status: REVIEW READY, posted on #833 as issuecomment-6585270926 (`receipts/ready.md`). Base: round 5 head `a67eaf66`. Head `a987b601a0c10049321c18847504c4a94a862e04`, 6 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6582669797 (`receipts/taken.md`).

Sources, in this order:
- The manager's ruling: issue #833 issuecomment-6582585294. It is the authority for this round.
- R763-5: PR #834 issuecomment-6582577857, NEGATIVE.
- R764-5: issuecomment-6582542764, NEGATIVE.
- Both packets on `833-review-evidence` at `bc7e014c` (`receipts/review-evidence-fetch-head.txt`). Their probes ran unchanged, from a scratch export.

`scripts/owned_process.py` is byte-identical to `a67eaf66` and to `c1b29617` (`git diff --quiet`, rc 0). No probe or mutant showed the product wrong.

## The findings, each with its change and control

| Finding | IDs | Change at the head | Control | Evidence |
|---|---|---|---|---|
| The 61-pass hold had no upper bound on the owner's clock, so from about 0.17 s a pass the unmutated control reached its 10.4 s verdict first | R763-5-F3 (MAJOR; R764-5 has none) | `scripts/test_suite_cancellation.py:580-583`: `REAP_SECONDS=40.5`. Pass 61 is at most 30.5 s of owner clock at the cap, so the verdict at 40.9 s leaves the child 10.4 s after its SIGKILL. The lower bound, the resume past 1.2 s, is unchanged | `owner_shell_window` | `slow_census_probe.py`: head `a67eaf66` FAIL at 0.15 and 0.5 s. At `a987b601`, PASS at 0.15, 0.2, 0.3 and 0.5 s (14.0, 17.1, 23.6 and 36.6 s); 1.0 and 1.75 s PASS too. `none` green 6/6 and 24/24. Every listed mutant red 6/6 with its words: `shell-window-one-pass`, `shell-window-1s`, `shell-killed-when-resumed`, `no-shell-window` (M05), `-kept`, `-pass`, `no-trap-window`, `root-killed-unresumed` (M06) and `trap-commands-*`. Receipts: `item1/`, `final/slow-*`, `final/repeat-*` |
| The second stage, `TESTING.md:224` at `a67eaf66`, was unpinned for a parent whose child outlives SIGKILL | R763-5-F1 = R764-5-F1 (`rv-parent-spared-past-kill-all`) | `owner_stated_seconds` (`:784-829`), a stubborn-parent listing. The parent's SIGKILL comes in pass 9, 4 s; `parents-killed-at-grace` gives 5 and the spared mutant 29 | `owner_stated_seconds` | `kill_all_probe.py`: rc 0 at the head, rc 1 on both of R763-5's mutants. `probe_mutants.py`: `rv-parent-spared-past-kill-all` is red |
| `TESTING.md:219`, signals through the handle, was unpinned | R764-5-F1 (`rv-signal-by-number`; the ruling: must be pinned) | `owner_reused_identity` (`:833-885`): the entry's number names its own process until the recheck, and another process from then on. That process blocks SIGTERM, so a SIGTERM sent to it is pending at once in its status | `owner_reused_identity` | `signal-by-number` red: "a census entry was signalled by its number, after it changed hands" (also `probe_mutants.py`) |
| `TESTING.md:232`, a vanishing listing's 10 s, was unpinned from above | R764-5-F1 (`rv-vanishing-waits-30s-more`) | `owner_stated_seconds`, a vanishing listing: verdict in pass 49, 24 s. `starved_cleanup` takes the reap to use (`:757`) | `owner_stated_seconds` | `vanishing-waits-30s-more` (89) and `vanishing-waits-no-more` (29) red. `probe_effect.py`'s head row equals R764-5's own |
| `TESTING.md:277`, the report's parent and age, was checked by presence only | R763-5-F2 (R764-5 has none) | `owner_report` (`:435-467`): ` parent <pid> (first parent 1) ` as its own field, and an age between a 0.1 s pause before the description and the control's start | `owner_report` | `report_probe.py`: rc 0 at the head, rc 1 on both of R763-5's mutants. `report-without-current-parent` and `report-age-in-ticks` red |
| Comment | R764-5-R1 (RESIDUE) | `:799`, the exact fix: "It is never really signalled: this control's send only records the signal." | | |
| `TESTING.md:224`'s exception omitted the trap's commands | R763-4-X1 (RESIDUE, retained by both) | Merged into the table's second-stage row, as R763-5 asked: "...except a cancelled shell and any command its trap started, which keep the shell's own window" | | |
| The campaign inherits a launcher's ignored SIGHUP | R763-5-S1 (SUGGESTION) | Taken. `scripts/process_test_support.py:561-574`: under an ignored SIGHUP the campaign installs a no-op handler for its runs. A handler is reset at exec, so the runs get the default, and the campaign still outlives a hangup. A per-run reset in the child would need `preexec_fn` in a thread pool, which Python documents as unsafe | the campaign | Launched with SIGHUP ignored, `--mutants none --matrix`: `none / whole` red (hard-HUP timeout) at `ebe98b3a`, green at the head (`item5/hup-ignored-*`) |
| Mutants green on every control, product-comment behaviours only | R764-5-S1 (SUGGESTION) | Taken as a consequence of the rule that every published mutant is listed. Its three are in `MUTANTS` with no control and why, and they are the not-pinned list. The ones it found red on a control are listed with that control | | |

## Item 2: the table

`docs/testing/TESTING.md:255-289`:
- **The table (`:260-277`).** 16 rows: each stated cleanup behaviour, the owner controls that pin it, and the `MUTANTS` names that prove it.
- **What moved into it.** Every cleanup statement of the old prose (`:217-219`, `:223-235` at `a67eaf66`) and of the old control list (`:269-280`) is a row. Nothing was narrowed. `:217` now points to the table. "These cleanup intervals" (`:221`) became "Cleanup's intervals", since its antecedent moved.
- **Not pinned by a control (`:279-283`).** Three reasons the product's comments give, each with why no row changes. These are R764-5-S1's three.
- **The rule (`:285-289`).** "A stated cleanup behaviour is a row of this table; one that no control pins is on the list above, with the reason." Every published mutant is in `MUTANTS`, it names its control and words, and the table names it in the row it breaks. One that breaks no row names no control, and says why.

At item 2's own commit the four unpinned gaps were on the not-pinned list with their reasons. Item 3 moved each into its row.

Checked by `tools/table_check.py`, which parses the table: every mutant with a control is in a row whose controls include it, and none without one is in any row. At the head: 16 rows, 70 mutants named, 74 in `MUTANTS` (`final/`, `item4/table_check.log`).

`MUTANTS` gained 31 entries, 74 mutants and `none`, all 75 mutated texts distinct (`final/duplicates.log`):
- Item 2 (9): R763-5's and R764-5's mutants that the table's existing rows already catch, and the three with no control. Plus two of the lane's own for rows with no published mutant: `grace-1s` and `return-with-zombies`. The second needed `owner_late_exit` to assert the child is reaped before cleanup returns (`:522`).
- Item 3 (6): the five gaps' mutants.
- Item 4 (16): below.

Every round 5 reviewer mutant equals a committed entry by hash (`final/map-reviewer-mutants.log`): 15 published, 13 distinct.

## Item 4: the lane's own mutant for each row

Each is red on its control with its words in every campaign since item 4, and 3/3 in a dedicated repeat (`item4/own-*.log`). At the head's matrix each is also red on the whole test.

| Row | Mutant | Edit | Control: words |
|---|---|---|---|
| Handle | `check-before-open` | identity recheck before the handle is opened | `reused_identity`: "a census entry was signalled by its number" |
| SIGTERM, grace | `no-sigterm` | no SIGTERM | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Second stage | `kill-all-a-pass-late` | `clock < kill_all` -> `<=` | `stated_seconds`: "a stubborn parent's stated seconds were not kept" |
| 14 s | `verdict-past-deadline` | `clock >= limit` -> `>` | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Resume | `resume-only-when-alone` | resume only when nothing else is listed | `stated_seconds`: "a late resume's stated seconds were not kept" |
| Window, 20 s | `trap-window-from-grace` | window counted from grace | `stated_seconds`: "a late resume's stated seconds were not kept" |
| No SIGKILL in window | `shell-spared-only-while-stopped` | shell spared only in state `T` | `shell_window`: "the shell was killed in the pass that resumed it, before its trap" |
| Trap commands | `trap-commands-until-grace` | spared only until grace + 1 s | `shell_window`: "the resumed shell's trap command was killed inside the shell's window" |
| 0.5 s a pass | `cap-on-total` | cap on the total, not each pass | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Short passes | `first-pass-full-cap` | first pass charged the full cap | `stated_seconds`: "a survivor's stated seconds were not kept" |
| Vanishing | `vanishing-waits-from-grace` | verdict at grace + 20 s | `stated_seconds`: "a vanishing listing's stated seconds were not kept" |
| Collected, reaped | `verdict-counts-census` | verdict judges the census | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| Re-parented | `sigterm-needs-live-parent` | no SIGTERM while the census's parent is not live | `reparented`: "SIGTERM waited for a later census" |
| Late cancel | `resume-unless-reaped-now` | resume unless collected in this very pass | `late_cancel`: "a cancel after the shell was collected resumed it" |
| Failing run | `verdict-kills-only-the-killed` | verdict SIGKILLs only the already SIGKILLed | `survivor`: "stopped shell left behind" |
| Message | `report-parent-is-first-parent` | first parent printed as the current | `report`: "the report's current parent is not its own field" |

Run first against the item 3 controls, unchanged (`item4/pre.log`), two needed a change:
- **`resume-unless-reaped-now` was green.** That is a gap in `owner_late_cancel`: it modelled only a shell collected in the pass the cancel landed in. Its census now lists the shell, and its reap collects it, in the first pass only (`:696-738`). Each earlier `late_cancel` mutant stays red, and `none` is green 24/24 (`item4/late-cancel-repeat.log`).
- **`kill-all-a-pass-late` was red, with the late-resume listing's words.** `owner_stated_seconds` now asserts its stubborn-parent and vanishing listings before the late resume. The campaign shows no other mutant's words changed.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `d40a42ce` | 1 | Bound the shell-window control's hold from above too: a 40.5 s reap stage keeps its verdict past the child's 61 census passes at the 0.5 s cap |
| `5460d051` | 2 | List every stated cleanup behaviour in TESTING.md with the control that pins it and the mutants that prove it, and what no control pins with the reason |
| `151adbea` | 3 | Pin the five open cleanup gaps: a signal through the handle, a stubborn parent's SIGKILL at 4 s, a vanishing listing's 10 s, the report's current parent and age |
| `a25ee52d` | 3 (fix) | Take the report control's age pause before it sees the child asleep, so the child is still asleep when described |
| `ebe98b3a` | 4 | Add one more mutant of each table row, each red on its control; a cancel after the shell was collected in an earlier pass now opens no window either |
| `a987b601` | 5 | Say the stated-seconds control's child is never really signalled, and run every campaign run with SIGHUP at its default under a launcher that ignores it |

One-line subjects, empty bodies, no trailers. **Deviation, disclosed: six commits for five items.**
- Item 3 put `owner_report`'s new 0.1 s pause after its "child asleep" check. The child wakes every 20 ms, so it could be described in state `R`.
- Item 4's first campaign caught it once. A repeat measured it: 3 of 160 red, unmutated, at 16 jobs at `151adbea`, and 0 of 160 after the fix (`item3-fix/`).
- The fix was committed alone, with only that hunk staged, so item 4's commit stayed item 4. It was gated on a clean clone first: `--mutants` PASS, idiom, doc style, docs check, bare-metal and diff check rc 0.

`git diff --stat a67eaf66 HEAD`: `TESTING.md` +37 -33, `process_test_support.py` +112 -7, `test_suite_cancellation.py` +101 -25. `scripts/test_suite_cancellation.py` is 958 lines, under the 1000-line module ratchet.

## Cost

`final/cost.txt`: each control 3 times at `a67eaf66` and at the head, interleaved, at host load 50 to 80:
- `owner_report`: 0.21 to 0.31 s.
- `owner_reused_identity`: 0.11 to 0.16 s.
- Every other control is unchanged; `owner_shell_window` is 4.4 s at both.

The whole test, 4 runs each, 8 at once: mean 60.8 s at `a67eaf66`, 61.2 s at the head. **Round 6 adds about 0.2 s to the preflight**, well within the 2 s allowed.

## Gates

All at head `a987b601a0c10049321c18847504c4a94a862e04`, one log and rc each, never piped. The lane gates ran on a fresh clean clone with `TMPDIR` in scratch (`receipts/gates/lane.sh`); `tree-after.txt` is empty with `--ignored`. SIGHUP was at its default in every launcher (`gates/sigign.txt`: `SigIgn 0x4`, SIGQUIT only).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's `run_docs_yml.py` and `verify_docs_yml.py`; only the venv and HOME paths are pointed at this round's scratch (`gates/runner-vs-round1.diff`), and `not_run.json` is unchanged. Fresh venv, identical to round 1's freeze (`gates/venv-freeze-new.txt`), and a fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | `gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/`. `gate_41`'s log is over 200 KB: sha256 and size in `gates/LARGE-LOGS.txt`, tail in `docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`. `owner-stated-seconds: {... 'parent_kill_pass': 9, 'vanishing_verdict_pass': 49}`, `owner-reused-identity: {'signalled': False, 'through_handle': True}`, `owner-shell-window: {... 'trap_finished': True}` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants` | 0 | `owned-process mutants: PASS (74 mutants, 70 with a control that must fail)`. Also run at every item's commit (`item*/mutants*.log`). `--matrix` at the head: 825 runs in 3 parts, each rc 0 and PASS, none cut (`final/matrix-*.log`, `final/matrix-table.md`) | `gates/lane/mutants.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`. The log is 235,305 bytes: sha256 in `gates/LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` (also inside docs.yml) | 0 each | Run before each commit, on the working tree (`item*/quick*/`). They refused two things on the way, both fixed before their commit: a 124-column line, and `/proc` in a comment and a docstring (bare-metal scope) | |
| Reviewers' probes at the head | | `slow_census_probe.py` PASS at 0.15, 0.2, 0.3 and 0.5 s. `kill_all_probe.py` and `report_probe.py`: rc 0 at the head, rc 1 on each mutant. `probe_mutants.py` rc 0, and its F1 mutants red. R763-5's mutants red under `--matrix`. `probe_effect.py`'s head row equals R764-5's | `final/` |
| Full sweep | not run | Round 6 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

## Not taken

- R763-2-S2 (manager actions R763-1-S1/S2) and R763-2-S3 (the census-cost comment in `owned_process.py`): unchanged, on the manager's checklist; the product is not touched.
- No full sweep: round 6 changes only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1.

## Incidents, no harm

- Item 3's report-control flake, above. It was found by the lane's own campaign and fixed before any later item.
- Until item 5, my mutant and probe runs used the default temporary directory for their small, self-cleaning temp trees. From item 5 on, every run set `TMPDIR` to scratch, the gates included. My own scratch files were in scratch throughout.
- `/tmp/suite-cancellation-ii93o563` predates this session (17:22). It is not mine and was left alone.
- Nothing was signalled by name, and no process outside my own runs was signalled. The docs.yml runner ran in its own session.
- No `.pyc` was written to the lane: every run used `-B` or `PYTHONDONTWRITEBYTECODE`. The lane's ignored `scripts/__pycache__`, `tb/verilator/gptp_shadow/__pycache__` and `sw/builder/out` predate this session.
- This unit's memory stayed under 12 GB: `memory.peak` 8.1 GB with page cache, 0.5 GB anonymous when read.

## Files

- `PR-BODY.md`: round 5's body, with a Round 6 section and the status, roles, validation and limitation lines updated. It stays under GitHub's 65,536-character limit because two superseded tables became pointers to the same tables on `833-review-evidence`: round 5's mutation table and round 2's per-mutant tables.
- `receipts/`:
  - `taken.md`, `ready.md`, `review-evidence-fetch-head.txt`;
  - `tools/`: repeat, quick gates, table check, edit counter, appender, tabulator, cost, reviewer map, SIGHUP launcher;
  - `item1/` to `item5/`, `item3-fix/`, `final/` (probes, matrix, cost at the head), `gates/`.

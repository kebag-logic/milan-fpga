# #833 round 7 HANDOFF ([A726g])

Status: REVIEW READY, posted on #833 as issuecomment-6587935556 (`receipts/ready.md`, `ready-url.txt`). Base: round 6 head `a987b601`. Head `887fdd53b013cc8796c1d595644a2a9f0b8c27a5`, 5 commits on top, nothing pushed. TAKEN: issue #833 issuecomment-6585945735 (`receipts/taken.md`, `taken-url.txt`).

Sources, in this order:
- The manager's round 7 ruling: issue #833 issuecomment-6585868556. It is the authority for this round.
- R764-6: PR #834 issuecomment-6585788698, NEGATIVE: MINOR F1 and F2, RESIDUE R1 to R3, SUGGESTION S1 and S2.
- R763-6: PR #834 issuecomment-6585853678, NEGATIVE: MINOR F1, RESIDUE X1 to X4, SUGGESTION S1.
- Both packets on `833-review-evidence` at `589b13ed`. Their probes ran unchanged, from a scratch export.

`scripts/owned_process.py` is byte-identical to `a987b601` (and to `c1b29617`). No probe or mutant showed the product wrong.

## The findings, each with its change and control

| Finding | IDs | Change at the head | Control | Evidence |
|---|---|---|---|---|
| Row 1 was pinned for `SIGTERM` only: `SIGKILL` or `SIGCONT` by number survived | R764-6-F1 (MINOR); ruling item 1 | `scripts/test_suite_cancellation.py:876-924`: `owner_reused_identity` hands the number over for `SIGTERM` and then for `SIGKILL` (`:896`), each with a fresh entry process, and the stale-start check runs for both. `BLOCKING` (`:861`) blocks `SIGTERM` and `SIGCONT`; a `SIGKILL` stays pending until its target is collected. So any of the three sent by number is pending at once (`:911`) | `owner_reused_identity`: "a census entry was signalled by its number, after it changed hands: ['SIGKILL']" (or `['SIGCONT']`) | `rv6-sigkill-by-number`, `rv6-sigcont-by-number` in `MUTANTS` (`process_test_support.py:508-515`), named in row 1. R764-6's `row_mutants.py` at the head: both red, no survivor among its 10 (`final/row-mutants.log`). `final/sigkill-pending.log`: 200 of 200 runs show the `SIGKILL` bit in every sample until the target is collected, in states R, D and Z |
| Row 5 was pinned only for a resume at 5.5 s | R764-6-F2 (MINOR); ruling item 2 | `owner_stated_seconds` (`:793-857`) resumes the shell in the first pass, with nothing else ever live, inside grace (`:841`) | `owner_stated_seconds`: "a first-pass resume's stated seconds were not kept" | `rv6-resume-not-before-grace`, `rv6-resume-not-first-pass` (`process_test_support.py:516-521`), named in row 5; both red, as is R764-6's own run of them |
| Rows 6 and 8 claimed a resume inside grace and its trap's command, and not-pinned item 2 gave a false reason | R763-6-F1 (MINOR); ruling item 2 | The first-pass listing lists the trap's command from the second pass, inside grace: no `SIGTERM` to it, `SIGKILL` only 10 s after the resume. A second listing (`:843-846`) has a survivor's trap start a cleanup command with no shell resumed: no `SIGTERM` to it either. Row 2 states that a descendant new since the first census gets none, row 6 that the trap's command gets none even inside grace. Not-pinned item 2 is gone: all of it is pinned | `owner_stated_seconds`: "a first-pass resume's ..." and "a new descendant's stated seconds were not kept" | `sigterm-to-new` now names `owner_stated_seconds` (`:429`); `rv6-sigterm-trap-commands` (`:522`) and `sigterm-to-new-before-resume` (`:526`, the lane's, the other half of `sigterm-to-new`). R763-6's `grace_resume_probe.py` at the head: PASS 3 of 3; FAIL 3 of 3 on `sigterm-to-new`, `rv6-sigterm-to-new` and `rv6-sigterm-trap-commands` (`final/grace-resume-*`) |
| Each row needs a note of the domain its controls cover, equal to what it states | R764-6-S2 (required by the ruling) | `TESTING.md:255-279`: the "Pinned by" cell names, for each control, the domain it covers. `:257-260` say so. Where a domain fell short of its row, the control was widened, never the row narrowed: see "Item 3" below | | Every row's domain is checked by an edge mutant (item 4) |
| Row 1 wording | R764-6-R1 (RESIDUE) | `TESTING.md:264`, the exact fix | | |
| Rows 12 and 15 wording | R764-6-R2 (RESIDUE) | `TESTING.md:275`, the sentence appended; `:278`, "every descendant it reports that it has not collected" | | |
| Row 10 listed `owner_shell_window` but no mutant named it | R764-6-R3 (RESIDUE) | The first exact fix: `owner_shell_window` dropped from row 10. Reason: its real passes count their own length only while the host keeps them short, so a row-10 mutant there would be red only under light load (a candidate, `pass-floor-cap`, is red there today, `item4/edge-screen.log`); `owner_stated_seconds` covers the row's whole domain with no timing | | |
| A return before a confirming census | R763-6-S1 (SUGGESTION, taken) | `rv6-return-before-confirm` (`process_test_support.py:583`), named in row 12; row 12 lists `owner_vanishing` with its domain | `owner_vanishing`: "an endless listing did not fail the run" | red at the head (`gates/lane/mutants.log`) |
| The direct preflight under a launcher that ignores SIGHUP | R764-6-S1 (SUGGESTION, not taken) | None. Reason: the HUP stops it trips are on base `1f29f189`, so it predates this PR, and R764-6 itself places it out of #833's scope. Fixing `main()` would change preflight behaviour this Issue does not cover. Suggested for a new Issue | | |
| R763-6-X1 to X4 | RESIDUE | Not taken: not in this round's list, so left to the manager's residue checklist. X1 and X3 overlap R764-6-R1 and R2, whose exact text is applied | | |

## Item 3: the domain notes, and where a domain fell short

`owner_stated_seconds` was widened, in `:742-857`:
- **The clock lands a tick (2^-20 s) short of each stated time, then on it.** Every time in a listing's expected events is approached that way. So the pass before each stated time is a tick early, and a stated time held a tick early or late is red. On the old clock, which moved in half-second passes, a grace or window anywhere in the half second below its stated time was green.
- **Its passes span the clock rows' domains.** Passes that stall are a tick over the cap or an hour long, alternately. Passes shorter than the cap are a tick, or half a second less a tick. `final/clock-audit.log` shows, for each of its ten runs, a pass a tick before and a pass on every stated time.
- **Resumes cover row 5's and row 6's domain:**
  - in the first pass;
  - at 3 s, between grace and 4 s;
  - at 5.5 s;
  - a tick before 14 s, which is the last pass before a survivor's verdict, so the deadline is a tick before 34 s;
  - never, while the child outlives 14 s.
- **Rows 11 and 15.** A listing that dies inside every census after the last-pass resume gets its verdict a tick before 44 s. Every verdict sends `SIGKILL` to each listed descendant not collected.
- **Expected events are in seconds, not pass numbers.** Each listing's words are unchanged, and the new listings are checked after the old ones. So every earlier mutant keeps its words (`item3-pre/mutants.log`).

Row 16's "how long ago it was sent `SIGKILL`" was pinned only for `_describe`'s format. Item 4's `killed-ago-from-start` (the age counted from cleanup's start) survived every control (`item4/edge-screen.log`). A starved verdict now must report its real child's wall time since that child's first `SIGKILL` (`:770-786`). It is deterministic, on the fake clock: "sent SIGKILL 36007.00 s ago".

`scripts/test_suite_cancellation.py` is 994 lines, under the 1000-line module ratchet. The old `starved_clock` context manager is folded into `starved_cleanup` to stay under it.

## Item 4: the lane's own mutant at the edge of each row's domain

`TESTING.md`'s table names each in its row. Each is red on its control with its words in the head's campaign, and on the whole test in `--matrix` (`final/matrix-new.log`, `final/matrix-new-table.md`). They were screened first against all ten controls (`item4/edge-screen.log`, with `tools/edge_mutants.py`), where only `killed-ago-from-start` survived; it is now pinned, above.

| Row | Edge | Mutant | Control: words |
|---|---|---|---|
| 1 | the last signal | `sigcont-by-number-after-kill`: `SIGCONT` by number after `SIGKILL` only | `reused_identity`: "a census entry was signalled by its number" |
| 1 | the other signal, before the open | `recheck-spares-sigkill`: start time not rechecked for `SIGKILL` | `reused_identity`: "a census entry whose process was replaced was signalled" |
| 2 | 2 s, from below | `grace-a-tick-short`: grace 2 s less two ticks | `stated_seconds`: "a survivor's stated seconds were not kept" |
| 3 | 4 s, from below | `kill-all-a-tick-early`: the second stage two ticks early | `stated_seconds`: "a stubborn parent's ..." |
| 4 | 14 s, from below | `verdict-a-tick-early` | `stated_seconds`: "a survivor's ..." |
| 4 | the shell never resumed | `verdict-waits-for-resume`: no verdict while a cancelled shell waits | `stated_seconds`: "cleanup never reached a verdict on the owner's clock" |
| 5 | the last pass | `no-resume-before-verdict`: no resume within a pass of the verdict | `stated_seconds`: "a last-pass resume's ..." |
| 6 | 10 s, from below | `trap-window-a-tick-short` | `stated_seconds`: "a late resume's ..." |
| 7 | the first pass, inside grace | `no-window-inside-grace`: no window for a resume before grace ends | `stated_seconds`: "a first-pass resume's ..." |
| 8 | the first pass, inside grace | `trap-commands-spared-only-past-grace` | `stated_seconds`: "a first-pass resume's ..." |
| 9 | the slowest pass | `cap-lifted-past-a-minute`: a pass over a minute counts in full | `stated_seconds`: "a survivor's ..." |
| 10 | the shortest pass | `tick-passes-count-nothing`: a pass under a millisecond counts nothing | `stated_seconds`: "a survivor's ..." |
| 11 | after the last-pass resume | `vanishing-verdict-ignores-resume`: the vanishing verdict fixed at 24 s | `stated_seconds`: "a resumed vanishing listing's ..." |
| 12 | the first pass | `no-reap-after-first-census` | `late_exit`: "CLEANUP FAILED: owned descendants remain" |
| 13 | the other signal | `sigterm-rechecks-parent`: the current parent rechecked before `SIGTERM` | `reparented`: "SIGTERM waited for a later census" |
| 14 | a later pass | `resume-collected-shell-past-grace` | `late_cancel`: "a cancel after the shell was collected resumed it" |
| 15 | the other signal | `verdict-sends-sigterm` | `stated_seconds`: "a survivor's ..." |
| 16 | the `SIGKILL` age's origin | `killed-ago-from-start` | `stated_seconds`: "not in the report" |

Rows 7, 8, 15 and 16 now list `owner_stated_seconds` too, which these mutants name.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `9cfabae4` | 1 | Pin every signal _send sends to the handle: the reused-identity control hands the number over for SIGTERM and SIGKILL, and sees SIGCONT too |
| `6a39abb6` | 2 | Resume the cancelled shell in its first pass, inside grace, in the stated-seconds control: its trap's command gets no SIGTERM, and nor does a new descendant before a resume |
| `d2f438f5` | 3 | Give each cleanup table row the domain its controls cover, and widen the stated-seconds control to it: each time to a tick, resumes from the first pass to the last before 14 s |
| `b2f875b8` | 4 | Add a mutant of each cleanup table row at the edge of its domain, each red on its control; a starved verdict must report a real process's wall time since its SIGKILL |
| `887fdd53` | 5 | Word the cleanup table's handle, collection and kill-before-fail rows exactly, pin a return before a confirming census on the vanishing control, and drop the shell-window control from the short-pass row |

One per item, one-line subjects, empty bodies, no trailers. Before each commit: idiom, doc style, docs check, bare-metal scope, diff check, the table check, and the full `--mutants` campaign (`item*/`).

The reviewers' mutants keep their published names (`rv6-*`), as the ruling and this round's brief name them, so each matches the reviewer's own by name as well as by edit. Round 6 had dropped the `rv-` prefix instead.

`MUTANTS`: 74 to 99 mutants (25 new; `sigterm-to-new` gained a control), 96 with a control. The table names all 96. The 3 with no control are in no row: `sigterm-checks-parent` (equivalent) and the two not-pinned items' mutants.

## Cost

`final/cost.txt`: each control 3 times at `a987b601` and at the head, interleaved, host load 42 to 45.
- Every control is unchanged within 0.06 s: `owner_stated_seconds` 0.16 s and `owner_reused_identity` 0.16 to 0.17 s at both.
- The whole test, 4 runs each, 8 at once: mean 63.5 s at both.

**Round 7 adds no measurable time to the preflight.**

## Gates

All at head `887fdd53b013cc8796c1d595644a2a9f0b8c27a5`, one log and rc each, never piped. The lane gates ran on a fresh clean clone with `TMPDIR` in scratch (`receipts/gates/lane.sh`); `tree-after.txt` is empty with `--ignored`. SIGHUP was at its default in every launcher: `SigIgn 0` for the lane gates, `0x4` (SIGQUIT only) for the detached docs.yml launcher (`gates/sigign.txt`).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's runner and verifier, as copied in round 6; only the venv and HOME paths point at this round's scratch (`gates/runner-vs-round6.diff`), `not_run.json` unchanged. Fresh venv, identical to round 1's freeze (`gates/venv-freeze-new.txt`), fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job. Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN` | `gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml/`. `gate_41`'s log is over 200 KB: sha256 and size in `gates/LARGE-LOGS.txt`, tail in `docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; `owner-stated-seconds: {'grace': 2, 'verdict': 14, 'parent_kill': 4, 'vanishing': 24, 'resumes': [0, 3, 5.5, 13.999999046325684], ...}`, `owner-reused-identity: {'signalled': False, 'through_handle': ['SIGTERM', 'SIGKILL', 'SIGCONT']}` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants --jobs 4` | 0 | `owned-process mutants: PASS (99 mutants, 96 with a control that must fail)`. Also at every item's commit (`item*/mutants*.log`; item 5's two load-flake runs are below). `--matrix` at the head in 4 parts (`final/matrix-new.log`, `matrix-old-1..3.log`), each rc 0 and PASS, no run cut: `none` green on all 11, each of the 96 red on its control with its words and on the whole test, the 3 with no control green on all 11 (`final/matrix-table.md`) | `gates/lane/mutants.*` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`; the log is 235,305 bytes, sha256 in `gates/LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` (also inside docs.yml) | 0 each | Before each commit, on the working tree (`item*/quick/`). The idiom gate refused one 122-column line on the way, wrapped before item 2's commit | |
| Reviewers' probes at the head, unchanged | | `row_mutants.py` (R764-6): its 10 mutants all red, no survivor (`final/row-mutants.log`). `grace_resume_probe.py` (R763-6): PASS 3 of 3 at the head; FAIL 3 of 3 on `sigterm-to-new`, `rv6-sigterm-to-new` and `rv6-sigterm-trap-commands`, each tree built by its `mktree.py` (`final/grace-resume-*`). `sigcont_pending.py`: rc 0. `table_vs_mutants.py`: R764-6's rc 0; R763-6's rc 1 for `windows-2s` only, in two rows, which R763-6 accepted at round 6 | `final/` |
| Full sweep | not run | Round 7 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

## Incidents, no harm

- **Item 5's own campaign hit two load flakes on the unchanged real-time control `owner_shell_window`.**
  - At load 91, `trap-commands-1s` was green: the run took 8.5 s, against about 4 s.
  - At load 102, `shell-window-one-pass` was red, but with the trap-command words instead of its own.
  - Both mutants and the control are as at `a987b601`.
  - The cause is the census pass time. A pass over about 0.75 s makes a 1 s window take longer in wall time than the trap's 1.5 s command. A shell starved before it forks its command is killed with no child to spare it.
  - Logs: `item5/mutants-run1-load91.log`, `item5/mutants-run2-load102.log`.
  - At load 25 to 42, all three are red 8 of 8 with their words (`final/load-repeat-shell-window.log`). The gate at the head, at `--jobs 4`, is PASS.
  - Not changed: outside this round's items. Both mutants are also red, deterministically, on `owner_stated_seconds` (the late-resume listing), so naming that control would make the campaign immune to load. That is a decision for the manager.
- Every run set `TMPDIR` to scratch. One inline check at 20:41, run without `-B`, rewrote three `.pyc` files in the lane's ignored `scripts/__pycache__` (`owned_process`, `process_test_support`, `test_suite_cancellation`). That directory and its other files predate this session. Nothing tracked changed, and the gates ran on a clean clone.
- `final/matrix-old-1-run1-load90.log`: the first run of matrix part 1 failed only because `trap-commands-1s` was green on `owner_shell_window` as load rose to 90. Its re-run is `matrix-old-1.log`, PASS.
- The unit's memory peak was 8.0 GB, page cache included, under the 12 GB asked.
- Nothing was signalled by name.
- SIGHUP was at its default in this unit (`SigIgn 0`) and in the detached docs.yml launcher (`SigIgn 0x4`, SIGQUIT only).

## Files

- `PR-BODY.md`: round 6's body with a Round 7 section; round 6's two superseded tables now point to their copy on `833-review-evidence`.
- `receipts/`: `taken.md`; `item1/` to `item5/`, `item3-pre/`; `final/` (probes, matrix, cost at the head); `gates/` (lane gates, docs.yml); `tools/`.

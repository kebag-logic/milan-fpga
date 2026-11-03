# #833 round 10 HANDOFF ([A726j])

Status: REVIEW READY, posted on #833 as issuecomment-6594752309 (`receipts/ready.md`, `ready-url.txt`).

Base: round 9 head `e803d94b`. Head `fce77f0efc1425ef7732a8d70c02addc108f7afe`, 6 commits on top, one per item, nothing pushed. TAKEN: issue #833 issuecomment-6593124267 (`receipts/taken.md`, `taken-url.txt`).

Sources, in this order:
- The manager's round 10 ruling: issue #833 issuecomment-6592794168. It is the authority for this round.
- R763-9: NEGATIVE: MINOR F1 and F2, MAJOR F3, RESIDUE R1, SUGGESTION S1; R764-6-S1 retained.
- R764-9: NEGATIVE: MINOR F1 (= R763-9-F3), SUGGESTION S1 and S2.
- Every reviewer packet from rounds 6 to 9, copied fresh with links dereferenced and checked against its `MANIFEST.sha256`: all 8 OK (`receipts/final/r9-sweeps/*.manifest-check.txt`).

`scripts/owned_process.py` is byte-identical to `e803d94b` and to `c1b29617`. No probe or mutant showed the product wrong.

## The findings, each with its change and control

Line numbers are at the head. TSC is `scripts/test_suite_cancellation.py`, PTS `scripts/process_test_support.py`, the guide `docs/testing/TESTING.md`.

| Finding | IDs | Change at the head | Control: words | Evidence |
|---|---|---|---|---|
| `owner_report` fails by chance under load (its child woke every 20 ms) | R763-9-F3 = R764-9-F1; ruling item 1 | TSC:441-442, R763-9-F3's exact fix byte for byte: the child writes its PID and waits in `signal.pause()`. `STUBBORN` unchanged | `owner_report`; its 6 mutants red with their words | `receipts/item1/`: 0 of 15,200 against the round 9 head's 33 of 15,200 beside it, load 41 to 78, Fisher p = 1.1e-10 |
| No listing listed a new descendant before 0.5 s | R763-9-F1; ruling item 2 | PTS:294-295, 307 (a stated census is a pass placed and noted); TSC:776-787 (`kept` keeps a listing whose census grows after the first pass again early); guide:261, 297-309, rows 2 and 6 (:314, :318) | `early-new-sigtermed-0.25`, `-0.5`, `early-trap-command-sigtermed`: "an early first-pass resume's ..."; `early-live-new-sigtermed`: "an early first-pass resume and its live trap command's ..." (PTS:882-897) | `item2/per-listing-early.log`, `final/r9-sweeps/r763-9-per-listing.log`: red on 8, 8, 2 and 5 early listings, no other |
| No listing had a live new descendant beside a shell never resumed | R763-9-F2; ruling item 3 | TSC:866-872, R763-9-F2's preferred listing and event list; guide:291, 308, rows 3 and 4 (:315, :316) | `parent-of-live-new-unspared-beside-shell`, `verdict-early-live-new-beside-stopped-shell`, edge `parent-under-unresumed-shell-unspared`: "a live new descendant beside a shell never resumed's ..." (PTS:898-912) | `item3/per-listing-f2.log`, `final/r9-sweeps/r763-9-f2-feasibility.log` |
| R764-9-S1's three listings | R764-9-S1; ruling item 4 | TSC:847 (the live trap command after the 1 s resume); TSC:866-872 (item 3's listing; a parent beside the shell, not under it); guide:292-293, 309; rows 2, 6, 8 drop "not live" at 1 s (:314, :318, :320); row 3 (:315) | R764-9's sweep mutants | `final/r9-sweeps/cell-sweep.log`: 9 survivors of round 9 now red |
| The listing-time domain | R763-9-S1; ruling item 5 | guide:262, its exact sentence | | |
| The printed summary | R763-9-R1 = R764-9-S2; ruling item 6 | TSC:831-832, R763-9-R1's exact keys | | `gates/lane/test_suite_cancellation.log` |
| R764-9-S2 | at judgement: taken through R1 | Reason: it asks for the same three facts as R1's exact fix | | |
| R764-6-S1 | retained, not taken | Reason: as in rounds 7 to 9, it predates this PR and is outside #833 | | |

### Interpretations made public

- **"A new descendant first listed a tick after the first pass"** is placed by a census a listing states. `starved_cleanup` lands a pass on a stated census and notes it among the events, so the listing's own `events == stated` proves the pass was placed. No other listing's schedule changes.
- **Which listings are early is a rule, not a list:** `kept` keeps again, early, every listing whose census lists at a tick what its first census did not. The anchored lines reviewer probes patch (`kept("a first-pass resume", ...)`, the not-live matrix line, the `starved_cleanup` call, the assert, the survivor comment, `print("owner-stated-seconds: "`) stay byte-identical, so "an early first-pass resume" comes from that rule too. The rule makes 8 early listings; a reviewer probe that adds a listing gets its early one by the same rule.
- **"Named in rows 2 and 6"** is read as each of the four in both rows: each breaks row 2's new descendant and row 6's trap command. R763-6's one-row check therefore reports them beside `windows-2s`.
- **R764-9-S1's third listing** is a parent beside the stopped shell, not under it: item 3's listing already has the shell's own child as the spared parent. Both share one loop (TSC:866-872).
- **The 1 s live cell** joins the live matrix loop as one more entry, so it is listed exactly as the matrix's cells are.
- **No mutant beyond those the ruling names joins `MUTANTS`:** the four early ones, both F2 ones and one edge mutant. The sweeps' own mutants stay in their packets.

## Item 1: `owner_report`

| Driver | Fix (round 9 head + item 1) red | Round 9 head red | Host load |
|---|---:|---:|---|
| `tools/stress_report.py`, 8 busy loops of this unit | 0 / 3000 | 3 / 3000 | 41.2 to 57.5 |
| the same, 16 busy loops | 0 / 3000 | 5 / 3000 | 54.8 to 68.7 |
| the same, 24 busy loops | 0 / 3000 | 5 / 3000 | 66.4 to 78.0 |
| R763-9 `stress_owner_report.py <tree> 3000 8`, side by side | 0 / 3000 | 12 / 3000 | 48.5 at the end |
| R764-9 `repeat_control.sh <tree> owner_report 16 200`, side by side | 0 / 3200 | 8 / 3200 | mean 54.9 |

Totals 0 / 15,200 against 33 / 15,200 (`item1/stress-stats.txt`). Every red: `('state S', '... state R wchan hrtimer_nanosleep | 0 ...')`. At the final head: R763-9's driver 0 / 3000 and R764-9's 0 / 3200, with 16 busy loops, load 34.8 to 50.1, mean 44.2 (`final/r763-9-stress-final-head.log`, `r764-9-repeat-final-head.log`). The six `owner_report` mutants: red with their words once and in 20 more campaigns (`item1/report-mutants*.log`); the child's wchan now reads `__do_sys_pause`.

## Item 2: the early edge

`receipts/item2/classify-r9.txt` against `classify-item2.txt`: round 9's 35 listings classify identically (resume pass and clock, first new-descendant census); 6 early listings added, each first listing its new descendant at a tick (9.5e-07 s). Items 3 and 4 add two more by the same rule. R763-9's `audit_new_in_grace.py` at the head: 8 listings list one at a tick (`final/r9-sweeps/r763-9-audit-new-in-grace.txt`).

The four mutants are R763-9's `natural.py` edits byte for byte (`item2/`, item checks). Every listing checked: `-0.25` and `-0.5` red on the 8 early listings, `early-trap-command-sigtermed` on the 2 early first-pass ones, `early-live-new-sigtermed` on the 5 early live ones, and none on any other.

## Room under the module ratchet

`check_py_idiom.py` counts a module over 1000 lines as "long module", budget 10, measured 10: no slack, and both modules were at 997 and 970 before this round. Item 2's commit makes room without changing a value:
- `BLOCKING` moves unchanged from TSC to PTS:264-271, and is imported;
- 17 `MUTANTS` entries' words continue at the dict's 8-space indent, as its edits already do, where that saves a line (`tools/rewrap_words.py`, which refuses unless the dict is identical value for value and nothing outside it changed).

`tools/values_check.py` at items 2, 3 and 4 (`item*/values-check.log`): every round 9 entry identical and in order, the new ones appended, `BLOCKING` byte-identical. Final sizes: TSC 999, PTS 996; `owner_stated_seconds` and `stated_liveness` under 100 lines.

## Item 6: every reviewer probe and sweep, at the head

Run from the fresh packet copies, unchanged, at a clean clone of the head (`$VALIDATION_STORAGE/833-a726j/wt-head`); the round 9 sweeps ran on a snapshot whose tree is identical to the head's (`diff -r`), before item 6 was committed.

| Probe | Result | Receipt (`receipts/final/`) |
|---|---|---|
| R763-9 `sweep.py`, 4224 mutants, in 7 chunks | 2716 equivalent, 1107 killed, 401 survivors (440 at round 9). Every F1 and F2 variant killed. Its `classify.py`: 12 classes touch a listed cell, its own round 9 out-of-domain classes (6 `five-half`, 6 between sampled passes); with this round's two new cells claimed, the same 12 | `r9-sweeps/sweep-*.log`, `classified-*.txt`, `LARGE-LOGS.txt` |
| R764-9 `cell_sweep.py`, 99 mutants | 24 survive every control and the whole test (33), 1 more red only on `owner_shell_window`; 9 killed since round 9; none new; the 24 are its own 6 equivalent and 18 out-of-domain | `r9-sweeps/cell-sweep.*` |
| R764-9 `cell_sweep.py --author` | every `MUTANTS` entry mapped on 46 listings; those red on none have another control | `r9-sweeps/author-cellmap.*` |
| R763-9 `natural.py` | all 6 survivors killed, each red on `owner_stated_seconds` and the whole test | `r9-sweeps/r763-9-natural.*` |
| R763-9 `probe_cells.py`, `f2_feasibility.py`, `per_listing.py`, `table_check.py`, `bytecheck*.py`; R764-9 `byte_match.py` | 65 of 65; both F2 mutants red with or without its listing; `none` 0 of 46; no problem; 11 + 3 SAME; 13 of 13 | `r9-sweeps/` |
| R763-8 `r8_mutants.py`, `r8_feasibility.py`, `probe_all_listings.py --classify`, `probe_table.py`, `probe_byte_mapping.py` | both red; as published (`none` 0 of 49); 46 green; no problems; 9 of 9 | `r8-*`, `r763-8-*` |
| R763-8 `probe_mutants_all_listings.sh`, round 9's 47 names | each red on at least one of 46 listings | `r763-8-mutants-all-listings.*` |
| R764-8 `r764_8_probes.py`, `_live_probes.py`, `_live_feasibility.py`, `_rename_check.py` | all red; all 3 red on the whole test; as published; PASS | `r764-8-*` |
| R763-7 `r7_mutants.py`, R764-7 `rv7_mutants.py`, `row_mutants.py` | no survivor among 5, 4, 10 | `r7-mutants.*`, `rv7-mutants.*`, `row-mutants.*` |
| R764-7 `RV7_WHOLE=1` | stops at its own report line on the first red run, which was red, as in rounds 8 and 9 | `rv7-mutants-whole.*` |
| R763-6 `matrix.py` over its 8 `mktree.py` mutants | each red on a control and on the whole test | `r763-6-matrix.*` |
| R763-7 `grace_trees.py`, `pin_feasibility.sh`, `pin_feasibility_row2.sh`; R764-7 `rv7_pin_feasibility.py`, `stated_seconds_check.py` | as published: `none` green, each mutant red with its listing's words; PASS; both red | `grace-trees.*`, `pin-feasibility*`, `rv7-pin-feasibility.*`, `stated-seconds-check.*` |
| `grace_resume_probe.py`; R763-7 `grace_resume_probe2.py` | PASS 5 of 5; PASS 3 of 3 at the head and on `live-trap-command-unspared-after-in-grace-resume`, FAIL 3 of 3 on the five `SIGTERM` mutants | `grace-resume-head.*`, `grace2-*` |
| R763-6 `slow_census.py` on `owner_shell_window` | `none` green at 0.15, 0.3, 0.5, 0.75 s; 15 of its 16 mutant runs red; see below | `slow-census/` |
| R764-6 `slow_shell_window.py campaign <head> 8 4 0.15,0.3,0.5`, `sigcont_pending.py` | PASS, 45 runs; rc 0 | `slow-shell-window.*`, `sigcont-pending.*` |
| R763-6 `hup_ignored.py ... --mutants none --matrix` | rc 0, `none` green on all 11 | `hupign-head.*` |
| R763-6 `repeat.py` (4 controls x 64), R764-6 `repeat_controls.sh` | all green, `owner_report` 64 + 64 | `stress-*`, `repeat-controls.*` |
| Table checks: R763-7, R764-7, R764-6; R763-6 | rc 0 each; R763-6 rc 1 for `windows-2s` and the four early mutants, each named in two rows | `table-*` |

Disclosed:
- **R763-6's slowed census, `trap-commands-1s` at 0.5 s a pass: green once** (42.5 s, beside the docs.yml jobs); 6 repeats red with the words in 36.5 s (`slow-census/repeat-trap-commands-1s-0.5-*.log`). At that pass time the mutant's kill 1 s after the resume and the trap's 1.5 s command race on wall time, so a pass of 0.75 s or more lets the command finish. Its own control, `owner_stated_seconds`, is red on every run; `owner_shell_window` and the product are unchanged since round 9, where it was red.
- `r7_mutants.py` needs a `scratch` directory beside its packet; its first run stopped there (`r7-mutants-first-no-scratch.*`), the rerun is the receipt. `rv7_mutants.py`, `slow_shell_window.py` and `pin_feasibility*.sh` had theirs created first.
- R764-9 `byte_match.py`'s first run had a wrong second argument of mine (IndexError); the rerun with the round 8 packets is the receipt.

## Commits

| Commit | Item | Subject |
|---|---|---|
| `28ac8ac8` | 1 | Keep owner_report's child asleep from its handshake to its SIGKILL: it writes its PID and waits in signal.pause(), with no timer of its own, so the report's read cannot catch it runnable |
| `29cc68ae` | 2 | Keep each stated-seconds listing whose census grows after the first pass again early, its census stated a tick in, so the trap's command after a first-pass resume and a new descendant with no shell or beside a stopped shell, live or not, are first listed there, and add early-new-sigtermed-0.5 and its three variants, named in rows 2 and 6; BLOCKING moves unchanged and 17 MUTANTS words are re-laid, for the module ratchet |
| `bd2bc180` | 3 | List a live new descendant beside a shell never resumed, its child's trap's command from pass 2 while the child is spared to 4 s, with its stated events, name it in rows 3 and 4 and the liveness table, and add both reviewer mutants of that cell and an edge mutant, each red on it with its words |
| `6676e9fe` | 4 | List a live trap command after the 1 s resume and, beside a shell never resumed, a parent beside it rather than under it whose trap's live command spares it to 4 s, table both with the shared listing beside a shell never resumed, and drop not live at 1 s from rows 2, 6 and 8 |
| `500b0f61` | 5 | Say once in the testing guide that between stated times the starved owner's passes are half a second apart, so a listing's domain is its listed passes |
| `fce77f0e` | 6 | Print in the stated-seconds summary the next-to-last in-grace resume, the lone 1 s and 10 s resumes and the liveness axis |

One-line subjects, empty bodies, no trailers. Before each commit (`receipts/item1/` to `item6/`): the quick gates (idiom, doc style, docs check, bare-metal scope, diff check), the table check, per listing at `none`, and the full `--mutants` campaign: PASS at 142/139, 146/143, 149/146, 149/146, 149/146, 149/146.

## Cost

`final/cost.txt`, `final/inproc-cost.txt` (its label "round 8" is round 9's head: `inproc-cost.NOTE`), round 9's head against this one, interleaved, beside the docs.yml jobs, host load 18 to 36:
- `owner_stated_seconds` in one process, 20 calls a tree, 3 times: median 39.6 to 40.2 ms at round 9, 51.5 to 51.9 ms here;
- as its own process: 0.16 s at both; `owner_report` 0.26 s at both; every other control within 0.05 s;
- the whole test, 4 runs each, 8 at once: mean 60.4 s at round 9, 60.6 s here.

**Round 10 adds about 12 ms to the preflight**, well under the 2 s allowed.

## Gates

All at head `fce77f0efc1425ef7732a8d70c02addc108f7afe`, one log and rc each, never piped.
- The lane gates ran on a fresh clean clone (`receipts/gates/lane.sh`, round 9's with this head and this round's scratch); `tree-after.txt` is empty with `--ignored`.
- SIGHUP was at its default in every launcher: `SigIgn 0` for the lane gates, item checks, campaigns and probes; `0x4` (SIGQUIT only) for the docs.yml launcher, as in rounds 7 to 9 (`gates/sigign-docsyml.txt`).

| Gate | rc | Result | Receipt |
|---|---:|---|---|
| Every `run:` step of `.github/workflows/docs.yml` | 0 | Round 1's runner and verifier; only the venv and HOME paths point at this round's scratch (`gates/runner-vs-round1.diff`); `not_run.json` is round 1's, unchanged. Fresh venv, identical to round 8's freeze (`gates/venv-freeze-new.txt` = `requirements-round8.txt`), fresh HOME. Verifier: 64 steps rc 0, 31 not run with round 1's reasons, 0 bad. Tree clean after each job (the no-git job has no `.git` to check). Builder legs `ALL GATES PASS EXCEPT 1 NOT RUN` and `EXCEPT 16 NOT RUN`. Jobs 03:43 to 04:31, in the background, polled |  `gates/docsyml-table.md`, `docsyml-verify.rc`, `docsyml-jobs.txt`, `docsyml/`. `gate_41`'s log is over 200 KB: sha256 and size in `LARGE-LOGS.txt`, tail in `docsyml/` |
| `python3 scripts/test_suite_cancellation.py` | 0 | `suite cancellation: PASS`; the summary prints `next_to_last`, `lone=[1, 10]`, `live_new_descendant=True` | `gates/lane/test_suite_cancellation.*` |
| `python3 scripts/test_suite_cancellation.py --mutants --jobs 4` | 0 | `owned-process mutants: PASS (149 mutants, 146 with a control that must fail)` | `gates/lane/mutants.*` |
| `--matrix`, 4 parts, `--jobs 10` | 0 each | 1683 runs, none cut. `none` green on all 11; each of the 146 red on its control with its words and on the whole test; the 3 with no control green on all 11 | `final/matrix-part1..4.*`, `final/matrix-table.md` |
| `make --no-print-directory -C tb/verilator/gptp_shadow lifecycle` | 0 | `mutant lifecycle: PASS` | `gates/lane/lifecycle.*` |
| `cd tests && behave` | 0 | 14 features, 508 scenarios, 2330 steps passed, 0 failed | `gates/lane/behave.rc`, `behave.log.tail`; 235,305 bytes, sha256 in `LARGE-LOGS.txt` |
| `git diff --check 1f29f189 HEAD` | 0 | silent | `gates/lane/diffcheck.*` |
| `check_py_idiom.py`, `check_doc_style.py`, `docs_check.py`, `check_baremetal_only.py --check` | 0 each | before each commit (also inside docs.yml) | `item*/quick/` |
| Full sweep | not run | Round 10 touches only `scripts/test_suite_cancellation.py`, `scripts/process_test_support.py` and `docs/testing/TESTING.md`, all changed by round 1 | |

## Incidents, no harm

- The reviewer packet directories are links into the reviewers' own areas. My first copies were links too; before any probe that writes beside its packet ran, they were re-copied with links dereferenced, and a check found nothing newer than this round's TAKEN in the reviewers' packets.
- Every run set `TMPDIR` to scratch. Nothing was signalled by name: busy loops and children ended through their own handles or PIDs.
- docs.yml ran once in the background, as in round 9 (a builder step alone takes about 18 minutes), polled while the other gates ran in the foreground.
- The unit's memory peak was 11.9 GB, page cache included, just under the 12 GB asked; it came while the docs.yml jobs ran beside the probes. It is 6.7 GB now.
- One ignored cache file this round wrote into the lane (`scripts/__pycache__/process_test_support.cpython-314.pyc`, from an in-lane value check) was removed; the lane's other ignored entries predate this session.
- Nothing was pushed; no PR or issue text was edited.

## Files

- `PR-BODY.md`: round 9's published body with Round 8 replaced by a link to its archived body, as rounds 2 to 7 were, Round 9 kept, and a Round 10 section; the shared sections brought to this head. 43,694 characters.
- `receipts/`: `taken.md`, `ready.md`; `item1/` to `item6/`; `final/` (probes, sweeps, matrix, stress, cost at the head); `gates/` (lane gates, docs.yml); `tools/` (this round's drivers and checks); `LARGE-LOGS.txt` (sha256 and size of each file over 200 KB, kept in scratch).

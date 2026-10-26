# [A681b] #665 lane S2, round 2: the CPU cycle and latency budget (HANDOFF)

Status: **REVIEW READY**, 2026-10-26. Every R703-1 and R704-1 finding is fixed at its cause, with a check that fails on `d58c8e22`; both points, both arms, the SHUTDOWN arm and three controls are re-measured on the corrected harness. The measured rows still miss T_svc = 10 ms (owner decision D4: S2b follows), as round 1 reported.

- Head: `cd3525c3ddcbdb5d78bf8fccdab354c468926997`, one commit on round 1's `d58c8e22e9bd96237b9a28ea1ddd55b0426380c4`. Subject `Measure the defined composed load, the whole notification fan-out and SHUTDOWN, and protect every figure (#665)`, no body, no trailers.
- Branch `665-s2-cpu-budget`, base `origin/dev-soft-core` `e76a755afc0536453161e3cd33f6f4d2dcd7641f` (verified with `git merge-base`). The PR targets `dev-soft-core`.
- Remote `https://github.com/kebag-logic/milan-fpga.git` (verified). Submodules `third_party/lwSRP` and `third_party/tsn-c-stack` and `protocol-processor` verified with `rev-parse --show-toplevel` and their own origins; no git command was run inside them.
- Assignment: issuecomment-6415127884. Findings: R703-1 (PR #792 issuecomment-6415122678), R704-1 (issuecomment-6414619069). TAKEN: issuecomment-6415150849. REVIEW READY: issuecomment-6417347947 (its body is `REVIEW-READY-COMMENT.md`).
- Every change is under `tb/verilator/ctrl_service_budget/` (one new file, `selftest_mutants.py`). No shipping RTL, SoC, firmware, CI, workflow or doc file outside it changed. Nothing pushed; no PR, issue or comment edited; no Vivado, bench or hardware.
- The commit was amended twice before publication, both times before any push: once to add three docstrings the Python idiom gate found only after the new file was tracked, once to drop two unused constants. Every gate and every regrade below was rerun at the final head.

## Contents

1. [Result](#1-result)
2. [Findings and their fixes](#2-findings-and-their-fixes)
3. [Changes, file:line and reason](#3-changes-fileline-and-reason)
4. [New checks, planted mutants and failing words](#4-new-checks-planted-mutants-and-failing-words)
5. [Gate table](#5-gate-table)
6. [Run history and reproducibility](#6-run-history-and-reproducibility)
7. [Acceptance](#7-acceptance)
8. [Open items, risks and questions](#8-open-items-risks-and-questions)

## 1. Result

Every figure is a measured clock count on the shipping cacheless VexiiRiscv, CPU 50 MHz, bus 100 MHz. The tables are in the README (Results) and `receipts/report.md`; every probe is in `receipts/runs/<arm>/table.md` and the per-group JSON.

| Arm | Groups | Paths missing T_svc | Probe instances missing T_svc | Refusals |
|---|---:|---:|---:|---:|
| A 1x1 | 17 | 10 of 61 | 11 of 78 | 0 |
| A 8x8 | 16 | 37 of 106 | 45 of 125 | 0 |
| B 1x1 | 7 | 4 of 20 | 4 of 20 | 0 |
| B 8x8 | 7 | 4 of 36 | 4 of 36 | 0 |
| SHUTDOWN arm 1x1 / 8x8 | 2 / 2 | 0 of 2 / 0 of 3 | 0 / 0 | 0 |

| Figure | 1x1 | 8x8 |
|---|---|---|
| Worst pass, A | 1,565,803 cycles (31.32 ms), backlog-adp | 2,989,496 (59.79 ms), acmp-notk |
| Composed maximum, A / B | 31.32 / 14.81 ms | 44.19 / 27.84 ms |
| Event behind 15 others | 15.49 ms (bound 29.11), 15 ahead | 44.65 (73.70), 16 ahead |
| ACMP command behind a full acmp ring | 63.30 (70.05), 11 ahead | 108.71 (120.30), 11 ahead |
| ENTITY_AVAILABLE behind the adp ring at its burst (observed) | 67.93 (81.83), 7 ahead | 83.51 (107.83), 7 ahead |
| the same with the bucket refilling (observed) | 88.33 (107.65), 4 ahead | 118.81 (156.29), 6 ahead |
| 7 frames owed ahead | 125.79 (129.81); 65.79 from the room | 151.92 (161.44); 91.92 |
| SHUTDOWN -> ENTITY_DEPARTING (test-only entry) | 0.58 (1.94) | 0.58 / 1.17 (5.14) |
| SET_NAME fan-out (8x8 if1, two recipients) | - | 8.39 ms (was 7.93, the first recipient) |

Round 1's lighter load measured the four rows at 14.12, 60.35, 43.90 and 75.76 ms (1x1): every row is worse under the defined load, as both reviews predicted. Paths not touched by this round's load or grader reproduce round 1 to the cycle (the aecp group's 8x8 start cycles equal the published ones).

## 2. Findings and their fixes

| Finding | Fix (file:line at the head) | Check that fails on `d58c8e22` |
|---|---|---|
| R703 F1 / R704 F1 (MAJOR): load lighter than defined; "admitted backlog" not a bound | Every backlog group's composed window offers every channel's admitted burst at once, MAAP and SRP included (`scenario.py:580` `composed_load`, `:534` `admission`, `:562` `maap_conflict`, `:552` `listener_ready`, `:607` `announced`); the owed row now runs under the load too (`:660`). `grade.py:569` `composed` refuses a window whose population is not the group's load (`:542`, `:555`). The README states which rows are bounds (event, ACMP, MAAP: ring room) and which are observed (ADP, AECP, SRP: burst below room); `backlog-adp-refill` (`scenario.py:612`) is R703's arrival-curve plant, and each probe reports the records ahead of it (`grade.py:369`). | `a composed load missing one channel is refused`; mutants `composition: the window's population is not checked`, `composition: the composed maximum is the run's worst pass`; receipts `drain/*.txt` show each window's population, releases per pass and records ahead |
| R703 F3 / R704 F2 (MAJOR): fan-out ends at the first recipient | `notify:<ch>:<cmd>:<dtype>:<dindex>` with the probe's `recipients` (`scenario.py:115`, `:425`, `:467`); `grade.py:276` `recipients` matches the causal command and descriptor (`:212`), `:220` `fanout_end` takes the last, `:424` `fan_out` refuses a missing recipient and a recipient outside the set | the six notification checks; mutant `notify: the first unsolicited response on any interface ends it (d58c8e22)`; `review-probes/`: late recipient 4.0 ms fits at `d58c8e22`, 14.0 ms misses at the head; missing recipient measured vs `no end` |
| R703 F2 (MAJOR): headline figures unprotected | Every conversion through `Grader.cpu_cycles/ms/bus_cycles/cpu_ms` (`grade.py:233-247`), pass end and origin (`:334`, `:345`); `oracle.json` pins each row's bound and records ahead, the worst pass and the composed maximum with its population (`selftest.py:134`, `:65`); run exit, trap, ceiling with W, expectation and commit attribution have checks | 36 named mutants all caught (section 4); R703's 12 source mutants adapted to the new anchors: 12 caught, 0 escaped (`review-probes/review_mutants_r2.log`) |
| R703 F5 / R704 F3: reuse does not bind the image | `build.py:352` firmware trees, `:356` `tree_digest`, `:368` `input_key`, `:378` `resolve`, `:395` `run_inputs` (ELF, runtime archives, every ROM `.init`, `budget_config.hpp`, sources incl. `sim.v`, CPU netlist and RAM models), `:431` `reused` refuses a changed, missing, unrecorded or unresolved input | ten `reuse refuses ...` checks; mutants `reuse: an input outside the checkout is not rechecked (d58c8e22)`, `reuse: the ROM files are not attested`; `review-probes/`: 11 zeroed digests accepted at `d58c8e22`, all 11 refused at the head; a round-1 build.json is refused (`input key 'ctrl_app.elf' does not resolve`) |
| R703 F6 / R704 F4: missing logs dropped silently | `run.py:154` `recorded` refuses each absent script or log and each stale script by name; `run.py:190` `verdict` fails a run of no group | `a regrade refuses each absent log or script, and a stale script, by name`; mutant `regrade: a selected group without its log is dropped (d58c8e22)`; `review-probes/`: empty regrade rc 0 at `d58c8e22`, rc 1 with two named refusals at the head |
| R703 F7 / R704 F5: SHUTDOWN unmeasured | Labelled `shutdown-entry` arm (`build.py:78`): a scratch fixture poll calls `adp_mbx_set_enable(false)` once at NOW_MS 2,500 (`scenario.py:748`); the path starts at that function's entry (`grade.py:260`, `sim_main.cpp:258`, `build.py:271`) and ends at each interface's DEPARTING; control `slow-adp-shutdown` (`build.py:52`) | `an entry start is its own function's`; mutant `marker: an entry start takes any function entry`; control caught at 24.903 ms against 0.582 ms |
| R703 F4: worse instance hidden; instance counts | `scenario.py:118` `path_key` (fixture, control and MAAP probes carry their path); `run.py:49` `paths` reports each path's worst instance, `:69` `counts` per path and per instance; table.md lists both and every timed-out wait | `each path reports its worst instance`, `misses are counted per path and per probe instance`; two `(d58c8e22)` mutants |
| R703 R-1 / R704 R1 | `#665 S2` -> `#665` in all six comments (incl. `split_soc.py:13`); `(the lane's -j16)` -> `(-j16)`; selftest docstring `(#665; the method of #397)` (R703's exact text; R704's alternative wording differs only in words) | wording |
| R703 R-2, R-3 | README Passes paragraph: "AECP's two modules ... mostly their polls"; "The `backlog` group's composed maximum (arm B's maximum)" | wording |
| R703 R-4 | **Not applied**: `docs/testing/TESTING.md` is in the release lanes' file map (#396 part A, #784 step 2), and this lane may not touch a release file. Left for the manager's residue checklist. | - |
| R703 S1 | `WIRE` parsed in the order `sim_main.cpp` prints it (`grade.py:141`); each run's table.md lists its timed-out waits | - |
| R703 S2 | README D3: flash window 138 to 303 cycles, 15 to 29 times a block RAM fetch | - |

One rule R703 named was inverted rather than restored. R703's R8 planted "a receive commit given to the newest frame" as a defect. `KL_mbx_rx.sv:199` holds `rx_ready_o` low from a frame's last byte to its verdict, and all 469 commits in round 1's logs follow their own frame's last byte by exactly 4 bus cycles with no frame starting in between. So the commit belongs to the newest pending frame and every older pending frame was refused (`grade.py:87` `owner`). Round 1's oldest-frame rule with a 64-cycle window misattributes a refused frame followed within 64 cycles by a committed one; `a receive commit belongs to the frame it follows` plants exactly that, and the mutant `marker: a receive commit goes to the oldest pending frame (d58c8e22)` is caught. The adapted R8 plants the oldest-frame rule and is caught.

## 3. Changes, file:line and reason

| File:line | What | Reason |
|---|---|---|
| `scenario.py:113-136` | `Probe.recipients`, `Probe.path`/`path_key`, `Group.load`/`admission`/`offer` | the fan-out's recipient set; one path across groups; the composed population a window must commit |
| `scenario.py:534-610` | `admission`, `listener_ready`, `maap_conflict`, `gm_run`, `composed_load`, `announced` | every channel's admitted burst at once; MAAP records that pass the range filter (each interface's own range, `reply ... on=<if>`); SRP Listener Ready; MAAP announced first |
| `scenario.py:612`, `:660`, `:689` | `bound_talker_groups` (burst and refill leg), `owed_group`, `backlog_groups` | the four rows under the defined load; the arrival-curve plant |
| `scenario.py:748-779` | `SHUTDOWN_MS`, `shutdown_groups` (`adp-shutdown`, `control-shutdown`) | the SHUTDOWN row and its control |
| `scenario.py:782-835` | fixture: a short composed window (one record per channel, two GM events); SET_NAME recipients; AVAILABLE/DEPARTING carry the current GM | pins a composed maximum and population in the oracle; a GM change makes a gm_id-0 AVAILABLE a mismatch (Milan v1.2 Table 5.54) |
| `scenario.py:838` | `all_groups`: the shutdown-entry build runs only its groups | the variant arm |
| `grade.py:1-18` | docstring: the rule each figure rests on, one place each | now true |
| `grade.py:87`, `:104-178` | `owner`; RXS length, ENTRY lines, refused frames, WIRE order | exact commit attribution; the entry start; refused frames named in a population refusal |
| `grade.py:212-225`, `:276-293`, `:424-438` | `causal`, `fanout_end`, `Grader.recipients`, `fan_out` | the whole fan-out |
| `grade.py:233-247`, `:334-366` | `bus_cycles`, `cpu_ms`, `pass_end`, `pass_origin`, `pass_bound` | every conversion in one method |
| `grade.py:369-395` | `ahead`, `unwrapped` | the backlog at each input |
| `grade.py:534-588` | `refuse_run`, `population`, `check_load`, `composed_passes`, `composed` | the defined load is asserted |
| `run.py:44-105` | `verdict_word`, `paths`, `counts`, `table` | worst instance per path, counts per path and per instance, timed-out waits |
| `run.py:108-207` | `--mutation`/`--variant` from `build.py`; `select` checks a mutation's variant; `recorded`; `verdict` | absent logs refused by name; a run of no group fails |
| `run.py:209-` | reuse refusal prints `REFUSED` and returns 1 | a stale build is a failure, not a traceback |
| `build.py:1-12`, `:44-90` | docstring; `MUTATIONS` with control group and variant; `slow-adp-shutdown`; `VARIANTS['shutdown-entry']` | SHUTDOWN's test-only input and its planted defect |
| `build.py:271`, `:302-306` | `ENTRY_SYMBOLS`, `entry_pc`/`entry_name` in `budget_config.hpp` | the testbench reports the entry |
| `build.py:352-460` | firmware trees, `tree_digest`, `input_key`, `resolve`, `digest`, `run_inputs`, `build`, `reused` | every run input attested; nothing skipped |
| `sim_main.cpp:4`, `:177`, `:207`, `:255-259`, `:400-423` | comment; `Sent` keeps each egress frame's interface; ENTRY lines; `reply ... on=<n>` | the entry start; MAAP conflicts copied from each interface's own ANNOUNCE |
| `split_soc.py:13` | `#665` | R-1 |
| `selftest.py` | 51 checks in seven families, the headline figures pinned, temporary-file reuse and regrade checks | section 4 |
| `selftest_mutants.py` | 36 mutants | section 4 |
| `fixture.log`, `oracle.json` | regenerated by `selftest.py --write-fixture` from a fresh 1x1 `fixture` run at this code | the fixture gained a composed window |
| `README.md` | run (reuse, regrade, arms, controls), grading rules, every result table, findings, controls and self-test, limits | the corrected harness and figures |

## 4. New checks, planted mutants and failing words

`python3 -B tb/verilator/ctrl_service_budget/run.py --self-test`: 51 `PASS` lines, 36 `MUTANT caught`, `self-test: 0 failures`, rc 0 (`receipts/gates/selftest.log`). A failing check prints `FAIL: <check>: <differing fields>`; an uncaught mutant prints `MUTANT ESCAPED: <mutant>` and fails the run.

| Planted mutant (`selftest_mutants.py`) | Failing check, as printed |
|---|---|
| marker: the frame tag is ignored | tagged start |
| marker: a timer path starts when its record is posted | fixture row fixture.tmr_no_resp1.if0 |
| marker: a timer path starts one millisecond after its deadline | fixture row fixture.tmr_no_resp1.if0 |
| marker: an entry start takes any function entry | an entry start is its own function's |
| marker: any response on the channel ends the path | sequence and interface |
| marker: the interface is ignored | sequence and interface |
| marker: the first required output ends the path | fixture row fixture.set_name.if0 |
| marker: a receive commit goes to the oldest pending frame (d58c8e22) | a receive commit belongs to the frame it follows |
| marker: the expected-response check is skipped | the expected response is checked |
| notify: the first recipient's commit ends the fan-out | two recipients across interfaces end at the last |
| notify: the first unsolicited response on any interface ends it (d58c8e22) | two recipients across interfaces end at the last |
| notify: any unsolicited response counts as the change | unrelated unsolicited responses do not end it |
| notify: a missing recipient is not refused | a missing recipient is refused |
| notify: a recipient outside the set is not refused | a notification to a controller outside the set is refused |
| clock ratio: CPU cycles equal bus cycles | fixture row fixture.link_up.if0 (`cpu_cycles 10562 (pinned 5281)`) |
| clock ratio: inverted | fixture row fixture.link_up.if0 |
| clock ratio: CPU cycles rounded down | fixture row fixture.malformed.if0 (`cpu_cycles 107472 (pinned 107473)`) |
| clock ratio: milliseconds from the CPU clock | fixture row fixture.link_up.if0 |
| clock ratio: a pass's milliseconds from the bus clock | fixture passes: worst pass and composed maximum (`worst_ms 14.35369 (pinned 28.70738), composed_ms 4.18342 (pinned 8.36684)`) |
| clock ratio: a pass's bus cycles equal its CPU cycles | fixture row fixture.link_up.if0 (`bound_cpu_cycles 124226 (pinned 248452)`) |
| pass bound: it starts at the input, not at the running pass | fixture row fixture.malformed.if0 (`bound_cpu_cycles 107473 (pinned 107505)`) |
| composition: the window's population is not checked | a composed load missing one channel is refused |
| composition: the composed maximum is the run's worst pass | fixture passes (`composed_cycles 1435369 (pinned 418342)`) |
| deadline: T_svc 20 ms | planted over-budget path is caught |
| deadline: strictly below the budget | exact budget passes |
| deadline: the normative wait is not added | W + T_svc passes |
| deadline: the ceiling drops the normative wait | W + T_svc passes |
| deadline: the ACMP ceiling is the transaction timeout | ceilings pinned |
| run: a CPU trap is not refused | a CPU trap is refused |
| run: a T_svc miss never fails the run | a T_svc miss fails the run unless recorded |
| run: a refusal does not fail the run | a refusal fails the run, recorded or not |
| regrade: a selected group without its log is dropped (d58c8e22) | a regrade refuses each absent log or script, and a stale script, by name |
| reuse: an input outside the checkout is not rechecked (d58c8e22) | reuse refuses the image |
| reuse: the ROM files are not attested | reuse refuses a ROM file |
| tables: a path's first instance is reported, not its worst (d58c8e22) | each path reports its worst instance |
| tables: misses are counted per probe instance only (d58c8e22) | misses are counted per path and per probe instance |

Full-harness controls, regraded at the head (`receipts/runs/C-*-regrade.log`):

| Control | Plant | Failing words | Verdict |
|---|---|---|---|
| `--mutation slow-adp-rx` | 16,000-iteration spin before `adp_rx` | `BUDGET control.discover.if0: 24.614 ms over T_svc 10 ms` (0.294 ms unplanted) | `CONTROL slow-adp-rx caught`, rc 0 |
| `--variant shutdown-entry --mutation slow-adp-shutdown` | spin before disabling ADP | `BUDGET control.shutdown.if0: 24.903 ms over T_svc 10 ms` (0.582 ms unplanted) | `CONTROL slow-adp-shutdown caught`, rc 0 |
| `--cpu-regions as-built` | the generator gets the 224 KiB regions | `REFUSED boot-fault: ... ['TRAP 330592 0 1 00006880', ...]` | `CONTROL as-built caught: an instruction access fault (cause 1)`, rc 0 |

R703's own twelve mutants, adapted to the new anchors (`scripts/review_mutants_r2.py`, `receipts/review-probes/review_mutants_r2.log`): `review mutants: 12 run, 0 escaped the self-test`.

## 5. Gate table

Every gate ran at the head `cd3525c3`, foreground and unpiped; logs in `receipts/gates/` with the rc on the last line.

| Gate | Command | rc |
|---|---|---:|
| Harness self-test | `python3 -B tb/verilator/ctrl_service_budget/run.py --self-test` | 0 |
| BDD conformance (rtl-fast) | `cd tests && behave`: 14 features, 406 scenarios, 1,977 steps | 0 |
| Docs wording and links | `python3 scripts/docs_check.py` | 0 |
| Doc cited paths | `python3 scripts/check_doc_paths.py` | 0 |
| Doc style, its self-test | `python3 scripts/check_doc_style.py`, `--selftest` | 0, 0 |
| Archive, its self-test | `python3 scripts/check_archive.py`, `--selftest` | 0, 0 |
| Em dash, its self-test | `python3 scripts/check_em_dash.py --base e76a755afc0536453161e3cd33f6f4d2dcd7641f` (483 added lines), `--selftest`, pinned renderer env | 0, 0 |
| Per-page contents | `python3 scripts/gen_toc.py --selftest`, `--verify-anchors`, `--check`, pinned renderer env | 0, 0, 0 |
| Python idiom, its self-test | `python3 scripts/check_py_idiom.py`, `--selftest` | 0, 0 |
| C++ idiom, its self-test | `python3 scripts/check_cpp_idiom.py`, `--selftest` | 0, 0 |
| Hygiene | `python3 scripts/check_hygiene.py --check` | 0 |
| TODO ownership | `python3 scripts/check_todo_ownership.py` | 0 |
| SoC sources | `python3 scripts/check_soc_sources.py` | 0 |
| RTL source lists | `python3 scripts/check_rtl_source_lists.py` | 0 |
| Whitespace | `git diff --check e76a755a HEAD` | 0 |
| Regrade at the head, six arms | `run.py ... --regrade --record-budget-findings`; results.json and table.md byte-identical to the measuring regrade | 0 each, 0 refusals |
| Controls, three | section 4 | 0 each |

The full serial sweep was not run: the lane changes only files under `tb/verilator/ctrl_service_budget/`, and no shared file, as the brief allows.

## 6. Run history and reproducibility

- Builds: nine (A1, A8, B1, B8, S1, S8, C-slow, C-shutdown, C-asbuilt), each 15 s. The unmodified 1x1 and 8x8 ELFs are `d4c28047...` and `c89a1871...`, identical to round 1's.
- Measuring campaigns ran in parallel (`--jobs 8`, then 4 and 5 for the extra arms), split into long and backlog sets, then merged per arm and regraded together (`receipts/drivers/`).
- The first fixture run refused `fixture.entity_departing.if0` (`no end: missing ['tmr:1']`): the new window's GM changes made TALKER_A's gm_id-0 AVAILABLE a mismatch. The fixture's AVAILABLE and DEPARTING now carry the current grandmaster; the rerun measured 25.174 ms (round 1: 25.172), and the fixture was regenerated from it.
- A launch line lost its shell variables, so four of the five short legs did not start at first (their logs were never created); they were relaunched and ran to completion.
- `backlog_groups` was split for the 100-line function limit after the campaigns started. Every group script at both points and every variant was digested before and after; all 37 are identical (`receipts/scripts-digest-*.json`).
- At the head, all nine builds were rebuilt into fresh directories (`receipts/drivers/repro.log`): every native model and every ELF is byte-identical. `sim.v` differs in its two LiteX date lines, and the runtime archives in their `ar` member timestamps only.
- Every arm and control was regraded at the head from copies of the measured logs: results.json and table.md byte-identical.

## 7. Acceptance

| Item | Status | Evidence |
|---|---|---|
| Round 2, 1: the defined load; bound vs observed | met | README Backlog rows (admission, population, rows); `drain/*.txt` |
| 2: fan-out to the last required recipient | met | AECP table (8x8 if1 8.39 ms); six checks |
| 3: self-protecting figures | met | 36 mutants; R703's 12 adapted: 0 escaped |
| 4: reproducibility | met | ten reuse checks; `review-probes/` |
| 5: no silent drops | met | regrade check; `review-probes/` empty regrade rc 1 |
| 6: tables, MINORs and RESIDUE | met except R-4 (release file; section 8) | README; section 2 |
| Re-measure at both points | met | section 1 |
| Round 1: every row of `MAILBOX_SPLIT.md:495-502` | met (SHUTDOWN through the labelled test-only entry) | README ADP |
| Rows within T_svc | **not met**: owner decision D4, S2b follows | section 1 |

So the PR body says "Relates to #665".

## 8. Open items, risks and questions

- **R-4 not applied**: `docs/testing/TESTING.md:518` is a release-lane file (#396 part A, #784 step 2 in the plan's file map). Its exact text also links into a review-evidence path; a corrected link would be `../../tb/verilator/ctrl_service_budget/README.md`. For the manager's residue checklist.
- R704-R1's alternative wording for two comments was not used; R703's exact text was, and both remove the labels.
- The ADP, AECP and SRP rows are observed at the burst; the refill leg is one sample of sustained arrivals, not a bound.
- The SHUTDOWN arm's poll reads NOW_MS once a pass (9 CPU cycles); it is labelled and never the formal image.
- On the `backlog` group's interface 0, the event row's LINK_DOWN arrives with the load, so MAAP and SRP there take their records with the link down; `backlog-adp` and `backlog-owed` carry the load with the link up.
- Large logs (40 files over 200 KB) are listed in `receipts/MANIFEST.json` by sha256 and size; every group's graded JSON is kept.
- The self-test is portable, but no CI job runs it (registering it is a CI change outside this lane).
- START_STREAMING remains unrun (an empty fixture port). Physical calibration NOT RUN; nothing here is hardware evidence.

# HANDOFF: #665 lane S5, round 2, [A702b]

STATUS: REVIEW READY. Head `26ba56e1d5749a71668f9e4436f28e8635f03f95`, four commits on `eef3d97a`, no rebase, no force, nothing pushed.

Repository: origin is `kebag-logic/milan-fpga`, verified. The lane branched from `dev-soft-core` `5b5f4336`, verified an ancestor. Target `dev-soft-core`.
TAKEN was already posted (issuecomment-6682531069) and not posted again.
REVIEW READY posted: issuecomment-6692163137; text in `REVIEW-READY-COMMENT.md`.

## Authority

- Assignment: [A10] issuecomment-6677495623 (round 2), on R783-1 (issuecomment-6677488199) and R784-1 (issuecomment-6677104394).
- The STOP (issuecomment-6682623686) is answered by issuecomment-6682851386: grade against the bounds in the tree at this PR's base and mark them so; one column of the amended bounds of the round 18 ruling, for information; no numerical grading rule changes; S5 re-grades when #810 merges; per-descriptor and ALL-push rows both stay; finish the rest from the recovery patch.
- The recovery patch equalled the working tree byte for byte at resume, and was kept and extended. The STOP session's files are in `superseded-stop/`.

## Commits

| Commit | What |
|---|---|
| `bc7ceb2f` | `hooks_build.py` takes the firmware tree's path from the split boot harness; the `OUTSIDE` entry goes, so `ctrl_configs.py` equals its base. |
| `d5add6f9` | Plant verdict, grading-rule checks, per-descriptor rows, amended column, README text. |
| `78415f7a` | An escaped late plant says which path was not found. |
| `26ba56e1` | README: the results. |

## Changes (file:line at the head, reason)

| File:line | Change | Reason |
|---|---|---|
| `tb/verilator/ctrl_service_hooks/hooks.py:116` | `Plant.probe`, the path a late plant delays | item 1: a plant is caught only by a finding its defect causes |
| `hooks.py:129` and each late plant, `:234` for `counters-late` | `late()` takes the path; all eight late plants name theirs | item 1, for every late plant, not `counters-late` alone |
| `hooks.py:75-78` | `AMENDED_SRP_MS`, `AMENDED_QUEUED_CEILING_MS`, `QUEUED_PATH` | ruling 6682851386: the amended bounds, for information |
| `hooks.py:92`, `:101` | `amended_service_ms`, `amended_ms` | the column's values; no grade reads them |
| `hooks.py:349-356` | a probe per descriptor beside `counters.all`, through `Group.together`, the whole push listed first | item 4; `mark` costs no simulated time, so the script's timing is unchanged, and listing the whole push first keeps it named as the worst at the tie with the last descriptor |
| `hooks.py:481` | docstring: no lane name | R783-1 R1 = R784-1 RESIDUE-1 |
| `run.py:4` | docstring: no lane names | R783-1 R2 |
| `run.py:47` | `BOUNDS_NOTE` | ruling 6682851386: mark the bounds so |
| `run.py:190`, `:208`, `:215` | the amended column, computed in the table alone | that the column cannot reach a verdict by construction |
| `run.py:251`, `:257`, `:328` | `plant_wanted`, `plant_findings`, used by the verdict | item 1 |
| `hooks_build.py:93-96` | `FIRMWARE`, `IMAGE`, `PROVISIONAL` from the split boot harness | item 3, option 2 of the ruling |
| `sw/firmware/ctrl/test/ctrl_configs.py` | the six-line entry removed; byte-identical to `5b5f4336` | item 3. The only shared file touched, and only to restore it |
| `hooks_selftest.py:28` | the harness's own directory first again before `import run` | R784-1 S-2: the module's direct entry works |
| `hooks_selftest.py:47-48` | `PROBE_TX`, `FACE_COMMIT` fixed at import | two round 1 mutants passed only because their check's setup crashed; see below |
| `hooks_selftest.py:391`, `:413` | `plant_verdict`, `check_plant_verdict`: `run.main` on all 16 plants | item 1's self-test |
| `hooks_selftest.py:434`, `:455`, `:472` | `check_held_grade`, `check_missing_held`, `check_summary` | item 2 |
| `hooks_selftest.py:501` | `check_counter_rows` | item 4 |
| `hooks_selftest.py:529` | `check_amended` | the column grades nothing |
| `hooks_selftest.py:642-667` | `held_fields`, `summary_fields`, `worst_by`, `counters_edited` | mutant helpers. They wrap a function's real output, as the file's other mutants do: the idiom gate refuses `exec` |
| `README.md:15` | FR_NFR at this base still reads 10 ms | R784-1 RESIDUE-3 = R783-1 S4 |
| `README.md:16` | the bounds at this base, the amended bounds | ruling 6682851386 |
| `README.md:74`, `:78` | the plant verdict rule; the `OUTSIDE` sentence replaced | items 1, 3 |
| `README.md:112`, `:168`, `:178` | the hooks table's columns; the amended rule; the ALL push both ways | ruling; item 4 |
| `README.md:205-206` and the mutant table | the self-test's new reach, the table generated from `MUTANTS` | item 2 |
| `README.md:293-450` | Results and Findings, the tables generated from the runs | item 4, ruling |
| `README.md:440-441` | "(H-COUNTERS on the answering arm only, where it runs)" | R784-1 RESIDUE-2 |
| `README.md:499-500` | two limits | the ALL push under load is not measured; the bounds |

No firmware, RTL or shared harness file is edited. No file outside `tb/verilator/ctrl_service_hooks/` differs from the base (`probes/trial_merges.txt`).

## New checks: each mutant and its failing words

Six new checks (28 in all), 48 new mutants (79 in all). Each must fail its named check, and `probes/mutant_audit.txt` records why every one of the 79 fails: none fails on an incidental exception.

| Mutant | Fails check | Failing words |
|---|---|---|
| plant: any finding of the hook catches it (the earlier rule) | a plant is caught only by its own finding | `adp-late: reported caught with no plant applied, rc 0: PLANT adp-late caught: LATE H-ADP` |
| plant: any finding of its kind catches it | a plant is caught only by its own finding | `adp-late: reported caught with no plant applied, rc 0: PLANT adp-late caught: LATE H-ADP` |
| plant: a path that only starts with its own catches it | a plant is caught only by its own finding | `adp-late: reported caught with no plant applied, rc 0: PLANT adp-late caught: LATE H-ADP` |
| plant: a late plant names no path | a plant is caught only by its own finding | `adp-late: names the path None` |
| plant: every run is caught | a plant is caught only by its own finding | `adp-late: reported caught with no plant applied, rc 0: PLANT adp-late caught: LATE H-ADP` |
| plant: an escape exits 0 | a plant is caught only by its own finding | `adp-late: reported caught with no plant applied, rc 0: PLANT adp-late ESCAPED: LATE H-AD` |
| held: W added to its bound | the held push's grade | `the held bound includes W: 920.0` |
| held: the exact bound misses | the held push's grade | `a held push at its bound misses` |
| held: the verdict is relaxed by 1 ms | the held push's grade | `a held push past its bound fits` |
| held: W is not recorded | the held push's grade | `the held W is not recorded: 0.0` |
| held: its cycles round down | the held push's grade | `3 bus cycles are 1 at the 50 MHz CPU, not 2` |
| held: its cycles are the bus's | the held push's grade | `3 bus cycles are 3 at the 50 MHz CPU, not 2` |
| held: its margin omits W | the held push's grade | `the held margin is 980.0, not 1000 - 900 - 20` |
| held: its timeout is the notification family's | the held push's grade | `the held timeout is 240.0` |
| held: it counts as under the composed load | the held push's grade | `held row classification {'hook': 'H-COUNTERS', 'group': 'hooks-counters', 'probe': 'coun` |
| held: it counts as never served | the held push's grade | `held row classification {'hook': 'H-COUNTERS', 'group': 'hooks-counters', 'probe': 'coun` |
| held: it is H-NOTIFY's | the held push's grade | `held row ('H-NOTIFY', 'hooks-counters', 'counters.held', 'notify', 0)` |
| held missing: silently accepted | a held push never sent | `a held push never sent is no finding: []` |
| held missing: it fits | a held push never sent | `a missing push fits: {'hook': 'H-COUNTERS', 'group': 'hooks-counters', 'probe': 'counter` |
| held missing: it counts as served | a held push never sent | `a missing push fits: {'hook': 'H-COUNTERS', 'group': 'hooks-counters', 'probe': 'counter` |
| held missing: its finding is dropped | a held push never sent | `a held push never sent is no finding: ['LATE H-COUNTERS: counters.held.if0: never served` |
| held missing: its timeout is the notification family's | a held push never sent | `missing row {'hook': 'H-COUNTERS', 'group': 'hooks-counters', 'probe': 'counters.held.if` |
| summary: the fastest path is the worst | the worst path and the counts | `the worst alone is fast, not slow` |
| summary: W is left in the service | the worst path and the counts | `the worst alone is waiting, not slow` |
| summary: a path never served is not worst first | the worst path and the counts | `the worst under load is loaded, not the path never served` |
| summary: alone and under load are not apart | the worst path and the counts | `the worst alone is starved, not slow` |
| summary: alone and under load are swapped | the worst path and the counts | `the worst alone is starved, not slow` |
| summary: another hook's paths are its own | the worst path and the counts | `the worst alone is other, not slow` |
| summary: a miss counts as a narrow fit | the worst path and the counts | `4 narrow fits, not 1` |
| summary: no narrow fit is counted | the worst path and the counts | `0 narrow fits, not 1` |
| summary: no miss is counted | the worst path and the counts | `0 misses, not 3` |
| summary: the path count is every hook's | the worst path and the counts | `a hook with no path has a worst` |
| summary: the applied count is dropped | the worst path and the counts | `the ordering results are not kept: {'paths': 6, 'misses': 3, 'narrow': 1, 'worst': {'alo` |
| summary: the undecided count is dropped | the worst path and the counts | `the ordering results are not kept: {'paths': 6, 'misses': 3, 'narrow': 1, 'worst': {'alo` |
| summary: the ordering findings are dropped | the worst path and the counts | `the ordering results are not kept: {'paths': 6, 'misses': 3, 'narrow': 1, 'worst': {'alo` |
| summary: the obligation is dropped | the worst path and the counts | `the obligation or clauses are not kept` |
| summary: the clauses are dropped | the worst path and the counts | `the obligation or clauses are not kept` |
| ALL: the push ends at its first descriptor | the ALL push both ways | `the ALL push ends at ['notify:2:0029:5:1']` |
| ALL: no descriptor has a row | the ALL push both ways | `a descriptor has no row of its own: {(5, 1): None, (6, 0): None, (9, 0): None, (36, 0): ` |
| ALL: a descriptor's row ends at the whole push | the ALL push both ways | `counters.all.t5.i1.if0 ends at ['notify:2:0029:5:1', 'notify:2:0029:6:0', 'notify:2:0029` |
| ALL: a descriptor's row opens after the change | the ALL push both ways | `counters.all.t5.i1.if0 opens after the change` |
| amended: SRP keeps its ceiling | the amended column grades nothing | `the amended bounds` |
| amended: the ceiling at two interfaces is 20 ms | the amended column grades nothing | `the amended bounds` |
| amended: every counter push is queued | the amended column grades nothing | `a path the decisions leave has another bound` |
| amended: W is left off | the amended column grades nothing | `W left off the column` |
| amended: the column grades a path | the amended column grades nothing | `SRP 22.0` |
| amended: the table does not say which bounds graded | the amended column grades nothing | `the table does not say which bounds graded` |
| amended: the column repeats the bound | the amended column grades nothing | `SRP 18.0` |

The real plants: all 16 caught at `78415f7a`, `plants/plant-*.log`, each late plant on its path, every figure equal to round 1's. The no-op control: `plants/noop-counters-late.log`, the spin replaced by a comment, as R783-1 did it, prints `PLANT counters-late ESCAPED: LATE H-COUNTERS: counters.first.if0 not found`, rc 1 (the required result; its run still has `LATE` findings on `counters.all`).

## Reviewers' verification, re-run at the head

| Reviewer's check | Result | Receipt |
|---|---|---|
| R784-1 `plant_vacuity_probe.py` | `ESCAPED`, `run.main()` rc 1 | `probes/plant_vacuity_probe.txt` |
| R784-1 `extra_mutants.py` | all three caught by named checks; worst-path and LATE-against-rows consistency OK on all four runs | `probes/extra_mutants.txt` |
| R783-1 catch rules on the real unplanted runs | 0 of 16 match | `probes/plant_controls.txt` |
| R783-1 `probes.py` | P1, P7, P8, P10 caught; P11 escapes, as that control must; P2, P3, P4, P6, P9 escape (below); P5, P12 anchors moved | `probes/r783_probes.txt` |
| P5, P12 with their anchors restated | both caught | `probes/r783_probes_moved.txt` |

## Measurements

The four runs at `d5add6f9`, CPU 100 MHz on `sys`, bus 100 MHz, each in a clean clone with its own build, pinned Verilator 5.050, regraded at `26ba56e1` with every input digest checked. Graded against the bounds in the tree at this base.

| Point | Arm | Groups | Paths | Refusals | ORDER | NARROW | LATE | Run rc | Regrade rc |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1x1 | idle | 27 | 145 | 0 | 0 | 0 | 28 | 0 | 0 |
| 1x1 | answering | 29 | 164 | 0 | 0 | 0 | 31 | 0 | 0 |
| 8x8 | idle | 27 | 207 | 0 | 0 | 0 | 38 | 0 | 0 |
| 8x8 | answering | 29 | 240 | 0 | 0 | 0 | 60 | 0 | 0 |

All 732 paths of round 1 are unchanged to the CPU cycle with the same verdicts; the 24 new paths are the per-descriptor rows (`probes/compare_round1.txt`).

H-COUNTERS' ALL push: as one path 27.58 ms at 1x1 and 218.71 ms at 8x8. Per descriptor, 2 of 5 rows at 1x1 and 18 of 19 at 8x8 are over 20 ms; each descriptor's own fan-out is about 2.7 ms and 5.9 ms, the rest of its row the queue ahead of it; the first notice leaves after 2.76 and 4.68 ms. For information: 2 of 5 and 14 of 19 rows are over the amended ceiling, and no H-SRP path lies between 18 and 20 ms, so the amended bounds change no verdict.

## Shared files touched

`sw/firmware/ctrl/test/ctrl_configs.py`, only to remove this lane's entry. It equals `5b5f4336`. Trial merges with #810, #812 and `dev-soft-core` have no conflict.

## Disclosures

- **Two hollow round 1 mutants.** `H-DISC: the sink's PROBE_TX_COMMAND is never recognised` and `H-AECP: no face commit is recognised` passed only because the check's own setup raised an exception, so neither had exercised its rule. Fixed at `hooks_selftest.py:47-48`; both now fail on the rule. Outside the four items, inside the Tests lens, found by auditing why each mutant fails.
- **A lost receipt.** The builder passed at `78415f7a`, but a chain's next step truncated its log before a watcher stopped that chain. That run is not cited; the builder ran again at the head.
- **Round 1's Verilator.** Its `env.sh` left Verilator to `PATH`. This round pins 5.050 in `scripts/env.sh`. The executables differ from round 1's, and every shared path still equals it to the cycle.

## Open questions

- **For the maintainer:** the amended column applies the queued ceiling to the ALL push's rows only, the rows ruling 6677495623 ties to the queued-notice question, and gives the ceiling because the derived bound is #810's. Any other notification path keeps its bound in that column. It grades nothing either way, and #810's re-grade settles it.
- **Suggestions not taken,** being outside the four items: R783-1 S1's P2, P3, P4, P9 and the probe P6, which still escape the self-test; S2; S3 = R784-1 S-1; S5; S6; R784-1 S-3.
- S5's acceptance "each hook within its bound" stays open on #665, by the ruling.

No STOP condition was met: no firmware instrumentation, RTL or shared-harness change was needed.

## Gate table

Each in a clean clone, foreground of its own unit; every log ends with its rc and the tree's state after. `78415f7a..26ba56e1` changes only the README. `d5add6f9..78415f7a` changes an escape's printed line and its self-test check.

| Gate | Command (from the clone's root) | At | Result | Receipt |
|---|---|---|---|---|
| Hook self-test and its mutants | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | `26ba56e1` | rc 0; 28 of 28 checks, 79 of 79 mutants | `gates-head/docs/hooks_selftest.log` |
| The 16 plants | `python3 -B tb/verilator/ctrl_service_hooks/run.py --plant <name> --build-dir <build>` | `78415f7a` | 16 of 16 `PLANT <name> caught`, rc 0 | `plants/plant-*.log` |
| No-op `counters-late`, its spin a comment (one scratch edit) | `python3 -B tb/verilator/ctrl_service_hooks/run.py --plant counters-late --build-dir <build>` | `78415f7a` | rc 1, 1123 s; **rc 1 is the required result**, `ESCAPED` | `plants/noop-counters-late.log` |
| Hooks 1x1-idle | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --build-dir <build> --record-findings --jobs 4` | `d5add6f9` | rc 0, 9022 s | `runs/1x1-idle/run.log` |
| Regrade 1x1-idle | `... --point 1x1 --build-dir <build> --regrade --record-findings` | `26ba56e1` | rc 0 | `runs/1x1-idle/regrade.log` |
| Hooks 1x1-ans | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --arm answering --build-dir <build> --record-findings --jobs 4` | `d5add6f9` | rc 0, 10622 s | `runs/1x1-ans/run.log` |
| Regrade 1x1-ans | `... --point 1x1 --arm answering --build-dir <build> --regrade --record-findings` | `26ba56e1` | rc 0 | `runs/1x1-ans/regrade.log` |
| Hooks 8x8-idle | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 8x8 --build-dir <build> --record-findings --jobs 4` | `d5add6f9` | rc 0, 10440 s | `runs/8x8-idle/run.log` |
| Regrade 8x8-idle | `... --point 8x8 --build-dir <build> --regrade --record-findings` | `26ba56e1` | rc 0 | `runs/8x8-idle/regrade.log` |
| Hooks 8x8-ans | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 8x8 --arm answering --build-dir <build> --record-findings --jobs 4` | `d5add6f9` | rc 0, 10162 s | `runs/8x8-ans/run.log` |
| Regrade 8x8-ans | `... --point 8x8 --arm answering --build-dir <build> --regrade --record-findings` | `26ba56e1` | rc 0 | `runs/8x8-ans/regrade.log` |
| Firmware self-test, shard 0 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 0/4 --jobs 8` | `26ba56e1` | rc 0, 339 s | `gates-head/selftest-shard0.log` |
| Firmware self-test, shard 1 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 1/4 --jobs 8` | `26ba56e1` | rc 0, 1293 s | `gates-head/selftest-shard1.log` |
| Firmware self-test, shard 2 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 2/4 --jobs 8` | `26ba56e1` | rc 0, 467 s | `gates-head/selftest-shard2.log` |
| Firmware self-test, shard 3 | `python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test --shard 3/4 --jobs 8` | `26ba56e1` | rc 0, 788 s | `gates-head/selftest-shard3.log` |
| CPU budget harness, 1x1 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 1x1 --build-dir <build> --record-budget-findings --jobs 4` | `78415f7a` | rc 0, 7213 s; 18 groups, 0 refusals | `gates/s2_harness-1x1.log` |
| CPU budget harness, 8x8 | `python3 -B tb/verilator/ctrl_service_budget/run.py --point 8x8 --build-dir <build> --record-budget-findings --jobs 4` | `78415f7a` | rc 0, 7670 s; 17 groups, 0 refusals | `gates/s2_harness-8x8.log` |
| End-station builder | `python3 sw/builder/test_builder.py --require-rv32` | `26ba56e1` | rc 0, 1483 s; one registered NOT RUN, gate 11, the calibration arm needing a build tree absent here, as in round 1: its verdict does not cover that arm | `gates-head/builder_require_rv32.log` |
| TSN stack boundary, without Verilator | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --without verilator` | `26ba56e1` | rc 0, 1149 s; `ctrl_boundary: PASS`, no `OUTSIDE` entry | `gates-head/ctrl_boundary.log` |
| TSN stack boundary, Verilator half | `python3 sw/firmware/ctrl/test/ctrl_boundary.py --require-rv32 --selftest --only verilator` | `26ba56e1` | rc 0, 716 s; `ctrl_boundary: PASS`, no `OUTSIDE` entry | `gates-head/ctrl_boundary-verilator.log` |
| Docs, scope, idiom, CI and behave gates (gates_s5.py), including `cd tests && behave` and the CPU budget harness's self-test | see each log's first line | `26ba56e1` | 0 of 98 gates nonzero or left the tree dirty; behave 1977 steps passed | `gates-head/docs/summary.md` |
| Merge candidate, self-test | `python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test` | `1281508a` | rc 0, 3 s; the lane head merged onto `dev-soft-core` `a68536fa` | `merge/hooks_selftest-head.log` |
| Merge candidate, 1x1 idle | `python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 --build-dir <build> --record-findings --jobs 6` | `4a8cb576` | rc 0, 3612 s; `78415f7a` merged; 145 paths, 0 refusals, the same 28 findings by path and verdict, 84 paths shift by at most 0.945 ms on timer phases | `merge/m1x1-idle.log` |

Trial merges with #810, #812 and `dev-soft-core`, and the file scope: `probes/trial_merges.txt`.

Not run: the full sweep and Vivado, as no RTL changed. No hardware or bench access. Nothing pushed.

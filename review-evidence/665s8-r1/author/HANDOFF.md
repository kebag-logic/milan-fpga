# HANDOFF: #868 (#665 S8), wire timing in the split simulation ([A758b], round 2)

Status: REVIEW READY at `bfb2df3707` (every gate of the one clean-clone pass has a passing result; see the gate table). Head `bfb2df3707` (6 round 2 commits on round 1's `086e186e87`, one commit on dev-soft-core `1d6bf5556a`), not pushed. Resumed 2026-11-10T08:44Z after the planned host power-off (07:49 local); the tree was clean, nothing uncommitted.

- Resumed again 2026-11-10T17:03Z after the 16:00Z host reset (memory fault); the tree was clean at `bfb2df3707`, nothing uncommitted. The gate pass at `bfb2df3707` had finished chains A, B, C and the `elaborate-gates-1` re-run; chain D had finished rtl.yml's jobs and shards and five of the named extra gates. Cut by the reset: `budget-1x1` (its log kept in `receipts/gates/extra/cut-at-reset/`, not cited), and not started: `budget-8x8`, `wire-8x8-none`, `wire-8x8-composed` and the full sweep. Restarted: the sweep as four shard units at 17:06Z, and the four gates as `extra2.sh` (the same commands as `extra.sh`) in two units of their own, S2's harness at 17:09Z (CPUs 76-79) and the wire pair on a second clone at 18:28Z (CPUs 84-87, once free); then the two wall-clock re-runs, the LiteX aggregate 18:28Z-18:47Z and `capture_coherence` 19:05Z-19:43Z (gate table). All ended by 19:43Z.
- TAKEN: issuecomment-6755290617 (posted by the first round 2 session; not posted again). REVIEW READY: issuecomment-6777582801 (2026-11-10, the text in `REVIEW-READY-COMMENT.md`). PR body for the manager: `PR-BODY.md`. Authority: the round 2 ruling, issuecomment-6755260058.
- Lane `$LANES/665-s8-wire-timing`, branch `665-s8-wire-timing`; scratch `$VALIDATION_STORAGE/665s8-a758b`.
- Round 2 commits on `086e186e87`:
  1. `79997664d5` the harness at 8x8/2if, the load, the MAAP/ADP/AECP grades, the plants; `tb_split_top.sv` and the split recipe generalised.
  2. `e3ca55422f` the 250 ms tail and the grader's censoring of a command the log ends within the bound of.
  3. `6404b60ba1` the `wire-timing` job in rtl-fast, required by the fast verdict, pinned in `ci_events.py`.
  4. `7af28346ba` docs: the harness page, milan_dp's split recipe, the CI page, the MAAP egress note closed.
  5. `107f3f95de` a timer deadline's load leaves out the ACMP and AECP records (the draws' channels); `run.py` refuses a stimulus whose deadline load reaches them; self-test controls `clean-loaded-script` and `deadline-load-on-a-draw-channel`.
  6. `bfb2df3707` docs only (and one docstring): the README's results at `107f3f95de`, the campaign's four units and their figures, the MAAP note closed over every run, the CI replica's wall time, the dropped records' measured timing. Every run's stimulus regenerates byte-identical at `bfb2df3707` (`receipts/head/stimulus-at-bfb2df3707.txt`).
- First campaign (2026-11-10T01:23Z-06:28Z, the stimulus of `79997664d5`): units 0, 1 (no load) rc 0; units 2, 3 (composed load, the whole burst at every MAAP and ADP deadline) rc 1, one finding each. An ADP deadline's 12 GET_RX_STATEs filled ACMP's ring (room 12: 256 words, 20-word records; the bucket's burst is 16) 56 us before a BIND_RX (unit 2, seed 3, `acmp-bind-63`) and 0.26 us before a PROBE_TX_RESPONSE (unit 3, seed 4, sequence_id 0x0089), and `KL_mbx` dropped each. Receipts `receipts/campaign/first-79997664d5/`. That is the stimulus loading a measured path's own channel, which S2's harness never does; commit 5 answers it. Its restart at `107f3f95de` (06:33Z) was killed by the power-off.
- Campaign at `107f3f95de`: all four units again (the stimulus they read changed since `79997664d5`: the tail and the deadline load), started 2026-11-10T08:46Z, `systemd-run --user --unit=milan-a758b-camp<N> -p MemoryMax=4G taskset -c <range>`, ranges 56-63, 48-55, 40-47, 24-31 from `cpu_ranges.py pick`; seeds 1-4; units 0, 1 no load, 2, 3 composed. All four rc 0, 0 findings, nothing censored, both plants caught; ended 11:18Z-11:21Z (9,086-9,288 s each). Receipts `receipts/campaign/head-107f3f95de/` (`summary.md`; the logs over 200 KB by sha256 and size in `logs.sha256`).
- A gate pass begun at `107f3f95de` at 08:50Z was stopped at 09:00Z, before any job finished: the README's results and the MAAP note quoted the loaded figures of `6404b60ba1` (before commit 5), and the docstring's "6 us" was 56 us, so the docs commit 6 followed the campaign, and the one gate pass runs on its head, `bfb2df3707`, from 11:25Z. The pass at `7af28346ba` (before commit 5) is not cited.
- Head measurements at `107f3f95de` (scratch `m-head/`, `ci-head/`): the CI step from scratch on 4 CPUs, PASS, 578 s (build 68 s, self-test 33 controls 0 failed); 8x8 composed and none on a fresh 8x8 build. Determinism: the 1x1 composed run on the reused build and the CI step's composed run have byte-identical logs and results; the 1x1 and 8x8 unloaded runs at the head are byte-identical (stimulus, log, results) to `6404b60ba1`'s receipts.

## Changes (file:line, reason)

| File:line | Reason |
|---|---|
| `tb/verilator/milan_dp/tb_split_top.sv:49` `N_STREAMS_P` | the datapath's streams at the point's shape (8 at 8x8), forwarded to `milan_datapath` (`:439`) |
| `tb_split_top.sv` mailbox nets (`wire [N-1:0][...]`) | KL_mbx built at its package's interface count; interface 0's slices to `KL_mbx_cdc` |
| `tb_split_top.sv:360` `g_one_if` | one interface: the streams wired as before, so the 1x1 split leg and the twin are byte-identical |
| `tb_split_top.sv:370` `g_bench_streams` | two interfaces: receive a whole frame at a time, interface 0 first at a frame boundary; transmit by `tx_if_o` to the crossing or the bench (ruling item 1: interface 1 driven as S2 drives it, not a second datapath) |
| `tb_split_top.sv:404` `g_bench_if` | interface 1's link from the bench, its commit acknowledged at `MBX_FACE_ACK_CYCLES_C` (S2's `slowest_ack`), windows, grandmaster and face events idle |
| `tb_split_top.sv:399` `p_mbx_tx_*` | each frame's last byte leaving KL_mbx, so the grader pairs commits with frames per interface |
| `tb/verilator/milan_dp/Makefile:857` `SPLIT_SHAPE/STREAMS/IF` | the split recipe at another shape and interface count; past one interface, the generator's variant into `SPLIT_MDIR` (`:876`); the defaults keep the split and twin command lines identical (`make -n` compared) |
| `tb/verilator/ctrl_wire_timing/wire_soc.py:85` | the CPU half at two interfaces (S2's variant sources), and the ledgered memory plan at 8x8/2if (`:102`) |
| `wire_build.py:43` `POINTS` | `8x8`: `endstation_ax7101_8x8`, two interfaces (S2's point) |
| `wire_build.py:48` `LEDGERED` | the platform image at 8x8/2if is 59.0 RAMB36, the planner's one ledgered point `platform-8x8-two-interfaces` (owner ruling 6505997821); the link and the plan name it (`:72`, `:85`) |
| `wire_build.py:92` `streams` | the shape's `N_STREAMS` from the builder's `datapath_params`, never restated |
| `wire_build.py:97` `split_top`, `:109` `same_mailbox` | the recipe at the point; refuses a split-top variant that differs from the CPU half's |
| `wire_main.cpp:121` `LoadItem`, `:490` `offer`, `:513` `define_load` | named loads (frames, and S2-style echoes of the newest sent frame), offered at once (`load`) or a lead before every armed deadline (`onarm`, `:307`) |
| `wire_main.cpp:132` `enqueue` | one queue per interface, ordered by the cycle each frame may go from |
| `wire_main.cpp:431` `bench_fired`, `:456` `bench_drive` | interface 1 at KL_mbx's byte boundary, `RXB`/`TXB` lines |
| `wire_main.cpp:200` `MTX` | KL_mbx egress per frame, interface and channel |
| `wire_main.cpp:565` `wait sent` | end a run after its N-th ANNOUNCE at the MAC |
| `wire_scenario.py:93` `AECP_COMMANDS` | one AEM command per draw, S2's AECP rows in turn (item 3) |
| `wire_scenario.py:117` `draws` | seed 0: round 1's prime steps; another seed: its own generator (the campaign) |
| `wire_scenario.py:151` `load_items`, `:172` `load_lines` | S2's `composed_load` per measured channel, offered before each bind and AEM command and 200 us before every MAAP/ADP deadline (ruling item 3); ADP records target another entity (`:148`), MAAP echoes skip until the first ANNOUNCE (both stated) |
| `wire_scenario.py:83` `TAIL_MS` | 250 ms after the last draw and ANNOUNCE: every command's bound inside the log (commit 2) |
| `wire_grade.py:293` `matched_commits` | commits to KL_mbx egress to MAC frames, per interface; refuses a lost interface 0 frame |
| `wire_grade.py:332` `expiries`, `:348` `expired_arm` | a timer's expiry: no later write of its slot before its millisecond, or at once for a past deadline |
| `wire_grade.py:429` `aecp` | AECP response time, bound 240 ms (`:96`; FR_NFR.md 3.4.1, #868 cites IEEE 1722.1-2021 9.2.1) |
| `wire_grade.py:455` `maap` | B.3.4.2/B.3.4.1 intervals, draws in the reserved range, egress and interval error under the 11 ms reserve (`:103`) |
| `wire_grade.py:498` `adp` | Table 5.50: advertise timer 5000 ms, delay 0-4000 (startup 0-2000), egress under 400 ms (200 at startup), period 4998-9400 ms |
| `wire_grade.py:359` `Window` | a command the log ends within the bound of, unanswered, is censored and reported (commit 2) |
| `run.py:125` `ci`, `:87` `graded` | the CI step (self-test, build, both loads at once); every grade followed by its two plants on the real log |
| `wire_selftest.py` | 4 clean logs and 27 controls; `plants` on real logs |
| `.github/ci-templates/rtl-fast.yml:679` `wire-timing` | the CI job (item 5), timeout 30, elaborate's LiteX/sbt setup under its keys; the fast verdict needs it |
| `.github/workflows/rtl-fast.yml` | regenerated by `scripts/ci_gate_workflows.py` |
| `scripts/ci_events.py:2646` `WIRE_TIMING_JOB`, `:601`, `:633` | the job's step list pinned, its three env-file writers recorded, its result in the verdict's env |
| `docs/testing/CI_WORKFLOWS.md` | the job, its requirement in the verdict, the docs-only skip, its measured wall time |
| `tb/verilator/ctrl_wire_timing/README.md` | round 2's page: points, load, grades, results, campaign, controls |
| `tb/verilator/milan_dp/README.md` | the split recipe's shape and interface variables |
| `sw/firmware/ctrl/maap/README.md:47-50` | the egress note closed with the measured error: 0.26 to 2.46 ms over 36 timer-driven PROBEs and ANNOUNCEs, every interval within 1.7 ms of its draw (commit 6, over the head's seed-0 runs and the campaign) |
| `wire_scenario.py:157` `DRAW_CHANNELS`, `:160` `channel_of` | the channels whose received records the draws measure, and a frame's mailbox channel (commit 5) |
| `wire_scenario.py:167` `load_items(..., leave_out)`, `:190` `load_lines` | a MAAP or ADP deadline's burst leaves out ACMP's and AECP's records; the draws' own bursts are whole (commit 5; the first campaign's two drops) |
| `wire_scenario.py:199` `deadline_load_channels`, `:211` `deadline_loads_clear`; `run.py:74` | a stimulus whose deadline load reaches a draw channel is refused before the model starts (commit 5) |
| `wire_selftest.py:387` | the stimulus controls `clean-loaded-script` and `deadline-load-on-a-draw-channel` (commit 5) |
| `wire_scenario.py:33-39` docstring, `README.md:112-116` | the dropped records' measured timing, 56 us and 0.26 us, and what a deadline's burst then carries (commit 6) |
| `README.md:150` Results, `:186` The local campaign | the head's seed-0 figures; the campaign's four units, their figures and wall time (commit 6) |
| `docs/testing/CI_WORKFLOWS.md:470` | the CI replica's wall time at the head, 578 s (commit 6) |

No firmware, shape config, ring geometry, saved-state, contract, production RTL or `milan_soc.CtrlMailbox` change.

## New checks (planted mutant, failing words)

The self-test (`run.py --self-test`, also the first part of `--ci`) at `107f3f95de`: `33 controls, 0 failed` (`receipts/head/ci-head.console`, lines 1-34).
Every control is a planted mutant of a clean input; each must be refused or found by its own words, and each clean input must pass.

| Control | Planted mutant | Failing words | Acceptance item |
|---|---|---|---|
| `clean-loaded-script` (clean) | none: the 1x1 composed script; its deadline loads reach no draw channel | (must pass) | ruling 3 |
| `deadline-load-on-a-draw-channel` | a GET_RX_STATE added to ADP's deadline load | `the deadline load adp reaches the acmp channel` | ruling 3 (commit 5) |
| `clean`, `clean-announce-interval`, `clean-two-interfaces` (clean) | none | (must pass, no finding) | 1-3 |
| `clean-censored-at-the-end` (clean) | ends 49 ms after an unanswered command | (must pass, the command reported censored) | 3 (commit 2) |
| `shifted-clock` | the clean log graded at 125 MHz (#868 item 4) | `the clock is shifted` | 4 |
| `drifted-milliseconds` | one millisecond one cycle late | `the clock is shifted` | 4 |
| `missing-response` | the first BIND_RX_RESPONSE gone | `has no BIND_RX_RESPONSE` | 1 |
| `late-response` | each response 200 ms after its command | `acmp.bind_rx: 200.0 ms is not under 200.0 ms` | 1 |
| `unhandled-answer` | the handling's arm gone, the PROBE_TX's own arm kept after the answer | `was never handled` | 1 |
| `handled-on-another-slot` | the handling armed on another slot | `was never handled` | 1 |
| `frame-before-commit` | a commit moved past its frame's first byte | `before its commit` | grader integrity (1-3) |
| `incomplete-model` | the model's tally gone | `did not complete` | grader integrity (1-3) |
| `no-mailbox-egress` | every `MTX` line gone | `no KL_mbx egress` | grader integrity (1-3) |
| `egress-without-commit` | a frame leaving `KL_mbx` with no commit | `frames left KL_mbx after` | grader integrity (1-3) |
| `bench-frames-counted-as-interface-0` | at two interfaces, interface 1's frames logged as interface 0's | `never reached the MAC` | grader integrity (1-3) |
| `missing-aecp-response` | the first AEM response gone | `has no final response` | 3 |
| `late-aecp-response` | each AEM response 240 ms after its command | `aecp.response: 240.0 ms is not under 240.0 ms` | 3 |
| `aecp-in-progress` | an IN_PROGRESS answer before each final response | `IN_PROGRESS answers` | 3 |
| `unanswered-before-the-end` | a command 300 ms before the log ends, unanswered | `has no final response` | 3 |
| `egress-past-reserve` | the third PROBE 11 ms and one cycle late at the MAC (#868 item 4) | `maap.egress: 11.` | 4 |
| `interval-error-past-reserve` | the next deadline armed 11 ms after its PROBE left | `maap.interval_error: 11.` | 2 |
| `probe-draw-outside-reserve` | a probe interval drawn at 590 ms | `outside the reserved 511 to 589 ms` | 2 |
| `probe-interval-outside-clause` | the second PROBE 42 ms late, its interval 600.03 ms | `is not strictly inside 500 to 600 ms` | 2 |
| `maap-frame-on-no-expiry` | the first probe deadline's arm gone | `left on no expired timer` | 2 |
| `maap-expiry-cancelled` | that deadline cancelled before it came | `left on no expired timer` | 2 |
| `announce-interval-outside-clause` | the second ANNOUNCE 1,001 ms late | `is not strictly inside 30000 to 32000 ms` | 2 |
| `no-announce-interval` | the second ANNOUNCE gone | `ANNOUNCEs left the MAC, the run asked for 2` | 2 |
| `advertise-timer-not-5s` | every advertise timer armed for 4,999 ms | `not 5000 ms` | 3 |
| `adp-delay-outside-table` | a delay drawn at 4,001 ms | `outside 0 to 4000 ms` | 3 |
| `adp-egress-past-ceiling` | every ENTITY_AVAILABLE 400 ms after its delay | `adp.egress: 400.` | 3 |
| `available-sent-twice` | the same expiry's ENTITY_AVAILABLE sent twice, a millisecond apart | `adp.advertise_period: 1.000 ms` | 3 |

After every run (each CI run, each 8x8 run, each campaign unit), two plants on that run's own log, each must be caught (`run.py` exits 1 on an escaped plant):

| Plant | Planted mutant | Failing words | Item |
|---|---|---|---|
| `egress-past-reserve` | the first timer-driven PROBE moved 12 ms later at the MAC, past the 11 ms reserve | `maap.egress: ... is not under 11.0 ms` | 4 |
| `shifted-clock` | the log graded at 125 MHz | `the clock is shifted` | 4 |

CI (item 5): `scripts/ci_events.py` pins the `wire-timing` job's step list, its env-file writers and its result in the fast verdict, which `ci_events.py --check` compares with the workflow (docs.yml's docs-gates-2, rtl.yml's full-ci-gate), so a dropped or reordered step fails it; the job's run is the gate table's `rtl-fast / wire-timing` row.

## Measurements

See `receipts/measure/summary-short.md`.

## Gate table

One clean-clone pass at `bfb2df37079f0172d6e94841ea5b9bd084e3ee06`, each workflow job on its own fresh clone (`gates/run_wf.py`, verified by `gates/verify_wf.py` / `verify_docs_yml.py` from the workflow at the head, so a step missing from a table is a red). Chains A to D ran 11:25Z-15:49Z on 4-CPU ranges of the session pool (100-103, 108-111, 116-119, 124-127) at host load 82-87; the gates the 16:00Z reset cut ran 17:06Z-19:43Z. Receipts: `receipts/gates/` (runner scripts, tables, `jobs.txt`, every step log and rc under 200 KB; larger logs by sha256 and size in each directory's `large.sha256`), `receipts/sweep/` (each shard's spec, result, summary, preflight and suite logs; the `capture_coherence` re-run). Paths in the table's last column are under `receipts/`.

| Gate | Command / runner | Result | Receipt |
|---|---|---|---|
| `rtl-fast.yml`, 18 jobs, every `run:` step | `run_wf.py rtl-fast` per job (LiteX venv for `firmware-boundary`, `wire-timing`) | 56 steps rc 0, 64 not run with a stated reason, 0 bad | `gates/rtl-fast-table.md` |
| `rtl-fast / wire-timing` (item 5) | step `python3 tb/verilator/ctrl_wire_timing/run.py --ci` | rc 0, `33 controls, 0 failed`, both runs `0 finding(s)`, both plants caught per run, `PASS, wall 2317 s` (build 445 s); results, wire text, UART and logs byte-identical to the head measurement at `107f3f95de` | `gates/rtl-fast/logs/rtl-fast__wire-timing__ci_step_20.log`, `gates/wire-timing-ci-vs-head.txt` |
| firmware self-test | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` in `firmware-unit`, `-control-mutants`, `-aecp-mutants`, `-srp-mutants` | rc 0 each, `test_ctrl_firmware: PASS`; control shard `mutants: 570 of 570 caught` | `gates/rtl-fast/logs/*firmware-*__ci_step_9.log`, `*firmware-unit__ci_step_10.log` |
| coverage ratchet | `fw_coverage.py --selftest`, `--check` (`firmware-unit` step 12) | rc 0, `firmware coverage: PASS (35 files)` | `gates/rtl-fast/logs/rtl-fast__firmware-unit__ci_step_12.log` |
| behave | `cd tests && behave --no-capture -f plain` (`bdd-conformance` step 5) | rc 0, 508 scenarios, 2330 steps passed, 0 failed | `gates/rtl-fast/logs/rtl-fast__bdd-conformance__ci_step_5.log` |
| `docs.yml`, 9 jobs, every `run:` step | `run_docs_yml.py` per job | 64 steps rc 0, 31 not run with a stated reason, 0 bad | `gates/docs-yml-table.md` |
| `elaborate.yml`, 6 jobs, every `run:` step | `run_wf.py elaborate` per job | 13 steps rc 0, 33 not run with a reason; `elaborate-gates-1` gate_19 (the LiteX aggregate) below | `gates/elaborate-table.md` |
| `elaborate-gates-1` gate_19 | `scripts/run_litex_sims.sh --selftest`, then the aggregate | attempts 1 and 2 (whole job, fresh clones, CPUs 116-119 at load 82-87): rc 92, 7 of 8 PASS, `test_soc_timing_cuts` killed at its 900 s member wall clock, `result UNKNOWN, not a failure`, the script's own instruction being "re-run it uncontended". Attempt 3 (the step alone in attempt 2's clone, `gates/run_step.py`, CPUs 20-23 free): rc 0, `simulations: 8 passed: 8`, `test_soc_timing_cuts` 832 s, tree clean. The branch changes nothing under `sw/litex` or `scripts/run_litex_sims.sh` | `gates/elaborate/first-attempt-gates-1/`, `gates/elaborate/logs/*gate_19*`, `gates/elaborate/litex-sim-logs-attempt{1,2,3}/` |
| `rtl.yml` `full-ci-gate` | `run_wf.py rtl full-ci-gate` (ACT=true) | rc 0, `draft=false rtl=true run_full=true` | `gates/rtl-table.md` |
| `rtl.yml` `yosys-shards` 0-3 | `syn/yosys/run.sh --shard k/4` | rc 0 each, `RESULT: PASS`; tree clean after | `gates/rtl/logs/rtl-yosys-shard-*.log` |
| `rtl.yml` `verilator-shards`: the full sweep | `native-shards.py` 4 units, `MAKEFLAGS=-j4 --no-print-directory`, CPUs 56-59, 60-63, 48-51 (shard 2, capture_coherence, 4 CPUs), 52-55; started 17:06Z | shard 0: 15/15, 360,992 checks, rc 0, 6,117 s; shard 1: 17/17, 1,526,104 checks, rc 0, 5,821 s; shard 3: 16/16, 21,575 checks, rc 0, 5,801 s; shard 2: 16 of 17 passed, 0 failed, `capture_coherence` TIMEOUT at its 2,400 s wall clock (rc 92, `result UNKNOWN, not a failure`; it ran 17:52Z-18:32Z on CPUs 48-51, which another lane's sweep shard on 48-55 also used, 17:07Z-18:23Z, at about 3.3 CPUs on average by its journal), 284,186 checks, 7,085 s. Preflight (incl. `test_suite_cancellation.py`) PASS in all four. `capture_coherence` re-run below | `sweep/shard-k/spec-01.log`, `spec-results.json`, `logs/` |
| `capture_coherence` re-run | `timeout 2400 make -C tb/verilator/capture_coherence`, then `suite_tally.py --verdict` (the sweep's own per-suite command), fresh clone, CPUs 84-87 free, sweep env (`cc_rerun.sh`) | rc 0 in 2,262 s (19:05Z-19:43Z, inside the 2,400 s wall clock), `suite_tally.py --verdict` rc 0; `capture_coherence: checks: 20832 failures: 0`, `capture_coherence_dp: checks: 847 failures: 0`, mutant arm `42 checks: 42 PASS, 0 FAIL`; tree clean. With it the sweep is 65 of 65 suites | `sweep/capture_coherence-rerun/` |
| `rtl.yml` `physical-gptp` | not triggered by a pull request (`if:` schedule or workflow_dispatch); run anyway | step 11 rc 2 twice (#833 procedure: re-run once, both kept): the preflight `test_suite_cancellation.py` timed out at `process_test_support.py:215` `wait(timeout=12)` at load 82-87; the same preflight at the same head passed in all four sweep shards at 17:06Z | `gates/rtl/first-attempt-gptp/`, `gates/rtl/logs/` |
| `git diff --check` against the merge base `1d6bf5556a` | `extra.sh` | rc 0 | `gates/extra/logs/diff-check.log` |
| tally mutants | `sw/firmware/gtest/tally_selftest.py --mutants` | rc 0, `listener defects: 18 of 18 caught` | `gates/extra/logs/tally-mutants.log` |
| saved-state self-test | `test_ctrl_nvm.py --require-rv32 --self-test --jobs 8` | rc 0, 5 shapes, 435 tests, 109 of 109 planted defects | `gates/extra/logs/nvm-self-test.log` |
| `test_builder.py --require-rv32` | LiteX venv | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`: gate 1b's `MAKEFLAGS += -e` mutant has no effect on this make, gate 11 needs a placed Vivado report (no route in this lane) | `gates/extra/logs/test-builder.log` |
| S2's harness, self-test | `ctrl_service_budget/run.py --self-test` | rc 0, `self-test: 0 failures` | `gates/extra/logs/budget-self-test.log` |
| S2's harness at 1x1/1if | `run.py --point 1x1 --record-budget-findings` | rc 0, `18 groups graded, 0 refusals` (34 recorded T_svc misses: S2b's budget findings, which this flag records); the harness reads nothing this branch changes | `gates/extra/logs/budget-1x1.log` |
| S2's harness at 8x8/2if | `run.py --point 8x8 --record-budget-findings` | rc 0, `17 groups graded, 0 refusals` (63 recorded T_svc misses, S2b's) | `gates/extra/logs/budget-8x8.log` |
| wire timing at 8x8/2if, no load and composed | `ctrl_wire_timing/run.py --point 8x8 --draws 16 --load none`, then `--reuse-build --load composed` (`WIRE_JOBS=4` on 4 CPUs) | rc 0 each, `0 finding(s)`, both plants caught; results, wire text, UART and logs byte-identical to `107f3f95de`'s | `gates/extra/logs/wire-8x8-*.log`, `gates/wire-8x8-vs-head.txt` |

The `wire-timing` job's local wall time in this pass, 2,317 s for the step, is on 4 CPUs of the session pool at 100% use (the same step took 578 s on four CPUs at `107f3f95de`, `receipts/head/ci-head.console`); a hosted runner's 4 vCPUs are its own. The hosted figure is the measurement item 5 needs and it is open until the PR runs.

### rtl.yml physical-gptp, step 11 (#833 procedure)

- Attempt 1 at `bfb2df3707` (11:28Z, CPUs 124-127): rc 2, `ABORTING: sweep cancellation controls failed.`; `scripts/test_suite_cancellation.py` raised `TimeoutExpired` at `process_test_support.py:215` (`self.process.wait(timeout=12)`) in `cancel-transition-SIGTERM`.
- Attempt 2 (re-run once on a fresh clone, 11:30Z, CPUs 104-107): rc 2, the same raise (`wait(timeout=12)`) in a later case, `hard-HUP` (`hard_stop`), every case before it passing.
- Both results kept (`gates/rtl/first-attempt-gptp/`, `gates/rtl/logs/`). At `7af28346ba` the same step also failed both attempts the same way.
- Diagnosis, not a third attempt: the fixture the test builds takes only `scripts/run_all_suites.sh`, `owned_process.py`, `suite_shards.py`, `suite_tally.py` and its own support, and `git diff 1d6bf5556a bfb2df3707` is empty for all six (the branch's only `scripts/` change is `ci_events.py`). The same step at the base `1d6bf5556a`, same runner, CPUs 104-107, 11:42Z: the preflight passed (its output is printed only on failure) and the suite began; I cancelled it through its owner after 685 s (`CANCELLED: signal 15`), the comparison being the preflight. Host load average 82 to 87 throughout.
- After the reset, the same `test_suite_cancellation.py` passed at `bfb2df3707` in all four sweep shards' preflights (17:06Z-17:08Z, `receipts/sweep/shard-k/logs/preflight/test_suite_cancellation.log`: `suite cancellation: PASS`).
- The job is outside the bar: `rtl.yml`'s `physical-gptp` runs only on `schedule` or `workflow_dispatch` (its `if:`), and `docs/testing/CI_WORKFLOWS.md:726-729` says PR and push events exclude it. It was run as extra evidence; its suite never started at the head in this pass. A third attempt was not made.

### Remaining risks

- Item 5's hosted wall time (above).
- `capture_coherence` took 2,262 s of its 2,400 s wall clock uncontended on 4 CPUs, and `test_soc_timing_cuts` 832 s of its 900 s. Both are existing members whose inputs this branch either does not change (`sw/litex`) or changes only in the split recipe's new variables (`capture_coherence` reads milan_dp's `print-srcs` and `print-dp-vflags`, whose output is byte-identical at the base and the head, `receipts/regress/milan_dp-print-targets.txt`); the margins are theirs, not this lane's.
- The open question on the timers' load (PR body, Known limitations): a deadline's burst leaves out ACMP's and AECP's records.


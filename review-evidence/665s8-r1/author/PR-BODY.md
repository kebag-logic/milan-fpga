[A758b]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why, the measurements and the campaign.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result, and the gate table.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, why, and the one open question.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `bfb2df3707`; hosted runs pending. `665-s8-wire-timing` -> `dev-soft-core`.

- Acceptance items 1 to 5 are met, with measurements below. Item 5's hosted wall time will come from the first hosted run; the job's own 30-minute timeout enforces it. One question for the reviewers is open on the timers' load ([below](#known-limitations--out-of-scope)).
- Clean-clone pass at the head: every `run:` step of the four workflows a pull request runs either passes or is not run, with a stated reason. Two members needed a re-run because a wall clock killed them on a shared host. Both passed uncontended. The [gate table](#gate-table) has the detail.
- The full sweep ran as four shard units: 65 of 65 suites, 0 failed. 64 passed in the sweep, with 2,192,857 checks. `capture_coherence` hit its 2,400 s wall clock on CPUs that another sweep was also using, and passed when re-run uncontended (21,721 checks).

## Linked Issue / roles

Closes #868
Relates to #665

Executor: `[A758b]` (round 2; round 1 was `[A758]`)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

This PR adds the split placement's wire timing in simulation (#665 S8). It runs at both points the round 2 ruling ([issuecomment-6755260058](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6755260058)) names, without and with the stated background load, and grades offline.
Round 1 (`086e186e87`) built the harness and graded item 1 at 1x1. This round adds:

| Piece | What it does |
|---|---|
| `tb/verilator/milan_dp/tb_split_top.sv`, `Makefile` | the split top and its recipe at another shape and interface count (ruling item 1, option (a)): `SPLIT_SHAPE`, `SPLIT_STREAMS` and `SPLIT_IF`; past one interface, the contract generator's variant. Interface 0 goes through `KL_mbx_cdc` to the datapath. Interface 1 is not a second datapath: the bench drives it as S2 drives `KL_mbx` (link, frames at the mailbox's byte boundary, the commit acknowledged at `MBX_FACE_ACK_CYCLES_C`, windows idle). With the defaults the 1x1 split leg's and the twin's command lines and captures are byte-identical. No change to `milan_soc.CtrlMailbox`, `sw/mailbox/mailbox.yaml` or production RTL |
| `tb/verilator/ctrl_wire_timing/wire_soc.py`, `wire_build.py` | the 8x8 point with two interfaces; the platform image there is the planner's ledgered `platform-8x8-two-interfaces` (59.0 RAMB36, owner ruling 6505997821), named in the link and the CPU half's plan |
| `wire_main.cpp`, `wire_scenario.py` | named loads (ruling item 3): S2's `composed_load`, offered before each bind and AEM command and 200 us before every armed MAAP and ADP deadline; one AEM command per draw; seeds; the 250 ms tail; the run ends after its N-th ANNOUNCE. A deadline's burst leaves out the ACMP and AECP records, the draws' channels, and `run.py` refuses a stimulus whose deadline load reaches them (see [the open question](#known-limitations--out-of-scope)) |
| `wire_grade.py` | the AECP response time (item 3; 240 ms); MAAP's probe and announce intervals against B.3.4.2 and B.3.4.1, its draws against the reserved range, each frame's egress and each interval's error against the 11 ms reserve (item 2, ruling item 5); ADP's advertise period against Table 5.50 (item 3); commits paired per interface through KL_mbx's egress; a command the log ends within the bound of is reported as censored |
| `wire_selftest.py`, `run.py` | the self-test: the stimulus check (one clean loaded script, one planted), 4 clean logs and 27 log controls, 33 in all; after every run, two plants on its own log, an egress delay past the reserve and a grader with a shifted clock (item 4) |
| `.github/ci-templates/rtl-fast.yml` (and the generated workflow), `scripts/ci_events.py` | the `wire-timing` job (item 5): one gate step, `run.py --ci`, the 1x1 short paths without and with the load; required by the `rtl-fast` verdict; pinned in the event contract |
| docs | the harness page, milan_dp's split recipe, the CI page, and the `sw/firmware/ctrl/maap/README.md:47` note closed with the measured egress error |

### Measurements, 16 draws a run, seed 0

Every run is 16 ACMP and AECP draws, each run to its first ANNOUNCE and 250 ms on.
Each cell is N: min / mean / max, in ms unless marked us:

| Path (N: min / mean / max ms) | bound ms | 1x1 none | 1x1 composed | 8x8/2if none | 8x8/2if composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 16: 0.378 / 0.665 / 0.968 | 16: 0.625 / 1.183 / 3.403 | 16: 0.383 / 0.900 / 1.708 | 16: 0.758 / 12.212 / 17.651 |
| `acmp.probe_tx` | 200.0 | 16: 0.399 / 0.909 / 1.080 | 16: 0.399 / 2.973 / 5.263 | 16: 0.841 / 1.175 / 2.177 | 16: 0.841 / 1.860 / 5.763 |
| `acmp.probe_tx.entity` | - | 16: 0.177 / 0.458 / 0.839 | 16: 0.219 / 2.522 / 4.540 | 16: 0.180 / 0.725 / 1.456 | 16: 0.180 / 1.409 / 5.042 |
| `aecp.response` | 240.0 | 16: 0.872 / 1.611 / 2.248 | 16: 2.945 / 3.569 / 4.151 | 16: 1.518 / 2.211 / 3.178 | 16: 4.035 / 9.783 / 20.567 |
| `maap.egress` | 11.0 | 4: 0.744 / 0.815 / 0.872 | 4: 0.798 / 1.477 / 2.306 | 4: 0.927 / 1.222 / 1.460 | 4: 1.425 / 1.848 / 2.455 |
| `maap.probe_interval` | 600.0 | 3: 512.915 / 530.368 / 559.068 | 3: 513.491 / 531.374 / 560.240 | 3: 515.467 / 539.808 / 582.677 | 3: 516.544 / 540.547 / 583.672 |
| `maap.interval_error` | 11.0 | 3: 0.068 / 0.091 / 0.120 | 3: 0.491 / 1.041 / 1.391 | 3: 0.279 / 0.474 / 0.677 | 3: 0.425 / 1.214 / 1.672 |
| `adp.egress` | 400.0 | 1: 0.838 / 0.838 / 0.838 | 1: 1.550 / 1.550 / 1.550 | 1: 0.911 / 0.911 / 0.911 | 1: 2.207 / 2.207 / 2.207 |
| `egress.acmp.first` | - | 48: 0.36 / 0.37 / 0.37 us | 240: 0.36 / 0.36 / 0.37 us | 48: 0.36 / 0.36 / 0.37 us | 240: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 5: 0.36 / 0.36 / 0.37 us | 12: 0.36 / 0.37 / 0.37 us | 5: 0.36 / 0.36 / 0.37 us | 9: 0.36 / 0.37 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load offers |
|---|---:|---|---:|---:|---|
| 1x1 none | 0 | none | 1935 | 49.102 | none |
| 1x1 composed | 0 | none | 1935 | 49.102 | acmp 16, adp 2, aecp 16, maap 5 |
| 8x8/2if none | 0 | none | 2001 | 115.271 | none |
| 8x8/2if composed | 0 | none | 2001 | 115.271 | acmp 16, adp 2, aecp 16, maap 5 |

Measured at `107f3f95de`; the head `bfb2df3707` changes only documentation and one docstring, and regenerates each run's stimulus byte for byte. The 1x1 runs are the CI step's own (from scratch, 578 s on four CPUs: build 68 s, then both runs at once); the 8x8 runs are on one fresh build, 679 s for the loaded one. The gate pass repeated the CI step and both 8x8 runs at the head, on clean clones, and reproduced every run's results and log byte for byte ([gate table](#gate-table)).

- ACMP (item 1): the slowest transaction is the loaded 8x8 bind at 17.7 ms, 182.3 ms inside Table 5.26's 200 ms.
- AECP (item 3): the slowest response is the loaded 8x8's at 20.6 ms, 219.4 ms inside 240 ms.
- MAAP (item 2, ruling item 5): round 1's three probe gaps, recomputed from its own log (PROBE first byte to first byte), are 558.713, 519.341 and 513.012 ms, each strictly inside B.3.4.2's 500 to 600 ms. The grader now grades that acquisition on every run; at the head's unloaded 1x1 stimulus it is 559.068, 519.120 and 512.915 ms, the stimulus having changed since round 1. Each frame's egress is at most 2.5 ms and each interval within 1.7 ms of its draw, inside the 11 ms reserve.

### The campaign (ruling item 2)

Four units at 1x1 on one build at `107f3f95de`, side by side, each to its second ANNOUNCE and 250 ms on, no time compression, 342 draws each. Each unit is one command (unit 0 shown in [How to validate](#how-to-validate)); seeds 1 to 4, loads none, none, composed, composed. Started 2026-11-10T08:46Z; wall time 9,086 to 9,288 s a unit (2.5 to 2.6 h), about 3.8 ms of simulated time a second, each a single-threaded process on a shared host.

| Path (N: min / mean / max ms) | bound ms | unit 0, seed 1, none | unit 1, seed 2, none | unit 2, seed 3, composed | unit 3, seed 4, composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 342: 0.356 / 0.708 / 2.560 | 342: 0.355 / 0.748 / 2.627 | 342: 0.380 / 1.285 / 5.324 | 342: 0.379 / 1.257 / 3.623 |
| `acmp.probe_tx` | 200.0 | 342: 0.399 / 1.050 / 2.839 | 342: 0.399 / 1.165 / 4.490 | 342: 0.399 / 2.759 / 5.351 | 342: 0.399 / 2.847 / 5.318 |
| `acmp.probe_tx.entity` | - | 342: 0.166 / 0.576 / 2.420 | 342: 0.171 / 0.641 / 3.534 | 342: 0.163 / 2.261 / 5.025 | 342: 0.164 / 2.354 / 4.965 |
| `aecp.response` | 240.0 | 342: 0.834 / 1.731 / 4.093 | 342: 0.841 / 1.729 / 3.937 | 342: 1.813 / 3.495 / 6.431 | 342: 1.856 / 3.491 / 6.730 |
| `maap.egress` | 11.0 | 5: 0.448 / 0.752 / 1.026 | 5: 0.438 / 0.563 / 0.681 | 5: 0.264 / 1.410 / 2.267 | 5: 0.940 / 1.542 / 2.191 |
| `maap.probe_interval` | 600.0 | 3: 513.099 / 530.419 / 558.773 | 3: 513.138 / 530.300 / 559.006 | 3: 514.098 / 531.166 / 559.592 | 3: 513.458 / 531.088 / 560.389 |
| `maap.interval_error` | 11.0 | 4: 0.099 / 0.305 / 0.509 | 4: 0.006 / 0.151 / 0.243 | 4: 0.003 / 0.625 / 1.098 | 4: 0.418 / 0.856 / 1.389 |
| `maap.announce_interval` | 32000.0 | 1: 31956.491 / 31956.491 / 31956.491 | 1: 31956.784 / 31956.784 / 31956.784 | 1: 31956.997 / 31956.997 / 31956.997 | 1: 31958.159 / 31958.159 / 31958.159 |
| `adp.egress` | 400.0 | 6: 0.443 / 0.695 / 0.815 | 6: 0.335 / 0.606 / 0.839 | 6: 0.789 / 1.081 / 1.609 | 6: 1.155 / 1.602 / 2.098 |
| `adp.advertise_period` | 9400.0 | 5: 5362.967 / 6820.442 / 8386.951 | 5: 5363.043 / 6820.099 / 8385.684 | 5: 5363.180 / 6820.759 / 8386.078 | 5: 5364.174 / 6821.812 / 8387.581 |
| `egress.acmp.first` | - | 1026: 0.36 / 0.36 / 0.37 us | 1026: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 6: 0.36 / 0.37 / 0.37 us | 6: 0.36 / 0.36 / 0.37 us | 33: 0.36 / 0.36 / 0.37 us | 34: 0.36 / 0.37 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load offers |
|---|---:|---|---:|---:|---|
| unit 0, seed 1, none | 0 | none | 34703 | 49.102 | none |
| unit 1, seed 2, none | 0 | none | 34706 | 49.102 | none |
| unit 2, seed 3, composed | 0 | none | 34705 | 49.102 | acmp 342, adp 12, aecp 342, maap 6 |
| unit 3, seed 4, composed | 0 | none | 34690 | 49.102 | acmp 342, adp 12, aecp 342, maap 6 |

- B.3.4.1: each announce interval is 31,956.5 to 31,958.2 ms, strictly inside 30 to 32 s and 41.8 ms or more below the ceiling; every interval is within 1.4 ms of its draw and MAAP's egress at most 2.3 ms on all 20 timer-driven frames.
- Table 5.50: each advertise period is 5,363.0 to 8,387.6 ms, inside 5 to 9 s; each ENTITY_AVAILABLE leaves within 2.1 ms of its delay.
- Over the 1,368 draws the slowest transaction is an AEM response at 6.7 ms, and the slowest ACMP one 5.4 ms.

The units' receipts:

| Unit | Seed | Load | Start (UTC) | End (UTC) | rc | `results.json` sha256 | `wire.log` sha256, bytes |
|---|---:|---|---|---|---:|---|---|
| 0 | 1 | none | 2026-11-10T08:46:38Z | 2026-11-10T11:21:26Z | 0 | `36cc704d8e35cf45` | `9e5c33c0148c197e`, 1306201 |
| 1 | 2 | none | 2026-11-10T08:46:42Z | 2026-11-10T11:18:08Z | 0 | `16c21c8b9f7e18f5` | `9458dd9f67d23954`, 1306261 |
| 2 | 3 | composed | 2026-11-10T08:46:45Z | 2026-11-10T11:18:54Z | 0 | `84c985c107b627b9` | `9d6085a8e6fd4de3`, 12765770 |
| 3 | 4 | composed | 2026-11-10T08:46:48Z | 2026-11-10T11:19:07Z | 0 | `5d9e787be5a29317` | `40ee89f0dd5232a0`, 12766771 |

**The first campaign** ran the same four units at `79997664d5`, when a MAAP or ADP deadline's burst still carried ACMP's and AECP's records. Units 0 and 1 passed. Units 2 and 3 each had one finding: an ADP deadline's 12 GET_RX_STATEs filled ACMP's ring (room 12) 56 us before a BIND_RX (seed 3) and 0.26 us before a PROBE_TX_RESPONSE (seed 4), and `KL_mbx` dropped each. That is the stimulus loading a measured path's own channel, which S2's composed load never does; `107f3f95de` leaves those records out of a deadline's burst and refuses a stimulus whose deadline load reaches them. Under the whole burst those two units measured the timers inside their clauses: announce intervals 31,956.7 and 31,956.8 ms, advertise periods 5,364.1 to 8,386.6 ms, MAAP egress at most 1.9 ms, ADP egress at most 2.7 ms.

## Authoritative references

- #868 acceptance 1 to 5, and the round 2 ruling, issuecomment-6755260058.
- Milan v1.2 5.5.2.3 and Table 5.26 (ACMP, 200 ms); Table 5.50 and 5.6.3.5 (ADP advertise timer and delays).
- IEEE 1722-2016 B.3.4.1 and B.3.4.2 (MAAP announce and probe intervals), B.3.6.1 (the seed), Table B.4.
- IEEE 1722.1-2021 9.2.1 (as #868 names the AECP response); the bound, 240 ms, is `docs/reference/FR_NFR.md` 3.4.1's (IEEE 1722.1-2021 9.3.2.6, Milan v1.2 5.4.3.4, NFR-LAT-02).
- `sw/firmware/ctrl/maap/README.md:43-47` (the 11 ms reserve and the egress note).
- `docs/design/SPLIT_CONTROL_MEMORY.md` section 5 (the ledgered point).
- `tb/verilator/ctrl_service_budget` (S2's split SoC, frames and composed load), read only.

## How to get into the same state

```sh
git fetch origin 665-s8-wire-timing
git checkout --detach bfb2df37079f0172d6e94841ea5b9bd084e3ee06
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The product LiteX tree with the patch series applied, the pinned RV32 SDK, Verilator 5.050 and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`), as `tb/verilator/ctrl_service_budget/README.md` states.

## How to validate

```sh
python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test
python3 -B tb/verilator/ctrl_wire_timing/run.py --ci --build-dir /tmp/wire-ci
python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir /tmp/wire-8x8 --draws 16 --load none --out /tmp/wire-8x8-none
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-8x8 --reuse-build --draws 16 --load composed --out /tmp/wire-8x8-composed
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir /tmp/wire-ci --seed 1 --load none --out /tmp/camp0
```

Expected result / pass criteria: the self-test prints `33 controls, 0 failed`; every run prints `0 finding(s)` and both plants `caught`; `--ci` ends `PASS`.
The last line is campaign unit 0; units 1 to 3 take seeds 2, 3 and 4 with loads none, composed and composed.

### Gate table

The pass ran once at `bfb2df37079f0172d6e94841ea5b9bd084e3ee06`. Each workflow job ran on its own fresh clean clone. The step list was read from the workflow at the head, so a step missing from the record fails the check. Steps that only make sense on a hosted runner were not run, each with its reason recorded: the apt package resolution, the tool installs whose pinned builds are present locally, and the hosted step records.

| Gate | Result |
|---|---|
| `rtl-fast`, all 18 jobs | 56 steps rc 0, 64 not run with a reason, 0 failed |
| `rtl-fast / wire-timing` (item 5): `python3 tb/verilator/ctrl_wire_timing/run.py --ci` | rc 0. `33 controls, 0 failed`; both runs `0 finding(s)`; both plants caught on each run. Results and logs byte-identical to the measurements above. Wall time 2,317 s, of which the build took 445 s, on four CPUs that other work was keeping fully busy (see the note under this table) |
| firmware self-test, `test_ctrl_firmware.py --require-rv32 --self-test`, four shards | rc 0 each; the control shard reports `mutants: 570 of 570 caught` |
| `fw_coverage.py --selftest`, `--check` | rc 0, `firmware coverage: PASS (35 files)` |
| `cd tests && behave` | rc 0, 508 scenarios and 2,330 steps passed, 0 failed |
| `docs`, all 9 jobs | 64 steps rc 0, 31 not run with a reason, 0 failed |
| `elaborate`, all 6 jobs | 13 steps rc 0, 33 not run with a reason. The LiteX aggregate (`elaborate-gates-1`) was killed twice at the 900 s member wall clock on a loaded host (`test_soc_timing_cuts`, rc 92, `result UNKNOWN`). Re-run uncontended, as the script's rc 92 message says to do: 8 of 8 passed, `test_soc_timing_cuts` in 832 s. This branch changes nothing that simulation reads |
| `rtl / full-ci-gate` | rc 0, `rtl=true run_full=true` |
| `rtl / yosys-shards`, 0 to 3 | rc 0 each, `RESULT: PASS` |
| `rtl / verilator-shards`: the full sweep as four shard units | Shard 0: 15/15, 360,992 checks. Shard 1: 17/17, 1,526,104 checks. Shard 3: 16/16, 21,575 checks. Shard 2: 16 of 17 passed, 0 failed, 284,186 checks; `capture_coherence` was killed at its 2,400 s wall clock (rc 92, `result UNKNOWN`) on CPUs another sweep was also using. Re-run uncontended with the sweep's own per-suite command and verdict check, on a fresh clone: rc 0 in 2,262 s, 20,832 + 847 + 42 checks, 0 failures. The suite builds the datapath through milan_dp's Makefile, so it reads this branch's change. The cancellation preflight passed in all four shards |
| `rtl / physical-gptp` | Not run on a pull request: the job's condition is schedule or dispatch only. It was run anyway. Step 11 stopped both times in its cancellation preflight, a `wait(timeout=12)` under host load (#833: re-run once, both results kept). The same preflight at this head passed in all four sweep shards |
| `git diff --check` against the merge base `1d6bf5556a` | rc 0 |
| `tally_selftest.py --mutants`; `test_ctrl_nvm.py --require-rv32 --self-test` | rc 0: `18 of 18`; 5 shapes, 435 tests, 109 of 109 planted defects caught |
| `test_builder.py --require-rv32` | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`. Not run: gate 1b's `MAKEFLAGS += -e` mutant, which has no effect on this make, and gate 11, which needs a placed implementation report |
| S2's harness: `ctrl_service_budget/run.py --self-test`, `--point 1x1`, `--point 8x8` (both with `--record-budget-findings`) | rc 0 each. 1x1: 18 groups graded, 0 refusals. 8x8: 17 groups graded, 0 refusals. The T_svc misses they record are S2b's findings. The harness reads nothing this branch changes |
| wire timing at 8x8/2if, without load and with the composed load | rc 0 each, `0 finding(s)`, both plants caught. Byte-identical to the measurements above |

The wire-timing step's local wall time differs between two runs on four CPUs. In this pass it took 2,317 s, on CPUs the other work kept fully busy. The earlier run took 578 s. A hosted runner's four vCPUs are not shared. The hosted run's time is the figure that settles item 5's 30-minute budget.

## Known limitations / out of scope

- Out of scope, as #868 states: 32x32 (#859), the service budget itself (S2b) and bench confirmation (S12). `ctrl_service_hooks` is #869 (ruling item 6).
- Interface 1 at 8x8 is driven from the bench and has no datapath (ruling item 1); its figures are not graded. Every figure is interface 0's.
- The announce interval and the advertise period are graded at 1x1 in the local campaign (ruling item 2), not in CI and not at 8x8.
- MAAP draws its intervals from an xorshift32 seeded with the MAC plus NOW_MS at `maap_begin` (B.3.6.1), which the boot fixes in a cycle-true model, so every run at a point draws the same intervals; the seeds move the stimulus and its load against each expiry.
- The MAC core's and the PHY's own pipeline delays are outside the simulation (a fixed sub-microsecond each way); the CSR window's AXI4-Lite access is the testbench's; the flash is blank; the firmware polls the mailbox.
- The load differs from S2's composed load in three stated ways ([the harness page](../tb/verilator/ctrl_wire_timing/README.md#the-stimulus-and-the-load)): its ADP records name another entity, its MAAP echoes are skipped before the first ANNOUNCE, and a MAAP or ADP deadline's burst leaves out ACMP's and AECP's records. The grandmaster changes of S2's other rows are not part of it.
- **Open question for the reviewers (ruling item 3).** The ruling asks for the other windows' traffic and timers as S2b's model loads them. For a MAAP or ADP timer that traffic includes ACMP's and AECP's records, but a deadline's burst here leaves them out, because the same burst then lands on the draws' own channels: the first campaign's two drops. Under the whole burst, that campaign measured the timers inside their clauses (figures above). An alternative keeps the whole burst at every deadline and holds a draw's frame while that burst's records of its channel are still in the ring; it needs a bench change and another campaign. A decision is requested if the timers' loaded figures must carry those records.
- **Observation, not changed here.** ACMP's receive ring holds 12 records of a 70-byte frame (256 words; the bucket's burst is 16), so a 13th ACMP frame arriving while a 12-frame burst is still queued is dropped, as the first campaign measured. Ring geometry is S15's (#859, #865).

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied
- [x] New or changed behavior has self-checking tests
- [x] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [x] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

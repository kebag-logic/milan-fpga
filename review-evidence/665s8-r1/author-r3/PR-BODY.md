[A758c]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What round 3 changed, finding by finding, and the measurements.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result, the reviewers' probes and the gate table.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN locally at `e3f96a67b5`; hosted runs pending. `665-s8-wire-timing` -> `dev-soft-core`.

- Round 3 answers every finding of R815-1 and R816-1 under the ruling on them (issuecomment-6788719673). Acceptance items 1 to 5 are met, with the measurements below; every reviewer probe named in the findings is found or refused by its own words at the fixed head.
- Item 5: the `wire-timing` job's first hosted run stopped at its build for packages the bench venv had and a fresh runner lacks. The job now installs them, and a replica of the job as a fresh runner does it passes. Its hosted wall time comes from the first hosted run of this head.
- Clean-clone pass at the head: every `run:` step of the four workflows a pull request runs either passes or is not run with a stated reason, 0 failed. The full sweep ran as four shard units: 65 of 65 suites, 2,192,899 checks, 0 failed. No member needed a re-run.

## Linked Issue / roles

Closes #868
Relates to #665

Executor: `[A758c]` (round 3; round 2 was `[A758b]`, round 1 `[A758]`)
Internal cleared-context reviewer: `[R<n>]`
External reviewer: `[R<n>]`

## Description

This PR adds the split placement's wire timing in simulation (#665 S8): the ACMP round trips, MAAP's intervals and egress, ADP's advertise period and the AECP response time, graded offline at the MAC boundary, at both points of the ruling on its points and load ([issuecomment-6755260058](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6755260058)), without and with the composed load.
Round 3 answers R815-1 and R816-1 under the ruling on those reviews ([issuecomment-6788719673](https://github.com/kebag-logic/milan-fpga/issues/868#issuecomment-6788719673)): harness, grader, CI and docs only. The firmware, the RTL and the mailbox contract are unchanged.

| Finding (ruling item) | Change |
|---|---|
| R815 F3, R816 F1 (1): a bind's PROBE_TX | `wire_grade.py`: a bind's PROBE_TX is the first one out after the bind's own BIND_RX_RESPONSE and before the next draw's bind (every draw binds the same stream, so its identity cannot tell them apart); a bind without one is a finding; so is a count of graded PROBE_TX transactions other than the draws, and a BIND_RX_RESPONSE whose status is not SUCCESS. At `announces > 1` a missing `adp.advertise_period` sample is a finding, and so is a log that runs on 9,400 ms past its last ENTITY_AVAILABLE |
| R816 F2 (2): GET_AVB_INFO | `wire_scenario.py`: the draw sends GET_AVB_INFO, 0x0027, on AVB_INTERFACE 0, its IEEE 1722.1-2021 7.4.40.1 command (descriptor_type 9, descriptor_index 0). Each AEM command states the status its final response must carry, SUCCESS for every one, and any other AEM or MVU final status is a finding |
| R815 F1 (3): the MAAP echo | `wire_main.cpp`: each echo keeps its own newest match as each frame is sent, so interface 0's last ANNOUNCE is found whenever one has been sent, whatever traffic followed; the grader finds an echo skipped after its interface's first ANNOUNCE left |
| R815 F2 (4): the delivered load | each load frame is tagged with its offer; `results.json` and the tables keep queued (offers, those an arm queued, frames, echoes skipped), delivered (offers whole and in part, frames that reached the MAC or the bench inside the run) and expiries met apart; delivered load frames + 4 a draw must equal `SUMMARY`'s `rx_frames` + `bench_rx`, checked on every run |
| R815 F4, R816 F3 (5): the reuse guard | `wire_build.py`: the record holds the split recipe's own source list (milan_dp's new `print-split-srcs`), every file a Verilator run or the native compile read (from their dependency lists), the export's checkout modules, the build's tools (`milan_dp/Makefile` among them), the shape's config and the firmware's source trees (the CPU budget harness's `FIRMWARE_TREES`: tsn-c-stack and lwSRP among them) |
| R815 R1, R816 RES-1; R816 SUG-1 (6) | `THE LOAD (#868):`; the advertise period's clause text carries the widened 4,998 to 9,400 ms bound, and its row publishes the margin to the strict 9,000 ms |
| R815 S1 | a refused stimulus or an unreadable log is exit 2 on every `run.py` path |
| item 5, found this round | the `wire-timing` job's first hosted run (at `bfb2df3707`) stopped at the build, `No module named 'pythondata_software_picolibc'`: `sw/litex/litex_pins.txt` carries no runtime sources, and no local pass could see it because the bench venv has them. A replica of the job as a fresh runner does it then stopped at the CPU half's export for tapcfg's data. The job now installs the three packages at the bench venv's revisions; the replica passes, byte-identical to the bench venv's runs |

The self-test has 49 controls, 16 of them new (the [harness page](../tb/verilator/ctrl_wire_timing/README.md#controls-and-self-test) lists each with its planted mutant and its words).

### Measurements, 16 draws a run, seed 0

At `267fc9815d`, whose model, build, stimulus and grader the head keeps. Every run is 16 ACMP and AECP draws, each to its first ANNOUNCE and 250 ms on. Each cell is N: min / mean / max, in ms unless marked us:

| Path (N: min / mean / max ms) | bound ms | 1x1 none | 1x1 composed | 8x8/2if none | 8x8/2if composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 16: 0.396 / 0.673 / 0.966 | 16: 0.728 / 1.339 / 3.423 | 16: 0.401 / 0.920 / 1.727 | 16: 0.758 / 11.940 / 18.277 |
| `acmp.bind_to_probe_tx` | - | 16: 0.585 / 0.862 / 1.155 | 16: 0.917 / 1.528 / 3.613 | 16: 0.607 / 1.127 / 1.933 | 16: 0.965 / 12.147 / 18.483 |
| `acmp.probe_tx` | 200.0 | 16: 0.399 / 0.909 / 1.080 | 16: 0.399 / 2.946 / 5.263 | 16: 0.841 / 1.175 / 2.177 | 16: 0.841 / 1.921 / 5.763 |
| `acmp.probe_tx.entity` | - | 16: 0.177 / 0.458 / 0.839 | 16: 0.219 / 2.495 / 4.539 | 16: 0.180 / 0.725 / 1.456 | 16: 0.180 / 1.470 / 5.043 |
| `aecp.response` | 240.0 | 16: 0.964 / 1.708 / 2.264 | 16: 3.003 / 3.710 / 4.151 | 16: 1.550 / 2.234 / 3.178 | 16: 4.053 / 9.820 / 24.504 |
| `aecp.response.get_avb_info` | - | 3: 1.528 / 1.593 / 1.639 | 3: 3.296 / 3.550 / 3.746 | 3: 1.611 / 2.139 / 2.877 | 3: 8.543 / 15.044 / 24.504 |
| `maap.egress` | 11.0 | 4: 0.410 / 0.787 / 1.008 | 4: 1.147 / 1.546 / 1.972 | 4: 0.961 / 1.250 / 1.479 | 4: 1.771 / 2.036 / 2.472 |
| `maap.probe_interval` | 600.0 | 3: 513.505 / 530.413 / 559.139 | 3: 514.340 / 531.270 / 560.297 | 3: 515.482 / 539.817 / 582.696 | 3: 516.571 / 540.663 / 583.689 |
| `maap.interval_error` | 11.0 | 3: 0.139 / 0.349 / 0.505 | 3: 0.174 / 0.937 / 1.340 | 3: 0.274 / 0.484 / 0.696 | 3: 0.728 / 1.329 / 1.689 |
| `adp.egress` | 400.0 | 1: 0.838 / 0.838 / 0.838 | 1: 1.550 / 1.550 / 1.550 | 1: 0.911 / 0.911 / 0.911 | 1: 2.207 / 2.207 / 2.207 |
| `egress.acmp.first` | - | 48: 0.36 / 0.37 / 0.37 us | 240: 0.36 / 0.36 / 0.37 us | 48: 0.36 / 0.36 / 0.37 us | 240: 0.36 / 0.37 / 0.37 us |
| `egress.maap.first` | - | 5: 0.36 / 0.37 / 0.37 us | 12: 0.36 / 0.37 / 0.37 us | 5: 0.36 / 0.37 / 0.37 us | 9: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | load queued: offers (by an arm) / frames / echoes skipped | delivered: offers whole (in part) / frames | expiries met |
|---|---:|---|---:|---:|---|---|---|
| 1x1 none | 0 | none | 1935 | 49.102 | none | none | - |
| 1x1 composed | 0 | none | 1935 | 49.102 | acmp 16 (0) / 896 / 112, adp 2 (2) / 64 / 14, aecp 16 (0) / 839 / 105, maap 5 (5) / 200 / 0 | acmp 16 (0) / 896, adp 1 (0) / 32, aecp 16 (0) / 839, maap 3 (0) / 120 | adp 1, maap 3 |
| 8x8/2if none | 0 | none | 2001 | 115.271 | none | none | - |
| 8x8/2if composed | 0 | none | 2001 | 115.271 | acmp 16 (0) / 896 / 112, adp 2 (2) / 64 / 14, aecp 16 (0) / 839 / 105, maap 5 (5) / 200 / 0 | acmp 16 (0) / 896, adp 1 (0) / 32, aecp 16 (0) / 839, maap 3 (0) / 120 | adp 1, maap 3 |

- ACMP (item 1): the slowest transaction is the loaded 8x8 bind at 18.3 ms, 181.7 ms inside Table 5.26's 200 ms; every bind has its own PROBE_TX and every BIND_RX_RESPONSE carries SUCCESS.
- AECP (item 3): the slowest response is the loaded 8x8's GET_AVB_INFO at 24.5 ms, 215.5 ms inside 240 ms. Round 2's 20.6 ms was a GET_AS_PATH refusal on AVB_INTERFACE 9 (R816 F2); every AEM and MVU response now carries SUCCESS.
- MAAP (item 2): each frame's egress is at most 2.5 ms and each interval within 1.7 ms of its draw, inside the 11 ms reserve.
- The load (ruling item 3): a loaded run's arms queue 5 MAAP and 2 ADP bursts, of which 3 and 1 are delivered and meet their expiry; the other three deadlines fall past the log's end. Delivered load frames and four a draw are the frames the model received in every run (1,887 + 64 = 1,951).
- The CI step at the head on four CPUs of a shared host: `PASS`, 693 s (build 85 s, then both runs at once, 608 s each).

### The campaign (ruling item 2, re-measured under ruling item 3)

Four units at 1x1 on one build at `267fc9815d`, side by side, each to its second ANNOUNCE and 250 ms on, no time compression, 342 draws each; seeds 1 to 4, loads none, none, composed, composed. Every unit's stimulus changed since round 2 (GET_AVB_INFO), so all four ran again, not only the loaded two. Wall time 8,834 to 9,975 s a unit (2.45 to 2.77 h), each a single-threaded process on a shared host.

| Path (N: min / mean / max ms) | bound ms | unit 0, seed 1, none | unit 1, seed 2, none | unit 2, seed 3, composed | unit 3, seed 4, composed |
|---|---:|---|---|---|---|
| `acmp.bind_rx` | 200.0 | 342: 0.358 / 0.734 / 2.694 | 342: 0.355 / 0.733 / 2.650 | 342: 0.389 / 1.288 / 5.024 | 342: 0.384 / 1.296 / 6.728 |
| `acmp.bind_to_probe_tx` | - | 342: 0.548 / 0.923 / 2.883 | 342: 0.545 / 0.923 / 2.839 | 342: 0.579 / 1.477 / 5.213 | 342: 0.573 / 1.485 / 6.918 |
| `acmp.probe_tx` | 200.0 | 342: 0.399 / 1.045 / 4.487 | 342: 0.399 / 1.167 / 4.490 | 342: 0.399 / 2.959 / 5.593 | 342: 0.399 / 3.039 / 5.591 |
| `acmp.probe_tx.entity` | - | 342: 0.166 / 0.570 / 3.528 | 342: 0.171 / 0.643 / 3.534 | 342: 0.163 / 2.462 / 5.298 | 342: 0.164 / 2.546 / 5.245 |
| `aecp.response` | 240.0 | 342: 0.834 / 1.756 / 3.902 | 342: 0.834 / 1.709 / 3.550 | 342: 2.202 / 3.997 / 7.251 | 342: 2.328 / 4.037 / 6.882 |
| `aecp.response.get_avb_info` | - | 57: 1.353 / 1.731 / 3.716 | 57: 1.362 / 1.672 / 3.550 | 57: 2.825 / 3.964 / 6.214 | 57: 2.831 / 4.032 / 6.637 |
| `maap.egress` | 11.0 | 5: 0.323 / 0.556 / 0.856 | 5: 0.302 / 0.641 / 0.800 | 5: 0.981 / 1.639 / 2.457 | 5: 0.957 / 1.346 / 2.083 |
| `maap.probe_interval` | 600.0 | 3: 513.174 / 530.274 / 558.840 | 3: 513.086 / 530.344 / 559.099 | 3: 513.730 / 531.435 / 559.756 | 3: 513.386 / 531.094 / 560.408 |
| `maap.interval_error` | 11.0 | 4: 0.160 / 0.199 / 0.267 | 4: 0.086 / 0.209 / 0.498 | 4: 0.730 / 1.172 / 1.819 | 4: 0.021 / 0.576 / 1.408 |
| `maap.announce_interval` | 32000.0 | 1: 31957.267 / 31957.267 / 31957.267 | 1: 31956.502 / 31956.502 / 31956.502 | 1: 31958.383 / 31958.383 / 31958.383 | 1: 31957.021 / 31957.021 / 31957.021 |
| `adp.egress` | 400.0 | 6: 0.415 / 0.608 / 0.834 | 6: 0.355 / 0.494 / 0.839 | 6: 0.233 / 0.897 / 1.304 | 6: 0.281 / 1.229 / 2.637 |
| `adp.advertise_period` | 9400.0 | 5: 5362.581 / 6820.423 / 8387.053 | 5: 5363.114 / 6820.105 / 8385.816 | 5: 5362.966 / 6820.604 / 8385.438 | 5: 5364.705 / 6821.437 / 8387.356 |
| `egress.acmp.first` | - | 1026: 0.36 / 0.36 / 0.37 us | 1026: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us | 5130: 0.36 / 0.36 / 0.37 us |
| `egress.maap.first` | - | 6: 0.36 / 0.36 / 0.37 us | 6: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us | 1656: 0.36 / 0.36 / 0.37 us |

| Run | findings | censored | simulated ms | ready ms | queued: offers (by an arm) / frames / echoes skipped | delivered: offers whole (in part) / frames | expiries met |
|---|---:|---|---:|---:|---|---|---|
| unit 0, seed 1, none | 0 | none | 34703 | 49.102 | none | none | - |
| unit 1, seed 2, none | 0 | none | 34706 | 49.102 | none | none | - |
| unit 2, seed 3, composed | 0 | none | 34705 | 49.102 | acmp 342 (0) / 21434 / 112, adp 12 (12) / 454 / 14, aecp 342 (0) / 20073 / 105, maap 6 (6) / 240 / 0 | acmp 342 (0) / 21434, adp 11 (0) / 415, aecp 342 (0) / 20073, maap 5 (0) / 200 | adp 11, maap 4 |
| unit 3, seed 4, composed | 0 | none | 34690 | 49.102 | the same as unit 2 | the same as unit 2 | adp 11, maap 4 |

- B.3.4.1: each announce interval is 31,956.5 to 31,958.4 ms, strictly inside 30 to 32 s and 41.6 ms or more below the ceiling; every interval is within 1.82 ms of its draw and MAAP's egress at most 2.46 ms on all 20 timer-driven frames.
- Table 5.50: each advertise period is 5,362.6 to 8,387.4 ms, 1,012.6 ms inside the graded 9,400 ms and 612.6 ms inside the strict 9,000 ms; each ENTITY_AVAILABLE leaves within 2.7 ms of its delay.
- Over the 1,368 draws the slowest transaction is an AEM response at 7.3 ms and the slowest ACMP one 6.7 ms. Every ACMP frame the entity sends and every AEM and MVU response carries SUCCESS; GET_AVB_INFO takes 1.35 to 6.64 ms.
- The echo (R815 F1): in each loaded unit, the 664 offers queued after the first ANNOUNCE found all 4,641 of their echoes and skipped none (round 2's units delivered 49 of 4,788 MAAP records); the 231 skipped were all queued before it. The entity answered with 1,650 DEFENDs on the MAAP channel.
- The load (R815 F2): of a loaded unit's 6 MAAP and 12 ADP deadline bursts, 5 and 11 are delivered and 4 and 11 meet an expiry: the probe deadline the final probe expiry's pass arms and cancels is delivered and meets none, and the next announce deadline and the last advertise timer fall past the log. Delivered load frames and four a draw are the frames the model received: 42,122 + 1,368 = 43,490.

| Unit | Seed | Load | Start (UTC) | End (UTC) | rc | `results.json` sha256 | `wire.log` sha256, bytes |
|---|---:|---|---|---|---:|---|---|
| 0 | 1 | none | 2026-11-11T08:55:57Z | 2026-11-11T11:23:11Z | 0 | `7c81713941dbf4fc` | `76a7704ae987301a`, 1308488 |
| 1 | 2 | none | 2026-11-11T08:55:57Z | 2026-11-11T11:30:10Z | 0 | `914ab8afb3e307e5` | `b625a4e17544ecf2`, 1308548 |
| 2 | 3 | composed | 2026-11-11T08:55:57Z | 2026-11-11T11:42:12Z | 0 | `3a1c556f145d0c79` | `16392dda7ea94c1a`, 13973246 |
| 3 | 4 | composed | 2026-11-11T08:55:57Z | 2026-11-11T11:32:43Z | 0 | `c71d91edbe9e3458` | `bde6bddace411ce1`, 13972937 |

## Authoritative references

- #868 acceptance 1 to 5; the ruling on its points and load, issuecomment-6755260058; the ruling on R815-1 and R816-1, issuecomment-6788719673.
- Milan v1.2 5.5.2.3 and Table 5.26 (ACMP, 200 ms); Table 5.50 and 5.6.3.5 (ADP advertise timer and delays).
- IEEE 1722-2016 B.3.4.1 and B.3.4.2 (MAAP announce and probe intervals), B.3.6.1 (the seed), Table B.4.
- IEEE 1722.1-2021 7.4.40 (GET_AVB_INFO), Table 7-170 (AECP status), Table 8-3 (ACMP status); 9.2.1 (as #868 names the AECP response); the bound, 240 ms, is `docs/reference/FR_NFR.md` 3.4.1's (IEEE 1722.1-2021 9.3.2.6, Milan v1.2 5.4.3.4, NFR-LAT-02).
- `sw/firmware/ctrl/maap/README.md:43-50` (the 11 ms reserve and the egress note).
- `tb/verilator/ctrl_service_budget` (S2's split SoC, frames and composed load), read only.

## How to get into the same state

```sh
git fetch origin 665-s8-wire-timing
git checkout --detach e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor third_party/lwSRP third_party/tsn-c-stack
```

The product LiteX tree with the patch series applied, the pinned RV32 SDK, Verilator 5.050 and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`), as `tb/verilator/ctrl_service_budget/README.md` states. A fresh interpreter also needs the three packages the `wire-timing` job installs:

```sh
python3 -m pip install git+https://github.com/litex-hub/pythondata-software-picolibc.git@6a13ccce7c575b32c102dd9dc52178505b81fe39 git+https://github.com/litex-hub/pythondata-software-compiler_rt.git@6eb76609c9627bf26635e57c63fb22cda7115887 git+https://github.com/litex-hub/pythondata-misc-tapcfg.git@a12c3f592c99f9c082fdc68c065b81cbd6e6b238
```

## How to validate

```sh
python3 -B tb/verilator/ctrl_wire_timing/run.py --self-test
python3 -B tb/verilator/ctrl_wire_timing/run.py --ci --build-dir /tmp/wire-ci
python3 -B tb/verilator/ctrl_wire_timing/run.py --point 8x8 --build-dir /tmp/wire-8x8 --draws 16 --load none --out /tmp/wire-8x8-none
python3 -B tb/verilator/ctrl_wire_timing/run.py --build-dir /tmp/wire-8x8 --reuse-build --draws 16 --load composed --out /tmp/wire-8x8-composed
python3 -B tb/verilator/ctrl_wire_timing/run.py --campaign --build-dir /tmp/wire-ci --seed 1 --load none --out /tmp/camp0
```

Expected result / pass criteria: the self-test prints `49 controls, 0 failed`; every run prints `0 finding(s)` and both plants `caught`; `--ci` ends `PASS`.
The last line is campaign unit 0; units 1 to 3 take seeds 2, 3 and 4 with loads none, composed and composed.
A build is reused only at the tree it was built from: `--reuse-build` refuses it once any recorded input changed.

### The reviewers' probes at the fixed head

The reviewers' own scripts, unchanged, on the head's fresh logs (the CI step's 1x1 runs and the 8x8 runs), and on a disposable clone for the edit probes:

| Probe | Result |
|---|---|
| R816 `grader_probes.py` R0 | 1x1 and 8x8 unloaded: 0 findings, results identical to the head's |
| R816 R1: draw 5's PROBE_TX never sent | `ACMP: the BIND_RX acmp-bind-5 caused no PROBE_TX after its response and before the next bind`; `ACMP: 15 PROBE_TX transactions graded (15 sent), the run asked for 16 draws` |
| R816 R2: only the last of 16 sent | 16 findings: each of binds 0 to 14 `caused no PROBE_TX ...`, and the count |
| R816 R4: the first BIND_RX_RESPONSE at status 1 | `carries status 1, not SUCCESS (IEEE 1722.1-2021 Table 8-3)` |
| R816 R5: the first AECP response at status 1 | `carries status 1, not the 0 its scenario states` |
| R815 `probe_missing_probe_tx.py`, 1x1 k=0 and k=3, 8x8 k=3 | `VERDICT: caught` each, by the same two findings |
| R815 `probe_no_advertise.py` | `adp.advertise_period: no sample in a run to its second ANNOUNCE`, and `the entity stopped advertising`; the control passes |
| R815 `probe_reuse_stale.py` | 6 of 6 edits refused: the split top, `KL_mbx.sv`, `KL_ctrl_split.sv` and `KL_mbx_wb.sv` by name, `maap_mbx.c` by the firmware trees' digest, `milan_dp/Makefile` because its source list no longer reads (a valid comment line is refused by name too) |
| R816 `reuse_probe.py` | the record as made accepted; `wire_main.cpp`, the split top, `KL_mbx.sv` and `milan_datapath.sv` refused by name, tsn-c-stack's `maap.c` and `maap_mbx.c` by the firmware trees' digest |
| R816 `status_census.py`, `aecp_status.py` | every ACMP and AECP response status 0 in the four head runs; GET_AVB_INFO is `0x0027` on `(9, 0)`, 3 of 3 SUCCESS |

### Gate table

The pass ran once at `e3f96a67b5dd1b9e4536ca67a6bd1595f4c19d53`. Each workflow job ran on its own fresh clean clone, with one build per point at that head. The step list was read from the workflow at the head, so a step missing from the record fails the check. Steps that only make sense on a hosted runner were not run, each with its reason recorded: the apt package resolution, the tool installs whose pinned builds are present locally, and the hosted step records.

| Gate | Result |
|---|---|
| `rtl-fast`, all 18 jobs | 56 steps rc 0, 65 not run with a reason, 0 failed |
| `rtl-fast / wire-timing` (item 5): `python3 tb/verilator/ctrl_wire_timing/run.py --ci` | rc 0. `49 controls, 0 failed`; both runs `0 finding(s)`; both plants caught on each run. Results and logs byte-identical to the measurements above. Wall time 2,505 s (build 626 s) on four CPUs that other work kept busy |
| firmware self-test, `test_ctrl_firmware.py --require-rv32 --self-test`, four shards | rc 0 each; the control shard reports `mutants: 570 of 570 caught` |
| `fw_coverage.py --selftest`, `--check` | rc 0, `firmware coverage: PASS (35 files)` |
| `cd tests && behave` | rc 0, 508 scenarios and 2,330 steps passed, 0 failed |
| `docs`, all 9 jobs | 64 steps rc 0, 31 not run with a reason, 0 failed |
| `elaborate`, all 6 jobs | 13 steps rc 0, 33 not run with a reason, 0 failed; the LiteX aggregate 8 of 8 |
| `rtl / full-ci-gate` | rc 0 |
| `rtl / yosys-shards`, 0 to 3 | rc 0 each, `RESULT: PASS` |
| `rtl / verilator-shards`: the full sweep as four shard units | Shard 0: 15/15, 360,992 checks. Shard 1: 17/17, 1,526,104 checks. Shard 2: 17/17, 284,228 checks, `capture_coherence` included. Shard 3: 16/16, 21,575 checks. The cancellation preflight passed in all four |
| `rtl / physical-gptp` | Not run: the job's condition is schedule or dispatch only, so a pull request does not trigger it |
| `git diff --check` against the merge base `1d6bf5556a` | rc 0 |
| `tally_selftest.py --mutants`; `test_ctrl_nvm.py --require-rv32 --self-test` | rc 0: `18 of 18`; 5 shapes, 435 tests, 109 of 109 planted defects caught |
| `test_builder.py --require-rv32` | rc 0, `ALL GATES PASS EXCEPT 2 NOT RUN`. Not run: gate 1b's `MAKEFLAGS += -e` mutant, which has no effect on this make, and gate 11, which needs a placed implementation report |
| S2's harness: `ctrl_service_budget/run.py --self-test`, `--point 1x1`, `--point 8x8` (both with `--record-budget-findings`) | rc 0 each. 1x1: 18 groups graded, 0 refusals. 8x8: 17 groups graded, 0 refusals. The T_svc misses they record are S2b's findings, as in round 2 |
| wire timing at 8x8/2if, without load and with the composed load | rc 0 each, `0 finding(s)`, both plants caught. Byte-identical to the measurements above |

Beside the pass: the `wire-timing` job replicated as a fresh runner does it (a fresh clone, a fresh venv built by the job's own install steps, the RV32 SDK installed fresh, the CPU netlist generated cold) at `fbe5acc983`: every setup step rc 0, the step `PASS` in 1,299 s with its build 323 s, byte-identical to the bench venv's runs.

## Known limitations / out of scope

- Out of scope, as #868 states: 32x32 (#859), the service budget itself (S2b) and bench confirmation (S12). `ctrl_service_hooks` is #869.
- The CPU budget harness's GET_AVB_INFO row (`tb/verilator/ctrl_service_budget/scenario.py:464`) sends 0x0028 the same way; it is outside this lane (ruling item 2) and needs its own Issue.
- Interface 1 at 8x8 is driven from the bench and has no datapath; its figures are not graded. Every figure is interface 0's.
- The announce interval and the advertise period are graded at 1x1 in the local campaign, not in CI and not at 8x8.
- MAAP draws its intervals from an xorshift32 seeded with the MAC plus NOW_MS at `maap_begin` (B.3.6.1), which the boot fixes in a cycle-true model, so every run at a point draws the same intervals; the seeds move the stimulus and its load against each expiry.
- The MAC core's and the PHY's own pipeline delays are outside the simulation (a fixed sub-microsecond each way); the CSR window's AXI4-Lite access is the testbench's; the flash is blank; the firmware polls the mailbox.
- The load differs from S2's composed load in three stated ways ([the harness page](../tb/verilator/ctrl_wire_timing/README.md#the-stimulus-and-the-load)): its ADP records name another entity, its MAAP echoes are skipped only before their interface's first ANNOUNCE, and a MAAP or ADP deadline's burst leaves out ACMP's and AECP's records, as the ruling keeps it (its item 7).
- The `wire-timing` job's hosted wall time is open until the first hosted run of this head; the replica on four CPUs of a shared host took 1,299 s for the step, its build 323 s with the CPU netlist generated cold.

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

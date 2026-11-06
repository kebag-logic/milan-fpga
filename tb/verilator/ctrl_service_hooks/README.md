<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# The F2-F5 timing hooks on the target core (#665 S5)

This harness measures the eight NFR-SCOUT-03 hooks of [FR_NFR.md 3.4.2](../../../docs/reference/FR_NFR.md#342-control-service-test-hooks) on the split placement's core.
The hooks are H-ADP, H-DISC, H-ACMP (its commit part), H-AECP, H-NOTIFY, H-COUNTERS, H-MAAP and H-SRP.
The image is the split platform's ([`ctrl_plat_image.py`](../../../sw/firmware/ctrl/test/ctrl_plat_image.py), lane S3), linked unmodified.
It runs on the [CPU budget harness](../ctrl_service_budget/README.md)'s split SoC (lane S2), with the platform's CSR window added.
Each path is measured in target cycles, from its RX_HEAD commit or triggering event to its last TX commit.
Each is graded against its hook's bound, at the shipping shape and the largest, alone and under the composed load.
Each hook's ordering obligation is checked on the same logs, apart from the budget.
Each hook has a planted late service and a planted ordering defect, and each must be caught by its own words.

Its contract is the [S5 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6513150371) on #665, which amends the plan's S5:

- **The bound.** T_svc = 20 ms (owner, 2026-10-29). Each path is graded against min(T_svc, its family's ceiling), per [the ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075): 18 ms for SRP, 20 ms for every other hook. A path with a normative wait W is bounded by W plus that.
- **The clock.** The split CPU's product clock is 100 MHz, the SoC's `sys` clock, which is also its bus clock ([the owner's decision of 2026-10-30](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6514866239)). That decision supersedes the 50 MHz Milan clock that [the correction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508196970) named as the product's. Every hook is graded at 100 MHz. This base's `MilanSoC` still drives the CPU from the Milan clock; lane S2b (#810) moves it to `sys`. The 50 MHz figures are history: the clock stays selectable, labelled so, and is never graded as the product's.
- **The firmware.** `dev-soft-core` as it is: S2b's firmware cuts are not merged.

## Contents

- **[Run and reproduce](#run-and-reproduce)** -- The prerequisites, the points, the clocks, the face arms, the plants and the self-test.
- **[The SoC and the testbench](#the-soc-and-the-testbench)** -- What is the CPU budget harness's, what this harness adds, and the two face arms.
- **[The hooks](#the-hooks)** -- Each hook's paths, bound, normative timeout, ordering obligation and plants.
- **[Grading](#grading)** -- The bound, the layout swing, the margin, alone and under load, the ordering checks, and a superseded probe.
- **[Results](#results)** -- Each hook at both points and both arms at the product clock, and the plants.
- **[Findings](#findings)** -- What the measurement shows, by hook.
- **[History](#history)** -- The 50 MHz figures recorded before the 100 MHz decision.
- **[Limits](#limits)** -- What is not measured, and why.

## Run and reproduce

Use the [CPU budget harness's prerequisites](../ctrl_service_budget/README.md#run-and-reproduce): the product LiteX tree, the pinned RV32 SDK, Verilator and the offline CPU generator (`COURSIER_MODE=offline`, `SBT_OPTS=-Dsbt.offline=true`).
The tsn-c-stack and lwSRP submodules must be initialised.
Keep build directories outside the checkout.
The portable self-test needs Python and PyYAML only:

```sh
python3 -B tb/verilator/ctrl_service_hooks/run.py --self-test
```

Each point builds the runtime, the image, the SoC and the native model, then runs every group of its face arm.
At the product clock, on the formal arm:

```sh
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 1x1 \
  --build-dir /tmp/hooks-1x1 --record-findings
python3 -B tb/verilator/ctrl_service_hooks/run.py --point 8x8 \
  --build-dir /tmp/hooks-8x8 --record-findings
```

`1x1` is `endstation_ax7101_1x1_tdm8` with one interface, the shipping shape.
`8x8` is `endstation_ax7101_8x8` with two, the largest.
At `8x8`, and only there, the image and the SoC's memory plan name the ledgered point `platform-8x8-two-interfaces`, which plans 59.0 RAMB36 by [the ruling of 2026-10-29](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6505997821) on #665, owed to lane S14.

`--cpu-clock` names the CPU clock: `sys`, the product's 100 MHz, by default, or `milan`, the 50 MHz history clock. The bus stays at 100 MHz.
`--arm answering` runs the labelled answering-face arm ([The SoC and the testbench](#the-soc-and-the-testbench)), the only arm with H-COUNTERS.
So the four runs of [Results](#results) are these two commands, each as written and with `--arm answering`.

Without `--record-findings` a path over its bound fails the run.
A path within its bound by less than the layout swing fails it too ([Grading](#grading)).
With it, those paths are recorded and the run still fails on any refusal and on any ordering finding.
`--groups` selects groups and `--jobs` sets how many run at once (8 by default).
`--reuse-build` reuses a build only if every input recorded in its `build.json` still has its digest: the image, its runtime, the ROM files, the testbench as built, the CPU budget harness's testbench and observers, the SoC Verilog, this harness's SoC and build modules, and the firmware and configuration trees.
`--regrade` grades the logs already in the results directory, on a reused build, and refuses a group whose log is absent or whose script the groups no longer make.

A plant builds a scratch copy of the firmware's tree with one planted defect, at 1x1 and the product clock (100 MHz), and runs the plant's group:

```sh
python3 -B tb/verilator/ctrl_service_hooks/run.py --plant adp-late --build-dir /tmp/hooks-plant-adp-late
```

The plants are `adp`, `disc`, `acmp`, `aecp`, `notify`, `counters`, `maap` and `srp`, each `-late` and `-order`.
The run prints `PLANT <name> caught: <its finding>` and exits 0 when its hook's finding starts with the plant's words, and `ESCAPED` and 1 otherwise.

The directory has no Makefile, for the CPU budget harness's reason: the serial sweep discovers every Makefile, and registering a suite is a CI change.
The TSN stack boundary gate finds `hooks_build.py` by text, because it names the firmware's tree; it is listed in [`ctrl_configs.py`](../../../sw/firmware/ctrl/test/ctrl_configs.py) `OUTSIDE` with its reason.

## The SoC and the testbench

[`hooks_soc.py`](hooks_soc.py) builds the CPU budget harness's split SoC from its own parts ([`split_soc.py`](../ctrl_service_budget/split_soc.py), imported read only):

- the shipping VexiiRiscv with the split placement's 4 KiB instruction cache, the CPU at 100 MHz (`sys`, the product's) or 50 MHz (`milan`, history), and its bus at 100 MHz. Either way the CPU keeps this base's own clock input and its crossing to the bus. Under `sys` the two clocks are equal, so the crossing costs only its own latency. The product wiring of the 100 MHz decision clocks the CPU from `sys` itself, with no crossing, so these figures include a latency it drops;
- `milan_soc.add_ctrl_memory` built from the linked image;
- `KL_mbx` behind `KL_mbx_wb`, its datapath on the testbench's pads, each face commit acknowledged at the contract's bound;
- LiteSPI and `timer0` where F1's port addresses them; the UART.

It adds the Milan CSR window at `milan_soc.MILAN_CSR_BASE`, answered in gateware from a register file.
ID and VERSION are the datapath's reset values; every other word is the [split boot simulation](../ctrl_split_boot/README.md)'s seeded value until written, then the value written.
`TOD_RD_LO/HI` hold the simulated time of the last `PTP_CMD` snapshot.
The split boot simulation answers the same words from its testbench, so the boot, the CSR policy and MAAP's report run as there.

The image is linked twice, as the split boot simulation links it: against the platform's fixture map, then against this SoC's own `csr.csv`, and the two exports' maps must be equal.

The face block (contract 2.3) has two arms:

- **`idle`**, the formal arm: connected exactly as the CPU budget harness connects it, its window answers and events held idle as `milan_soc.CtrlMailbox` holds them, each commit acknowledged at the bound. A window read times out, as on the fabric-less split SoC.
- **`answering`**, a labelled test arm: a datapath that answers the CTR and GSI windows at the slowest the contract allows, `wait_cycles - 1` cycles after the request opens, the last cycle `KL_mbx`'s window accepts. CTR answers word *w* with (changes on that interface << 8) | *w*, and `counters_valid` with every bit; GSI answers 3 to the format verdict and 0 to every other word. The testbench drives the counter-change event. H-COUNTERS runs only here: its push reads the CTR window, so on the idle arm it is never sent. The AMAP and EDIT windows and the AVB_INFO, AS_PATH and live-map events stay idle in both arms.

The testbench is the CPU budget harness's [`sim_main.cpp`](../ctrl_service_budget/sim_main.cpp), copied into the build directory with the additions of [`hooks_build.py`](hooks_build.py) (`TESTBENCH`, `CSR_STORES`):

- the `ctrchg <if> <type> <index>` step, a one-cycle counter-change pulse with its descriptor, logged `CTRCHG <bus cycle> <if> <type> <index>`;
- every CPU store into the Milan CSR window, logged `CSRW <bus cycle> <offset>`, which the H-MAAP check reads.

Each addition's anchor must occur exactly once, or the build is refused by name.
The CPU budget harness's observers, configuration header and grader are used unchanged.
Its parser refuses a line it does not know, so this harness takes its own lines off first and hands each counter change to it as a pad, `pad:CTR:<if>` ([`hooks.py`](hooks.py), `parsed`).

## The hooks

| Hook | Its paths | Bound | Normative timeout (margin) | Ordering obligation, checked apart from the budget |
|---|---|---:|---|---|
| H-ADP | family `adp`: DISCOVER, the timers, GM, link, the event row, ADP records under load | 20 ms | 2 s random window (Milan v1.2 5.6.3.5.2) | An ENTITY_AVAILABLE carries the grandmaster in force when it is built: the first after a grandmaster change carries the new one (Milan v1.2 5.6.3.5.7; IEEE 1722.1-2021 6.2.2.16) |
| H-DISC | family `disc`: ENTITY_AVAILABLE and ENTITY_DEPARTING from RX_HEAD, TMR_NO_ADP, the bound-talker rows | 20 ms | 200 ms (Milan v1.2 5.5.2.3, Table 5.26) | Discovery records are applied in arrival order: a bound talker's DEPARTING then AVAILABLE leaves its sink discovered, so its PROBE_TX_COMMAND follows (Milan v1.2 5.6.4.5.1, 5.6.4.5.3, Table 5.54) |
| H-ACMP | family `acmp`: every listener and talker command, the timers, the ring and owed rows | 20 ms | 200 ms (Milan v1.2 5.5.2.3, Table 5.26) | The commands of one controller are answered in arrival order |
| H-AECP | family `aecp`: every solicited response, AECP records under load | 20 ms | 240 ms (IEEE 1722.1-2021 9.3.2.6) | Every face value a response promises is committed before the response ([`ARCHITECTURE_HW_SW_SPLIT.md` section 1](../../../docs/ARCHITECTURE_HW_SW_SPLIT.md#1-ownership-rule); Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2) |
| H-NOTIFY | family `notify`: every fan-out at registration capacity, alone and under load | 20 ms | 240 ms, shared with AECP | The successful command's response is committed before any of its notifications (Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2) |
| H-COUNTERS | the counter push (answering arm): a change, every served descriptor (ALL), the held push, under load | 20 ms | counters update within 1 s (Milan v1.2 5.3.7.7, 5.3.8.10) | One descriptor's pushes to one recipient leave at least 1 s apart at the wire (Milan v1.2 5.4.5.2, Table 5.22) |
| H-MAAP | family `maap`: the PROBEs, ANNOUNCE, DEFEND, MAAP records under load | 20 ms | 500 ms probe interval (IEEE 1722-2016 B.3.4.2, Table B.8) | The talker DA gate is published before the allocation is reported (Milan v1.2 4.3.3.1; `maap_mbx.c`, `range`) |
| H-SRP | family `srp`: startup, Listener Ready, malformed, Domain, SRP records under load | 18 ms (+ W) | 180 ms JoinTime (IEEE 802.1Q-2018 10.7.11; Milan v1.2 Table 4.3) | The adopted Domain is published (SR_DOMAIN) before the MRPDUs that carry it (`srp_mbx.c`, `change_domain`; contract 2.2) |

The CPU budget harness's groups carry seven hooks' paths, graded by its own grader, but its fixture and boot-fault groups.
This harness adds, in [`hooks.py`](hooks.py):

- `hooks-counters` and `hooks-load-counters` (answering arm): every registration a recipient; a change of STREAM_INPUT 0's counters, then 100 ms later a change of a descriptor the source keeps no bit for, which posts ALL; then the held push; and the push under the composed load, sixteenth on the event ring;
- `hooks-load-notify`: a SET_NAME fan-out to every registration, last of the AECP ring's burst, while every other channel carries its admitted burst and fifteen grandmaster changes fill the event ring;
- `hooks-disc-aging`: H-DISC's aging, its window opened after the arm ([Grading](#grading));
- `hooks-order-adp` and `hooks-order-acmp`: the instances H-ADP's and H-ACMP's ordering checks apply to;
- `hooks-late-disc`, `-acmp`, `-aecp`, `-notify`, `-maap` and `-srp`: one path each with a wait long enough to see a late service end, for the late plants. The CPU budget harness's own groups wait only as long as their paths take unplanted. H-ADP's late plant runs in that harness's `control` group.

Each composed row of this harness carries the CPU budget harness's defined load of its rows without a LINK event (`grade.defined_load('backlog-owed')`): every channel's admitted burst and fifteen grandmaster changes.
The window must commit exactly that, as there.
It opens a full refill after the registrations, so every token bucket is full. Its fifteen grandmaster changes come at its first instant, ahead of every channel's burst, as in the CPU budget harness's backlog rows (`scenario.gm_run` before `scenario.composed_load`).
That is the burst [the ruling of 2026-11-04](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6634982529), item 1, puts in the SRP row's scope: a grandmaster change at the load's first instant with every bucket full. So H-SRP's figure under the composed load is that row's.

### The plants

Each plant is a scratch copy of the firmware's tree with its edits, every anchor found exactly once ([`hooks_build.py`](hooks_build.py), `planted`), never an edit of the checkout.
A late plant spins 120,000 turns in the hook's service path, each a load and a store of a counter in sram, well past every bound at 100 MHz ([Results](#results) gives each plant's figure). An ordering plant reorders the hook's outputs or the state they carry.

| Plant | Its defect | Group | Its words |
|---|---|---|---|
| `adp-late` | `adp_mbx.c`: the receive handler spins before `adp_rx` | `control` | `LATE H-ADP` |
| `adp-order` | `adp_mbx.c` `port_gptp`: each read returns the grandmaster of the read before | `hooks-order-adp` | `ORDER H-ADP` |
| `disc-late` | `acmp_mbx.c` `on_adp_frame`: spins before `acmp_adp_rx` | `hooks-late-disc` | `LATE H-DISC` |
| `disc-order` | `acmp_mbx.c` `on_adp_frame`: an ENTITY_DEPARTING is held and applied after the next AVAILABLE | `acmp-disc` | `ORDER H-DISC` |
| `acmp-late` | `acmp_mbx.c` `on_frame`: spins before `acmp_rx` | `hooks-late-acmp` | `LATE H-ACMP` |
| `acmp-order` | `acmp_mbx.c` `on_frame`: a command is held and taken after the next | `hooks-order-acmp` | `ORDER H-ACMP` |
| `aecp-late` | `aecp_mbx.c` `frame`: spins before `aecp_rx` | `hooks-late-aecp` | `LATE H-AECP` |
| `aecp-order` | `aecp_face.c` `changed` defers the publication to the face's poll, and `aecp.c` no longer waits for it | `aecp` | `ORDER H-AECP` |
| `notify-late` | `aecp.c` `transmit`: spins once before a fan-out's first recipient | `hooks-late-notify` | `LATE H-NOTIFY` |
| `notify-order` | `aecp.c` `transmit`: the notifications are sent before the owed response | `aecp-fanout` | `ORDER H-NOTIFY` |
| `counters-late` | `ctrl_app_aecp.c` `face_event`: spins on COUNTERS_CHANGED | `hooks-counters` | `LATE H-COUNTERS` |
| `counters-order` | `aecp.c` `asynchronous`: the 1 s spacing after a counter push's departure is dropped | `hooks-counters` | `ORDER H-COUNTERS` |
| `maap-late` | `maap_mbx.c` `receive`: spins before `maap_rx` | `hooks-late-maap` | `LATE H-MAAP` |
| `maap-order` | `maap_mbx.c` `range`: the allocation is reported before the DA gate is published | `maap` | `ORDER H-MAAP` |
| `srp-late` | `srp_mbx.c` `receive`: spins before `apply_receive` | `hooks-late-srp` | `LATE H-SRP` |
| `srp-order` | `srp_mbx.c`: the adopted Domain is published after the next MRPDU is sent | `srp` | `ORDER H-SRP` |

## Grading

[`run.py`](run.py) grades each group's log with the CPU budget harness's grader ([`grade.py`](../ctrl_service_budget/grade.py)): the starts and ends, the clock conversion, the pass bound, the composed load and its service, as that harness defines them.
Then, for each measured path:

- its hook is its family's, but a counter push, whose probe names start `counters.`;
- its bound is min(T_svc, its family's ceiling) plus its normative wait W; it fits at its bound and not one hundredth of a microsecond past it; a record never released or a command never answered never fits;
- its slack is its bound in CPU cycles less its own CPU cycles. A path within its bound by fewer CPU cycles than the layout swing, 6,490, is a finding, `NARROW`, as a path over it is `LATE`. That swing is one pass's measured spread from data layout alone, 195,050 to 201,540 cycles on the same records, and a fit by less than it fits by chance ([the ruling of 2026-11-04](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6634982529), item 2). This harness takes that figure as given and does not measure a swing of its own;
- its margin is its family's normative timeout less W and the path, the allowance left for ingress, egress and the network, which this harness does not measure;
- it is under the composed load when its group is one of the CPU budget harness's backlog rows or one of this harness's composed rows.

Each hook's figure is its worst path alone and its worst under the composed load.

H-COUNTERS' held push is graded from its eligibility, as the hook row says ("previous notification wire time supplies eligibility"): from 1 s after the first push's last departure at the wire, or from the change if later, to its last recipient's commit.
The time it was held after the change is its W, recorded beside it.

Each ordering check reads the order of the hook's outputs and the state they carry, never their latency, and counts the instances it applied to.
A check that applied to nothing is reported as not applied, never as passed.
On the idle arm H-COUNTERS' check has nothing to apply to, by construction.

H-DISC's check can also leave an instance undecided, counted apart from the instances it applied to.
The sink sends its PROBE_TX_COMMAND only after its TMR_DELAY, a draw of 0 to 1000 ms (Milan v1.2 Table 5.29; tsn-c-stack `ACMP_TMR_DELAY_MAX_MS`).
The check's window ends at the interface's next ADP record, which could rediscover the talker.
A PROBE_TX_COMMAND inside the window passes the instance.
A window without one is a finding only when it is longer than 1040 ms: the ENTITY_AVAILABLE's service, the longest delay, then the timer's service, each service at its 20 ms bound.
A shorter window without one is undecided: the draw may simply have run past the next record.
At 8x8 on the answering arm the CPU budget harness's `acmp-disc` gives such a case. Interface 1's sink drew about 672 ms, and the script's next ADP record came 557 ms after the ENTITY_AVAILABLE.
The `disc-order` plant's window is 1243 ms at 100 MHz, because without a probe that group's wait for two runs to its full 1.2 s, so the plant is decided.

**A superseded probe.** On the platform image at 8x8 and the 50 MHz history clock, the CPU budget harness's `acmp.tmr_no_adp.if1` (group `acmp-disc`) finds no TMR_NO_ADP expiry after its mark.
Interface 1's sink re-arms its aging timer, from an ENTITY_AVAILABLE with valid_time 1, after that group's mark, so the expiry 2 s later falls past the group's 1.9 s window.
`hooks-disc-aging` measures the same path with its window opened after the arm.
A refusal of the earlier probe is reported as superseded only where `hooks-disc-aging` measured the same path on the same interface (`hooks.SUPERSEDED`); any other unmeasured path is a refusal and fails the run.
At the product clock `acmp-disc` measures that probe itself at both points, so no run of [Results](#results) supersedes anything; the rule stays for a run at the history clock.

[`hooks_selftest.py`](hooks_selftest.py) (`run.py --self-test`) pins the bounds, the normative timeouts, the layout swing, the clock labels and the product clock as the default.
It runs each ordering check on a clean synthetic log, which it must apply to and pass, and on a defective one, which it must report by its hook's words; H-DISC's also on a log it must leave undecided.
It checks every plant's and testbench addition's anchors against the checkout, the held push's eligibility, the findings by hook, a fit under the layout swing, the superseded rule, the aging window and the composed rows' full buckets.
Then it replaces each rule in turn, and a named check must fail:

| Mutant | Caught by |
|---|---|
| bound: a stale T_svc of 10 ms | bounds pinned |
| bound: SRP graded against T_svc alone | an 18 to 20 ms SRP path misses |
| bound: the ceiling alone | bounds pinned |
| bound: the normative wait is not added | the exact bound fits and W adds |
| bound: the margin is not recorded | the exact bound fits and W adds |
| map: the counter push is a notification | the hooks map |
| map: no composed row of this harness is loaded | the hooks map |
| label: the Milan clock labelled the product's (the earlier rule) | the clock labels |
| label: the Milan clock the default (the earlier rule) | the clock labels |
| split: the counter change is no pad | own lines are split off |
| H-ADP: the grandmaster is not checked | H-ADP ordering |
| H-DISC: the sink's PROBE_TX_COMMAND is never recognised | H-DISC ordering |
| H-DISC: the window never ends (the earlier rule ended it at the next tagged record) | H-DISC ordering |
| H-DISC: a window shorter than the sink's TMR_DELAY decides (the earlier rule) | H-DISC ordering |
| H-ACMP: no response is matched to its command | H-ACMP ordering |
| H-AECP: no face commit is recognised | H-AECP ordering |
| H-NOTIFY: the notification is not found | H-NOTIFY ordering |
| H-COUNTERS: spacing of 0.1 s accepted | H-COUNTERS spacing |
| H-COUNTERS: the held push from its change | the held push |
| H-MAAP: no allocation report is recognised | H-MAAP ordering |
| H-MAAP: every AAF_CTRL store is a report (earlier rule) | H-MAAP ordering |
| H-SRP: the ADOPTED bit is never seen set | H-SRP ordering |
| plants: a plant edits nothing | the plants apply |
| supersede: any later group supersedes a refusal | a refusal is superseded only by its own path |
| aging: the window opens before the arm (the earlier rule) | the aging window opens after the arm |
| aging: the sink still waits for its PROBE_TX_RESPONSE (the earlier rule) | the aging window opens after the arm |
| aging: both sinks bound before either is answered (the earlier rule) | the aging window opens after the arm |
| buckets: the window opens right after the registrations (the earlier rule) | a composed row opens on full buckets |
| findings: a path over its bound is not a finding | findings by hook |
| narrow: the layout swing is not applied | a fit under the layout swing is a finding |
| narrow: the slack counted at the 50 MHz CPU (the earlier clock) | a fit under the layout swing is a finding |

A mutant whose name ends in a bracket saying "earlier" restores a rule, or the clock, this harness had before its check, so that check is the test that fails on it.

## Results

The four runs at the product clock, the CPU at 100 MHz on `sys` and the bus at 100 MHz, were measured at `fa925043`, each in a clean clone with its own build.
That commit's harness, firmware, configurations and build inputs are this head's: only this README changed after it, and a regrade at the head on each reused build checks every input's digest ([Run and reproduce](#run-and-reproduce)).
Each run exits 0 with `--record-findings`: 0 refusals, nothing superseded, no ordering finding and no path within its bound by less than the layout swing.
Every path over its bound is a `LATE` finding, listed in the run's `table.md`.

| Point | Arm | Groups | Paths | Refusals | Ordering findings | `NARROW` | `LATE` |
|---|---|---:|---:|---:|---:|---:|---:|
| 1x1 | idle | 27 | 145 | 0 | 0 | 0 | 28 |
| 1x1 | answering | 29 | 159 | 0 | 0 | 0 | 29 |
| 8x8 | idle | 27 | 207 | 0 | 0 | 0 | 38 |
| 8x8 | answering | 29 | 221 | 0 | 0 | 0 | 42 |

Each hook's worst path alone and under the composed load, in ms against its bound; bold is over it, and "never served" is a command never answered or a record never released by the run's end.

1x1, CPU 100 MHz on `sys`:

| Hook | Bound | Alone, idle | Alone, answering | Under load, idle | Under load, answering |
|---|---:|---:|---:|---:|---:|
| H-ADP | 20 | 0.63 | 0.63 | **29.40** | **21.26** |
| H-DISC | 20 | 8.40 | 0.81 | **24.78** | 14.03 |
| H-ACMP | 20 | 8.16 | 0.87 | **never served** | **never served** |
| H-AECP | 20 | 1.89 | 1.88 | **159.48** | **85.82** |
| H-NOTIFY | 20 | 3.78 | 3.78 | **59.38** | **59.38** |
| H-COUNTERS | 20 | - | **27.58** | - | **20.76** |
| H-MAAP | 20 | 1.01 | 1.01 | **29.43** | **21.25** |
| H-SRP | 18 | 1.81 | 1.81 | **never served** | **68.05** |

8x8, CPU 100 MHz on `sys`:

| Hook | Bound | Alone, idle | Alone, answering | Under load, idle | Under load, answering |
|---|---:|---:|---:|---:|---:|
| H-ADP | 20 | 3.37 | 3.37 | **44.15** | **31.50** |
| H-DISC | 20 | 15.93 | 1.34 | **37.32** | **21.79** |
| H-ACMP | 20 | 15.99 | 1.64 | **never served** | **never served** |
| H-AECP | 20 | 2.40 | 2.40 | **205.20** | **102.26** |
| H-NOTIFY | 20 | 6.85 | 6.85 | **84.07** | **84.07** |
| H-COUNTERS | 20 | - | **218.71** | - | **36.62** |
| H-MAAP | 20 | 1.76 | 1.76 | **44.19** | **31.48** |
| H-SRP | 18 | 4.04 | 4.04 | **never served** | **102.31** |

The paths over their bound of each hook's paths, and its ordering check: the instances it applied to, those it left undecided in brackets, and its findings.

| Hook | 1x1 idle | 1x1 answering | 8x8 idle | 8x8 answering | Ordering, 1x1 idle / answering | Ordering, 8x8 idle / answering |
|---|---:|---:|---:|---:|---|---|
| H-ADP | 1 of 28 | 1 of 30 | 5 of 44 | 5 of 46 | 2 (0), 0 / 2 (0), 0 | 4 (0), 0 / 4 (0), 0 |
| H-DISC | 1 of 8 | 0 of 8 | 2 of 13 | 1 of 13 | 1 (0), 0 / 1 (0), 0 | 2 (0), 0 / 1 (1), 0 |
| H-ACMP | 11 of 30 | 12 of 32 | 11 of 43 | 12 of 45 | 65 (0), 0 / 76 (0), 0 | 68 (0), 0 / 79 (0), 0 |
| H-AECP | 5 of 36 | 6 of 38 | 5 of 50 | 6 of 52 | 7 (0), 0 / 7 (0), 0 | 14 (0), 0 / 14 (0), 0 |
| H-NOTIFY | 1 of 11 | 1 of 11 | 1 of 15 | 1 of 15 | 11 (0), 0 / 11 (0), 0 | 15 (0), 0 / 15 (0), 0 |
| H-COUNTERS | - | 2 of 4 | - | 2 of 4 | not applied / 16 (0), 0 | not applied / 32 (0), 0 |
| H-MAAP | 2 of 17 | 1 of 19 | 5 of 23 | 6 of 25 | 44 (0), 0 / 48 (0), 0 | 44 (0), 0 / 48 (0), 0 |
| H-SRP | 7 of 15 | 6 of 17 | 9 of 19 | 9 of 21 | 1 (0), 0 / 1 (0), 0 | 2 (0), 0 / 2 (0), 0 |

Where each worst path is, with its margin to its family's normative timeout in ms; a path never served has none:

| Hook | Point | Alone (idle / answering) | Margin | Under load (idle / answering) | Margin |
|---|---|---|---|---|---|
| H-ADP | 1x1 | `adp.tmr_advertise.if0` / the same | 1999 / 1999 of 2000 | `backlog-adp.service.adp.last.if0` / `hooks-load-counters.service.adp.last.if0` | 1971 / 1979 of 2000 |
| H-ADP | 8x8 | `adp.link_down.if1` / the same | 1997 / 1997 of 2000 | `backlog-adp.service.adp.last.if0` / `backlog.service.adp.last.if1` | 1956 / 1969 of 2000 |
| H-DISC | 1x1 | `acmp.entity_departing.if0` / `acmp.tmr_no_adp.if0` | 192 / 199 of 200 | `backlog.adp_available.if0` / the same | 175 / 186 of 200 |
| H-DISC | 8x8 | `acmp.entity_available.if1` / `acmp.tmr_no_adp.if1` | 184 / 199 of 200 | `backlog.adp_available.if0` / the same | 163 / 178 of 200 |
| H-ACMP | 1x1 | `acmp.probe_tx.if0` / `acmp.tmr_delay.if0` | 192 / 199 of 200 | `backlog.owed_behind0.if0` / the same | none |
| H-ACMP | 8x8 | `acmp.unbind_rx.if1` / `acmp.tmr_no_resp1.if1` | 184 / 198 of 200 | `backlog.owed_behind0.if0` / the same | none |
| H-AECP | 1x1 | `aecp.set_name.if0` / `aecp.get_counters.if0` | 238 / 238 of 240 | `backlog-adp-refill.service.aecp.last.if0` / `backlog-owed.service.aecp.last.if0` | 81 / 154 of 240 |
| H-AECP | 8x8 | `aecp.set_name.if0` / the same | 238 / 238 of 240 | `backlog-adp-refill.service.aecp.last.if1` / `backlog-owed.service.aecp.last.if1` | 35 / 138 of 240 |
| H-NOTIFY | 1x1 | `aecp_fanout.set_name.if0` / the same | 236 / 236 of 240 | `hooks-load-notify.set_name.if0` / the same | 181 / 181 of 240 |
| H-NOTIFY | 8x8 | `aecp_fanout.set_name.if0` / the same | 233 / 233 of 240 | `hooks-load-notify.set_name.if0` / the same | 156 / 156 of 240 |
| H-COUNTERS | 1x1 | - / `counters.all.if0` | 972 of 1000 | - / `counters.loaded.if0` | 979 of 1000 |
| H-COUNTERS | 8x8 | - / `counters.all.if0` | 781 of 1000 | - / `counters.loaded.if0` | 963 of 1000 |
| H-MAAP | 1x1 | `maap.announce.if0` / the same | 499 / 499 of 500 | `backlog-adp.service.maap.last.if0` / `hooks-load-counters.service.maap.last.if0` | 471 / 479 of 500 |
| H-MAAP | 8x8 | `maap.announce.if1` / the same | 498 / 498 of 500 | `backlog-adp.service.maap.last.if0` / `backlog.service.maap.last.if0` | 456 / 469 of 500 |
| H-SRP | 1x1 | `srp.startup.if0` / the same | 178 / 178 of 180 | `backlog-adp-refill.service.srp.first.if0` / `hooks-load-counters.service.srp.last.if0` | none / 112 of 180 |
| H-SRP | 8x8 | `srp.startup.if1` / the same | 176 / 176 of 180 | `backlog-adp-refill.service.srp.first.if0` / `hooks-load-counters.service.srp.last.if1` | none / 78 of 180 |

H-COUNTERS' paths on the answering arm, ms against 20:

| Path | 1x1 | 8x8 | Notices pushed |
|---|---:|---:|---|
| `counters.first`, a change of STREAM_INPUT 0 | 5.64 | 10.16 | one a registration: 16 and 32 |
| `counters.all`, ALL: every other served descriptor | **27.58** | **218.71** | 5 descriptors x 16 = 80, and 19 x 32 = 608 |
| `counters.held`, from its eligibility, W 896.26 and 880.00 | 5.19 | 9.93 | 16 and 32 |
| `counters.loaded`, under the composed load | **20.76** | **36.62** | 16 and 32 |

**The plants.** All 16, at `fa925043`, 1x1 and the product clock, each in a clean clone, each caught by its own words, exit 0:

| Plant | Its first finding |
|---|---|
| `adp-late` | `LATE H-ADP: control.discover.if0: 74.532 ms against its bound 20 ms` |
| `adp-order` | `ORDER H-ADP`: an ENTITY_AVAILABLE on interface 0 carries grandmaster `0000000000000000`, not the one in force |
| `disc-late` | `LATE H-DISC: hooks-late-disc.entity_departing.if0: 129.678 ms against its bound 20 ms` |
| `disc-order` | `ORDER H-DISC`: after the ENTITY_DEPARTING and the ENTITY_AVAILABLE on interface 0 the sink never probed its talker, in a window of 1243 ms |
| `acmp-late` | `LATE H-ACMP: hooks-late-acmp.get_rx_state.if0: 74.760 ms against its bound 20 ms` |
| `acmp-order` | `ORDER H-ACMP`: on interface 0 the command `0x7401`, received after `0x7400`, was answered first |
| `aecp-late` | `LATE H-AECP: hooks-late-aecp.read_descriptor.if0: 76.069 ms against its bound 20 ms` |
| `aecp-order` | `ORDER H-AECP`: `aecp.lock_entity.if0`'s response precedes any face commit since its receive commit |
| `notify-late` | `LATE H-NOTIFY: hooks-late-notify.set_name.if0: 79.352 ms against its bound 20 ms` |
| `notify-order` | `ORDER H-NOTIFY`: `aecp_fanout.set_name.if0`, a notification precedes its response |
| `counters-late` | `LATE H-COUNTERS: counters.first.if0: 81.819 ms against its bound 20 ms` |
| `counters-order` | `ORDER H-COUNTERS`: descriptor `0x0005 0` to one recipient on interface 0, pushes 115.251 ms apart at the wire, under 1000 ms |
| `maap-late` | `LATE H-MAAP: hooks-late-maap.defend.if0: 74.690 ms against its bound 20 ms` |
| `maap-order` | `ORDER H-MAAP`: the allocation report follows no DA_GATE publication |
| `srp-late` | `LATE H-SRP: hooks-late-srp.listener_ready.if0: 75.638 ms against its bound 18 ms` |
| `srp-order` | `ORDER H-SRP`: the MRPDU committed on interface 0 after the Domain record precedes its SR_DOMAIN publication |

## Findings

At the product clock, alone, every hook is within its bound at both points and on both arms but H-COUNTERS, whose ALL push misses.
Under the composed load every hook misses at both points and on both arms but one: H-DISC at 1x1 on the answering arm, 14.03 ms.
So S5's acceptance, each hook within its bound and inside its normative timeout, is met alone but for H-COUNTERS and is not met under the composed load, on `dev-soft-core` as it is.
The CPU budget harness's findings explain the composed misses, and their two starvations reproduce here on the platform's image at 100 MHz: SRP takes no record in the idle arm's ADP backlog windows, and the ACMP core drops the commands it cannot owe ([its Findings](../ctrl_service_budget/README.md#findings)).
The firmware cuts that answer them are S2b's (#810), not merged at this base, so these figures are the hooks' before.
No ordering check found a defect, every check applied at every point it can, and no path fits by less than the layout swing.

- **H-ADP.** Alone at most 3.37 ms (8x8, LINK_DOWN). Under the composed load its worst, the burst's last ADP record, is 21.26 to 44.15 ms. The 2 s random window leaves 1956 ms or more.
- **H-DISC.** Alone at most 15.93 ms (8x8, idle arm, an ENTITY_AVAILABLE on interface 1). Under the composed load 21.79 to 37.32 ms, but 14.03 ms at 1x1 on the answering arm. The ordering check applied at every point; at 8x8 on the answering arm it left one instance undecided, the sink's TMR_DELAY running past the next ADP record ([Grading](#grading)). At the 50 MHz history clock H-DISC missed alone at 8x8 (24.15 ms, [History](#history)); at 100 MHz it fits.
- **H-ACMP.** Alone at most 15.99 ms (8x8, idle arm, UNBIND_RX). Under the composed load the four commands behind the owed one are never answered, at both points and on both arms, after at least 363 ms: their controller's 200 ms timeout (Milan v1.2 Table 5.26) expires. The owed command itself is answered after 77.84 ms (1x1) and 90.26 ms (8x8), inside 200 ms but over 20.
- **H-AECP.** Alone at most 2.40 ms. Under the composed load the burst's last AECP response takes 48.47 to 205.20 ms. The idle arm's worst are `backlog-adp` and `backlog-adp-refill`, 159 ms at 1x1 and 205 ms at 8x8, where the change notices retry each millisecond after the bind ([Limits](#limits)); the answering arm's worst is 85.82 and 102.26 ms. The 8x8 idle worst leaves 35 ms of the 240 ms timeout.
- **H-NOTIFY.** Alone a fan-out to every registration takes at most 3.78 ms at 1x1 (16) and 6.85 ms at 8x8 (32). Under the composed load, SET_NAME last of the AECP ring's burst reaches its last registration after 59.38 and 84.07 ms.
- **H-COUNTERS.** A push costs about 32,000 to 36,000 CPU cycles a notice, with the CTR window answered at the slowest the contract allows. So one descriptor to every registration fits, 5.64 and 10.16 ms, and the held push fits from its eligibility. ALL, every other served descriptor to every registration, is 80 notices at 1x1 and 608 at 8x8, and takes 27.58 and 218.71 ms; 20 ms holds about 57 notices at 35,000 cycles each. Under the composed load the one-descriptor push takes 20.76 and 36.62 ms. The spacing check applied to 16 and 32 instances without a finding. Every figure is far inside the 1 s update.
- **H-MAAP.** Alone at most 1.76 ms. Under the composed load its worst, the burst's last MAAP record, is 21.25 to 44.19 ms. The 500 ms probe interval leaves 456 ms or more.
- **H-SRP.** Alone at most 4.04 ms (SRP's startup). Under the composed load, on the idle arm, SRP takes no record in `backlog-adp` and `backlog-adp-refill` at either point, its records waiting at least 524.8 to 567.5 ms by the run's end. Those are the windows where the CPU budget harness's formal arm starves SRP too: `srp_mbx.c` (`rx_order_ready`) takes a record only when no TICK is owed and no event is pending. On the answering arm SRP is served, its worst last record after 68.05 ms at 1x1 and 102.31 ms at 8x8, against 18 ms. These composed rows open with every bucket full and the grandmaster changes first, the burst in the SRP row's scope.

## History

Before the owner's decision of 2026-10-30 the product's split CPU clock was the Milan clock, 50 MHz, and this harness graded there. These are its last runs at that clock, at `3c514839`, the four combinations regraded at that head.
They are history, not the product's figures, and are not re-measured: `--cpu-clock milan` gives them again.
That head had neither the layout swing nor H-DISC's undecided rule. None of these runs had an ordering finding or a refusal.

1x1, CPU 50 MHz on the Milan clock, ms; bold is over its bound:

| Hook | Bound | Alone, idle | Alone, answering | Under load, idle | Under load, answering |
|---|---:|---:|---:|---:|---:|
| H-ADP | 20 | 1.11 | 1.11 | **51.38** | **34.33** |
| H-DISC | 20 | 8.83 | 1.14 | **43.82** | **22.60** |
| H-ACMP | 20 | 12.52 | 1.23 | **never served** | **never served** |
| H-AECP | 20 | 3.10 | 3.10 | **255.51** | **106.87** |
| H-NOTIFY | 20 | 6.37 | 6.37 | **94.72** | **94.72** |
| H-COUNTERS | 20 | - | **46.80** | - | **33.52** |
| H-MAAP | 20 | 1.24 | 1.24 | **51.42** | **34.32** |
| H-SRP | 18 | 3.22 | 3.22 | **never served** | **115.55** |

8x8, CPU 50 MHz on the Milan clock, ms; bold is over its bound:

| Hook | Bound | Alone, idle | Alone, answering | Under load, idle | Under load, answering |
|---|---:|---:|---:|---:|---:|
| H-ADP | 20 | 5.21 | 5.21 | **64.47** | **54.31** |
| H-DISC | 20 | **24.15** | 2.01 | **53.85** | **34.21** |
| H-ACMP | 20 | 19.06 | 2.83 | **never served** | **never served** |
| H-AECP | 20 | 4.35 | 4.35 | **315.06** | **151.79** |
| H-NOTIFY | 20 | 11.88 | 11.88 | **138.87** | **138.87** |
| H-COUNTERS | 20 | - | **371.62** | - | **52.49** |
| H-MAAP | 20 | 2.44 | 2.44 | **59.34** | **54.29** |
| H-SRP | 18 | 6.53 | 6.53 | **never served** | **180.70** |

## Limits

- Ends are mailbox commits. Ingress, egress, wire departure and the network are not measured, so the margins are what remains for them, not a wire proof. ACMP's wire round trip and MAAP's egress are lane S8's.
- The idle arm's face block never answers a window, as on the split SoC without the datapath. So AECP's change notices retry every millisecond after a bind, as the CPU budget harness found, and the figures after a bind include those passes. The answering arm separates them.
- The answering arm answers CTR and GSI only, with the values above, at the contract's slowest. It is a test arm, not the datapath; the placement switch (S6) connects the real one.
- One phase is measured per probe; the CPU budget harness's pass bound covers any phase under the same passes.
- The filter checks of the hook rows (tagged frames, wrong destinations, wrong subtypes, FILTER_MISMATCH) are lane FC's, in the mailbox suite (`tb/verilator/mbx`), and are not repeated here.
- Not every required check of the hook rows is run: SHUTDOWN (the platform never disables ADP), every Table 5.54 cell, received validities of 10 and 31, reset and timer wrap, CPU stalls, both bus adapters, flash erase and program waits (zero here, as in the CPU budget harness), lock expiry and the Identify spacing are not.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the platform is linked.
- The plants run at 1x1 and the product clock only.
- The CPU runs at 100 MHz behind this base's crossing to the bus. The product wiring of the 100 MHz decision has no crossing, so it is not measured here; it reaches this harness with S2b (#810), and these figures include the crossing's latency.
- The retried change notice's row, graded from its port's answer against 20 ms ([the ruling of 2026-11-04](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6630265194)), belongs to S2b's firmware, which bounds the retry, and to its harness. At this base the notice retries each millisecond while its window is unanswered (above). Neither arm here switches from unanswered to answering, so that row is not measured.
- The 50 MHz figures are history and are not re-measured at this head. The 50 MHz runs recorded before the 100 MHz decision are in [History](#history).

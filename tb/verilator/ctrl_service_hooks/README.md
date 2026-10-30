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
- **The clock.** The split CPU's product clock is 50 MHz and its bus 100 MHz. Every run is also made at a 100 MHz CPU, a labelled variant, because the owner's clock decision is pending ([the correction](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6508196970)). No figure here presents the variant as the product's.
- **The firmware.** `dev-soft-core` as it is: S2b's firmware cuts are not merged.

## Contents

- **[Run and reproduce](#run-and-reproduce)** -- The prerequisites, the points, the clocks, the face arms, the plants and the self-test.
- **[The SoC and the testbench](#the-soc-and-the-testbench)** -- What is the CPU budget harness's, what this harness adds, and the two face arms.
- **[The hooks](#the-hooks)** -- Each hook's paths, bound, normative timeout, ordering obligation and plants.
- **[Grading](#grading)** -- The bound, the margin, alone and under load, the ordering checks, and a superseded probe.
- **[Results](#results)** -- Each hook at both points, both clocks and both arms, and the plants.
- **[Findings](#findings)** -- What the measurement shows, by hook.
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
At `8x8`, and only there, the image and the SoC's memory plan name the ledgered point `platform-8x8-two-interfaces`, which plans 59.0 RAMB36 by the owner's ruling (#665, 6505997821), owed to lane S14.

`--cpu-hz 100000000` runs the labelled 100 MHz CPU variant; the bus stays at 100 MHz.
`--arm answering` runs the labelled answering-face arm ([The SoC and the testbench](#the-soc-and-the-testbench)), the only arm with H-COUNTERS.
So the eight runs of [Results](#results) are these two commands with each of the four combinations added.

Without `--record-findings` a path over its bound fails the run.
With it, the paths over their bounds are recorded and the run still fails on any refusal and on any ordering finding.
`--groups` selects groups and `--jobs` sets how many run at once (8 by default).
`--reuse-build` reuses a build only if every input recorded in its `build.json` still has its digest: the image, its runtime, the ROM files, the testbench as built, the CPU budget harness's testbench and observers, the SoC Verilog, this harness's SoC and build modules, and the firmware and configuration trees.
`--regrade` grades the logs already in the results directory, on a reused build, and refuses a group whose log is absent or whose script the groups no longer make.

A plant builds a scratch copy of the firmware's tree with one planted defect, at 1x1 and the product clock, and runs the plant's group:

```sh
python3 -B tb/verilator/ctrl_service_hooks/run.py --plant adp-late --build-dir /tmp/hooks-plant-adp-late
```

The plants are `adp`, `disc`, `acmp`, `aecp`, `notify`, `counters`, `maap` and `srp`, each `-late` and `-order`.
The run prints `PLANT <name> caught: <its finding>` and exits 0 when its hook's finding starts with the plant's words, and `ESCAPED` and 1 otherwise.

The directory has no Makefile, for the CPU budget harness's reason: the serial sweep discovers every Makefile, and registering a suite is a CI change.
The TSN stack boundary gate finds `hooks_build.py` by text, because it names the firmware's tree; it is listed in [`ctrl_configs.py`](../../../sw/firmware/ctrl/test/ctrl_configs.py) `OUTSIDE` with its reason.

## The SoC and the testbench

[`hooks_soc.py`](hooks_soc.py) builds the CPU budget harness's split SoC from its own parts ([`split_soc.py`](../ctrl_service_budget/split_soc.py), imported read only):

- the shipping VexiiRiscv with the split placement's 4 KiB instruction cache, the CPU at the Milan clock (50 MHz, or the variant's 100 MHz) and its bus at 100 MHz;
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
| H-AECP | family `aecp`: every solicited response, AECP records under load | 20 ms | 240 ms (IEEE 1722.1-2021 9.3.2.6) | Every face value a response promises is committed before the response (ARCHITECTURE_HW_SW_SPLIT.md section 1; Milan v1.2 5.4.5.2; IEEE 1722.1-2021 7.5.2) |
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

### The plants

Each plant is a scratch copy of the firmware's tree with its edits, every anchor found exactly once ([`hooks_build.py`](hooks_build.py), `planted`), never an edit of the checkout.
A late plant spins 60,000 turns, about 60 ms of the 50 MHz CPU, in the hook's service path; an ordering plant reorders the hook's outputs or the state they carry.

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
- its margin is its family's normative timeout less W and the path, the allowance left for ingress, egress and the network, which this harness does not measure;
- it is under the composed load when its group is one of the CPU budget harness's backlog rows or one of this harness's composed rows.

Each hook's figure is its worst path alone and its worst under the composed load.

H-COUNTERS' held push is graded from its eligibility, as the hook row says ("previous notification wire time supplies eligibility"): from 1 s after the first push's last departure at the wire, or from the change if later, to its last recipient's commit.
The time it was held after the change is its W, recorded beside it.

Each ordering check reads the order of the hook's outputs and the state they carry, never their latency, and counts the instances it applied to.
A check that applied to nothing is reported as not applied, never as passed.
On the idle arm H-COUNTERS' check has nothing to apply to, by construction.

**A superseded probe.** On the platform image at 8x8, the CPU budget harness's `acmp.tmr_no_adp.if1` (group `acmp-disc`) finds no TMR_NO_ADP expiry after its mark.
Interface 1's sink re-arms its aging timer, from an ENTITY_AVAILABLE with valid_time 1, after that group's mark, so the expiry 2 s later falls past the group's 1.9 s window.
`hooks-disc-aging` measures the same path with its window opened after the arm.
A refusal of the earlier probe is reported as superseded only where `hooks-disc-aging` measured the same path on the same interface (`hooks.SUPERSEDED`); any other unmeasured path is a refusal and fails the run.

[`hooks_selftest.py`](hooks_selftest.py) (`run.py --self-test`) pins the bounds, the normative timeouts and the clock labels.
It runs each ordering check on a clean synthetic log, which it must apply to and pass, and on a defective one, which it must report by its hook's words.
It checks every plant's and testbench addition's anchors against the checkout, the held push's eligibility, the findings by hook, the superseded rule and the aging window.
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
| label: the variant labelled the product's | the clock labels |
| split: the counter change is no pad | own lines are split off |
| H-ADP: the grandmaster is not checked | H-ADP ordering |
| H-DISC: the sink's PROBE_TX_COMMAND is never recognised | H-DISC ordering |
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
| findings: a path over its bound is not a finding | findings by hook |

A mutant whose name ends in "(earlier rule)" restores a rule this harness had before its check, so that check is the test that fails on it.

## Results

(filled from the runs at the head)

## Findings

(filled from the runs at the head)

## Limits

- Ends are mailbox commits. Ingress, egress, wire departure and the network are not measured, so the margins are what remains for them, not a wire proof. ACMP's wire round trip and MAAP's egress are lane S8's.
- The idle arm's face block never answers a window, as on the split SoC without the datapath. So AECP's change notices retry every millisecond after a bind, as the CPU budget harness found, and the figures after a bind include those passes. The answering arm separates them.
- The answering arm answers CTR and GSI only, with the values above, at the contract's slowest. It is a test arm, not the datapath; the placement switch (S6) connects the real one.
- One phase is measured per probe; the CPU budget harness's pass bound covers any phase under the same passes.
- The filter checks of the hook rows (tagged frames, wrong destinations, wrong subtypes, FILTER_MISMATCH) are lane FC's, in the mailbox suite (`tb/verilator/mbx`), and are not repeated here.
- Not every required check of the hook rows is run: SHUTDOWN (the platform never disables ADP), every Table 5.54 cell, received validities of 10 and 31, reset and timer wrap, CPU stalls, both bus adapters, flash erase and program waits (zero here, as in the CPU budget harness), lock expiry and the Identify spacing are not.
- The firmware polls (`CTRL_MBX_WFI` undefined), as the platform is linked.
- The plants run at 1x1 and the product clock only.

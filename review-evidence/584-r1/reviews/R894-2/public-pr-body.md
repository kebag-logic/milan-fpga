[A818]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev-soft-core`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

Green, review ready at `64d539f12532b2591f734b8e756f8a9358bb742c`, round 2 (corrections for R894-1 and R893-1). Every local gate below passes, apart
from the builder suite's two not-run gates and the docs workflow's four hosted-environment rows, which fail as at the
base. One decision is open: the owner's disposition of the 8x8's backing (Description). `pf-584-1` ->
`dev-soft-core`.

Round 2 changes no RTL, firmware or entity model; all five configurations' builder outputs are byte-identical to
round 1's, so round 1's route, firmware bank and saved-state evidence carry. It adds `milan_dp_render`'s `ship8` case
and its planted faults, states the backing deviation as pending, corrects the memory figures and the stale waiver
text, and republishes the receipt index from the published bytes.

## Linked Issue / roles

Closes #584
Relates to #665

Executor: `[A818]`
Internal cleared-context reviewer: `[R<n>]` (assigned by the manager)
External reviewer: `[R<n>]` (assigned by the manager)

## Description

Every STREAM_PORT_INPUT of every tracked configuration now owns at least one AUDIO_CLUSTER (Milan v1.2 5.3.3.8),
derived from the configuration, with its meaning stated and, where the board routes a sink, backed.

**Pending owner disposition.** The owner's decision of 2026-11-22 asked to back the input model with the loopback
lane and the first TDM8 channel only. This change departs from that wording in two ways, stated in
[#584's decision comment](https://github.com/kebag-logic/milan-fpga/issues/584#issuecomment-7077045073) and awaiting
the owner's disposition there:

- No input cluster is backed by the loopback lane, and the 8x8 builds no loopback lane (`fabric.loopback_lane:
  false`, as before). The lane's feed is the depacketizer clone of every received stream, which no input mapping
  steers, so an input cluster named for it would claim a route no mapping can make. Ports 1-7 own `Unrouted S<p>`
  clusters, which reach no pin; they are not loopback clusters.
- The first render channel is slot 0 of the 8x8's TDM32 bus, `TDM32 Out 0`, standing for the decision's first TDM8
  channel: the 8x8's bus is TDM32.

D8, D10 and the descriptor-ownership page say the same. If the owner requires loopback-backed input clusters, the
model and the lane posture change in a later round.

| Configuration | Input ports' clusters | Backing |
|---|---|---|
| 8x8/1if | port 0: `TDM32 Out 0`; ports 1-7: `Unrouted S<p>`, one each | port 0's is slot 0 of the TDM32 bus on `tdm.dout` (J11.5), the first key of the crossbar's TDM render lane; ports 1-7 project onto no render key |
| 1x1/1if TDM8 | port 0: `TDM8 Out FL..SR` (8) | unchanged: TDM8 slots 0-7; artifacts byte-identical |
| Arty (3) | unchanged | artifacts byte-identical |

No input cluster is named for the loopback lane: its feed is the depacketizer clone of every received stream, which
no input mapping steers; it stays the backing of the output ports' loopback clusters where a build has it (the 1x1 has
it, the 8x8 does not). Output ports keep their clusters. No STREAM_PORT_INPUT owns an AUDIO_MAP (Milan v1.2 5.3.3.9):
the builder already refused a static listener map, so D1's "one AUDIO_MAP per port" text is corrected.

| Piece | Change |
|---|---|
| Builder | `unrouted` role: one mono cluster on an input port no render channel reaches. `cluster_mapping.render_ports` (`every`, D8's default; `first`, the 8x8's): which input ports own the physical render channels. `STREAM_PORT_CLUSTER_MINIMUM`: a resolved layout with a zero-cluster port of either direction is refused by name. A master TDM render lane may be narrower than its bus. The 8x8's L1 model-lint waiver is gone |
| Gateware | `KL_tdm_render_master` gains `BUS_SLOTS_P`: it frames the bus's slots and stores only the first `SLOTS_P`, serializing zero after them; a full-width lane elaborates as before. The datapath passes `BUS_SLOTS_P = AUDIO_IF_SLOTS_P` and keeps the narrow-lane refusal for a slave lane |
| 8x8 config | `physical_channels.render: 1`, `cluster_mapping.render_ports: first`; the stale "the board routes nothing" comments corrected (the J11 TDM header has been routed since the item-4 header) |
| Identity | 8x8 `entity_model_id` `0x001BC5F6CB4A37D1` -> `0x001BC5CFD464421E` (IEEE 1722.1-2021 6.2.2.8, #495: `render_ports` is hashed when declared); the 1x1 and Arty ids unchanged |
| Firmware memory | the 8x8 images grow by 1,336 B of `rom` at three points and 1,344 B at the size fixture's 8x8/2if, and by 1,744 B of `sram` at three points and 1,808 B at the platform's 8x8/2if (`SPLIT_CONTROL_MEMORY.md` section 3 gives each image's sizes); each 8x8 control image plans one more RAMB36, recorded as ROM debt owed to S14 (the owner's rule of 2026-11-15): the product 8x8/1if image 58.0 -> 59.0, the platform 8x8/2if 63.0 -> 64.0, the size fixture's 8x8/2if 60.5 -> 61.5 (its arms' most) and its 8x8/1if 56.0 -> 57.0, a new ledgered point. Each entry is the most any image of its point plans, every harness variant, arm and plant linked at the head and at the base; the 1x1 images are unchanged to the byte |
| 8x8/1if image | routed on the recipe's three placement directives: #818's floor met at every corner on all three, best AltSpreadLogic_high at +0.363 ns setup and +0.036 ns hold. 44,191 to 44,610 LUT (+1,089 to +1,625 against the flip's image on the same directive), 53,066 FF (+2,072), 99 BRAM tiles (+4.5: the render queue's 4 RAMB36 and the control memory's tile), 15,667 to 15,694 slices. The growth is the render path the first TDM channel brings into the 8x8: the render crossbar (451 LUT, 1,605 FF), the render queue's memories and the 71-LUT render master. The head's route inputs equal the routed commit's (17 compared, 0 differ) |
| Tests | firmware host tests `Inputs.*` at every tracked configuration (the entity-model check over AECP; REMOVE_AUDIO_MAPPINGS of a non-empty list on every input port); builder tests for the named refusal and the derived pools; the `tdm_render` suite's four narrow-lane legs, one on the real capture master's pins; the all-fabric 8x8 leg of `milan_dp` graded for one cluster per port (the loopback-on control); `milan_dp_render`'s new `ship8` case, the 8x8 render lane as it ships, at the pins: the builder's own render parameters for the 8x8 (eight listeners, TDM32 master, one render slot, loopback and DAC lanes off), eight live streams, slot 0 graded for port 0's selected source at its presentation time and slots 1-31 for zero, across power-on, remaps, mapped unrouted ports, REMOVE, bind falls and a reset; `ship8-mutants` plants projection, adapter and bus-binding faults, each caught |
| Docs | `ENDSTATION_BUILDER.md` (index, D1, D2, D8, D10, sections 1 and 4), `PP_DESCRIPTOR_OWNERSHIP.md` (processor #122 disposition), `SUBMODULES.md`, `SPLIT_CONTROL_MEMORY.md`, `SAVED_STATE_FASTCONNECT.md` 4.2, `SAVED_STATE_FORMAT_32X32.md` and the 8x8 record table regenerated, `TESTING.md`, the changelog |

What a mapping does on the 8x8: on STREAM_PORT_INPUT 0 a mapping of stream 0's channel c to its cluster is stored by
the AECP owner, committed through the EDIT window to input key 0 and projected onto render key 2, so listener 0's
channel c is placed once per media tick in slot 0 of the 32-slot frame on `tdm.dout`, 24-in-32 MSB first; REMOVE
renders zero there. On ports 1-7 the mapping is stored, returned and saved and changes no route. At power-on each port
holds D7's identity map, stream p channel 0 on its one cluster. On Ethernet an edit is its AECP response and
notification only.

## Authoritative references

- Milan v1.2 5.3.3.7-5.3.3.9 (printed p. 27), 5.4.2.26-5.4.2.28.
- IEEE 1722.1-2021 6.2.2.8, 7.2.13 (Table 7-23), 7.2.16, 7.2.19.
- [#584](https://github.com/kebag-logic/milan-fpga/issues/584): the approved design and fallback, the parking, and
  issuecomment-7077045073 (this round's decision).
- [Processor #122's disposition](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/122#issuecomment-5853884588).
- `docs/ENDSTATION_BUILDER.md` D1, D2, D7, D8, D10; `docs/design/SPLIT_CONTROL_MEMORY.md` sections 3 and 5.

## How to get into the same state

```sh
git fetch origin 64d539f12532b2591f734b8e756f8a9358bb742c && git checkout --detach FETCH_HEAD
test "$(git rev-parse HEAD)" = 64d539f12532b2591f734b8e756f8a9358bb742c
git submodule update --init protocol-processor gptp-processor third_party/verilog-axis third_party/tsn-c-stack third_party/lwSRP
python3 sw/builder/endstation_builder.py configs/endstation_ax7101_8x8.yaml
```

## How to validate

```sh
python3 sw/builder/test_builder.py --require-rv32 --require-elaboration
(cd sw/builder && python3 -c "import test_declarations as t; t.test_stream_port_cluster_minimum(); t.test_input_cluster_pools()")
python3 sw/firmware/ctrl/test/aecp_arms.py --output /tmp/aecp-inputs --inputs
python3 sw/firmware/ctrl/test/test_ctrl_firmware.py --require-rv32 --self-test
make -C tb/verilator/tdm_render && make -C tb/verilator/tdm_render master-mutants
make -C tb/verilator/milan_dp build-nxn8 exec-nxn8
make -C tb/verilator/milan_dp_render ship8 && make -C tb/verilator/milan_dp_render ship8-mutants
python3 sw/litex/test_ctrl_memory.py
python3 tb/verilator/ctrl_split_boot/plat_ledger.py --build-dir /tmp/plat-ledger
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 1x1/1if
python3 -B tb/verilator/ctrl_service_budget/flip_grade.py --check --point 8x8/1if
python3 scripts/check_nvm_capture.py
python3 scripts/check_nvm_format_32x32.py && python3 scripts/check_nvm_record_space.py
python3 scripts/check_entity_shape.py
bash scripts/run_all_suites.sh <logs> --wait
```

Expected result / pass criteria:

- The builder suite prints `ALL GATES PASS EXCEPT 2 NOT RUN` over its two legs (gate 1b's arm for a make that does
  not re-read MAKEFLAGS; gate 11's bench-local calibration report), as at the base.
- The two #584 builder tests pass; five planted builder defects (`render_ports` ignored, the unrouted fallback
  dropped, the minimum check stubbed, an unrouted cluster projected, a narrow slave lane accepted) each fail them.
- `aecp_arms.py --inputs` passes at all five tracked configurations; at the base tree the 8x8 fails both tests with
  "STREAM_PORT_INPUT 0 owns an AUDIO_CLUSTER (Milan v1.2 5.3.3.8)" and "holds a mapping to remove". The firmware
  bank passes with every planted defect caught, the two new ones (`input-port-served-headless`,
  `remove-keeps-its-rows`) included.
- `tdm_render`: the four lane legs and the slave bench pass; `master-mutants` catches 5 of 5.
- `nxn8` passes with the 8x8 graded for one cluster per port (render key 2 driven by port 0 alone).
- `ship8` passes, 124 checks: every window decodes whole 1024-bclk frames; slot 0 carries port 0's selected source (stream 0 channel 0 at power-on, then stream 0 channel 5, stream 3 channel 2 and stream 0 channel 1) in every frame at its presentation time, slots 1-31 zero; ports 1-7 mapped with their streams live leave the pins unchanged; REMOVE gives 32 silent slots; a bind fall on stream 5 opens no epoch, one on stream 0 opens one and silences the slot, and the rebind and a reset render only later events. `ship8-mutants` prints `6 checks: 6 PASS`: the clean leg, four plants caught by name and the bus mis-tie refused at elaboration.
- `test_ctrl_memory.py` and `plat_ledger.py` pass: the product 8x8/1if image plans 59.0 RAMB36 at its entry, the
  platform 8x8/2if 64.0, the 1x1 points 45 and 46 as at the base.
- `flip_grade.py`: 1x1/1if load 0.511 (0.70), last queued notice 127.31 ms (140), ACMP 29.06 ms (30), txL 47.88 ms
  (49); 8x8/1if load 0.744 (0.75). Unchanged: the change touches no stated cost.
- `check_nvm_capture.py` passes against the re-measured receipt: the 8x8 maximum is 14.533 ms at 50 MHz (24.5 ms
  bar; 13.861 ms before, at 164 records), 10.944 ms at the 100 MHz comparison clock; the 1x1 arms are unchanged.
- The split saved state at 8x8 (`nvm_split_target --point 8x8`): every case passes and every service step is within
  T_svc 20 ms (longest 1.039 ms); the capture of 172 records takes 28.888 ms of CPU time over 66.785 ms elapsed,
  recorded, as the owner's 2026-10-29 decision has it.
- `check_nvm_format_32x32.py` and `check_nvm_record_space.py` pass: the 32x32 TDM8 bound shape, which sizes layout 3,
  is unchanged; the 8x8's record table and the section 4.2 figures are regenerated.
- `check_entity_shape.py` passes (176 checks).
- 8x8/1if routed on the three placement directives, each meeting #818's floor at every corner: ExtraPostPlacementOpt
  +0.123 / +0.015 ns, AltSpreadLogic_high +0.363 / +0.036 ns, ExtraTimingOpt +0.207 / +0.036 ns (WNS / WHS, worst
  corner); the head's route inputs equal the routed commit's, 17 compared, 0 differ.
- The docs workflow's 103 commands: 99 pass; the four that read the hosted environment (`act_ci.py`'s install
  directory and `GITHUB_EVENT_PATH` three times) fail here as they do at the base.
- `run_all_suites.sh`: all 65 suites pass. `fw_service_budget` passes on its regenerated 8x8 trace row (oracle 55
  checks, flash 19 checks, 0 failures); the 1x1 rows and their image are unchanged. Round 2 touches one suite,
  `milan_dp_render`, and its full default target passes with the new case (ship 263 checks, multi 79, ship8 124, the
  five leg-side defect arms caught).

## Known limitations / out of scope

- The 8x8 renders its **first** TDM channel only, on port 0. No input cluster is backed by the loopback lane, and
  the 8x8's lane stays off (`fabric.loopback_lane: false`), so its talkers' loopback clusters still carry silence:
  both are pending the owner's disposition (Description).
- `ship8` drives the all-fabric AECP face. The split product's control CPU writes the same edit beats into
  `i_ctl_edit_*`, which `milan_datapath` assigns to `ppo_amap_edit_*` (its `CTRL_SPLIT_P = 1` arm), so from there the
  transaction server, map store, projection, crossbar, render stage, adapter and serializer are one path. Its clocks
  are model rates (axis 100 MHz, TDM 98.303 MHz); the shipping image clocks axis at 50 MHz.
- The in-order binding of the render channel is the declared `cluster_mapping.render_ports: first`, not a new default:
  changing D8's every-port default would move the 32x32 TDM8 bound shape that sizes saved-state layout 3, and with it
  the 1x1's own `nvm_split.json`.
- `render_ports: every`, the default, still lets several input ports' clusters project onto one render key (the last
  edit drives it). No tracked configuration has two listeners with physical render channels under it; the 32x32 TDM8
  bound shape does. Recorded here for a follow-up decision, not changed.
- Each 8x8 control image plans one more RAMB36, recorded as ROM debt owed to S14 (the owner's rule of 2026-11-15); the
  8x8/1if image fits the device (99 of 135 BRAM tiles, 44,191 to 44,610 of 63,400 LUT) and closes.
- The CPU budget harness's measured rows at 8x8/1if (64 parts) were not re-run: the flip check reads stated costs, which
  no part of this change touches (no record type's cost depends on the input-port cluster count beyond one map key a
  port). The split saved state was re-measured at its 8x8 point only (two interfaces, the harness's point); its base
  was not re-run at this clock.
- The all-fabric processor's out-of-context 8x8 endpoint (`pp_resource_gate.py check`) was not re-synthesized: the
  September area STOP priced that processor, which the split does not build. The all-fabric 8x8 now has 115 writable
  names, within its 128-record NAME block.
- The service-budget trace's 8x8 row (`tb/verilator/fw_service_budget/oracle.json`) is regenerated, because it pins
  the 8x8 image. On the all-fabric 8x8 product firmware, the `milan_nvm` console listing of the populated store was
  already over the harness's 500 ms per-command budget at the base (860.4 and 862.4 ms, recorded as
  `over-budget duty: milan_nvm`). It takes 901.6 and 903.6 ms here, because it walks 172 records instead of 164. The
  command keeps serving inside its handler (period bound margin +131 ms, heartbeat gap 345.3 of 500 ms). No owner
  bound covers it and no issue tracks it yet, so it is recorded here for a follow-up; this change does not fix it.
- No bench run: the bench scenarios are re-run after merge. The model-identity change means a controller re-reads
  the 8x8 model.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied
- [ ] New or changed behavior has self-checking tests
- [ ] Required local verification bar passes
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [ ] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done


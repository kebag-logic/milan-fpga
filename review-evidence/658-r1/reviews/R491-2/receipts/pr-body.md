[A539]

## Contents

- **[Status](#status)** — Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** — Public task, executor, and independent reviewers.
- **[Description](#description)** — What changed and why.
- **[Authoritative references](#authoritative-references)** — Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** — Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** — Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** — What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** — The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN at `5747a8cb` (on dev `510fae60`, merged with `--no-ff`). Every
suite that compiles `milan_datapath.sv` passes: `milan_dp` 12,064 checks,
`milan_dp_render` 334, `capture_coherence` 21,194, `pp_shadow` 2,184 and
`milan_dp_mclk` 168, all with 0 failures (35,944 in total). The `[DYNMAP]` leg
reports 162 checks and 0 failures. `dynmap-mutants` passes 16 of 16, and all 11
of review R490-1's probes that its round killed or asked for are KILLED. The
nightly physical gPTP leg passes (179 checks, 0 failures). Yosys passes 55 of
55 tops, and the builder bank, lint, xvlog, source-list and docs gates all
exit 0. The bench read of the power-on maps is pending: the manager does it
after flashing.

`658-dynmap-default` -> `dev`.

## Linked Issue / roles

Closes #658
Relates to #70 (saved-state stage 3 takes the boot window over), #583 (the Arty observation), #645 (also edits `milan_datapath.sv`)

The bench read of the power-on maps on the AX7101 stays with the manager, after flashing.

Executor: `[A539]`
Internal cleared-context reviewer: `[R490]`
External reviewer: `[R491]`

## Description

The AX7101 powered up with every audio map empty: no store that GET_AUDIO_MAP
reads had a reset value but zero, and nothing wrote one at boot (#658 stage 1,
comment 5988813022). The owner's ruling (comment 5988843004) is implemented:

- **Power-on map, option A.** On every dynamic Stream Port, stream channel c
  maps to the port's cluster c, for c below the smaller of the channel count
  and the cluster count. `milan_datapath` computes the image from the existing
  `ADP_DMAP_*` constants and the declared default formats, with the bounds an
  ADD is validated against. It is the reset value of the input store and of
  the output owner and cluster registers.
- **Milan v1.2 5.4.2.7 kept.** A SET_STREAM_FORMAT that would orphan a mapping
  is still refused with BAD_ARGUMENTS. Nothing prunes or adds mappings at run
  time, so narrowing a stream needs a REMOVE first.
- **The restore clip.** From reset until the restore's terminal (D3 COMPLETE or
  DEFAULTS, the cycle AECP is released; or CLOSED), the stores hold the image
  without the mappings the CURRENT format does not carry. A persisted narrower
  format therefore restores beside a clipped map, it is kept, and nothing is
  notified because no controller can be registered yet. Both directions.
- **The crossbar RAMs** take the same set from a boot writer on the existing
  AECP write legs: continuously in the window, then one final sweep and a
  drain clock. While it runs the edit face waits and the CSR map writer is
  refused. Reset images in the two leaves were not used: the clip needs the
  writer anyway, and they would have been leaf parameter changes.
- **The boot window's guard arms are graded** (review R490-1 F1). The CSR
  hold, the CLOSED terminal, the sweep after the terminal, its drain clock and
  the edit face's wait each guard a clock the round-1 scenario never reaches.
  `[DYNMAP]` now stages each one on its clock, and `dynmap-mutants` removes
  each one and requires its named check to fail.

No port, register field, parameter, leaf module or processor file changes.
The lane merges dev `510fae60` (#663, processor pin `ead80360`) with `--no-ff`.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | The identity image (constant functions), the boot clip (`amap_boot_clip`), the boot writer (`amap_boot_walk`, `amap_boot_slot`) on the `amap_edit_iwr/owr` legs, the edit-face wait and the CSR hold while it runs. Comments that said the RAMs have no seeder corrected. Hunks stay in the map stores, their writers and resets. |
| `tb/verilator/milan_dp/sim_nxn.cpp` | `[DYNMAP]` to the stage-2 ruling: power-on maps on both ports, over the wire and in both crossbar RAMs; 8 -> 4 refused while 4..7 are mapped; REMOVE 4..7; 8 -> 4; 4 -> 8 keeps 4; the output clip in a boot window; a restored 4-channel input format. The guard arms: a CSR map write committed on every clock from inside the window to past the sweep against a forced CLOSED terminal, per side; a D3 roll-back that invalidates both format rows on the clock CLOSED ends the window; an output ADD meeting a sweep held open. An NVM window model and the firmware's load sequence. Re-based empty-start sections: `[AMAP]`, `#67`, `#67dv`, the 8x8 `0x002C` block, `[T66]`. `await_aecp` takes an optional per-clock callback. |
| `tb/verilator/milan_dp/gen_nvm_window.py` | Frames a saved-state window for a config from `scripts/nvm_shape.py` and `scripts/nvm_klj2.py`; writes nothing unless the codec's own decoder accepts it. |
| `tb/verilator/milan_dp/dynmap_probes.vlt` | Opens the processor's format rows and the D3 writer's CLOSED flag for staging; reads the parent's stores and the CSR commit pulse; opens the post-terminal sweep flag so an edit can meet it. |
| `tb/verilator/milan_dp/dynmap_mutants.py`, `Makefile`, `sim_pool.py`, `README.md` | The `dynmap` leg joins `run`. `make dynmap-mutants` plants 13 defects over three legs: four of the map image and writer, seven guard-arm removals, and the empty reset under the listener and the talker. The README states why the hold's two RAM sites are equivalent on the shipping shape. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp` | Proves the power-on map, REMOVEs it before each permutation, decodes it end to end after a hard reset with no map command (`T18 POWER-ON`), and pads the inserted proofs to whole CRF periods so the #643 law windows keep their phase. |
| `tb/verilator/capture_coherence/sim_dp.cpp` | No CSR map programming: the talker carries the power-on map, so its decoded columns are the talker's end-to-end check. |
| `tb/verilator/pp_shadow/sim_main.cpp`, `README.md` | Each K boot clears the power-on maps through the CSR window, so K12 still starts from an empty map. |
| `scripts/measure_test_evidence.py` | `dynmap_mutants.py` registered as an explained reader of production HDL. |
| Docs | `SAVED_STATE_MATERIALIZATION.md` (section 1 table, section 5.2: the reset and roll-back target is the clipped identity, stage 3 takes the window over; section 8.4: formats judged on "supported" alone, and the clip raises neither the live-write pulse nor map-persistence work); `ENDSTATION_BUILDER.md` D7 (the power-on map, the 5.4.2.7 rule and the bench consequence) and D8; `CHANNEL_MAP_64.md` section 5; `REGISTER_MAP.md` 0x900 (each dynamic direction's store and crossbar; the CSR refusal); `DATAPLANE_WALKTHROUGH.md`; `TESTING.md`; `CHANGELOG.md`. |

### Area

Out-of-context 1x1 recipe (`syn/resmap/datapath_ooc.tcl`, `ship` point
`endstation_ax7101_1x1_tdm8`, xc7a100tfgg484-2, Vivado 2026.1). Base is dev
`510fae60` (processor `ead80360`), head is `5747a8cb`. Both points come from
clean checkouts, and their point files are identical apart from the tree
prefix.

| `milan_datapath` (whole OOC top) | Base | Head | Delta |
|---|---|---|---|
| Slice LUTs, after synth | 43369 | 43508 | +139 |
| Slice LUTs, after opt_design | 42526 | 42863 | +337 (+0.79 %) |
| Flip-flops, after synth | 43398 | 43359 | -39 |
| Flip-flops, after opt_design | 43282 | 43274 | -8 |
| F7 muxes, after opt_design | 949 | 979 | +30 |
| LUTRAM | 3274 | 3276 | +2 |
| BRAM tiles, DSP | 31, 14 | 31, 14 | 0 |

The reset image alone costs nothing: only the stores' reset values change, so
no flip-flop is added. The cost is in the boot writer, the clip and the
edit-face wait. Before this change the processor's `amap_edit_wait_i` was tied
to 0, and synthesis removed its wait path; it is now live.

After opt_design, the instances this change touches move by +137 LUT: the
parent's own cells +3 (and -49 FF), `pp_shadow` +71, `chan_map_capture` +63.
That matches round 1's whole-top +135 on the previous base (`c36bfb03`). The
other +200 is movement between instances whose RTL and connections this
change leaves alone: the gPTP shadow +272, the CSR block -229, the AVTP
parser +72, CRF RX +71 and the talker diagnostics -52, among smaller ones.
That movement is still this change's cost in this measurement. The routed
image's figure, and the `route-1x1` resource-gate record on the merge result
(`docs/design/AREA_BUDGET.md`), are measured in the merge bank. `KL_pp_shadow`
is unchanged, so the standalone `ooc-1x1` and `ooc-8x8` endpoints see
identical inputs.

## Authoritative references

- #658 rulings: comment 5988293154 (the power-on default) and comment 5988843004 (stage 2).
- Milan v1.2 5.4.2.7 (SET_STREAM_FORMAT refused while a mapping would be orphaned), 5.4.2.26 to 5.4.2.28 (GET_AUDIO_MAP, ADD/REMOVE_AUDIO_MAPPINGS), 5.3.9.1 (an output channel is unmapped or mapped to a cluster channel).
- IEEE 1722.1-2021 7.4.9, 7.4.44 to 7.4.46.
- `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 1, 5.2, 8.4 and 8.6.
- `docs/reference/REGISTER_MAP.md` 0x900 (the CSR map window's refusal while the boot writer runs).

## How to get into the same state

```sh
git fetch origin
git checkout 658-dynmap-default
git submodule update --init third_party/verilog-axis protocol-processor gptp-processor
# Verilator 5.050 on PATH
```

## How to validate

```sh
make -C tb/verilator/milan_dp dynmap              # the [DYNMAP] leg alone
make -C tb/verilator/milan_dp_render ltn_rom.hex ucode.hex tdm8r_aemi.bin
make -C tb/verilator/capture_coherence ltn_rom.hex ucode.hex
make -C tb/verilator/milan_dp dynmap-mutants      # 13 planted controls, 3 clean controls
make -C tb/verilator/milan_dp                     # the whole suite, dynmap in the pool
(cd tb/verilator/milan_dp_render && make)
make -C tb/verilator/capture_coherence
make -C tb/verilator/milan_dp_mclk
make -C tb/verilator/pp_shadow
syn/yosys/run.sh
python3 sw/builder/test_builder.py
python3 scripts/lint_rtl.py --check
python3 scripts/check_rtl_source_lists.py
python3 scripts/pp_srcs.py --check
python3 scripts/xvlog_gate.py --check             # on a host with Vivado
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4  # nightly physical leg
```

Expected result / pass criteria: every command exits 0.

- The `[DYNMAP]` leg reports 162 checks and 0 failures. Its CSR hold arms print
  each write's offset from the forced CLOSED terminal: refused through +9 (the
  8-key sweep and its drain clock), landed from +10, and never split between
  the store and the RAM.
- `dynmap-mutants` reports 16 checks, 16 PASS. The generated inputs of the
  render and talker suites must exist first (the two `make ... .hex` lines),
  because the campaign builds those legs without remaking them.
- Review R490-1's probe script, run on this head unmodified, reports P1, P2,
  P3, P5 and P9 KILLED (4, 2, 6, 2 and 4 failures of 162). P4, P6, P7, P8, P10
  and P12 stay KILLED. P11 is equivalent on this shape, as that review found.
- The nightly physical gPTP leg writes the eight capture keys through the CSR
  window after the restore walk, and its payload check needs those words. So
  it grades that the CSR hold ends and that the window is usable after the
  walk. It does not grade the refusal while the hold is up: `[DYNMAP]`'s CSR
  hold arms grade that, and probe P1 is killed there.

## Known limitations / out of scope

- **The bench read** of the power-on maps on the AX7101 is the manager's, after flashing.
- **The hold's two RAM sites are equivalent on the shipping shape.** The boot writer drives both crossbar write legs on every busy clock, and each leaf's mux gives that leg priority over the CSR writer. So removing either RAM site alone changes no write here, and no leg plants it alone. The two store sites are planted alone and caught, and so is the removal of all four (`tb/verilator/milan_dp/README.md`).
- **The edit face's wait is graded with a held sweep.** On the shipping shape the first edit after AECP release reaches the face long after the 8-key sweep ends, so the leg holds the post-terminal sweep open while an ADD is in flight. That models a longer key space or a restore that edits.
- **8x8 (not a shipping image).** The ruled identity maps each output's stream channels 1..7 to that port's first loopback clusters, which carry silence while the loopback lane is off. The builder's unconsumed `AEM_ODMAP_INIT_C` (the task #65 rule) maps only the backed Pilot. Restricting the image to backed clusters is a one-term change if the owner prefers it; on the shipping 1x1 TDM8 shape every identity cluster is backed, so nothing changes there.
- **The output clip cannot be reached by a command today:** the format verdict admits only the declared output channel count. It is graded by staging the processor's row in a boot window (`dynmap_probes.vlt`), with a planted control.
- **#70 stage 3** restores map records through the edit face inside the boot window, which this change holds and recomputes. Stage 3 takes the window over for the ports it restores (recorded in the design page). Map records `0x60` to `0x7F` remain unmaterialized in stages 1 and 2.
- **`CHMAP_STAT`** counts a CSR map write that the boot window refuses as a commit, as it already did for the transaction exclusion.
- **The Arty observation** stays recorded under #583.
- **The xelab-only class** (CONTRIBUTING section 3) was checked by hand: no
  declaration with an initialiser was split. The new variables carry none, and
  the two `wire x = ...` lines are net declaration assignments.

## Definition of Done

- [x] Linked Issue acceptance criteria are satisfied (all but the bench read, above)
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


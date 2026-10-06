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

GREEN at `fb4953bd`: 59/59 suites pass (2,149,203 checks, 0 failures),
`dynmap-mutants` 9/9, Yosys 55/55 tops, and the builder bank, lint, xvlog,
source-list and docs gates all exit 0. The nightly physical gPTP leg passes
on the trial merge with `dev` (179 checks, 0 failures). The bench read of the
power-on maps is pending: the manager does it after flashing.

`658-dynmap-default` -> `dev`.

## Linked Issue / roles

Closes #658, except the bench read of the power-on maps on the AX7101, which the manager does after flashing.
Relates to #70 (saved-state stage 3 takes the boot window over), #583 (the Arty observation), #645 (also edits `milan_datapath.sv`)

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
  AECP write legs: continuously in the window, then one final sweep. While it
  runs the edit face waits and the CSR map writer is held out. Reset images
  in the two leaves were not used: the clip needs the writer anyway, and they
  would have been leaf parameter changes.

No port, register field, parameter, leaf module or processor file changes.

| Piece | Change |
|---|---|
| `hdl/milan/milan_datapath.sv` | The identity image (constant functions), the boot clip (`amap_boot_clip`), the boot writer (`amap_boot_walk`, `amap_boot_slot`) on the `amap_edit_iwr/owr` legs, the edit-face wait and the CSR hold while it runs. Comments that said the RAMs have no seeder corrected. Hunks stay in the map stores, their writers and resets. |
| `tb/verilator/milan_dp/sim_nxn.cpp` | `[DYNMAP]` to the stage-2 ruling: power-on maps on both ports, over the wire and in both crossbar RAMs; 8 -> 4 refused while 4..7 are mapped; REMOVE 4..7; 8 -> 4; 4 -> 8 keeps 4; the output clip in a boot window; a restored 4-channel input format. An NVM window model and the firmware's load sequence. Re-based empty-start sections: `[AMAP]`, `#67`, `#67dv`, the 8x8 `0x002C` block, `[T66]`. |
| `tb/verilator/milan_dp/gen_nvm_window.py` | Frames a saved-state window for a config from `scripts/nvm_shape.py` and `scripts/nvm_klj2.py`; writes nothing unless the codec's own decoder accepts it. |
| `tb/verilator/milan_dp/dynmap_probes.vlt` | Opens the processor's output format row, the only stimulus that reaches the output clip. |
| `tb/verilator/milan_dp/dynmap_mutants.py`, `Makefile`, `sim_pool.py`, `README.md` | The `dynmap` leg joins `run`; `make dynmap-mutants` plants six defects over three legs. |
| `tb/verilator/milan_dp_render/sim_tdm8_render.cpp` | Proves the power-on map, REMOVEs it before each permutation, decodes it end to end after a hard reset with no map command (`T18 POWER-ON`), and pads the inserted proofs to whole CRF periods so the #643 law windows keep their phase. |
| `tb/verilator/capture_coherence/sim_dp.cpp` | No CSR map programming: the talker carries the power-on map, so its decoded columns are the talker's end-to-end check. |
| `tb/verilator/pp_shadow/sim_main.cpp`, `README.md` | Each K boot clears the power-on maps through the CSR window, so K12 still starts from an empty map. |
| `scripts/measure_test_evidence.py` | `dynmap_mutants.py` registered as an explained reader of production HDL. |
| Docs | `SAVED_STATE_MATERIALIZATION.md` (`:188`, `:595-597`, section 8.4: the reset and roll-back target is the clipped identity, the clip raises no record trigger, stage 3 takes the window over); `ENDSTATION_BUILDER.md` D7 (the power-on map, the 5.4.2.7 rule and the bench consequence) and D8; `CHANNEL_MAP_64.md` section 5; `REGISTER_MAP.md` 0x900; `DATAPLANE_WALKTHROUGH.md`; `TESTING.md`; `CHANGELOG.md`. |

### Area

Out-of-context 1x1 recipe (`syn/resmap/datapath_ooc.tcl`, `ship` point
`endstation_ax7101_1x1_tdm8`, xc7a100tfgg484-2, Vivado 2026.1). Base is
`c36bfb03`, head is this PR's head. Both points are clean checkouts with
identical source lists.

| `milan_datapath` (whole OOC top) | Base | Head | Delta |
|---|---|---|---|
| Slice LUTs, after synth | 44253 | 44393 | +140 |
| Slice LUTs, after opt_design | 43634 | 43769 | +135 (+0.31 %) |
| Flip-flops, after synth | 48858 | 48858 | 0 |
| Flip-flops, after opt_design | 48764 | 48770 | +6 |
| F7 muxes, after opt_design | 1260 | 1146 | -114 |
| LUTRAM, BRAM tiles, DSP | 1822, 36, 14 | 1822, 36, 14 | 0 |

The reset image alone costs nothing, as the ruling expected: only the stores'
reset values change, so no flip-flop is added. The cost is in the boot
writer, the clip and the edit-face wait. Before this change the processor's
`amap_edit_wait_i` was tied to 0, and synthesis removed its wait path. It is
now live, which shows as +189 LUT in `pp_shadow` after opt_design. The
parent's own cells grow by +5 LUT and +6 FF. Cross-boundary optimization
moves smaller amounts between other instances, in both directions.

## Authoritative references

- #658 rulings: comment 5988293154 (the power-on default) and comment 5988843004 (stage 2).
- Milan v1.2 5.4.2.7 (SET_STREAM_FORMAT refused while a mapping would be orphaned), 5.4.2.26 to 5.4.2.28 (GET_AUDIO_MAP, ADD/REMOVE_AUDIO_MAPPINGS), 5.3.9.1 (an output channel is unmapped or mapped to a cluster channel).
- IEEE 1722.1-2021 7.4.9, 7.4.44 to 7.4.46.
- `docs/design/SAVED_STATE_MATERIALIZATION.md` sections 1, 5.2, 8.4 and 8.6.

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
make -C tb/verilator/milan_dp dynmap-mutants      # six planted controls, three clean controls
make -C tb/verilator/milan_dp                     # the whole suite, dynmap in the pool
(cd tb/verilator/milan_dp_render && make)
make -C tb/verilator/capture_coherence
make -C tb/verilator/pp_shadow
scripts/run_all_suites.sh "$(mktemp -d)"
syn/yosys/run.sh
python3 sw/builder/test_builder.py
python3 scripts/lint_rtl.py --check
python3 scripts/xvlog_gate.py --check             # on a host with Vivado
make -C tb/verilator/milan_dp_gptp VERILATOR_JOBS=4  # nightly physical leg; programs the capture map after the walk
```

Expected result / pass criteria: every command exits 0. The dynmap leg
reports 142 checks and 0 failures. `dynmap-mutants` reports 9 checks, 9 PASS.

## Known limitations / out of scope

- **The bench read** of the power-on maps on the AX7101 is the manager's, after flashing.
- **8x8 (not a shipping image).** The ruled identity maps each output's stream channels 1..7 to that port's first loopback clusters, which carry silence while the loopback lane is off. The builder's unconsumed `AEM_ODMAP_INIT_C` (the task #65 rule) maps only the backed Pilot. Restricting the image to backed clusters is a one-term change if the owner prefers it; on the shipping 1x1 TDM8 shape every identity cluster is backed, so nothing changes there.
- **The output clip cannot be reached by a command today:** the format verdict admits only the declared output channel count. It is graded by staging the processor's row in a boot window (`dynmap_probes.vlt`), with a planted control.
- **#70 stage 3** restores map records through the edit face inside the boot window, which this change holds and recomputes. Stage 3 takes the window over for the ports it restores (recorded in the design page). Map records `0x60`-`0x7F` stay unmaterialized.
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

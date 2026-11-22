[R893] NEGATIVE - exact head 2b295a44d136275ccbf060fe4f36c42e573b6460

Round R893-1, internal independent review of kebag-logic/milan-fpga PR #975 (issue #584), cleared context.
Head `2b295a44d136275ccbf060fe4f36c42e573b6460`, tree `d18031d79799e3e765e05b82528cbcc40b0af332`; delta
`dd163e41..2b295a44` (17 commits, 46 files). Lenses applied: Conformance, RTL, Robustness, Tests, Docs.
Open: three MINOR findings (F1-F3) and four RESIDUE items (R1-R4). RTL and Robustness are clean; Conformance,
Tests and Docs are unclean.

## Reconstruction (public state only)

- Issue #584 body (acceptance 1-4), the decisions on the issue: the September proposal and its approval
  (5854191783, 5854199817), the one-cluster fallback (5857155362), the parking (5857540091), the executor's
  TAKEN+DECISION (7077045073) and REVIEW READY (7083459655). The PR body and the manager's review-start comment
  (PR 7083496180).
- Authorities used: Milan v1.2 5.3.3.8 (each Stream Port Input and Output owns at least one AUDIO_CLUSTER),
  5.3.3.9 (no AUDIO_MAP on a Stream Port Input), 5.4.2.26-28 (GET/ADD/REMOVE_AUDIO_MAP[PINGS]); IEEE 1722.1-2021
  7.2.13 (STREAM_PORT: number_of_clusters at +12, number_of_maps at +16), 7.2.16 (AUDIO_CLUSTER: channel_count at
  +84), 6.2.2.8 (entity_model_id); AGENTS.md sections 2, 6 and 7.
- Diff and history `dd163e41..2b295a44`, then the author's public evidence packet
  `review-evidence/584-r1/author-r1/receipts` at `4ee921e6` (route, builder, budget, nvm, gates and decision
  receipts).
- Prior public review findings on PR #975: **none**. The PR has no reviews and no review comments, and its only
  comment is the manager's review-start. No earlier round's finding needs resolving or keeping at this head.

## Findings

### F1 - MINOR - Conformance, Docs - the 2026-11-22 owner decision as implemented: the loopback half is not met and is not stated as a deviation, and the decision record is not public

- Artifacts: issue #584 TAKEN+DECISION (issuecomment-7077045073), "Loopback lane" bullet; PR #975 body,
  "Open risks"; `docs/ENDSTATION_BUILDER.md:739-753` (D8);
  `configs/endstation_ax7101_8x8.yaml:204` (the `render: 1` comment cites only the "FIRST channel" half);
  `sw/builder/endstation_builder.py:185-191` (CLUSTER_ROLES `unrouted` comment).
- Authority/evidence: the owner decision, as given to this review, says to back the model with the loopback lane
  and the first TDM8 channel only. The executor's comment paraphrases it as "the loopback lane and the first TDM
  render channel only". Two departures from the decision's wording remain:
  1. **Loopback half.** Nothing in the 8x8 model is backed by the loopback lane. No input cluster is named for it,
     which is technically sound: its feed is the depacketizer clone and no input mapping steers it. The 8x8 also
     keeps `fabric.loopback_lane: false`, so its 64 output loopback clusters stay unbacked on the shipping build.
  2. **TDM half.** "First TDM8 channel" is implemented as slot 0 of the 8x8's TDM32 bus, named `TDM32 Out 0`,
     reached through the crossbar's 8-key TDM window (key 2). This is a reasonable reading, but it is a reading.

  AGENTS.md section 2 requires that a conflict be published and marked as needing a decision, not settled by
  choosing an interpretation. The executor published its reading in the TAKEN, as "the DECISION", not as a
  deviation. Three gaps follow:
  - no public comment records the owner's decision in its own words;
  - no public manager approval of the 7077045073 DECISION exists (the issue body requires one);
  - D8 cites the owner's decision for the TDM half only, and omits that its loopback half is unmet.
- Impact: a cold reviewer cannot tell from GitHub whether the owner wanted the loopback lane built or used on the
  8x8. If the owner did, the PR merges a model the owner did not ask for while saying it meets the decision.
- Required outcome: the owner's decision is recorded publicly on #584. The manager or owner then either accepts
  the implemented reading or rejects it:
  - if accepted, the loopback half is stated as an accepted deviation in the PR text and in D8, with its reason
    (no input mapping steers the lane; the 8x8 lane stays off) and where it was accepted;
  - if rejected, the model or the lane posture is changed to match.
- Verification: a public owner or manager comment on #584 naming both points, plus the D8 and PR wording that
  cites it.

### F2 - MINOR - Tests, Conformance - the approved design's shipping lane-off 8x8 `sim_nxn` leg is not in the suite, and no committed bench elaborates the datapath at the shipping 8x8 render parameters

- Artifacts: `tb/verilator/milan_dp/Makefile:840-841` (`build-nxn8`, the only 8x8 `sim_nxn` leg that grades input
  ports, built with `-GLOOPBACK_P=1` and no `AUDIO_IF_SLOTS_P`/`AUDIO_IF_MASTER_P`/`AUDIO_IF_RENDER_SLOTS_P`, so its
  render lane is pruned); `tb/verilator/milan_dp/Makefile:437-443` (`maprec8`, lane off, runs only the output-port
  `MAPREC_MP` section); `tb/verilator/milan_dp_render/Makefile` (no narrow-lane leg);
  `tb/verilator/milan_dp/sim_nxn.cpp:10547` (`prove_every_input_port_owns_one_mono_cluster`, graded at the render
  RAM read port only).
- Authority/evidence: three sources require or plan this leg:
  - the approval (5854199817): "The planned tests, including the shipping lane-off 8x8 shape in `sim_nxn`, are
    required";
  - the fallback (5857155362) keeps "the tests, adapted to one cluster per port";
  - the executor's TAKEN plans "the datapath 8x8 legs (loopback lane off, as shipped, and on)".

  The REVIEW READY reports `nxn8`, `maprec8` and `dynmap`. None of them runs the input-port sections at the shipping
  8x8 parameters (loopback lane off; TDM32 master; one render slot). AGENTS.md section 6 (Tests) also asks for real
  integration wiring where practical.

  The D8 claim "ADD of stream 0 channel c ... in slot 0 of the 32-slot frame on `tdm.dout`" is proven only in
  pieces:
  - AECP to render key 2 (`nxn8`, RAM port);
  - the narrow lane on the pins (`tdm_render` unit legs, including `bus1of32` on the real capture master).

  The datapath's one-slot adapter walk (`RLAST_C = 0`) feeding `KL_tdm_render_master` with `BUS_SLOTS_P = 32` runs
  in no committed simulation. `milan_dp_render`'s `AX_SLOTS`/`AX_RENDER` knobs show the leg is practical.

  The behaviour itself checks out. This round's probe `scripts/probe_nxn8_shipping.sh` built `sim_nxn` at
  `-GLOOPBACK_P=0 -GAUDIO_IF_SLOTS_P=32 -GAUDIO_IF_MASTER_P=1 -GAUDIO_IF_RENDER_SLOTS_P=1
  -GAUDIO_IF_CLK_HZ_P=98304000`. It elaborated, and all 572 T66/AMAP/B2/#584 input-surface checks passed
  (`receipts/probe_nxn8_shipping.log`). Its 121 failures are #632/#773 capture-timestamp and one `0x0042` capture
  check: that bench drives no TDM master clock, so the capture grid is dead. They are a limit of the bench, not this
  PR. So this finding is a gap in committed coverage, not a known defect in behaviour.
- Impact: a later change can break the input-port surface on the shipped lane-off shape, or the AECP-to-`tdm.dout`
  slot 0 chain inside `milan_datapath`, and every committed leg stays green.
- Required outcome: the suite gains a committed leg that runs the input-port sections at the shipping 8x8
  datapath parameters (loopback lane off, TDM32 master, render 1). Preferably the leg also decodes slot 0 on
  `tdm.dout` after an input ADD and REMOVE through `milan_datapath`. Otherwise the manager records publicly that
  the approved test requirement is waived, and why.
- Verification: the new leg passes at the head; a planted defect in the one-slot path is caught (for example the
  adapter's first write moved off slot 0, or `.BUS_SLOTS_P` tied to `AUDIO_IF_RENDER_SLOTS_P`); and the leg is
  listed in the sweep.

### F3 - MINOR - Docs - `SPLIT_CONTROL_MEMORY.md` claims a uniform growth that two of its own table rows contradict

- Artifact: `docs/design/SPLIT_CONTROL_MEMORY.md:312` against lines 307-310.
- Evidence: line 312 says "Every image grows by the same 1,336 B of `rom` and 1,744 B of `sram`". The table directly
  above shows otherwise:
  - the platform's 8x8/2if grows `sram` 115,504 -> 117,312 = **+1,808 B**;
  - the size fixture's 8x8/2if grows `rom` 131,536 -> 132,880 = **+1,344 B**.

  The other two rows are +1,336 / +1,744. The ledger strings in `sw/litex/ctrl_memory.py` carry the same table
  figures, so the prose is what is wrong. The same sentence's breakdown ("the 1,280 B of descriptors and names, the
  stage's 656 B and the input ports' map rows") also does not add up to either total as written.
- Impact: an authoritative memory page misstates a measured figure, and a later ledger change would be checked
  against a false invariant.
- Required outcome: the sentence states the measured per-image deltas, or states the uniform part and names the two
  rows that differ and why. The breakdown either adds up or is dropped.
- Verification: arithmetic against lines 307-310 and the `Ledgered` reason strings in `sw/litex/ctrl_memory.py`.

### RESIDUE (wording only; does not block and does not unclean a lens)

- **R1** - `docs/ENDSTATION_BUILDER.md:760-761`: "hand a\n8x8 talker" -> "hand an 8x8 talker".
- **R2** - the `render_ports: first` wording says the channels bind "in order to the first input ports' clusters"
  or "across the input ports". The code gives **all** of them to STREAM_PORT_INPUT 0:
  `max(0, ph_render - render_from)` at `sw/builder/endstation_builder.py:1674`. `test_input_cluster_pools` asserts
  this with `[render or 1] + [1] * 7` for render 2 and 8. Exact fix, in each of
  - `docs/ENDSTATION_BUILDER.md:736-738` and `:1089` (row 16f),
  - `sw/builder/endstation_builder.py:196`, `:1595`, `:1659-1662` and `:4454`,
  - `configs/endstation_ax7101_8x8.yaml:222-224`:

  replace "bind(s) in order to the first input ports' clusters" or "across the input ports" with "binds every
  physical render channel to STREAM_PORT_INPUT 0's clusters, in order".
- **R3** - `tb/verilator/milan_dp/README.md:77`: the `obj_nxn8` row still says "retired input-pool posture". Change it
  to "one mono cluster per input port (#584)".
- **R4** - the generated `build_plan.md` sentence (builder template) "Clusters past that are non-physical ... named
  ... `Virtual`, `Pilot Tone`, `Loopback S<s> ch <c>`" does not list `Unrouted S<p>`. Adding it would change every
  configuration's `build_plan.md`, so it is optional and outside the byte-identity claim.

Examined and not raised:
- `"B2: ..."` check labels in `sim_nxn.cpp` continue an existing section tag; they are runtime strings, not
  comments.
- `S14` in `Ledgered` reason strings is data that follows 15 existing uses.
- The "owner decision 2026-11-22" comment citations carry no forbidden token.

## Lens results (PASS lines carry their artifacts)

```text
[R893] PASS RTL - hdl/ieee1722/aaf/KL_tdm_render_master.sv:137-237,430-443; hdl/milan/milan_datapath.sv:1153-1180,8681-8736 - BUS_SLOTS_P framing: FRAME_C/SW_C come from the bus and FRAME_BITS_C/bank from the lane. The g_bus_slots_guard (power-of-two bus, 1<=SLOTS_P<=BUS_SLOTS_P) and the frame-pos guard are consistent. The g_full_lane arm is the pre-#584 expression, so the 1x1 TDM8 elaborates unchanged. The narrow arm returns zero past SLOTS_P with an in-range index ((24*slot) % FRAME_BITS_C). smp_wr_slot_i is 1 bit at SLOTS_P=1 and matches the adapter's RSLOT_W_C. There is no new CDC crossing (same cdc_pair_fifo, narrower payload). The datapath's slave guard is relaxed for master only and the master arm passes BUS_SLOTS_P=AUDIO_IF_SLOTS_P. Pinned Verilator 5.050 -Wall lint is clean at 1of32 and 8of8 (receipts/lint_render_master_*.log). The datapath elaborates at the shipping 8x8 parameters (receipts/probe_nxn8_shipping.log). The routed 8x8/1if receipt meets #818's floor at all three directives, best AltSpreadLogic_high +0.363/+0.036 ns, and its 17 route inputs equal 2d29d45a's; 2d29d45a..2b295a44 touches only docs, README, oracle.json and measurements.json (git diff --stat).
[R893] PASS Robustness - sw/builder/endstation_builder.py:1641-1690,1833-1844,1052-1067,4448-4470; tb/verilator/milan_dp/sim_nxn.cpp:10547-10620 - zero-cluster ports of either direction are refused by name, whatever the policy (validate_cluster_minimum after layout). render_ports is refused when its value is unknown or the policy is not role-pools. A narrower slave lane is refused (test patches tdm_bus_master False). The 8x8's 64-key input surface narrows to 8 keys with RPHYS {0x42,0,...}. Out-of-range cluster offsets and an 8-row page past the one cluster are refused BAD_ARGUMENTS without touching other mappings. REMOVE of a non-empty list succeeds and empties the page. Mappings on unrouted ports drive no render key, and the power-on maps are restored. The feature-disabled shipping shape (loopback lane off, render lane built) was probed: 572/572 input-surface checks pass (receipts/probe_nxn8_shipping.log).
```

| Lens | Result | Covering evidence at this head |
|---|---|---|
| Conformance | UNCLEAN (F1, F2) | All five configs: every STREAM_PORT_INPUT owns >= 1 cluster, every `maps_in` = 0, and outputs own >= 1 (`receipts/all_config_pools_script.log`, `overlay_ports.log`). AECP `Inputs.*` reads number_of_clusters, number_of_maps and channel_count over the wire and passes at all 5 configs (`aecp_inputs_all_configs.log`). It fails on the base 8x8 model with its words, ports 0-7 (`probe_base_8x8_model_inputs.log`). Acceptance 1, 3 and 4 are met: the named refusal plus its test, a 20,800 B image with id 0x001BC5F6CB4A37D1 -> 0x001BC5CFD464421E, and the 1x1 TDM8 and three Arty outputs byte-identical at both placements (`artifacts_compare.log`). Acceptance 2 is met in text. F1: the decision record. F2: the approved test requirement. |
| RTL | CLEAN | see the PASS line |
| Robustness | CLEAN | see the PASS line |
| Tests | UNCLEAN (F2) | The builder's #584 tests pass (`builder_584_tests.log`), including the guard-removal mutants. Both AECP input plants are caught (`aecp_input_plants.log`). `tdm_render` passes all legs plus the slave bench (`tdm_render_all.log`), 5 of 5 render-master plants caught (`tdm_render_master_mutants.log`). `nxn8` PASS 4217/0 (`nxn8_exec.log`); `maprec8` PASS (`maprec8.log`). The `render_ports: every` default is justified: forcing in-order binding makes `check_nvm_format_32x32.py` report t32_names 907 -> 690 and a layout-3 mismatch (`probe_render_ports_default_first.log`). |
| Docs | UNCLEAN (F1, F3) | Read: D1, D2, D8, D10 and key-map row 16f in `docs/ENDSTATION_BUILDER.md`, `PP_DESCRIPTOR_OWNERSHIP.md` (F5, #122 disposition), `SUBMODULES.md`, `CHANNEL_MAP_64.md`, the SAVED_STATE_* pages, `SPLIT_CONTROL_MEMORY.md`, the 649 finding and `CHANGELOG.md`. The figure checkers pass: `check_nvm_format_32x32.py`, `check_nvm_record_space.py`, `check_nvm_capture.py`, `check_entity_shape.py` (176/0). F3 is the memory-page sentence; R1-R4 are wording. |

## Reviewer-owned completion ledger

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | issue #584 decisions (5854199817, 5857155362, 7077045073); builder pools at 5 configs; AEM overlay; AECP `Inputs.*` at 5 configs plus the base-model probe; five-config artifact comparison at both placements | R893-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| RTL | CLEAN | `KL_tdm_render_master.sv`, `milan_datapath.sv` guards and master/slave arms, lint 1of32/8of8, shipping-parameter elaboration, route receipts | R893-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Robustness | CLEAN | builder refusals (minimum, render_ports, slave lane); T66 boundary/refusal/restore; lane-off shipping-shape probe | R893-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Tests | UNCLEAN | `test_declarations.py` #584 tests; `test_aecp.cpp` Inputs plus `aecp_input_mutants.py`; `tdm_render` legs plus `master_mutants.py`; `sim_nxn` nxn8/maprec8; Makefile leg inventory | R893-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |
| Docs | UNCLEAN | D1/D2/D8/D10/16f, `PP_DESCRIPTOR_OWNERSHIP`, `SUBMODULES`, `CHANNEL_MAP_64`, the saved-state, memory and changelog pages, the checkers | R893-1 | 2b295a44d136275ccbf060fe4f36c42e573b6460 |

## Commands run here (foreground, pinned Verilator 5.050 verified by `--version`)

| Command | Result |
|---|---|
| `test_declarations.test_stream_port_cluster_minimum()` and `test_input_cluster_pools()` | rc 0 |
| `aecp_arms.py --inputs` | 5/5 configs, 2 tests each, PASS |
| `scripts/aecp_input_plants.py` (the repository campaign, filtered to the #584 rows) | 2/2 caught |
| base-model probe: head tree with the base builder and 8x8 config | `Inputs.EveryStreamPortInputOwnsAMonoCluster` FAIL, "STREAM_PORT_INPUT p owns an AUDIO_CLUSTER (Milan v1.2 5.3.3.8)" for p = 0..7 |
| `make -C tb/verilator/tdm_render all`, `master_mutants.py` | PASS; 5/5 caught |
| `make build-nxn8 exec-nxn8`, `make maprec8` | PASS |
| `scripts/probe_nxn8_shipping.sh` | input surface 572/0; 121 capture-timestamp failures from the bench's limit (F2) |
| `scripts/artifacts_compare.sh` (base and head exports, 5 configs x 2 placements) | 8 identical, only the 8x8 differs (6 files each) |
| `check_nvm_capture.py`, `check_nvm_format_32x32.py`, `check_nvm_record_space.py`, `check_entity_shape.py` | PASS |
| `test_ctrl_memory.py` | 217 ok; 12 failures, all SoC-build arms that need `pythondata_cpu_vexiiriscv`, absent here (an environment limit, not a PR finding); every ledger arm passes, including the 57.0/59.0/61.5/64.0 points |
| render_ports default probe (in-order binding forced) | the layout-3 bound moves, as the author's receipt says |

After the probes the clone was cleaned. HEAD and tree are exact, the index equals the HEAD tree (same sha256 over
mode/blob/path), all six gitlinks match, and every submodule worktree is clean (`receipts/restore_verification.txt`).

## Real limits

- No manager source bank ran at this head, and none is claimed or inferred. Source-head execution evidence is the
  author's published receipts plus the focused runs listed above.
- Not reproduced here:
  - the builder suite's 113 gates;
  - the firmware bank shards;
  - the 65-suite sweep;
  - the `fw_service_budget` run and its oracle regeneration (no product firmware link in this environment). The
    diff confirms only that oracle entry 1, the 8x8 row, changed (274 leaves) and the 1x1 rows did not;
  - the all-fabric capture re-measure (14.533 ms; only its checker was re-run);
  - the split saved-state measurement;
  - the CPU-budget flip check;
  - the control-image links;
  - the Vivado routes. Route and timing figures are taken from the author's receipts.
- The `SoC build` arms of `test_ctrl_memory.py` could not run here (missing CPU data package).
- Physical calibration NOT RUN. No hardware was touched, and skipped field contexts are not hardware proof.
- Hosted checks at this head were still queued or in progress when inspected (`verilator-lint`, `wire-accountability`,
  `full-ci-gate` and `elaborate-gates-2..4` had succeeded; Physical gPTP was skipped). The manager owns hosted and
  local-replica acceptance.
- The all-fabric `milan_nvm` listing over its 500 ms duty budget (901.6/903.6 ms here, 860/862 ms at the base) is a
  pre-existing finding filed separately, not this PR's.

## Pending manager duties

- F1: publish the owner's 2026-11-22 decision on #584, and accept or reject the implemented reading of its
  loopback and TDM halves.
- F2: require the shipping-parameter 8x8 leg, or record a public waiver of the approved test requirement.
- F3 and R1-R4: route to the executor (R1-R4 to the residue checklist).
- Validate the current-dev merge candidate (source base `dd163e41`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`)
  with the builder and native banks, and link the receipts.
- Hosted and local-replica acceptance at the exact head.
- Re-review at the corrected head: every lens whose artifacts change must be covered again.

R893-1 FINISHED

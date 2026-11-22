# [A818] round 1 handoff: #584, 8x8/1if STREAM_PORT_INPUT clusters (lab readiness)

Status: REVIEW READY at `2b295a44d136275ccbf060fe4f36c42e573b6460` (started 2026-11-22 10:04 CET; updated 19:20).
17 local commits on `pf-584-1`, not pushed. Every round deliverable is met and measured below. All 65 sweep suites
pass: 64 at `2d29d45a`, plus `fw_service_budget` at `2b295a44` after its 8x8 trace row was regenerated through the
suite's own procedure (the 8x8 product firmware's populated `all` run, then `gen_oracle.convert`). That regeneration
surfaced an existing, untracked budget finding that this change extends; it is open question 2.

- Base: `dd163e41438acb86e0c4d4e76df90f3f91ace1c0` (PR #960 reviewed head), branch `pf-584-1`, PR base `dev-soft-core`.
- Comments on #584: TAKEN with the DECISION in it, issuecomment-7077045073 (`receipts/public/taken.md`); REVIEW
  READY, issuecomment-7083459655 (`receipts/public/review-ready.md`). No other comment was posted, edited or deleted. The round asked for a DECISION comment first and allowed only TAKEN and REVIEW READY/STOP
  comments, so the DECISION is a section of the TAKEN comment.

## Decision (posted with TAKEN)

- 8x8/1if: STREAM_PORT_INPUT 0 owns one cluster, `TDM32 Out 0`, the TDM bus's slot 0 (the first key of the crossbar's
  TDM render lane, key 2), built by `KL_tdm_render_master` framing the bus's 32 slots and storing slot 0 alone;
  ports 1-7 own one `Unrouted S<p>` each (no projection). 1x1/1if TDM8 and the Arty configs are unchanged.
- The loopback lane backs no input cluster: no input mapping steers it (its feed is the depacketizer clone); it stays
  the backing of the output ports' loopback clusters where built (1x1 yes, 8x8 no).
- Deviation from the posted DECISION's wording, for review: the in-order binding of the render channel to port 0 is
  the config's declared `cluster_mapping.render_ports: first` (default `every`, D8's per-port copies). Binding in order
  for every role-pools config would have changed the 32x32 TDM8 bound shape that sizes saved-state layout 3 (names
  907 -> 690), and with it the 1x1's own `nvm_split.json` (`id_space`), so it is opt-in. The 8x8's emitted model is
  exactly the one the DECISION states.

## Changes (file:line, reason)

| Where | Reason |
|---|---|
| `sw/builder/endstation_builder.py:192` `CLUSTER_ROLES` + `unrouted` | the one cluster of an input port no render channel reaches (Milan 5.3.3.8) |
| `sw/builder/endstation_builder.py:197` `RENDER_PORTS`, `:4455` parse, `:3693` model shape | which input ports own the physical render channels; hashed only when declared (#495) |
| `sw/builder/endstation_builder.py:1641-1690` `_role_pool` | `render_from` binding under `first`; unrouted fallback for inputs; output zero refused by name |
| `sw/builder/endstation_builder.py:1833` `validate_cluster_minimum` | `STREAM_PORT_CLUSTER_MINIMUM` over every resolved layout, both directions |
| `sw/builder/endstation_builder.py:1931` `_name_unrouted` | `Unrouted S<p>` (D10) |
| `sw/builder/endstation_builder.py:1055` `validate_render_lane` | a master render lane may be narrower than its bus; a slave lane stays full-width |
| `hdl/ieee1722/aaf/KL_tdm_render_master.sv:147,234,436-443` | `BUS_SLOTS_P`: the bus frame's slots; storage for `SLOTS_P` only; zero past the lane; a full-width lane elaborates as before |
| `hdl/milan/milan_datapath.sv:1177,8736` | the narrow-lane refusal kept for the slave arm only; the master instance gets `BUS_SLOTS_P = AUDIO_IF_SLOTS_P` |
| `configs/endstation_ax7101_8x8.yaml:204,222` | `render: 1`, `render_ports: first`; the L1 model-lint waiver removed; stale "routes nothing" comments corrected |
| `configs/generated/endstation_ax7101_8x8/gen/adp_shape_defaults.svh` | regenerated: 8 input keys, RPHYS `{0x42, 0 x7}`, names 107 -> 115 |
| `sw/litex/ctrl_memory.py:263` and the three 8x8 entries; `ctrl_memory_ledger.py`; `test_ctrl_memory.py` | the 8x8 images at their re-measured tiles, the stage 14,250 B; the size fixture's 8x8/1if image a new ledgered point (57.0) |
| `tb/verilator/ctrl_service_budget/build.py:318`, `selftest.py` | the harness plans its 8x8/1if image at that point |
| `sw/firmware/ctrl/test/test_aecp.cpp:328,348`, `aecp_arms.py:47-55` | `Inputs.*` at every tracked config: the entity-model check over AECP, REMOVE of a non-empty list |
| `sw/builder/test_declarations.py:657,710`; `test_builder.py` gate 6 | the named refusal, its guard mutants, the derived pools |
| `tb/verilator/tdm_render/` (Makefile, `sim_master.cpp`, `sim_master_bus.cpp`, `master_bus_wrap.sv`, `master_mutants.py`) | the narrow lane, including the 8x8's slot 0 of TDM32 on the real capture master's pins |
| `tb/verilator/milan_dp/sim_nxn.cpp:10547` and the AMAP, #67 and B2 sections | the all-fabric 8x8 leg graded for one cluster per port |
| docs: `ENDSTATION_BUILDER.md` (index, D1, D2, D8, D10, sections 1 and 4), `PP_DESCRIPTOR_OWNERSHIP.md`, `SUBMODULES.md`, `SPLIT_CONTROL_MEMORY.md`, `SAVED_STATE_FORMAT_32X32.md` (regenerated), `SAVED_STATE_FASTCONNECT.md` 4.2, `SAVED_STATE_SNAPSHOT_OWNERSHIP.md` section 18, `CHANNEL_MAP_64.md`, `nvm_backend/README.md`, `CHANGELOG.md`, `DOCUMENTATION_AUDIT.md` (regenerated) | the model, its refusal and its costs |
| `tb/verilator/nvm_capture_cpu/measurements.json`, its README, `ctrl_nvm/README.md`, `nvm_split_target/README.md` | the four 8x8 arms re-measured at the 172-record census; maxima recomputed by the harness's grader |
| `tb/verilator/fw_service_budget/oracle.json` | the 8x8 `all` row regenerated by `gen_oracle.convert` from a populated run at `b1d164ef`; the two 1x1 rows kept and re-checked against their unchanged image |

## New checks (planted mutant -> failing words)

| Check | Planted | Failing words |
|---|---|---|
| `Inputs.EveryStreamPortInputOwnsAMonoCluster` | the base tree's 8x8 (zero clusters) | "STREAM_PORT_INPUT 0 owns an AUDIO_CLUSTER (Milan v1.2 5.3.3.8)" (x8) |
| `Inputs.EveryStreamPortInputRemovesANonEmptyList` | the same | "status for command 44", "STREAM_PORT_INPUT 0 holds a mapping to remove" |
| `test_stream_port_cluster_minimum` | `validate_cluster_minimum` stubbed, per direction | the controls see "accepted zero-cluster input/output port" |
| `tdm_render` `lane1of32` | the narrow lane unmasked | "frame 0 slot 1 (past the lane: zero)" |
| `tdm_render` `lane2of8` | the lane one slot wide | "frame 0 slot 2 (past the lane: zero)" |
| `tdm_render` `lane8of8` | the bank slot off by one | "frame 0 slot 0 (rendered: sample, 24-in-32 MSB first)" |
| `tdm_render` `bus1of32` | the narrow lane unmasked, real capture master | "slots 1..31 past the lane carry zero" |
| `tdm_render` `lane1of32` | the narrow lane takes the full-lane branch | "frame 0 slot 2 (past the lane: zero)" |
| `milan_dp` `nxn8` (the rewritten 8x8 sections) | the base tree's 8x8 model (zero input clusters) under the head's bench | 13 checks fail, e.g. "render key 2 = SPI 0's cluster = {en, avb 1.1} (#584)", "status SUCCESS(0): SPI 0 owns a cluster (#584)"; the run then hit its unit's memory cap | 
| AECP campaign rows | `input-port-served-headless`, `remove-keeps-its-rows` | "STREAM_PORT_INPUT 0 owns an AUDIO_CLUSTER (Milan v1.2 5.3.3.8)"; "STREAM_PORT_INPUT 0: the removed list leaves the page empty" |
| Builder plants (in place) | `render_ports` ignored; unrouted fallback dropped; minimum check stubbed; unrouted cluster projected; narrow slave lane accepted | "is not the unrouted port render_ports first leaves it"; "STREAM_PORT_CLUSTER_MINIMUM"; "accepted zero-cluster input port"; the projection list; "slave TDM render lane" |

## Gate table

| Gate | Command | Head | Result | Receipt |
|---|---|---|---|---|
| Five-config artifacts | `artifacts.py` + `artcmp.py` (builder `_derive_artifacts`, the AEM image set, the shape include, the firmware's generated AEM header), both placements | `dd163e41` vs `4c446df2` | 1x1/1if TDM8 and the three Arty configs IDENTICAL at both placements (15/16 files each); the 8x8 differs, model `0x001BC5F6CB4A37D1` -> `0x001BC5CFD464421E` | `builder/artifacts-base-vs-head.txt`, `artifacts-receipt.json` |
| Routed commit vs head, builder outputs | same | `92fd1635` vs `4c446df2` | all ten IDENTICAL | `builder/artifacts-routed-vs-head.txt` |
| Descriptor statistics | `desc_stats.py` | same | 8x8 image 19,520 -> 20,800 B; descriptors 124 -> 132; largest 452 B (line 576); clusters 72 -> 80 | `builder/descriptor-stats.txt` |
| #584 builder tests | `test_declarations` two tests | head | PASS | `builder/declarations-584.txt` |
| #584 builder plants | `builder_mutants.py` (in place, scratch clone) | `6f947731` | 5 of 5 caught | `builder/builder-mutants.txt` |
| Builder suite, leg 1 (112 gates) | `ci_builder_legs.py run 1 -- test_builder.py --require-elaboration --require-rv32` | `2d29d45a` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11's bench-local calibration report) | `gates/builder-leg1.txt`, `builder-leg-1.json` |
| Builder suite, leg 0 (bare-metal profile) | same, leg 0 | `2d29d45a` | ALL GATES PASS EXCEPT 1 NOT RUN (gate 1b's make arm) | `gates/builder-leg0.txt`, `builder-leg-0.json` |
| Builder legs' union | `ci_builder_legs.py union --workflow elaborate` | `2d29d45a` | 113 gates exactly once; requirements judged on the union; rc 0 | `gates/builder-legs-union.txt` |
| AECP input tests | `aecp_arms.py --inputs` (every tracked config) | head / base (planted) | PASS at all five; the base 8x8 fails both with their words | `firmware/aecp-inputs-*.log` |
| AECP campaign, the two new plants | `aecp_input_campaign.py` (full table's drift control first) | `b1d164ef` | 2 of 2 caught | `firmware/aecp-input-campaign.txt` |
| Firmware bank | `test_ctrl_firmware.py --require-rv32 --self-test --shard k/4` x4 | `3a6563ae` (later commits touch no firmware source or test) | 4 of 4 shards PASS; every plant caught | `gates/firmware-bank-shard*.txt` |
| Control memory | `test_ctrl_memory.py` | head | PASS (0 failures; the planted ledgers caught) | - |
| Platform images vs ledger | `plat_ledger.py` | `4c446df2` | PASS; 8x8/1if 59.0, 8x8/2if 64.0, 1x1 45/46 | `firmware/ledgerF.log` |
| Size-fixture images, every variant/arm/plant | `variant_sizes.py` | `47be7ceb` (image inputs equal to the head's but the model id's bytes) / base | worst 57.0 / 61.5 (base 56.0 / 60.5) | `firmware/variants-*.log` |
| Render lane suite | `make -C tb/verilator/tdm_render` + `master-mutants` | head | 4 legs PASS + the slave bench; 5 of 5 plants caught | `rtl/tdm_render-*.txt` |
| Datapath lint at 8x8/1if | `verilator --lint-only` (TDM32 master, render 1 and 0, split) | head | 0 errors; warning set unchanged | `rtl/lint-8x8-1if.txt` |
| Quick self-tests | `check_entity_shape.py --self-test`, `check_feature_status.py --self-test`, `check_sweep_shape.py --self-test`, `baremetal_uart_smoke.py --self-test`, `soc_sweep.py --selftest`, `check_wire_accountability.py` | `b1d164ef` | all rc 0 | `gates/quick-selftests-b1d164ef.txt` |
| Yosys portability | `syn/yosys/run.sh --top KL_tdm_render_master --mode full`; `--top milan_datapath --mode elaborate` | `b1d164ef` | PASS (4,195 cells); PASS (80,395 cells); tied-input and tap-purity PASS | `rtl/yosys-*.txt` |
| All-fabric 8x8 leg | `make -C tb/verilator/milan_dp build-nxn8` + run | `92fd1635` + bench | PASS (0 failures) | `rtl/nxn8-summary.txt` |
| maprec8, dynmap | `make maprec8`, `dynmap` | `4c446df2` | PASS (219, 711 checks) | - |
| 8x8/1if route, three directives | `gchain.sh` x3, `signoff.py` | `92fd1635` (inputs = head: 17 of 17 equal) | #818 floor met at every corner on all three; best AltSpreadLogic_high +0.363/+0.036 ns | `route/TIMING.md`, `route/*` |
| Split boot simulation of the new 8x8 image | the route chain's `boot.sh` | `92fd1635` | completed; `aem-image: PASS (AEM=loaded)` | (route chain) |
| Flip check | `flip_grade.py --check --point 1x1/1if`, `--point 8x8/1if`; `load_grade.py --check` | head | PASS: 1x1/1if load 0.511 (0.70), last 127.31 ms (140), ACMP 29.06 ms (30), txL 47.88 ms (49); 8x8/1if load 0.744 (0.75) | `budget/*` |
| CPU budget harness self-test | `run.py --self-test` | `d9b8dda9` | 0 failures | `budget/run-selftest.txt` |
| All-fabric capture (24.5 ms bar) | `nvm_capture_cpu/run.py` x4 8x8 arms, 16 captures; `check_nvm_capture.py` | head | 8x8 max 14.533 ms at 50 MHz (was 13.861), 10.944 ms at 100 MHz; check PASS; 3 mutations refused | `nvm/*` |
| Split saved state (T_svc per step) | `nvm_split_target/run.py --point 8x8` (two interfaces, the harness's point) | `72c49fd7` | every case passes, controls caught; longest step 1.039 ms (T_svc 20 ms); capture 172 records, CPU 28.888 ms, elapsed 66.785 ms (recorded) | `nvm/split-8x8-*` |
| Docs workflow, 103 commands | `quick.sh docswf.tsv` | `b1d164ef`, `2b295a44` | 99 pass at both; the 4 hosted-environment rows (act install dir, `GITHUB_EVENT_PATH` x3) fail as at the base; tree clean after | `gates/docswf-b1d164ef.txt`, `gates/docswf-2b295a44.txt` |
| Full sweep, 4 shards | `native-shards.py` | `2d29d45a` | shards 0, 1, 3: 15/15, 17/17, 16/16 PASS; shard 2: 16/17, `fw_service_budget` failing on its pinned 8x8 trace ("oracle image changed") | `gates/sweep-shard*.txt`, `gates/sweep-shard2-fw_service_budget.log` |
| 8x8 service-budget trace | `fw_service_budget/run.py --shape endstation_ax7101_8x8 --build-only`, then `--reuse-build --populated --record-budget-findings`; `gen_oracle.convert` | `b1d164ef` | RESULT: PASS (checks 1, failures 0); row regenerated; 1x1 rows unchanged; the same two budget findings as at the base (open question 2) | `budget/service-8x8-all-oracle-row.md` |
| `fw_service_budget` suite | `make -C tb/verilator/fw_service_budget` (`run.py --self-test`), clean clone | `2b295a44` | PASS: oracle 55 checks 0 failures, flash 19 checks 0 failures, controls caught. With the 64 at `2d29d45a`: 65 of 65 sweep suites. The commits after `2d29d45a` change only the capture receipt (read by `check_nvm_capture.py`, in the docs workflow), docs and READMEs, and this oracle (read by this suite alone) | `gates/fw_service_budget-2b295a44.txt` |

## Open questions

1. The DECISION's per-direction binding is the declared `render_ports: first` (see above).
2. An existing, untracked service-budget finding that this change extends. On the all-fabric 8x8 product firmware,
   the `milan_nvm` console listing (commands 2 and 5 of the `all` plan, the populated store) already took 860.4 and
   862.4 ms at the base, against the harness's 500 ms per-command duty budget. The suite records both as
   `over-budget duty: milan_nvm`, and its README says recording "never approves a missed budget". At the head they
   take 901.6 and 903.6 ms (+4.8%), because the listing walks 172 records instead of 164. The command keeps serving
   inside its handler (period bound margin +131 ms, heartbeat gap 345.3 ms of 500, every sampled command backed).
   No owner bound covers it, and no open issue tracks it. The round allows no new issue or comment, so filing one is
   the manager's call. The 1x1 rows have no finding (222 ms).

REVIEW READY 2b295a44d136275ccbf060fe4f36c42e573b6460

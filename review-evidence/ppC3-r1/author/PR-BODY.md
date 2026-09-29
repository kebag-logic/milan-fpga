[A446]

Closes #40
Closes #41
Relates to #85

Lane C3 of the PP program (ADP), assignment on #40 comment 5888002660. Branch `c3-adp-coverage`, five commits on `main` `c951a9ff`, head `9185c49`.

| Commit | Item |
|---|---|
| `cfb7bbb` | 1. #40: the ADPDU carries the SET_CONFIGURATION overlay, sampled at build; unit P11, top section AD; the ADP mutation campaign |
| `ee69db2` | 2. #41: the boot gate over the full T-ADP-DELAY span; unit P12, top AD0 and S3 |
| `4a895f2` | 3. #85: the MTXW walk of F04.2 and F04.3 from Milan Tables 5.51 and 5.54 |
| `e8ec039` | the campaign's patch files keep their blank context lines out of whitespace checks (as `tb/srp_top`'s do) |
| `9185c49` | the consumer's C++ and Python idiom rules for the new test code |

## 1. #40: ADPDU invariance across SET_CONFIGURATION (REQ-ADP-005)

**Clauses.** Milan v1.2 §5.6.2 (note: the ADPDU fields are independent of the currently set Configuration); IEEE 1722.1-2021 §6.2.2.18 (current_configuration_index is the currently set CONFIGURATION descriptor index); §7.4.8.2 (GET_CONFIGURATION and ENTITY.current_configuration are the same value).

**Acceptance 3, the preferred way, with no top-level port change.** `protocol_processor_top` now feeds the ADP engine the entity's current configuration: the dynamic overlay (`aecp_cur_config_o`) once it has been written, and the integrator's `current_cfg_i` (the image default) before that. That is the value GET_CONFIGURATION and READ_DESCRIPTOR(ENTITY) already serve. The overlay's valid flag comes from a new output of `KL_aecp_engine`, `dyn_cur_config_v_o`: one flop on the store's own write bus that is set by an accepted write of the configuration row, exactly the store's flag. The store's port list is not touched, because the reference platform instantiates it by name. No loopback is needed; `docs/guides/integrator.md` §6 and `02_interfaces.md` §2 rule 4 say what `current_cfg_i` now means.

**RTL defect found by the new unit arm, fixed.** `KL_adp_engine` read `current_cfg_i` live while it wrote wire bytes 64 and 65. Once the index is dynamic, a SET_CONFIGURATION that lands between the two bytes tears the field. The index is now sampled at PDU build, like the grandmaster and domain (`bld_cfg_r`, builder `B_SAMPLE`). Failing arm: unit P11c against the previous engine puts `0104` on the wire, the high byte of `0102` and the low byte of `0304`.

**Tests.**
- Acceptance 2, `tb/adp_engine` P11: `current_cfg_i` moves between two adverts. Only wire bytes 64..65 move, besides available_index (50..53), which moves by its own +1. P11c moves the index right after byte 64 is written, and P11d checks that ENTITY_DEPARTING carries the current index.
- Acceptance 1, `tb/pp_top` section AD. It runs on a fresh processor of its own, so the main run's clock is untouched. The image declares two configurations with default 1, and `current_cfg_i` says 1.
  - AD1: the first ENTITY_AVAILABLE carries 1.
  - AD1b: SET_CLOCK_SOURCE writes another row of the store, and the index stays 1.
  - AD2: after a SUCCESS SET_CONFIGURATION(0), GET, the ENTITY descriptor and the next ENTITY_AVAILABLE all say 0. That advert equals the previous one in every wire byte except available_index and current_configuration_index.
  - AD3: the same back to 1.
  - AD4: `current_cfg_i` moving after a SET does not reach the wire.
  - Against the shipped RTL, AD2 and AD4 fail.
- Acceptance 4, mutation record (`tb/adp_engine/README.md`, all killed by the named check):

| Arm | Failing checks |
|---|---|
| `cfg-read-live` (unit) | P11c |
| `cfg-dependent-field` (unit: identify_control_index made configuration-dependent) | 14, P11b first |
| `cfg-dependent-field-top` | 5, AD2 first |
| `cfg-frozen-at-top` (the index frozen: the pre-lane wiring) | 3, AD2 |
| `cfg-overlay-only` (no image-default fallback) | 2, AD1 |
| `cfg-nonzero-for-valid` | 2, AD2 |
| `cfg-valid-not-sticky` | 3, AD2 |
| `cfg-valid-any-selector` | 1, AD1b |

## 2. #41: pre-enable ADP quiescence over the full T-ADP-DELAY span (REQ-ADP-006)

**Clauses.** Milan v1.2 §5.6.1 (ADP starts only when the entity is ready to accept commands); §5.6.3.5.3 (T-ADP-DELAY is 0..4 s after LINK_UP). No RTL change: the gate is correct.

- Acceptance 1, `tb/adp_engine` P12 (runs right after P0). With `entity_enable_i` low, the link rises and stays up for 4100 ms of modeled time, bounces for 20 ms, and stays up for another 4100 ms. The timer service is modeled end to end in that window, so a leaking gate would reach the wire. Graded: no draw request, no timer arm or cancel, no committed frame, `dbg_adv_state` DOWN in every clock, and the PRNG seeded (the stimulus is live).
- Acceptance 2, `tb/pp_top`.
  - AD0: link up for 4200 ms, a bounce, then 4200 ms more with enable low and nothing flushing the queue. `q_adp` stays empty, the advertise SM reads DOWN at every 100 ms sample, and the flags word reads {seeded, link, !enable}.
  - S3 checks `q_adp` before its flush. This is a queue read only, so no later clock moves.
- Acceptance 3, mutation record in `tb/adp_engine/README.md`, for `gate-enable-dropped` (entity_enable_i removed from the DOWN-exit condition):
  - Unit: 30 failures, all four P12 checks among them.
  - Top: 3 failures, AD0 first.
  - Under this mutant the full default pp_top run fails only AD (3 of 7,766). S0's 20 ms window and S3 stay green, which confirms the issue's analysis.

## 3. #85: the F04.2 advertise SM walked MTXW (GAP-16), acceptance 1-3

No RTL change: the walk found no defect.

**Acceptance 1, F04.2.** `tb/adp_engine` P13 walks every cell from an independent transcription of Milan v1.2 Table 5.51 and the §5.6.3.5 clauses.
- The DISCOVER event is split per §5.6.3.1: entity_id 0, own entity_id, or anyone else's.
- An extra column covers the §5.6.1 boot gate, where the hardware holds DOWN.
- DELAY is walked in both hardware phases: the draw in flight, and the timer armed.
- 45 cells, ending in `CHECK(adv_cells == 45)`: 12 transitions, 20 ignored and proven inert, 6 `x` cells reachable as stray expiries (injected and proven inert), 7 `x` cells impossible by construction (precondition checked).
- Each cell grades:
  - the state, the draw requests (kind 2, 0..4000 ms), and every timer arm and cancel with its deadline;
  - the committed frame byte-exact, and available_index;
  - GPTP_GM_CHANGED ticks, discovery events, and RX-slot frees.

**Acceptance 1 and 3, F04.3.** The same walk covers the talker-discovery SM from Milan Table 5.54 and the §5.6.4.5 guards, each guard its own row. It adds the unbound column of §5.6.4.1 and bind/unbind.
- 33 cells, rotated over all eight sinks, ending in `CHECK(disc_cells == 33)`.
- TK_NOT_DISCOVERED is entered with a stale saved record (index and interface) that §5.6.4.5.1 must not compare against.
- Each of F04.3's eight arcs is a walked cell that passed, checked as 8 of 8.

**Acceptance 2.**
- DOWN x DISCOVER, DOWN x GM_CHANGE and DOWN x SHUTDOWN are proven inert: no draw, no frame, no timer operation, only the GM counter tick.
- DELAY x LINK_DOWN stops the timer with no ENTITY_DEPARTING.
- DELAY x SHUTDOWN sends ENTITY_DEPARTING byte-exact and resets available_index.
- The two DELAY rows are checked in both DELAY phases.

**Acceptance 3, mutation record** (17 arms, all killed by the named cell):
- The issue's two named mutations:
  - `walk-down-answers-discover`: 16 failures, in both DISCOVER rows x DOWN and x NOT STARTED.
  - `walk-delay-ignores-link-down`: 4 failures, LINK_DOWN x both DELAY phases.
- F04.2: `walk-down-answers-gm-change`, `walk-down-shutdown-departs`, `walk-delay-answers-discover`, `walk-delay-shutdown-silent`, `walk-stale-draw-arms`, `walk-departing-keeps-index`, `walk-foreign-discover-answered`, `walk-link-down-keeps-timer`.
- F04.3: `disc-fresh-checks-gm`, `disc-not-discovered-checks-index`, `disc-not-discovered-checks-interface`, `disc-restart-not-rediscovered`, `disc-departing-ignores-interface`, `disc-stray-noadp-departs`, `disc-unbind-keeps-timer`.

The campaign also exposed a weakness in the walk itself, which is fixed. A DISCOVER needs two clocks to classify, so in the draw phase it used to act on the delivery edge, and `walk-delay-answers-discover` stayed green in that column. The column now enters one clock earlier, so every event acts strictly inside the draw.

**Acceptance 4 stays open**: the available_index interop against a live controller needs a bench lane. The README's interop limit is restated as open (issue #85 item 4), with the reason the walk cannot close it: it grades the documented rule in every cell.

## 4. Parent-visible list

1. **No port or parameter change** of `protocol_processor_top`, or of any processor module the parent instantiates by name: `KL_aecp_dyn_state` (nvm_cosim), `KL_acmp_nvm_shadow`, `KL_pp_nvm_port` and `KL_pp_nvm_mgr_arb`. `KL_aecp_engine` gains one output, and only the processor top instantiates it.
2. **`current_cfg_i` changes meaning.** It is now the image-default fallback. After a SUCCESS SET_CONFIGURATION, the ADPDU's current_configuration_index follows `aecp_cur_config_o`, which is the value GET_CONFIGURATION answers.
   - The parent drives `current_cfg_i` from the ADP_IDX0 CSR, and its image declares one configuration. The only legal SET is therefore 0, and the wire is unchanged while ADP_IDX0 is 0.
   - milan_dp's printed [GAP] on the configuration face (graded for crossing, not for carrying, with one configuration) remains true.
   - The comment at `KL_pp_shadow`'s `current_cfg_i` ("ADPDU current_configuration_index") can say "until a SET_CONFIGURATION" at pin adoption.
3. **Test-evidence ratchet.** `tb/adp_engine` is now armed, through a new processor CI step (`make -C tb/adp_engine mutants`). `scripts/measure_test_evidence.py --check` passes 74 <= 77 and reports that the ratchet can be lowered to 74. No DUT-reader disposition is needed (0 unexplained readers): the driver applies patch files and reads logs only.
4. **New entry points:** `make -C tb/adp_engine mutants` and `make -C tb/pp_top adp-config`.
5. **Optional matrix citations.** The parent's `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 5.6.3/5.6.4 row can cite the MTXW walk, and a 5.6.1/5.6.2 citation can use P12/AD0 and P11/AD.

All sixteen consumer commands are rc 0 with no parent edit (table below).

## Validation

Verilator 5.050 (the CI pin).

Processor, at `9185c49`. The campaign marked * ran at `e8ec039`; the one commit after it touches only `tb/adp_engine`.

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,016,684 checks, 0 failing (adp_engine 1,367, was 533; pp_top 7,786, was 7,751). Base `c951a9ff`: 1,015,815 |
| `./scripts/lint_hdl.sh` | 0 | 40 modules |
| `make check` | 0 | lint, WaveDrom, links, both matrices, parameters, stale |
| `python3 scripts/gen_matrix.py --check` | 0 | |
| `./syn/yosys/run.sh` | 0 | 35 tops and the Xilinx memory-map check |
| `make -C tb/adp_engine mutants` (new, in CI) | 0 | 2 controls pass, 27 arms killed by their named checks |
| `make -C tb/srp_top mutants` | 0 | 7 controls pass, 56 arms killed, assertion coverage 49/49 |
| `make -C tb/nvm_port figures` | 0 | with PR #13's objects fetched read-only |
| `tb/pp_top/gsi_mutants.py` * | 0 | 20 detected, golden and restored pass |
| `tb/pp_top/name_wr_mutant.py` | 0 | decode killed, golden and restored pass |
| `tb/acmp_talker/retry_mutants.py` | 0 | 62 killed, 7 equivalence and 1 performance controls |
| `tb/srp_admission/mutants.py` | 0 | 12/12 |
| `tb/desc_mem_guard/mutate.py` | 0 | hold-deleted mutant detected |
| `git diff --check c951a9ff..9185c49` | 0 | |

Parent consumer set: a scratch parent exported from milan-fpga dev `9e3ccbfb`, with `external`, `gptp-processor` and `third_party/verilog-axis` at their pins and the `protocol-processor` gitlink at `9185c49`. The sixteen commands, in the manager's order:

| Command | rc | Note |
|---|---:|---|
| `python3 scripts/check_cpp_idiom.py` | 0 | at `e8ec039` it refused this lane's new test code (Rule 11: 3 multi-declarator array initializers, 1 long function); fixed in `9185c49` |
| `python3 scripts/check_py_idiom.py` | 0 | at `e8ec039` one undocumented function in the new campaign driver; fixed in `9185c49` |
| `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet; none introduced here (the one in `protocol_processor_top.sv`, `srp_class_a_prio_w`, predates this lane) |
| `python3 scripts/check_rtl_source_lists.py` | 0 | |
| `python3 scripts/pp_srcs.py --check --selftest` | 0 | |
| `python3 sw/builder/test_builder.py` | 0 | all gates pass except one recorded NOT RUN arm (gate 11: the placement report is absent on the host) |
| `make -C tb/verilator/pp_shadow -j8` | 0 | 635 checks, 0 failures |
| `python3 scripts/check_port_contracts.py` | 0 | protocol-processor 111 <= 111 undocumented |
| `python3 scripts/measure_naming.py --check` | 0 | |
| `python3 scripts/measure_test_evidence.py --check` | 0 | 74 <= 77 unarmed suites, 0 unexplained readers |
| `python3 scripts/docs_check.py` | 0 | |
| `python3 scripts/lint_rtl.py --check` | 0 | 90 <= ratchet 90 |
| `make -C tb/verilator/nvm_cosim lint` | 0 | no PINMISSING |
| `make -C tb/verilator/nvm_cosim quick` | 0 | 315/315 |
| `make -C tb/verilator/milan_dp -j8` | 0 | every leg passes (gptp, gptp-lat, gmstep, main, nxn, nxndv, nxn8, nxn4c, nolpf, prune, ax1x1, aclk, notify, crflic) |
| `make -C tb/verilator/milan_dp_render -j8` | 0 | 65/65, 152/152, 5/5 |

## What remains

- **#85 item 4.** The available_index interop against a live controller needs a bench lane. #85 stays open.
- **Found here, not acted on.** IEEE 1722.1-2021 §6.2.2.18 sets current_configuration_index to 0 on transmit unless AEM_CONFIGURATION_INDEX_VALID (mask `0x02000000`) is set in entity_capabilities. F04.6 leaves that flag clear, and Milan §5.6.2 neither requires nor forbids it. This lane follows #40's acceptance, so the index moves. Whether F04.6 should set the flag is a decision for the manager.
- **Merge-train note with the open PR #132.** #132 adds a restore writer to the dynamic store. The new valid flag decodes the store's write bus as this tree has it. Whichever PR merges second must keep that decode on the bus the store actually takes, so a restored configuration row counts as set. Otherwise a restored configuration advertises `current_cfg_i` until the first SET_CONFIGURATION.
- Hosted CI and the two reviews. No hardware was used.

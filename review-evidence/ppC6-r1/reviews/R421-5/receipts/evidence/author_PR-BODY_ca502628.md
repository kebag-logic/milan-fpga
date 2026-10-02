[A463]
Closes #54
Closes #58
Closes #80
Closes #86

Lane C6 of the PP program (notifications and Identify), assignment on #80 comment 5915639621, design gate ruled on #80 comment 5915765717 (authorized with four conditions). Branch `c6-notifications`, five commits on `main` `0451d83d`, head `5e80629`.

| Commit | Item |
|---|---|
| `018ee6c` | 1, 2. #54, #80, #86: IDENTIFY_NOTIFICATION origination behind `EN_IDENTIFY_NOTIF_P` (default 0), `identify_button_i`, the third `tb/pp_top` build (section ID) and section ID0; integrator guide §2/§6, diagram 21, F01.5, 02, 08 |
| `b5beed6` | 3. #58: a byte-exact wire push per notifying command class (section NP); the unsolicited SET_STREAM_INFO fixed to Figure 7-40; `tb/ucpu` N6/N7 |
| `4ce963e` | 4. #80, #86: the STORM and RND suites (`tb/pp_top` ST, RN) and the originator's seeded inflight session (`tb/originator` R) |
| `5cf99f7` | 4. the lane's 30 negative controls: `tb/pp_top/notify_mutants.py` |
| `5e80629` | 1, 3, 4. #86 acceptance 1/4 and #58 acceptance 3 in 03 §4/§5 and 06 §7; GAP-06, GAP-17, REQ-AEM-026, REQ-NOT-001/-002 in 00; 09 §8.3; the guides; the suite READMEs and mutation records |

## 1. #80, #86: the identify machinery and the producers

**Clauses.** IEEE 1722.1-2021 §7.4.39 and Figure 7-61 (the unsolicited-only IDENTIFY_NOTIFICATION, u = 1, CONTROL / the IDENTIFY control's index), §7.4.39.2 (as a command: BAD_ARGUMENTS), §7.5.1 (multicast to the Table B.1 "Identification Notifications" address 91-E0-F0-01-00-01, three times 150 ms apart, controller_entity_id the Table 7-180 value 90-E0-F0-FF-FE-01-00-01, a sequence_id from 0 at power up), §7.5.1.2.1 (txIdentify: all three frames carry identifySequenceID), §7.5.1.3 and Figure 7-142 (IDENTIFY re-entered at timeout = entry + 1 s while `identifyButtonPressed`, WAITING on release); Milan §5.4.5.4 (a "should" for a PAAD that lets its user report it; the mapping to the user's action is vendor-specific; not the IDENTIFY control of §5.3.12).

**RTL, under the ruling's conditions.**
- `protocol_processor_top` gains `EN_IDENTIFY_NOTIF_P` (P-EN-IDENTIFY-NOTIFICATION, default **0**, condition 1) and the input `identify_button_i`. The input is 2FF-synchronised inside `KL_aecp_notify`; its contract (top port comment, integrator guide §1/§6) says the integrator debounces it; it is read only when the parameter is 1 (condition 2).
- `KL_aecp_notify`: a generate-gated sequencer. At 0 it leaves no flop and no gate; at 1 it presents one job per frame on the existing `uns_*` face (new kind `PP_UNS_IDENT_C` = 15, the one free code), with the Table B.1 DA, the Table 7-180 controller EID, identifySequenceID and {CONTROL, `identify_index_i`}. t0 is the first frame's next ms boundary, frames 2 and 3 are due t0 + T-IDENT-BURST and t0 + 2 x T-IDENT-BURST through the IDENT-BURST singleton, each armed only after the frame before it has gone (a held engine delays a burst, never bunches it), and IDENT-REARM at t0 + T-IDENT-REARM re-arms a held button (two owner-tag generations, 0xB2/0xB3, so a REARM armed for an abandoned wait never passes for the current one). The job takes the `uns_*` face only between two registry jobs, owns it until the engine retires it, and holds the command path meanwhile; it needs no registration, touches no row and is not lock-gated.
- `KL_aecp_engine` maps kind 15 to command_type 0x0026 and the 6-word µprogram `E_IDNOTIF` only with the parameter (no-send otherwise). The top passes the singletons `single + 1` / `+ 2` and extends the owner-tag guard.

**TIMER, SELF, MGMT (#86 acceptance 1 and 4).** The landed shape is made normative in 03 §4/§5, GAP-17's disposition and the top's tie-off comments: dispatch is RX-only; expiries reach their owners on the expiry bus; AECP unsolicited responses (IDENTIFY_NOTIFICATION among them) are engine-internal SELF jobs; CONTROLLER_AVAILABLE is the one command PDU through the originator; the PROBE_TX exact-duplicate retry stays in the listener (`PROBE_SLOTS_P = 0`); **MGMT is not supported by this build**.

**Tests.** Section ID (third build, `obj_idn/Vpp_top_idn`, parameter 1), 62 checks: ID1 one press, three frames byte-exact, gaps 15,264 and 15,000 clocks (150 ms = 15,000; the second gap is exact because both deadlines chain from one t0), nothing else on the wire; ID2 held 2.5 s, three bursts at sequence_id 1, 2, 3, re-arms 100,265 and 100,200 clocks after the previous burst's first frame, none after the release; ID3 a release and a press inside a burst (the burst is not cut; the next follows at once); ID4 the command form still BAD_ARGUMENTS and SET_CONTROL IDENTIFY sends nothing; ID5 a 15-row fan-out delays the burst by at most two frames and every row keeps its sequence_id; ID6 a press before the restore goes out at the release with its spacing, at sequence_id 0 after the reset. Section ID0 (default build): the button puts nothing on the wire.

**Both settings graded (condition 4).** At 1: section ID and eleven identify mutants, all killed (record below). At 0:
- every pre-lane check of the default build passes unchanged (7,924), and ID0 grades the button inert;
- yosys `equiv_*` proves `KL_aecp_notify` at 0 equivalent to main's (6,365 `$equiv` cells, 0 unproven), and the engine's own logic at 0 equivalent to main's plus this lane's SET_STREAM_INFO fix (21,481, 0 unproven; its five submodules are byte-identical to main and matched as cut points);
- out of context the flip-flop, carry, RAM and DSP counts equal main's exactly (table below).

## 2. #54: IDENTIFY_NOTIFICATION origination, graded on the wire

Acceptance 1 to 4 as in item 1: the input behind the parameter, default off with zero area; three byte-exact frames to 91-E0-F0-01-00-01 with controller_entity_id 90-E0-F0-FF-FE-01-00-01 and an identifySequenceID that increments per burst (the §7.5.1.2.1 / Figure 7-142 reading), spaced by T-IDENT-BURST through the shared timer service; a held button re-arms no faster than T-IDENT-REARM, graded with recorded mutations; A6 unchanged; 06 §7 and GAP-06 updated.

## 3. #58: a wire-level push per command class, and the non-ATDECC path

**Clauses.** Milan §5.4.5.1 (every registered controller but the requester, per-entry DA, entity_id and sequence_id, +1 per notification), §5.4.5.2 (a successful response that modifies the state; the non-ATDECC paragraph); IEEE §7.5.2 (the notification is an unsolicited response to the command: its body is the command's response format, §7.4.7.1, §7.4.9.1, §7.4.15.1, §7.4.25.1, §7.4.21.1, §7.4.35.1/§7.4.36.1).

**Tests.** Section NP, 47 checks: with the requester and a second controller registered, each of SET_CONFIGURATION (to 1 and back to 0), SET_STREAM_FORMAT, SET_STREAM_INFO, SET_CONTROL (255 and 0), SET_SAMPLING_RATE, STOP_STREAMING and START_STREAMING answers byte-exact, pushes exactly one byte-exact u = 1 response to the second controller at its own sequence_id (modelled from the wire: the count of what that entry was sent), and none to the requester; a SET from the second controller reaches the requester at its own untouched count; unchanged SETs push nothing.

**RTL defect found by NP3 and fixed** (`hdl/aecp/KL_aecp_engine.sv:1372-1375`, `hdl/aecp/ucode/gen_ucode.py:2076` `E_SINFOUNS`). The unsolicited SET_STREAM_INFO carried Milan's 56-byte GET_STREAM_INFO body (cdl 68) under the SET_STREAM_INFO command type. IEEE §7.4.15.1 gives the SET_STREAM_INFO response Figure 7-40's 84-byte body (cdl 96), and Milan §5.4.2.10 replaces the GET response's format alone. The job now builds {type, index}, MSRP_ACC_LAT_VALID alone, the presentation-time offset in force, zeros elsewhere: the bytes of the successful solicited answer. Failing arm on the landed RTL: NP3 (`got (94 B) ... 00 44 ...`, `exp (122 B) ... 00 60 ...`).

**Acceptance 2.** `enq_dropped_configuration`, `enq_dropped_stream_info`, `class_4_mapped_to_rate` and `class_9_mapped_to_control` (the `KL_aecp_notify` class pick) are each killed by the named NP checks (record below, and `tb/pp_top/README.md`).

**Acceptance 3, second arm.** 06 §7 trigger class (2) and the REQ-NOT-002 row state that MGMT-origin (non-ATDECC) changes are not supported by this build: nothing outside ATDECC can change command-settable state, so §5.4.5.2's second paragraph has no trigger.

## 4. The RND and STORM notification suites (#80), and #86's inflight RND

- **ST** (18 checks): sixteen controllers registered in three waves (rows at sequence_id 2, 1, 0), one change from row 15 reaches the other fifteen byte-exact at their own sequence_ids; GET_COUNTERS churned at 10 Hz on five descriptors for 3.5 s emits at least three and at most one round per descriptor per second (closest rounds 99,994 clocks apart), every counter frame byte-exact; a GET_CONFIGURATION and an ACMP GET_RX_STATE every 700 ms stay inside T-BUDGET-AECP-WC and T-BUDGET-ACMP-RESP counted in clocks at the wrap's nominal clock (worst 70,958 and 249 clocks against 100,001 and 50,001).
- **RN** (4 checks): seed 0xC6A46301, 720 steps from twenty controllers of REGISTER / DEREGISTER / LOCK / UNLOCK / SET_CONTROL / SET_CLOCK_SOURCE / GET_CONTROL against an independent registry and lock model (capacity 16, refresh keeps the sequence_id, one holder, keep-alive, the compressed 60 s expiry, requester-excluded pushes): 2,203 frame comparisons, zero divergence; 24 NO_RESOURCES, 117 lock denials, 10 takes, 7 automatic unlocks, 239 lock-refused SETs, 375 pushes.
- **`tb/originator` R** (3 checks, #86 acceptance 3): seed 0x86A46301, 4,000 steps over sixteen owners of overlapping CONTROLLER_AVAILABLE-shaped exchanges, with responses (also to a first attempt whose retry still waits), stray responses, expiries fired in random order among the due slots, and cancellations, against an independent inflight model: 3,757 events, zero divergence, up to eight live exchanges; 661 routed, 366 retried, 87 failed, 95 cancelled, 409 strays.

**Mutation record** (`python3 tb/pp_top/notify_mutants.py --output DIR`; 30 of 30 KILLED at the head, goldens pass):

| Mutant | Failing checks |
|---|---|
| `ident_two_frames` | 19, ID1 first |
| `ident_seq_per_frame` | 22, ID1b first |
| `ident_no_rearm` | 12, ID2 first |
| `ident_rearm_from_third_frame` | 12, ID2 and ID2d |
| `ident_burst_100ms` | 20, ID1c first |
| `ident_t0_at_request` | 22, ID6d among them |
| `ident_cut_on_release` | 22, ID1 first |
| `ident_release_ignored` | 35, ID1 first |
| `ident_unicast_da` | 7, ID1 first |
| `ident_face_taken_mid_job` | 3: ID5b, ID5c, ID5f |
| `ident_built_at_default` | 2: ID0, ID0b |
| `enq_dropped_configuration` | 2: NP1, NP1b |
| `enq_dropped_stream_info` | 1: NP3 |
| `class_4_mapped_to_rate` | 4: NP4, NP4b, NP8, RN |
| `class_9_mapped_to_control` | 2: NP6, NP7 |
| `requester_not_excluded` | 12, NP1 first |
| `entry_seq_not_advanced` | 13, NP1b first |
| `stream_info_get_body` | 1: NP3 |
| `counter_limit_500ms` | 12: ST2, ST2b, ST3, ST3b |
| `fan_out_skips_row_0` | 9, ST1b among them |
| `refresh_resets_seq`, `foreign_unlock_allowed`, `lock_taker_notified`, `deregister_keeps_row`, `set_control_ignores_lock` | 1 each: RN |
| `registry_holds_15` | 2: ST1, RN |
| `inflight_highest_free_id`, `inflight_match_ignores_seq`, `inflight_cancel_keeps_timer`, `inflight_shared_seq` | 15, 7, 5, 10, `tb/originator` R among them |

## 5. Parent-visible list

Read against the parent at milan-fpga dev `ccdd07b5`.

1. **`protocol_processor_top` gains an input, `identify_button_i`, and a parameter, `EN_IDENTIFY_NOTIF_P` (default 0).** Authorized by the ruling on #80. The parent's `KL_pp_shadow` instantiates the top by named ports and must connect the pin. Adoption edits, in `parent-adoption-c6.patch` (applied after the combined #132 + C1 adaptation):
   - `hdl/milan/KL_pp_shadow.sv`: `.identify_button_i (1'b0)` and `.EN_IDENTIFY_NOTIF_P (1'b0)`, each with a `//!` rationale above it (the port gate's literal-bound rule): 0 until a debounced board button is wired.
   - `scripts/measure_test_evidence.py`: a `DUT_READER_DISPOSITIONS` entry for `protocol-processor/tb/pp_top/notify_mutants.py`, the new mutation driver (a campaign that plants defects in an isolated copy and reads no expected value from the text). Without it the evidence ratchet fails: 1 unexplained DUT-source reader.
   - The port-contract and naming checks gain the port with no edit: `check_port_contracts.py` counts it documented (protocol-processor 111 <= 111 undocumented, and the tie-off carries its rationale), and `measure_naming.py` passes (96 recorded).
2. **The integrator guide (§1, §2, §6) and diagram 21 gain the parameter and the input**, in this repository; `check-integrator-params.py` passes (27 = 27 = 27).
3. **Behaviour at the parent's setting (0):** none changes except the SET_STREAM_INFO fix of item 3: an unsolicited SET_STREAM_INFO (sent only to other registered controllers after a successful, changing SET_STREAM_INFO on a Stream Output) now carries Figure 7-40's 84-byte body instead of the GET_STREAM_INFO form. The parent's benches do not grade that frame.
4. **Entry points:** `make -C tb/pp_top identify` (the third build and ID0), `./obj_dir/Vpp_top_sim --notify-only` (NP, ST, RN), `--identify-only` (ID0), and `python3 tb/pp_top/notify_mutants.py --output DIR`. `make -C tb/pp_top` now builds three executables and sums three tallies.
5. **Optional matrix citations:** the parent's `docs/reference/MILAN_COMPLIANCE_MATRIX.md` 5.4.5 rows can cite sections NP, ST, RN and (for 5.4.5.4, with the parameter at 1) ID.

## Validation

Verilator 5.050 (the CI pin), builds capped at eight jobs. Processor, every command at `5e80629`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | 33 suites, 1,017,309 checks, 0 failing. `pp_top` 8,078 (default build 7,996 = the pre-lane 7,924 + ID0 3 + NP 47 + ST 18 + RN 4; fixture 20; identify 62), `originator` 107 (104 + R 3), `ucpu` 396 (386 + N6/N7 10). Base `0451d83d`: 1,017,162 |
| `./scripts/lint_hdl.sh` | 0 | 41 modules; the three changed modules also lint clean at `EN_IDENTIFY_NOTIF_P` = 1 |
| `make check` | 0 | lint (41 mermaid + 18 wavedrom), WaveDrom, links, both matrices, parameters (27 = 27 = 27), stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `python3 tb/pp_top/notify_mutants.py` (new) | 0 | goldens pass, 30 of 30 KILLED by their named checks |
| `make -C tb/adp_engine mutants` | 0 | 30 of 30 killed |
| `make -C tb/srp_top mutants` | 0 | 78 of 78 killed, assertion coverage 65/65 |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 of 20 detected; golden and restored pass |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed; 7 equivalence and 1 performance controls retained |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` (two `--only` chunks) | 0 | 83 of 83 killed; goldens pass |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the tree |
| `git diff --check 0451d83d..5e80629` | 0 | |

Out-of-context cost (condition 1; yosys 0.66 `synth_xilinx -family xc7 -flatten` of the whole top, no Vivado on this host):

| Build | LUT | FF | CARRY4 | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|
| main `0451d83d` | 62,463 | 30,454 | 2,317 | 16 / 1 | 4 |
| head, parameter 0 | 62,783 | 30,454 | 2,317 | 16 / 1 | 4 |
| head, parameter 1 | 63,352 | 30,530 | 2,331 | 16 / 1 | 4 |

At 0 the flip-flop, carry, RAM and DSP counts are main's; the LUT difference is the mapper's variance between netlists proven equivalent (`KL_aecp_notify` alone maps 6,598 vs 8,002 LUT at the same 1,721 FF). The identify sequencer at 1 costs +76 FF, +14 CARRY4 and +569 LUT as mapped (dominated by the 165-bit uns-face mux).

Parent consumer set (the 16 commands) at milan-fpga dev `ccdd07b5`, in a scratch copy (git archive of the trusted checkout and its submodules, the processor at this head) with `parent-adaptation-132-c1.patch` and then the C6 adoption edits applied:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet within budget |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | processor undocumented 111 <= 111; 52 literal-bound and 62 without local rationale, all recorded |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | 74 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 9 | `python3 scripts/xvlog_gate.py` | 0 | 4 findings == ratchet |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local mf48 build tree) |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 295 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | every bench PASS, 0 FAIL (compile jobs bounded for memory; model parameters unchanged) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 5 leg-defect arms caught |

Measured need for the adoption edits: without the `KL_pp_shadow` tie-off, command 11 fails (a new PINMISSING on `identify_button_i`); without the `measure_test_evidence.py` disposition, command 7 fails (1 unexplained DUT-source reader).

## What remains

- Hosted CI on the PR, and the reviews ([R420] internal, [R421] external).
- The parent adopts the item 5 edits (`parent-adoption-c6.patch`, supplied with the lane handoff) when it moves its processor pin past this head; no parent change was made here.
- No hardware was used. The identify sequencer is graded in simulation only; no board button exists yet, so the parent keeps the parameter at 0.
- Resource figures are yosys `synth_xilinx` out of context (no Vivado on this host); a Vivado out-of-context run at the parent is the authoritative figure.
- Not attempted: the optional overflow eviction sweep (MAY; a recorded decision, no work owed per #80). RN grades a lock-refused SET on its status and length, not its body, which is #53's decision.
- Observation, outside this lane's acceptance: IEEE §7.5.2 lists DEREGISTER_UNSOLICITED_NOTIFICATION among the notifying commands, and a solicited DEREGISTER does not push; recorded, not changed.

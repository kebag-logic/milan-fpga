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

Round 2 (the merge of `main` `3f3ea56b` and four commits, head `88e0bf8`) is under [Round 2](#round-2). It replaces round 1's identify schedule. Frames 2 and 3 are no longer deadlines from t0: every frame is due T-IDENT-BURST after the previous one left. A release and a press inside a burst now start the next burst T-IDENT-BURST after the third frame, not at once. Section ID is 106 checks and the mutation record has 34 controls. The round-1 text below describes the head `5e80629`.

Round 3 (two commits on round 2, head `9624ef4`) is under [Round 3](#round-3). The gap round 2 put after a burst's third frame no longer drops a press: a press made inside a burst or in that gap is latched, and its burst starts when the gap ends. Section ID is 178 checks, `tb/aecp_notify` grades the schedule's one-tick margins at the full timebase, and the mutation record has 40 controls.

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

## Round 2

Round 2 answers R420-1 (comment 5921785256, two MINOR) and R421-1 (comment 5921513647, one MINOR), in the order of the assignment on #80 (comment 5924910356). The merge is a merge commit; nothing is rebased. Head `88e0bf8`.

| Commit | Item |
|---|---|
| `a011b14` | 1. Merge `main` `3f3ea56b` (#136, #135, #137), keeping both sides |
| `6094928` | 2. R420-1 F1, R421-1 F1: every IDENTIFY_NOTIFICATION frame is due T-IDENT-BURST after the previous one's departure; `tb/pp_top` ID5i-ID5l and ID7 (MAC stalls), four new controls |
| `48718d6` | 3. R420-1 F2: the HDL engineer's CDC rule and `hdl/README.md` name the `identify_button_i` synchroniser |
| `2e99ab0` | 4. Suggestions: `ASYNC_REG` and the integrator's constraint, the release-and-press reading, the SINFO `tix_w` comment, the retained controls and the limiter decision recorded |
| `88e0bf8` | the parent's C++ and Python idiom gates (Rules 11 and 12) on round 2's test code |

### 1. The merge of `main` `3f3ea56b`

Main touched 48 files, and six of them are shared with the lane. Three of those auto-merged with no edit: `docs/00_MILAN_COMPLIANCE_REVIEW.md`, `docs/architecture/09_verification.md` and `tb/pp_top/pp_top_wrap.sv`. Three conflicted, and each was resolved by keeping both sides:
- `tb/pp_top/Makefile`: one `.PHONY` line carries main's `maap-internal` and the lane's `identify-build identify`.
- `tb/pp_top/sim_main.cpp` `main()`: all six section flags, then main's MP call, then main's sections followed by the lane's.
- `tb/pp_top/README.md`: main's sections MP and AC first, then "Lane C6", each whole.

`.gitattributes` and `.github/workflows/hdl.yml` come from main alone, so every main entry and CI step is kept. Every text-plant mutation driver was checked against the merged tree, and none of their anchors moved: `acmp_mutants.py` (main's, 19 entries), `notify_mutants.py`, `d3_mutants.py` (83) and `gsi_mutants.py` (20). The `.patch` campaigns (`tb/adp_engine`, `tb/maap`) touch files the lane does not.

### 2. The burst spacing (R420-1 F1, R421-1 F1)

**Clauses.** IEEE 1722.1-2021 §7.5.1 and §7.5.1.2.1: txIdentify sends the notification three times "with a 150 ms delay between transmissions". Figure 7-142 sets the 1 s timeout on entry to IDENTIFY, which is unchanged.

**Defect.** Round 1 made frames 2 and 3 due at t0 + 150 ms and t0 + 300 ms. The timer service fires a past deadline on its next sweep, so a late frame 2 made frame 3 due at once. The RTL banner, F08.1, 09 §8.3, the suite README, the ID6 test name and this body all said that could not happen.

**Why departure, not retirement.** The engine retires a job (`uns_done`) at the TX arbiter's lane grant. A MAC with `tx_ready_i` low still holds a frame the engine has let go, so scheduling from retirement would still bunch frames. That variant is now a control (`ident_departure_is_retirement`): with the MAC stalled inside frame 1, it leaves frames 1 and 2 63 clocks apart.

**RTL fix.**
- `hdl/aecp/KL_aecp_notify.sv:290`: new input `uns_tx_busy_i`, high while an unsolicited frame is granted and its last byte has not left yet. It is read only with `EN_IDENTIFY_NOTIF_P` (`:851-854`).
- `:736`: `dep_w = (done_w || left_r) && !uns_tx_busy_i`. With `left_r` (`:789-790`), the face is still released at retirement, but the schedule waits for the frame itself.
- `:802-807`: every departure arms IDENT-BURST and sets `gap_r`. `:746`: the deadline is `now_ms_i + 151`, so frame N+1 is due at least T-IDENT-BURST after frame N left, and under one tick more.
- `:794`, `:840`: a burst's first frame (a fresh press, or the re-arm of a held button) also waits for `gap_r`. So a stall that pushes a third frame past the timeout cannot put the next burst straight behind it.
- t0 (`:814`) is now only the REARM base: the first frame's departure, rounded up to the next ms boundary.
- `hdl/top/protocol_processor_top.sv:4314-4325` `gen_uns_departure`, built only with the parameter (at 0 `uns_tx_busy_w` is 0):
  - `busy_r` is set on the UNS lane's grant and cleared on the arbiter's eof handshake. Grants are frame-atomic, the same property the ACMP prepend shim relies on.
  - `uns_done_o` is registered on the same grant edge (`KL_aecp_engine.sv:2510`, A_TXW to A_FREE), so `busy_r` is already high when the job retires.
- No top port, no parameter and no register.

**Tests** (`tb/pp_top/notify_phases.hpp`; section ID grows from 62 to 106 checks):
- `SLACK` is 400 clocks: one tick, plus the sweep's walk to the identify slots (at most 91), plus the build and serialization (under 200).
- **ID1-ID3:** every gap now measures 15,264 to 15,301 clocks (150 ms = 15,000). **ID3f:** a release and a press inside a burst start the next burst 15,301 clocks after the third frame. It was 106 clocks in round 1.
- **ID5i-ID5l** (R421-1's shape): a 15-row SET_NAME fan-out is fed at frame 1 + 14,450, + 14,700 and + 14,950 clocks.
  - The largest gap 1->2 is 16,147 clocks (ID5l, the anti-vacuity check).
  - The smallest of the six gaps is 15,240 clocks. In round 1 it was 14,109.
- **ID7** (the assignment's arm: the MAC stalled mid-burst):
  - ID7-ID7e, a 400 ms stall inside frame 1: gap 1->2 is 15,270 clocks.
  - ID7f-ID7i, a 400 ms stall after frame 1 (R420-1's probe): gap 2->3 is 15,264 clocks. In round 1 it was 164.
  - ID7j-ID7m, a 250 ms stall after frame 2.
  - ID7n-ID7t, a button held through a 900 ms stall after frame 1, so the timeout passes mid-burst. The next burst starts 15,301 clocks after the third frame, never at once, and still no sooner than T-IDENT-REARM after its own first frame.
- **ID6** is renamed `a_press_before_the_restore_goes_out_at_the_release`. It holds the engine only before frame 1, so its old "never bunches" name claimed too much.
- **Failing arm on the round-1 RTL:** the new `notify_phases.hpp` built against the merge's HDL fails 7 of 106 checks: ID3f (106 clocks), ID5k (14,109), ID7d (63), ID7e (207), ID7i (164), ID7q (63) and ID7r (10,111).

**Controls** (`tb/pp_top/notify_mutants.py`, all KILLED):

| Mutant | Planted | Failing checks |
|---|---|---|
| `ident_burst_from_t0` (the assignment's control) | round 1's schedule: IDENT-BURST due t0 + 150 / 300 ms | 5: ID3f, ID5k, ID7i, ID7q, ID7r |
| `ident_departure_is_retirement` | `dep_w = done_w` | 2: ID7d, ID7q |
| `ident_departure_unwired` | the top ties `uns_tx_busy_i` to 0 | 2: ID7d, ID7q |
| `ident_next_burst_at_once` | `gap_r` dropped from the WAIT and HOLD starts | 2: ID3f, ID7r |

`ident_two_frames`, `ident_rearm_from_third_frame` and `ident_t0_at_request` are re-anchored to the new text. Under the new schedule t0 drives only REARM, so `ident_t0_at_request` is now named on ID2d (burst 3 starts) instead of ID6d.

**Corrected text:**
- the RTL banner (`KL_aecp_notify.sv:154-170`) and the t0 comment;
- F08.1 T-IDENT-BURST and 09 §8.3's TIM row;
- 06 §7 "Identify" and integrator guide §6: a stalled `tx_ready_i` delays the burst and never bunches it;
- the section-ID text in `tb/pp_top/README.md`.

### 3. R420-1 F2: the synchroniser in the HDL contract

`docs/guides/hdl-engineer.md` §2's CDC row now names the one synchroniser inside the modules: `btn_q1_r`/`btn_q2_r`, which take `identify_button_i` into `KL_aecp_notify` and are built only with `EN_IDENTIFY_NOTIF_P` = 1, under the ruling on #80. It links integrator guide §1/§6 and 02 §2 rule 3. Every other crossing stays the integrator's. `hdl/README.md` says the same. No RTL change.

### 4. Suggestions

| Suggestion | Disposition |
|---|---|
| R420-1 S1: the `!core_arm_w` collision and the `gen_r` flip are not exercised | **Retained, recorded** in `tb/pp_top/README.md`. The reviewer's three extra mutants, re-run unchanged at round 2, all SURVIVE with every section-ID check passing. Reasons: a collision needs a registry op to arm in the single cycle after a departure, which a directed check could only reach by sweeping the command arrival cycle by cycle; the stale-REARM window is a few cycles, and the departure clears `fired_r`; a missing second synchroniser flop is CDC hygiene that a two-state simulation cannot see |
| R420-1 S2, R421-1 S2: no synchroniser marking or constraint | **Taken.** `(* ASYNC_REG = "TRUE" *)` on `btn_q1_r` and `btn_q2_r` (`KL_aecp_notify.sv:712-713`). Integrator guide §1 makes declaring the pin-to-`btn_q1_r` path asynchronous (false path or max delay) the integrator's job |
| R420-1 S3, R421-1 S4: the LUT figures | **Taken.** The flow is stated and the table is re-measured at this head (Validation, round 2). The LUT deltas are mapper variance between netlists proven equivalent, so FF, CARRY4, RAM and DSP are the cost figures |
| R420-1 S4: ST2b accepts rounds 99,994 clocks apart | **Retained, recorded** in `tb/pp_top/README.md` ST2. The limiter predates the lane and counts "once per second" on the 1 ms timebase like every T- value (08 §3), so two rounds are at least 1,000 ticks apart, which can be up to one tick short of a second in core clocks. A change to a shared limiter that other suites grade belongs to its owner |
| R421-1 S1: a release and a press inside a burst | **Taken, as a stated reading** in 06 §7 and F06.16. The edge is latched while txIdentify runs, and the next burst starts T-IDENT-BURST after the third frame (item 2's gap). ID3 grades it |
| R421-1 S3: `gstri_r` still set for `PP_UNS_SINFO_C` | **Kept, and the reason is now in the RTL** (a comment in `KL_aecp_engine.sv`). The flag selects `tix_w`, the {type, index} operand that `E_SINFOUNS`'s `BUILD_FLD ra=13` reads, and the job gathers nothing. Comment only; the engine is unchanged |

### 5. The parent's idiom gates on round 2's test code

The parent consumer set at `2e99ab0` failed three commands. Two of the failures were in this lane's round-2 test code; the round-1 versions of both files were clean. `88e0bf8` fixes them:
- `check_cpp_idiom.py` (Rule 11): `notify_phases.hpp`'s ID5i had a one-line array initializer (counted as a multi-declarator) and a two-variable declaration, and ID7's function was 101 lines against a limit of 100. The initializer is split across lines, as #137 did in `a7ccd9e`. The two variables are declared apart. Each of ID7's four stalls gets its own function, every check message byte-identical.
- `check_py_idiom.py` (Rule 12): one 122-column line in `notify_mutants.py`. Every planted string is unchanged.

Section ID still passes 106 of 106 with the same measured gaps.

The third failure, `measure_test_evidence.py` (1 unexplained DUT-source reader), is main's `tb/pp_top/acmp_mutants.py` from #137. It fails the same way with the processor at `main` `3f3ea56` alone, and #137 records its parent disposition line.

### Parent-visible list, round 2

Round 2 adds no top port, no top parameter and no register. Nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0), and `parent-adoption-c6-e4b771f9.patch` is unchanged.

1. **`KL_aecp_notify` gains one internal input, `uns_tx_busy_i`** (documented), driven inside the top. It is not a top port, but the parent's port-contract gate counts it: processor ports go from 1,748 at `main` `3f3ea56` to 1,752 at this head (round 1's three identify ports, plus this one), with 111 <= 111 undocumented at both. No parent edit and no budget change.
2. **`gen_uns_departure`** and **`ASYNC_REG`** on the two synchroniser flops exist only with the parameter at 1. A parent that sets 1 must declare the pin-to-`btn_q1_r` path asynchronous (integrator guide §1).
3. **Main's `tb/pp_top/acmp_mutants.py` (#137) arrives with the merge.** The parent's `measure_test_evidence.py` needs #137's documented `DUT_READER_DISPOSITIONS` line. Whichever adoption first moves the parent's processor pin past `3f3ea56` owes it; it is not part of the C6 patch.
4. `notify_mutants.py` now holds 34 controls. The C6 patch's disposition covers the driver as a whole.

### Validation, round 2

Verilator 5.050 (the CI pin), builds capped at eight jobs, one heavy command at a time. Processor, every command at `88e0bf8`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate PASS; 33 suites, 1,018,084 checks, 0 failing. `pp_top` 8,170 (default build 8,044, fixture 20, identify 106) |
| `make -C tb/pp_top identify` | 0 | section ID 106 checks, ID0 3 checks |
| `./scripts/lint_hdl.sh` | 0 | 41 modules; `KL_aecp_notify`, `KL_aecp_engine` and `protocol_processor_top` also lint clean at `EN_IDENTIFY_NOTIF_P` = 1 |
| `make check` | 0 | lint (41 mermaid + 18 wavedrom), WaveDrom, links (999), both matrices, parameters (27 = 27 = 27), stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `git diff --check 3f3ea56b..88e0bf8`, `5e80629..88e0bf8` | 0 | |

Mutation campaigns at `88e0bf8` (each plants its defects in private copies; the tree was clean after each):

| Command | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --jobs 1` | 0 | goldens pass; 34 of 34 KILLED by their named checks (round 1's 30, re-anchored where item 2 names, and round 2's 4) |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` (main's, #137; its anchors sit in the top this lane edits) | 0 | goldens pass; 19 of 19 KILLED |
| `make -C tb/adp_engine mutants` | 0 | 30 of 30 killed |
| `make -C tb/maap mutants` (main's, #135) | 0 | 3 controls pass; 29 of 29 killed |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 of 20 detected; golden and restored pass |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed; 7 equivalence and 1 performance controls retained |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the tree |
| `make -C tb/srp_top mutants` | 0 | 78 of 78 killed, assertion coverage 65/65 |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` (the whole set, then two `--only` chunks) | 0 | 83 of 83 killed; goldens pass in each run. A host reboot cut the whole-set run after 77 kills, and the six it had not reached ran at the same head in two chunks |

Out-of-context cost (yosys 0.66: `sv2v` of the whole tree with the generated ROM images, then `synth_xilinx -family xc7 -flatten -top protocol_processor_top`, the parameter set by `chparam`; no Vivado on this host):

| Build | LUT | FF | CARRY4 | MUXF7 / MUXF8 | RAM32M / RAM64M | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|---:|---:|
| main `3f3ea56` | 63,151 | 30,454 | 2,317 | 577 / 125 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, parameter 0 | 61,488 | 30,454 | 2,317 | 615 / 123 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, parameter 1 | 63,283 | 30,533 | 2,339 | 659 / 190 | 1,497 / 3 | 16 / 1 | 4 |

- At 0 the FF, CARRY4, RAM and DSP counts are main's. The LUT count moves by mapper variance: main's own top maps 688 LUT more at `3f3ea56` than round 1 measured at `0451d83d`, at the same FF. This time the head at 0 maps 1,663 LUT fewer than main. At 0 round 2 adds only a constant-0 net that `KL_aecp_notify` never reads.
- The identify sequencer at 1 costs +79 FF and +22 CARRY4. Round 1 measured +76 FF and +14 CARRY4. The difference is round 2's schedule: three flops (`gap_r`, `left_r`, and the top's `busy_r`) and the 32-bit `now_ms_i + 151` deadline adder (8 CARRY4). The LUT figure, +1,795 as mapped, carries the same mapper variance.

Parent consumer set (the 16 commands) at milan-fpga dev `e4b771f9`, in a scratch copy: a `git archive` of the trusted checkout with its submodules at their recorded pins and the processor at `88e0bf8`. Its index equals the trusted checkout's except the processor gitlink. Applied on top: `parent-adoption-c6-e4b771f9.patch` (unchanged), then #137's documented `DUT_READER_DISPOSITIONS` line for `acmp_mutants.py`, verbatim.

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget (multi-declarator 0 <= 0, long function 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet within budget (over-long line 0 <= 0) |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | processor 1,752 ports, undocumented 111 <= 111; 52 literal-bound and 62 without local rationale, all recorded |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | 73 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3. With the C6 patch alone: rc 1 on main's `acmp_mutants.py` only, as at `main` `3f3ea56` with no patch |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, the same four keys |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local mf48 build tree) |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | every bench PASS, 0 FAIL (compile jobs bounded for memory; model parameters unchanged) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 5 leg-defect arms caught |

At `2e99ab0`, commands 1 and 2 failed on round 2's test code. Item 5 above records those findings and their fix.

### What remains, round 2

- Hosted CI on the PR, and the round-2 reviews.
- The parent adopts `parent-adoption-c6-e4b771f9.patch` (unchanged by this round) when it moves its processor pin past this head. #137's `acmp_mutants.py` disposition line is owed by whichever adoption first moves the pin past `3f3ea56`.
- A reading this round relied on: the assignment's STOP covers top-level ports, parameters and parent-visible changes. `uns_tx_busy_i` is a port of the internal `KL_aecp_notify`, the one way the sequencer can see a frame's departure, and no top port or parameter changed. It is listed in the parent-visible list because the parent's port-contract gate counts it. If that reading is wrong, the round stands on that point for a ruling.
- Retained with their reasons in `tb/pp_top/README.md`: R420-1 S1 (three controls that survive, with every section-ID check passing) and R420-1 S4 (the shared GET_COUNTERS limiter's one-tick reading).
- No hardware was used. Resource figures are yosys out of context; a Vivado out-of-context run at the parent is the authoritative figure.
- Unchanged from round 1: the optional overflow eviction sweep is not attempted (a recorded decision), and the solicited DEREGISTER that does not push is recorded, not changed.

## Round 3

Round 3 answers R420-2 (comment 5930357457) and R421-2 (comment 5930105280), both NEGATIVE on the same MINOR, in the order of the assignment on #80 (comment 5932649053). This round has no merge of main, and nothing is rebased. Head `9624ef4`.

| Commit | Item |
|---|---|
| `ed000fe` | 1. R420-2 F1, R421-2 F1: a press made inside a burst or in the T-IDENT-BURST gap after it is latched, and its burst starts when the gap ends; `tb/pp_top` ID8; three controls |
| `9624ef4` | 2. Suggestions: a MAC stall on a frame's last byte (ID9) with a `ready` control; the `sim_main.cpp` build count; the one-tick timer margins graded at the full timebase (`tb/aecp_notify` section FT) with two controls |

### 1. A press made during the gap is latched (R420-2 F1, R421-2 F1)

**Ruling** (#80 comment 5932649053): latch, do not document the window.

**Clauses.** IEEE 1722.1-2021 Figure 7-142: WAITING moves to IDENTIFY on `identifyButtonPressed`, and IDENTIFY's entry action is txIdentify(). §7.5.1 and §7.5.1.2.1: the notification is sent three times "with a delay of 150 milliseconds between transmissions". Milan §5.4.5.4: the variable is TRUE while the user wants the PAAD to report itself.

**Defect.** Round 2 added `&& !gap_r` to the WAITING start and read the button as a level, with no latch. A press that began and ended inside the T-IDENT-BURST gap after a burst's third frame sent nothing. The HOLD start had the same guard, so a release and a new press inside a burst, still held when the third frame left and let go inside the gap, also sent nothing. A new press made and let go while a burst was still going out was never seen either (R421-2's related note).

**RTL fix** (`hdl/aecp/KL_aecp_notify.sv`; no port, no parameter, no register):
- `:728` a new flop, `prs_r`: a press is owed a burst when the gap ends.
- `:801-804` a new press after a release seen inside a burst is latched, while txIdentify or the gap after it runs.
- `:806-818` WAITING latches a press seen while `gap_r` runs (`:810`), and starts the burst on `(btn_q2_r || prs_r) && !gap_r` (`:811`), clearing the latch; the HOLD start clears it too (`:863`). Every start still waits for `!gap_r`, so no inter-frame gap goes under T-IDENT-BURST.
- Banner `:170-176`. Lint is clean at `EN_IDENTIFY_NOTIF_P` 0 and 1. At 0 the generate that holds the flop is not built.

**Tests** (`tb/pp_top/notify_phases.hpp`, section ID8; section ID is 178 checks at the head, 106 at round 2). The gap's end is the IDENT-BURST expiry on the shared timer bus. The test wrap gains three observe-only taps for it (`dbg_ident_gap_arm_o`, `dbg_ident_gap_deadline_o`, `dbg_ident_gap_end_o`), so a press can be placed against the gap's end to the clock:
- **ID8-ID8e** a 30 ms press made 2 ms after the third frame left, over long before the gap ends: one burst, 15,301 clocks after the third frame, its first frame 166 clocks after the expiry.
- **ID8f-ID8i** a 200 ms press made at the same point: one burst, starting as the latched press did.
- **ID8j-ID8n** "a press made exactly at gap end": a 30 ms press whose synchronised level the sequencer first samples one edge before the edge that samples the expiry, on it, and one and two edges after it. Each sends exactly one burst. The first three start on the latched press's edge (166 clocks after the expiry); the last starts one clock later (167), so the measure resolves a single clock. ID8j checks that the expiry came on the predicted clock.
- **ID8o-ID8r** a release and a new press inside a burst, held past the third frame and let go 30 ms into the gap: one more burst at the gap's end.
- **ID8s-ID8v** a release and a new 30 ms press between frames 1 and 2, let go before the burst ends: one more burst at the gap's end.
- ID8 and ID9 run after ID5 and before ID6's reset, so section ID still ends with ID7. Every ID1-ID7 measured value is unchanged from round 2.

**Failing arm on the round-2 RTL** (the head's tests on `88e0bf8`'s `hdl/`): 29 of 155 checks fail. Three are the lost presses (ID8, ID8o, ID8s: 3 frames in all, want 6). The rest follow from them: identifySequenceID is short by the lost bursts (ID8g, ID8l, ID9b, ID9f), and ID8's start is never measured (ID8i, ID8n).

**Controls** (`tb/pp_top/notify_mutants.py`, all KILLED):

| Mutant | Planted | Named checks |
|---|---|---|
| `ident_wait_ignores_gap` (the single-guard control) | `&& !gap_r` dropped from the WAITING start only; the latch stays | ID8c, ID8h |
| `ident_press_not_latched` | the WAITING latch removed | ID8 |
| `ident_burst_press_not_latched` | the in-burst latch removed | ID8o, ID8s |
| `ident_next_burst_at_once` (kept, re-anchored) | both starts' `!gap_r` dropped | ID3f, ID7r |

**Docs.** The operator guide's button row, integrator guide §6 and 06 §7 (with F06.16) now say the same thing. Every new press after a release is answered with a burst. A press made while a burst or the gap after it runs is latched, and its burst starts when the gap ends, however short the press. Presses made while a burst is already owed add none. F08.1's T-IDENT-BURST row, 09 §8.3 and the suite README follow.

### 2. Suggestions

| Suggestion | Disposition |
|---|---|
| R421-2 S1: a MAC stall on a frame's last byte, with a control that drops `ready` from the departure check | **Taken.** Section ID9: the bench's eof-beat hook holds `tx_ready_i` low on frame 1's last byte (ID9-ID9d), then frame 2's (ID9e-ID9h), for 400 ms. The next frame follows the byte's acceptance by 15,232 and 15,299 clocks. `ident_departure_ignores_ready` (`&& arb_tx_ready_w` dropped from the top's departure flop) is KILLED by ID9d and ID9h: 63 clocks, the round-1 bunching |
| R420-2 S2: the `tb/pp_top/sim_main.cpp` "two builds" comment | **Taken.** The tally comment says three builds, and so does the file header |
| R420-2 S1, R421-2 S2: the one-tick timer margins, invisible on the compressed timebase | **Taken, as a full-timebase check.** `tb/aecp_notify` builds a second time with `EN_IDENTIFY_NOTIF_P` = 1 and runs section FT. There 1 ms is 100,000 clocks, the F01.5 default P-CLK-HZ. The bench is the engine, the MAC and a timer model that fires on the first clock of the deadline's ms, the least favourable placement. FT2: a frame that leaves two clocks before a ms boundary is followed T-IDENT-BURST after that boundary (15,000,004 clocks). FT3: one that leaves on a ms's first clock is followed less than a tick later (15,100,002). FT4: a held button's next burst comes T-IDENT-REARM after the boundary following the first frame (100,000,004). `ident_burst_deadline_one_tick_short` (FT2: 14,900,004) and `ident_t0_same_ms` (FT4: 99,900,004) are KILLED. The suite's two builds take about 30 s |

### Parent-visible list, round 3

Round 3 adds no top port, no top parameter, no register and no module port. Nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0), and `parent-adoption-c4c6-ea3fb388.patch` is unchanged.

1. **`KL_aecp_notify` gains one flop, `prs_r`,** inside the identify generate: nothing at 0, one flip-flop at 1.
2. **The test wrap `tb/pp_top/pp_top_wrap.sv` gains three observe-only outputs** (`dbg_ident_gap_*`). They are test RTL inside the processor's suite; the parent's port-contract gate reads only `hdl/`.
3. **`tb/aecp_notify` builds twice** and its Makefile prints one summed tally, as `tb/pp_top`'s does.
4. **`notify_mutants.py` holds 40 controls** (34 at round 2), with one `tb/aecp_notify` suite target and one more tally shape. The combined patch's disposition entry covers the driver as a whole.

### Validation, round 3

Verilator 5.050 (the CI pin), builds capped at eight jobs, one heavy command at a time, every command on a `git archive` export of the head except the two marked as run in a clone at the head. Processor, every command at `9624ef4`:

| Command | rc | Result |
|---|---:|---|
| `./scripts/run_suites.sh` | 0 | UPC map gate PASS; 33 suites, 1,018,160 checks, 0 failing. `pp_top` 8,242 (default build 8,044, fixture 20, identify 178), `aecp_notify` 14 (10 + section FT 4) |
| `./scripts/lint_hdl.sh` | 0 | 41 modules; `KL_aecp_notify`, `KL_aecp_engine` and `protocol_processor_top` also lint clean at `EN_IDENTIFY_NOTIF_P` = 1 |
| `make check` | 0 | lint (41 mermaid + 18 wavedrom), WaveDrom, links (999), both matrices, parameters (27 = 27 = 27), stale |
| `python3 scripts/gen_matrix.py --check` | 0 | 94 rows, 0 untested |
| `./syn/yosys/run.sh` | 0 | 36 tops and the Xilinx memory-map check |
| `git diff --check 3f3ea56b..9624ef4`, `88e0bf8..9624ef4` | 0 | |

Mutation campaigns at `9624ef4` (each plants its defects in private copies):

| Command | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --jobs 1` (four `--only` chunks) | 0 | goldens pass; **40 of 40 KILLED** by their named checks (round 2's 34, re-anchored where item 1 names, and round 3's 6) |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | goldens pass; 19 of 19 KILLED |
| `make -C tb/adp_engine mutants` | 0 | 30 of 30 killed |
| `make -C tb/maap mutants` | 0 | 3 controls pass; 29 of 29 killed |
| `python3 tb/pp_top/gsi_mutants.py` | 0 | 20 of 20 detected; golden and restored pass |
| `python3 tb/acmp_talker/retry_mutants.py` | 0 | 62 killed; 7 equivalence and 1 performance controls retained |
| `make -C tb/nvm_port figures` | 0 | every measured figure agrees with the tree (run in a clone at the head: its provenance check reads git revisions an export does not carry) |
| `make -C tb/srp_top mutants` (in the clone) | 0 | 78 of 78 killed, assertion coverage 65/65 |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` (five `--only` chunks) | 0 | 83 of 83 killed; goldens pass in each chunk |

Both reviewers' probes, re-run unchanged at `9624ef4` (the arms ID8 and ID9 run before ID6, so section ID still ends with ID7 and their anchors apply):
- R420-2's `r420_probes.py`: RP2 (an 80 ms press 20 ms after the third frame) now sends its burst, 3 frames where round 2 sent none; RP1's second burst follows the third frame by 15,301 clocks; the stall and fan-out sweeps' smallest gap is 15,232 clocks. `hold_ignores_gap` is killed (ID3f, ID7r, ID8q, ID8r). `wait_ignores_gap` no longer applies: its anchor is round 2's WAITING start, and `ident_wait_ignores_gap` is the control on the new one. `burst_deadline_one_tick_short` still passes section ID, as expected on the compressed timebase, and is killed by `tb/aecp_notify` FT2.
- R421-2's `r421_arms.py`: R421c (a 30 ms press 2 ms after the third frame) and R421d (200 ms) each send the next burst 15,301 clocks after the third frame; R421a and R421b (eof-beat stalls) keep their gaps at 15,232 and 15,299 clocks. 188 checks, 0 failures.

Out-of-context cost (yosys 0.66 `synth_xilinx -family xc7 -flatten`, module `KL_aecp_notify`, the parameter set by `chparam`; no Vivado on this host): at 0 the head is round 2's exactly (1,721 FF, 249 CARRY4, 1,048 RAM32M, 6,523 LUT); at 1 the latch adds one flip-flop (1,788 FF against 1,787) and no carry. The whole top was not re-synthesised this round: at 0 nothing in it changed (the flop sits in a generate that is not built), so round 2's whole-top figures at 0 stand.

Parent consumer set (the 16 commands) at milan-fpga dev `ea3fb388`, in a scratch copy: a `git archive` of the trusted checkout with its submodules at their recorded pins and the processor at `9624ef4`. Its index equals the trusted checkout's except the processor gitlink. `parent-adoption-c4c6-ea3fb388.patch` applied on top, unchanged:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1 | `python3 scripts/check_cpp_idiom.py` | 0 | every ratchet within budget (multi-declarator 0 <= 0, long function 0 <= 0) |
| 2 | `python3 scripts/check_py_idiom.py` | 0 | every ratchet within budget (over-long line 0 <= 0) |
| 3 | `python3 scripts/check_rtl_source_lists.py` | 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded |
| 4 | `python3 scripts/pp_srcs.py --check --selftest` | 0 | OK |
| 5 | `python3 scripts/check_port_contracts.py` | 0 | processor 1,752 ports (as at round 2), undocumented 111 <= 111 |
| 6 | `python3 scripts/measure_naming.py --check` | 0 | 96 candidates, all recorded |
| 7 | `python3 scripts/measure_test_evidence.py --check` | 0 | 73 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8 | `python3 scripts/docs_check.py` | 0 | 0 findings |
| 9 | `python3 scripts/xvlog_gate.py --check` | 0 | 4 findings == ratchet, the same four keys |
| 10 | `python3 sw/builder/test_builder.py` | 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local mf48 build tree) |
| 11 | `python3 scripts/lint_rtl.py --check` | 0 | 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13 | `make -C tb/verilator/nvm_cosim lint` | 0 | pass |
| 14 | `make -C tb/verilator/nvm_cosim quick` | 0 | 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL (compile jobs bounded for memory; model parameters unchanged) |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 5 leg-defect arms caught |

### What remains, round 3

- Hosted CI on the PR, and the round-3 reviews.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged by this round) when it moves its processor pin past this head.
- Retained with their reasons in `tb/pp_top/README.md`, unchanged: R420-1 S1 (three controls that survive, with every section-ID check passing) and R420-1 S4 (the shared GET_COUNTERS limiter's one-tick reading).
- No hardware was used. The identify sequencer is graded in simulation only; the parent keeps the parameter at 0. The cost figures are yosys out of context; a Vivado out-of-context run at the parent is the authoritative figure.
- Unchanged from round 1: the optional overflow eviction sweep is not attempted (a recorded decision), and the solicited DEREGISTER that does not push is recorded, not changed.

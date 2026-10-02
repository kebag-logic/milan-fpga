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

Rounds 4 and 4b are merges only, under [Round 4](#round-4) (`main` `16ea10ac`, head `651839e`) and [Round 4b](#round-4b) (`main` `03c842a7`, head `95a78c0`). Neither changes the lane's behaviour. `tb/pp_top` now builds five times, and the lane's 09 section is §8.4.

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

This round's tables, verbatim with every figure, are in the archived round-4 body, section "Validation" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.

Verilator 5.050 (the CI pin), builds capped at eight jobs. Processor, every command at `5e80629`, all rc 0: `run_suites.sh` (33 suites, 1,017,309 checks; base `0451d83d` 1,017,162; `pp_top` 8,078: default 7,996 = the pre-lane 7,924 + ID0 3 + NP 47 + ST 18 + RN 4, fixture 20, identify 62; `originator` 107 = 104 + R 3; `ucpu` 396 = 386 + N6/N7 10), `lint_hdl.sh` (the three changed modules also at `EN_IDENTIFY_NOTIF_P` = 1), `make check`, `gen_matrix.py --check`, `syn/yosys/run.sh`, `git diff --check`. Campaigns: the new `notify_mutants.py` 30 of 30 KILLED (goldens pass); adp 30/30; srp_top 78/78 (coverage 65/65); gsi 20/20; retry 62; d3 83/83 (two chunks); the nvm_port figures agree.

Out-of-context cost (condition 1; yosys 0.66 `synth_xilinx -family xc7 -flatten` of the whole top, no Vivado on this host):

| Build | LUT | FF | CARRY4 | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|
| main `0451d83d` | 62,463 | 30,454 | 2,317 | 16 / 1 | 4 |
| head, parameter 0 | 62,783 | 30,454 | 2,317 | 16 / 1 | 4 |
| head, parameter 1 | 63,352 | 30,530 | 2,331 | 16 / 1 | 4 |

At 0 the flip-flop, carry, RAM and DSP counts are main's; the LUT difference is the mapper's variance between netlists proven equivalent (`KL_aecp_notify` alone maps 6,598 vs 8,002 LUT at the same 1,721 FF). The identify sequencer at 1 costs +76 FF, +14 CARRY4 and +569 LUT as mapped (dominated by the 165-bit uns-face mux).

Parent consumer set (the 16 commands) at milan-fpga dev `ccdd07b5`, in a scratch copy (git archive of the trusted checkout and its submodules, the processor at this head) with `parent-adaptation-132-c1.patch` and then the C6 adoption edits applied: all 16 rc 0 (port contracts: processor undocumented 111 <= 111; evidence ratchet 74 <= 77, 0 unexplained DUT readers; `pp_shadow` 295 checks; `test_builder.py` every gate but gate 11, which needs a local mf48 build tree). The latest round's section carries the full table.

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

This round's tables, verbatim with every figure, are in the archived round-4 body, section "Validation, round 2" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.

Verilator 5.050 (the CI pin), builds capped at eight jobs, one heavy command at a time. Processor, every command at `88e0bf8`, all rc 0: `run_suites.sh` (33 suites, 1,018,084 checks; `pp_top` 8,170: default 8,044, fixture 20, identify 106), `make -C tb/pp_top identify` (ID 106, ID0 3), `lint_hdl.sh` (also at `EN_IDENTIFY_NOTIF_P` = 1), `make check`, `gen_matrix.py --check`, `syn/yosys/run.sh` and `git diff --check`. Mutation campaigns, all rc 0, each in private copies: notify 34 of 34 KILLED (round 1's 30, re-anchored, and round 2's 4); acmp 19 of 19 (main's, #137); adp 30 of 30; maap 29 of 29 (main's, #135); gsi 20 of 20; the talker retry campaign 62; srp_top 78 of 78; d3 83 of 83 (a host reboot cut the whole-set run after 77 kills, and the other six ran at the same head in two chunks); the nvm_port figures agree.

Out-of-context cost (yosys 0.66: `sv2v` of the whole tree with the generated ROM images, then `synth_xilinx -family xc7 -flatten -top protocol_processor_top`, the parameter set by `chparam`; no Vivado on this host):

| Build | LUT | FF | CARRY4 | MUXF7 / MUXF8 | RAM32M / RAM64M | RAMB36 / RAMB18 | DSP48 |
|---|---:|---:|---:|---:|---:|---:|---:|
| main `3f3ea56` | 63,151 | 30,454 | 2,317 | 577 / 125 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, parameter 0 | 61,488 | 30,454 | 2,317 | 615 / 123 | 1,497 / 3 | 16 / 1 | 4 |
| head `88e0bf8`, parameter 1 | 63,283 | 30,533 | 2,339 | 659 / 190 | 1,497 / 3 | 16 / 1 | 4 |

- At 0 the FF, CARRY4, RAM and DSP counts are main's. The LUT count moves by mapper variance: main's own top maps 688 LUT more at `3f3ea56` than round 1 measured at `0451d83d`, at the same FF. This time the head at 0 maps 1,663 LUT fewer than main. At 0 round 2 adds only a constant-0 net that `KL_aecp_notify` never reads.
- The identify sequencer at 1 costs +79 FF and +22 CARRY4. Round 1 measured +76 FF and +14 CARRY4. The difference is round 2's schedule: three flops (`gap_r`, `left_r`, and the top's `busy_r`) and the 32-bit `now_ms_i + 151` deadline adder (8 CARRY4). The LUT figure, +1,795 as mapped, carries the same mapper variance.

Parent consumer set (the 16 commands) at milan-fpga dev `e4b771f9`, in a scratch copy with `parent-adoption-c6-e4b771f9.patch` (unchanged) and #137's documented `DUT_READER_DISPOSITIONS` line for `acmp_mutants.py` applied: all 16 rc 0 (evidence ratchet 73 <= 77; with the C6 patch alone, rc 1 on main's `acmp_mutants.py` only, as at `main` `3f3ea56` with no patch). At `2e99ab0`, commands 1 and 2 failed on round 2's test code. Item 5 above records those findings and their fix.

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

This round's tables, verbatim with every figure, are in the archived round-4 body, section "Validation, round 3" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.

Verilator 5.050 (the CI pin), builds capped at eight jobs, one heavy command at a time, every command on a `git archive` export of `9624ef4` (the nvm_port figures and srp_top campaign in a clone at the head), all rc 0: `run_suites.sh` (33 suites, 1,018,160 checks; `pp_top` 8,242: default 8,044, fixture 20, identify 178; `aecp_notify` 14), `lint_hdl.sh` (also at 1), `make check`, `gen_matrix.py --check`, `syn/yosys/run.sh`, `git diff --check`. Campaigns: notify **40 of 40 KILLED** (round 2's 34, re-anchored, and round 3's 6), acmp 19/19, adp 30/30, maap 29/29, gsi 20/20, retry 62, srp_top 78/78, d3 83/83; the nvm_port figures agree.

Both reviewers' probes, re-run unchanged at `9624ef4` (the arms ID8 and ID9 run before ID6, so section ID still ends with ID7 and their anchors apply):
- R420-2's `r420_probes.py`: RP2 (an 80 ms press 20 ms after the third frame) now sends its burst, 3 frames where round 2 sent none; RP1's second burst follows the third frame by 15,301 clocks; the stall and fan-out sweeps' smallest gap is 15,232 clocks. `hold_ignores_gap` is killed (ID3f, ID7r, ID8q, ID8r). `wait_ignores_gap` no longer applies: its anchor is round 2's WAITING start, and `ident_wait_ignores_gap` is the control on the new one. `burst_deadline_one_tick_short` still passes section ID, as expected on the compressed timebase, and is killed by `tb/aecp_notify` FT2.
- R421-2's `r421_arms.py`: R421c (a 30 ms press 2 ms after the third frame) and R421d (200 ms) each send the next burst 15,301 clocks after the third frame; R421a and R421b (eof-beat stalls) keep their gaps at 15,232 and 15,299 clocks. 188 checks, 0 failures.

Out-of-context cost (yosys 0.66 `synth_xilinx -family xc7 -flatten`, module `KL_aecp_notify`, the parameter set by `chparam`; no Vivado on this host): at 0 the head is round 2's exactly (1,721 FF, 249 CARRY4, 1,048 RAM32M, 6,523 LUT); at 1 the latch adds one flip-flop (1,788 FF against 1,787) and no carry. The whole top was not re-synthesised this round: at 0 nothing in it changed (the flop sits in a generate that is not built), so round 2's whole-top figures at 0 stand.

Parent consumer set (the 16 commands) at milan-fpga dev `ea3fb388`, in a scratch copy with the processor at `9624ef4` and `parent-adoption-c4c6-ea3fb388.patch` applied, unchanged: all 16 rc 0 (processor ports 1,752, undocumented 111 <= 111; evidence ratchet 73 <= 77).

### What remains, round 3

- Hosted CI on the PR, and the round-3 reviews.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged by this round) when it moves its processor pin past this head.
- Retained with their reasons in `tb/pp_top/README.md`, unchanged: R420-1 S1 (three controls that survive, with every section-ID check passing) and R420-1 S4 (the shared GET_COUNTERS limiter's one-tick reading).
- No hardware was used. The identify sequencer is graded in simulation only; the parent keeps the parameter at 0. The cost figures are yosys out of context; a Vivado out-of-context run at the parent is the authoritative figure.
- Unchanged from round 1: the optional overflow eviction sweep is not attempted (a recorded decision), and the solicited DEREGISTER that does not push is recorded, not changed.

## Round 4

Round 4 is a merge only, as assigned on #80 (comment 5939839032). R420-3 (comment 5939598551) and R421-3 (comment 5939832953) are both POSITIVE at `9624ef4`. Processor `main` moved to `16ea10ac` (#138, lane C5b, AECP dispatch). The merge is a merge commit (`--no-ff`), nothing is rebased, and nothing else changed. Head `651839e`.

| Commit | Item |
|---|---|
| `651839e` | 1. Merge `main` `16ea10ac` (#138), keeping both sides |

`git merge-tree --write-tree 16ea10ac 651839e` gives the head's own tree (`8599a8b0`), so the merge tree equals the head.

### 1. The merge of `main` `16ea10ac`

Main touched 60 files; 14 are shared with the lane. Ten merged with no textual conflict (six docs, the engine, the generator, the top and `tb/ucpu/sim_main.cpp`). Four conflicted, each resolved by keeping both sides:
- `tb/pp_top/Makefile`. Each side had taken the bench from two builds to three: the lane added the identify build, main added the line build (`DESC_LINE_BYTES_P` = 584) with `aecp-dispatch`, `line-build`, `aecp-line`, `aecp-dispatch-mutants` and `line-guards`. `make` now runs four builds: default, fixture, identify (third) and line (fourth). The tally requires four, and `clean` and `.PHONY` carry every target.
- `tb/pp_top/sim_main.cpp`. Both build arms are kept, with the union of the section flags (`--identify-only`, `--notify-only`, `--aecp-dispatch-only`). Main's section AX runs after AD, then the lane's ID0, NP, ST and RN, so main's order comes first and the lane's follows, as in round 2. Main's build line, which now names `DESC_LINE_BYTES_P`, is kept, and the comments say four builds.
- `tb/pp_top/pp_top_wrap.sv`. Both sets of observe-only taps are kept (the lane's three `dbg_ident_gap_*`, main's seven AX taps), and both `ifdef` parameter overrides.
- `tb/pp_top/README.md`. The `make` paragraph says four builds. Main's section AX comes first, then "Lane C6", each whole. In main's text, "the third build" for the line build becomes "the fourth", and section DV's build table gains the identify row.

`hdl.yml` and `.gitattributes` come from main alone, so its `aecp-dispatch-mutants` CI step is kept.

Three more edits were needed to keep both sides working. All three are in the merge commit:
1. **A ROM collision that the textual merge did not show.** The lane's unsolicited IDENTIFY_NOTIFICATION body (IEEE 1722.1-2021 §7.4.39.1, Figure 7-61) sat at ROM word 2000, and its unsolicited SET_STREAM_INFO body (§7.4.15.1, Figure 7-40) at 2016. Main put READ_DESCRIPTOR's current-value overlays at 2000 and 2024: `E_RDESCAU` and `E_RDESCCD` (§7.2.3, §7.2.32; #82). `gen_ucode.py`'s `place()` refused the merged file (`overlap at 2000`). Main's layout is kept. The lane's two bodies move together into main's free 456..511 run after `E_COPYT`: `E_IDNOTIF` to 464 and `E_SINFOUNS` to 480 (`hdl/aecp/ucode/gen_ucode.py:230-235`, `hdl/aecp/KL_aecp_engine.sv:895,897`, and the mirror in `tb/ucpu/sim_main.cpp:52-53`). Neither body branches, so neither depends on where it sits. The regenerated ROM equals main's word for word except those 27 words, and they equal the lane's bodies word for word. `check_upc_map.py` passes (60 engine constants, 88 entry points), and `tb/ucpu` N6/N7, `tb/pp_top` ID1 and NP3 grade both bodies byte-exact at their new addresses.
2. **`tb/pp_top/notify_mutants.py`'s tally pattern** (`:262`) accepts main's build line, which now carries `DESC_LINE_BYTES_P`. Without it, every `tb/pp_top` run would read as incomplete.
3. **`set_control_ignores_lock` re-anchored** (`notify_mutants.py:236-239`). For #53, main rewrote E_SCTRL so that every refusal carries the value in force (IEEE 1722.1-2021 §7.4.25.1). The found-control lock check is now `CHECK_LOCK ra=15, imm=SCTRL_EMIT`, and main's own `lk-sctrl-lock-nop.patch` plants the same NOP. The control turns that word into a NOP in place, as before, and RN still kills it.

Every other anchor holds on the merged tree, each found once (notify 43, d3 92, acmp 19; gsi 20 at their stated counts), and `git apply --check` is clean for every patch (aecp-dispatch 35, adp 28, maap 27, srp_top 73). The ROMs and tables were regenerated from their generators (`ucode.hex` 2048 words, 88 programs; the module matrix; WaveDrom); no tracked file changed.

### Parent-visible list, round 4

Round 4 adds no top port, no top parameter, no register and no module port. Nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0). `parent-adoption-c4c6-ea3fb388.patch` is unchanged (sha256 `67bcd698…7bd7c`).

1. **Two microprogram entry points move** (`E_IDNOTIF` 2000 to 464, `E_SINFOUNS` 2016 to 480). `KL_aecp_engine`'s `UPC_*_C` localparams follow them. These are internal constants, and the parent builds `ucode.hex` from the generator as before. At 0, `E_IDNOTIF` is never dispatched. `E_SINFOUNS` serves the SET_STREAM_INFO push, which is byte-identical (NP3).
2. **`tb/pp_top` builds four times**, and the lane's campaign reads the new build line. This is test code inside the processor's suite, and the combined patch's disposition covers `notify_mutants.py` as a whole.
3. Main's own C5b changes come in with the merge: the `DESC_LINE_BYTES_P` range refused at elaboration, the response buffer at exactly 16 + line, and the new `aecp_dispatch_mutants.py`, `line_guards.py` and `check_m9_opcodes.py`. They belong to #138, not to this lane. The parent consumer gates below pass with them and with the unchanged patch, and the test-evidence gate finds no unexplained DUT-source reader.

### Validation, round 4

This round's tables, verbatim with every figure, are in the archived round-4 body, section "Validation, round 4" ([full tables][c6-r1-r4-tables]). The paragraphs below condense them.

Verilator 5.050 (the CI pin), builds capped at eight jobs, and one heavy command at a time. Every processor command ran on a `git archive` export of `651839e`, except `make -C tb/nvm_port figures`, which reads pinned git revisions and ran in a scratch clone at `651839e`.

All rc 0: `run_suites.sh` (UPC map gate 60 constants, 88 entry points; M9 opcode gate 30 opcodes; 33 suites, 1,018,785 checks; `pp_top` 8,855: default 8,439, fixture 20, identify 178, line 218; `ucpu` 408), `lint_hdl.sh` (also at 1), `make check` (links 1,012), `gen_matrix.py --check`, `syn/yosys/run.sh`, `git diff --check`.

**No arm is lost.** Every section line of main's `tb/pp_top` run and of the lane head's appears in the merge's run, unchanged, and the merge has no section line of its own. The default build is main's 8,367 plus the lane's ID0 3, NP 47, ST 18 and RN 4, which gives 8,439. ID is 178 and AX 218 in their own builds, as on each side. `tb/ucpu` is the base's 386, plus main's 12 and the lane's 10, which gives 408.

Mutation campaigns at `651839e`, all rc 0, each in private copies: notify **40 of 40 KILLED** and aecp-dispatch **35 of 35**, every failing-check count equal to its README record; acmp 19/19; d3 83/83 (the 59 recorded pp_top counts unchanged); adp 30/30; maap 29/29; srp_top 78/78 (assertion coverage 65/65); gsi 20/20; retry 62; srp_admission 3 defects x 3 suites; name_wr 1; the nvm_port figures agree (in the clone).

Both reviewers' round-3 probes were re-run, unchanged, at `651839e`: R420-3's RP3a-RP3j (600 checks, 0 failures), its S1 boundary control and round-2 driver, and R421-3's round-2 arms (188 checks), 16 random-press campaigns, latch mutants and FT phase sweep. Every result is identical to the reviewer's own receipt at `9624ef4`; the only difference is the build line, which names main's `DESC_LINE_BYTES_P`.

Parent consumer set (the 16 commands) at milan-fpga dev `7f0927bb`, in a scratch copy (its 983-entry index equal to the trusted tree's except the processor gitlink, `651839e`) with `parent-adoption-c4c6-ea3fb388.patch` applied, unchanged: all 16 rc 0 (processor ports 1,752, undocumented 111 <= 111; evidence ratchet 72 <= 77, C5b's campaign arming one more suite; `milan_dp` 9 benches and the 6 + 6 mutant arms).

Cost: `KL_aecp_notify.sv` is round 3's byte for byte, so its out-of-context figures stand (one flip-flop at 1, none at 0); the ROM depth is unchanged.

### What remains, round 4

- Hosted CI on the PR, and the delta review of the merge.
- Processor `main` moved again after this round was assigned: `03c842a7` (#140, lane C5a, AECP deadlines, 18 commits past `16ea10ac`). This round merges `16ea10ac` only, as assigned. A merge of `03c842a7` is the manager's call.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged) when it moves its processor pin past this head.
- Retained, unchanged: R420-1 S1 and R420-1 S4 (recorded in `tb/pp_top/README.md`). Round 3's two SUGGESTIONs are not taken in this merge-only round: R420-3 S1 (a 1-clock press on the expiry edge; RP3j k = -2 still kills the reviewer's control at the merge) and R421-3 S1 (FT4 at phase 99,999; the sweep still holds there).
- No hardware was used. The identify sequencer is graded in simulation only, and the parent keeps the parameter at 0.

## Round 4b

Round 4b is a merge only, before the delta review, as assigned on #80 (comment 5944153047). Processor `main` moved to `03c842a7` (#140, lane C5a: the AECP transaction deadline and the hazard classes) while round 4 ran. The merge is a merge commit (`--no-ff`) on round 4's `651839e`; nothing is rebased, and nothing else changed. Head `95a78c0`. One delta review covers rounds 4 and 4b.

| Commit | Item |
|---|---|
| `95a78c0` | 1. Merge `main` `03c842a7` (#140), keeping both sides |

`git merge-tree --write-tree 03c842a7 95a78c0` gives the head's own tree (`d0be0f91`).

### 1. The merge of `main` `03c842a7`

C5a had merged `16ea10ac` too, so the merge base is round 4's main. Main touched 65 files. The six the assignment lists conflicted, and each keeps both sides:
- `tb/pp_top/Makefile`. Main added the timebase build (`PP_TOP_TIM_REAL`, `make budget`, section TB) and the `deadline`, `d3`, `hazards` and `aecp-mutants` targets; the lane has the identify build. `make` now runs **five builds**, numbered the same everywhere: default, fixture, identify (third), line (fourth), timebase (fifth). The tally requires five, and `clean` and `.PHONY` carry every target.
- `tb/pp_top/sim_main.cpp`. Main's DL, HZ and TB code comes before the lane's `notify_phases.hpp`. The flags are the union (`--deadline-only`, `--hazards-only`, `--identify-only`, `--notify-only`). The default build runs main's AX, DL and HZ, then the lane's ID0, NP, ST and RN: main's order first, as in rounds 2 and 4.
- `tb/pp_top/pp_top_wrap.sv`. Both sets of observe-only taps (the lane's three `dbg_ident_gap_*`, main's DL and HZ taps) and every `ifdef` override; the banner names all five builds.
- `tb/pp_top/README.md`. The `make` paragraph and section DV's build table say five builds. C5a's DL, HZ and TB sections and its `aecp_mutants.py` record stay whole beside "Lane C6".
- `tb/ucpu/sim_main.cpp`. Main's P19/P20 deadline-preempt checks, then the lane's N6/N7.
- `docs/architecture/09_verification.md`. Each side added a §8.3. Main's (the AECP deadline and the hazard classes) keeps its number, because six links anchor it (00, 03 twice, 06, 08 and 09 itself). The lane's notifications and identify evidence becomes §8.4, which nothing links.

Main's text called the timebase build "the fourth". It now says "the fifth" in the bench, the wrap, the README, 08 §4, 09 §8.3 and `aecp_mutants.py`, and the README's "`make` runs all three" (already stale on main) says all five. The lane's "third build" for section ID stands. `hdl.yml`, `.gitattributes`, `aecp_mutants.py` and its 42 patches come from main alone, so the C5a campaign and its CI step are kept.

**ROM words, checked beyond the text.** Every ROM was regenerated from its generator. C5a adds one microprogram, `E_DLKILL` at words 6..7 (03 §6 rule (e); it falls into `E_FAILSAFE`, IEEE 1722.1-2021 §9.3.2.6), and changes no other word. The merged `ucode.hex` (89 programs) equals main's except words 464..469 and 480..500, which hold the lane's `E_IDNOTIF` (§7.4.39.1, Figure 7-61) and `E_SINFOUNS` (§7.4.15.1, Figure 7-40) word for word. It equals round 4's except words 6..7. C5a's microcode does not use 464 or 480, so nothing moves. `check_upc_map.py` passes (61 engine constants, 89 entry points). `tb/ucpu` N6/N7, `tb/pp_top` ID1 and NP3 grade both bodies byte-exact where they are.

**No RTL edit.** The merge's `hdl/` change from round 4 is main's own change, and its change from main is round 4's (equal patch-ids both ways). Where the two sides meet, nothing needs a change. The deadline kill and the µCPU preempt never reach an unsolicited job (`dl_kill_r` and `dl_queued_o` are gated by `!uns_r`). An unsolicited job is loaded as an AEM response, so C5a's NOT_IMPLEMENTED echo for the other message types (IEEE Table 9-2) never applies to `E_IDNOTIF` or `E_SINFOUNS`. C5a's classifier gives a command-form IDENTIFY_NOTIFICATION, which the lane refuses with BAD_ARGUMENTS, RO_SNAPSHOT and the NONE key (03 §6 F03.7).

Every mutation anchor occurs once on the merged tree (notify 43, d3 92, acmp 19; gsi 20 at their stated counts). `git apply --check` is clean for every patch (C5a 42, aecp-dispatch 35, adp 28, maap 27, srp_top 73).

### Parent-visible list, round 4b

Round 4b adds no top port, no top parameter and no register. `git diff 651839e 95a78c0 -- hdl/top` declares no port or parameter (its one `input` line is an argument of C5a's `hz_key` function), and nothing changes at the parent's setting (`EN_IDENTIFY_NOTIF_P` = 0). `parent-adoption-c4c6-ea3fb388.patch` is unchanged (sha256 `67bcd698…7bd7c`).
1. **`tb/pp_top` builds five times.** `make -C tb/pp_top identify`, `--identify-only`, `--notify-only` and the build line `notify_mutants.py` reads are unchanged. This is test code inside the processor's suite.
2. **The lane's 09 section is now §8.4.** The parent cites none of 09's anchors.
3. **Main's own C5a changes come with the merge.** These are the deadline kill (internal ports `dl_kill_i` and `dl_queued_o` on `KL_aecp_engine`, `preempt_i`, `preempt_upc_i` and `preempted_o` on `KL_aecp_ucpu`), the classifier, `E_DLKILL`, the NOT_IMPLEMENTED echo for MVU and the other message types, and `aecp_mutants.py` with its CI step. They belong to #140. The parent's port-contract gate now counts 1,757 processor ports (1,752 at round 4: these five, each documented; undocumented 111 <= 111). The 16 consumer gates pass with them and the unchanged patch.

### Validation, round 4b

Verilator 5.050 (the CI pin), builds capped at eight jobs, and one heavy command at a time. Every processor command ran on a `git archive` export of `95a78c0`, except `make -C tb/nvm_port figures`, which reads pinned git revisions and ran in a scratch clone at `95a78c0`.

All rc 0: `run_suites.sh` (UPC map gate 61 engine constants, 89 entry points; M9 opcode gate 30 opcodes; 33 suites, **1,019,110 checks**, 0 failing; `pp_top` 9,151: default 8,679, fixture 20, identify 178, line 218, timebase 56; `ucpu` 437), `lint_hdl.sh` (41 modules; `KL_aecp_notify`, `KL_aecp_engine` and `protocol_processor_top` also at `EN_IDENTIFY_NOTIF_P` = 1), `make check` (links 1,035; parameters 27 = 27 = 27), `gen_matrix.py --check` (94 rows, 0 untested), `syn/yosys/run.sh` (36 tops and the Xilinx memory-map check) and `git diff --check` against both parents and the base.

**No arm is lost.** Every section line of main's `tb/pp_top` run and of round 4's appears in the merge's, unchanged, and the merge has none of its own:

| Build | main `03c842a7` | round 4 `651839e` | merge `95a78c0` |
|---|---:|---:|---:|
| default | 8,607 | 8,439 | 8,679 = main + ID0 3, NP 47, ST 18, RN 4 |
| fixture (DV) | 20 | 20 | 20 |
| identify (ID) | - | 178 | 178 |
| line (AX) | 218 | 218 | 218 |
| timebase (TB) | 56 | - | 56 |

`tb/ucpu` is `16ea10ac`'s 398, plus main's 29 (P19/P20) and the lane's 10 (N6/N7): 437.

Mutation campaigns at `95a78c0`, each in private copies, one at a time:

| Command | rc | Result |
|---|---:|---|
| `python3 tb/pp_top/notify_mutants.py --jobs 1` | 0 | five goldens pass; **40 of 40 KILLED**; every failing-check count equals the README record |
| `python3 tb/pp_top/aecp_mutants.py` (C5a) | 0 | five controls pass; **55 of 55 KILLED**; every count equals C5a's record |
| `python3 tb/pp_top/aecp_dispatch_mutants.py` | 0 | three controls pass; **35 of 35 KILLED**; every count equals the record |
| `python3 tb/pp_top/acmp_mutants.py --jobs 1` | 0 | goldens pass; **19 of 19 KILLED**; the pp_top counts equal the record |
| `python3 tb/pp_top/d3_mutants.py --jobs 1` | 0 | goldens pass; **83 of 83 KILLED**; all 71 recorded counts equal, C5a's two updated ones among them |
| `make -C tb/adp_engine mutants`, `tb/maap`, `tb/srp_top` | 0 | 30 of 30, 29 of 29, and 78 of 78 with assertion coverage 65/65; every control passes |
| `gsi_mutants.py`, `tb/acmp_talker/retry_mutants.py`, `tb/srp_admission/mutants.py`, `name_wr_mutant.py` | 0 | 20 of 20; 62 killed with 7 equivalence and 1 performance controls retained; 3 defects x 3 suites; the decode defect killed |
| `make -C tb/nvm_port figures` (in the clone) | 0 | every measured figure agrees with the tree |

Both reviewers' round-3 probes were re-run, unchanged, at `95a78c0`. Every result is identical to the reviewer's own receipt at `9624ef4`; the only difference is the build line, which names `DESC_LINE_BYTES_P`:
- R420-3. RP3a-RP3j: 600 checks, 0 failures. The S1 boundary control passes section ID (178/0), and RP3j k = -2 kills it. The round-2 driver gives the same six records (RP1 15,301 clocks, RP2 3 frames, smallest gap 15,232; `hold_ignores_gap` killed; `burst_deadline_one_tick_short` passes ID).
- R421-3. The round-2 arms: 188 checks, 0 failures. The seeded random-press probe: all 16 campaigns pass, with logs identical. The latch mutants: the same nine verdicts. The FT phase sweep: the same nine phases, both lower bounds holding.

Parent consumer set (the 16 commands) at milan-fpga dev `cdf49d1a`, in a scratch copy: a `git archive` of the trusted checkout with its submodules at their recorded pins and the processor at `95a78c0`. Its 984-entry index equals the trusted tree's except the processor gitlink. `parent-adoption-c4c6-ea3fb388.patch` is applied on top, unchanged (`git apply --check` clean), and the copy stayed clean after every gate:

| # | Command | rc | Result |
|---:|---|---:|---|
| 1, 2 | `check_cpp_idiom.py`, `check_py_idiom.py` | 0, 0 | every ratchet within budget |
| 3, 4 | `check_rtl_source_lists.py`, `pp_srcs.py --check --selftest` | 0, 0 | 107 files, 4 of 4 consumer lists; processor 36/42 tops, 6 recorded; OK |
| 5 | `check_port_contracts.py` | 0 | processor 1,757 ports (C5a's five), undocumented 111 <= 111 |
| 6, 7 | `measure_naming.py --check`, `measure_test_evidence.py --check` | 0, 0 | 96 candidates, all recorded; 72 <= 77, 10 <= 10, 0 <= 0 unexplained DUT readers, 3 <= 3 |
| 8, 9 | `docs_check.py`, `xvlog_gate.py --check` | 0, 0 | 0 findings; 4 findings == ratchet, the same four as round 4 |
| 10, 11 | `sw/builder/test_builder.py`, `lint_rtl.py --check` | 0, 0 | ALL GATES PASS EXCEPT 1 NOT RUN (gate 11 needs a local mf48 build tree, as before); 90 <= 90 |
| 12 | `make -C tb/verilator/pp_shadow -j8` | 0 | 311 checks, 0 failures |
| 13, 14 | `make -C tb/verilator/nvm_cosim lint`, `quick` | 0, 0 | pass; 315 of 315 |
| 15 | `make -C tb/verilator/milan_dp -j8 VERILATOR_JOBS=3` | 0 | 9 benches RESULT: PASS, 0 FAIL; the 6 + 6 mutant arms pass |
| 16 | `make -C tb/verilator/milan_dp_render -j8` | 0 | 65 + 152 checks, 0 failures; 5 of 5 leg-defect arms caught |

Cost: no RTL line of the lane changed in this round, so round 3's out-of-context figures for `KL_aecp_notify` stand. The ROM depth is unchanged (2048 words).

### What remains, round 4b

- Hosted CI on the PR, and the one delta review that covers rounds 4 and 4b.
- The parent adopts `parent-adoption-c4c6-ea3fb388.patch` (unchanged) when it moves its processor pin past this head.
- Retained, unchanged: R420-1 S1 and R420-1 S4 (`tb/pp_top/README.md`). Round 3's two SUGGESTIONs are still not taken in this merge-only round: R420-3 S1 (RP3j k = -2 still kills the reviewer's control) and R421-3 S1 (the sweep still holds at phase 99,999).
- No hardware was used. The identify sequencer is graded in simulation only, and the parent keeps the parameter at 0.

[c6-r1-r4-tables]: https://github.com/kebag-logic/milan-fpga/blob/ca50262850d156308a45ce5237e9adff64419f89/review-evidence/ppC6-r1/author-r4/PR-BODY.md


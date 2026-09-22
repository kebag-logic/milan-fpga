<!-- SPDX-License-Identifier: CERN-OHL-W-2.0 -->
# pp_top — the processor top, end-to-end wire truth

Builds `protocol_processor_top` (every landed module of the tree wired:
validator + replicated RX pools + normalizer + dispatch + ADP engine + ACMP
listener/talker + SRP engine behind `KL_mrp_strip` + TX pool/arbiter + the
ACMP Ethernet-prepend shim + timer/PRNG muxes + scoreboard, event router,
originator, trace ring, side port, NVM shadow + port) under `pp_top_wrap`
and drives it ONLY through the top's external contract: one MAC byte stream
in, one MAC byte stream out, the side-port host face, the SRP service face,
the NVM device face and the descriptor-image memory master. Time is compressed to 1 ms = 100 clk (the 89-slot
deadline sweep still fits a ms tick), so every window measured below is the
REAL timer/PRNG path.

Expectations are independent C++ builders/parsers from the doc byte
offsets — F04.5 ADPDU, F05.13 Milan ACMPDU, 802.1Q §10.8/§35.2.2 MRPDU BNF,
Milan §4.3.3.2 Σ-slope — never DUT logic.

`make`: exit 0 = PASS. It builds the bench twice (section DV): each executable
prints its own build's tally, and the last line sums both into the one canonical
tally.

## What it proves

- **A** **READ_DESCRIPTOR end to end** (06 §6.1, 07 §3.3) — the seam this
  suite used to stop at. A real AEM command on the MAC byte stream comes back
  as a byte-exact AECPDU carrying a descriptor that lives in MAIN MEMORY,
  fetched over the top's read-only memory master from a latency-injecting
  DRAM model (31-clock first-word latency, never zero):
  - **A1** ENTITY descriptor, whole 354-byte frame byte-exact against an
    independent IEEE §7.2.1 builder; command/response counters move once; and
    **exactly ONE memory burst per command** — the line buffer's whole purpose
    is that a descriptor costs one memory latency, not one per byte.
  - **A2** a bad `descriptor_index` and an unknown `descriptor_type` answer
    `NO_SUCH_DESCRIPTOR` with the 4-byte {type, index} stub of IEEE §7.4.5.
  - **A3** a bad `configuration_index` answers `BAD_ARGUMENTS` (06 §6.1), not
    `NO_SUCH_DESCRIPTOR`.
  - **A4** an 82-byte CLOCK_DOMAIN - a length that is NOT a multiple of 8, so
    `COPY_BUFFER` has to stop mid-lane; a whole-lane advance would put 6 bytes
    of the next descriptor on the wire and lie about `control_data_length`.
  - **A5/A6/A7** an unimplemented opcode answers `NOT_IMPLEMENTED` with the
    command ECHOED (F06.14 / IEEE §9.3.5.3.3) — never silence, never a
    malformed frame; IDENTIFY_NOTIFICATION as a COMMAND answers
    `BAD_ARGUMENTS` (IEEE §7.4.39.2 beats §9.3.5.3.3); a truncated
    READ_DESCRIPTOR answers `BAD_ARGUMENTS` rather than locating whatever
    followed the header.
  - **A5b** the NOT_IMPLEMENTED response is sized by ITS OWN command, swept
    over payloads of 0, 4, 8, 16 and 72 octets and two opcodes Table 7-140
    leaves unassigned: `control_data_length` is read off the wire (not
    compared to the builder, which would share any bug) and must be 12 + the
    command's payload, the echoed bytes are a non-zero pattern, and the frame
    is the padded 60 octets only where the payload is genuinely short. A5
    alone proves one 4-byte case, which a length stuck at 4 or a length held
    over from the previous command both survive. (An echo of ZEROS does not:
    A5 grades the echo byte for byte and catches it. An earlier revision of
    this list said otherwise.) A live Hive 4.3.1 session reported "Incorrect
    payload size" against exactly this class - see 06 §8.2 for who was right,
    which was us.
  - **A8/A9** a command addressed to another `entity_id` and an AECP RESPONSE
    arriving as input are both dropped and counted — answering a response is
    how a control plane builds a storm.
  - **A10/A11** three back-to-back commands each echo their own
    `sequence_id`; the snapshot window publishes the counters and image-valid.
- **N** **GET_NAME and SET_NAME end to end** (Milan v1.2 5.4.2.11/.12):
  every named slot in the fixture answers with cdl 84 and the exact 64 bytes
  carried by its descriptor. The sweep includes both ENTITY semantic indices,
  all other named descriptor types at index 0, and negative cases for an
  unnamed descriptor, an invalid semantic index, a missing descriptor, and a
  truncated command. Successful SET_NAME is followed by GET_NAME and
  READ_DESCRIPTOR for both offset-4 `object_name` and the ENTITY group name at
  offset 180. A foreign controller under lock receives `ENTITY_LOCKED` with
  the old current name, and the stored value remains unchanged.
- **M** **MVU GET_MILAN_INFO end to end** (Milan v1.2 §5.4.4.1) — the command a
  Milan controller sends FIRST, before a single descriptor, and the one whose
  answer decides whether it treats this device as a PAAD-AE at all. It is not
  an AEM opcode: §5.4.3.2 puts a 48-bit `protocol_id` at @22..@27 and the MVU
  `command_type` at @28..@29, so the field the 03 §4 record calls `opcode`
  holds the head of the protocol_id and nothing that names the command.
  - **M1/M2** the Figure 5.4 response byte-exact (44-byte AECPDU, cdl 32,
    message_type VENDOR_UNIQUE_RESPONSE, protocol_id intact), and the three
    fields decoded OFF THE WIRE: `protocol_version` 1 (§4.2.4),
    `features_flags` 0 and `certification_version` 0. The last two are checked
    by name because Table 5.20's REDUNDANCY would claim Milan §8 on a
    single-interface PAAD and TALKER_DYNAMIC_MAPPINGS_WHILE_RUNNING would claim
    map changes while a Stream Output is running, which the root integrator
    deliberately refuses.
  - **M3/M4** a FOREIGN vendor-unique protocol (same Avnu OUI-36, protocol id
    0x101) and an MVU `command_type` this build does not serve
    (GET_SYSTEM_UNIQUE_ID) both come back echoed with MVU status 1. M3 is what
    proves the whole 48 bits are compared: nothing above @26 tells the two
    protocols apart.
  - **M5** the r field is compared and the reserved field is not — §5.4.3.2.2
    requires r = 0 and gives the receiver no leave to ignore it, while
    §5.4.4.1's reserved field is explicitly "ignored by the receiver". So r = 1
    is echoed, and a junk reserved field still gets the real answer with a
    reserved field of 0.
  - **M6/M7** a truncated MVU command is echoed rather than answered from bytes
    nobody read; and a READ_DESCRIPTOR after the MVU traffic is still
    byte-exact, because Hive enumerating is worth more than the gap this closes.
- **Audio-map edit transaction**: ADD/REMOVE_AUDIO_MAPPINGS cover atomic
  validation and commit, duplicate-safe removal, static-port refusal,
  running-output refusal, state-changing success notifications with
  idempotent ADD kept silent,
  normalized Figure 7-71 responses, reserved-field clearing, timeout behavior
  after the phase-1 reservation point, and live scoreboard ownership. R19a
  parks MAP_CFG at the output streaming recheck, injects a state-changing
  source-1 PROBE_TX, proves the scoreboard hold is nonzero and the ACMP response
  and declaration edge are absent, then releases the map and grades both
  transactions in order. R21 grades the `aecp_nvm_stb_o` /
  `aecp_nvm_mark_o` export (issue #90) on this face and the name store: a
  committed ADD carries mark 6 and a committed SET_NAME mark 7, one strobe
  each, and the GET between them carries none — a mark has no wire shape, so
  the pin is the only place any of this is visible.
- **R** boot restore over a blank NVM device: all 8 BINDING regions read,
  `restore_done` without `restore_fail`.
- **S0/S1** quiescence + snapshot identity; SRP bring-up: the FIRST MSRP
  frame is the Domain default declaration `New {6,3,2}`, byte-exact.
- **S2** `DECLARE_TALKER` (svc face) → Σ-slope admission equals the
  independent Milan model (sum, granted, admitted, no over-limit) → Talker
  Advertise `New` AND MVRP VID `New` byte-exact on the MAC stream.
- **S3** entity enable → 82 B ENTITY_AVAILABLE byte-exact (aidx 0) inside
  the T-ADP-DELAY-START window; re-advertise with aidx 1 at the T-ADP-ADV
  5 s + 0-4 s anti-storm cadence.
- **S4** ENTITY_DISCOVER in → delayed byte-exact response at the running
  available_index; zero front-end drops.
- **S5** host face: ctrl scratch RW, status flags, firmware-window error
  when disabled, snapshot reads clean.
- **S6** BIND_RX in → byte-exact BIND_RX_RESPONSE; talker ENTITY_AVAILABLE
  in → discovery event through the router (trace-ring record checked via
  the host face) → byte-exact PROBE_TX_COMMAND inside the T-ACMP-DELAY
  window, Ethernet header prepended by the top (lane 2 shim).
- **S7** TX interleave: ADP response + ACMP GET_RX_STATE response + SRP
  Talker Advertise pushed together — each frame byte-exact and whole, all
  three arbiter lanes take grants.
- **S8** certified two-class Domain arrival (FirstValue {5,2,5}, nov 2)
  adopts {3,5} and re-declares `Lv{6,3,2}+New{6,3,5}` byte-exact; listener
  READY end-to-end (class-D snapshot + Listener Ready `New` byte-exact +
  TK_ATTR_REGISTERED trace record).
- **S9** the S6 binding commits through the debounced NVM shadow: framed
  F07.8 record (magic 0x1722) carrying the bound talker EID at the device
  face, and the `nvm_unflushed_o` export (issue #90) sampled every cycle
  across it — the sink reads unflushed while the change waits, and 0 once
  the commit reports done.
- **S10** the `maap` face (02 §4.2), which the top publishes because 01 §3
  puts address allocation in the integrating fabric. Run in two halves. With
  NO allocator (`maap_req_ready_i` 0 for the whole run above): the port is
  seen OFFERING requests, nothing is accepted, `acmp_declaring_o` is 0, and —
  the regression — a GET_TX_STATE_COMMAND is still answered byte-exact, plus
  a PROBE_TX answered byte-exact TALKER_DEST_MAC_FAILED. Before the accept
  window existed, one unaccepted allocation parked the single talker walker
  forever and neither answer ever came. With the allocator on: the ALLOC_DA
  is accepted for source 0, `acmp_declaring_o[0]` is observed rising 0 -> 1,
  the granted address is what the next GET_TX_STATE_RESPONSE carries, and the
  same address appears as the dest MAC of the Talker Advertise on the MSRP
  wire — MAAP -> DA gate -> ACMP answer -> SRP declaration, end to end.
- **V** **GET_AVB_INFO / GET_AS_PATH and their Table 5.22 triggers**: both
  solicited responses are byte-exact over the integrator-owned gather face;
  missing descriptors and truncated commands fail with the required status;
  a GM identity publish raises the independent AVB-info and AS-path strobes
  and produces both pushes; a PathTrace-tail publish produces only
  `GET_AS_PATH`; another AVB-info-word change produces only `GET_AVB_INFO`;
  and `gm_change_i` alone produces only `GET_AVB_INFO`, because the same ADP
  duty also covers a domain-only change whose path sequence did not move.
- **DV** **the Domain default is the top's `SRP_DOM_DEF_VID_P`** (issue #95;
  10 §6.1 F10.2, F01.5 `P-SRP-DOM-DEF-VID`), in both builds on a fresh model:
  the reset value, the LINK_UP declaration byte-exact with all 16 bits of
  SRclassVID, the GET_TX_STATE stream VLAN, a bridge's Domain still adopted
  over it, the LINK_DOWN revert and the LINK_UP re-declaration. See section DV.

## Snapshot window map (side port 0x20000, implemented by the top)

The map moved out of this file. It is a product contract, not a testbench note, and it is
now maintained word by word and bit by bit in the
[operator guide](../../docs/guides/operator.md#5-the-snapshot-window-word-by-word), with
the window list in [07 §5.5](../../docs/architecture/07_memory_maps.md). This suite reads
words 0, 3, 32, 33 and 34 as part of scenarios S5 and A11, and words 35 and 36 in B6
through B9.

Trace window 0x40000: record = 4 words, lane 0 = now_ms, lane 1 =
{source, flags, payload} (event-router consumer glue).

## Mutation record (backup / sed / run / restore)

| # | what was broken | result |
|---|---|---|
| M1 | `KL_mrp_strip` strips 13 bytes instead of 14 (`body_w` compare 4'd14→4'd13) | 9 FAIL — S8 Domain adoption, listener READY, class-D: the SRP RX seam is load-bearing |
| M2 | ACMP prepend shim EtherType 0x22F0→0x22F1 | 8 FAIL — S6/S7 every ACMP wire check: the prepended header is what the wire sees |
| M3 | steer prefetch reads the addressed EID at PDU offset 27 instead of 28 | 16 FAIL — S6/S7/S9 the listener silently ignores mis-addressed heads (and the binding never commits): the target_eid rewrite is the real multicast discriminator |
| M4 | `KL_acmp_talker` S_EV_MAAP loses its timeout exit (the deadlock restored) | 5 FAIL — S10: with no allocator the talker walker never consumes another command, so neither ACMP answer reaches the wire |
| M5 | the top re-ties `.maap_req_ready_i (1'b0)` on the talker instance | 6 FAIL — S10: no grant, no gate, no declared DA on the SRP wire. The port is load-bearing, not decoration |
| M6 | `KL_aecp_dyn_state` drops the SEL_CFG write (`cfg_r` assignment removed) | 8 FAIL -- W17j, W18c, W18d3, W18f, W18g, W19a, W19g3, W19h: the configuration overlay is observed end to end. The W22 block passes under this mutation by construction: its echo is command-sourced and its expected 0 equals both the reset value and the image default. W22 exists for two other properties: a SUCCESS-arm refusal predicate stuck after W21u's unbind (W22a) and a lost later write against W18's residue of 1 (W22d) |
| M7 | the engine's SET_STREAM_FORMAT running route forced dead (`run_this_w` arm to `1'b0`) | 2 FAIL -- W23h + W23h2: the per-descriptor STREAM_IS_RUNNING refusal against a REALLY bound sink, and the write its absence lets through |
| M8 | the verdict requirement dropped (E_SFMTI/E_SFMTO `MOVE r4, 3` to `MOVE r4, 0`) | 8 FAIL -- both refusal rows (W23c/W23c2 unsupported, W23d shrink) AND the success rows (W23a/W23a2/W23b, W23h/W23h2 -- the latter as collateral: their expected bodies ride W23a.s write through the fold): CHECK_ARG.s comparator is load-bearing in both directions, not a tautology |
| M9 | the engine's SET_STREAM_INFO flag gate forced open (the SIF_ACC_LAT compare to `1'b0`) | 3 FAIL -- W24d/W24e, and W24f collaterally because the extra-flag command's write now lands: nothing is partially applied is a checked property |
| M10 | E_SINFO's WRITE_ST replaced with NOP | 4 FAIL -- W24a2/W24b (the published row and the folded GET), W24d/W24f (rows that assert the value survived refusals). W24a's byte-exact echo PASSES under this mutation -- the echo cannot see a dropped write, which is exactly why the face checks exist |
| M11 | the engine's SET_STREAM_INFO running route forced dead | 2 FAIL -- W25b + W25b2 against a REALLY streaming output (Advertise + registered Listener on the wire) |
| M12 | restored the pre-fix `.ev_asp_i (gm_change_i || gsi_asp_chg_i)` wiring | 1 FAIL at 1,269 checks — V6i: `gm_change_i` alone emits the forbidden `GET_AS_PATH`; the positive simultaneous-strobe arm stays live |
| M13 | tied `.ev_asp_i` to zero | 5 FAIL at 1,269 checks — V6/V6c/V6d lose both GM-entry and tail-only `GET_AS_PATH`; V6f/V6h fail collaterally because the missing frame shifts the per-controller sequence IDs |
| M14 | E_SCLKS+7 (ROM word 1191, the image read that supplies the CURRENT index while the clock-source row is unset) replaced with NOP, in a review copy of `gen_ucode.py`; the ROM is swapped, the tracked generator is not touched | 1 FAIL at 1,300 checks -- W10i2: the refusal on the unset row answers the zero r6 preload instead of the image's 1. W10i (BAD_ARGUMENTS at cdl 20), W10i4 (GET still reads the image) and every W10j effect count PASS under this mutation, which is why W10i exists: no set-row arm (W10f) can see this word |
| M15 | the ROM `gen_ucode.py` generated at 2faa5af8, the last commit before the range check (31 words differ, 1185 to 1215) | 20 FAIL at 1,300 checks -- W10e and W10f for both refused values, W10h, W10i/W10i2/W10i4, and the effect grades of W10j: the refusal of 3 is stored and marked (W10j2, W10j4, W10j5), the refusal of 65535 is stored, marked, enqueued AND announced at the second controller (W10j2 to W10j6), and the accepted SET that follows carries the residue in its counts and in its notification sequence (W10j8, W10j10 to W10j12) |
| M16 | E_SCLKS+19 (ROM word 1203, the BUILD_FLD that puts the stored index, r12, at @28 of the success response) rewritten to build r6, the CURRENT index read before the write, in a review copy of `gen_ucode.py`; the same shape as the refusal tail nine words later, so a refactor that shares that tail produces it. The ROM is swapped, the tracked generator is not touched | 2 FAIL at 1,300 checks -- W10j7b: the accepted SET from the unset row answers 0, the index it replaced, not the 1 it stored; W10b: the SET on the set row answers 1, not the 2 it stored. Every other check PASSES, W10j8 included: the engine rebuilds the unsolicited copy from the stored row through GET_CLOCK_SOURCE's program, not from the response, so only the response body can see this word, and only when the SET changes the index; which is why W10j stores 1 and W10 then stores 2 |
| M17 | `KL_acmp_talker` keys REGISTERING_FAILED on the retired private code 3 again (`rf_live_w` compares `srp_pkg::srp_decl_e'(2'd3)`, the pre-fix `LSN_ASKING_FAILED_C`), in a copy of the tree | 5 FAIL at 1,316 checks -- T2 and T3 for Asking Failed (flags 0x0000) and for Ready Failed (flags 0x0040), and T5. The same five failures are the reproduction of issue #46 at `2ccb427`, before the fix |
| M18 | `srp_pkg::srp_decl_e` swaps ASKING_FAILED and READY_FAILED (1 and 3), in a copy of the tree | the same 5 FAIL at 1,316 checks, and nothing else in this suite: the decoder publishes the wire code and the top's streaming reduction tests bit 1. The SRP engine's own readers of the package move too (the talker FSM's ACTIVE term, the listener FSM's declaration), but this suite never grades them against an Asking Failed; `srp_stream_fsms` (4) and `srp_top` (1) do, and fail under the same mutation, as does `acmp_talker` (3) |
| M19 | THE LIST CHECK REMOVED: E_SSRATE+13 (ROM word 1165) `BRANCH E_SSRWALK` rewritten to `BRANCH SSR_ACCEPT`, so no rate is ever looked up, in a review copy of `gen_ucode.py`; the ROM is swapped, the tracked generator is not touched | 28 FAIL at 1,361 checks, the same 28 as M24: W9i/W9i2 (44100 answered SUCCESS on the unset row and read back), W9j/W9j2 (192000 stored on the set row), W11e (collateral: W9j's 192000 is still in the row), W9k2-W9k6 for all three refused values (each stored, marked and announced to the second controller), W9k8 and W9k10-W9k12 (the accepted SET carries the residue in its counts and its notification sequence), W9l2, W9l5, W9l6, W9m5 |
| M20 | the count bound removed: the walk's two `BR_STATUS` per lane that leave on `count == k` replaced with NOP (E_SSRWALK+1, +7, +11, +17, +21, +27, +31, +37) | 10 FAIL at 1,361 checks -- W9k2-W9k6 for the zero rate, which the walk now "finds" in the lane past the 152-byte descriptor, and the residue it leaves in W9k8 and W9k10-W9k12; W9l2: with the count patched to 1, entry 1's 96000 is accepted |
| M21 | the offset check removed: E_SSRATE+12 (ROM word 1164, the `CHECK_ARG` of `sampling_rates_offset` against 144) replaced with NOP | 1 FAIL at 1,361 checks -- W9l6: with the offset patched to 148 the walk still reads the list at 144 and accepts 48000. Nothing else can see this word, which is why W9l patches the offset |
| M22 | the refusal tail builds r12, the REJECTED rate, at @28 instead of r6, the current one (E_SSRATE+17, ROM word 1169) | 9 FAIL at 1,361 checks -- every refusal that is graded byte-exact: W9i, W9j, W9k2 three times, W9l2, W9l5, W9l6, W9m5. Status, GET and every effect count PASS under it |
| M23 | the unset row's image read removed: E_SSRATE+6 (ROM word 1158, `SHIFT_R` of the image's current_sampling_rate into r6) replaced with NOP, so r6 keeps its zero preload | 1 FAIL at 1,361 checks -- W9i: the refusal on the unset row carries 0 instead of the image's 96000. Every set-row arm reads the dynamic row instead and PASSES, which is why W9i runs before W9 |
| M24 | the ROM `gen_ucode.py` generates at `6a9a124`, the last commit before the list check (the issue #51 reproduction with the final harness) | 28 FAIL at 1,361 checks, the M19 list |
| M25 | the top's `.DOM_DEF_VID_P (SRP_DOM_DEF_VID_P)` binding line removed | fixture build 13 FAIL of 20: every value check of DV1 to DV6. The default build PASSES all 1,391, which is why the fixture build exists |
| M26 | the binding misbound to a literal, `.DOM_DEF_VID_P (16'd2)` | fixture build 13 FAIL of 20, the M25 set |
| M27 | the binding truncated to 12 bits, `.DOM_DEF_VID_P (16'(SRP_DOM_DEF_VID_P[11:0]))` | fixture build 4 FAIL of 20: DV2 (byte-exact and the decoded SRclassVID), DV4 and DV6, the checks that read the 16-bit wire field. Every 12-bit face PASSES |
| M28 | the value bound to the wrong child parameter, `.DOM_DEF_PRIO_P (SRP_DOM_DEF_VID_P[7:0])`, the VID left unbound | default build 16 FAIL of 1,391 (S1 twice, S2, S7, S8 and 11 in DV); fixture build 13 FAIL of 20 |
| M29 | the top's own default changed from 2 to 3 | default build 18 FAIL of 1,391 (S1 twice, S8, T0, MP3 and 13 in DV). The fixture build PASSES 20 of 20, because it overrides the default |
| M30 | the wrap's fixture override removed (test infrastructure) | fixture build 13 FAIL of 20: the build cannot pass on the top's or the child's own default |
| M31 | control, not a defect: `KL_srp_top`'s own `DOM_DEF_VID_P` default changed from 2 to 7, binding intact | both builds PASS, 1,391 and 20: the child's default is no longer a source |

All twenty-four bite; originals restored; suite back to green. The M1-M6 counts were
taken when the suite stood at 86 checks (scenario A and section B have since
been added) and the M7-M11 counts at 1,139, so re-run a mutation before quoting
its blast radius. M12-M13 were measured at 1,269 checks, M14-M16 at 1,300,
M17-M18 at 1,316, M19-M24 at 1,361. M14 to M16 and M19 to M24
are ROM swaps (`ucode.hex` is read at simulation start), so they need no
rebuild: generate the review ROM elsewhere, copy it over `ucode.hex`, run
`./obj_dir/Vpp_top_sim`, and put the generated ROM back. Only its sha256 against
the generator's output proves the ROM is the pinned one again: a copied ROM is
newer than `gen_ucode.py`, so `make` alone leaves it in place, and `git status`
cannot see it (`ucode.hex` is ignored); `rm ucode.hex && make` regenerates it.
M25 to M31 were measured on 2026-09-22 at 1,391 checks in the default build and
20 in the fixture build, each in its own scratch copy of `hdl/` and `tb/pp_top/`,
so there was nothing to restore. M25 to M30 bite; M31, a control, stays green as
it must.

## Recorded seams and honest limits

- The validator's V9 pass-through has NO msrp/mvrp select — `KL_mrp_strip`
  derives it from the EtherType bytes it strips (V9 already enforced the
  DA/EtherType pairing).
- The validator's F03.4 `target_eid` for ACMP is the @4 stream_id; both
  ACMP engines discriminate on the ADDRESSED entity id — the top's steer
  prefetch rewrites the head from the slot bytes (doc conflict reported;
  03 §4 says only "as applicable").
- S6 allows the probe to RACE the trace record: a short bind-armed
  T-ACMP-DELAY draw can put the probe on the wire around the discovery
  walk, so the trace check polls a bounded 500 ms window instead of
  reading once.
- MSRP byte-exact checks run under `la_guard()`: the PRNG-drawn 10-15 s
  LeaveAll would otherwise fold the expected vector into an LA PDU. The
  MVRP byte-exact check runs early (before the first LeaveAll) because an
  idle MVRP participant latches an expired LeaveAll until its next tx
  opportunity — there is no clean later window by construction.
- The AECP pop face is still exposed and still tied `ready = 0` here: the
  AECP head is now drained by `KL_aecp_engine` INSIDE the top, and the port
  is an additional, optional consumer (see its banner).
- Scenario A is the only one that touches the descriptor memory. The image is
  loaded into the DRAM model BEFORE reset, exactly as software does before
  `entity_enable`; the "software has not loaded it" and "no bridge at all"
  arms live in the `desc_store` suite, which owns that face.
- The `A` expectations are byte builders from the IEEE §9.3.1 AECPDU and
  §7.2 descriptor field offsets plus the documented image layout — nothing in
  them comes from the DUT or from `gen_desc_image.py`'s output.
- The S10 allocator is a harness model of the 02 §4.2 op semantics only
  (accept a request, answer once, hand back an address). It proves the FACE
  and the address flow through this processor — never MAAP itself: the
  probe/defend/announce state machine of IEEE 1722 Annex B lives in the
  integrating fabric, outside this repo.
- The NVM device model is blank flash (reads answer 0xFF): a record failing
  the F07.8 magic/layout check is SKIPPED by the shadow, which is the
  documented no-saved-binding path. Torn-stream restore aborts are covered
  by the `acmp_nvm` suite, not here.
- The wrap exposes observe-only cross-module taps (`dbg_*`) used during
  bring-up; the checks themselves read only wire frames + the host face.

## Section B — the response buffer lives in main memory (03 §7.1)

The 592-byte AECP response buffer is no longer fabric state; it is
`KL_aecp_resp_buf` over the `resp_mem_*` master, and the model behind that
master injects **non-zero latency on both channels by default** (23 clocks
read, 17 write). B1 demands one read burst and exactly the lane writes the
write pattern implies; B2 compares the payload on the wire against the model's
own memory image, not against the DUT's account of it; B3 proves a byte whose
write strobe is 0 is never modified; B4/B4b measure the whole path — MAC
command byte 0 to MAC response byte 0 — and check it against the IEEE §9.2.1.1
100 ms budget (10,000,000 clocks at `P-CLK-HZ`), once at the suite's latency
and once at the reference SoC's measured ~1424 ns (143 clocks) per access;
B5 proves an echoed payload costs the response memory **nothing** (it comes
straight out of the RX slot); B6–B9 tie the master off, fail its writes and
fail its reads, and demand a well-formed 60-byte `ENTITY_MISBEHAVING` answer
plus the counters and the snapshot window that name the fault; B10 demands the
slot pools back afterwards; B11 proves a four-times-slower bridge only costs
time.

## Mutation-proven 2026-08-13 (scenario A)

| Break | Went red |
|---|---|
| `COPY_BUFFER` advances by the whole 8-byte lane instead of the residual | **10** red |
| response buffer places fields little-endian instead of big-endian | **8** red |
| unimplemented opcodes fall through to the READ_DESCRIPTOR µprogram | **1** red |
| the frame builder ignores whether the payload byte has arrived from memory yet | **58** red |

## Mutation-proven 2026-08-14 (A5b, response sizing)

| Break | Went red |
|---|---|
| `control_data_length` pinned at 16 (12 + 4) instead of 12 + payload | **23** red, **8** of them A5b |
| the echoed payload capped at 8 octets, with `control_data_length` following it down | **5** red, **all** A5b |

The second one is the result that justifies the block. It produces an
INTERNALLY CONSISTENT frame (the length field matches the bytes actually
emitted, and it still pads to 60), so every pre-existing check stays green:
before A5b the suite could not tell a response sized by its command from one
sized by something else, which is precisely what a controller complains about.
The first row also leaves A5 itself green, because 16 is the right answer for
the one 4-byte payload A5 sends.

## Mutation-proven 2026-08-14 (M, GET_MILAN_INFO)

| Break | Went red |
|---|---|
| `MILAN_PROTOCOL_VERSION` 1 -> 2 in `gen_ucode.py` | **3** red (M1, M2, M5b) |
| `MILAN_FEATURES_FLAGS` 0 -> 0x2, claiming a feature this build cannot serve | **3** red (M1, M2, M5b) |
| the protocol_id tail compare (@26..@27) dropped from the sub-decode | **1** red, M3 |
| the MVU `command_type` compare dropped from the sub-decode | **2** red, M4 and M5 |
| the Figure 5.3 length guard dropped (`pld_cmd_r >= 8` -> `>= 0`) | **1** red, M6 |

Every one of these produces a WELL-FORMED frame of the right length — the first
two are a correct Figure 5.4 response carrying a false claim, and the last three
answer SUCCESS to a command that was never GET_MILAN_INFO. None of them is
visible to a check that only counts bytes, which is why M2 decodes the three
fields by name and M3 uses a protocol id that differs from MVU's in its last
16 bits alone.

The `COPY_BUFFER` one is the interesting result: it goes red HERE and stays
green in `tb/ucpu` (0 checks red there), because that suite's µprogram only copies a
whole number of 8-byte lanes. A descriptor whose length is not a multiple of 8
is a thing only the end-to-end suite sees.

## Section K — GET_COUNTERS (06 §6.6; IEEE §7.4.42, Milan §5.4.2.25)

The harness plays the **integrator's counter store**, never the DUT's: it decides
what a quadlet means and which of them exist, and the suite then demands the
processor carry that answer onto the wire unchanged. Two masks on purpose —
`0x00000FFF` for an AAF sink that keeps the tv-bit tallies, Milan v1.2 Table
5.16's `0x00000F3F` for a CRF Media Clock Input that does not, and Milan Table
5.17's compact `0x0000001F` for a Stream Output. A processor that substituted a
mask of its own would therefore be caught. The store holds every beat for two
cycles by default, because a face that answers in the same cycle never exercises
the hold.

K1 demands the byte-exact 174-byte frame (Figure 7-67's block runs to byte 156,
so the AECPDU is 160 and `control_data_length` 148 — a short one is what Hive
4.3.1 reports as "Incorrect payload size"); K2 demands the Milan mandatory set
la_avdecc gates the badge on; K3 asks for STREAM_INPUT **1** and demands a
different object's answer, which is the whole point of reading `descriptor_index`
from @26 rather than @30, and demands zero bytes behind a clear mask bit; K4
demands SUCCESS with an EMPTY mask and a full-size block for ENTITY; K5 makes a
truncated command `BAD_ARGUMENTS`; K6 runs the same command at zero hold and at
an 11-cycle hold per quadlet and demands identical bytes; K7 wedges the store
outright and demands a bounded `ENTITY_MISBEHAVING` **and a working
READ_DESCRIPTOR immediately afterwards**; K8 demands the store be asked for the
mask and then quadlets 0..31 in order, consecutive repeats folded away — a
repeat under back-pressure is free, an index that MOVES under it is a lost beat.

| Break | Went red |
|---|---|
| `descriptor_index` read at the READ_DESCRIPTOR offset instead of §7.4.42.1's @26 | **3** red |
| the block stops after 12 quadlets instead of 32 | **9** red |
| a voided response is still sealed with its intended payload length | **2** red |
| the counters-face watchdog never fires | **5** red |
| `counters_valid` is a constant `0xFFF` instead of what the store returns | **6** red |

The last one is the one worth keeping: it is the advertised-zero lie in its
purest form — a full mask over a block the fabric never fills — and it must not
be able to pass.

## Section W8: GET_DYNAMIC_INFO

The suite sends `0x004B` through the complete MAC, RX slot, dispatch, AECP
engine, response memory, and TX path. Its expected bytes are built from the
standard's record layout and the harness models, not from standalone DUT
responses.

W8 covers implemented getters including full GET_NAME records in one byte-exact
aggregate, a missing
descriptor that changes only one record status, whole-command `BAD_ARGUMENTS`
for a forbidden `GET_AUDIO_MAP` with proof that no earlier record reached the
descriptor store, silent overflow omission followed by successful processing
of a later record, the Milan 56-byte `GET_STREAM_INFO` body, and
record-level `NOT_SUPPORTED` with exact command-data copy for a permitted but
unimplemented getter. It also covers an empty batch, truncated and
overrunning records, per-record `BAD_ARGUMENTS` for a non-SUCCESS command
status, preservation of the full 16-bit record command discriminator, every
member of the exact 13-command whitelist, retention at the exact cdl 524
response boundary, and rejection of an oversized cdl 525 command before record
processing. The batch-only falsifiers use distinct overflow targets,
non-zero unsupported data, a non-zero image configuration, full-body
wrong-target refusals, and sampling-rate image hits both before another record
and at the end of the aggregate. The final hit also verifies that the word
after its four-byte body remains untouched.

## Section U10: controller availability monitor

U10 verifies the full registered-controller liveness path through the real
timer, PRNG, frame builder, inflight tracker, TX slot pool, serializer, and RX
validator. It checks the independent 30 to 60 second draw, exact one-time retry,
targeted deregistration after silence, any-status response rearm, sequence
advancement across row reuse, and valid-command cancellation.

The cancellation case interrupts a CONTROLLER_AVAILABLE frame during allocation
or construction, then requires a solicited response to pass through the same TX
writer, the writer lock to return idle, and all five TX slots to be free. The
response-match cases inject both a colliding MAC fold and a correct MAC carrying
the wrong target Entity ID. Neither may suppress the exact retry.

The queue-delay case stalls a solicited response in the serializer, waits for a
CONTROLLER_AVAILABLE handle to queue behind it for longer than two response
budgets, and proves that no attempt timeout starts before serializer acceptance.
A valid command then cancels the queued exchange. The stale handle must drain,
both solicited responses must resume, and all five TX slots must return free.

## Section U11: non-head cancellation

U11 stalls the serializer until two independent controller probes occupy the
originator queue. It cancels the controller owning the second handle and
requires the queue to compact immediately, before the released physical slot
can be reused. Cleanup commands then prove that no queued or inflight exchange
survives and that all five shared TX slots return free.

## Section T: GET_TX_STATE against a registered Listener (issue #46)

Milan §5.5.4.3 sets REGISTERING_FAILED (0x0040) in a GET_TX_STATE_RESPONSE iff
the talker is registering a Listener Asking Failed attribute for the stream.
`acmp_talker` grades that flag against a code its own harness drives; this is
the one place the code comes from the SRP engine registering a real inbound
MRPDU, so it is the one place the talker and the engine can disagree about
what the code means. They did: the talker keyed on 3, which the engine
publishes for Ready Failed (`srp_pkg::srp_decl_e`, 02 F02.10).

T0 re-pings source 0 and requires its PROBE_TX answer and its Talker Advertise
back. T1 to T4 then register, by MRPDU exactly as W17b does, Asking Failed,
Ready Failed and Ready in turn: each arm checks the code the engine published
(snapshot word 13), grades the GET_TX_STATE_RESPONSE byte-exact and its flags
word alone (0x0040, 0, 0), and the Asking Failed arm asks source 1 too, which
must answer flags 0. T5 to T7 prove the flag is read live in both directions:
Asking Failed after Ready sets it again, and the Listener leaving clears it.

It runs on the main DUT after U11, not beside W17b, on purpose. S10's
PROBE_TX is the only ping source 0 gets, and W21 to W25 lean on that
T-SRP-DAFRESH window still being open: the same arms placed after W17b took
about 1.7 s of simulated time and moved the window's lapse into W21t2 and
W25pre, which then failed for a reason that has nothing to do with them. At
the end of the run two response fields have moved since S10, and neither is
read from the talker: the DA is the one the bench's own allocator model last
granted source 0 (`maap_src_da`), and the VID is the SR-class level on
snapshot word 10, because the S8 Domain registration has aged out under the
processor's own LeaveAll and the bench never re-declares it.

## Section W9i-W9m: SET_SAMPLING_RATE against the AUDIO_UNIT list (issue #51)

Milan §5.4.2.13 / IEEE §7.4.21.1 (06 §6.4): SET_SAMPLING_RATE accepts only a
rate the located AUDIO_UNIT's `sampling_rates` list holds. Any other rate is
`BAD_ARGUMENTS` carrying the CURRENT rate, with nothing stored, marked or
notified. Before the check, `E_SSRATE` stored any 32-bit rate, answered
`SUCCESS` and announced it. The fixture lists 48000 and 96000 and its
`current_sampling_rate` is 96000.

- **W9i** (before W9, on the unset row) refuses 44100 byte-exact carrying the
  image's 96000, and GET still reads 96000. This is the reproduction. **W9c**
  adds the GET_DYNAMIC_INFO member's read of W9's 48000 (W8q graded the
  member's image arm). **W9j** refuses 192000 on the set row carrying the
  stored 48000.
- **W9k** registers a second controller and refuses 44100, 0x2000BB80 (48000
  with pull 1: the list stores whole words, so a pulled rate is another rate)
  and 0 (what a lane past the 152-byte descriptor reads). Each refusal is
  graded at the dynamic store's write counter, the NVM-mark and notify
  strobes, and the second controller's queue. The accepted 96000 (list entry
  1) moves each counter once and sends one unsolicited SET_SAMPLING_RATE.
- **W9l** patches the image in place: count 1 refuses entry 1, a replaced
  entry is accepted and the rate it replaced refused, and offset 148 refuses
  everything (the walk reads the list at 144 only, 07 §3.1 L10).
- **W9m** proves the lock outranks the list check: a foreign controller is
  `ENTITY_LOCKED` for a listed and an unlisted rate alike and moves nothing.
  The body of that refusal is issue #53's decision and is not graded here.

W9k, W9l and W9m run LAST on the main DUT, after section T, for section T's
reason: their empty notification windows cost about 1.3 s of simulated time,
and placed beside W9 they moved source 0's T-SRP-DAFRESH lapse into W25pre
(5 FAIL, W25pre to W25b2, in the first placement). U10 and U11 reset the DUT,
so the phase deregisters both bench controllers and sets the listed 48000
before it starts.

## Section DV: the Domain default is the top's parameter (issue #95)

`KL_srp_top` has a 16-bit `DOM_DEF_VID_P` with its own default of 2, and the top
used to leave it unbound, so nothing outside the processor could drive the
Domain default. The top now declares `SRP_DOM_DEF_VID_P` (`P-SRP-DOM-DEF-VID`,
default 2) and binds it to the child explicitly. The Domain FSM reads it three
times: as its reset value, in the declaration on every LINK_UP, and in the
revert on LINK_DOWN (10 §6.1 F10.2).

A build that only runs the product value cannot see that binding. The child's
own default is also 2, so a dropped or misbound connection produces exactly the
frames the default build expects (M25: 0 failures there). The Makefile therefore
builds the bench twice:

| Build | Override | Runs | Expects |
|---|---|---|---|
| `obj_dir/Vpp_top_sim` | none: the top's own default | every section, DV last | 2 (Milan §4.2.7.2.1) |
| `obj_vid/Vpp_top_vid` | `SRP_DOM_DEF_VID_P = 0x5A3C` (`SRP_VID_FIXTURE`) | DV alone | 0x5A3C |

The fixture is a verification value, not a product profile: Milan §4.2.7.2.1
fixes a shipping build at 2. It is chosen so that each plausible fault gives a
value of its own: a missing binding or a literal (2), an 8- or 12-bit truncation
(0x003C, 0x0A3C), a byte swap (0x3C5A), or routing it to the priority parameter
(priority 0x3C, read as 4 on the 3-bit face). Its low 12 bits are a legal VID,
0xA3C, and that is what the 12-bit faces carry: the class-D port, snapshot word
10, GET_DOMAIN and the ACMP talker. Only the MSRP wire field shows the top
nibble, which is why M27 fails the wire checks alone. The C++ expectation is
compiled from the same Makefile variable the wrap receives, never read back from
the DUT, and the wrap overrides nothing in the first build.

The fixture branch refuses compilation unless its 16-bit wire value and its
low 12-bit class-D value both differ from product default 2 (issue #97).
`SRP_VID_FIXTURE=0002` fails both assertions; `SRP_VID_FIXTURE=1002` fails the
class-D assertion even though its wire value differs. Each diagnostic names
the fixture, product default and affected width. These are verification-bench
assertions only. The default build has no fixture override and no distinctness
assertion.

`make` also runs `make fixture-guards`, a focused compile check of the actual
`sim_main.cpp` against generated model headers in a disposable directory. It
requires the no-override and pinned `5A3C` cases to compile, `0002` to fail with
both diagnostics and `1002` to fail with only the class-D diagnostic. An
unrelated compiler error fails the check. Run `make fixture-guards` alone for
this coverage without simulation; it does not change the sources or reuse
`obj_dir`/`obj_vid`. This check does not replace the two executable builds or
the missing-binding and child-default controls in the mutation record.

The compiler subprocess uses `LC_ALL=C` so diagnostic matching is independent
of the caller's language; all other environment inputs and compiler arguments
are preserved. `make fixture-guards-test` checks this isolation with mocked
subprocesses, without requiring non-English compiler catalogs, and is required
by `fixture-guards`. Removing the locale override makes this regression fail.

DV runs on a fresh model in both builds, after reset and with the link down:

- **DV1** the reset value on the class-D ports, snapshot word 10 and GET_DOMAIN;
  nothing is declared before the link.
- **DV2** LINK_UP: the first MSRP frame is `New {6, 3, default}` byte-exact, and
  the decoded SRclassVID is all 16 bits of the parameter.
- **DV3** GET_TX_STATE answers the default as `stream_vlan_id`. F05.11 leaves
  that field undefined while a source is not declaring; this talker answers the
  SR-class VID either way, as S10 and MP3 grade.
- **DV4** a bridge's certified two-class Domain `{5, 2, 5}` (NumberOfValues 2)
  is still adopted over the parameter: class-D `{3, 5}`, ADOPTED, one
  DOMAIN_CHANGE, and `Lv {6, 3, default}` + `New {6, 3, 5}` byte-exact.
- **DV5** LINK_DOWN restores the default and DEFAULTS with one DOMAIN_CHANGE,
  and nothing is declared for the 500 ms the link stays down.
- **DV6** LINK_UP declares `New {6, 3, default}` again, byte-exact.

Every edge is aligned into a clean slot of the 200 ms join cadence
(`sync_join`): the cadence timers are armed at reset, and a periodic re-join
drained into the same MRPDU would change the frame. The phase costs about 3.4 s
of simulated time on its own model, so the main DUT's timeline is untouched.
M25 to M31 in the mutation record are its evidence.

# [A483] Lane M1 for #629, round 2: media-clock following, design only

Status: STOPPED for the owner or manager decision. Design committed at `49899572741b732563bdca0bff03cefb69aea867`
(two round-2 commits on `78d4fef2`: `4845f158`, `49899572`; local, not
pushed). Gates rc 0. DECISION posted: #629 comment 5936327987.

- Lane: `629-media-clock-follow` at `78d4fef220c0ad4873a89b138828c0543c2bcad0`
  (one commit on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`). Add commits,
  amend nothing, do not push. Live dev was still `d4dd7426` when fetched.
- Assignment: #629 comment 5935864862. Round-1 reviews: PR #631 comments
  5935858741 (R428-1, six MINOR) and 5935860128 (R429-1, five MINOR). Manager
  rulings: #629 comment 5935520588. TAKEN: #629 comment 5935894826.
- Scope: design only. No RTL, builder, generator, config or processor change.
- B6 (PR #630) is still open at `26dfc82f`; the page keeps citing it through
  the PR.

## Progress

- [x] TAKEN posted on #629: comment 5935894826
- [x] Clause texts re-read (below), code sites re-verified (below)
- [x] Desk model of the revised meter rules: `meter_rules_model.py`,
      output `meter_rules_model.out`, rc in `meter_rules_model.rc` (rc 0)
- [x] Page rewrite: items 1 to 6, D1 and D5 re-argued (`4845f158`)
- [x] Precision fixes (`49899572`): bound wording, rate term in the
      deviation measurement, C2's lock and its counter-test line
- [x] Gates at `49899572`, all rc 0 (logs in `gates/`)
- [x] PR-BODY.md (template form, [A482] first line kept, Round 2 section)
- [x] DECISION posted: #629 comment 5936327987 (text: `decision.md`). STOPPED.

## Clause findings (round 2 re-read)

- Milan v1.2 5.3.3.6: "exactly one" INPUT_STREAM source binds each CRF-capable
  Stream Input, or the single AAF input of a Configuration with no CRF input.
  No clause sets a count for an AAF input beside a CRF input. INTERNAL is
  required with a Stream Output; EXTERNAL zero or more.
- Milan v1.2 5.3.11.1: the domain uses one listed source at any time; "The
  PAAD-AE is able to dynamically change the clock source to any of the
  CLOCK_SOURCE descriptors"; the current source is saved and restored after a
  power cycle.
- Milan v1.2 5.4.2.15: only "If the PAAD-AE is locked by a controller" does it
  forbid a non-ATDECC change. So no-fallback is a requirement only while
  locked; otherwise this design's choice.
- Milan v1.2 5.3.11.2 / Table 5.7: LOCKED/UNLOCKED of "the media clock used in
  the Clock Domain"; "locked" left to the manufacturer; invariant.
- Milan v1.2 6.2: Base formats: PCM, 32-bit, 48/96/192 kHz, 1/2/4/6/8 ch,
  6/12/24 samples per PDU, 1 timestamp per PDU, normal mode, not sparse.
- Milan v1.2 7.4: media clock sources better than +/-50 ppm.
- Milan v1.2 7.6 is a recommendation and "only deals with ... separate CRF
  Streams"; 7.6.2 binds one Media Clock Domain per Clock Domain.
- IEEE 1722-2016 4.4.4.3: "need not be seamless ... any appropriate action"
  describes the reaction to a talker's `mr` (a source change), not a stopped
  stream. Same in 10.4.3 for CRF.
- IEEE 1722-2016 10.6, last paragraph: lost CRF timestamps: "the media clock
  free-wheels until the CRF stream resumes". 4.4.4.7 NOTE: free-wheel while tu.
- IEEE 1722-2016 7.2.4/7.5: sp=1 means a timestamp in every eighth PDU only.
  7.3.5: every PDU of a stream holds the same number of samples. 7.3: AAF PCM
  carries format, nsr, channels_per_frame, bit_depth, stream_data_length, sp;
  no samples-per-frame field.
- IEEE 1722-2016 4.4.4.6: sequence_num 8 bits, wraps FF to 00.
- IEEE 1722-2016 10.8: Equation 15, talker following CRF within +/-5 % of a
  sample period (+/-1,041.7 ns at 48 kHz); Equation 16, a listener slaving to
  CRF accepts within +/-25 % and "may interpret the stream as invalid" beyond.
  No clause bounds an internally clocked AAF talker's timestamp regularity
  (no jitter rule in 1722-2016; none in Milan v1.2 or the media-clocking spec).
- IEEE 1722.1-2021 Table 7-16: STREAM_ID at bit 15, LOCAL_ID at bit 14 of
  `clock_source_flags`; the emitted 0x0002 is labelled STREAM_ID
  (`avdecc/aem_descriptors.py:456`; R428-1 O1).
- IEEE 1722.1-2021 7.4.23: success sends an unsolicited notification;
  7.4.23.1: the response carries the current value (old value on failure).

## Code map additions (dev d4dd7426)

- Parser AAF fields: `hdl/ieee1722/avtp/avtp_stream_parser.sv:165-177`
  (subtype, mr, tv, seq, tu at o+3 bit 0, fsh = o+16..o+23).
- RX monitor family compare (no spf, no channel check):
  `hdl/ieee1722/avtp/KL_avtp_rx_monitor_ctx.sv:465-491`.
- Advertised input formats spf 6: `avdecc/aem_descriptors.py:133`.
- KL_crf_rx jump bound derivation `:279-294`, restart rule `:394-403`, era
  rules `:529-558` (silence), `:611-674` (bind rise), mr seed `:380`, `:586-587`.
- Servo: rate sampled once per window `KL_mmcm_drp_servo.sv:609`; lock
  threshold `:232-233`, `:648`; LOCKED -> ACQUIRE on one bad window
  `:567-568` with `:689-694`; PI gated on rate valid `:613-615`.
- `KL_media_clock_restart.sv:225-246`: the merge window ends with the first
  PDU at the adopted level.
- CLOCK_DOMAIN counters on `~clkv_tu_w`: `milan_datapath.sv:3469-3475`,
  edge `:3492`. The rule was written in `c947acd8d` (2026-08-14, VERSION
  0x0047); live CRF selection arrived in `c92159ac9` (2026-09-02).
- CRF tu wiring trap: `milan_datapath.sv:5530-5534`.
- CSR read window: `hdl/common/csr/milan_csr.sv:2562-2581`.
- Saved state refused across a model change:
  `sw/firmware/milan_baremetal/milan_baremetal.c:634-636`;
  `docs/design/SAVED_STATE_FASTCONNECT.md:638-640`;
  `docs/design/SAVED_STATE_MATERIALIZATION.md:1153-1158`.
- Default clock_source_index 0: `avdecc/aem_descriptors.py:476`.
- Token-pinned CRF compare: `scripts/check_gptp_docs.py:114`,
  `docs/diagrams/timesync_chain.gen.py:49`; builder test
  `sw/builder/test_builder.py:19580-19590`; `sw/litex/milan_soc.py:872-874`.
- Processor restore compare: `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:501-503`
  (banner `:84-90`); 7.4.23.1 credits at `gen_ucode.py:1414`,
  `07_memory_maps.md:135`, parent `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:89`.

## Desk model result (meter_rules_model.out)

- Shape "group" (every pick of a 16-PDU group shares one sign, the case no
  averaging removes): bound 2,048 never validates at +/-1,042 ns; 4,096
  validates up to +/-1,426 ns at 300 ppm.
- Shape "white" (independent per PDU): with the first-PDU pick and bound
  4,096, only 74 % of 512 ms windows are inside the servo's 2 ppm at
  +/-1,042 ns (56 % at +/-1,426); with the group mean, 100 %.
- Conclusion: bound 4,096 ns derived from 10.8 Eq. 15, plus the group-mean
  pick.

## Design options and recommendation (round 2)

Full text: `docs/design/MEDIA_CLOCK_FOLLOWING.md` at `49899572`.

| ID | State | Recommendation |
|---|---|---|
| D1 order | re-opened | L1 by class (INTERNAL 0, CRF 1, AAF k at 2+k); saved-state reason withdrawn; argued on CRF index stability; on a shape without INTERNAL, CRF is 0 |
| D2 measurement | ruled M1 | plus round 2's contract: 48 kHz base format only (spf from `stream_data_length` = 24 x channels), groups of 16 by `sequence_num` mod 16, group mean (P2 over P1), jump bound 4,096 ns (B2 over B1 2,048 / B3 16,384) |
| D3 switch | ruled W2 | one-cycle unlocked presentation in the root; meter era restart on a switch |
| D4 A2 at INTERNAL | with the owner | A2-a (manager agrees) |
| D5 domain counters | re-opened | C1 (servo LOCKED), reversal of `:3469-3475` stated; C2 (reference lock) and C0 (rule stands) as alternatives; C3 (raise tu) not recommended |
| D6 configs | ruled all five | consequence recorded: every unit loses saved state once, comes up on index 0 (INTERNAL) |
| D7 phase | filed #632 | |

Design choices stated, changeable by ruling: no fallback at any time (Milan
requires it only while locked); `mr` on a followed AAF stream's loss and echo.

`mr` switch rule: a meter era starts at every change of the followed listener
and at entry into AAF following; it clears lock without a disruption trigger
(trigger = lock fall while the followed source is unchanged) and re-seeds the
received `mr` silently. Only the source-change edge requests a restart on a
switch. Reason: the #387 merge lasts only until each output's first PDU at the
adopted level (at most 125 us for AAF).

Area: meter 330-480 LUT, 270-400 FF, 1 RAMB18 (group mean adds 80-130 LUT,
70-100 FF); total about 380-560 LUT, 290-440 FF, 1 RAMB18.

## Parent-visible changes (from the page)

- Requirements: FR-CLK-03/04 and the status row (`docs/reference/FR_NFR.md:155,237,238`).
- Config: `input_stream` re-admitted; five shipping configs; saved-state
  release note.
- Builder: `_load_clocking`, `_overlay_clock_sources` (class order),
  `CLOCK_SOURCE_NAMES` (`:141`), `_load_names` (`:3784-3790`), shape tables
  (`:2836-2853`); `test_builder.py:19580-19590`.
- Model: `CS_TYPE`/`CS_RETIRED`, `clock_source_shape`, `aem_emit.py`, the
  `clock_source_flags` value (`aem_descriptors.py:456`, O1).
- Generated: shape headers, AEM images, `hdl/common/gen`.
- RTL new: the meter. RTL root: decode, consumers, one-cycle presentation,
  meter on the parser bundle (`tu` from `avtprx_tu_bit`), AAF `mr` triggers
  with the switch rule, A2-a / D5 as decided, banner `:3469-3475` under C1/C2,
  stale comments `:607`, `:3112`, `:5576-5578`. RTL servo: `sel_i`, `ref_*`;
  harnesses in `tb/verilator/mmcm_servo/`, `mmcm_servo_autorepair/`,
  `crf_rx/crf_talker_wrap.sv`, `milan_dp/sim_main.cpp`.
- Registers: two RO words in `0x8E0`-`0x8F4`, each with its `rd_in_window`
  term (`milan_csr.sv:2562-2581`); VERSION moves.
- Gates/diagrams: `scripts/check_gptp_docs.py:114`,
  `docs/diagrams/timesync_chain.gen.py:49` keep their token under L1 if the
  CRF row keeps the compare text.
- Docs: TIME_SYNC Media boundary, compliance matrix rows, L6 (with its
  7.4.23.1 credit), ENDSTATION_BUILDER, README-parameters, feature ledger.

## Processor-visible changes (protocol-processor #141)

- RTL/microcode: none (range check `gen_ucode.py:1410-1440`, restore compare
  `KL_aecp_nvm_writer.sv:501-503`).
- Docs: L6 (`07_memory_maps.md:135`), REQ-MDL-005, and the range-check comment
  (`gen_ucode.py:1414`) credit BAD_ARGUMENTS to 7.2.32 and Table 7-141.
- Tests with failing mutants: 10-source SET/notify/read-back; index 10
  BAD_ARGUMENTS with current index; D3 save/restore of an AAF index; restore
  refusal above a smaller count. Lands before or with the parent; then a pin
  bump.

## Test plan (summary)

Simulation, each with a failing mutant: meter rate vs `KL_crf_rx` (mutant:
decimation 1, `rate_valid` never rises); error at the bound (mutants B1, P1);
beyond the bound (mutant B3); formats (mutant: no `stream_data_length` check);
sequence wrap (mutant: continuity without the 8-bit wrap); lock/unlock;
history restarts incl. the `tu` net trap; selection; `mr` seed (mutant: no
re-seed); servo W1 mutant; true-ratio leg with AAF and CRF talkers at
different offsets (mutants: CRF-only decode, mux stuck on CRF); root W2
presentation (mutant: removed); switches with opposite `mr` (mutants: no
re-seed, unmasked disruption trigger, ungated AAF triggers); lock loss; echo;
D5 counters (mutant: another option's level); CSR words (mutant: missing
read-window term); AECP walk (mutant: stale decode table); builder order
(mutant: L2 overlay).

Bench (B6 method): B AAF (restart count unchanged after lock; largest
deviation recorded as the peer's timestamp-quality measurement), B CRF, B
INTERNAL control, A1, A2 at INTERNAL, A2 under following graded through B AAF
and B CRF, a switch case (one MEDIA_RESET per switch), lock loss (D5 counters
and the invariant), synthetic controls.

## Packet contents

- `taken.md`, `decision.md`: the posted comment texts.
- `PR-BODY.md`: the round-2 PR body for the manager to apply.
- `meter_rules_model.py`, `meter_rules_model.out`, `meter_rules_model.rc`:
  the desk model (standard library only, seed 629, rc 0).
- `gates/`: the gate logs at `49899572`.

## Notes for the manager

- Pushing the two round-2 commits and applying `PR-BODY.md` are yours.
- O1 (the `clock_source_flags` label) is recorded on the page as (d) item 8;
  filing it as an issue is yours.
- B6's page (PR #630) is still unmerged; the design cites it through the PR.
- Round 2 is two commits because a re-read before publication found three
  imprecise statements; nothing was published between them.

[R429] NEGATIVE - exact head 78d4fef220c0ad4873a89b138828c0543c2bcad0

# R429-1: external review of PR #631 (issue #629, lane M1, design only)

- **Head under review:** `78d4fef220c0ad4873a89b138828c0543c2bcad0`, tree `3fba1fdc1c8f172d7d744d18da1e4d4c4afadf55`, one commit on dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`.
- **Diff:** `docs/design/MEDIA_CLOCK_FOLLOWING.md` (new, 577 lines) and its design-index row in `docs/README.md` (+1). No RTL, builder, model, configuration or processor change. Code is byte-identical between `d4dd7426` and the head.
- **Reconstructed from:**
  - AGENTS.md, CONTRIBUTING.md and docs/README.md.
  - #629's body and its public comments: the lane M1 assignment 5935051587, the TAKEN and DECISION comments, and the manager rulings 5935520588 (D1-D3, D5 and D6 accepted; D7 filed as #632; the processor part filed as protocol-processor #141; D4 to the owner).
  - The PR body.
  - The clause texts: Milan v1.2, the Milan media-clocking specification rev 2.1, IEEE 1722.1-2021 and IEEE 1722-2016.
  - The code at `d4dd7426` and at the processor pin `b2db3a97`.
  - The public evidence tree `review-evidence/629-r1` at `0c17547b` (manifest and author hand-off).
  - The B6 findings page at PR #630 head `26dfc82f`, and #74 comment 5932380322.
- **Prior public review findings on this PR:** none. PR #631 carries only the two review-start notices at the time of this review, so nothing is resolved or retained.

Verdict: **NEGATIVE** on five open MINOR findings (F1-F5). The clause reading is largely right, every code citation resolves at `d4dd7426`, the area basis reproduces exactly and the docs gates pass. Four problems remain:

- The proposed AAF meter inherits a CRF-only jump bound that a conformant AAF talker can exceed.
- Its accept and decimation rule breaks at the 8-bit sequence wrap for most of the formats it says it accepts.
- Its received-`mr` seeding allows a phantom second toggle on an AAF-to-AAF switch.
- The test plan does not grade three of the behaviours the page says a test grades, and two clause statements are stated more strongly than the clause text allows.

## Contents

- [Clause questions](#clause-questions)
- [Code map](#code-map)
- [Design assessment](#design-assessment)
- [Findings](#findings)
- [Suggestions](#suggestions)
- [Executed evidence](#executed-evidence)
- [Ledger](#ledger)
- [Limits](#limits)
- [Pending manager duties](#pending-manager-duties)

## Clause questions

**(a) An INPUT_STREAM source per AAF input beside the CRF source: confirmed, it may coexist.**

- Milan v1.2 5.3.3.6 requires exactly one INPUT_STREAM CLOCK_SOURCE for each CRF-capable Stream Input, or for the single AAF Stream Input when the Configuration has no CRF input. It requires INTERNAL when there is a Stream Output, and allows any number of EXTERNAL sources. It says nothing about INPUT_STREAM sources on AAF inputs when a CRF input exists, so it is a minimum, not a closed list.
- Milan v1.2 5.3.11.1 names "two categories of clock sources: internal or input stream".
- IEEE 1722.1-2021 7.2.9 and Table 7-17 make an Input Stream a valid source. Table 7-61 (7.2.32) caps `clock_sources_count` at 216 and sets no order.

The page's answer is correct. Its "at most one per Stream Input" over-reads the clause (F1).

**(b) No automatic fallback, holdover allowed: the design choice is sound, but the page presents it as a clause requirement.**

- Milan v1.2 5.3.11.1 requires that the domain always uses one listed source and that the current source is saved state. It then says "The PAAD-AE is able to dynamically change the clock source to any of the CLOCK_SOURCE descriptors".
- Milan v1.2 5.4.2.15 forbids a non-ATDECC change only "If the PAAD-AE is locked by a controller".
- IEEE 1722-2016 4.4.4.3 and 10.4.3 ("need not be seamless", "any appropriate action") and the 4.4.4.7 NOTE (free-wheel) support holdover.

So no fallback is required only while the entity is locked by a controller; otherwise it is a permitted choice. The page itself says at line 99 that Milan sets "no fallback rule" (F1).

**(c) `mr`: correct.**

- IEEE 1722-2016 4.4.4.3 requires a toggle on a source change, held for at least 8 AVTPDUs. PICS Table F.7 AAF-5 and AAF-6 make both mandatory for AAF.
- The disruption and echo shalls (4.4.4.3 third paragraph, 10.4.3) name CRF only. The rule that only the recovery stream's `mr` counts is in both last paragraphs.
- Applying the disruption and echo rules to a followed AAF stream is permitted, not required.
- The phase rules are read correctly: 10.8 Equation 15 (+/-5 % of a sample period, +/-1,041.7 ns at 48 kHz) and 4.3.5 (whole periods). They are deferred to #632 by ruling.

**(d) The claimed repository misreadings: all seven confirmed.**

1. FR-CLK-03, the status row, L6 and TIME_SYNC 141-145 and 198 state #389's product decision as if it were the clause.
2. BAD_ARGUMENTS for an unlisted index is attached to Milan 5.4.2.15/.16 (compliance matrix row 120, #629's body). Those clauses defer to IEEE 1722.1-2021 7.4.23 and 7.4.24, and 7.4.23.1 names no status. The refusal follows from 7.2.32's list and Table 7-141's BAD_ARGUMENTS. 7.4.23.1 adds that the response carries the current value.
3. Milan 7.2.2 only requires a CRF input. The builder (`endstation_builder.py:3893-3899`, docstring `:5019-5028`) and `aem_specs.py:234-241` cite it for a source restriction.
4. Milan 7.2.3 only requires the CRF output to exist, but #74's comment cites it for A2. The A2 basis is correct: IEEE 1722.1-2021 7.2.32 ("a source of a common clock signal"), Table 7-8 (STREAM_OUTPUT `clock_domain_index`, "the Clock Domain providing the media clock for the Stream") and the Milan 7.1 note.
5. #629's "applies to AAF and CRF alike" overstates the shall.
6. The stale comments at `milan_datapath.sv:607` and `:5576-5578` are confirmed. A third is at `:3112` (S1).
7. The compliance matrix row 187 has no A2 caveat.

The over-citation of 7.2.2 and 7.2.3 is real.

## Code map

`probes/code_map_check.sh` prints every cited range at `d4dd7426` and at the processor pin (`receipts/code_map_check.txt`, 73 ranges). Every fact the page states holds at its cited lines:

- **Builder and AEM model:**
  - the five configuration lines, `_load_clocking`, the sink rules and `_overlay_clock_sources`;
  - the pre-#389 order at `aea44c071^:4180-4203`, and the model-shape and prune gates;
  - `CS_TYPE`/`CS_RETIRED`, `clock_source_shape` and the identity CLOCK_DOMAIN;
  - `AEM_N_CLKSRC_C`/`AEM_CRF_CLKSRC_C`, which read `2` and `16'd1` in the generated 1x1 header.
- **Processor:**
  - the `E_SCLKS` range check `index < clock_sources_count`, answering the current index on refusal (`gen_ucode.py:1410-1440`);
  - L6, the D3 record, REQ-AEM-013 and REQ-MDL-005;
  - the export of CLOCK_DOMAIN 0 only (`KL_aecp_dyn_state.sv:114`, `:352`);
  - `KL_aecp_nvm_writer.sv:86-90`, which is the banner stating the restore rule. The compare itself is the `CD_SRCCNT_C` lane walk (`:319`, `:743`), which exists.
- **Fabric chain:**
  - `media_clk_resolve`, the servo ports and its `clk_src_i == crf_src_idx_i` select;
  - servo IDLE (trim cleared), and HOLDOVER to ACQUIRE with `win_skip_r = 2`;
  - the aligner and NCO gate, and the INTERNAL free-run rule;
  - the `mr` triggers and the #387 merge, the #386 settle and the I2S `servo_en_i`;
  - CLOCK_DOMAIN LOCKED/UNLOCKED on `~clkv_tu_w`;
  - the parser bundle, the inert RX-monitor ports and `PCMRX_TS`.
- **The CRF output's clock:** `KL_crf_tx` stamps every 96th event of `clk_audio_i/512`, and the AAF talker latches on the packet grid (`KL_aaf_packetizer.sv:720-726`). 48,000 x (1 - 10.64e-6) = 47,999.4893 Hz.

The only errors are cosmetic offsets: `CLOCK_SOURCE_NAMES` is at `:141`, not `:134-140`, and the MMCM-plan comment in Limits starts at `:3937`, not `:3936` (S1). The 0x8E0-0x8F4 window is unmapped (`REGISTER_MAP.md:1833`; no `milan_csr.sv` decode).

## Design assessment

- **D2, the 1-in-16 meter: right in spacing and rate, open on jitter and format.**
  - *Spacing.* Milan v1.2 6.2 fixes 6 samples per PDU at 48 kHz, so one PDU in 16 is 96 samples, the CRF `timestamp_interval` (Milan v1.2 7.3.2). 16 divides 256, so the `sequence_num` pick survives the wrap for spf 6.
  - *Rate.* `KL_crf_rx`'s 256-entry ring over 2 ms picks gives the servo's ns-per-512 ms units (`KL_mmcm_drp_servo.sv:20-27`). The servo gates PI on `rate_valid` (`:613-615`).
  - *Jitter.* The inherited 2,048 ns jump rule was derived for CRF, and a 10.8-conformant AAF talker can exceed it (F2).
  - *Format.* The general "spf dividing 96" rule breaks at the wrap for six of the twelve divisors (F3).
- **D3 (W2), hold and re-acquire: sound against the servo.** A one-cycle low `ref_locked` moves ACQUIRE or LOCKED to HOLDOVER (`:564`). It then returns to ACQUIRE with `win_skip_r = 2` and `lock_cnt_r = 0` (`:574-577`). The integrator is kept and the aligner stays engaged. The test plan does not grade the root's one-cycle presentation (F5).
- **Lock loss, holdover and `mr`: sound for loss and return; underspecified for an AAF-to-AAF switch.** A loss gives one toggle and the return gives none. On a switch, the received-`mr` reference is not re-seeded, and a lock fall can land after the #387 merge window (F4).
- **D5 (C1):** consistent with Milan v1.2 5.3.11.2. "Locked" is manufacturer-defined and the counters stay edges of one level, so the invariant stays structural. It supersedes the recorded "one clock-validity authority" rationale (S3).
- **A2 options:** the analysis is correct. Under following, B6's B CRF already shows `SLIP_TDM` static. A2-a at INTERNAL is plausibly one gate. D4 is with the owner and is not judged here.
- **Area: the basis reproduces exactly.**
  - `ooc.sh KL_crf_rx` at the 1x1 TDM8 shape gives 433 LUT, 544 FF, 1 RAMB18 and 147 CARRY4 (`receipts/ooc_KL_crf_rx.log`).
  - The meter range follows from it. Removing the ten 32-bit Table 5.6 tallies (320 FF), the interval divider and `delta_o` leaves about 190 FF before the selection logic.
  - Growing the 8x8 AEM by 8 x 86 + 16 = 704 B is safe. The image measured here is 11,049 B against the 65,536 B bound (`aem_assemble.py:314`).
- **Test plan and bench.**
  - The bench cases follow B6's method. B6's B CRF ran the tone over the DUT-talker-to-peer path while the DUT followed, and B AAF mirrors that. So THD+N does grade the DUT following each source, against the INTERNAL control and the synthetic controls.
  - The simulation plan has the gaps listed in F2-F5.

## Findings

### F1: MINOR (Conformance, Docs). Two clause statements are stronger than the clause text

- **Where:** `docs/design/MEDIA_CLOCK_FOLLOWING.md`
  - `:64-65`: "The clauses allow at most one per Stream Input".
  - `:73-80`: "What the listener must do: Keep the selection".
  - `:372-373`: "as (b) requires".
  - `:61`: 7.6.2's stated consequence.
- **Evidence:**
  - Milan v1.2 5.3.3.6's "exactly one" binds only CRF-capable inputs and the sole AAF input of a CRF-less Configuration. No clause sets a count for AAF inputs beside a CRF input.
  - Milan v1.2 5.3.11.1 also says "The PAAD-AE is able to dynamically change the clock source to any of the CLOCK_SOURCE descriptors associated with the Clock Domain".
  - Milan v1.2 5.4.2.15 forbids a non-ATDECC change only "If the PAAD-AE is locked by a controller". The page itself says at `:99` that Milan sets "no fallback rule".
  - 7.6.2 sits inside 7.6, which is a recommendation, and binds a Clock Domain to one Media Clock Domain. "This entity has one domain" is a fact of this AEM, not of 7.6.2.
- **Impact:** this page is the clause basis for the FR-CLK-03/04 amendments. A "must" with no clause behind it would pass into requirements, which is the same class of defect that item (d) corrects elsewhere.
- **Required outcome:**
  - (b) separates what is required from what is permitted. Required: one listed source at all times and saved state (5.3.11.1); no non-ATDECC change while locked (5.4.2.15); the 5.3.11.2 counters. Permitted otherwise: an entity-initiated change.
  - "No fallback" is recorded as this design's choice, with its reason.
  - The "at most one" sentence and the 7.6.2 consequence are restated to what the clauses say.
- **Verification:** re-read `(a)`, `(b)` and Holdover item 2 against the quoted clause text.

### F2: MINOR (RTL, Robustness, Tests). The meter inherits a CRF-derived jump bound that a conformant AAF talker can exceed

- **Where:** `:307-310`, the history restart on "a picked-timestamp spacing outside 2 ms plus or minus the jump bound"; test plan `:518-521`.
- **Evidence:**
  - `KL_crf_rx.sv:279-294` derives `TS_JUMP_NS_C` = 2,048 ns for CRF. It assumes the remote talker shares the local PHC envelope with under 384 ns quantisation, and that arrival jitter is absent.
  - The page gives no basis that AAF presentation timestamps meet it. IEEE 1722-2016 10.8 only bounds a CRF-following talker's timestamps to within +/-5 % of a sample period (+/-1,041.7 ns) of the CRF timing points. So two picks 2 ms apart may legally differ from nominal by up to 2,083 ns, before any rate term.
  - Probe `probes/crf_jitter` drives `KL_crf_rx`, whose rules the meter copies, at 2 ms spacing and 0 ppm with an alternating phase error (`receipts/crf_jitter_probe.log`):
    - at +/-1,041 ns, inside 10.8, lock is held (593 of 600 PDUs) but `rate_valid` never rises (0 of 600);
    - at +/-1,023 ns, `rate_valid` rises (344 of 600).
  - The servo runs PI only on valid history (`KL_mmcm_drp_servo.sv:613-615`). It would sit in ACQUIRE without ever trimming, and under C1 the domain would stay UNLOCKED.
- **Impact:** the DUT may fail to follow a Milan-conformant AAF talker that itself follows CRF, which is the ordinary Milan topology. Nothing would show the failure except a low `rate_valid`. Adding the 601 ns rate term narrows the tolerated phase error further.
- **Required outcome:**
  - The page states the AAF timestamp-regularity assumption, with a clause or measurement basis.
  - It decides the meter's jump bound: inherit it with the risk stated, or derive it from 10.8 plus the rate term.
  - The meter suite gains a planted-phase-jitter case at and beyond the chosen bound, with a mutant.
  - B AAF records the meter's history-restart count as a pass item (the proposed status word already carries it).
- **Verification:** the revised page and test rows; later, the simulation case and the bench count.

### F3: MINOR (RTL, Robustness, Tests). The accept and decimation rule fails at the sequence-number wrap for most of the formats it accepts

- **Where:** `:297-302` ("`spf` dividing 96"; "one PDU in 96/`spf`, picked by `sequence_num` modulo 96/`spf`") and `:299-300` ("Anything else never locks").
- **Evidence:**
  - `sequence_num` is 8 bits and wraps (IEEE 1722-2016 4.4.4.6), so the pick is periodic only when 96/spf divides 256.
  - `probes/seq_decimation.py` (`receipts/seq_decimation.log`) shows the picked spacing broken at every wrap for spf 1, 2, 4, 8, 16 and 32, with 32- or 64-sample gaps.
  - The jump rule then restarts the history every 256 PDUs, at most 42.7 ms, under the 512 ms ring. So `rate_valid` never rises for a format the meter accepts.
  - AAF carries no spf field. It must come from `stream_data_length`, channels and bit depth (`fsh_o`, `avtp_stream_parser.sv:176`) or from the bound input's current format. The page names neither.
- **Impact:** an accepted format that can never be followed contradicts the page's own rule. Exposure is low while listeners advertise only Milan base formats, but the rule as written is wrong for the implementation lane.
- **Required outcome:**
  - The accept rule is Milan v1.2 6.2's 48 kHz base format (spf 6, one pick in 16), or "96/spf a power of two", with the spf source named.
  - The selection test refuses a non-power-of-two divisor, for example spf 8.
- **Verification:** revised page and test row.

### F4: MINOR (RTL, Robustness, Tests). A switch between two AAF inputs can raise a second `mr` toggle

- **Where:** `:313-315` (the `mr`-toggle pulse "seeded per era as `KL_crf_rx` seeds its own"); `:388-394` (merging, "each stream carries exactly one toggle"); test row `:524`.
- **Evidence:**
  - `KL_crf_rx`'s era is a bind rise or 100 ms of silence (`KL_crf_rx.sv:85-92`, `:259-263`). The page restarts the rate history on "a change of the selected listener" (`:309-310`) but not the received-`mr` seed.
  - On a switch from input k to input j whose talkers carry different `mr` levels, j's first accepted PDU reads as a received toggle and raises an echo request.
  - The #387 merge absorbs a second request only until the first outgoing PDU at the adopted level is reported (`KL_media_clock_restart.sv:236-264`). j's first PDU and each AAF output's next PDU both fall at uncorrelated points within one 125 us period, so about half the AAF outputs carry a second toggle after the 8-PDU hold.
  - The page also leaves open which lock fall goes with a switch: the meter's own, or the root's one-cycle presentation. A meter lock fall that lands after that window double-toggles the same way.
  - Row `:524` does not require the two streams to carry different `mr` levels, so it can pass with the defect present.
- **Impact:** every listener of the DUT's streams sees a phantom media-clock restart when the followed AAF input changes, contrary to the page's own rule.
- **Required outcome:**
  - The page specifies that a change of the measured listener, and entry into AAF selection, start a new `mr` era with a silent seed.
  - It specifies that a switch raises exactly one request, or proves that any second request falls inside the merge window.
  - The input-0-to-input-1 test drives opposite `mr` levels and carries a no-re-seed mutant.
- **Verification:** revised page and test row.

### F5: MINOR (Tests). The simulation plan does not grade three behaviours the page relies on, and two stated failure modes are wrong

- **Where:** `:351` ("the one-cycle presentation is what prevents it, so a test grades it"); test table `:516-529`.
- **Evidence:**
  1. No row grades the root's one-cycle unlock presentation on a switch onto an already-locked CRF input. The `mmcm_servo` row drives the servo's reference directly. The `milan_dp` switch row checks `mr`, the recentre, the aligner and `SLIP_TDM`, but not servo HOLDOVER then ACQUIRE. No mutant removes the presentation.
  2. The true-ratio leg does not require the AAF and CRF stimuli to carry different rate offsets. A reference mux stuck on `KL_crf_rx` (the servo follows CRF while AAF is selected) would pass. The listed mutant, the CRF-only decode, is weaker.
  3. The decimation-by-1 mutant is said to give a rate "off by the decimation ratio". Under the inherited jump rule every 125 us spacing restarts the history, so `rate_valid` never rises and `rate_o` holds its reset value. At the 0 ppm stimulus point the rate comparison still matches.
  4. The AECP-walk row's "mutant" (a non-identity list refused by the builder) is a builder negative test, not a fault that makes the walk fail.
- **Impact:** checks the page names as protection for D3 and D2 could pass with the defect present. AGENTS section 6 requires that each test can fail for the defect it claims to detect.
- **Required outcome:** rows and mutants for items 1 and 2; corrected failure modes for items 3 and 4, with `rate_valid` asserted wherever rate is compared.
- **Verification:** revised test table.

## Suggestions

These are optional and do not affect lens coverage.

- **S1 (Docs).**
  - (d)6 lists two stale comments. `hdl/milan/milan_datapath.sv:3112` ("selects the CRF media clock (2)", a pre-#389 index) is a third.
  - The Builder row should also name `_load_names`'s refusal of `names.clock_sources.stream`, which a "restored stream entry" must lift.
  - Two citation offsets: `endstation_builder.py:141`, not `:134-140`; and `:3937-3955`, not `:3936-3955`.
- **S2 (RTL).** Name two traps for the implementation lane:
  - The AAF `tu` is the common-header bit `avtprx_tu_bit`. `KL_crf_rx`'s `tu_i` is wired to `avtprx_tv_bit` for the CRF alternative header (`milan_datapath.sv:5530-5534`), so copied wiring would never see an AAF `tu` edge.
  - The two new CSR words need `rd_in_window` terms (`milan_csr.sv:2562-2581`), or they read 0. This is the recorded 0x8F8 trap.
- **S3 (Conformance, Docs).**
  - Milan v1.2 7.6 ("only deals with ... separate CRF Streams") puts AAF sources outside Milan's media-clock-management model. A 7.6 controller will not select them, and the page could say so.
  - C1 supersedes the recorded rationale at `milan_datapath.sv:3469-3475` that LOCKED equals `~tu`. The page could say so explicitly.
- **S4 (Conformance).** "Index 1 keeps meaning CRF on every shape" (`:267`) holds only where INTERNAL and CRF are both declared. The builder also admits `[internal]` alone, and CRF without INTERNAL on an output-less configuration (`endstation_builder.py:4262-4267`). State the general order, or require both whenever `input_stream` is declared.

## Executed evidence

Every command ran in the foreground, with the rc shown. Receipts are listed in `MANIFEST.sha256`.

| Run | Result | Receipt |
|---|---|---|
| Markdown gates in a pinned-requirements venv: `docs_check`, `check_doc_style`, `gen_toc --check`, `gen_toc --verify-anchors`, `check_em_dash --base d4dd7426` and `check_doc_paths`; also `check_feature_status --self-test`, `git diff --check d4dd7426 HEAD` and `git diff --check` | all rc 0 | `receipts/docs_gates.log` |
| `OOC_SHAPE=configs/generated/endstation_ax7101_1x1_tdm8 syn/yosys/ooc.sh KL_crf_rx` (one top, scratch temp dir) | rc 0; 433 LUT, 544 FF, 1 RAMB18, 147 CARRY4, exactly the page's figures | `receipts/ooc_KL_crf_rx.log` |
| `KL_crf_rx` jump-rule probe on the pinned simulator 5.050 | rc 0; `rate_valid` 344/600 at 0, +/-1,000 and +/-1,023 ns; 0/600 at +/-1,041 and +/-1,042 ns; lock 593/600 throughout | `probes/crf_jitter/`, `receipts/crf_jitter_probe.log` |
| Sequence-wrap decimation probe | 6 of the 12 divisors of 96 broken at the wrap | `probes/seq_decimation.py`, `receipts/seq_decimation.log` |
| Code-map dump of every cited range | 73 ranges, all facts as stated | `probes/code_map_check.sh`, `receipts/code_map_check.txt` |
| AEM size: the builder for the 8x8 configuration and the 8-channel board configuration, output to scratch | rc 0; `AEM_ROM_BYTES_C` 11,049 and 9,257 against the 65,536 B bound | scratch only, not published |
| Restore check | exact head; index tree equals the HEAD tree; blob bytes and modes match for all 979 tracked files; gitlinks unchanged (external `efeb541a` uninitialised as found, gptp-processor `5dce647a`, protocol-processor `b2db3a97`, verilog-axis `48ff7a7e`); three ignored bytecode files from one builder `--help` call removed; 0 untracked or ignored entries left | `receipts/restore_check.log` |
| Hosted checks at the head, read only | success: `rtl-fast`, `changes`, `elaborate`, `bdd-conformance`, `docs-check-no-git`, `wire-accountability`, `full-ci-gate`; in progress when read: `docs-check`; skipped by path scope, not executed: the verilator and yosys suites and shards, the physical gPTP nightly, `yosys-elaboration` and `verilator-lint` | none; hosted acceptance is the manager's |
| Public-text scan of the added lines (addresses; host, peer, switch, instrument and capture names; home or temp paths) | no hit; the page names only "the reference peer" | none |

Reference-text and tool identities are in `receipts/identities.txt`. The clause texts were read from local copies and are not republished.

## Ledger

The head for every lens is `78d4fef220c0ad4873a89b138828c0543c2bcad0`, covered by round R429-1.

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | `MEDIA_CLOCK_FOLLOWING.md:51-168` against Milan v1.2 5.3.3.6, 5.3.11.1, 5.3.11.2, 5.4.2.15/.16, 6.2, 7.1, 7.2.2, 7.2.3, 7.3.2, 7.4 and 7.6; IEEE 1722.1-2021 7.2.6 Table 7-8, 7.2.9 Tables 7-15/7-17, 7.2.32 Table 7-61, 7.4.23/.24 and Table 7-141; IEEE 1722-2016 4.3.2, 4.3.5, 4.4.4.3, 4.4.4.6, 4.4.4.7, 10.4.3, 10.8 and Table F.7; the media-clocking specification rev 2.1 | R429-1 | `78d4fef220c0ad4873a89b138828c0543c2bcad0` |
| RTL | UNCLEAN (F2, F3, F4) | design `:241-461` against `KL_crf_rx.sv:267-403`, `KL_mmcm_drp_servo.sv:263-273`, `:411` and `:538-700`, `KL_media_clock_restart.sv:203-267`, `milan_datapath.sv:1554-1570`, `:3108-3203`, `:3469-3495`, `:5418-5446`, `:5508-5627`, `:5713-5748` and `:6079-6126`, and `avtp_stream_parser.sv:90-96` and `:176-180`; the area re-run | R429-1 | `78d4fef220c0ad4873a89b138828c0543c2bcad0` |
| Robustness | UNCLEAN (F2, F3, F4) | meter accept, restart and lock rules `:291-315`; lock loss and holdover `:362-380`; switching `:346-360`; the `crf_jitter` and `seq_decimation` probes; the AEM size bound `aem_assemble.py:314` | R429-1 | `78d4fef220c0ad4873a89b138828c0543c2bcad0` |
| Tests | UNCLEAN (F2, F3, F4, F5) | test plan `:509-546` against whether each mutant is reachable in the cited RTL; the B6 page at PR #630 `26dfc82f` (method, B CRF tone path); the processor test plan `:497-504` | R429-1 | `78d4fef220c0ad4873a89b138828c0543c2bcad0` |
| Docs | UNCLEAN (F1) | the whole of `MEDIA_CLOCK_FOLLOWING.md`; the `docs/README.md:72` index row; the docs gates (all rc 0); the code-map receipt; the PR body; the public-text scan | R429-1 | `78d4fef220c0ad4873a89b138828c0543c2bcad0` |

## Limits

- **Design review only.** No RTL exists to simulate. The probes exercise today's `KL_crf_rx` as a stand-in for the rules the meter is to copy, not the proposed meter.
- **The jitter probe is an extreme case.** It uses a 0 ppm stimulus and an alternating phase error, an extreme pattern still inside 10.8. Real AAF talkers' timestamp regularity was not measured.
- **No hardware.** No bench run or physical calibration was done, and field skips are not hardware proof.
- **Area tool versions.** The area re-run used the locally installed synthesis and conversion tools (versions in `receipts/identities.txt`). Only the identical figures show that they match the author's run.
- **Hosted state.** The hosted `docs-check` context was still in progress when read. The long hosted suites were path-scoped skips, not executions.
- **Out of scope.** D4 is with the owner and was not judged. #632 (phase) and protocol-processor #141 were not reviewed.

## Pending manager duties

- Publish this report and the manifest-listed receipts, and post the verdict.
- Hosted and local-replica acceptance at the head, including the in-progress `docs-check`.
- After the findings are answered:
  - a re-review at the new head;
  - the internal review's verdict;
  - the candidate merge against live dev (base `d4dd7426`; live dev was `d4dd7426` at assignment);
  - post-merge containment;
  - the owner's D4 ruling before the implementation lanes start.

R429-1 FINISHED

# [A482] Lane M1 for #629: media-clock following, design only

Status: STOPPED for the owner or manager decision. Design committed at `78d4fef220c0ad4873a89b138828c0543c2bcad0` (local, not pushed); gates rc 0; DECISION posted: #629 comment 5935490330.

- Lane: `629-media-clock-follow`, from dev `d4dd742679b902b2bc5eedf89d525066d59aafbb`.
- Assignment: #629 comment 5935051587. TAKEN posted: #629 comment 5935072991.
- Scope: design only. No RTL, builder, generator, config or processor change.
- Deliverable: `docs/design/MEDIA_CLOCK_FOLLOWING.md` and its row in `docs/README.md`
  (the "Architecture and integration" table is the design index: it lists the
  other `docs/design/` pages).

## Progress

- [x] TAKEN posted on #629
- [x] Item 1: clause double check (below)
- [x] Item 2: code map with file:line (below)
- [x] Item 3: design options and recommendation
- [x] Item 4: design note and index row, gates, commit `78d4fef2`
- [x] PR-BODY.md (this directory)
- [x] DECISION posted on #629: comment 5935490330 (text: `decision.md` here). STOPPED.

## Clause findings

(a) INPUT_STREAM source per AAF input beside the CRF source:
- Milan v1.2 5.3.3.6: exactly one INPUT_STREAM CLOCK_SOURCE per CRF Stream
  Input, or, when the Configuration has no CRF input, for the single AAF
  Stream Input. It is a minimum. It neither requires nor forbids an
  INPUT_STREAM source on an AAF input when a CRF input exists. INTERNAL is
  required when there is a Stream Output. No ordering rule.
- IEEE 1722.1-2021 7.2.9 / 7.2.9.2: INPUT_STREAM = "sourced from the media
  clock of an Input Stream"; location fields name the descriptor (STREAM_INPUT k).
- IEEE 1722.1-2021 7.2.32: `clock_sources` is the list the index may be set to;
  `clock_sources_count` max 216 (508-octet descriptor). No order rule.
- Processor rule (not a clause): the list must be the identity permutation
  (protocol-processor `docs/architecture/07_memory_maps.md:135`, L6).
- Milan 8.3.2.3.3 (redundant pairs) not applicable (non-redundant).

(b) Listener when the selected stream stops:
- MUST: Milan 5.3.11.1 the domain is always using one listed source, and the
  selected source is saved state; Milan 5.4.2.15 no change by non-ATDECC means
  while locked by a controller -> no autonomous fallback that rewrites the index.
  Milan 5.3.11.2 (Table 5.7/5.15) LOCKED/UNLOCKED invariant (definition open).
  Milan Table 5.6 MEDIA_UNLOCKED on the stream input.
- MAY: hold over (1722-2016 4.4.4.7 NOTE: free-wheel when tu; 4.4.4.3/10.4.3:
  restart "need not be seamless", take "any appropriate action"); restart
  recovery when the stream returns. Milan specifies no holdover time.

(c) `mr` for a talker following a received stream:
- 1722-2016 4.4.4.3: toggle on a change of the media clock source; hold >= 8
  AVTPDUs. SHALL toggle when a received CRF stream it derives timestamps from is
  disrupted or its `mr` toggles (CRF only, literally).
- 1722-2016 10.4.3: a CRF listener shall use `mr` to adjust quickly and shall
  toggle `mr` in outgoing streams deriving timestamps from the CRF stream; only
  the `mr` of the stream used for recovery is valid (also 4.4.4.3 last para).
- PICS Table F.7 AAF-5/AAF-6 (source change, 8-PDU hold) are mandatory.
- For a followed AAF stream: no literal shall on disruption or echo; the
  source-change rule applies; toggling on disruption and echoing the followed
  stream's `mr` is permitted and is the design's recommendation.
- Phase: 1722-2016 10.8 (Eq. 15) talker timestamps within +/-5 % of a sample
  period of the CRF timing points (shall); 4.3.5 integer-multiple rule for
  streams generated from a recovered stream. The fabric is frequency-locked
  only, so neither holds by construction: a pre-existing gap, proposed as a
  separate issue.

(d) What the repository's reading gets wrong:
1. 5.3.3.6 paraphrase is right as a minimum but used as an exclusive set
   (FR-CLK-03 "No CLOCK_SOURCE is advertised on an AAF listener"; L6 "AAF-derived
   sources are unsupported"). The exclusion was #389 decision (a), not the clause.
2. "unlisted index gets BAD_ARGUMENTS" is not in Milan 5.4.2.15/16 or 1722.1
   7.4.23.1; it follows from 7.2.32's list and Table 7-141's BAD_ARGUMENTS.
   7.4.23.1 adds: the response carries the current (old) value on failure.
3. Builder and model messages cite Milan 7.2.2 for "only INTERNAL and the CRF
   sink drive the media clock"; 7.2.2 only requires a CRF input to exist.
4. #74's note cites Milan 7.2.3 for "CRF output must represent the same media
   clock as its AAF streams"; 7.2.3 only requires the output to exist. The
   correct basis: 1722.1-2021 7.2.32 (a CLOCK_DOMAIN is one common clock) with
   7.2.6 (each STREAM_OUTPUT names the domain providing its media clock), and
   the Milan 7.1 note. A2 stands on that basis.
5. #629's body says 4.4.4.3 disruption `mr` "applies to AAF and CRF following
   alike"; the shall names CRF only (see c).
6. Stale RTL comments: `hdl/milan/milan_datapath.sv:607` and `:5576-5578` say
   the root cannot select CRF (false since #74).
7. Compliance matrix 7.2.3 row (`docs/reference/MILAN_COMPLIANCE_MATRIX.md:187`)
   reads "implemented" with no A2 caveat.

## Code map (dev d4dd7426)

Builder / AEM model:
- `configs/endstation_ax7101_1x1_tdm8.yaml:128` (also arty_8ch:132,
  ax7101_8x8:146, arty_4x4:96, arty_current:166): `[internal, crf]`.
- `sw/builder/endstation_builder.py:3874-3972` `_load_clocking`; refusal of
  `input_stream` 3887-3899; set 3900-3902; CRF sink rules 3956-3971.
- `sw/builder/endstation_builder.py:5018-5045` `_overlay_clock_sources`:
  INTERNAL then CRF located on STREAM_INPUT len(L) (5040-5044).
- `sw/builder/endstation_builder.py:2836-2853` emits `AEM_N_CLKSRC_C`,
  `AEM_CRF_CLKSRC_C`; generated `configs/generated/*/gen/adp_shape_defaults.svh:54-55`.
- `sw/builder/endstation_builder.py:3292-3301` servo prune gate;
  `:3414-3419` model_shape carries the set; `:4262-4267` INTERNAL with outputs.
- `avdecc/aem_specs.py:22` CS_TYPE, `:35` CS_RETIRED, `:234-241` refusal, `:267-272`.
- `avdecc/aem_descriptors.py:428-442` clock_source_shape, `:445-462`
  d_clock_source, `:464-482` d_clock_domain (identity list).
- `avdecc/aem_assemble.py:231-236`, `avdecc/aem_emit.py:220-224`.
- pre-#389 order (INTERNAL, per-listener, CRF): `git show aea44c071^:sw/builder/endstation_builder.py` lines 4180-4203.

Processor (submodule b2db3a97, read-only):
- `protocol-processor/hdl/aecp/ucode/gen_ucode.py:1410-1419` range-check
  rationale; `:1436-1440` count, CHECK_ARG, WRITE_ST, NVM_MARK; refusal tail
  carries the current index.
- `protocol-processor/hdl/aecp/KL_aecp_nvm_writer.sv:87-89` restore value rule
  (index below count).
- `protocol-processor/hdl/aecp/KL_aecp_dyn_state.sv:114,352` exports domain 0 only.
- `protocol-processor/docs/architecture/07_memory_maps.md:135` (L6), `:343`, `:479`.
- `protocol-processor/docs/00_MILAN_COMPLIANCE_REVIEW.md:377` (REQ-AEM-013), `:420` (REQ-MDL-005).

Fabric:
- `hdl/milan/milan_datapath.sv:684-706` source banner and nets;
  `:1554-1570` media_clk_resolve (one compare against AEM_CRF_CLKSRC_C).
- `:3108-3156` mr triggers (CRF disruption, CRF mr echo, gated by
  crf_clk_selected_r); `:3180-3203` KL_media_clock_restart (source-change edge
  inside, `KL_media_clock_restart.sv:211-213,230`).
- `:3469-3475,3492,3509` CLOCK_DOMAIN LOCKED/UNLOCKED level = ~clkv_tu_w.
- `:5418-5446` parser bundle (match, idx, ts, tv, tu, mr, seq, fsh).
- `:5508-5572` KL_crf_rx (en/sid 5537-5538, locked 5564).
- `:5594-5637` KL_mmcm_drp_servo (select/rate ports 5608-5612).
- `:5639-5719` chain banner; `:5713-5718` INTERNAL free-run rule.
- `:5733-5748` KL_media_grid_align sel = crf_clk_selected_r; NCO enable.
- `:5756-5758` KL_crf_tx on clk_audio_i.
- `:5834-5866` rx monitor; `:5858-5865` clk_src inert; `:5905` last_ts_o.
- `:2576` PCMRX_TS = stream 0 last accepted avtp_ts
  (`KL_avtp_rx_monitor_ctx.sv:218`; `milan_csr.sv:396,771,2371`).
- `:6079-6126` #386 recentre (src_grid_ok 6091-6092); `:6153` i2s servo_en.
- `hdl/ieee1722/crf/KL_crf_rx.sv:21-44` outputs, `:275-277` window,
  `:296-298` lock, `:390-403` era breaks and rate_valid.
- `hdl/ieee1722/crf/KL_mmcm_drp_servo.sv:20-30` rate-only error,
  `:166-170` states, `:263-273` ports, `:411` select, `:538-551` IDLE resets u,
  `:571-579` HOLDOVER -> ACQUIRE with win_skip.
- `hdl/ieee1722/crf/KL_media_grid_align.sv:38-41,95-100,247-272`.
- `hdl/ieee1722/crf/KL_crf_tx.sv:20-28` CRF grid = clk_audio_i / 512 (A2 cause).
- `hdl/ieee1722/aaf/KL_aaf_packetizer.sv:720-726` AAF ts latched on the packet grid.

Area reference measured here: `syn/yosys/ooc.sh KL_crf_rx` with OOC_SHAPE =
1x1 TDM8: 433 LUT, 544 FF, 1 RAMB18, 147 CARRY4 (Yosys estimate, not placement).

## Design options and recommendation

Full text: `docs/design/MEDIA_CLOCK_FOLLOWING.md` at `78d4fef2`.

- Reuse everything after the servo input. New: an AAF clock meter on the
  selected listener (parser bundle tap), keeping one timestamp in 96/spf
  (16 at Milan 6.2's 6 samples per PDU) = the CRF 96-sample 2 ms spacing, then
  KL_crf_rx's ring, era and lock rules -> rate in the servo's units.
- Decode in media_clk_resolve against a generated per-index table (kind,
  STREAM_INPUT index): crf_clk_selected_r, aaf_clk_selected_r,
  aaf_follow_idx_r, follow_sel_r. Servo select becomes 1-bit (follow_sel_r);
  reference mux CRF / meter; aligner, NCO enable, #386 settle and I2S servo_en
  on follow_sel_r. Servo ports crf_* -> ref_*.
- Holdover = servo HOLDOVER, indefinite, index unchanged, no fallback.
- mr: source change (existing); CRF triggers (existing); AAF meter lock fall
  and received toggle gated by aaf_clk_selected_r; #387 merge -> one toggle.
- A2: fixed under following (B CRF evidence); at INTERNAL needs D4.

| ID | Recommendation |
|---|---|
| D1 order | L1: INTERNAL 0, CRF 1, AAF k at 2+k (saved state keeps meaning) |
| D2 measurement | M1: one meter on the selected input (vs M0 packet-grid compare, M2 per-input, M3 shared ring) |
| D3 switch | W2: HOLDOVER then ACQUIRE, reference shown unlocked one cycle on every change (vs W1 via IDLE) |
| D4 A2 at INTERNAL | A2-a: aligner engaged at INTERNAL too (reverses the INTERNAL free-run rule) |
| D5 domain counters | C1: locked = clock valid and (INTERNAL or servo LOCKED) |
| D6 configs | all five, one regeneration |
| D7 phase (10.8, 4.3.5) | new issue |

Area: meter 250-350 LUT, 200-300 FF, 1 RAMB18; decode+mux 50-80 LUT, 20-40 FF;
servo compare -10 LUT; A2-a < 5 LUT. Total about 300-430 LUT, 220-340 FF, 1 RAMB18.

## Parent-visible changes

- Requirements: FR-CLK-03, FR-CLK-04, status row (`docs/reference/FR_NFR.md:155,237,238`).
- Config: `media_clock_sources` re-admits `input_stream` (one per AAF listener); five shipping configs.
- Builder: `_load_clocking` (3887-3902), `_overlay_clock_sources` (5018-5045, append after CRF),
  names (134-141), shape header tables (2836-2853); servo prune gate unchanged.
- Model: `avdecc/aem_specs.py` CS_TYPE/CS_RETIRED; `clock_source_shape` tables; `aem_emit.py`.
  New entity_model_id per regenerated image (1722.1-2021 6.2.2.8).
- Generated: shape headers, AEM images, `hdl/common/gen` via `--write-rtl`.
- RTL: new meter module (beside KL_crf_rx); root decode and consumers; AAF mr triggers;
  A2-a / C1 if taken; stale comments 607 and 5576-5578; servo select port and ref_* rename.
  Unchanged: KL_crf_rx, KL_crf_tx, KL_media_grid_align, KL_media_nco, KL_media_clock_restart.
- No new top port, pin, SoC change or root parameter.
- Registers: two RO words in unmapped 0x8E0-0x8F4 (REGISTER_MAP.md:1833): meter status, meter rate. VERSION bump.
- Docs: TIME_SYNC Media boundary, compliance matrix rows, PP_DESCRIPTOR_OWNERSHIP L6,
  ENDSTATION_BUILDER row 9, builder README-parameters, feature ledger.

## Processor-visible changes

Own protocol-processor issue (to be filed by the manager): "SET/GET_CLOCK_SOURCE over
INTERNAL, CRF and one source per AAF input (milan-fpga #629)".
- RTL/microcode: none (range check gen_ucode.py:1410-1440 and restore check
  KL_aecp_nvm_writer.sv:86-90 accept any index < count over an identity list).
- Docs: 07_memory_maps.md:135 (L6), 00_MILAN_COMPLIANCE_REVIEW.md:420 (REQ-MDL-005).
- Tests: 10-source domain, index 9 accepted + notified + read back; index 10 BAD_ARGUMENTS
  with current index; D3 save/restore of an AAF index; restore refusal above a smaller count.
- Then a parent submodule pin bump.

## Test plan

Simulation (each with a failing mutant): meter suite (rate vs KL_crf_rx within 1 LSB at
0/+-10.64/+-50/+-100 ppm; lock/unlock; era restarts incl. 32-bit wrap; selection filters);
mmcm_servo (1-bit select, switch with select held keeps integrator; W1 mutant fails);
milan_dp true-ratio leg (each source in turn within 0.5 ppm, zero junction slips; switches:
one mr toggle per output per switch, one #386 recentre, aligner engaged, SLIP_TDM static;
lock loss AAF and CRF: HOLDOVER, one toggle, none on return; followed-AAF mr echo gated);
AECP model walk; builder tests.
Bench (B6 method): B AAF (DUT follows peer AAF on STREAM_INPUT 0, index 2), B CRF repeat,
B INTERNAL control, A1 repeat, A2 at INTERNAL (passes only under A2-a), A2 under following
not run (clock loop) and graded through B AAF/B CRF, lock loss (unbind 10 s), synthetic controls.

## Gates

At `78d4fef2`, pinned Markdown environment, outputs to files under /tmp, never piped, all rc 0:
- `scripts/docs_check.py`: 0 findings, 184 md + 955 scrubbed files.
- `scripts/check_doc_style.py`: OK.
- `scripts/gen_toc.py --check`: OK; `--verify-anchors`: 292 links reproduced.
- `scripts/check_em_dash.py --base d4dd7426`: 0 findings over 578 added lines.
- `scripts/check_doc_paths.py`: OK, 871 paths.
- `scripts/check_feature_status.py --self-test`: rc 0.
- `git diff --check` and `git diff --check d4dd7426 HEAD`: clean.

An earlier commit `bc1741dd` failed `docs_check` (bare .md references and processor
.md paths as dead references); it was amended into `78d4fef2` before anything was
published. Not pushed.

## Notes for the manager

- Pushing the branch and opening the PR (body: `PR-BODY.md`) are yours.
- File: the protocol-processor issue (above) and, if D7 is accepted, the phase-alignment issue.
- B6's page (PR #630) was unmerged at writing; the design cites it through the PR.

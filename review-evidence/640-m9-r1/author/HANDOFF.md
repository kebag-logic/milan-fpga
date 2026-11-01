# HANDOFF - [A720] issue #640 Mark II charter (docs only)

Status: REVIEW READY at head dfc310fb3dec28f3d06333973e61cde44a4e786d (2026-11-01). Local only, nothing pushed.

- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6550573360
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6551084628
- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter, base dev e5b8405db4c1f7cbdafb5df92b15b580142e0232.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- Scratch: $VALIDATION_STORAGE/640-a720 (issue dumps, standards text extracts, gate logs, export). Evidence copies (small): ./evidence/.

## Commits (one per file group, one-line subjects, no body, no trailers)

| # | SHA | Files | Deliverable |
|---|---|---|---|
| 1 | 4083cea5baf984ae113ece054f3dcc3df87a503d | docs/reference/FR_NFR.md | 1 |
| 2 | cf342310580f777f1a6f392b3df44acd347bc74a | docs/ARCHITECTURE_HW_SW_SPLIT.md | 2 |
| 3 | 8ad286590896e3d34f2935322f2534261784b9e5 | docs/design/MARK_II_STREAM_ENGINES.md (new), docs/README.md (index row) | 4 and 5 |
| 4 | dfc310fb3dec28f3d06333973e61cde44a4e786d | docs/design/MARK_II_AREA_PLAN.md | 3 |

## Sources read (all of it before writing)

- #640 body ("Updated 2026-10-31" first) and its 2026-10-31 comments: 6538132102 (daily measurement), 6545523624 (16:39 target), 6545540394 (16:40 lever order), 6545621753 (16:47 shape), 6545655255 (16:51 gPTP), 6545820658 (17:04 flexptpd and 65 us), 6545999204 (17:21 LiteX stages).
- #665 body and 2026-10-31 comments 6545457321 (16:33 processor removed), 6545523910 (16:39).
- #823 body and 2026-10-31 comments 6545894131 (17:11 save), 6545924397 (17:14 confirmed).
- #664 (closed) body, for the requirement-change scope it already landed.

## Changes, file:line, and source

### docs/reference/FR_NFR.md (commit 1)

| Line | Change | Source |
|---|---|---|
| 301 | NEW NFR-LAT-03: every talker stream, last sample at the TDM pin to first bit on the wire, below 65 us, as short as possible; verification A (derivation) and T (AAF latency taps, bench, 32x32) | #640 6545820658; IEEE 802.1Q-2022 8.6.8.2, 34.6.1.1; Milan v1.2 4.3.4 |
| 465 | NFR-RES-01 amended: Mark II below 20,000 LUTs at 32x32, as few as possible, fits BRAM, timing at every corner; Mark I bound 60 % (38,040) kept for the current all-fabric image; verification A | #640 6545523624 |
| 468 | NEW NFR-REL-03: saved-state change durable within 0.5 s worst case at 32x32; no erase on the save path; verification A and T | #823 6545924397, 6545894131 |
| 323 | NFR-SCOUT-02: firmware only in the end state; all-fabric default only until bench qualification, then deleted, no dual maintenance; gPTP to firmware under #665 F6, fabric plane owner until F6 qualifies; timestamps on both ports stay fabric | #665 6545457321; #640 6545820658 |
| 324 | NFR-SCOUT-03: audio deadlines fabric-only; gPTP deadlines fabric-only until F6, then per-path firmware bounds | #640 6545655255, 6545820658 |
| 326 | NFR-SCOUT-05: Mark II adopts Milan v1.2 Section 8 redundancy at 32x32; current release stays one port; design approved before RTL (REQUIREMENTS.md section 9) | #640 6545621753 |
| 490, 492 | Section 4.2 plane table: Control and Time owners restated (transition, F6) | same |
| 586 (blockquote) | Out-of-scope note: Mark II adopts redundancy | #640 6545621753 |
| 604-609 | Traceability rows: Streaming adds NFR-LAT-03 and Milan 4.3.4; new Saved state row (Milan v1.2 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.2, 5.3.8.7, 5.3.9.1, 5.3.13 each say "saved in a non-volatile memory"); Redundancy row | Milan v1.2 text read |

Why NFR-SCOUT-02/03/05 were touched: the decisions directly contradict their old text ("gPTP ... MUST remain fabric-owned", "all-fabric remains supported", "redundancy out of scope for v1.2"). Leaving them would leave a contradiction in the tree next to the restated split. They are docs, so amendable under the lane rules; no STOP. REQUIREMENTS.md is the contract for VERSION 0x0002_0060 (the current product) and stays true until each switch-over; it was not edited.

### docs/ARCHITECTURE_HW_SW_SPLIT.md (commit 2)

| Line | Change | Source |
|---|---|---|
| 3-15 | Intro: Mark II moves every control protocol to firmware; no retained-fabric option; all-fabric default only until bench qualification; then deleted | #665 6545457321 |
| 36-58 | Ownership table re-columned "Shipping image until the switch-over" / "Mark II end state"; gPTP row to firmware (flexPTP-based daemon, per interface, F6); new PHC/timestamp row (802.1AS-2020 8.4.3); new milan_csr row (information and diagnostics, D2); MAAP/SRP per interface (Milan v1.2 8.3.3.1, 8.3.5) | #640, #665 2026-10-31 |
| 72 | NEW "Mark II end state": the decisions, each linked | as listed |
| 96 | NEW "Transition and deletion": the removed permanent all-fabric option; processor and build switch deleted at the switch-over; fabric gPTP plane follows the same rule at F6 | #665 6545457321 (manager default confirmed in #665 body) |
| 216, 227 | Publication boundary and option OFF scoped "until F6" | #640 6545655255 |
| 255 | Known incomplete: F6 licence, stream engines design only, #823 format, LiteX stages, BRAM | this lane's findings |
| 314, 318, 335 | Flip: F1 to F5 evidence; deletion of processor, build switch and major-2 leg at the flip | #665 2026-10-31 |

### docs/design/MARK_II_STREAM_ENGINES.md (commit 3, new)

Sections (line): scope 29, wire load 46, shared engines 74, capture buffer 116, stagger 134, talker latency budget 163 (shaper 171, schedule 204, budget 230, fewer reservations 254), listener and render buffer 280, redundancy pairing and merge 318, per-port units 365, register maps 387 (engine 398, talker context 423, listener context 454), BRAM ledger 491, 0.5 s save path 542 (maxima 556, sequence 577, derivation 595, compaction 620, assumptions 653), verification 672, open questions 686.

Clauses cited (each read in the standard): IEEE 1722-2016 4.3.2, 4.4.4.3, 4.4.4.6, 4.4.4.7, 4.4.4.8, 4.4.4.9, 7.5, 7.6; IEEE 1722.1-2021 7.2.6; IEEE 802.1Q-2022 8.6.8.2, 34.3, 34.4, 34.6.1, 34.6.1.1, 34.6.1.2, L.3.1.1; IEEE 802.1AS-2020 8.4.3; IEEE 802.1BA-2011 6.3, 6.5; Milan v1.2 4.3.3.2 (Table 4.4), 4.3.4, 5.3.7.3, 5.3.7.6, 5.3.7.7, 5.3.8.2, 5.3.8.7, 5.3.8.10, 5.3.9.1, 6.2, 8.2.2, 8.2.4, 8.2.5, Annex C, 8.3.1, 8.3.2.1.4, 8.3.4, 8.3.5.1. Flash: N25Q128 datasheet Table 32, Table 17, section 9.1.20 (datasheet sha256 c252fc3debfb41eda5955c30ad7f18f03b0ca4bd38b591e203a566cb1264186c).

docs/README.md:80: index row "Review the Mark II 32x32 datapath".

### docs/design/MARK_II_AREA_PLAN.md (commit 4)

| Line | Change |
|---|---|
| 1-10 | Intro: Mark II sections govern; Mark I sections are history |
| 33 | Summary rewritten for Mark II |
| 50 | Target: Mark II ceiling, shape, BRAM, timing, #818 gate comparison, latency, save, function, gate, start; Mark I bound row kept |
| 71 | NEW measured basis (route of build_ax7101_asl_e240b77bbd) with report digests and hierarchical rows |
| 134 | NEW Mark II levers: owner's derivation of 34.2k, owner's 16:40 table verbatim (least risky first), 32x32 additions, further levers |
| 186 | NEW LiteX removal stages |
| 221 | NEW Mark II block RAM ledger |
| 242 | NEW Mark II decisions D10 to D17 |
| 255 | NEW Mark II lane sequence |
| 283 | NEW Mark I plan history marker |
| 681, 757, 783, 815 | 2026-10-31 notes on L2, L6, L8, L10 (as #665 6545457321 asked) |
| 1497, 1504 | What holds throughout: gPTP after F6; redundancy adopted |
| 1547 | D9 row: all-fabric until D11 deletes it |

## Measured basis: where the reports were found (please note)

The prompt said to search $VALIDATION_STORAGE and $WORKSPACE_HOME/prjs-avb-on-fpga. A find over both found no `*e240b77bbd*`. A wider find found the build at $WORKSPACE_HOME/litex-milan/work/build_ax7101_asl_e240b77bbd (outside the two named roots). I read its reports there (read-only) and cite them; the docs name only the build and report file names and digests, no paths. If that location should not have been used, the fallback is the #640 figures, which agree: 52,008 LUTs, 87.5 tiles, 13 DSP.

- Source commit: 40b77bbd61 "Qualification image: eth_port e2", a local commit on a merge of PR #826 into 787-reboot-reset (worktree build-dev-e2-40b77bbd). Not on origin; the plan says "not on dev".
- Design state of the utilization reports: "Physopt postPlace". Route status: 103,262/103,262 routed, 0 errors. Signoff: WNS +0.129 ns (slow corners), WHS +0.036 ns (fast corners).
- Directives: synth AreaOptimized_high, opt ExploreArea, place AltSpreadLogic_high, phys_opt AggressiveExplore, route AggressiveExplore.

| Report | Bytes | SHA-256 |
|---|---:|---|
| alinx_ax7101_utilization_place.rpt | 13,375 | d9561a05dee55ef0c0f8f9350bfe27ea63b215639afdf708f2f4f00aba70356e |
| alinx_ax7101_utilization_hierarchical_place.rpt | 30,075 | ec345a49f14e03038c428bb23029872639085de825038b8a99539e0fee08f42d |
| alinx_ax7101_route_status.rpt | 651 | 22ed0c58b84876ae9ac2253b8291a1d760aa95f3f9d1d78112679dc5e8e42378 |
| alinx_ax7101_signoff_all_timing.rpt | - | 3632d97a686d8ace0a874bfa49af79a71089538eccfa3bef51e3e8afe4a37cef |

## Derived numbers and their derivations

Wire load (Milan v1.2 6.2, Table 4.4; 1722-2016 7):
- AAF 8 ch x 6 samples x 4 octets = 192; AVTPDU 216; wire 216 + 22 + 20 = 258 octets = 2,064 bits = 2.064 us.
- Table 4.4 bandwidth 1536 x 8 + 4288 = 16,576 kb/s; per port 16 x = 265.216 Mb/s (26.52 %); with CRF 5,632 kb/s: 270.848 Mb/s (27.08 %).
- Frames: 16 x 8,000 = 128,000/s per port; 256,000/s both ports each way.

Shaper (802.1Q-2022 8.6.8.2): spacing = L / idleSlope. 2,064 / 270.848e6 = 7.6205 us; CRF 704 / 270.848e6 = 2.5992 us; phase period 125/6 = 20.833 us. Schedule (preferred order 3,3,2,3,3,2, CRF in phase 2): worst wait 18.333 us (phase 4); phase 5 frees the shaper at 124.527 us < 125. All 90 orders (15 placements of the two light phases x 6 CRF phases): worst 23.925 us (2,2,3,3,3,3). Interference (802.1Q-2022 L.3.1.1; 802.1BA 6.3): (1522 + 20) x 8 / 1e9 = 12.336 us.

Byte-resolution model (evidence/cbs_sim.py, sha256 221a822800757ae5ccf55cb19de12df9c23448e4a91c2e439511761b33d3cb41; not committed, not a gate): full load preferred order 18.336 us, with saturated best effort 30.352 (max) / 30.632 (random sizes) <= 18.333 + 12.336 = 30.669; worst order 23.928. Partial loads: lone pair 62.264, lone triple 83.016 (95.320 with max-size best effort), pair phases 0/1 41.424, pair phases 0/3 0.

Talker budget (worst slot = slot 0, frame-end release):
- pin to capture 7 x 32 / 12.288 MHz = 18.229; CDC 0.200 (estimate); packetizer 6 x 1.28 + 2 x 0.44 = 8.560 (estimate: 64 cycles at 50 MHz per 8-ch frame, 22 per CRF); MAC+PHY 1.000 (426 ns register stages per REQUIREMENTS.md section 4 + 219 ns egress_latency_ns from the 1x1 config + margin).
- Preferred order: 18.229 + 0.2 + 8.56 + 18.333 + 12.336 + 1.0 = 58.658 us (margin 6.342).
- Worst order: 64.250 us (margin 0.750). Slot 7, worst order: 46.021 us.
- Consequence not in the docs (my reading, not verified against the #773 implementation): the #773 AAF stamp rule (CHANGELOG) stamps 8 periods (166.667 us) after the PDU's first frame instant. If that instant is the first sample, Mark II departure = 104.167 + 64.250 = 168.417 us at slot 0 worst order, so frame-end release would need a 9th period (still within Milan 5.3.7.6's 125 us fixed delay); 104.167 + 46.021 = 150.188 us keeps 8. The PR body only says the delay must be re-derived.

Engine throughput (estimate): 4 + 5 + 6 + 48 + 1 = 64 cycles = 1.28 us per 8-ch frame at 50 MHz, 32-bit; 256,000 x 1.28 us = 32.8 % load; 1,600 Mb/s capacity vs 528 Mb/s of stream frames.

Buffers: capture 8 x 16 x 32 = 4,096 bits = one RAMB18; render: 2.000 + 0.125 + 0.125 ms = 2.25 ms = 108 samples -> 128; 8 x 128 x 32 = 32,768 bits = one RAMB36. Listener lookup 16 contexts / 2 per cycle = 8 cycles = 160 ns vs 672 ns minimum frame.

BRAM ledger (estimates except mailbox, milan_csr, CPU which are measured): fabric 24.0 tiles; firmware extrapolated from SPLIT_CONTROL_MEMORY.md section 5 two-interface points: rom 98,056 + 62 x 985 = 159,126; sram 57,152 + 62 x 3,951 = 302,114; total 461,240 B / 4,096 = 112.6 -> 113; stage 3,344 + 62 x (13,264 - 3,344)/14 = 47,275 B = 11.5 tiles; gPTP allowance 16 (unmeasured). Total 24 + 113 - 11.5 + 16 = 141.5, 20 over 121.5. Names 907 x 64 = 58,048 B = 14.2 tiles.

Save path (N25Q128 Table 32 maxima): t_page = 0.166 (PP command 260 octets at 12.5 MHz) + 0.011 (WREN, polls, allowance) + 5.000 (tPP) + 0.166 (read-back) = 5.343 -> 5.35 ms. P_max 32 pages. T_worst = 10 (T_svc) + 1 (suspend allowance; Table 17 gives only a 15 us typical) + 2 x 32 x 5.35 = 353.4 ms <= 500 (margin 146.6 ms, 29 %). Slot 4 sectors = 1,024 pages; image 240 pages (#823 estimate); append space 784; trigger at 392 free; compaction 240 x 5.35 = 1.28 s; erase 4 x 3 s = 12 s; boot read 256 KiB x 8 / 12.5e6 = 168 ms. Flash rate 1/5.35 ms = 187 pages/s; S2 10 % = 18.7 pages/s = 4.8 KB/s. Burst of all 907 names at about 80 octets per record = 72,560 octets = 284 pages = about 1.5 s.

Area (central, estimates): owner 52,008 - 24,354 - 481 + 3,948 + 3,102 = 34,223; owner levers -> ~20.7k (owner range 19.1k-22.4k from the 15:39 ranges); +1.75k second port (TCAM 494 + timestamp units 192 + 218 + 32 = 442 placed, MAC unmeasured); +1.0k engines; -1.75k LiteX stages 2-3 beyond levers 1-2; -0.5k L3/L4/FIFO trims -> ~21.2k (17.6k-25.2k). Placed rows: crossbar and endpoints 835 + 143 + 77 + 499 + 368 + 627 + 265 + 475 = 3,289; diagnostics 671 + 285 + 721 + 527 = 2,204; other datapath rows by difference 43,425 - 41,389 = 2,036.

## Why no STOP

- Contradicted requirements (NFR-SCOUT-02/03/05, plus NFR-RES-01) are docs and were amended; REQUIREMENTS.md describes the current VERSION and stays true until the switch-overs.
- The 65 us budget IS shown under the shaper at the 32x32 shape with the stated idleSlope assumption (Table 4.4 sum of the port's 16 reserved AAF streams plus one CRF): 58.658 us preferred order, 64.250 us worst order. The prompt asked to "state any assumption about idleSlope"; that assumption is stated.
- It is NOT shown for every smaller load: with fewer reservations idleSlope shrinks, and two or three co-phased streams left alone wait 62.3 to 83.0 us for credit (74.6 to 95.4 us with interference). Re-phasing breaks 1722-2016 7.6; padding breaks Milan Table 4.4. Published as open question 1 in the design page and in REVIEW READY, and NFR-LAT-03 keeps the owner's wording with the open question named. If the manager reads the STOP rule as covering partial loads, this is the point to stop the lane.

## Open questions published (design page, Open questions)

1. Talker latency below the 32x32 load (owner reading).
2. Save bursts beyond S1 (more than 32 pages changed during one save) exceed 0.5 s at datasheet maxima.
3. BRAM: the 32x32 estimate is 20 tiles over the usable ceiling.
4. The 500 ms / 1,000 ms debounce windows (SAVED_STATE_MATERIALIZATION.md DR2a) exceed 0.5 s; #823 and F1 must restate them.
5. The gPTP daemon's source and licence (#665 F6).

## Gate table (committed head dfc310fb, clean tree)

| Gate | Command | rc | Result |
|---|---|---:|---|
| docs_check | python3 scripts/docs_check.py | 0 | 0 findings, 211 md + 1427 scrubbed files |
| docs_check without .git | git archive HEAD into scratch; python3 scripts/docs_check.py | 0 | 0 findings (inventory parity skipped, needs git) |
| feature status | python3 scripts/check_feature_status.py | 0 | 0 findings |
| feature status self-test | ... --self-test | 0 | 0 findings |
| feature status without .git | export copy | 0 | 0 findings |
| em dash | venv python3 scripts/check_em_dash.py --base e5b8405d | 0 | 0 findings over 1,095 added lines in 5 pages |
| em dash self-test | venv ... --selftest | 0 | 339 arms |
| doc style | python3 scripts/check_doc_style.py | 0 | OK, 23 current documents |
| doc style self-test | ... --selftest | 0 | OK |
| doc style on touched pages | evidence/style_touched.py (the checker's own analyze() on blocks this change adds) over the 5 touched pages | 0 | 0 findings in changed blocks |
| gPTP docs | python3 scripts/check_gptp_docs.py (+ --selftest) | 0, 0 | OK, 30 controls |
| TOC self-test | venv python3 scripts/gen_toc.py --selftest | 0 | 1501/1501 arms |
| TOC anchors | venv ... --verify-anchors | 0 | 563 cross-page fragment links reproduced |
| TOC check | venv ... --check | 0 | 150 pages carry contents |
| doc paths | python3 scripts/check_doc_paths.py | 0 | 1075 cited paths resolve |
| traceability | python3 docs/traceability/gen_module_matrix.py --check | 0 | up to date |
| doc map | python3 docs/DOC_MAP.gen.py --check | 0 | OK |
| solution docs | python3 scripts/check_solution_docs.py | 0 | OK |
| archive | python3 scripts/check_archive.py | 0 | OK |
| submodule docs | python3 scripts/check_submodule_docs.py | 0 | OK |

Not run: wire-accountability self-test (needs the gptp-processor submodule; this lane has no submodules) and the non-docs jobs of the workflow. Pinned venv: $VALIDATION_STORAGE/818-mdvenv (cmarkgfm + html5lib); TOC blocks regenerated only through gen_toc.py --write. Logs: ./evidence/*.log.

## Not done / not allowed

No push, PR, merge, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited.

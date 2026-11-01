[R758] NEGATIVE - exact head dfc310fb3dec28f3d06333973e61cde44a4e786d

Round R758-1, external independent review of PR #828 (issue #640, with #665 and #823).
Head `dfc310fb3dec28f3d06333973e61cde44a4e786d`, tree `4881b68d4cbb69d920bc154af3ded7d14fa3e83c`,
source base `e5b8405db4c1f7cbdafb5df92b15b580142e0232` (also the live dev tip at review time).
Delta: five Markdown pages, 1,095 added lines, four commits, no code, generator, gate or configuration change.

Verdict basis: one BLOCKER, four MAJOR and seven MINOR findings are open. Every lens is applied and every
lens is UNCLEAN at this head (ledger below). The owner's 2026-10-31 decisions themselves were not
reviewed; only how faithfully and correctly this delta records and derives from them.

## Findings

### R758-1-F1 BLOCKER - Docs, Tests - docs/design/MARK_II_AREA_PLAN.md:155 and :268 - a required documentation gate is red at this head

- Authority/evidence: the documentation workflow's bare-metal scope gate (`scripts/check_baremetal_only.py --check`,
  part of the required `docs-check` context). Hosted run 41256380559 at this exact head: job `docs-gates-0` step 28
  "Bare-metal scope gate" failed with `baremetal-only: FAIL (2 finding(s) across 1425 scanned file(s))`, both on added
  lines naming the retired surface `hostplane` (`[H] retired target host-plane surface`, #259). `docs-check` then failed
  its "Require every gate exactly once" step, and legs 1 and 2 were cancelled. Reproduced locally on the clean clone:
  rc 1, same two findings (`receipts/gates/baremetal_only.log`, `.rc`); the gate's self-test passes (867 arms). The
  base page has no `hostplane` (count 0), so the delta introduces both. The author's published validation list
  (REVIEW READY and `review-evidence/640-m9-r1`) does not include this gate.
- Impact: the required `docs-check` context cannot pass, so the head cannot merge, and the published "all docs gates
  green" evidence is incomplete.
- Required outcome: neither line names the retired surface (the owner's quote can be paraphrased, for example
  "host-side tooling"), and the full docs-workflow gate set is run and recorded on the new head.
- Verification: `python3 scripts/check_baremetal_only.py --check` rc 0 on the new head; hosted `docs-check` green.

### R758-1-F2 MAJOR - Conformance, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:57 and :230-252; docs/reference/FR_NFR.md:301 (NFR-LAT-03) - the 32x32 latency bound fails with mixed channel counts

- Authority/evidence: the page states "The worst case is eight channels on every stream" and derives 58.658 / 64.250 us
  from it. NFR-LAT-03 says the design "derives the bound at the 32x32 shape" and scopes the open question to "fewer
  reservations". Under IEEE 802.1Q-2022 8.6.8.2 a frame's class spacing is L / idleSlope, and idleSlope is the Table 4.4
  sum (34.6.1.1). With all 16 streams per port running but mixed formats, the sum shrinks while 8-channel frames keep
  their length. Milan v1.2 6.2 allows N in {1, 2, 4, 6, 8}, and the context maps allow any channel count.
  Independent exact-arithmetic model (`scripts/cbs_mixed.py`, `receipts/cbs_mixed.out`): at the preferred order
  `3, 3, 2, 3, 3, 2`, CRF in phase 2, with six 8-channel streams in phases 0 and 1 and ten 1-channel streams elsewhere,
  the last frame waits 42.875 us. With the page's other terms (18.229 + 0.200 + 8.560 + 12.336 + 1.000) the total is
  83.200 us, above 65 us even without the interference term (70.864 us).
- Impact: the requirement's verification-by-analysis claims a bound at the full shape that does not hold for valid
  configurations of that shape. The open questions do not list the case, so the owner is not asked about it, and the
  verification table tests only the uniform load.
- Required outcome: the derivation covers mixed formats at full stream count (or states the configurations it
  excludes), NFR-LAT-03's wording matches what is shown, and the open question and verification plan include it.
- Verification: rerun a shaper model over mixed {1, 2, 4, 6, 8}-channel assignments at 16 streams per port; the page's
  bound and its stated scope agree.

### R758-1-F3 MAJOR - Robustness, Conformance, Docs - docs/design/MARK_II_STREAM_ENGINES.md:638-648; docs/reference/FR_NFR.md:470 (NFR-REL-03) - compaction can lose saved changes without a power cut

- Authority/evidence: compaction "serializes from the live tables" into the standby slot while "Saves keep appending
  to the active slot meanwhile"; then "a header commits the new slot" and "the old slot is erased". A record changed
  after compaction copied it is appended only to the old slot. Committing the new slot and erasing the old one discards
  that change from flash, and the next boot restores the stale value. No rule re-copies, double-writes or replays those
  records. NFR-REL-03 requires the change to be durable within 0.5 s and compaction "without losing state".
- Impact: a saved-state change that met the 0.5 s bound is silently lost at the next compaction. That breaks the
  persistence clauses the traceability row cites (Milan v1.2 5.3.7.6, 5.3.8.2, 5.3.9.1, 5.3.13: "saved in a non-volatile
  memory and restored after a power cycle").
- Required outcome: the save path states how a change saved during compaction reaches the committed slot (for example,
  saves during compaction also append to the new slot after the copy, or the commit replays the old slot's tail), and
  the power-cut argument covers that window.
- Verification: a host flash-model test that changes a record after compaction copied it, commits, erases, reboots and
  reads the new value; plus power-cut points inside that window.

### R758-1-F4 MAJOR - Conformance, Docs - REQUIREMENTS.md:25-36; docs/reference/FR_NFR.md:75-80 and :469; docs/overview/ARCHITECTURE.md:3-10; docs/design/MARK_II_AREA_PLAN.md:157 and :273 - requirement text left contradicting the amended split

- Authority/evidence: the amended NFR-SCOUT-02 removes any retained-fabric option and moves gPTP to firmware at F6.
  Still at this head:
  (a) `REQUIREMENTS.md` section 1, the top of the authority order: control functions "MUST each have build-selectable
  placement", "The all-fabric build remains a supported option", "The fabric gPTP plane is the sole product PHC,
  protocol, servo, and public state owner", "The fabric MUST retain ... the gPTP plane", "Audio and gPTP deadlines MUST
  remain independent of firmware service";
  (b) `FR_NFR.md` section 1.2, in the same edited file: "Mark II selects ... per function", "The all-fabric option
  remains supported"; NFR-OBS-01 still requires "fabric-gPTP status/publication counters";
  (c) `docs/overview/ARCHITECTURE.md` (the docs index's current-boundaries authority): "build-selectable placement",
  "gPTP and media remain in fabric", "All-fabric remains supported";
  (d) the plan schedules lever 5 (lane 8, "MMCM servo in firmware", the media-clock actuator), while the amended
  NFR-SCOUT-02 keeps "media MUST remain fabric-owned" and NFR-SCOUT-03 keeps "Audio deadlines MUST depend only on bounded
  fabric handshakes". The conflict is not published.
- Impact: the normative set contradicts itself after this change, so an implementer cannot tell which text governs.
  AGENTS.md section 2 requires such a conflict to be published, not left.
- Required outcome: each listed text is amended to the 2026-10-31 decisions (or explicitly scoped to the current
  release), and the lever 5 versus media-ownership conflict is recorded as an open owner decision.
- Verification: a search of REQUIREMENTS.md, FR_NFR.md and the overview for build-selectable placement, a supported
  all-fabric option and fabric-only gPTP finds only release-scoped or transition text.

### R758-1-F5 MAJOR - Conformance, Docs - docs/reference/FR_NFR.md:465 (NFR-RES-01); docs/design/MARK_II_AREA_PLAN.md:64 and :67 - a "Mark I bound" of 60 % is presented as an owner decision

- Authority/evidence: the #640 body (2026-10-31) says the 20,000-LUT target "replaces the 60 % (38,040-LUT) target",
  and the 16:39 comment says it "replaces NFR-RES-01's 38,040 (60 %) as the Mark II goal". The cited
  [#234 ruling](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270) says the 60 % target stays,
  and "How it is met: a redesign ... tracked as #640", that is by Mark II, not by Mark I. The PR instead writes, in a
  MUST row, that the current all-fabric image "keeps the earlier target of at most 60 % LUT (38,040) as its bound", and
  the plan says "The owner retained the 60 percent target for Mark I". The current image is 52,008 LUTs (82.03 %,
  measured basis below).
- Impact: the normative register states a bound the shipping image fails and nobody decided, and attributes it to the
  owner.
- Required outcome: NFR-RES-01 records only what was decided (the 60 % target is replaced, and the resource gate holds
  the current image at its recorded figures), or the Mark I bound is raised as an open owner question.
- Verification: the row and the plan's Target table cite a decision that says what they say.

### R758-1-F6 MINOR - Conformance, Docs - docs/design/MARK_II_STREAM_ENGINES.md:49, :173-174 and :433 - two clause claims misstate their clause

- (a) "Milan v1.2 6.2 ... one to eight channels" and TCTX `NCH` "1 to 8 (Milan v1.2 6.2)": 6.2 fixes N in
  {1, 2, 4, 6, 8}.
- (b) "Milan v1.2 4.3.4 ... cites IEEE 802.1Q-2022 34.6.1 for both": Milan v1.2's normative reference is
  IEEE 802.1Q-2014, whose 34.6.1 is "Talker behavior" (2022's 34.6.1.1).
- Impact: a reader checking conformance against the cited clause finds different text, and (a) widens the format set.
- Required outcome: each sentence says what its clause says (base formats {1, 2, 4, 6, 8}; Milan cites 802.1Q-2014
  34.6.1, which is 802.1Q-2022 34.6.1.1).
- Verification: read Milan v1.2 6.2 and its reference list.

### R758-1-F7 MINOR - Conformance, Docs - docs/design/MARK_II_STREAM_ENGINES.md:235 and :160-161 - two latency-derivation statements do not follow from their basis

- (a) "Capture clock-domain crossing | 0.200 | Four 50 MHz cycles": four cycles at 50 MHz are 0.080 us.
- (b) "Stops and restarts can produce any order of those loads": under the page's own policy (fewest running streams,
  ties 0, 1, 3, 4, 2, 5, at most 16 per port), an exhaustive search reaches only `3, 3, 2, 3, 3, 2` at 16 streams
  (`receipts/cbs_mixed.out`, 2,304 reachable states).
- Both are conservative (the worst-order total becomes 64.130 us, and the worst order is unreachable), but the page is
  the requirement's analysis evidence.
- Required outcome: the CDC term's basis matches its value (or is stated as an allowance), and the order claim is either
  dropped or stated as a policy-independent bound.
- Verification: recompute the budget rows from their stated bases.

### R758-1-F8 MINOR - Conformance, RTL, Robustness - docs/design/MARK_II_STREAM_ENGINES.md:300-316, :434 and :465 - the shared render buffer is sized for 48 kHz only

- Authority/evidence: Milan v1.2 4.4.2.1: a Listener "shall support buffering of received audio samples for up to
  2,126 ms" (2.126 ms). The one-RAMB36 buffer is 8 slots x 128 samples: 2.667 ms at 48 kHz, but 1.333 ms at 96 kHz and
  0.667 ms at 192 kHz. The contexts advertise 96 and 192 kHz (`NSR`), and the ledger books 1.0 tile.
- Impact: at 96 or 192 kHz the design cannot hold the required presentation offset, or the ledger understates the RAM.
- Required outcome: the page states the buffer depth per rate (or limits the shape to 48 kHz), and the ledger matches.
- Verification: depth x sample period >= 2.25 ms at every advertised rate.

### R758-1-F9 MINOR - Conformance, RTL, Robustness - docs/design/MARK_II_STREAM_ENGINES.md:338-363 - redundancy time-domain handling is incomplete on the talker and over-strict on the listener

- (a) Milan v1.2 8.3.4 gives each interface its own gPTP end station, and IEEE 1722-2016 4.4.4.9 derives avtp_timestamp
  from gPTP time. The page converts secondary timestamps on the listener, but the talker "builds both frames from one
  capture read" with no statement of which time base the odd (secondary) contexts' timestamps use.
- (b) "A copy from an unsynchronized network is discarded. IEEE 1722-2016 4.4.4.7's tu bit marks it." With only one
  network up, a grandmaster change sets tu and every copy is discarded. 4.4.4.7 lets a listener stop correlating, and
  Milan v1.2 4.4.2.3 says it should free-wheel; neither tells it to drop samples.
- Impact: (a) secondary streams could carry primary-network time; (b) a grandmaster change on a single surviving
  network interrupts audio.
- Required outcome: the talker's per-port timestamp domain is stated, and the tu rule discards a copy only when the
  partner copy is valid (or states its behaviour when both carry tu).
- Verification: design text, plus the planned cable-pull simulation extended to a grandmaster change on the surviving
  network.

### R758-1-F10 MINOR - RTL, Docs - docs/design/MARK_II_STREAM_ENGINES.md:400-489 - register maps leave bits and offsets undefined

- A TI-style map lists every bit and offset. Missing: TCTX_CTRL bits 7:5, LCTX_CTRL bits 7:3, TCTX_PTO bit 31, and
  engine offsets 0x00C, 0x018-0x01C, 0x02C and 0x038-0x7FC. Also: the page's "resets are hexadecimal" rule against a
  reset of `n & 1`; the talker map has no unmapped-channel encoding, although Milan v1.2 5.3.9.1 allows unmapped
  channels; LCTX_DA_HI names a 16-bit field `VID` for a 12-bit VLAN ID.
- Impact: an implementer must invent read values and a map encoding, so two implementations could disagree.
- Required outcome: every bit range and offset in each block is defined (reserved where unused), and the talker map
  encodes "not mapped".
- Verification: the bit ranges of each register sum to 32, and offsets are contiguous or marked reserved.

### R758-1-F11 MINOR - Conformance, Docs - docs/ARCHITECTURE_HW_SW_SPLIT.md:42 and :79; docs/design/MARK_II_AREA_PLAN.md:249 - "a flexPTP-based daemon" is not the decided software

- Authority/evidence: owner 17:04: "The gPTP software is `flexptpd`, the daemon the test machine runs. Its source and
  licence get confirmed before adoption: it is not part of the public tsn-c-stack repository." The delta records
  "a flexPTP-based daemon", a provenance the owner did not state and marked as unconfirmed.
- Required outcome: name `flexptpd` as decided, with its source unconfirmed.
- Verification: the text matches the 17:04 comment.

### R758-1-F12 MINOR - Conformance, Docs - docs/design/MARK_II_AREA_PLAN.md:252 and :263-281 - the lane order departs from D16 without saying so

- Authority/evidence: D16 (owner 16:40) orders the levers least risky first, each measured before the next, and the
  decisions table gives "The lane order below" as its consequence. The lanes place lever 3 (lane 3) before lever 2
  (lane 5, folded into LiteX stage 3). Only the move of lever 4 is explained ("Dependencies put lanes 4 and 6 before
  lever 4").
- Required outcome: the departure for levers 2 and 3 is stated with its reason and marked as a proposal for owner
  approval, or the order follows D16.
- Verification: the lane table and D16 agree, or the difference is published.

### R758-1-R1 RESIDUE - Docs - the four touched prose pages - paragraph length against the 20-to-30-word rule

- Measured (`scripts/style_probe.py`, `receipts/style_probe.out`): of 180 added prose paragraphs, 155 are under 20
  words, 25 are 20 to 30 and none exceeds 30 (split page 16/3/0, area plan 37/4/0, stream-engine page 102/18/0). This
  matches the repository's own style gate (`check_doc_style.py`: at most 20 words and 2 sentences per paragraph) and
  the docs index rule ("Keep current sentences under eleven words"), which conflict with a 20-to-30-word floor.
- Exact fix if the 20-to-30 rule governs: join adjacent two-sentence paragraphs under the same heading until each is 20
  to 30 words. Otherwise no change; the manager records which rule applies.

### Suggestions (optional, do not affect coverage)

- S1: MARK_II_STREAM_ENGINES.md:173 says both shaping levels are required but derives only the class level. One
  sentence showing the per-stream shaper adds no wait would close the argument: with a 258-octet frame against a
  259-octet reservation the per-stream spacing is 124.5 us, below 125 us, so lateness only decays.
- S2: cite Milan v1.2 4.4.2.1 (2.126 ms) as the render buffer's sizing authority next to 802.1Q-2022 34.6.1.2.
- S3: the FR_NFR saved-state traceability row omits Milan v1.2 5.3.8.1 (Stream Input format), which is also saved.
- S4: the save sequence could state its read-back-failure path, and N25Q128 Table 17's "Erase to Suspend" 40 us typical
  spacing between a resume and the next suspend.
- S5: state the CRF frame's phase as part of the phase policy (the schedule puts it in phase 2).
- S6: NFR-SCOUT-02 and the split's gPTP bullet link the 17:04 comment; the move itself was decided at 16:51
  (6545655255), which D13 already cites.

## Independently verified (no finding)

- Wire load (Milan v1.2 4.3.3.2 Table 4.4 and its notes): 216-octet AVTPDU, 258-octet wire frame, 2.064 us,
  16,576 kb/s per stream, 265.216 / 270.848 Mb/s per port (26.52 / 27.08 %), CRF 88 octets (29 + 22 padded to 68,
  plus 20).
- Shaper (`scripts/cbs_model.py`, exact rationals, `receipts/cbs_model.out`): preferred-order per-phase waits 15.241,
  17.269, 14.276, 16.304, 18.333 and 12.740 us, shaper free at 124.527 us; worst of the 90 orders 23.925 us at
  `2, 2, 3, 3, 3, 3`; saturated best effort 28.635 us (preferred) and 33.004 us (worst order), within the additive
  bounds 30.669 / 36.261 us; fewer-reservation rows 62.259, 83.012, 41.425 and 0 us. The totals 58.658 and 64.250 us
  re-derive from the page's rows. Without a CRF reservation the worst order waits 23.106 us.
- Save path at N25Q128 maxima (Table 32: tPP 5 ms, tSE 3 s, tSSE 2 s; Table 17: erase suspend latency 15 us typical,
  no maximum; 9.1.20: program allowed during a suspended sector erase, not a suspended subsector erase; endurance over
  100,000 cycles per sector): t_page 5.343 ms, T_worst 353.4 ms, margin 146.6 ms; 187 pages/s; S2 4.8 KB/s; compaction
  1.28 s; erase 12 s; boot read 168 ms. Stated assumptions: T_svc 10 ms (NFR-SCOUT-03), 1 ms suspend allowance (to be
  measured), 12.5 MHz single lane (matches SAVED_STATE_FASTCONNECT.md 9.4), one save in flight, S1 and S2. Missing: F3.
- Measured basis: the four report SHA-256 digests match the build's reports (`receipts/report_digests.sha256`), and
  every quoted figure matches them: 52,008 LUTs (48,172 logic, 3,836 memory, 82.03 %), 54,104 registers, 15,800 slices,
  87.5 tiles (74 RAMB36, 27 RAMB18), 13 DSP, 103,262 of 103,262 nets routed with 0 errors, WNS +0.129 ns,
  WHS +0.036 ns, all constraints met, and every hierarchical row quoted (TCAM 494 is `mac_cam` inside the 506-LUT
  `rx_filter`). The sums 43,425, 3,289, 2,204 and 34,223 re-derive. Estimates are labelled as estimates, and the
  measured source commit is disclosed as not on dev.
- Block RAM ledger arithmetic: fabric 24.0, firmware 113 tiles from the SPLIT_CONTROL_MEMORY.md section 5 points
  (98,056 / 57,152 and 111,848 / 112,464 B), staging 11.5, total 141.5 against 121.5; mailbox 1 RAMB36 + 10 RAMB18 and
  CPU 2 + 5 match their measured sources; three RAMB36 in today's render master match the report.
- Area estimates: owner levers 19.1k to 22.4k from the stated ranges; 32x32 estimate 21.2k (17.6k to 25.2k).
- Clauses read and found to say what the text claims: IEEE 802.1Q-2022 8.6.8.2, 34.6, 34.6.1, 34.6.1.1, 34.6.1.2,
  L.3.1.1; IEEE 1722-2016 4.4.4.3, 4.4.4.6, 4.4.4.7, 4.4.4.8, 4.4.4.9, 7.5, 7.6; IEEE 1722.1-2021 7.2.6
  (avb_interface_index); IEEE 802.1AS-2020 8.4.3; IEEE 802.1BA-2011 6.3 (1522 octets); Milan v1.2 4.3.3.2, 4.3.4
  (except F6b), 5.3.5.1, 5.3.7.1, 5.3.7.3, 5.3.7.6 (2 ms default, 0 to 125 us, 31-bit range), 5.3.7.7, 5.3.8.2,
  5.3.8.7, 5.3.8.10, 5.3.9.1, 5.3.13, 6.2 (except F6a), 8.2.2, 8.2.4, 8.2.5, 8.3.1, 8.3.2.1.4, 8.3.4, 8.3.5.1.
  IEEE 802.1BA-2011 6.5 is not cited by the delta.
- Decisions stated faithfully elsewhere: processor removal and deletion at the switch-over; gPTP to software with fabric
  timestamps on both ports; `milan_csr` for information and diagnostics; milan_dp content; TCAM kept; the 32x32 shape;
  LiteX removed in three stages with a routed measurement each; ceiling, not goal; start after the release tasks; the
  0.5 s save reading confirmed on #823; the append-only direction. The five open questions (partial-load latency, save
  bursts beyond 32 pages, Block RAM over the ceiling, debounce windows, daemon licence) are stated at
  MARK_II_STREAM_ENGINES.md:686-704 and in the plan.
- Gates on the head (clean clone, pinned renderer): docs_check (0 findings, 211 pages), check_feature_status and
  self-test, check_em_dash --base e5b8405d (0 over 1,095 added lines) and self-test, check_doc_style and self-test,
  check_doc_paths, check_gptp_docs and self-test, check_solution_docs and self-test, check_submodule_docs and self-test,
  check_archive and self-test, gen_toc --selftest / --verify-anchors (563) / --check, DOC_MAP --check and --selftest,
  gen_module_matrix --check, check_diagram_pngs, ci_events --check, ci_gate_workflows --check: all rc 0. The 55 new
  fragment links all resolve (`receipts/new_anchor_check.out`). check_baremetal_only --check rc 1 (F1).
- Style: no non-ASCII dash and no hexadecimal literal in prose on any added line; the register maps use the TI layout
  (offset, name, bits, field, reset, access, description) apart from F10.
- Comment rule (owner 2026-10-15): the delta has no source file, so it adds no source-comment instance. The only
  lane-style token on an added line is the owner's own lever-table quote ("S2b round 11") in a docs table, which the
  rule does not cover.
- Privacy: the docs_check scrub is clean; no host, path, subnet, test-plan name or item numbering on added lines.

## Ledger (reviewer-owned)

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F4, F5, F6, F7, F8, F9, F11, F12) | FR_NFR.md NFR-RES-01, NFR-LAT-03, NFR-REL-03, NFR-SCOUT-02/03/05, sections 1.2, 4.2 and 6; ARCHITECTURE_HW_SW_SPLIT.md; MARK_II_STREAM_ENGINES.md, every section; MARK_II_AREA_PLAN.md new sections; every clause listed above; the #640, #665 and #823 bodies and 2026-10-31 comments; the #234 ruling 5967924270 | R758-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| RTL | UNCLEAN (F8, F9, F10) | MARK_II_STREAM_ENGINES.md shared engines, throughput, capture and render buffers, CDC terms, redundancy merge, per-port units, register maps, Block RAM ledger; the area plan's hierarchy against the hierarchical utilization report | R758-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Robustness | UNCLEAN (F2, F3, F8, F9) | latency at partial and mixed loads, the stop/restart phase policy, the save path, compaction and power-cut windows, flash suspend rules, tu and network-loss handling | R758-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Tests | UNCLEAN (F1, F2) | hosted check runs at the head (docs-check and docs-gates-0 failed, legs 1 and 2 cancelled, code and simulation contexts skipped for a docs-only change); local docs-workflow gates; author evidence `review-evidence/640-m9-r1` at 8d2ac568 (cbs_sim.py and gate logs); the verification tables of NFR-LAT-03, NFR-REL-03 and the stream-engine page | R758-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Docs | UNCLEAN (F1, F2, F3, F4, F5, F6, F7, F10, F11, F12; R1 residue) | all five touched pages; REQUIREMENTS.md sections 1 and 9; docs/overview/ARCHITECTURE.md; the docs index row; new fragment links; style probe | R758-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |

## Prior public review findings

Read after this round's verdict and ledger were written. At review time PR #828 carries two issue comments, both
round-start notices (6551117078 for R757-1 and 6551121963 for this round), no pull-request reviews and no line
comments (`receipts/pr828_comments.json`, `pr828_reviews.json`, `pr828_review_comments.json`). Issue #640 has no
comment after REVIEW READY 6551084628. No prior public finding exists to resolve or retain at this head. The author's
own five open risks in REVIEW READY are all present in the delta's open questions; F2, F3 and F5 are outside them.

## Real limits

- Seven code-quality gates (check_hygiene, check_todo_ownership, check_py_idiom, check_sh_idiom, check_sv_idiom,
  check_cpp_idiom, check_port_contracts) and five source gates (check_rtl_source_lists, check_soc_sources,
  check_nvm_record_space, check_nvm_capture, measure_test_evidence) refuse or fail locally because the clone's
  submodules are not initialised. None reads Markdown (check_hygiene's suffix list and check_todo_ownership's controls
  exclude `.md`), and the delta changes no code, so the delta cannot affect them. The hosted legs that run them were
  cancelled after F1 and are not evidence either way.
- The latency figures come from an independent class-level model of 802.1Q-2022 8.6.8.2, not from the implementation;
  the per-stream shaper level is argued (S1), not simulated. The mixed-load case in F2 is one configuration found by a
  search over 8-channel and 1-channel splits; other formats may be worse.
- The measured basis was checked read-only against the build's report files on the review host. Those reports are not
  in the repository or the public evidence tree, so a public reader can check only the digests, not the contents.
- No physical calibration or bench run took place; nothing here is hardware evidence. No manager source bank runs at
  this head, and none is claimed or inferred.
- No public source was found for the 20-to-30-word paragraph rule in the repository or the three issues' comments (R1).

## Pending manager duties

- Hosted and act acceptance of the exact head, including a rerun of the docs workflow after F1 is fixed (legs 1 and 2
  never ran).
- Builder and native banks on the current-dev merge candidate at the merge turn (source base and live dev both
  e5b8405db4c1f7cbdafb5df92b15b580142e0232 at review time).
- Owner approval of the requirement text (the author's own open item), including F4(d) and F5.
- Carry R1 to the residue checklist with the rule decision.

R758-1 FINISHED

# HANDOFF - [A720c] issue #640 Mark II charter, round 3 (docs only)

Status: REVIEW READY at head 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head; `git diff --check e5b8405d HEAD` rc 0. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-2 head f6b3e841646384177584ce75b657fb8dead7727c (PR #828). Round-3 head 69fd18f1d8f9d428687c07ede0f9c14597cf2d61, tree f7c3f02d8889081b89c7dcb46004d3ffb88623e2.
- Base: dev e5b8405db4c1f7cbdafb5df92b15b580142e0232, the live dev tip when round 3 started (05:0x CET). While the gates ran, dev moved to 1f29f189279f9fc0132f4918e47342b87d22f33a (PR #822, #787); the merge base is still e5b8405d. A trial merge of 69fd18f1 with 1f29f189 in the scratch clone is clean (`git merge-tree` rc 0, tree c3b75dc3ac0fe7aa7f8d8eebda146f787d84a859; dev touches one line each of REQUIREMENTS.md and docs/README.md), and on that merge result docs_check, gen_toc --verify-anchors and --check, check_doc_style, check_em_dash --base 1f29f189 and check_baremetal_only --check all exit 0 (the same held at 6f1e03ae, tree 83428b88). This is information only: candidate-merge validation stays with the manager; no rebase was done. The PR now adds 1,658 lines and removes 112 over 7 pages; round 3 adds 317 and removes 85 over 4 pages.
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6553091847 (text: evidence/taken_posted.md)
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6554386559 (text: evidence/review_ready_posted.md)
- Reviews answered: R757-2 (issuecomment-6553028166) and R758-2 (issuecomment-6553064958), both read in full, and their REPORT.md files (identical to the comments, checked by diff).
- Decisions re-read: #640 body and every 2026-10-31 comment, the 2026-11-01 survey comment 6551164172; #665 body and 2026-10-31 comments; #823 body and 2026-10-31 comments. No owner comment after 2026-10-31.
- Scratch: $VALIDATION_STORAGE/640-a720c (model, gate clone, gate venv and scratch HOME copied from round 2). Evidence (small files): ./evidence/.

## Commits (one per finding group, one-line subjects, no body, no trailers)

| # | SHA | Files | Finding group |
|---|---|---|---|
| 1 | f11e1eca496af71d861b13f2c578971c3e4e52f9 | SE | Residue: R757-2 RR2, R758-2-R1; suggestion R757-2 S5 / R758-2 S1 |
| 2 | 05f3e85ee305bff569525f797757ef125d7f0613 | SE, AP, FR | R757-2-N3; suggestion R757-2 S1 / R758-2 S3 |
| 3 | 45c2702000287dc763697ae6cdd5dc5ba1b248d5 | SE | R758-2-F1, F2; suggestions R757-2 S2, R758-2 S2 |
| 4 | 4b8a4d24b38adbc15dd83288cca609e063aa68b7 | SE | R758-2-F5 |
| 5 | 07f8eb91c9077b6b19d419983bc8b7c7a86938fb | SE | R757-2-N2, R758-2-F4 |
| 6 | 4e14b3313ae13836361b5f92e508c5846988ceca | SE, FR | R757-2-N1, R758-2-F3; suggestion R757-2 S3 |
| 7 | 6f1e03ae837c96911d206df37e973be673a47a92 | SP, SE, AP | R758-2-F6; suggestion R757-2 S4 |
| 8 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 | SE | Group 5 follow-up (R757-2-N2, R758-2-F4): each rule checks a reference time against the render point where it reads it; the sweep only guards the wrap (one context per 31.25 ms, 128 cycles per second), so the merge rests on no claim about which RAM port the engine or the firmware window uses |

`SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md, `FR` = docs/reference/FR_NFR.md, `SP` = docs/ARCHITECTURE_HW_SW_SPLIT.md. No rebase, no amend; nothing pushed.

R757-2 RR1 is in the PR body only: PR-BODY.md "Known limitations" now reads "(open questions 1 and 7)".

## Finding closure (file:line at 69fd18f1, then verification)

### Manager rulings

| Finding | Change, file:line | Verification |
|---|---|---|
| R757-2-N1, R758-2-F3, compaction window | SE:1003-1004 strict save priority at every page boundary, so each copy page holds durable values only; SE:1009-1014 the six steps (cursor at the log end, copy, replay from the cursor, header once the cursor meets the log end, saves to the new slot, erase later); SE:1016-1020 step 4's check and its header page are one step no save can split, and a save arriving during the header page waits for it, inside the existing 5.35 ms compaction-page term (T_worst unchanged, 359.75 ms); SE:1022-1028 boot order and why each key's newest durable value comes last; SE:1030-1039 table of every point a save can land (before step 1, between copy pages, between replay pages, at the boundary after the last replay page, between check and header: impossible, during the header page, after a failed header read-back, after the header); SE:1041-1046 power-cut table (a save append at any step, copy or replay, header page, after the header during the erase); SE:1114 verification row: a save at every page boundary including the one after the last replay page, one during the header page, a second save at every boundary, a power cut before, inside and after every page, and the test fails if a save may run between the check and the header or if step 3 is skipped; FR:476 NFR-REL-03 verification names the same | Host flash model `evidence/model/compaction_model.py` (lane evidence): 14,831 runs (one save at each of 12 boundaries or none, a second save at each or none, with and without a save during the header page, and a power cut before, inside and after every page operation, plus no cut): 0 lose a change or break a transaction. Mutation `split` (a save may run between the check and the header): 733 runs lose a change, the first with no power cut at all, which is the reviewers' sequence. Mutation `no_replay`: 2,704 lose a change |
| R757-2 S3, replay passes bounded | SE:996 table row (at most 311 pages, within 2.05 s, under S1 and S2); SE:1064-1080 S2 read exactly as a token bucket (32 pages, then 10 % of the flash), the derivation (code block), "step 3 replays at most 70 pages", "Compaction ends within 2.05 s of step 1", 70 appends cannot fill 392 free pages; SE:1082-1091 the standby is erased before the next compaction starts | Arithmetic under "Derived numbers" below |
| R757-2-N2, R758-2-F4, listener merge | SE:530-558 new "Conversion error bound": 1 µs per network (IEEE 802.1AS-2020 B.3, Milan v1.2 4.4.2.1), 100 ppm per grandmaster (B.1.1), 40 ns granule (B.1.2), E_x = 2.210 µs; assumption A3. SE:560-574 merge state (head time and position, 22-bit written map, render point). SE:576-587 clean copies: k = round((t - head) / 125 µs), a tolerance window of 62.5 µs either side; partners differ by at most 2.210 µs, neighbours by 125 µs less at most 0.6 µs of drift. SE:589-601 copies with tu set (IEEE 1722-2016 4.4.4.7): placed by their own sequence_num (4.4.4.6) from the context's last reference, a signed 8-bit count. SE:603-609 placement by count from the head, so conversion error never shifts a sample. SE:611-623 rules table: rule 2 discards a tu copy while the partner holds clean data (`CLEAN_VALID` set and `LCTX_CLEAN_PT` ahead of the render point); rule 3 anchors when there is no valid head (`HEAD_VALID` clear or `LCTX_LAST_PT` passed); rule 4 re-anchors on a clean copy when the head's anchor was tu; rule 7 duplicates. SE:625-638: a tu copy never writes while clean partner data remains; the window counts each duplicate once. SE:640-660 reference upkeep: a passed time counts as invalid where a rule reads it, a sweep of one context per 31.25 ms keeps every valid time within 1 s of the render point so wrapping compares stay exact (128 cycles per second), unpaired streams, and the double-fault limit (Milan v1.2 Annex D.3). Registers: SE:733-735 `SE_MERGE_DUP` (rule 7), `SE_MERGE_SEC` (rules 3 to 6), new `SE_MERGE_TU` at 0x038; SE:806-816 `LCTX_STATE` bits 9 `ANCHOR_TU`, 10 `SEQ_VALID`, 11 `CLEAN_VALID` (each valid while its time is ahead of the render point), `LCTX_LAST_PT`, new `LCTX_MERGE` at 0x1C (WMAP 21:0, HEAD_POS 30:22, HEAD_VALID 31); SE:826-828 new `LCTX_SEQ_PT` 0x48, `LCTX_CLEAN_PT` 0x4C, reserved 0x50-0x7C. Verification rows SE:1109-1110 | Merge model `evidence/model/merge_model.py` (lane evidence): 15 cases, all PASS (rendered samples equal the clean stream's, each sample once): both clean with a jittered ±2.210 µs conversion error and the secondary 1.1 to 1.5 ms slower (DUP = 4,000 of 4,000 packets, SEC = 0) or faster (SEC = 4,000); times 1 µs past a sample boundary; either network cut at packet 1,500; 1 % loss on the faster or on both networks, filled from the later copy; the secondary with tu set from packet 100, skewed +30, -30, +200, -200 µs and +1 ms, arriving first (`SE_MERGE_TU` = 3,900, no disturbed sample); tu from the first packet (startup: the clean copy re-anchors; 10 tu samples precede the clean span); a cut, then a grandmaster change on the surviving network (tu 0.25 s, 500 µs skew). Mutations: exact time compare fails 15 cases, placement by each copy's own time fails 3 (the boundary cases), no rule 2 fails 5 (the tu cases). The model checks every valid bit against the render point at each copy, which is the where-read rule of commit 8 |
| R757-2-N3, the 16-reservation condition | SE:19 Contents "One format meets it at 16 reservations."; SE:379-382 "At 16 reservations, one format per port meets 65 µs." and a link to the fewer-reservations results; AP:60 Target row "derived as met with one base format at 16 reservations per port; not met with mixed formats or with fewer reservations (open)"; AP:255 D14 likewise; FR:306 NFR-LAT-03 "16 reservations of one base format" and a link to the fewer-reservations results (123.337 µs with three co-phased streams) | `grep -n -E 'meets it|derived as met|meets 65|met with one base'` on SE, AP and FR: every hit carries "16 reservations" |
| R758-2-F1, largest legal 192 kHz load | SE:136 93.18 %, 14 eight-channel streams, no CRF, 748.160 Mb/s reserved; SE:138-142 every mix of 1 to 16 streams enumerated, 92.67 % at 16 reservations; SE:1150-1151 open question 7 | `evidence/model/load_any.py`: 48 kHz 33.47 %, 96 kHz 58.05 %, 192 kHz 93.18 % (any count) and 92.67 % (exactly 16); equals R758's `load_any_count.out` |
| R758-2-F2, every reachable 192 kHz placement | SE:353-354 results rows: one format 34.861 µs, exact over all 34 reachable placements; mixed 57.905 µs shaper wait (reached and the maximum), 84.319 µs reached, at most 100.825 µs; SE:362-376 why 34 placements exist (a start always takes the first empty phase in the tie order; 16 of the first 17 phases, the 17th the CRF or empty), the search, the 24.827 µs packetizer bound and the sum | `evidence/model/p192.py` (imports the unchanged round-2 model): a breadth-first search of every start and stop reaches 1,245,183 states, 34 with 16 AAF streams, exactly the set above; one format: 34.861 µs (N = 6), 4 and 8 simulated intervals agree; mixed: 57.905 µs superset maximum (equals R758's probe), 24.827 µs packetizer-delay superset maximum, bound 100.825 µs; reached 84.319 µs by an explicit start and stop sequence within the 75 % cap (peak 338.944 Mb/s), evaluated exactly with the packetizer queue. The full search was feasible, so nothing is left as an open question here |
| R758-2-F5, instrument time base | SE:415-430 capture stamps each TDM frame end on both PHCs on one edge; each port's launch observer stamps in its own PHC; a copy's interval uses its own port's PHC throughout, so no PHC offset enters it; SE:728-731 `SE_TLAT_MAX0/1`, `SE_TLAT_OVER` COUNT0/COUNT1 name the PHC; SE:778 `TCTX_TLAT_MAX` "both ends in the PHC time of the port `PORT` names"; SE:1106 verification row (an odd context with a non-zero, drifting PHC offset; bench capture on each port) | Design text and register rows read together |
| R758-2-F6, R757-2 S4, flexPTP | SP:79-80 only the owner's decision stays under "These decisions are final": `flexptpd`, "Its source and licence get confirmed before adoption" (the owner's 17:04 words); SP:93-101 the survey's proposal, stated as not an owner decision: public `kebag-logic/flexPTP`, MIT, a fork of `epagris/flexPTP`, surveyed revision branch `gptp` at `d116d3d`, the owner confirms source and licence, two-port use an open owner question; SP:51 plane row; SP:267; SE:1141-1144 open question 5; AP:254 D13 ("Not decided: the core survey proposes ..."); AP:279 lane 9; AP:308-314 new open owner decision 3 | 17:04 comment 6545820658 ("Its source and licence get confirmed before adoption") and survey comment 6551164172 ("adopt kebag-logic/flexPTP gptp d116d3d"). `grep -n -i -E 'adopted (fork|revision)'` on SP, SE, AP, FR: no hit |

### Residue and suggestions

| Item | Change, file:line | Verification |
|---|---|---|
| R757-2 RR1 | PR-BODY.md, Known limitations: "(open questions 1 and 7)" | Exact fix applied |
| R757-2 RR2 | SE:628 "No rule drops the only valid copy of a packet." (commit 1, kept verbatim through the merge rewrite) | Exact fix applied |
| R758-2-R1 | SE:704 "Every Milan counter is 32 bits and wraps to zero." | Exact fix applied |
| R757-2 S1 / R758-2 S3 | SE:395-402 fewer-reservations table gains "Total, with every fixed term" (102.584, 123.337, 81.750, 40.325 µs) and "Against 65 µs" | Arithmetic below |
| R757-2 S2 | SE:309-334 why the 8.560 and 9.840 µs packetizer terms bound mixed formats | Derivation below; it matches the round-2 model's `pkt_max` over the F3 superset |
| R757-2 S5 / R758-2 S1 | SE:957 t_page "5.344 ms, used as 5.35 ms" | 0.1664 + 0.011 + 5.000 + 0.1664 = 5.3438 ms |
| R758-2 S2 | SE:171 "about 114 µs" | 15 x 2,064 bits / 270.848 Mb/s = 114.31 µs (the CRF last in its phase) |
| R758-2 S4 | Not taken: it would add requirement text to REQUIREMENTS.md:58-59, which needs owner approval; NFR-SCOUT-03 already carries the obligation after the switch-over | - |

## Derived numbers and derivations

### Packetizer term for mixed formats (R757-2 S2)

- Let j join phase p last. When j joined, no phase was lighter than p (the phase rule). A port runs at most 17 entities (16 AAF and one CRF).
- 48 kHz: if p held over 4,128 bits (two eight-channel frames) before j, p held three or more entities and so did each of the five others: 3 + 15 + 1 = 19 > 17. So p never holds over 4,128 + 2,064 = 6,192 bits. Cycles per bit rise with N (16 + 6N over 8 x (66 + 24N)), so the AAF frames of a phase need at most 6,192 x 64 / 2,064 = 192 cycles; a CRF adds 22. Both ports: 2 x 214 x 20 ns = 8.560 µs.
- 96 kHz: if p held over 3,600 bits before j, each of the 12 phases held two or more: 24 + 1 = 25 > 17. So a phase holds at most 7,200 bits, 224 cycles; with a CRF, 2 x 246 x 20 ns = 9.840 µs.
- 8.560 < 20.833 µs and 9.840 < 10.417 µs, so no frame waits on an earlier phase's build.

### 192 kHz (evidence/model/p192.py, p192.out)

- Fixed terms other than the packetizer: pin 4.557 + CDC 0.200 + MAC 1.000 + interference 12.336 = 18.093 µs.
- One format, worst per N over the 34 placements: N = 1 29.918, N = 2 30.949, N = 4 32.921, N = 6 34.861 µs; N = 8 at 16 reservations exceeds the cap.
- Mixed: 57.905 + 24.827 + 18.093 = 100.825 µs at most; 84.319 µs reached (eight-channel streams at tie ranks 0, 4, 8 and 16, every other one-channel, no CRF; the hole at rank 15 left by a stopped CRF). Round-2 form "before packetizer time": 57.905 + 18.093 = 75.999 µs, equal to R758's probe.

### Engine load (evidence/model/load_any.py)

- 192 kHz: 14 x 53,440 kb/s = 748.160 Mb/s <= 750; 2 ports x 14 x 8,000 x 208 cycles = 46.592 M cycles/s over 50 MHz = 93.18 %. At 16 reservations: 13 x 8, 1 x 4, 2 x 1 channels, 92.67 %.

### Fewer reservations totals (48 kHz fixed terms 40.325 µs)

- 62.259 + 40.325 = 102.584; 83.012 + 40.325 = 123.337; 41.425 + 40.325 = 81.750; 0.000 + 40.325 = 40.325 µs.

### Conversion error and the merge window

- E_x = 2 x 1 µs (B.3, one per network: talker and listener PHCs agree within 1 µs on each network, so the two latched offsets differ by at most 2 µs) + 2 x 125 µs x 200 ppm (each offset up to 125 µs old; two grandmasters each within 100 ppm, B.1.1) + 4 x 40 ns (four PHC reads, B.1.2 granule) = 2.000 + 0.050 + 0.160 = 2.210 µs.
- Window: 62.5 µs either side of a packet (half the 125 µs interval). Neighbour separation: 125 µs less drift; drift across 22 packets at 200 ppm: 22 x 125 x 0.0002 = 0.55 µs. 2.210 + 0.55 << 62.5 << 125 - 2.210 - 0.55.
- Map: every renderable time lies in [render point, render point + 2.667 ms] (late and early checks), so |k| <= round(2.667 / 0.125) = 21: 22 bits (0 to 21). HEAD_POS: 9 bits address the 512-deep 192 kHz buffer.

### Compaction (S2 read exactly)

- p = 5.35 ms. In any interval t, saves program at most 32 + 0.1 t / p pages, using at most 32 p + 0.1 t of flash time. Compaction pages done by t >= (0.9 t - 32 p) / p - 1. Compaction needs 240 + A + 1 pages with A <= 32 + 0.1 t / p. Not done at t only if 0.9 t / p - 33 < 273 + 0.1 t / p, that is t < 382.5 p = 2.046 s. A <= 32 + 38.25 = 70.25, so 70 pages; work <= 311 pages.
- After compaction the new slot holds <= 311 pages, so >= 713 are free. The next trigger (392 free) needs >= 321 appended pages: 32 + 0.1 t / p >= 321 gives t >= 289 p / 0.1 = 15.46 s. The old slot's erase needs 12 s of flash: 0.9 x 15.46 - 0.17 - 0.32 = 13.42 s free by then (0.32 s: at most 321 saves, each suspending the erase for its 1 ms allowance).
- T_worst unchanged: 10 + 5.35 + 2 x 1 + 32 x 5.35 + 32 x 5.35 = 359.75 ms (the header page is the compaction page in flight).

## Gate table

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720c/gates/wt at 69fd18f1d8f9d428687c07ede0f9c14597cf2d61, a fresh clean clone of the lane with the four submodules the jobs fetch (gitlinks unchanged; each submodule's origin set to its .gitmodules URL, as the builder legs require). Gate venv: round 2's (pyyaml, the pinned Markdown renderer, the pinned HDL-reference requirements, wavedrom 2.0.3.post3), copied. Logs and rc files: ./evidence/gates/ (one log over 200 KB is listed with its digest in evidence/gates/LARGE_LOGS.txt).

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 211 md + 1427 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base e5b8405d` (merge base with live dev) | 0 | 0 findings over 1658 added lines in 7 pages |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | OK; 30 controls |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py --check/--selftest`, `timesync_chain.gen.py --check/--selftest` | 0 | OK |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | 43 controls |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and the three `--check` runs | 0 | current |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | 6 rasters, 28 controls |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | 0 findings |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | up to date, 79 modules |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | PASS |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 | 18 PASS |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check` and `--selftest` | 0 | 0 findings over 1425 files; 867 arms |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | SDK cache hit: verified (the pinned archive this lane installed fresh in its scratch HOME; see notes) |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations (666 s) |
| docs-gates-0 | gate_26 NVM record space | `check_nvm_record_space.py` (+ `--self-test`) | 0 | 0 findings, 5 configs |
| docs-gates-0 | gate_27 capture census | `check_nvm_capture.py` | 0 | PASS |
| docs-gates-0 | gate_28 saved-state writer | `test_nvm_firmware.py --self-test` | 0 | OK, 5 shapes |
| docs-gates-0 | gate_29 SoC sources | `check_soc_sources.py` (+ `--selftest`), `iob_pack_selftest.py` | 0 | 22 arms |
| docs-gates-0 | gate_30 RTL source lists | `check_rtl_source_lists.py` (+ `--selftest`) | 0 | 50 PASS |
| docs-gates-0 | gate_31 naming | `measure_naming.py --check/--selftest` | 0 | 66 PASS |
| docs-gates-0 | gate_32 port contracts | `check_port_contracts.py` (+ `--selftest`) | 0 | 82 PASS |
| docs-gates-0 | gate_33 fail-fast | `measure_fail_fast.py --check/--selftest` | 0 | 106 PASS |
| docs-gates-0 | gate_34 TODO ownership | `check_todo_ownership.py` (+ `--selftest`) | 0 | 45 PASS |
| docs-gates-0 | gate_35 test evidence | `measure_test_evidence.py --check/--selftest` | 0 | 105 PASS |
| docs-gates-0 | gate_36 hygiene | `check_hygiene.py --check/--selftest` | 0 | 35 PASS |
| docs-gates-0 | gate_37 to 40 idioms | `check_sv_idiom.py`, `check_cpp_idiom.py`, `check_py_idiom.py`, `check_sh_idiom.py` (+ `--selftest` each) | 0 | 55, 75, 54, 48 PASS |
| docs-gates-0 | gate_43 cited paths | `check_doc_paths.py` | 0 | 1075 paths resolve |
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | OK, 24 controls |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 150 pages; anchors reproduced |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1124 s) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN (102 of 103) |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | Markdown gates, pinned venv $VALIDATION_STORAGE/818-mdvenv | `docs_check.py`; `check_em_dash.py --base e5b8405d`; `check_doc_style.py`; `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | same results as above |
| (lane) | whitespace | `git diff --check e5b8405d HEAD` | 0 | no output |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over the 7 pages | 0 | 0 findings in changed blocks |

Notes:
- The 16 NOT RUN arms of leg 1 skip by their own rules, as in round 2: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. The leg's rc is 0 and its verdict is judged on the union of the legs.
- Runs. The table is the run at 69fd18f1 on a fresh clone (evidence/gates/, run_all.out). Before commit 8, the same full set ran at 6f1e03ae, every step rc 0 (evidence/gates/run_6f1e03ae_summary.txt); commit 8 changed one page's merge text, so everything was run again at the new head.
- First attempt at 6f1e03ae of the SDK, gate_24 and builder steps (evidence/gates/attempt1_6f1e03ae/): the copied round-2 SDK failed verification ("SDK provenance mismatch": the SDK records its install path, and the copy moved it); gate_24 hit this runner's 560 s step limit (it needs about 670 s); both legs refused because the scratch submodules' origins were local paths ("source dependency origin differs"). None of these reads a page. Fixes: the copied SDK in this lane's scratch HOME was deleted and the pinned archive installed fresh (digest-checked by the installer), the step limits raised, and each submodule origin set to its .gitmodules URL. All four steps then ran and exited 0. The shared SDK in the home directory was not touched.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.
- One slip: the information-only merge-result check wrote a single small temporary file to /tmp, deleted at once. Everything else ran under $VALIDATION_STORAGE/640-a720c.

## Evidence (./evidence)

| File | sha256 | What |
|---|---|---|
| model/mixed_stagger.py | bfebe546c8d3df2544660b274aa5c5d857a979932c31b3bf56a4785a09bae5b1 | The round-2 model, unchanged; p192.py and load_any.py import it |
| model/p192.py, p192.out | 36457f06..., 15f7b5df... | 192 kHz: every reachable placement, one format exact, mixed bound and reached witness (2 min 29 s) |
| model/load_any.py, load_any.out | 31e1b3be..., a3e68eaf... | Worst engine load over every mix of 1 to 16 streams |
| model/merge_model.py, merge_model.out | b97499eb..., 98d2695a... | Listener merge rules, 15 cases and 3 mutations |
| model/compaction_model.py, compaction_model.out | 6e64e6fd..., e68a58ca... | Host flash model of saves and compaction, 14,831 runs and 2 mutations |
| style_touched.py, style_touched.log | - | check_doc_style's analyze() over every changed block of the 7 touched pages: 0 findings |
| taken_posted.md, review_ready_posted.md | - | The TAKEN and REVIEW READY texts as posted |
| gates/ | - | Every gate step's log and rc at 69fd18f1 (LARGE_LOGS.txt: the one log over 200 KB, gate_41_ci_events.log, 337,511 bytes, sha256 be0a6c1d2b39b849139381d0110abea6930832c139ed7334212c3580852c68d9); run_6f1e03ae_summary.txt; attempt1_6f1e03ae/ |
| SHA256SUMS | - | Digests of every file above |

Reproduce: `python3 -I p192.py .`, `python3 -I load_any.py .`, `python3 -I merge_model.py`, `python3 -I compaction_model.py` in evidence/model.

## Not done / not allowed

No push, PR edit, merge, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. The shared RV32 SDK in the home directory was not touched (the CI step, gate_24 and both builder legs ran with the round-2 scratch HOME, copied into this lane's scratch).

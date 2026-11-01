# HANDOFF - [A720b] issue #640 Mark II charter, round 2 (docs only)

Status: REVIEW READY at head f6b3e841646384177584ce75b657fb8dead7727c (2026-11-01). Every docs-workflow gate step rc 0 on a clean clone of that head. Local only, nothing pushed.

- Lane: $LANES/640-mark2-charter, branch 640-mark2-charter. Round-1 head dfc310fb3dec28f3d06333973e61cde44a4e786d (PR #828). Round-2 head f6b3e841646384177584ce75b657fb8dead7727c, tree 4bb54f5edd8e777b1b7c13c045a318474e7e0d80.
- Base: dev e5b8405db4c1f7cbdafb5df92b15b580142e0232, also the live dev tip when the gates ran (fetched 2026-11-01 03:3x CET).
- Remote checked: https://github.com/kebag-logic/milan-fpga.git
- TAKEN: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6551372627
- REVIEW READY: https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6552845800 (text: evidence/review_ready_posted.md)
- Reviews answered: R757-1 (issuecomment-6551340614), R758-1 (issuecomment-6551352951). Both read in full.
- Scratch: $VALIDATION_STORAGE/640-a720b (model, gate clone, venv, scratch HOME with the pinned RV32 SDK). Evidence (small files): ./evidence/.

## Commits (one per finding group, one-line subjects, no body, no trailers)

| # | SHA | Files | Finding group |
|---|---|---|---|
| 1 | 7bcf9a9c93c1ec477522d7b179167b619cc15c3c | MARK_II_AREA_PLAN.md | R757-1-F1, R758-1-F1 (bare-metal gate) |
| 2 | 9aff05dcf3b474dc1c025a1cbaddedd5efa4b103 | FR_NFR.md, MARK_II_AREA_PLAN.md | R757-1-F2, R758-1-F5 (60 %) |
| 3 | f38baddad5934edd8aa42b541fa8b5c53cef415e | REQUIREMENTS.md, FR_NFR.md, overview/ARCHITECTURE.md, MARK_II_AREA_PLAN.md | R757-1-F3, R758-1-F4 a-d (requirement scoping, lever 5 conflict) |
| 4 | 9140079a538f9f871658ca0de90aeecdd3c615bb | ARCHITECTURE_HW_SW_SPLIT.md, MARK_II_AREA_PLAN.md, MARK_II_STREAM_ENGINES.md, FR_NFR.md | R757-1-F5, R758-1-F11, R758 S6 (flexptpd) |
| 5 | f0cfa69cbdc0dc9ccfbbb68a7d9d3df8ca0493ff | MARK_II_STREAM_ENGINES.md, FR_NFR.md, MARK_II_AREA_PLAN.md | R757-1-F4, R758-1-F2, R757-1-F6, F7a, F7c, F8, R1; R758-1-F6, F7a, F7b; R757 S1, S4; R758 S1, S5 (latency) |
| 6 | 3eb2f95061a3fdf12d9eb0fff6cc0a8907c15717 | MARK_II_STREAM_ENGINES.md, MARK_II_AREA_PLAN.md | R757-1-F9, R758-1-F8, R758 S2 (rates) |
| 7 | ec8ffd98e4089ce8264e7447ed7817fb4ca45c66 | MARK_II_STREAM_ENGINES.md | R758-1-F9, R757 S2 (redundancy) |
| 8 | 790f71796e1d128af7903e3df5d2ebe4ea310186 | MARK_II_STREAM_ENGINES.md | R757-1-F11, F7b; R758-1-F10 (register maps) |
| 9 | 119281c92a7bca5068b9bdc4d8dc83081296c6a7 | MARK_II_STREAM_ENGINES.md, FR_NFR.md | R758-1-F3, R757-1-F10, F7d, R2; R758 S3, S4 (save path) |
| 10 | f9786179f1d0de7b3905f62520122b5fb49a3153 | MARK_II_AREA_PLAN.md | R757-1-F12, F13, R3; R758-1-F12 (area plan) |
| 11 | 3baf35c1cbd10667d5bf586893bf17b3e54bc345 | REQUIREMENTS.md, split, overview, area plan | Style limits on lines of groups 2 to 4; R758-1-R1 |
| 12 | f6b3e841646384177584ce75b657fb8dead7727c | MARK_II_STREAM_ENGINES.md | Group 5 follow-up: the 95.867 us bound is for 16-stream mixes |

Commit 9 was amended once before anything else was built on it (a literal `{D823}` link placeholder replaced by its URL, caught by docs_check). No rebase was used; nothing was pushed.

## Finding closure (file:line at f6b3e841, then verification)

Lines are in the round-2 head. `SE` = docs/design/MARK_II_STREAM_ENGINES.md, `AP` = docs/design/MARK_II_AREA_PLAN.md, `FR` = docs/reference/FR_NFR.md, `RQ` = REQUIREMENTS.md, `OV` = docs/overview/ARCHITECTURE.md, `SP` = docs/ARCHITECTURE_HW_SW_SPLIT.md.

### Shared findings (manager rulings)

| Finding | Change, file:line | Verification |
|---|---|---|
| R757-1-F1 / R758-1-F1, bare-metal gate | AP:159 "the host tools" (owner's lever-3 "Why" cell paraphrased; the retired term removed); AP:273 "CSR, host-tool and firmware suites" | `check_baremetal_only.py --check` rc 0, 0 findings over 1425 files, and `--selftest` 867 arms, on the clean clone at the head (gate 21). Every docs-workflow step was run and recorded (gate table) |
| R757-1-F2 / R758-1-F5, 60 % | FR:473 NFR-RES-01: the 20,000 ceiling "replaces the earlier target of at most 60 % LUT (38,040), which the owner kept on 2026-10-03 for this redesign to meet ([#234 ruling](.../234#issuecomment-5967924270))"; shipping image "MUST fit xc7a100t; as that ruling says, the resource gate (#638) holds it at its recorded figures ... carries no other LUT bound". No "Mark I bound" remains. AP:65 Target row "Shipping image until Mark II"; AP:67-71 the 2026-10-03 record and the 2026-10-31 replacement | Public record: #234 comment 5967924270 (2026-10-03: "The target stays at 60 %... How it is met: a redesign in ... Mark II ... Until then: the #638 resource gate holds every resource at its recorded value") and #640's original body (2026-10-03). `git log -S '38,040' -- docs/reference/FR_NFR.md`: the 60 % text predates the 2026-07-11 reorganisation (32c0b98c9a); the base row read "Baseline (1 core, stereo 48 k) MUST fit xc7a100t with headroom (target <= 60 % LUT)". `grep -n 'Mark I bound'` on FR and AP: no hit |
| R757-1-F3 / R758-1-F4 a-c, requirement contradictions | RQ:25-37 (control functions, "Until the switch-over, each MUST have build-selectable placement", all-fabric default "until then", "After the switch-over, no all-fabric build remains", "Until F6, the fabric gPTP plane is the sole owner", "After F6, firmware owns the gPTP protocol and servo"); RQ:41-47 (fabric retains gPTP plane "Until F6"; "Until F6, gPTP deadlines MUST also remain independent"; after F6 each gPTP path states its firmware bound); RQ:58-59 (both placements, until the switch-over); RQ:110 (split architecture defines both placements until the switch-over); RQ:156-159 (section 4 preamble: until F6 the fabric plane owns that section's gPTP duties; after F6 firmware; PHC and timestamps stay in fabric on both ports); RQ:332-334 (REQ-VER-05 gPTP fabric-owned until F6). FR:75-85 (section 1.2 rewritten, scoped); FR:108; FR:305 NFR-LAT-02; FR:320 NFR-SCUP-02; FR:327 NFR-SCOUT-01; FR:456-457 (placement combinations until the switch-over); FR:477 NFR-OBS-01 (gPTP counters from the fabric plane until F6, then the firmware daemon); FR:500 Time row; FR:517 diagram. OV:3-19 and OV:81-87 | `evidence/requirement_scope_grep.txt`: R757's exact grep and R758's search at the head. Every hit is scoped inline ("until the switch-over", "until F6", "after the switch-over") or is transition text (NFR-SCOUT-02/03, NFR-RES-01), "current"/"today's" shipping text (FR:75, OV:19), or a test-oracle name (FR:33, FR:567 "fabric-gPTP capture/CSR oracles"). OV:66 "fabric-gPTP sources merge" sits in the implementation sections that OV:19 scopes to "today's all-fabric shipping build". REQUIREMENTS.md was edited for scoping only; restructured lines keep the existing meaning |
| R758-1-F4 d, lever 5 vs media ownership | FR:328 NFR-SCOUT-02 records the conflict and links it; AP:291-300 new "Open owner decisions" item 1 | The conflict is published as an owner decision; no lane may assume an answer (AP:293-294) |
| R757-1-F4 / R758-1-F2, mixed formats | SE:179-214 stagger: the phase rule (least wire time at start, CRF counts, spread ties, never moved, smallest frames first, CRF last), and what the rule cannot prevent with a reached example; SE:216-377 latency budget re-derived: shaper as a FIFO recursion (SE:252-258), interference, fixed terms, results table at 16 reservations per port for 48, 96 and 192 kHz (SE:312-336, table SE:317-324); fewer reservations (SE:338-357); open question 1 (SE:904-914). FR:306 NFR-LAT-03 states met with one base format per port (63.431 us), not met with mixed counts (up to 95.867 us at 48 kHz) or fewer reservations, open for the owner. AP:59 and AP:255 | Executable model `evidence/mixed_stagger.py` (sha256 below), output `evidence/mixed_stagger_results.txt`. Results: see "Derived numbers". The model reproduces both reviewers' cases exactly (R758-1-F2 42.875 us with the CRF in phase 1; R757-1-F4 42.765 us with the CRF in phase 0). Not presented as met for mixed formats anywhere |
| R758-1-F3, compaction loses changes | SE:830-860: seven-step ordering (note S0, copy, replay every active record above S0, repeat until nothing dirty or unreplayed, header with higher generation, saves move, erase old later); boot applies records in sequence order; the copied-newer-than-replayed case; power-cut table (SE:853-858). FR:476 NFR-REL-03 "loses no saved change, with or without a power cut"; verification adds the host-model test the reviewer named. SE:897 verification row | Design text; the verification row requires the host flash-model test (change after copy, commit, erase, reboot, read the new value) and a power cut at every step |
| R757-1-F5 / R758-1-F11, gPTP software | SP:51, SP:79-84, SP:261; AP:254 D13, AP:279 lane 9; FR:328 NFR-SCOUT-02 (16:51 decision link, `flexptpd` at 17:04); SE:924-926 open question 5 | `flexptpd` named as decided. Source: public `kebag-logic/flexPTP`, MIT, fork of `epagris/flexPTP` (checked with the GitHub API: fork=true, parent epagris/flexPTP, licence MIT; branch `gptp` head d116d3dfe8e6), cited to the #640 survey comment 6551164172. One global core state = one port per image, listed as the open redundancy item |
| R758-1-F12 / R757-1-F13, lane order | AP:257 D16 row ("except lever 2 after lever 3: a reading for the owner to confirm"); AP:288-289; AP:301-307 open decision 2 with the reason (stage 3 replaces the bus and CSR banks lever 2 would slim) | Departure stated with its reason and marked as a proposal pending owner approval |

### Other R757-1 findings and residue

| Finding | Change, file:line | Verification |
|---|---|---|
| F6, interference assumptions | SE:263-290: L.3.1.1 a) (larger of one maximum frame and mediumAccessDelay); A1 no frame above 1522 octets on an AVB port, A2 LPI never asserted; 802.1BA 6.3 caps frames at 2000 octets, 1522 is only its basic-header example; A2 is 802.1BA 6.1 option a), b) allows a 30 us wake; implementation enforces and tests both; 2000-octet figure 16.160 us shown | Clauses read: 802.1BA-2011 6.1 and 6.3, 802.1Q-2022 L.3.1.1 (text extracts in scratch/std) |
| F7 a | SE:227-233: Milan 4.3.4 cites 34.6.1 of [802.1Q]; Milan's reference list makes that 802.1Q-2014; 802.1Q-2022 numbers it 34.6.1.1 | Milan v1.2 reference list (IEEE Std 802.1Q-2014); 802.1Q-2022 34.6.1 / 34.6.1.1 headings |
| F7 b | SE:571-574 SE_RMAP (per render slot, Milan v1.2 5.3.10.1); SE:594 TCTX_MAP cites 5.3.9.1 (talker) | 5.3.10.1 maps each cluster channel to at most one stream input channel; the listener map is now per slot, which is that rule |
| F7 c | SE:48-52 "N is one of 1, 2, 4, 6 and 8"; SE:590, SE:630 NCH "1, 2, 4, 6 or 8 (Milan v1.2 6.2); any other value sets ERR" | Milan v1.2 6.2 and Table 6.1 |
| F7 d | FR:613 saved-state row: 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13 and 5.5.2.4 | `grep -n -i 'non-volatile' milan12.txt`: those are every "saved in a non-volatile memory" clause, plus 5.5.2.4 (binding parameters stored at bind) |
| F8, instrument interval | SE:359-377 "The latency instrument": start = PHC stamp of the TDM frame end less the synchronizer delay and less the slots after the stream's last slot (the pin instant of the packet's last sample); end = launch observer first bit plus the PHY egress constant; bench calibrates once against an external capture of pin and wire. Registers SE_TLAT_MAX0/1, SE_TLAT_OVER, TCTX_TLAT_MAX now "pin-to-first-bit" (SE:563-566, SE:612). FR:306 NFR-LAT-03 verification names "the Mark II latency taps, which measure this pin-to-wire interval itself" | Register descriptions and NFR-LAT-03 verification clause read together |
| F9, rates | SE:80-88 per-rate table and 75 % limit (192 kHz: at most 13 eight-channel streams with a CRF; 860.672 Mb/s, 86.07 % for 16); SE:118-142 engine load per rate (33.47, 58.05, 92.67 %); SE:393-417 render buffer per rate (1, 2, 4 RAMB36); ledger SE:677 4.0 tiles, subtotal 27.0, total 144.5 (SE:690); AP:238, AP:242, AP:46; talker budget at 48 and 96 kHz with 192 kHz in the results table | `evidence/load_by_rate.txt` (every legal 16-stream mix); depth x period = 2.667 ms >= 2.25 ms at every rate |
| F10, save terms and timeout | SE:760-764 read-back retry, per-save suspend and Table 17's 40 us resume-to-suspend; SE:789-801 T_worst = 10 + 5.35 + 2 x 1 + 2 x 32 x 5.35 = 359.75 ms (margin 140.25 ms, 28 %); SE:804-805 `T-NVM-COMMIT-TIMEOUT` restated by #823 and #665 F1 per the owner's 17:11 direction; SE:927-930 open question 6; FR:476 | Arithmetic below; matches R757's 359.75 ms |
| F11, register bits and counter resets | SE:522-663: every bit assigned or RESERVED (TCTX_CTRL 7 and 31:15; LCTX_CTRL 7:4 and 31:15; TCTX_PTO 31; and others); every offset defined (engine 0x00C, 0x018-0x01C, 0x02C, 0x038-0x03C, 0x060-0x7FC reserved); counter reset events: talker MEDIA_RESET, TIMESTAMP_UNCERTAIN, FRAMES_TX cleared when RUN rises (5.3.7.7), STREAM_START/STOP never cleared by a start; listener counters cleared by CNT_CLR written on not-bound to bound (5.3.8.10), unbinding keeps them | Per register the field widths sum to 32; offsets contiguous or reserved (checked by hand for each row) |
| F12, lever 6 credit | AP:175 new row "+0.25k" (u_txret 218 and u_txticket 32 stay; lever 6 nets 4,944 of 5,194); AP:180 32x32 estimate ~21.45k (17.8k to 25.45k); AP:45, AP:17, AP:182 ("about 1.45k") | Arithmetic below |
| F13 | See R758-1-F12 above | - |
| R1 | SE:297 "Four 50 MHz cycles (0.080 us), rounded up to 0.200 us (estimate)" | Exact fix applied |
| R2 | SE:920-923 open question 4: "Today's 500 ms window uses the whole bound." / "The 1,000 ms window exceeds it." | Exact fix applied (split into two items for the 10-word limit) |
| R3 | AP:226 heading "Mark II Block RAM ledger"; contents label regenerated by gen_toc.py --write | Anchor unchanged (`#mark-ii-block-ram-ledger`); gen_toc --check rc 0 |
| S1 | SE:239-245: the per-stream level never holds a frame (releases 125 us apart; frame bits over stream idleSlope under 125 us; CRF equals 125 us) | Model check `per_stream_spacing_ok`: largest ratio 125.000 us (the CRF) at every rate |
| S2 | SE:471-492 merge rules: a clean copy replaces the last packet's tu copy; both tu: first copy rendered; unpaired stream uses rules 1 and 2 only | Design text; verification row SE (listener merge) adds both-tu and grandmaster change |
| S3 | FR:500 Time row "one PHC and one timestamp unit per port" | Consistent with SE per-port table (PHC per port) |
| S4 | SE:185 "A CRF stream counts like any other" (phase by the same rule) and SE:196 "A CRF frame goes last in its phase" | Model places the CRF by the rule (uniform and 192 kHz searches) or relaxes it (superset) |

### Other R758-1 findings and residue

| Finding | Change, file:line | Verification |
|---|---|---|
| F6 a, b | As R757-1-F7 c and a | - |
| F7 a | As R757 R1 | - |
| F7 b, "any order" claim | Removed; the phase rule now names what starts and stops can reach (SE:199-214) and the results come from searches of the reachable set or a sound superset | Model sections `uniform` (exact reachable set) and `s48`/`s96` (superset with witnesses) |
| F8, render buffer at every rate | As R757-1-F9; Milan v1.2 4.4.2.1 (2.126 ms) cited as the sizing authority (SE:393-397, R758 S2) | depth x period >= 2.25 ms >= 2.126 ms at 48, 96, 192 kHz |
| F9 a, talker time base | SE:448-469: each copy carries its own port's time (802.1AS per interface, 1722 4.4.4.9); even copy port 0, odd copy port 1 via the PHC offset latched on one edge every 125 us; `PORT` bit names the base | Verification row "Port time bases" (SE) |
| F9 b, tu rule | SE:471-492: tu marks uncertain time; Milan 4.4.2.3 asks to free-wheel; neither clause drops samples; no rule drops the only copy | Verification row adds a grandmaster change on the surviving network |
| F10, register bits/offsets, n & 1, not-mapped, VID | As R757-1-F11; PORT reset "0x0 for even n, 0x1 for odd n" with the rule stated (SE:527); TCTX_MAP value 15 = not mapped (SE:594); VID 12 bits at 27:16 in TCTX_DA_HI and LCTX_DA_HI (SE:599, SE:638) | Field widths sum to 32 |
| R1, paragraph length | No change needed: the owner rule reads "short paragraphs, 20 to 30 words at most", an upper bound; the repository's check_doc_style.py limits (10 words per sentence, 20 words and 2 sentences per paragraph) are stricter and were applied to every changed block of every touched page: 0 findings | `style_touched.py` (the checker's own analyze()) over the 7 touched pages, rc 0 (gate table) |
| S1 to S6 | S1: SE:239-245; S2: SE:393; S3: FR:613; S4: SE:760-764; S5: SE:185, SE:196; S6: FR:328 and SP:79 link the 16:51 decision | - |

## Derived numbers and derivations

### Wire load (Milan v1.2 6.2, Table 4.4 and notes; 802.1Q-2022 34.3.1)

- Frame on the wire, N channels at 48 kHz: 24 + 24N + 22 (at least 68) + 20 = 24N + 66 octets. N = 1, 2, 4, 6, 8: 90, 114, 162, 210, 258 octets.
- Reservation: MaxFrameSize 24N + 25, + 22 (at least 68), + 20, x 8 x 8,000 = 1536N + 4288 kb/s: 5,824; 7,360; 10,432; 13,504; 16,576 kb/s. CRF: MFS 29 -> 68 -> 88 octets, 5,632 kb/s.
- 16 eight-channel streams and a CRF per port: 48 kHz 270.848 Mb/s (27.08 %); 96 kHz 16 x 28,864 + 5,632 = 467.456 Mb/s (46.75 %); 192 kHz 16 x 53,440 + 5,632 = 860.672 Mb/s (86.07 %) > 75 %. At 192 kHz with a CRF: 13 x 53,440 + 5,632 = 700.352 <= 750 Mb/s; 14 x 53,440 + 5,632 = 753.792 > 750.

### Shaper model (evidence/mixed_stagger.py)

- F1: without interference credit is never positive at a start, so s(k) = max(a(k), s(k-1) + L(k-1)/idleSlope). Checked equal to an event-exact 8.6.8.2 simulation on 300 random mixes at each rate: True.
- F2: one lower-priority frame delays any start by at most its duration (credit gained while blocked is spent later). Checked with a saturated best-effort queue of 1542-octet frames at several offsets: largest excess 12.335 us (48 kHz), 12.328 (96), 12.335 (192), against 12.336 us. A simulator bug (credit clipped for the whole best-effort frame when an arrival fell inside it) was found and fixed before this check.
- F3 (superset): when a stream joins phase p, every other phase holds at least load(p) - L(joining stream); with at most 16 streams at any time this bounds each phase, jointly over some order of last additions (subset DP). The CRF may stand in for scaffold in one phase per condition. The superset search is exact over that set (multisets of the phases ahead, all window lengths), so it is an upper bound on the rule.
- Witnesses are constructed and checked with the exact rule (greedy add with the stated tie order), so they are reachable.
- Fixed terms, 48 kHz: pin 18.229 (7 x 1/(48 kHz x 8)), CDC 0.200, packetizer largest phase both ports 8.560 (2 x (192 + 22) cycles x 20 ns), interference 12.336, MAC 1.000; sum 40.325. 96 kHz: 9.115, 0.200, 9.840 (2 x (224 + 22) x 20 ns), 12.336, 1.000; sum 32.491.
- Results at 16 reservations per port:

| Rate | Formats | Shaper wait, us | Derived bound, us | Basis |
|---|---|---:|---:|---|
| 48 kHz | one format | 23.106 (8 ch, counts 2,3,3,3,3,2, no CRF) | 63.431 = 23.106 + 40.325 | exact, 17,658 reachable states with the CRF |
| 48 kHz | mixed | reached 53.085; at most 55.542 | reached 92.530 = 53.085 + 18.229 + 0.2 + 7.680 + 12.336 + 1.0; at most 95.867 = 55.542 + 40.325 | witness [[8,8,8],[2,2,2,2,2],[1,1],[1,1],[1,1],[1,1]], no CRF, idleSlope 133.120 Mb/s; superset all windows, CRF-ahead mode (it bounds the other two modes) |
| 96 kHz | one format | 18.802 (1 ch, CRF in phase 2) | 51.293 = 18.802 + 32.491 | exact, 351,488 states |
| 96 kHz | mixed | reached 43.215; at most 60.725 | reached 74.826 = 43.215 + 9.115 + 0.2 + 8.960 + 12.336 + 1.0; at most 93.216 | random starts and stops under the exact rule; superset all windows |
| 192 kHz | one format, N <= 6 | - | 32.071 (6 ch, CRF first) | exact occupancy (one stream per phase, first 16 tie phases), packetizer as a queue (tandem) |
| 192 kHz | mixed | 54.822 reached (CRF first, 5 eight-channel frames ahead) | at least 72.915 before packetizer time = 54.822 + 4.557 + 0.2 + 1.0 + 12.336 | exact for the rule's occupancy and the three CRF placements |

- The two reviewer cases: R758-1-F2 configuration with the CRF in phase 1: 42.875 us; R757-1-F4 with the CRF in phase 0: 42.765 us (both match their figures).
- Fewer reservations, 48 kHz, eight channels, no CRF (exact recursion): two co-phased 2064/33.152 = 62.259 us; three 2 x 2064/49.728 = 83.012 us; phases 0 and 1: 62.259 - 20.833 = 41.425 us; phases 0 and 3: 0. Plus 12.336: 74.595, 95.348, 53.761, 12.336.
- Engine load, every legal 16-stream mix (evidence/load192.py): 48 kHz 33.47 % (16 x 8 ch + CRF); 96 kHz 58.05 %; 192 kHz 92.67 % (13 x 8, 1 x 4, 2 x 1 ch, no CRF). Cycles: 16 + NS x N per frame, CRF 22.

### Render buffer (Milan v1.2 4.4.2.1, 5.3.7.6)

- Needed 2.000 + 0.125 + 0.125 = 2.25 ms (>= 2.126 ms): 108, 216, 432 samples at 48, 96, 192 kHz; depth 128, 256, 512 (2.667 ms each); 8 x depth x 32 = 32,768, 65,536, 131,072 bits = 1, 2, 4 RAMB36.
- Ledger: fabric 24.0 - 1.0 + 4.0 = 27.0; total 141.5 + 3.0 = 144.5, 23 over 121.5.

### Save path (N25Q128 Table 32 maxima, Table 17)

- t_page 5.343 ms used as 5.35 (unchanged). T_worst = 10 (T_svc) + 5.35 (one compaction page in flight) + 2 x 1 (two suspends; the 1 ms allowance also covers Table 17's 40 us typical resume-to-suspend) + 32 x 5.35 + 32 x 5.35 = 359.75 ms; margin 140.25 ms (28.05 %).

### Area (estimates)

- Lever 6 net: 5,194 - 218 - 32 = 4,944, so +0.25k against the owner's ~5.2k. Central 20.7 + 0.25 + 1.75 + 1.0 - 1.75 - 0.5 = 21.45k; low 19.1 + 0.25 + 1.25 + 0.5 - 2.5 - 0.8 = 17.8k; high 22.4 + 0.25 + 2.25 + 1.75 - 1.0 - 0.2 = 25.45k. Miss 1.45k centrally.

## Gate table (clean clone at f6b3e841, submodules verilog-axis, protocol-processor, gptp-processor, tsn-c-stack; gate venv with pyyaml, the pinned Markdown renderer, the pinned HDL-reference requirements, wavedrom 2.0.3.post3)

Every step of `.github/workflows/docs.yml` was run as its jobs run it, sequentially (no parallel sweeps), on $VALIDATION_STORAGE/640-a720b/gates/wt at f6b3e841646384177584ce75b657fb8dead7727c. Logs and rc files: ./evidence/gates/ (one log over 200 KB is listed with its digest in evidence/gates/LARGE_LOGS.txt).

| Job | Step (workflow id) | Command | rc | Result |
|---|---|---|---:|---|
| wire-accountability | Advertised-vs-emitted gate | `check_wire_accountability.py --self-test` | 0 | RESULT: PASS |
| docs-check-no-git | Strip git metadata, then run the docs gate | `docs_check.py`, `check_feature_status.py` on `git archive HEAD` without .git | 0 | 0 findings |
| docs-gates-0 | gate_1 HDL reference | `gen_hdl_reference.py --selftest`; `--output` | 0 | index.html written |
| docs-gates-0 | gate_7 link health | `docs_check.py` | 0 | 0 findings, 211 md + 1427 scrubbed files |
| docs-gates-0 | gate_8 em dash | `check_em_dash.py --base e5b8405d` (merge base with live dev) | 0 | 0 findings over 1426 added lines in 7 pages |
| docs-gates-0 | gate_9 concise docs | `check_doc_style.py` (+ `--selftest`), `check_gptp_docs.py` (+ `--selftest`) | 0 | OK; 30 controls |
| docs-gates-0 | gate_10 diagram no-drift | `DOC_MAP.gen.py --check/--selftest`, `timesync_chain.gen.py --check/--selftest` | 0 | OK |
| docs-gates-0 | gate_11 solution docs | `check_solution_docs.py` (+ `--selftest`) | 0 | 43 controls |
| docs-gates-0 | gate_12 submodule docs | `submodule_boundaries.gen.py --check/--selftest`, `check_submodule_docs.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_13 WaveDrom | `gen_wavedrom.py --selftest` and the three `--check` runs | 0 | current |
| docs-gates-0 | gate_14 PNGs | `check_diagram_pngs.py` (+ `--selftest`) | 0 | 6 rasters, 28 controls |
| docs-gates-0 | gate_15 feature status | `check_feature_status.py --self-test` | 0 | 0 findings |
| docs-gates-0 | gate_16 traceability | `gen_module_matrix.py --check` | 0 | up to date |
| docs-gates-0 | gate_18 imported gPTP docs | `check_gptp_docs.py --with-submodule`; `make -C gptp-processor docs` | 0 | PASS |
| docs-gates-0 | gate_19 measurement self-tests | `measure_control_flow.py --selftest`, `measure_cohesion.py --selftest` | 0 | 18 PASS |
| docs-gates-0 | gate_21 bare-metal scope | `check_baremetal_only.py --check` and `--selftest` | 0 | 0 findings over 1425 files; 867 arms |
| docs-gates-0 | ci_step_28 RV32 SDK | `ci_rv32_sdk_selftest.py`; `ci_rv32_sdk.py --destination $HOME/br-milan-rv32/host` | 0 | pinned SDK verified (scratch HOME; see note) |
| docs-gates-0 | gate_24 compiler-absent controls | `test_firmware_compiler.py --selftest`; `--absent --audit` | 0 | GATE 1b PASS; 1 NOT RUN by design; 0 compiler invocations |
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
| docs-gates-0 | gate_44 archive | `check_archive.py` (+ `--selftest`) | 0 | OK |
| docs-gates-0 | gate_45 contents | `gen_toc.py --selftest`, `--verify-anchors`, `--check` | 0 | 150 pages; anchors reproduced |
| docs-gates-0 | gate_46 to 49 | `gen_aem_store.py --self-test`, `check_sweep_shape.py`, `check_deploy_shape.py`, `check_entity_shape.py` (`--self-test`) | 0 | PASS |
| docs-gates-0 | gate_50 CI controls | `ci_gate_workflows.py --check` and the thirteen self-tests | 0 | PASS |
| docs-gates-1 | gate_25_0 builder leg 0 | `ci_builder_legs.py run 0 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS (1 of 103) |
| docs-gates-2 | gate_25_1 builder leg 1 | `ci_builder_legs.py run 1 -- test_builder.py --require-rv32` | 0 | ALL GATES PASS EXCEPT 16 NOT RUN (102 of 103) |
| docs-gates-2 | gate_41 CI events | `ci_events.py --check/--selftest` | 0 | 2199 items, 5258 arms |
| docs-gates-2 | gate_42 act runner contract | `act_ci.py --selftest`; installed copy `--selftest --worktree` | 0 | PASS |
| (lane) | style on touched pages | `style_touched.py` (check_doc_style's analyze()) over 7 pages | 0 | 0 findings in changed blocks |

Notes:
- The 16 NOT RUN gates of leg 1 skip by their own rules: 15 need an interpreter that imports migen, litex and litex_boards, which the docs workflow never installs, and gate 11 needs a local Arty build report. The leg's rc is 0 and its verdict is judged on the union of the legs.
- The SDK step first ran against the SDK already in the home directory and refused it (rc 1: "missing regular SDK provenance receipt"; that tree predates the receipt). The installer never repairs an existing tree, so the pinned archive (sha256 d42680e9...) was installed into a scratch HOME and the CI step, gate_24 and both legs ran there: rc 0. The shared SDK was not modified.
- An earlier gate_24 run under the real HOME was stopped before it finished, to rerun it with the SDK present as CI orders the steps; its partial log is not evidence.
- docs-check "Require every gate exactly once" verifies the uploaded CI receipts and runs only on GitHub; ci-manifest, ci-fail-fast and ci-cancel-tail are CI orchestration. None was run locally. act was not used: it needs a pushed head, and this lane pushes nothing.

## Evidence (./evidence)

| File | sha256 | What |
|---|---|---|
| mixed_stagger.py | bfebe546c8d3df2544660b274aa5c5d857a979932c31b3bf56a4785a09bae5b1 | The executable shaper and phase-rule model (not committed, not a gate). Sections: `checks`, `uniform`, `s48`, `s96`, `c48`, `c96`, `e192` |
| mixed_stagger_results.txt | 8f10158c5eea2beb043c6948442b6286c9849b66d9ff7eda0724bcd552fcb703 | Its output for every section, plus the 192 kHz CRF-first one-format case |
| uniform192_crf_first.py | 0b7b65971a1f503e92a5a8e75907ed629eb3dac5596fb196b6e747ffbadbc945 | That 192 kHz case |
| load192.py, load_by_rate.txt | 4bf0245a..., 540e6ae2... | Worst legal engine load per rate over every 16-stream mix |
| requirement_scope_grep.txt | 5d77baa2a886716ce47562cb9b58acd8b146bf39d27389ddc4fa99a92ea95520 | R757's grep and R758's search at the head |
| style_touched.py, style_touched.log | a792b87b..., caa1e40d... | The checker's analyze() over changed blocks of the 7 touched pages |
| gates/ | per file | Every gate step's log and rc; LARGE_LOGS.txt lists the one log over 200 KB (gate_41_ci_events.log, 337,511 bytes, sha256 be0a6c1d2b39b849139381d0110abea6930832c139ed7334212c3580852c68d9) |
| SHA256SUMS | - | Digests of the files above |

Model run times on this host: checks and uniform under 5 min; `s48 ahead` and `s96 ahead` (full-depth superset) about 2.5 and 5 min. Reproduce with `python3 -I mixed_stagger.py <section>`.

## Not done / not allowed

No push, PR edit, merge, rebase, sub-agent, bench, flashing or Vivado. No RTL, firmware, generator, gate or configuration change. No existing comment edited. The shared RV32 SDK in the home directory was not touched (it carries no provenance receipt; the CI installer refuses it, so the pinned SDK was installed in a scratch HOME).

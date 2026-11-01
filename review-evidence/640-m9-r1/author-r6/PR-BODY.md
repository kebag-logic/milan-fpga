[A720f]

## Contents

- **[Status](#status)** -- Green/WIP/blocked, test tally, and `branch` -> `dev`.
- **[Linked Issue / roles](#linked-issue--roles)** -- Public task, executor, and independent reviewers.
- **[Description](#description)** -- What changed and why.
- **[Round 2](#round-2)** -- How each round-1 finding was closed.
- **[Round 3](#round-3)** -- How each round-2 finding was closed.
- **[Round 4](#round-4)** -- How each round-3 finding was closed.
- **[Round 5](#round-5)** -- How each round-4 finding was closed: the tu merge reduced to requirements.
- **[Round 6](#round-6)** -- How R758-5-F1 and the round-5 residue were closed: the short-margin limit stated and owned.
- **[Authoritative references](#authoritative-references)** -- Requirements/specification clauses and docs.
- **[How to get into the same state](#how-to-get-into-the-same-state)** -- Copy-pasteable checkout/dependency/environment commands.
- **[How to validate](#how-to-validate)** -- Exact reviewer commands and expected result.
- **[Known limitations / out of scope](#known-limitations--out-of-scope)** -- What this deliberately does not do, and why.
- **[Definition of Done](#definition-of-done)** -- The merge bar from [CONTRIBUTING.md](../CONTRIBUTING.md).

## Status

GREEN, documentation only -- every step of the docs workflow exits 0 on a clean clone of head `3f5fea241e8dacd976798ca817c67e55096cf1aa`, including the bare-metal scope gate and both builder legs, and `git diff --check` against the merge base is clean -- `640-mark2-charter` -> `dev` (live dev `1f29f189` merged in; merge base `1f29f189`).

Round 6 answers R757-5 (POSITIVE at `270866ec`, residue only) and R758-5 (NEGATIVE at `270866ec`, one MINOR). The requirement text (NFR-RES-01, NFR-LAT-03, NFR-REL-03, the NFR-SCOUT-02/03/05 amendments and the REQUIREMENTS.md scoping) needs owner approval before merge.

The talker latency target is met by the design only when each port carries 16 reservations of one base format. With mixed channel counts, or with fewer reservations, it is not met; that is an open owner question, not a claim.

## Linked Issue / roles

Relates to #640
Relates to #665
Relates to #823

This is the Mark II charter round; it does not complete #640.

Executor: `[A720f]` (round 1: `[A720]`; round 2: `[A720b]`; round 3: `[A720c]`; round 4: `[A720d]`; round 5: `[A720e]`)
Internal cleared-context reviewer: `[R757]`
External reviewer: `[R758]`

## Description

The owner decisions of 2026-10-31 on #640, #665 and #823, written into the requirements, the split contract, the area plan and a new datapath design. No RTL, firmware, generator, gate or configuration change.

| Commit | File | What changed |
|---|---|---|
| `4083cea5` | `docs/reference/FR_NFR.md` | Round 1: NFR-RES-01 Mark II ceiling; NEW NFR-LAT-03 (talker latency) and NFR-REL-03 (0.5 s save); NFR-SCOUT-02/03/05, the plane table, the out-of-scope note and the traceability rows amended. |
| `cf342310` | `docs/ARCHITECTURE_HW_SW_SPLIT.md` | Round 1: the split restated; no permanent all-fabric option; processor and, at F6, the fabric gPTP plane deleted at their switch-overs. |
| `8ad28659` | `docs/design/MARK_II_STREAM_ENGINES.md` (new), `docs/README.md` | Round 1: the 32x32 shared-engine datapath design. |
| `dfc310fb` | `docs/design/MARK_II_AREA_PLAN.md` | Round 1: target, measured basis, levers, LiteX stages, Block RAM ledger, decisions, lane sequence. |
| `7bcf9a9c` | area plan | The retired host-plane term replaced by "the host tools" (bare-metal scope gate). |
| `9aff05dc` | NFR-RES-01, area plan Target | The 60 % is recorded as the target the #234 ruling kept on 2026-10-03 for this redesign to meet, now replaced; the shipping image is held by the resource gate, with no other LUT bound. |
| `f38badda` | REQUIREMENTS.md, FR_NFR.md, overview architecture, area plan | Every placement, gPTP-owner and gPTP-deadline statement scoped "until the switch-over" or "until F6"; the lever 5 (MMCM servo in firmware) conflict with fabric-owned media published as an open owner decision. |
| `9140079a` | split, area plan, stream engines, FR_NFR.md | The gPTP software named `flexptpd`, with its public MIT fork and one global core state (one port per image) recorded. |
| `f0cfa69c` | stream engines, NFR-LAT-03, area plan | Talker latency re-derived over every legal base-format mix: phase chosen at start by least wire time, never moved; shaper as an exact queue recursion; interference assumptions A1 and A2 stated; per-stream level shown never to bind; the pin-referenced latency instrument. |
| `3eb2f950` | stream engines, area plan | Wire load, engine load and render buffer at 48, 96 and 192 kHz; the 192 kHz reservation limit; the ledger books the 192 kHz buffer (four RAMB36). |
| `ec8ffd98` | stream engines | Each redundant copy carries its own port's time; listener merge rules. |
| `790f7179` | stream engines | Register maps: every bit and offset defined or reserved, the not-mapped encoding, a per-slot render map (Milan v1.2 5.3.10.1), each Milan counter's reset event. |
| `119281c9` | stream engines, NFR-REL-03 | Compaction ordered with power-cut cases; the save worst case gains the compaction page in flight and the second suspend (359.75 ms); `T-NVM-COMMIT-TIMEOUT` restatement assigned; every saved-state clause in the traceability row. |
| `f9786179` | area plan | Lever 6 netted of the kept timestamp return (+0.25k, 32x32 estimate ~21.45k); the lever 2 after lever 3 departure from D16 stated with its reason, for owner approval; Block RAM heading. |
| `3baf35c1` | REQUIREMENTS.md, split, overview, area plan | Changed sentences within ten words, changed paragraphs within twenty. |
| `f6b3e841` | stream engines | The 95.867 µs mixed-format figure bounded to 16-stream mixes. |
| `f11e1eca` | stream engines | Residue: "the only valid copy"; "every Milan counter" wraps; t_page 5.344 ms. |
| `05f3e85e` | stream engines, area plan, NFR-LAT-03 | Every line that says one format meets 65 µs carries "at 16 reservations" and points to the fewer-reservations results; that table gains totals. |
| `45c27020` | stream engines | 192 kHz: the largest legal engine load (93.18 %); all 34 placements that starts and stops reach, searched; the packetizer term proved for mixed formats; the unstaggered wait corrected to 114 µs. |
| `4b8a4d24` | stream engines | Each TDM frame end stamped on both PHCs, so every latency tap measures a copy in its own port's PHC time; the registers name it. |
| `07f8eb91` | stream engines | Listener merge: partner copies matched within a 62.5 µs window derived from a 2.210 µs cross-port error bound; samples placed by count; a copy with tu set never displaces clean partner data; duplicates counted exactly; the merge registers. The tu text left in round 5. |
| `4e14b331` | stream engines, NFR-REL-03 | Compaction: the last replay check and the header are one step no save can split; every save and power-cut point tabled; the replay bounded at 70 pages under S1 and S2. |
| `6f1e03ae` | split, stream engines, area plan | Only the owner's `flexptpd` decision stays under the final decisions; the surveyed source, licence and revision are a proposal for the owner; one instance per port is open owner decision 3. |
| `69fd18f1` | stream engines | Merge follow-up: each rule checks a reference time against the render point where it reads it; a sweep of one context per 31.25 ms only guards the 32-bit wrap. |
| `309bfebc` | stream engines, NFR-REL-03 | A header that fails its read-back is zeroed, or its sector erased, before any save appends to the old slot; both compaction tables and the test name the case. |
| `4d75675f` | stream engines | The conversion error counts the PHC offset drift from the talker's latch to the listener's, under assumption A4: 2.744 µs. |
| `0f6ab84b` | stream engines | Merge: a tu copy waits only while a clean partner copy of its packet can still come; a tu copy no count places in the render span is discarded; tu on both networks stated against Milan v1.2 4.4.2.3; `LAST_TU` added; open design item 1. The tu text left in round 5. |
| `2405f2be` | stream engines, area plan | Redundancy needs gPTP on both ports; one instance per port is one way. |
| `b4b719ea` | stream engines | Why no save can split the check from the header; a save arriving while another is in flight. |
| `2322c6d7` | stream engines | Only a sequence jump out of the render span leaves tu copies unplaced; a restart inside the span is open design item 2. The jump text left in round 5. |
| `22f3cedb` | merge | Live dev `1f29f189` merged in; its REQUIREMENTS.md and docs/README.md lines kept beside this PR's. |
| `d22e071d` | stream engines, area plan | The listener merge reduced to clean copies. The tu rules, tu-only registers and tu loss claims removed. tu behaviour stated as requirements TU-1 to TU-5 with twelve named cases, in one open design item owned by lane 6. |
| `7906c586` | stream engines | Residue: a fault-free save waits for at most one compaction page; any non-header page failing read-back is rewritten further on. |
| `270866ec` | stream engines | TU-2 says a clean copy renders as the rules place it, so a discarded duplicate breaks nothing; case B takes the model's latency. |
| `872ff20e` | stream engines | A margin under 125 µs lapses the head every packet, so interleaved copies can land one sample apart; the placement and Annex D.2 claims hold under a valid head; open design item 3 for lane 6. |
| `3f5fea24` | stream engines | Residue: TU-4 names a stream starting with tu, unpaired or on both networks; rule 2 restarts the map with only bit 0 set. |

Key results (each marked in the pages as measured or estimated):

- **Talker latency at 16 reservations per port** (derived bound, pin to first bit, one interfering 1522-octet frame):

  | Rate | One base format per port | Mixed channel counts |
  |---|---|---|
  | 48 kHz | 63.431 µs worst: met | 92.530 µs reached, at most 95.867 µs: not met |
  | 96 kHz | 51.293 µs worst: met | 74.826 µs reached, at most 93.216 µs: not met |
  | 192 kHz | 34.861 µs worst (N up to 6, all 34 reachable placements): met | 84.319 µs reached, at most 100.825 µs: not met |

  Fewer reservations are worse: with three co-phased eight-channel streams the bound is 123.337 µs. Both cases are open owner question 1.
- **Save at 32x32:** 359.75 ms worst case at datasheet maxima, for change sets up to 32 pages; 365.10 ms after a reported header read-back fault; compaction replays at most 70 pages and ends within 2.05 s under S1 and S2.
- **Area:** about 21.45k LUTs on central estimates at 32x32 (17.8k to 25.45k), above the ceiling centrally.
- **Block RAM:** about 144.5 tiles estimated against 121.5 usable; firmware memory binds first.

## Round 2

Every finding and residue of R757-1 and R758-1 was closed in round 2 (head `f6b3e841`); both round-2 reviews record each as closed at its cause.

| Finding | Closure |
|---|---|
| R757-1-F1, R758-1-F1 (BLOCKER) | The term is gone; `check_baremetal_only.py --check` exits 0. |
| R757-1-F2, R758-1-F5 | NFR-RES-01 and the Target rows record only what was decided: the 60 % kept on 2026-10-03 for this redesign to meet, replaced by the 2026-10-31 ceiling; the resource gate holds the shipping image. |
| R757-1-F3, R758-1-F4 | Every placement, gPTP-owner and gPTP-deadline statement scoped to the switch-over or F6; lever 5 against fabric-owned media is an open owner decision. |
| R757-1-F4, R758-1-F2 | Stagger by wire time, chosen at start, never moved; an executable model over every legal mix at 16 reservations per port; mixed formats not presented as met. |
| R758-1-F3 | Compaction order and power-cut table; NFR-REL-03 names the host flash-model test (round 3 closes the remaining window). |
| R757-1-F5, R758-1-F11 | `flexptpd` named (round 3 separates the decision from the survey's proposal). |
| R757-1-F6 to F13, R758-1-F6 to F12 | Interference assumptions, citations, instrument interval, rates, save terms, register bits, lever 6 credit and the lane order, as listed in the round-2 handoff. |
| Residue and suggestions | Applied as written. |

## Round 3

Every finding and residue of R757-2 and R758-2 is closed below. The lane handoff carries each with file and line and its verification. Round 5 removed the tu text this table describes; [Round 5](#round-5) states what replaced it.

| Finding | Closure |
|---|---|
| R757-2-N1, R758-2-F3, compaction window | Saves have strict priority at every page boundary, so each copy page holds durable values only. Step 4's check (the replay cursor meets the log end) and the header page are one step no save can split; a save arriving during the header page waits for it, within the compaction page already in T_worst, and then appends to the new slot. A table places a save at every point of compaction and shows where it lands; a power-cut table covers every step. The verification row and NFR-REL-03 place a save at every page boundary, including between the last replay page and the header, and fail if the check and the header are split. A host flash model of this ordering (lane evidence): 14,831 runs lose nothing; letting a save run between the check and the header loses changes, the first with no power cut. |
| R757-2 S3, replay passes | S2 read exactly (32 pages, then 10 % of the flash rate): the replay is at most 70 pages and compaction ends within 2.05 s; the standby is erased before the next compaction is due. |
| R757-2-N2, R758-2-F4, listener merge | A clean copy's packet is `k = round((t - head) / 125 µs)`: a 62.5 µs tolerance window either side, against a cross-port conversion error of at most 2.210 µs (IEEE 802.1AS-2020 B.3 1 µs per network, B.1.1 100 ppm, B.1.2 granule; Milan v1.2 4.4.2.1). Samples are placed by count from the head, so the error never shifts a sample (round 6 conditions this on a valid head). A copy with tu set is identified by its own sequence_num (IEEE 1722-2016 4.4.4.6, 4.4.4.7) and is discarded while the partner holds clean data, so it never writes over, advances past or blocks a valid clean partner; a clean copy re-anchors a head a tu copy anchored. A 22-bit written map counts each duplicate once, and each rule treats a reference time the render point passed as invalid. New and changed merge registers; the verification rows add a jittered conversion error, a network latency difference, frame loss, a skewed tu copy arriving first, and three mutations that must fail. A merge model of these rules (lane evidence): 15 cases pass, each mutation fails. |
| R757-2-N3 | Every summary line that says one format meets 65 µs says "at 16 reservations" and links the fewer-reservations results, which gain a total column. |
| R758-2-F1 | 192 kHz engine load 93.18 % (14 eight-channel streams, no CRF), over every mix of 1 to 16 streams; 92.67 % at 16 reservations. |
| R758-2-F2 | At 192 kHz a start always takes the first empty phase in the tie order, so 34 placements hold 16 streams; a search of every start and stop confirms the set. One format: 34.861 µs over all of them (met). Mixed: 84.319 µs reached, at most 100.825 µs including packetizer delay (not met). Nothing is left uncovered. |
| R758-2-F5 | Capture stamps each TDM frame end on both PHCs; each copy's interval uses its own port's PHC at both ends; the latency registers say so; a verification row checks an odd context with a non-zero PHC offset. |
| R758-2-F6, R757-2 S4 | The split page keeps only the owner's decision (`flexptpd`, source and licence confirmed before adoption) under "These decisions are final". The surveyed source, licence and branch `gptp` at `d116d3d` are recorded as the survey's proposal; one instance per port is open owner decision 3. |
| R757-2 RR1 | This body: "(open questions 1 and 7)". |
| R757-2 RR2, R758-2-R1 | Applied as written. |
| Suggestions | R757-2 S1, S2, S3, S4, S5 and R758-2 S1, S2, S3 taken. R758-2 S4 not taken: it adds requirement text, and NFR-SCOUT-03 already carries the obligation after the switch-over. |

## Round 4

Every finding and residue of R757-3 and R758-3 was closed at its stated verification. The lane handoff carries each with file and line. Round 5 removed the tu mechanism the merge rows below describe; [Round 5](#round-5) states what replaced it.

| Finding | Closure |
|---|---|
| R757-3-N4, R758-3-F3, header read-back | A read-back can fail on an intact header, which boot would then prefer. So saves keep waiting, and the writer programs the header page to zeros (a program only clears bits, N25Q128 5.1.2); #823's header format must make an all-zero header fail its check. If the zeroed page fails its read-back too, the writer erases the header's sector, saves still held, a reported double fault outside the bound. Saves resume, on the old slot, only once the header reads back zeroed or erased. A save that waited on a failed header waits one more page: 365.10 ms, a reported fault, within 0.5 s. The landing table, the power-cut table (two new rows, and R757-3 RR3 applied as written), the verification row and NFR-REL-03 name the case. The host flash model gains three failed-read-back cases (intact, torn, and intact with a failing zeroing): 84,674 runs in all lose nothing; the reviewers' sequence (intact header, failed read-back, acknowledged save, cut before the standby erase) boots with the save; removing the zeroing, or ignoring a failed zeroing read-back, loses changes. |
| R757-3-N5, conversion error | The drift term now covers the whole interval between the talker's latch and the listener's. The talker latches at most 125 µs before stamping; a rendered copy arrives before its presentation time, at most the offset plus 125 µs after capture (Milan v1.2 5.3.7.6). Assumption A4: arrival within 2.792 ms of stamping; offsets up to the 2.667 ms span meet it, and a larger offset needs its queueing and transit within it (class A transit 2 ms, IEEE 802.1BA-2011 6.5). So E_x = 2.000 + 200 ppm x 2.917 ms + 0.160 = 2.744 µs; the 62.5 µs window and the neighbour separation still hold. The bench limit and the merge test carry 2.744 µs. A host model derives the error from two PHCs drifting at plus and minus 100 ppm: at most 2.640 µs over 201,280 cases, above the round-3 2.210 µs. |
| R758-3-F1, tu on both networks | Round 4 changed rule 2 so a tu copy waited only while a clean partner copy of its packet could still come, and listed the gaps it knew. R757-4-N6 and R758-4-F1 then found loss outside the model's cases. Round 5 removed the rule and its claims. |
| R758-3-F2, a tu copy far from the head | Round 4 added rule 4, which discarded a tu copy no count placed in the render span. R757-4-N7 and R758-4-F2 found a contradiction beside it. Round 5 removed the rule; the requirement survives as TU-3. The render-span edges stay open design item 1. |
| Merge model | The round-4 model passes its own 33 cases. The round-3 rule 2 fails 13 of them; removing rule 4 fails 7, as its published output says. Both reviews ran it outside those cases and it failed, so it is only a known-failing starting point for lane 6. |
| R758-3-R1 | "Redundancy needs gPTP on both ports (#665 F6). One instance per port is one way." at both places (two sentences, for the 10-word limit). |
| R757-3 RR3, RR4 | Applied as written; RR4's text left with the tu rules in round 5. |
| Suggestions | R757-3 S2 and S3 and R758-3 S1 and S2 taken. R757-3 S1 not taken: it changes the talker's conversion design, and the bound is restated for the design as written. R758-3 S3 (carried) not taken, for the reason given in round 3. |
| Dev merge | Live dev `1f29f189` is merged in. Its added REQUIREMENTS.md line (the soft reset is the controller's AECP REBOOT) names no placement, so this PR's scoping covers it. |

## Round 5

Both round-4 reviews were NEGATIVE with MINOR findings only, every one on the time-uncertain (tu) part of the listener merge or its evidence. Three rounds of rule changes had each opened new cases, so the manager ruled: reduce, do not patch. No new mechanism is added. Each finding below closes by the reduced text. The lane handoff carries file, line and verification.

| Finding | Closure |
|---|---|
| R757-4-N6, R758-4-F1 | The page no longer says what tu loses. Its rules take clean copies only, and rule 1's late and early check no longer reads a tu copy's time. The no-loss statement for tu on both networks, the time-step statement, the one-offset gap and the list of gaps are gone. TU-1 requires that a tu copy is not trusted for placement by its own time (IEEE 1722-2016 4.4.4.7) and that the listener follows Milan v1.2 4.4.2.3. TU-5 makes the loss bound the output of lane 6's model and bench run, for tu on both networks, one network lost, and a skew of at least the 1.5 s step the recovery page grades. The table reads "to be set by lane 6". Cases A to D, F, H and I name the reviewers' probes. |
| R757-4-N7, R758-4-F2 | The contradicting sentence left with the reference it described. TU-4 requires that a stream starting with tu still renders, unpaired or on both networks, with the lane stating how. Case G names the three starts from the first packet and the first clean copy after them. |
| R757-4-N8, R758-4-R1 | The Round 4 row above now reads "removing rule 4 fails 7", matching the published model output. A re-run prints the same. |
| R758-4-R2 | "Past rule 1, a packet's only clean copy always renders." stands as written. Its second sentence names rules that are gone; TU-2 carries what remains. |
| R757-4 RR5 | The two sentences it corrects are gone. Case K names a jump on both networks. |
| R757-4 RR6, RR7 | Applied as written. |
| Suggestions | R758-4 S2: the frame-loss case is in case L; naming a restart signal is not taken, because TU-3 leaves that to the lane. R757-4 S4, S5, S6, S7 and R758-4 S1, S3 are not taken: this round only reduces. S5 and S1 ask for one clause in NFR-REL-03, which waits for the owner's requirement approval. |

What left the page: rules 2 and 4 and the re-anchor on a tu head; the sections on tu placement and on tu on both networks; open design item 2's old count-based text; `SE_MERGE_TU`, `ANCHOR_TU`, `SEQ_VALID`, `CLEAN_VALID`, `LAST_TU`, `LCTX_SEQ_PT` and `LCTX_CLEAN_PT`, whose offsets and bits are now reserved.

What stays, unchanged: the clean-copy merge, the 62.5 µs window and the 2.744 µs bound behind it, the pairing, the duplicate count of clean copies, and the render span. The remaining rules are renumbered 1 to 6. No latency, save, area or Block RAM figure moves; each listener context keeps its 128 octets, 56 of them reserved for lane 6.

`docs/reference/FR_NFR.md` carries no merge or tu claim, so it does not change. The verification row and this body are restated.

## Round 6

R757-5 was POSITIVE with three residue items. R758-5 was NEGATIVE with one MINOR and one residue item. The manager took R758-5-F1's second outcome, which adds no mechanism: the merge rules do not change. No latency, save, area or Block RAM figure moves. The lane handoff carries file, line and verification.

| Finding | Closure |
|---|---|
| R758-5-F1 | The placement line reads "Under a valid head, conversion error never shifts a sample." After the "A new anchor" line the page adds "A margin under 125 µs lapses the head every packet." and "Interleaved copies can then land one sample apart." The Annex D.2 claim carries the same condition: "Under a valid head, clean copies keep that external behaviour." Open design item 3, for lane 6, states the requirement and its verification: clean copies on both networks 10 to 50 µs before their time, first arrival interleaved, at 48, 96 and 192 kHz, every grid phase; the test fails on a shift beyond what the lane states. The reviewer's [published probe](https://github.com/kebag-logic/milan-fpga/blob/f9cfe08cd3f526acde88e0d2a1c48ed2740583df/review-evidence/640-m9-r1/reviews/R758-5/scripts/probe_margin_r5.py) is the starting case. Its [output](https://github.com/kebag-logic/milan-fpga/blob/f9cfe08cd3f526acde88e0d2a1c48ed2740583df/review-evidence/640-m9-r1/reviews/R758-5/receipts/model/probe_margin_r5.out) (up to 766 shifts and 383 unwritten samples in 2,000 packets) is stated as the probe's result, not as a design figure. A re-run of the probe prints the same output. |
| R757-5 RR8, R758-5-R1 | TU-4 reads "A stream that starts with tu, unpaired or on both networks, still renders." The two reviews word this differently and mean the same; RR8's wording is the one applied, since it also gives the matching text for this body's Round 5 row. |
| R757-5 RR9 | Rule 2 reads "it anchors the head and restarts the map with only bit 0 set". |
| R757-5 RR10 | Commit row `07f8eb91` ends "The tu text left in round 5." |
| Suggestions | R757-5 S8 to S13 and R758-5 S1 to S4 are not taken: this round touches only the assigned text. R757-5 S9 is the one-network form of the same lapse, and R757-5 asks the manager to carry it to lane 6. Item 3 names both networks, as assigned. The page's "the pair loses no samples" is unchanged: R758-5 finds it holds, and S9 reads it as too strong in that regime. |

The Round 3 row above says "never shifts a sample"; it now notes the condition.

## Authoritative references

- #640 body ("Updated 2026-10-31") and comments of 2026-10-31; #665 body and comments of 2026-10-31; #823 body and comments of 2026-10-31; the #234 ruling of 2026-10-03; the #640 core survey of 2026-11-01.
- IEEE 802.1Q-2022 8.6.8.2, 34.3.1, 34.6.1, 34.6.1.1, 34.6.1.2, L.3.1.1; IEEE 802.1Q-2014 34.6.1 (Milan's reference).
- IEEE 1722-2016 4.4.4.3, 4.4.4.6 to 4.4.4.9, 7.5, 7.6.
- IEEE 1722.1-2021 7.2.6.
- IEEE 802.1AS-2020 8.4.3, B.1.1, B.1.2, B.3.
- IEEE 802.1BA-2011 6.1, 6.3, 6.5 (Table 6-2).
- Milan v1.2 4.3.3.2 (Table 4.4), 4.3.4, 4.4.2.1, 4.4.2.2, 4.4.2.3, 5.3.5.1, 5.3.7.1, 5.3.7.3, 5.3.7.6, 5.3.7.7, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7, 5.3.8.10, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13, 5.5.2.4, 6.2 (Table 6.1), 8.2.2 to 8.2.5, 8.3.1 to 8.3.5, Annex C, Annex D.2 and D.3.
- N25Q128 datasheet Table 32 (tPP 5 ms, tSE 3 s, tSSE 2 s maxima), Table 17 (suspend parameters), sections 5.1.2 and 9.1.20.
- `docs/design/GM_LOSS_RECOVERY.md` (the time step and its tu); `docs/design/SAVED_STATE_FASTCONNECT.md` section 9.4; `docs/design/SPLIT_CONTROL_MEMORY.md` section 5; `docs/design/MAILBOX_SPLIT.md` measured area.

## How to get into the same state

```sh
git fetch origin
git checkout 640-mark2-charter
git log --oneline --first-parent e5b8405d..HEAD   # thirty-six commits: one per file group or finding group, and the dev merge
git submodule update --init --depth 1 third_party/verilog-axis protocol-processor gptp-processor third_party/tsn-c-stack
python3 -m venv "$HOME/gatevenv"
V="$HOME/gatevenv/bin/python3"
"$V" -m pip install --quiet pyyaml wavedrom==2.0.3.post3
"$V" -m pip install --quiet --require-hashes -r tools/markdown/requirements.txt
"$V" -m pip install --quiet --require-hashes -r tools/hdl_reference/requirements.txt
# the pinned RV32 SDK, into a prefix that does not exist yet
"$V" scripts/ci_rv32_sdk.py --destination "$HOME/br-milan-rv32/host"
```

The gates also need `rsvg-convert`, `sv2v` and `tclsh` on the path, as the workflow installs them. The builder legs require each submodule's `origin` to be its `.gitmodules` URL.

## How to validate

Every step of `.github/workflows/docs.yml`, run as its jobs run them, with the venv first on `PATH`:

```sh
export PATH="$HOME/gatevenv/bin:$PATH"
python3 scripts/docs_check.py
python3 scripts/check_em_dash.py --base "$(git merge-base origin/dev HEAD)"
python3 scripts/check_doc_style.py && python3 scripts/check_doc_style.py --selftest
python3 scripts/check_gptp_docs.py && python3 scripts/check_gptp_docs.py --selftest
python3 docs/DOC_MAP.gen.py --check && python3 docs/DOC_MAP.gen.py --selftest
python3 docs/diagrams/timesync_chain.gen.py --check && python3 docs/diagrams/timesync_chain.gen.py --selftest
python3 scripts/check_solution_docs.py && python3 scripts/check_solution_docs.py --selftest
python3 docs/diagrams/submodule_boundaries.gen.py --check && python3 docs/diagrams/submodule_boundaries.gen.py --selftest
python3 scripts/check_submodule_docs.py && python3 scripts/check_submodule_docs.py --selftest
python3 scripts/gen_wavedrom.py --selftest   # and the three --check runs of the workflow
python3 scripts/check_diagram_pngs.py && python3 scripts/check_diagram_pngs.py --selftest
python3 scripts/check_feature_status.py --self-test
python3 docs/traceability/gen_module_matrix.py --check
python3 scripts/check_gptp_docs.py --with-submodule && make -C gptp-processor docs
python3 scripts/check_baremetal_only.py --check && python3 scripts/check_baremetal_only.py --selftest
python3 scripts/check_doc_paths.py
python3 scripts/check_archive.py && python3 scripts/check_archive.py --selftest
python3 scripts/gen_toc.py --selftest && python3 scripts/gen_toc.py --verify-anchors && python3 scripts/gen_toc.py --check
git diff --check "$(git merge-base origin/dev HEAD)" HEAD
# then the code-quality, source, NVM, shape, CI-control, builder-leg, events and act-runner steps
# of docs-gates-0/1/2, the wire-accountability self-test, and docs-check-no-git on an exported tree
```

Expected result / pass criteria: every step exits 0.

Recorded at `3f5fea24` (every step ran sequentially on a clean clone with the four submodules the jobs fetch):

| Job | Steps | rc |
|---|---|---:|
| wire-accountability | `check_wire_accountability.py --self-test` | 0 |
| docs-check-no-git | `docs_check.py`, `check_feature_status.py` without `.git` | 0 |
| docs-gates-0 | HDL reference; docs_check (0 findings, 213 pages); em dash (0 over 1,754 added lines in 7 pages); doc style and gPTP docs; diagram, solution and submodule no-drift; WaveDrom; PNGs; feature status; traceability; imported gPTP docs; measurement self-tests; **bare-metal scope (0 findings over 1,434 files)**; RV32 SDK; compiler-absent controls; NVM record space, capture census and writer; SoC and RTL source lists; naming, port-contract, fail-fast, TODO, test-evidence and hygiene ratchets; SV, C/C++, Python and shell idioms; cited paths (1,084); archive; contents (`--selftest`, `--verify-anchors`, `--check`); AEM store; sweep, deploy and entity shapes; CI scheduling controls | 0 each |
| docs-gates-1 | builder leg 0: ALL GATES PASS | 0 |
| docs-gates-2 | builder leg 1: ALL GATES PASS EXCEPT 16 NOT RUN; CI events; act runner contract | 0 each |
| (local) | `git diff --check` against the merge base | 0 |

Builder leg 1's 16 NOT RUN gates skip by their own rules: 15 need migen and LiteX, which the docs workflow does not install, and one needs a local build report. The docs-check union step reads GitHub artifacts and runs only there, and act needs a pushed head, so neither ran locally.

`check_doc_style.py`'s own `analyze()` over every changed block of the 7 touched pages: 0 findings (10 words per sentence, 20 words and 2 sentences per paragraph).

The shaper, placement, conversion-error and compaction models and their outputs are lane evidence, not gates; an implementation lane must turn each into a self-checking test. The merge model is only a known-failing starting point for tu (open design item 2). Their digests are in the lane handoffs.

## Known limitations / out of scope

- Documentation only: no RTL, firmware, generator, gate, configuration or saved-state format change. The format and flash layout belong to #823, the writer to #665 F1, gPTP to #665 F6.
- **Open owner question 1: talker latency with mixed formats or fewer reservations.** The phase rule balances wire time only when a stream starts; when other streams stop, heavy frames can stay clustered while idleSlope falls with the reservations. Re-phasing a running stream breaks IEEE 1722-2016 7.6 and padding a reservation breaks Milan Table 4.4. The owner called 65 µs ideal; the choices include accepting the derived bounds, one base format per port, re-phasing with an audio gap, or another stagger or shape.
- The derived bounds rest on assumptions A1 (no own frame above 1522 octets on an AVB port) and A2 (no LPI); with 2000-octet frames the interference term is 16.160 µs instead of 12.336 µs.
- At 192 kHz the shared engines reach 93.18 % load, and mixed formats reach 84.319 µs, at most 100.825 µs (open questions 1 and 7).
- The merge window rests on assumptions A3 (both networks meet IEEE 802.1AS-2020 B.3 in steady state) and A4 (a rendered copy arrives within 2.792 ms of its stamp).
- **Copies with tu set have no merge mechanism yet.** Open design item 2, owned by lane 6, states five requirements and twelve named cases. The merge model of the earlier rounds is a known-failing starting point. This PR states no loss figure for tu: the bound with tu on both networks, with one network lost and with a large skew is that lane's output. Milan v1.2 Annex D.3 covers connectivity loss only.
- The render-span edges are open design item 1 for the same lane.
- **Short margin on both networks:** a margin under 125 µs lapses the head every packet, so interleaved clean copies can land one sample apart; open design item 3 for the same lane sets the allowed shift, and this PR states none.
- After a reported header read-back fault the save waits one more page (365.10 ms); if the zeroed header also fails its read-back, saves wait for its sector's erase, a reported double fault outside the bound.
- Dev's end-station reset page has the protocol processor raise the REBOOT request; after the switch-over the firmware AECP owner must raise it. This charter round does not restate that page.
- **Open owner question: save bursts.** The 0.5 s bound holds while the records changed during one save fit 32 pages and saves stay within 10 % of the flash's worst-case write rate after that burst.
- Table 17 of the flash datasheet gives only typical suspend timings; the derivation allows 1 ms per suspend and the implementation must measure it.
- The 500 ms debounce window uses the whole bound and the 1,000 ms window exceeds it; `T-NVM-COMMIT-TIMEOUT` must be restated. Both belong to #823 and #665 F1.
- Lever 5 (MMCM servo in firmware) conflicts with fabric-owned media (NFR-SCOUT-02/03), lever 2 is proposed after lever 3, and `flexptpd` on two ports with its surveyed source awaits the owner: open owner decisions 1 to 3 in the area plan.
- Block RAM: about 23 tiles over the usable 121.5 on estimates; reductions are unmeasured.
- Area: the central 32x32 estimate is about 21.45k, above the ceiling.
- The measured basis comes from a qualification-image build whose source commit is not on dev; the report digests are recorded in the plan.

## Definition of Done

- [ ] Linked Issue acceptance criteria are satisfied (charter round only; #640's acceptance needs the implementation lanes)
- [ ] New or changed behavior has self-checking tests (no behavior change)
- [x] Required local verification bar passes (every docs-workflow step above)
- [ ] Self-test evidence is posted in a PR comment
- [ ] No undocumented requirement or interface change remains
- [ ] Internal cleared-context review is positive
- [ ] External review is positive
- [ ] Blocking and major findings are fixed and re-reviewed
- [ ] No review round remains in flight
- [ ] Candidate merge result is validated per [CONTRIBUTING.md](../CONTRIBUTING.md)
- [x] Documentation is updated where needed
- [ ] Post-merge containment will be checked before the Issue moves to Done

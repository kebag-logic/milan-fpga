[R757] NEGATIVE - exact head f6b3e841646384177584ce75b657fb8dead7727c

# R757-2: internal cleared-context review of PR #828 (issue #640), round 2

- Head: `f6b3e841646384177584ce75b657fb8dead7727c`, tree `4bb54f5edd8e777b1b7c13c045a318474e7e0d80`.
- Round-2 delta: `dfc310fb..f6b3e841`. Twelve commits, six Markdown pages, 575 lines added and 281 removed. Against base `e5b8405d`, the PR now adds 1,426 lines and removes 112 over seven pages.
- No code, generator, gate, configuration or gitlink is in the delta. That makes this a documentation-only round.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md;
  - docs/README.md;
  - the #640 body ("Updated 2026-10-31", plus the original 2026-10-03 text);
  - the 2026-10-31 owner comments on #640 (16:39, 16:40, 16:47, 16:51, 17:04, 17:21), #665 (16:33) and #823 (17:11, 17:14);
  - the #640 core survey of 2026-11-01;
  - the cited clauses, read in the standards;
  - the round-2 diff and its history;
  - the published evidence tree `review-evidence/640-m9-r1` at `d1a6596b`.
- **Taken as given:** the owner decisions of 2026-10-31 are final and are not reviewed here.
- **Order of reading:** I read my own round-1 report first. I read the other reviewer's round-1 findings only after the verdict, findings and ledger were written. The section "Prior external findings" records that later pass.

## Verdict

NEGATIVE. Three MINOR findings are open, and round 2 introduced all three. No BLOCKER or MAJOR is open.

- **Closed:** every R757-1 finding (F1 to F13) and residue item (R1 to R3) is closed at its cause (table below).
- **Gates:** the bare-metal scope gate and every Markdown-reading docs gate pass at this head (rc 0, `receipts/gates/`).
- **Model:** the `checks` and `uniform` sections reproduce the published output line for line.
- **Bounds:** the stated bounds re-derive.

The open findings:

- **N1:** the compaction ordering can lose a saved change without a power cut.
- **N2:** the listener merge identifies the partner copy by an exact time compare across two time bases.
- **N3:** two summary lines state "one format per port meets 65 µs" without the 16-reservation condition. One format with fewer reservations exceeds 65 µs.

## Findings

### N1 MINOR - Conformance, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:798-799, :831-841, :849, :857, :897; docs/reference/FR_NFR.md:476 (NFR-REL-03) - a save between the last replay and the header is never replayed

- **Authority and evidence:**
  - NFR-REL-03 (this PR) says compaction "loses no saved change, with or without a power cut". The page says "No step drops a durable record without a power cut" (:849). The power-cut table says the new slot has "every durable value" after the header (:857).
  - The ordering:
    - saves keep appending to the active slot "until its commit" (:831);
    - step 4 repeats the replay "until no record is dirty or unreplayed" (:837);
    - step 5 writes the header (:838);
    - only "from then on" do saves go to the new slot (:839).
  - "Compaction yields to saves only between pages" (:799). The step-5 header is a page of its own, so the boundary between step 4's last replay page and the header page is a point where a save may run.
  - **The failing sequence:**
    1. Step 4 exits with nothing dirty.
    2. A change arrives and its save takes the flash at that page boundary.
    3. The save appends record Sx to the old slot, and Sx becomes durable.
    4. The header is written. Boot now uses the new slot, which never received Sx.
    5. Step 7 erases the old slot.
  - So a durable change is lost at the next boot, with no power cut.
  - The verification row (:897) names "change a record after its copy, commit, erase, reboot". That test does not place a save in this window, so it cannot fail for this defect.
- **Impact:** a normative MUST row (NFR-REL-03) and the design's no-loss claim fail for one legal interleaving. A firmware lane that follows the ordering as written ships the window.
- **Required outcome:** one of these, with the verification row naming the interleaving:
  - **(a)** No save can start between step 4's final check and the end of step 5. A save that arrives then waits for the header page. That page is already inside the 5.35 ms "compaction page in flight" term, so T_worst is unchanged.
  - **(b)** Before switching, step 6 replays every active record above the last one replayed.
- **Verification:**
  - Read the ordering text and the power-cut table.
  - The host flash-model test issues a save between the last replay page and the header page, then commits, erases, reboots and reads the new value.

### N2 MINOR - RTL, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:456-468, :473-494, :644, :893-894 - the merge identifies the partner copy by an exact time compare across two time bases

- **Authority and evidence:**
  - **Two time bases:** the talker stamps the odd copy in port 1's time by adding "the offset between the two PHCs", latched in the talker (:457-463). The listener converts back with "the same measured offset in reverse", measured on its own two PHCs (:466-468).
  - **Two clocks:** each port's PHC follows a different network's grandmaster (Milan v1.2 8.3.4; IEEE 1722-2016 4.4.4.9). So the talker's latched offset and the listener's measured offset differ by the synchronization error of four PHCs.
  - **The compare:** after conversion, the two copies of one packet therefore carry presentation times that differ by a small, signed error. They are not equal. Rule 2 renders "a copy later than the last written time" (:484), compared exactly in wrapping 32-bit time (:494, `LCTX_LAST_PT` :644).
  - **When the partner copy lands later by any amount:**
    - rule 2 classifies it as a new packet;
    - a tu copy then overwrites a clean one, which defeats rule 3 (:485);
    - `LAST_TU` flips;
    - rule 4 never fires, so `SE_MERGE_DUP` and `SE_MERGE_SEC` miscount (:568-569).
  - **When it lands earlier:** it is a duplicate, so the outcome depends on the sign of a jitter term.
  - **Tests:** the verification rows (:893-894) cut a network, change a grandmaster and set tu on both copies. None runs two PHCs with a non-zero, jittered offset, so none can fail for this.
- **Impact:** the clean-copy preference the merge was written to provide (R757-1 S2, `ec8ffd98`) holds only when the conversion error is exactly zero, and the duplicate counters lose their meaning. In the worst case, a sample-boundary straddle writes one packet at two adjacent indices.
- **Required outcome:**
  - Packet identity across the pair is defined with a tolerance, for example a copy is new only if it is later by more than half a packet interval. Another shared key would also do.
  - The bound on the cross-port conversion error is stated.
  - The merge verification runs with a non-zero, jittered inter-network offset.
- **Verification:**
  - The merge rule text and the `LCTX_LAST_PT` row.
  - The merge simulation row, with a test that fails when the tolerance is removed.

### N3 MINOR - Conformance, Docs - docs/design/MARK_II_STREAM_ENGINES.md:19; docs/design/MARK_II_AREA_PLAN.md:60 - "one format per port meets 65 µs" stated without the 16-reservation condition

- **Authority and evidence:**
  - **The two lines:**
    - the stream-engine Contents label reads "Talker latency budget -- One format per port meets it." (:19);
    - the area plan Target row reads "derived as met with one base format per port, not with mixed formats" (:60).
  - **What was derived:** the page derives "met" for one format only at 16 reservations per port (:312-332).
  - **What it shows elsewhere:** one format with fewer reservations exceeds 65 µs. With two co-phased eight-channel streams, the shaper wait is 62.259 µs (:348). With the 40.325 µs fixed terms the total is 102.584 µs, and three co-phased streams give 123.337 µs (`receipts/arith_check.txt`).
  - **Where it is right:** NFR-LAT-03 (FR_NFR.md:306) and the area plan's D14 row (:255) state it correctly: "met with one base format per port, exceeded by mixed formats and fewer reservations".
  - Focus item 3 requires that no case above 65 µs is stated as met.
- **Impact:** two summary lines present a case above 65 µs as met, and they contradict the requirement row they summarise.
- **Required outcome:**
  - Both lines say "at 16 reservations per port".
  - The Target row also names fewer reservations as open.
  - For example: "One format per port meets it at 16 reservations." And: "derived as met with one base format at 16 reservations per port; not with mixed formats or fewer reservations (open)".
- **Verification:** grep both pages for "meets it" and "derived as met". Each hit carries the 16-reservation condition.

## RESIDUE (wording only; each changes no figure, verdict, test or gate)

- **RR1** - PR #828 body, "Known limitations". The text reads "the latency there was bounded only before packetizer time for mixed formats (open question 7)". Mixed-format latency at 192 kHz is open question 1 on the page (:904-905). Open question 7 is engine headroom. Exact fix: "(open questions 1 and 7)".
- **RR2** - docs/design/MARK_II_STREAM_ENGINES.md:488. The text reads "No rule drops the only copy of a packet." Rule 1 drops a copy that fails the stream checks, even when it is the only copy. Exact fix: "No rule drops the only valid copy of a packet."

## SUGGESTIONS (optional)

- **S1:** give the "Fewer reservations" table (:346-351) a total column, so that "With interference" is not read as the bound. For example, three co-phased streams total 95.348 + 27.989 = 123.337 µs.
- **S2:** state why the 8.560 µs packetizer term also bounds mixed formats. At 48 kHz, a phase's wire load before its last join is at most 4,128 bits. Any higher value needs at least three streams in each of the other five phases, which is 15 streams. So a phase never exceeds 6,192 bits, and eight-channel frames have the highest cycles per bit, so it never exceeds 192 cycles. The same argument at 96 kHz caps a phase at two eight-channel frames, 224 cycles. That closes the derivation's only unproved term.
- **S3:** say that step 4 terminates under S2, or bound its replay passes. "Until no record is dirty" waits for a quiet instant.
- **S4:**
  - docs/ARCHITECTURE_HW_SW_SPLIT.md:82 lists "The adopted revision is branch `gptp` at `d116d3d`" under "These decisions are final". The pin comes from the lane survey, not from an owner ruling. "Surveyed revision" would be exact.
  - The source and licence are now public and confirmed: `kebag-logic/flexPTP` is public, MIT, a fork of `epagris/flexPTP`, and branch `gptp` is at `d116d3dfe8e6`. Its `linux/` target builds `flexptpd` (`receipts/flexptp_identity.txt`).
- **S5:** SE:785 gives t_page as 5.343 ms. The exact sum is 5.3438 ms, which is 5.344 ms to three places. This is pre-existing and has no effect, since 5.35 ms is used.

## Round-1 findings (R757-1) at this head

| Item | Closed by | Evidence at this head |
|---|---|---|
| F1 BLOCKER, bare-metal gate | `7bcf9a9c` | `check_baremetal_only.py --check` rc 0, "0 findings across 1425 tracked first-party file(s)". `--selftest` rc 0, 867 arms. AP:159 reads "the host tools" and AP:273 reads "host-tool". **Closed** |
| F2 MAJOR, "Mark I bound" | `9aff05dc` | NFR-RES-01 (FR:473) says the ceiling replaces the 60 % "which the owner kept on 2026-10-03 for this redesign to meet". That matches the #234 ruling and the #640 original body. The shipping image is held by the resource gate (#638) "and carries no other LUT bound". 52,008 / 63,400 = 82.03 %. The AP Target row matches. "Mark I bound" no longer appears. **Closed** |
| F3 MAJOR, contradicting requirement text | `f38badda` | RQ:25-47, RQ:58-59, RQ:110, RQ:156-159 and RQ:333-334; FR:75-85, FR:108, FR:305, FR:320, FR:327, FR:456-457, FR:477 and FR:517; OV:2-19 and OV:81-87. Every hit of my round-1 grep is scoped "until the switch-over" or "until F6", or is current-image or transition text. The split page's hits are pre-existing transition or current-image lines (for example, :293 sits in the verification bar during transition). The changes scope only; see focus item 8. **Closed** |
| F4 MAJOR, mixed-format worst case | `f0cfa69c`, `f6b3e841` | Phase rule (SE:179-214); results table (SE:317-324); NFR-LAT-03; open question 1. Mixed formats are not stated as met anywhere. My `checks` run reproduces both round-1 cases: 42.765 µs (mine) and 42.875 µs. **Closed**. N3 is a new residual summary defect |
| F5 MINOR, flexptpd identity | `9140079a` | `flexptpd` is named as decided. Its source is public: MIT, a fork, branch `gptp` at `d116d3d`, confirmed via the API (`receipts/flexptp_identity.txt`). One port per image is open (SP:83-84; SE open question 5; AP D13 and lane 9). **Closed**, with S4 |
| F6 MINOR, interference assumptions | `f0cfa69c` | A1 and A2 (SE:274-285). 802.1BA-2011 6.3 caps frames at 2,000 octets and gives 1,522 only as its example. A2 is 6.1 a), and 6.1 b) 4) allows a 30 µs wake. 16.160 µs is shown. Read in the standard. **Closed** |
| F7 a-d, citations | `f0cfa69c`, `790f7179`, `119281c9` | a) SE:229-233. b) SE_RMAP cites 5.3.10.1, and TCTX_MAP cites 5.3.9.1. c) N in {1, 2, 4, 6, 8} at SE:51, :590 and :630. d) FR:613 lists every non-volatile clause found by grepping Milan v1.2 (5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.1, 5.3.8.2, 5.3.8.3, 5.3.8.7, 5.3.9.1, 5.3.10.1, 5.3.11.1, 5.3.13), plus 5.5.2.4. **Closed** |
| F8 MINOR, instrument interval | `f0cfa69c` | SE:359-377: the start is the PHC frame-end stamp, less the synchronizer delay and the slots after the stream's last slot; the end is the first bit plus the PHY egress constant. Registers are "pin-to-first-bit" (SE:563-566, :612). The NFR-LAT-03 test names these taps. **Closed** |
| F9 MINOR, rates | `3eb2f950` | Render buffer at 1, 2 and 4 RAMB36 (SE:407-411). The ledger books 4.0 (SE:677). The 192 kHz cap is at most 13 eight-channel streams with a CRF (SE:85). Engine loads are 33.47, 58.05 and 92.67 % (SE:134-136). There is a 96 kHz budget column. All re-derived (`receipts/arith_check.txt`). **Closed** |
| F10 MINOR, save terms and timeout | `119281c9` | T_worst = 10 + 5.35 + 2 x 1 + 2 x 32 x 5.35 = 359.75 ms (SE:789-792). The `T-NVM-COMMIT-TIMEOUT` restatement is assigned to #823 and #665 F1 (SE:804-805, open question 6, NFR-REL-03). **Closed**. N1 is a new defect in the compaction ordering added by the same commit |
| F11 MINOR, register bits and resets | `790f7179` | Every field covers bits 31:0 exactly once, and offsets are contiguous in all three tables. `scripts/regmap_check.py` reports PASS, with two negative controls (`receipts/regmap_check.txt`, `receipts/regmap_controls.txt`). Talker counters reset on RUN rising (5.3.7.7). Listener counters reset by CNT_CLR on not-bound to bound, and are kept on unbind (5.3.8.10). Both read in the standard. **Closed** |
| F12 MINOR, lever 6 credit | `f9786179` | AP:175 has +0.25k (5,194 - 218 - 32 = 4,944). The estimate is 21.45k (17.8k to 25.45k), 1.45k over. Re-derived. **Closed** |
| F13 MINOR, lane order vs D16 | `f9786179` | The AP D16 row, AP:288-289 and open decision 2 state the departure, its reason, and that it is a proposal for the owner. **Closed** |
| R1, R2, R3 | `f0cfa69c`, `119281c9`, `f9786179` | SE:297 reads "Four 50 MHz cycles (0.080 µs), rounded up to 0.200 µs (estimate)". SE:921-922 is split into two items. The AP heading reads "Mark II Block RAM ledger", with the anchor unchanged and `gen_toc --check` rc 0. **Closed** |
| S1 to S4 (optional) | various | Taken: the per-stream level at SE:239-245 (the model check prints 125.000 µs at each rate); the merge cases; one PHC per port (FR:500); the CRF phase and order (SE:185, :196) |

## What was checked, per focus item

1. **Round-1 findings:** see the table above. Every item is closed at its cause.
2. **Docs gates at the head:** I ran 22 commands myself, in a pinned-renderer venv (`receipts/gates/*.log` and `*.rc`). All rc 0:
   - `check_baremetal_only.py --check` and `--selftest`;
   - `docs_check.py`, with 0 findings over 211 pages;
   - `check_em_dash.py --base e5b8405d`, with 0 findings over 1,426 added lines in 7 pages, and its `--selftest`;
   - `check_doc_style.py` and its `--selftest`;
   - `check_gptp_docs.py` and its `--selftest`;
   - `DOC_MAP.gen.py --check` and `--selftest`;
   - `check_solution_docs.py`;
   - `check_submodule_docs.py`;
   - `check_feature_status.py` and its `--self-test`;
   - `gen_module_matrix.py --check`;
   - `check_doc_paths.py`, where 1,075 paths resolve;
   - `check_archive.py` and its `--selftest`;
   - `gen_toc.py --selftest`, `--verify-anchors` (566 links) and `--check`.

   The style probe runs `check_doc_style`'s `analyze()` over every changed prose block of the 7 pages. It finds 0 issues; paragraphs run 5 to 20 words (`receipts/style_probe.txt`). For the full workflow, the author's published receipts (gate table, `author-r2/evidence/gates/`) record rc 0 for every docs-workflow step, including both builder legs. I verified their digests against the manifest; I did not re-run the submodule, SDK or builder steps.
3. **Shaper model:** I ran the `checks` and `uniform` sections of `mixed_stagger.py`, after checking its digest against `SHA256SUMS`, and each finished in under 5 minutes (`receipts/model/`). All 30 output lines match the published `mixed_stagger_results.txt` exactly.
   - **48 kHz, one format:** a 23.106 µs wait over 17,658 reachable states, which gives 63.431 µs.
   - **96 kHz, one format:** 18.802 µs over 351,488 states, which gives 51.293 µs.
   - **Model facts:** F1 (the queue recursion equals the 8.6.8.2 simulation) and F2 (one interferer adds at most 12.336 µs) both print True at every rate. The per-stream level peaks at 125.000 µs.
   - **Witness:** I re-derived it by hand. It is a start and stop sequence under the rule (12 eight-channel streams, a 13th into phase 0, stop phase 1's pair, five two-channel streams, stop the scaffold, eight one-channel streams). It gives idleSlope 133.120 Mb/s, a 53.085 µs wait and 92.530 µs in total.
   - **Mixed bound:** 95.867 = 55.542 + 40.325 is the superset bound (sections s48 and s96 were not re-run; they are optional).
   - **192 kHz, one format:** the "first 16 tie phases" occupancy is the whole reachable set. With at most 16 streams, a new stream always takes the first empty phase in tie order.
   - **Above 65 µs:** every such case is recorded as open question 1 and not stated as met (NFR-LAT-03, SE:320-333, SE:904-913, AP D14). The exceptions are the two summary lines in N3.
4. **Save worst case:**
   - **Inputs:** the N25Q128 datasheet, read in the PDF. Table 32 gives tPP max 5 ms, tSE max 3 s and tSSE max 2 s. Table 17 gives an erase suspend latency of 15 µs typical with no maximum, and 40 µs typical from erase resume to suspend ("timing not internally controlled"). Section 9.1.20 allows programming in a suspended sector erase, but not in a suspended subsector erase.
   - **Result:** t_page is 5.3438 ms, used as 5.35 ms. T_worst is 359.75 ms with a 140.25 ms margin (`receipts/arith_check.txt`). The sum over-counts, because the compaction page and the save in flight cannot both precede the change. So it is a sound upper bound.
   - **Compaction ordering:** sound against copy and replay inversion, and against each power-cut row, except the window in N1.
5. **Render buffer and Block RAM:**
   - **Requirement:** Milan v1.2 4.4.2.1 requires 2.126 ms (2 ms + 125 µs + 1 µs).
   - **Buffer per rate:** 2.25 ms needs 108, 216 and 432 samples. The depths of 128, 256 and 512 hold 2.667 ms each, which is 1, 2 and 4 RAMB36.
   - **Other limits:** offsets above 2.667 ms count as EARLY_TIMESTAMP (5.3.8.10, "too far in the future to process").
   - **Ledger:** fabric 27.0; total 144.5 against 121.5 usable, 23 over. That is recorded as open question 3 and in the area plan.
6. **Redundancy time bases:**
   - **Time base per port:** Milan v1.2 8.3.4 requires two gPTP end stations, one per interface. IEEE 1722-2016 4.4.4.9 derives avtp_timestamp from gPTP. So each copy carries its own port's time, as the page now says.
   - **Merge rules:** tu (4.4.4.7) and Milan 4.4.2.3 (free-wheel) were read in the standards. Neither drops samples. The rule order never drops the only valid copy (RR2 is wording), but the identity compare is defective (N2).
   - **Mapping pairs:** Milan 8.3.2.1.4 pairs the mappings, as the page says.
7. **Register maps:** every bit and offset is defined or reserved, and the widths sum to 32 per register (`receipts/regmap_check.txt`). The not-mapped value is 15, and VID is 12 bits at 27:16. ERR covers NCH, NSR, PHASE and SLOT. The PTO reset of 0x001E_8480 is 2,000,000 ns (5.3.7.6), and its 31-bit field matches 0 to 0x7FFFFFFF.
8. **Requirement scoping:** the REQUIREMENTS.md and FR_NFR.md changes add scope qualifiers ("until the switch-over", "until F6", "after F6") or restate decisions that are recorded on the issues:
   - 16:33: no retained fabric processor;
   - 16:51: gPTP to software, timestamps on both ports;
   - 17:04: `flexptpd`;
   - #823 17:11 and 17:14: the 0.5 s save and the timeout restatement.
   
   The lever 5 conflict and the lever 2 order are published as open owner decisions, not decided. "After F6, each gPTP path states its firmware bound" restates the existing NFR-SCOUT-03 text. Nothing beyond the decisions is presented as decided. S4 is the one revision-pin wording point, on the split page.
9. **flexptpd:** named with its public source, `kebag-logic/flexPTP`, MIT. I confirmed it through the GitHub API: fork true, parent `epagris/flexPTP`, branch `gptp` at `d116d3dfe8e6`, and `linux/CMakeLists.txt` builds `flexptpd`. One port per image stays open (SP:83-84, SE open question 5, AP D13 and lane 9).

### Comment rule

No source file is in the delta, so no new comment-rule instance is possible.

### Privacy

- No private host, path or device appears in the added lines.
- Bench equipment is named by role.
- The PR body and the findings name lanes, which is allowed.

### Evidence integrity

- `author-r2/evidence/SHA256SUMS`: every file OK.
- `MANIFEST.json`: all 305 entries match their published digests, with none missing and none unlisted.
- Redacted files are flagged as such in the manifest.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N1, N3) | NFR-RES-01, NFR-LAT-03, NFR-REL-03, NFR-SCOUT-01/02/03, NFR-OBS-01, the Time row and the saved-state row in FR_NFR.md; REQUIREMENTS.md sections 1 and 4 and REQ-VER-05; split page sections 1 and the end state; the overview; the area plan Target and decisions; every changed clause citation, read in Milan v1.2, IEEE 1722-2016, 802.1Q-2022, 802.1BA-2011 and the N25Q128 datasheet; the 2026-10-31 decisions | R757-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| RTL | UNCLEAN (N2) | SE engines and throughput per rate, capture and render buffers, phase rule, shaper recursion, fixed terms, latency instrument, port time bases, merge rules, register maps (`scripts/regmap_check.py`), Block RAM ledger; AP lever arithmetic | R757-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Robustness | UNCLEAN (N1, N2) | mixed formats and fewer reservations; the 192 kHz cap; offset overflow; compaction interleavings and power-cut rows; merge under tu, a single copy and cross-base conversion error; ERR paths and reset values; counter reset events | R757-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Tests | UNCLEAN (N1, N2) | docs gates re-run at the head (`receipts/gates/`); model `checks` and `uniform` re-run (`receipts/model/`); the author gate receipts and digests; the SE verification table; NFR-LAT-03 and NFR-REL-03 verification clauses; hosted check runs at the head (`receipts/hosted_checks.tsv`) | R757-2 | f6b3e841646384177584ce75b657fb8dead7727c |
| Docs | UNCLEAN (N1, N2, N3) | all seven touched pages; the style probe; em dash, TOC, anchor, path and bare-metal gates; the PR body's round-2 table and claims (RR1) | R757-2 | f6b3e841646384177584ce75b657fb8dead7727c |

## Prior external findings (R758-1), read after the verdict and ledger

This section was written after the verdict, findings and ledger. Each item is resolved or retained at this head as follows.

| R758-1 item | At this head |
|---|---|
| F1 BLOCKER, bare-metal gate | **Resolved:** as R757-1-F1, rc 0 at the head |
| F2 MAJOR, mixed channel counts | **Resolved:** mixed formats are derived as not met and are open question 1. The model reproduces the 42.875 µs case. N3 retains a summary-line remainder for fewer reservations |
| F3 MAJOR, compaction loses changes | **Resolved for the named case:** a record changed after compaction copied it is replayed by steps 3 and 4 (SE:834-848). The verification row names the host-model test. **Retained in part as N1:** a save in the boundary between the last replay page and the header page is still not replayed |
| F4 MAJOR a-d, contradicting requirement text | **Resolved:** (a) RQ:25-47; (b) FR:75-85 and NFR-OBS-01 (FR:477); (c) OV:2-19; (d) the lever 5 conflict is open owner decision 1 (AP:291-300) and is recorded in NFR-SCOUT-02. The grep finds no unscoped hit, and AP:159 and AP:273 no longer use the retired term |
| F5 MAJOR, "Mark I bound" | **Resolved:** as R757-1-F2 |
| F6 MINOR a, b | **Resolved:** N in {1, 2, 4, 6, 8} (SE:51, :590, :630). 802.1Q-2014 34.6.1 is 802.1Q-2022 34.6.1.1 (SE:229-233) |
| F7 MINOR a, b | **Resolved:** (a) as R757 R1. (b) "Any order" is gone; SE:199-214 states what starts and stops reach, and the results come from the reachable set or a superset of it. The grep for "any order" finds nothing |
| F8 MINOR, render buffer per rate | **Resolved:** as R757-1-F9. 4.4.2.1 is cited as the sizing authority |
| F9 MINOR a, b, time domains and tu | **Resolved:** (a) each copy is stamped in its own port's time (SE:448-469). (b) No rule drops the only valid copy, and both-tu renders the first copy (SE:481-492). N2 is a separate, new defect in the identity compare those rules rely on |
| F10 MINOR, register bits and offsets | **Resolved:** `regmap_check.py` passes. The PORT reset rule is stated (SE:527); 15 means not mapped (SE:594); VID is 12 bits (SE:599, :638) |
| F11 MINOR, flexptpd | **Resolved:** as R757-1-F5. The 16:51 decision is linked (SP:79, FR NFR-SCOUT-02, AP D13) |
| F12 MINOR, lane order | **Resolved:** as R757-1-F13 |
| R1 RESIDUE, paragraph length | **Resolved, no change needed:** 0 changed paragraphs exceed 30 words, and all are within the enforced 20-word limit (`receipts/style_probe.txt`). The manager's residue list may close it |
| S1 to S6 | **Taken:** S1 at SE:239-245; S2 at SE:393; S3 at FR:613; S4 at SE:760-764; S5 at SE:185 and :196; S6 at SP:79 and FR:328 |

There are no PR review comments or line comments beyond the round-1 reports and the review-start notices. No other prior public finding exists.

## Real limits

- **Model sections:** I ran only `checks` and `uniform`. The superset sections `s48` and `s96` were not re-run, so the 55.542 µs and 60.725 µs superset bounds rest on the published output. I did re-derive the reached witness by hand.
- **Gates not re-run:** the submodule-dependent docs-workflow steps were not re-run. These are the HDL reference, the RV32 SDK, the builder legs, the code ratchets, NVM, CI events and the act contract. The author's published receipts are the source-head evidence for them, and the delta contains no file they scan.
- **Hosted runs:** at the time of reading (03:4x UTC), `docs-gates-0/1/2` were still in progress at this head. `docs-check-no-git`, `wire-accountability`, `rtl-fast` and `elaborate` had succeeded. `verilator-suites`, `yosys-portability` and the firmware jobs were skipped contexts, consistent with a docs-only delta.
- **Not used:** hardware, bench, act, a hosted re-run and the builder bank. Physical calibration was not run, and field skips are not hardware proof.
- **Manager bank:** no manager source bank ran at this head, and this round claims none.
- **Clone state:** the clone is unchanged. The worktree and index equal HEAD, and mode, blob and path listings are identical. The six gitlinks are unchanged (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept the hosted `docs-check` at this head, once `docs-gates-0/1/2` complete with all three legs executed.
- Accept `verilator-suites` and `yosys-portability` as skipped contexts for a documentation-only head.
- Validate the current-dev merge candidate at the merge turn, with the builder and native banks. Source base and live dev are both `e5b8405d`.
- Get owner approval of the requirement text, as the PR states, and of open decisions 1 and 2 in the area plan.
- Carry RR1 and RR2 to the residue checklist.

R757-2 FINISHED

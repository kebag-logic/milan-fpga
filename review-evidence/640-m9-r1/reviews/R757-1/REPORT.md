[R757] NEGATIVE - exact head dfc310fb3dec28f3d06333973e61cde44a4e786d

# R757-1: internal cleared-context review of PR #828 (issue #640)

- Head: `dfc310fb3dec28f3d06333973e61cde44a4e786d`, tree `4881b68d4cbb69d920bc154af3ded7d14fa3e83c`.
- Delta: `e5b8405db4c1f7cbdafb5df92b15b580142e0232..dfc310fb`. Four commits, five Markdown pages, 1,095 added lines. No code, generator, gate or configuration file changes.
- Reconstructed from: AGENTS.md, CONTRIBUTING.md (sections 6 and 6.1), docs/README.md, the #640 body ("Updated 2026-10-31") and its 2026-10-31 comments, the #665 body and its 2026-10-31 comments, the #823 body and its two 2026-10-31 comments, the #234 decision of 2026-10-03 that the area plan cites, the cited clauses, the diff, and the published evidence tree `review-evidence/640-m9-r1` at `8d2ac568`.
- Prior public review findings on PR #828: none. The PR has only the two review-start comments, so nothing had to be resolved or retained.
- The 2026-10-31 decisions are taken as final. Findings below concern how the pages record them, and the claims the pages derive from them.

## Verdict

NEGATIVE. One BLOCKER, three MAJOR and nine MINOR findings are open. All five lenses are unclean at this head.

The BLOCKER: the docs workflow's required gate fails at this exact head, both on the hosted run and when reproduced here. That contradicts the PR's "GREEN, every docs gate exits 0".

## Findings

### F1 BLOCKER - Docs, Tests - docs/design/MARK_II_AREA_PLAN.md:155 and :268 - the docs workflow's bare-metal scope gate fails at this head

- **Authority and evidence:**
  - `.github/workflows/docs.yml` job `docs-gates-0` runs `python3 scripts/check_baremetal_only.py --check`. This is part of the protected `docs-check` context (CONTRIBUTING lists `docs-check` among the required contexts).
  - Hosted run 41256380559, job 124700311433, step 28, at this head: failure. Its output: `docs/design/MARK_II_AREA_PLAN.md:155` and `:268`, `[H] retired target host-plane surface 'hostplane'` (#259), `baremetal-only: FAIL (2 finding(s))`.
  - Reproduced here: `receipts/gates/baremetal_check.log`, rc 1, the same two findings. The base page has 0 occurrences, so this delta introduced both.
  - The author's published validation list never runs this gate, and the PR body's "every docs gate exits 0" is false at this head.
  - Fail-fast cancelled `docs-gates-1` and `docs-gates-2`, so the hosted `docs-check` concluded failure (`receipts/hosted_checks.tsv`).
- **Impact:** a required status context is red, so the head cannot merge. The PR's evidence claim is wrong.
- **Required outcome:**
  - Both lines name the consumers without the retired term, for example "the host tools".
  - `check_baremetal_only.py --check` exits 0.
  - The PR's validation list includes every docs-workflow gate that reads Markdown.
- **Verification:**
  - `python3 scripts/check_baremetal_only.py --check` rc 0 at the new head.
  - A green hosted `docs-check` with all three `docs-gates-*` legs executed.

### F2 MAJOR - Conformance, Docs - docs/reference/FR_NFR.md:465 (NFR-RES-01) and docs/design/MARK_II_AREA_PLAN.md:64, :66 - "Mark I bound" of 60 % presented as an owner decision

- **Authority and evidence:**
  - The cited decision ([#234, 2026-10-03](https://github.com/kebag-logic/milan-fpga/issues/234#issuecomment-5967924270)) says the 60 % target is met "by a redesign in the new milestone Optimisations Mark II", and the resource gate holds recorded values until then. It retained 60 % as the redesign target. It set no bound on the current image.
  - The #640 body (2026-10-31) says the 20,000-LUT target "replaces the 60 % (38,040-LUT) target", and that "NFR-RES-01 ... is amended to match".
  - At this head, NFR-RES-01 says instead: "Mark I bound: the current all-fabric image ... keeps the earlier target of at most 60 % LUT (38,040) as its bound". The plan says "The owner retained the 60 percent target ... for Mark I".
  - The current image measures 52,008 LUTs (`receipts/build_report_digests.txt`).
- **Impact:**
  - A normative MUST row carries a bound that no decision set, attributed to a decision that says something else.
  - The shipping image fails that bound by 13,968 LUTs.
- **Required outcome:**
  - NFR-RES-01 and the plan's Target table record only what was decided: the Mark II ceiling replaces the 60 % target.
  - The current image is held at its recorded figures by the resource gate, as #234 says.
  - Any Mark I bound is either removed or raised as an owner question.
- **Verification:** the NFR-RES-01 text and the plan's Target rows, read against #234 and the #640 body.

### F3 MAJOR - Conformance, Docs - REQUIREMENTS.md:25-30, :32-33, :37-39 and docs/reference/FR_NFR.md:76-80 - requirement text left contradicting the new split

- **Authority and evidence:** the 2026-10-31 decisions (#665 body and 16:33; #640 16:51 and 17:04) are recorded in the amended NFR-SCOUT-02 and NFR-SCOUT-03 and in the split page. Three passages of requirement text still contradict them:
  - **Placement:** REQUIREMENTS.md section 1 still requires "build-selectable placement" for ADP, ACMP, AECP, MAAP and SRP. It also says "The all-fabric build remains a supported option."
  - **gPTP owner:** it says "The fabric gPTP plane is the sole product PHC, protocol, servo, and public state owner". It also says "The fabric MUST retain ... the gPTP plane" and "Audio and gPTP deadlines MUST remain independent of firmware service".
  - **FR_NFR section 1:** the same page this PR amends still says "Mark II selects ADP, ACMP, AECP, MAAP and SRP per function ... The all-fabric option remains supported."
  - NFR-SCOUT-08 points readers to REQUIREMENTS.md section 1 as the product-ownership authority.
- **Impact:** the top-level requirement authority and the amended FR_NFR rows disagree on the end state, the gPTP owner and the deadline rule. A cold reader or an implementation lane gets the superseded rule.
- **Required outcome:** every requirement passage that states placement, the gPTP owner or the gPTP deadline rule is consistent with the decisions. Pre-switch-over statements are scoped as "until the switch-over" or "until F6".
- **Verification:** `grep -n -i -E 'all-fabric|build-selectable|fabric gPTP plane is the sole|gPTP deadlines' REQUIREMENTS.md docs/reference/FR_NFR.md`. No unscoped hits should remain.

### F4 MAJOR - Conformance, RTL, Robustness, Docs - docs/design/MARK_II_STREAM_ENGINES.md:57, :179-180, :256, :275; docs/reference/FR_NFR.md:301 - the stated worst case is not the worst case at 32x32

- **Authority and evidence:**
  - The page's premise is "The worst case is eight channels on every stream", and it shows 65 µs "at the 32x32 load".
  - Milan v1.2 6.2 makes 1, 2, 4, 6 and 8 channels base formats. The engine contexts accept 1 to 8 (`NCH`). idleSlope is the Table 4.4 sum over the reserved streams (IEEE 802.1Q-2022 34.6.1.1), and the stagger balances stream counts, not bandwidth.
  - Take 16 streams per port at the 3,3,3,3,2,2 phase loads: one phase holds three 8-channel streams and the other 13 streams carry one channel. Then idleSlope is 131.072 Mb/s and the 8-channel frames are 15.747 µs apart.
  - The event-exact 8.6.8.2 model (`scripts/shaper_mixed.py`, `receipts/shaper_mixed.txt`) gives a 42.765 µs shaper wait. With the page's other terms the total is 83.090 µs.
  - The page's "Fewer reservations" open question and NFR-LAT-03's open-question clause cover fewer streams only. This case has all 16 reservations.
- **Impact:** the PR's key result ("Talker latency at 32x32 ... Below 65 µs") and NFR-LAT-03's derivation hold only when every stream on a port carries the same frame size. A legal 32x32 configuration misses 65 µs by about 18 µs, and the page neither shows nor lists that case.
- **Required outcome:** one of these:
  - restrict the claim, stating the equal-frame-size assumption, and add mixed channel counts to open question 1 and to NFR-LAT-03's open-question clause;
  - or change the stagger, for example balancing per-phase bits rather than counts, and re-derive the worst case over mixed formats.
- **Verification:** a re-derivation, or an executable model, over every base-format mix at 16 reservations per port, with the worst case stated.

### F5 MINOR - Conformance, Docs - docs/ARCHITECTURE_HW_SW_SPLIT.md:51, :79; docs/design/MARK_II_AREA_PLAN.md:249 - "a flexPTP-based daemon" is not the decision

- **Authority and evidence:**
  - Owner 17:04 on #640: "The gPTP software is `flexptpd`, the daemon the test machine runs. Its source and licence get confirmed before adoption."
  - No public record identifies `flexptpd` as based on flexPTP.
- **Impact:** an unconfirmed identity of the adopted software is recorded as the decision, ahead of the confirmation the owner required.
- **Required outcome:** name `flexptpd` as decided. Any lineage stays an open item until the source is confirmed.
- **Verification:** the three lines read against the 17:04 comment.

### F6 MINOR - Conformance, Docs - docs/design/MARK_II_STREAM_ENGINES.md:194-202, :239 - interference-term assumptions are unstated, and one is misattributed

- **Authority and evidence:**
  - IEEE 802.1BA-2011 6.3 sets a 2,000-octet maximum frame including headers and tags. It gives 1,522 octets only as the example for basic headers plus a C-VLAN tag. The page says "6.3 sets it at 1522 octets".
  - IEEE 802.1Q-2022 L.3.1.1 a) makes maxInterferenceTime the greater of one maximum frame and mediumAccessDelay. 802.1BA 6.1 b) 4) allows an EEE wake time of up to 30 µs.
  - The bound needs two unstated DUT egress properties: no non-class-A frame above 1,522 octets, and LPI never asserted on AVB ports.
  - With a 2,000-octet interferer, the worst order is 64.250 - 12.336 + 16.160 = 68.074 µs.
- **Impact:** the 0.75 µs margin rests on implementation properties the page attributes to a clause.
- **Required outcome:** state both properties as design assumptions, for the implementation to enforce and test, and correct the 6.3 attribution.
- **Verification:** the text of the interference term and its basis row.

### F7 MINOR - Conformance, Docs - clause citations that do not say what the text claims

The findings in this group:

- **a)** MARK_II_STREAM_ENGINES.md:173-174 says "Milan v1.2 4.3.4 ... cites IEEE 802.1Q-2022 34.6.1". Milan v1.2's [802.1Q] reference is IEEE Std 802.1Q-2014, whose 34.6.1 is "Talker behavior". The 2022 equivalent is 34.6.1.1.
- **b)** :467 cites 5.3.9.1 for `LCTX_MAP`. 5.3.9.1 is the STREAM_PORT_OUTPUT (talker) mapping. The listener mapping is 5.3.10.1.
- **c)** :49 "one to eight channels" and :433 "1 to 8 (Milan v1.2 6.2)": 6.2 allows N in {1, 2, 4, 6, 8}.
- **d)** FR_NFR.md:605, the new "Saved state" traceability row, lists 5.3.5.1, 5.3.7.1, 5.3.7.6, 5.3.8.2, 5.3.8.7, 5.3.9.1 and 5.3.13. It omits the other non-volatile clauses: 5.3.8.1 (input format), 5.3.8.3 (binding parameters), 5.3.10.1 (input mappings) and 5.3.11.1 (clock source).

Impact, outcome and check:

- **Impact:** a reader following the citations reaches the wrong clause or an incomplete saved-state set.
- **Required outcome:** each citation names the clause that says it, and the traceability row lists every saved clause.
- **Verification:** read each corrected citation against the standard.

### F8 MINOR - Conformance, RTL, Tests - docs/design/MARK_II_STREAM_ENGINES.md:414-417, :451; docs/reference/FR_NFR.md:301 - the latency instrument measures a different interval from the requirement

- **Authority and evidence:**
  - NFR-LAT-03 runs from "the last sample of a packet at the TDM pin". The page's own budget counts a pin-to-capture term of up to 18.229 µs.
  - `SE_TLAT_MAX0/1` and `TCTX_TLAT_MAX` record "capture-to-first-bit", and `SE_TLAT_OVER` counts frames at or above 65 µs on that interval.
  - The existing taps also start at the capture event (`docs/AAF_LATENCY_TAPS.md`, TX pipeline CAP). NFR-LAT-03 names those taps as the test.
- **Impact:** a frame 50 µs from capture can be about 68 µs from the pin, and `SE_TLAT_OVER` would not count it. The test named by the requirement does not cover the requirement's full interval.
- **Required outcome:** one of these:
  - the instrument measures from the pin-referenced instant, adding the slot offset of the stream's last mapped sample;
  - or the requirement and the register state exactly which interval each covers, and how the pin term is verified.
- **Verification:** the register definitions and the NFR-LAT-03 verification clause.

### F9 MINOR - RTL, Robustness, Docs - docs/design/MARK_II_STREAM_ENGINES.md:294-316, :503 - render buffer and budget sized at 48 kHz only

- **Authority and evidence:**
  - NFR-SCUP-01 makes 48, 96 and 192 kHz a configuration change. Milan v1.2 6.2 makes all three base formats, and the contexts carry `NSR` for each.
  - The 128-sample render buffer covers 2.667 ms at 48 kHz, but only 1.333 ms at 96 kHz and 0.667 ms at 192 kHz. Those are below the 2 ms default offset plus 125 µs (`receipts/arith_check.txt`), so the ledger's 1.0 tile holds at 48 kHz only.
  - At 192 kHz, 16 eight-channel streams plus a CRF need 860.672 Mb/s, 86.07 %. That is above the 75 % SR-class default, so this shape cannot be reserved (`receipts/shaper_rates.txt`).
  - The talker budget is derived at 48 kHz only. At 96 kHz it is 56.655 µs on the page's own terms, so it holds there, but the page does not state the rate assumption.
- **Impact:** a supported configuration overflows the render buffer at the default offset, and the Block RAM ledger understates it.
- **Required outcome:** state the rate assumption, and size the buffer and its ledger row for 96 and 192 kHz, or restrict the shape. Record the 192 kHz reservation limit.
- **Verification:** the buffer arithmetic per rate, and the ledger row.

### F10 MINOR - Conformance, Robustness, Docs - docs/design/MARK_II_STREAM_ENGINES.md:609-611, :584, :642 - the save worst case omits terms and a confirmed restatement

- **Authority and evidence:**
  - **Compaction page:** the page has saves preempt compaction "between two pages". A change can then wait for one compaction page already in flight, up to 5.35 ms.
  - **Second suspend:** step 6 resumes the background erase after every save. The save the change waits behind and the change's own save therefore each need an erase suspend. Table 17 also lists a typical 40 µs from erase resume to the next suspend.
  - With both terms, the worst case is 359.75 ms rather than 353.4 ms (`receipts/arith_check.txt`). It is still below 500 ms.
  - **Timeout:** the #823 direction the owner confirmed at 17:14 includes "`T-NVM-COMMIT-TIMEOUT` (8,000 ms) is restated against the new worst case". The page neither carries that restatement nor lists it as open.
- **Impact:** a figure labelled worst case is not, and a confirmed obligation is not recorded.
- **Required outcome:** T_worst includes, or explicitly bounds, the compaction page in flight and the per-save suspend. The restatement of `T-NVM-COMMIT-TIMEOUT` is assigned to #823 and F1, or listed as open.
- **Verification:** the derivation block and the open-question list.

### F11 MINOR - Conformance, RTL, Robustness, Docs - docs/design/MARK_II_STREAM_ENGINES.md:430-435, :461-466, :442, :446-450, :479-488 - register maps leave bits and counter resets undefined

- **Authority and evidence:** the page claims the technical-reference-manual style, which accounts for every bit. Two gaps:
  - **Undefined bits:**
    - `TCTX_CTRL` bits 7:5;
    - `LCTX_CTRL` bits 7:3;
    - `TCTX_PTO` bit 31.
  - **Counter resets:** the counters are access R with no reset rule. Milan v1.2 5.3.7.7 resets MEDIA_RESET, TIMESTAMP_UNCERTAIN and FRAMES_TX each time the talker starts. Milan v1.2 5.3.8.10 resets every listener counter on the transition from not bound to bound.
- **Impact:** the interface leaves the Milan-required reset behaviour and some bit positions to the implementation lane. The page presents itself as the reviewed design that lane follows.
- **Required outcome:** every bit is assigned or marked reserved. Each counter's reset event is stated, either an engine action on `RUN` or a firmware-writable clear.
- **Verification:** the bit coverage per register, and the reset column against 5.3.7.7 and 5.3.8.10.

### F12 MINOR - RTL, Docs - docs/design/MARK_II_AREA_PLAN.md:113, :158, :171 - lever 6 credited in full while part of it is kept

- **Authority and evidence:**
  - In the hierarchical report, `u_txret` (218) and `u_txticket` (32) are children of `g_gptp_plane.u_gptp_shadow` (5,194) (`receipts/build_report_digests.txt`).
  - The plan says they "stay", and it counts them as kept timestamp units for the second port (the 442 basis). It still credits lever 6 with about 5.2k.
  - The net saving is 4,944, so the central 32x32 estimate is about 21.45k.
- **Impact:** an estimate that is already above the ceiling is understated by about 0.25k, against the plan's own disposition.
- **Required outcome:** the lever-6 credit, or its note, accounts for the retained timestamp return.
- **Verification:** the plan's lever arithmetic against the hierarchical rows.

### F13 MINOR - Conformance, Docs - docs/design/MARK_II_AREA_PLAN.md:252, :263-281 - lane order departs from D16 without saying so

- **Authority and evidence:**
  - D16 (owner 16:40): levers least risky first, each measured before the next, in the order 1, 2, 3, 4, 5, 6.
  - The lane table runs lever 3 (lane 3) before lever 2, which it folds into LiteX stage 3 (lane 5). The decisions table maps D16 to "The lane order below".
  - The text explains only the deviation for lever 4.
- **Impact:** a reordering is recorded as the owner's order.
- **Required outcome:** state that lever 2 is credited through stage 3 and therefore lands after lever 3, as a reading of the 17:21 decision for the owner to confirm. Alternatively, order the lanes 1, 2, 3.
- **Verification:** the lane table and the D16 row.

## RESIDUE

These are wording only. Each changes no figure, claim or gate.

- **R1** - docs/design/MARK_II_STREAM_ENGINES.md:235. The basis "Four 50 MHz cycles (estimate)" sits beside a 0.200 µs bound, but four cycles are 0.080 µs. Exact fix: "Four 50 MHz cycles (0.080 µs), rounded up to 0.200 µs (estimate)".
- **R2** - docs/design/MARK_II_STREAM_ENGINES.md:701. "Today's 500 ms and 1,000 ms windows exceed it." The 500 ms window equals the bound. Exact fix: "Today's 500 ms window uses the whole bound; the 1,000 ms window exceeds it."
- **R3** - docs/design/MARK_II_AREA_PLAN.md heading "Mark II block RAM ledger" and its Contents label. Exact fix: "Mark II Block RAM ledger", matching the rest of the page. The anchor is unchanged.

## SUGGESTIONS (optional)

- **S1:** state why the per-stream shaper (34.6.1.1) never binds. Its spacing is 2,064 bits / 16.576 Mb/s = 124.52 µs, below 125 µs. A frame is therefore held only after a late predecessor, by at most that delay minus 0.48 µs.
- **S2:** define the listener merge when both copies carry `tu` = 1, and for an unpaired stream.
- **S3:** the FR_NFR Time row says "the PHC", while the stream-engine page has one PHC per port. Pick one wording.
- **S4:** say how the CRF stream's phase is chosen. The schedule places it in phase 2, and the worst order considers all six phases.

## What was checked, per focus item

### (1) Faithfulness to the decisions

These are stated faithfully:

- 32x32 shape;
- below 20,000 LUTs as a ceiling, as low as possible;
- processor removed, deleted at the switch-over;
- gPTP to software with timestamps kept on both ports;
- `milan_csr` for information and diagnostics;
- milan_dp content;
- talker latency target and its endpoints;
- the three LiteX stages and their criteria;
- the 0.5 s save and its append-only direction;
- lever order and figures;
- start condition.

The exceptions are F2, F3, F5 and F13.

### (2) Clauses read and confirmed

- **IEEE 802.1Q-2022:** 8.6.8.2, 34.6.1, 34.6.1.1 and 34.6.1.2. Also L.3.1.1, which applies to the single interferer.
- **IEEE 1722-2016:** 4.4.4.3, 4.4.4.6, 4.4.4.7, 4.4.4.8, 4.4.4.9, 7.5 and 7.6.
- **IEEE 1722.1-2021:** 7.2.6, via Milan Annex C.
- **IEEE 802.1AS-2020:** 8.4.3.
- **IEEE 802.1BA-2011:** 6.5.
- **Milan v1.2:**
  - 4.3.3.2 (Table 4.4) and 4.3.4;
  - 5.3.7.3, 5.3.7.6, 5.3.7.7, 5.3.8.2, 5.3.8.7, 5.3.8.10 and 5.3.9.1 (talker);
  - 6.2, used for its sample count per PDU;
  - 8.2.2 to 8.2.5 and 8.3.1 to 8.3.5.1;
  - Annex C.
- **N25Q128 datasheet:** Table 32 (tPP 5 ms, tSE 3 s, tSSE 2 s maxima), Table 17 (suspend latency typical only) and 9.1.20.

The exceptions are F6 (802.1BA 6.3) and F7.

### (3) Re-derivations

**Talker latency.**

- An event-exact 8.6.8.2 model (`scripts/shaper_schedule.py`) reproduces the page under its stated assumptions:
  - every preferred-order start time;
  - 18.333 µs (preferred order) and 23.925 µs (worst of all 90 orders);
  - totals of 58.658 µs and 64.250 µs.
- The smaller-load rows also reproduce: 62.259 µs and 83.012 µs.
- **Stated assumptions:**
  - idleSlope is the Table 4.4 sum, including one CRF;
  - a phase's frames are ready together;
  - the smaller frame goes first;
  - release at the TDM frame end;
  - one maximum interferer;
  - the estimate terms.
- **Unstated assumptions:**
  - equal frame sizes (F4, and the 8-channel premise is false);
  - a 1,522-octet own egress and no LPI (F6);
  - 48 kHz (F9);
  - the per-stream shaper never binds (S1);
  - the CRF phase choice (S4).

**Save path.**

- 5.343 ms per page and 353.4 ms reproduce. So do 187 pages/s, about 4.8 KB/s, 1.28 s compaction, 12 s erase, 168 ms boot read and about 1.55 s for 907 names (`scripts/arith_check.py`).
- **Stated assumptions:** S1, S2, the 12.5 MHz clock (matching SAVED_STATE_FASTCONNECT 9.4), T_svc = 10 ms, and a 1 ms suspend allowance flagged as unmeasured.
- **Unstated terms:** see F10.

### (4) Measured figures

- The four report digests match byte for byte. They were read in place, outside the repository.
- Every measured figure on the plan matches its report:
  - LUT, FF, slice, Block RAM, DSP;
  - route status;
  - signoff WNS +0.129 ns and WHS +0.036 ns;
  - every hierarchical row and both eight- and four-row sums;
  - the 2,036 difference row;
  - the TCAM's 494 inside `rx_filter`'s 506.
- Firmware memory, staging and the Block RAM ledger arithmetic reproduce.
- Estimates are labelled as estimates. The exception is F12's internal inconsistency.

### (5) Open questions

The pages state all five named open questions:

- partial-load latency;
- save bursts beyond 32 pages;
- Block RAM over the ceiling;
- the debounce windows (see R2);
- the gPTP daemon licence.

Not listed: mixed channel counts (F4), sample rates (F9) and the commit-timeout restatement (F10).

### (6) Requirement consistency

See F3.

### (7) Style

- **Gates that pass:** every Markdown-reading docs-workflow gate I ran passes, except the bare-metal scope gate (F1).
- **Style analyzer:** the analyzer from `check_doc_style.py` finds 0 issues in every added prose block on the five pages (`receipts/style_probe.txt`). Paragraphs are 5 to 20 words; the repository's limits are 10 words per sentence, and 20 words and 2 sentences per paragraph.
- **Paragraph length:** I found no repository authority for a 20-to-30-word paragraph range. The enforced limit is 20, so this is not a finding.
- **Characters and numbers:** added lines carry no U+2010 to U+2015 or U+2212. Decimal prose is used throughout.
- **Register maps:** they follow the technical-reference-manual layout (Offset, Name, Bits, Field, Reset, Access, Description), with the gaps in F11.

### Comment rule

No source file is in the delta, so no comment-rule RESIDUE is possible.

### Privacy

- No private host, path or device appears in the added lines.
- No test-plan name appears.
- Bench equipment is named by role.

## Gate receipts at the exact head (`receipts/gates/`, each with `.log` and `.rc`)

**rc 0:**

- `docs_check` (0 findings, 211 pages);
- `check_feature_status` and its `--self-test`;
- `check_em_dash --base e5b8405d` (0 over 1,095 added lines) and its `--selftest`;
- `check_doc_style` and its `--selftest`;
- `check_gptp_docs` and its `--selftest`;
- `DOC_MAP.gen.py --check`;
- `check_solution_docs`;
- `check_submodule_docs`;
- `gen_module_matrix.py --check`;
- `check_doc_paths` (1,075 paths);
- `check_archive`;
- `gen_toc.py --selftest`, `--verify-anchors` (563) and `--check`;
- `check_baremetal_only.py --selftest`;
- `ci_gate_workflows.py --check`.

The Markdown renderer was the pinned lock.

**rc 1:** `check_baremetal_only.py --check` (F1).

**Not run** (they refuse without submodules, which this clone does not carry):

- the code-quality ratchets and idiom gates;
- the source-list, port-contract, NVM and wire-accountability gates.

Their scan sets exclude Markdown, so a delta of five Markdown pages cannot change them. Hosted `wire-accountability`, `rtl-fast`, `elaborate` and `docs-check-no-git` succeeded at this head.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F2, F3, F4, F5, F6, F7, F8, F10, F11, F13) | FR_NFR.md NFR-RES-01, NFR-LAT-03, NFR-REL-03, NFR-SCOUT-02/03/05 and the traceability rows; REQUIREMENTS.md section 1; the split page sections 1, 3 to 7; every clause cited on the stream-engine page, read in the standards; the #640, #665, #823 and #234 decisions | R757-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| RTL | UNCLEAN (F4, F8, F9, F11, F12) | MARK_II_STREAM_ENGINES.md engines, throughput, capture and render buffers, stagger, shaper schedule, per-port units, register maps and Block RAM ledger; MARK_II_AREA_PLAN.md basis rows and lever arithmetic against the hierarchical report | R757-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Robustness | UNCLEAN (F4, F9, F10, F11) | mixed-format, sample-rate and smaller-load shaper cases; the save sequence with suspend, compaction preemption and bursts; counter reset events; render-buffer overflow | R757-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Tests | UNCLEAN (F1, F8) | docs-workflow gates run at the head (`receipts/gates/`); hosted check runs at the head; the NFR-LAT-03 and NFR-REL-03 verification methods; the stream-engine verification table; the AAF tap definition | R757-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |
| Docs | UNCLEAN (F1, F2, F3, F4, F5, F6, F7, F9, F10, F11, F12, F13) | all five touched pages; style probe; em-dash, TOC, anchor, path and bare-metal gates; the PR body's evidence claims | R757-1 | dfc310fb3dec28f3d06333973e61cde44a4e786d |

## Real limits

- I re-derived the shaper results with my own event-exact model. The author's byte-resolution model was not run.
- I did not initialise submodules, so the code-only gates were not run (see above).
- I read the build reports in place on the workstation that holds them. Their location is not published, and nothing about how they were built was re-run.
- No hardware, bench, act, hosted re-run or builder bank was used. Physical calibration was not run, and field skips are not hardware proof.
- This round claims no manager source bank, and none was run at this head.

## Pending manager duties

- Hosted `docs-check` is red at this head (F1). A new head needs the full docs workflow executed.
- `verilator-suites` and `yosys-portability` were skipped contexts at this head. That is consistent with a documentation-only delta, and the manager owns their acceptance.
- Validate the current-dev merge candidate (source base and live dev both `e5b8405d`) with the builder and native banks at the merge turn.
- Owner approval of the requirement text is still required, as the PR states.
- Carry R1 to R3 to the residue checklist.
- No source-head execution evidence exists beyond the author's published receipts and the receipts here.

R757-1 FINISHED

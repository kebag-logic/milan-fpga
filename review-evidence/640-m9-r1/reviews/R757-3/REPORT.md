[R757] NEGATIVE - exact head 69fd18f1d8f9d428687c07ede0f9c14597cf2d61

# R757-3: internal cleared-context review of PR #828 (issue #640), round 3

- Head: `69fd18f1d8f9d428687c07ede0f9c14597cf2d61`, tree `f7c3f02d8889081b89c7dcb46004d3ffb88623e2`.
- Round-3 delta: `f6b3e841..69fd18f1`. Eight commits on four Markdown pages, 317 lines added and 85 removed. Against base `e5b8405d` the PR adds 1,658 lines and removes 112 over seven pages.
- The delta has no code, generator, gate, configuration or gitlink. All modes are 100644. This is a documentation-only round.
- **Reconstructed from:**
  - AGENTS.md and CONTRIBUTING.md, and docs/README.md;
  - the #640 body and the 2026-10-31 owner comments (the 17:04 `flexptpd` and 65 µs decision re-read word for word), plus the 2026-11-01 core survey;
  - my own R757-2 report, read first;
  - the round-3 diff and its eight commits;
  - the author's round-3 packet `review-evidence/640-m9-r1/author-r3` at `1a5f9f3a` (HANDOFF.md, PR-BODY.md, models, gate receipts);
  - the A720c REVIEW READY comment on #640 and the review-start comment on #828.
- **Taken as given:** the owner decisions of 2026-10-31 are final and are not reviewed.
- **Order of reading:** I read the other reviewer's round-2 findings only after the verdict, findings and ledger below were written. The section "Prior external findings" records that later pass.

## Verdict

NEGATIVE. Two MINOR findings are open, and round 3 introduced both. No BLOCKER or MAJOR is open.

- **Closed:** every R757-2 finding (N1, N2, N3), both residue items (RR1, RR2) and all five suggestions are closed at their cause (table below).
- **Gates:** I re-ran 23 docs-gate commands at this head; every one exits 0. The author's full docs-workflow receipts at this head exit 0, and their digests verify.
- **Models:** all four author models reproduce their published output line for line, and every stated mutant fails as claimed.
- **Probes:** two probes of my own found the two open findings.

The open findings:

- **N4:** a header that fails its read-back can still be valid, and then boot picks the slot that lacks the saves made afterwards.
- **N5:** the 2.210 µs conversion-error bound leaves out the offset drift between stamping and arrival. The corrected bound is about 2.6 to 2.7 µs. The merge window still holds, but the figure and its bench limit are wrong.

## Findings

### N4 MINOR - Conformance, Robustness, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:1038, :1041-1046, :1114; docs/reference/FR_NFR.md:476 (NFR-REL-03) - a failed header read-back leaves a valid higher-generation header behind

- **Authority and evidence:**
  - NFR-REL-03 (FR:476) says compaction "loses no saved change, with or without a power cut".
  - Round 3 added the save-landing row "After a header that fails its read-back | The old slot, still active | Compaction erases the standby and restarts from step 1" (SE:1038).
  - **What a failed read-back means:** a read-back compares what was programmed with what was meant. It can fail while the programmed header is intact, for example after a transient error on the read path. Then the header sits in flash with its own valid check and a higher generation (SE:1022).
  - **The failing sequence:**
    1. The header page programs correctly, but its read-back reports a mismatch.
    2. As the row says, the old slot stays active and a save appends there. That save becomes durable and is acknowledged.
    3. A power cut lands before the erase of the standby has removed its header. That erase takes up to 12 s (SE:997).
    4. Boot takes the valid header with the highest generation (SE:1022-1023), which is the new slot. The save from step 2 is not in it.
  - **Probe:** `scripts/probe_header_readback.py` drives this sequence with the author's unchanged host flash model (`receipts/probe_header_readback.txt`, rc 0). As written, boot uses slot 1 and loses the acknowledged value of key 9. In a control arm the header page is overwritten with zeros before any save appends to the old slot (a NOR program can clear bits without an erase). In that arm boot uses slot 0 and nothing is lost.
  - **Gaps elsewhere:**
    - The power-cut table (SE:1041-1046) has no row for a cut after a failed header read-back.
    - The host flash model and the verification row (SE:1114) never fail a read-back, so neither can detect this.
- **Impact:**
  - Under a power cut in a window of up to about 12 s, a saved change is lost after a read-back fault. That breaks the MUST of NFR-REL-03.
  - The same row also claims to say where the save survives.
  - A firmware lane that follows the row as written ships this window.
- **Required outcome:**
  - After a failed header read-back, no save may append to the old slot while the standby's header could still pass its check. Making the header invalid first is one way to do this, as in the probe control.
  - Any extra page this adds is accounted for. It is a reported fault outside the bound, like the page retry at SE:932-933. Even a second page wait would give 365.10 ms, under 500 ms.
  - The power-cut table gains the row for a cut after a failed header read-back.
  - The verification row and NFR-REL-03 name a failed header read-back with an intact header, followed by a save and a cut.
- **Verification:**
  - Read SE:1030-1046 and SE:1114.
  - Run the host flash model with a read-back failure on an intact header, then a save and a power cut before the standby erase. No acknowledged value may be lost, and the model must fail when the invalidation step (or its equivalent) is removed.

### N5 MINOR - Conformance, Tests, Docs - docs/design/MARK_II_STREAM_ENGINES.md:541-555, :582, :1109-1110 - the conversion-error bound counts the offset drift over the latch age only, not over the time from stamping to arrival

- **Authority and evidence:**
  - **The two conversions:**
    - The talker adds its latched PHC offset when it stamps the odd copy (SE:515-522).
    - The listener subtracts its own latched offset when the copy arrives (SE:524-527).
  - **Why the instants matter:** the offset PHC1 - PHC0 drifts at the frequency difference of the two grandmasters. That difference is at most 200 ppm (IEEE 802.1AS-2020 B.1.1, 100 ppm each). So the error between the two applied offsets includes the drift between the instants at which they were latched.
  - **What the page counts:** the latch age alone, "Each offset is up to 125 µs old ... So an offset drifts at most 25 ns per latch", that is 2 x 125 µs x 200 ppm = 0.050 µs (SE:541-552).
  - **What it leaves out:** the talker's latch precedes stamping, and the listener's latch precedes arrival. Arrival comes up to one class A transit (2 ms) plus the talker latency after stamping. A copy that arrives later than its presentation time is late by rule 1, so its offsets are latched about 2.2 ms apart at the most.
  - **The arithmetic** (`scripts/probe_conversion_error.py`, `receipts/probe_conversion_error.txt`):
    - With 2.1 ms from stamp to arrival, the drift term is 200 ppm x 2.225 ms = 0.445 µs. E_x = 2.000 + 0.445 + 0.160 = 2.605 µs.
    - With the 2.667 ms render span taken as the separation, E_x = 2.718 µs.
    - Either way it is above the stated 2.210 µs.
  - **Effect on the merge:** none on the window. The author's merge model, unchanged except for its injected error, passes all 15 cases at ±2.210, ±2.715 and ±10 µs. So the 62.5 µs window, the placement by count and the rule verdicts all stand.
  - **What is wrong:**
    - The stated figure, repeated at SE:582 ("Clean partner copies differ by at most 2.210 µs") and in the PR body.
    - The bench limit in the verification row, "the converted times differ by at most 2.210 µs" (SE:1110). A compliant pair of networks can exceed that limit.
    - The model injects ±E_x uniformly instead of deriving it, so it cannot catch this.
- **Impact:** a derived figure tied to 802.1AS clauses is understated. A bench test written to SE:1110 can fail on a compliant installation, or it gets loosened without a stated reason. This changes a figure and a test limit, so it is not wording only.
- **Required outcome:**
  - The drift term covers the interval between the talker's latch and the listener's latch, bounded by the stamp-to-arrival time and the latch period.
  - E_x is restated, and SE:582, SE:1109-1110 and the PR body carry the new figure.
  - The window argument at SE:584-587 is re-checked against it. It still holds with a wide margin.
- **Verification:** re-derive the E_x block. Then check that the bench limit in the conversion-error row equals the restated bound. The neighbour-separation argument must still exceed it.

## RESIDUE (wording only; each changes no figure, verdict, test or gate)

- **RR3** - SE:1045. The power-cut row "The header page, step 4 | The old slot" is exact only for a cut before the header has programmed whole. A cut during its read-back boots the new slot, which also holds every durable save, so nothing is lost either way.
  - Exact fix: "| The header page, step 4 | The old slot, or the new slot if its header programmed whole | A torn header fails its check; either slot holds every durable save, and a save waiting on the header was not yet durable |".
- **RR4** - SE:1109. "`SE_MERGE_DUP` counts each packet's second copy once" also covers the tu cases in the same row. There the second copy is discarded by rule 2 and counted in `SE_MERGE_TU` (SE:735), as the model expects (`tu_drop` 3,900).
  - Exact fix: "`SE_MERGE_DUP` counts each packet's second copy once, or `SE_MERGE_TU` when rule 2 discards it".

## SUGGESTIONS (optional)

- **S1:** every TDM frame end is now stamped on both PHCs on one edge (SE:415-416). The talker could take the odd copy's avtp_timestamp straight from the port 1 stamp, with no talker-side offset at all. That removes one sync term and one latch from E_x (SE:515-522, :550-555).
- **S2:** a model that derives the conversion error would make the bench limit checkable. It would drift two PHCs at grandmaster offsets of up to ±100 ppm, latch them every 125 µs, and stamp and convert at their own instants.
- **S3:** the save-landing table could add the row "a save that arrives while a save is in flight during compaction". It is implied by "a pending save always runs before the next compaction page" (SE:1004), but it is the case S1 and T_svc both reach.

## Round-2 findings (R757-2) at this head

| Item | Closed by | Evidence at this head |
|---|---|---|
| N1 MINOR, save between the last replay and the header | `4e14b331` | Saves have strict priority at every page boundary (SE:1003-1004). Step 4's check and the header page are one step that no save can split (SE:1016-1017). A save arriving during the header waits inside the compaction-page term (SE:1019-1020), so T_worst stays 359.75 ms (re-derived, `receipts/arith_check_r3.txt`). The landing table (SE:1030-1039) puts the boundary after the last replay page before the check. The verification row (SE:1114) and NFR-REL-03 (FR:476) name that interleaving. The host model reproduces 14,831 runs with 0 lost; the `split` mutant loses 733, the first with no cut, which is my round-2 sequence; `no_replay` loses 2,704 (`receipts/model/compaction_model.txt`). **Closed**. N4 is a new defect in a row added by the same commit |
| N2 MINOR, exact time compare across two time bases | `07f8eb91`, `69fd18f1` | A clean copy is placed at k = round((t - head) / 125 µs), with a 62.5 µs window (SE:578-587). The bound is stated (SE:530-558) and assumption A3 is named. A tu copy is placed by sequence_num (SE:589-601), and samples are placed by count (SE:603-609). The rules table (SE:611-623) and reference upkeep (SE:640-652) are complete. The register rows (SE:733-735, :806-827) pass `regmap_check.py` (`receipts/regmap_check.txt`). The verification row runs a jittered error, and its test fails with an exact compare. The model reproduces 15 PASS; `exact` fails 15, `own_time` fails 3 and `no_rule2` fails 5 (`receipts/model/merge_model.txt`). **Closed**. N5 is a new defect in the bound's derivation |
| N3 MINOR, the 16-reservation condition | `05f3e85e` | SE:19, SE:379-382, AP:60, AP:255 and FR:306 each carry "at 16 reservations" and link the fewer-reservations results. My grep of all seven touched pages finds no other one-format "met" line. The results-table rows sit under "Results at 16 reservations per port" (SE:342). **Closed** |
| RR1, PR body open questions | PR body | "(open questions 1 and 7)" at PR body line 198. **Closed** |
| RR2, "only valid copy" | `f11e1eca` | SE:628. **Closed** |
| S1, fewer-reservations totals | `05f3e85e` | SE:395-402: 102.584, 123.337, 81.750 and 40.325 µs, all re-derived. **Taken** |
| S2, packetizer term for mixed formats | `45c27020` | SE:309-334. Re-derived: 2 x (6,192 x 64 / 2,064 + 22) x 20 ns = 8.560 µs, and 2 x (7,200 x 112 / 3,600 + 22) x 20 ns = 9.840 µs. The counting argument (19 > 17, 25 > 17) holds. **Taken** |
| S3, replay passes bounded | `4e14b331` | SE:1064-1091. S2 read as a token bucket: done by 382.5 p = 2.046 s, A <= 70.25, so the work is 311 pages. The next trigger comes at 15.46 s or later, with 13.42 s of flash free for the 12 s erase. All re-derived. **Taken** |
| S4, flexPTP pin under final decisions | `6f1e03ae` | See focus item 7. **Taken** |
| S5, t_page | `f11e1eca` | SE:957 "5.344 ms, used as 5.35 ms"; 5.3438 ms re-derived. **Taken** |

## What was checked, per focus item

1. **Round-2 findings:** see the table above.
2. **Compaction:**
   - **One step:** the last replay check and the header page are one step (SE:1016-1017). The model's `split` mutant reopens exactly that window and loses changes.
   - **Landing and power-cut tables:** each row of the landing table was checked against the ordering. Every row holds except SE:1038 (N4). Each power-cut row holds, with RR3 as wording.
   - **T_worst with a save waiting on the header page:** the header page is the compaction page already counted, so T_worst = 10 + 5.35 + 2 + 2 x 32 x 5.35 = 359.75 ms. As in round 2, the sum over-counts, because a change cannot both wait for the header page and arrive just after a save started.
   - **Model:** run, with both mutants (`receipts/model/compaction_model.*`). Output equals the published `compaction_model.out` line for line.
3. **Listener merge:**
   - **Clauses:** B.3 (1 µs over seven hops), B.1.1 (100 ppm) and B.1.2 (40 ns granule) are applied as the page says. My derivation of the drift term differs (N5).
   - **Window:** 62.5 µs is half the 125 µs interval. It holds against the corrected error with a margin of about 60 µs, and neighbours stay 125 µs - 0.55 µs - E_x apart.
   - **tu copies:** rule 2 sits before every writing rule and tests the partner's clean data where it reads it. So a tu copy never writes while clean partner data remains, and `no_rule2` fails the five tu cases.
   - **Duplicates:** rule 7 and the 22-bit map count each duplicate once, and the model gives DUP = 4,000 of 4,000 with both copies clean.
   - **Wrap:** the sweep covers 32 contexts at one per 31.25 ms, so every context is visited each second. A stale time trails the render point by under 1.03 s, well inside the 2.147 s half range.
   - **Model:** run, with its three mutants (`receipts/model/merge_model.*`). Output identical.
4. **192 kHz:**
   - **Engine load:** `load_any.py` gives 93.18 % (14 eight-channel streams, no CRF, 748.160 Mb/s) and 92.67 % at 16 reservations. I re-derived both by hand.
   - **Placement search:** `p192.py` reached 1,245,183 states, 34 of them with 16 AAF streams, exactly ranks 0..16 minus one. One format gives 34.861 µs (N = 6). Mixed formats reach 84.319 µs and are bounded at 100.825 µs. The run took 2 min 44 s at 165 MB, and its output equals `p192.out` line for line (`receipts/model/p192.*`). The page records the mixed case as not met (SE:354, open question 1).
5. **The 16-reservation condition:** see N3 above.
6. **Latency taps:**
   - Each TDM frame end is stamped on both PHCs on one edge, and each copy is measured in its own port's PHC (SE:415-430).
   - The registers name the time base: `SE_TLAT_MAX0/1`, `SE_TLAT_OVER` COUNT0 and COUNT1, and `TCTX_TLAT_MAX` (SE:728-731, :778).
   - The verification row runs an odd context with a drifting PHC offset (SE:1106).
7. **flexPTP:**
   - **The decision:** under "These decisions are final", the split page now says only `flexptpd`, with "Its source and licence get confirmed before adoption". That is the owner's 17:04 wording (SP:79-80).
   - **The proposal:** the source, the licence and branch `gptp` at `d116d3d` are the survey's proposal, "not an owner decision" (SP:93-101).
   - **The open question:** one instance per port is an open owner question, recorded at SP:51, SP:101, SE open question 5, AP D13 and lane 9, and AP open decision 3 (AP:308-314).
   - **Grep:** "adopted revision" or "adopted fork" has no hit on the touched pages.
8. **Docs workflow:**
   - **My runs:** 23 commands in a pinned-renderer venv (cmarkgfm 2025.10.22, html5lib 1.1, PyYAML), all rc 0 (`receipts/gates/`):
     - `docs_check.py`, with 0 findings over 211 pages;
     - `check_em_dash.py --base e5b8405d`, with 0 findings over 1,658 added lines in 7 pages, and its `--selftest`;
     - `check_doc_style.py` and its `--selftest`;
     - `check_gptp_docs.py` and its `--selftest`;
     - `DOC_MAP.gen.py --check` and `--selftest`, and `timesync_chain.gen.py --check`;
     - `check_solution_docs.py` and `check_submodule_docs.py`;
     - `check_feature_status.py --self-test` and `gen_module_matrix.py --check`;
     - `check_doc_paths.py`, where 1,075 paths resolve;
     - `check_archive.py` and its `--selftest`;
     - `gen_toc.py --selftest`, `--verify-anchors` (569 links) and `--check`;
     - `check_baremetal_only.py --check` (0 findings over 1,425 files) and `--selftest` (867 arms);
     - `git diff --check e5b8405d HEAD`.
   - **Style probe:** `check_doc_style` `analyze()` over every round-3 prose block finds 0 issues, and paragraphs run 5 to 20 words (`receipts/style_probe.txt`).
   - **Author receipts:** `author-r3/evidence/gates` records rc 0 for every docs.yml step at this head. That includes both builder legs, the RV32 SDK, CI events and the act-runner contract. A first attempt at `6f1e03ae` failed for environment reasons (SDK provenance and the submodule origin) and is published beside the final run. I did not re-run the submodule, SDK or builder steps, and the delta has no file they scan.

### Comment rule and privacy

- **Comment rule:** no source file is in the delta, so no new instance of the comment rule is possible.
- **Privacy:** the added lines have no private path, host or device. A grep for lane, round and reviewer labels on the added lines finds none.

### Evidence integrity

- **Manifest:** `MANIFEST.json` at `1a5f9f3a` lists 129 `author-r3` files. All 129 match their published digests, with none missing and none unlisted (`receipts/evidence_integrity.txt`).
- **SHA256SUMS:** 113 entries verify. The 13 that do not are exactly the path-redacted files, which the manifest flags as such.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (N4, N5) | NFR-REL-03 (FR:476) and NFR-LAT-03 (FR:306); SE:530-558 against IEEE 802.1AS-2020 B.1.1, B.1.2 and B.3; SE:589-601 against IEEE 1722-2016 4.4.4.6 and 4.4.4.7; SE:611-623 against Milan v1.2 4.4.2.2 and 5.3.8.10; SE:1003-1046 against NFR-REL-03; SP:76-101 and AP:254, :279 and :308-314 against the owner's 17:04 decision text | R757-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| RTL | CLEAN | SE:132-145 engine load (`load_any.py` re-run, 93.18 % and 92.67 % by hand); SE:309-334 packetizer bound (re-derived); SE:342-377 192 kHz placements (`p192.py` re-run, identical); SE:410-436 latency instrument time base; SE:560-660 merge state, placement, rules and wrap sweep (32 contexts x 31.25 ms = 1 s); SE:710-828 register maps (`regmap_check.py` PASS, `receipts/regmap_check.txt`); N5 changes no datapath (`receipts/probe_conversion_error.txt`: 15 of 15 at ±10 µs) | R757-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Robustness | UNCLEAN (N4) | compaction landing and power-cut tables SE:1030-1049 (`receipts/probe_header_readback.txt`); replay bound under S1 and S2 SE:1064-1091 (`receipts/arith_check_r3.txt`); merge under loss, cut, tu skew, startup tu and double fault SE:637-660 (`receipts/model/merge_model.txt`); stale and wrapping times SE:645-652 | R757-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Tests | UNCLEAN (N4, N5) | four author models re-run with all mutants (`receipts/model/`); verification rows SE:1104-1114; NFR-REL-03 and NFR-LAT-03 verification clauses; 23 docs gates re-run (`receipts/gates/`); author gate receipts and digests (`receipts/evidence_integrity.txt`); hosted check runs at the head (`receipts/hosted_checks.tsv`) | R757-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |
| Docs | UNCLEAN (N4, N5) | the four round-3 pages (SE, AP, FR, SP); the style probe; the em dash, TOC, anchor, path and bare-metal gates; the PR body (round-3 table, known limitations); RR3, RR4 | R757-3 | 69fd18f1d8f9d428687c07ede0f9c14597cf2d61 |

## Prior external findings (R758-2), read after the verdict and ledger

Written after the verdict, findings and ledger above. Each R758-2 item (issuecomment-6553064958) is resolved or retained at this head as follows.

| R758-2 item | At this head |
|---|---|
| F1 MINOR, 192 kHz engine load | **Resolved:** SE:136 gives 93.18 % (14 eight-channel streams, no CRF, 748.160 Mb/s), and SE:138-142 gives 92.67 % at 16 reservations. Open question 7 follows (SE:1149-1152). `load_any.py` reproduces both |
| F2 MINOR, 192 kHz placements | **Resolved:** all reachable placements are searched (SE:353-354, :362-377). The count is 34, not 35: "no CRF ever" is the same occupancy as "CRF stopped at rank 16". `p192.py` confirms this by a search of every start and stop (1,245,183 states, exactly 34 with 16 AAF streams). One format gives 34.861 µs and the mixed shaper wait is 57.905 µs, equal to the R758-2 probe figures. No touched page still carries 32.071, 54.822, 72.915 or "Exact occupancy" |
| F3 MINOR, compaction window | **Resolved:** as R757-2 N1 above. **New in the same area:** N4 (header read-back failure) |
| F4 MINOR, tu copy beside a valid partner | **Resolved:**<br>- A tu copy is matched by sequence_num (SE:589-601).<br>- Rule 2 discards it while the partner holds clean data (SE:618).<br>- Placement is by count (SE:603-609), so no tu copy moves the head past, or writes outside, the clean copy's span.<br>- The model's skew cases (±30 and ±200 µs, +1 ms, tu copy first) pass, and `no_rule2` fails them.<br>**New in the same area:** N5 (the derivation of the conversion bound) |
| F5 MINOR, latency instrument time base | **Resolved:** SE:415-430 and the register rows SE:728-731 and :778. The verification row is SE:1106 |
| F6 MINOR, flexPTP revision as decided | **Resolved:** as focus item 7. "adopted fork" and "adopted revision" no longer appear on the touched pages |
| R1 RESIDUE, counter rule | **Resolved:** SE:704 "Every Milan counter is 32 bits and wraps to zero." |
| S1 to S3 | **Taken:** S1 t_page 5.344 ms (SE:957); S2 "about 114 µs" (SE:171, re-derived 114.31 µs); S3 the totals column (SE:395-402) |
| S4 | **Not taken, with a stated reason.** The handoff says it would add requirement text needing owner approval, and that NFR-SCOUT-03 carries the obligation. It is optional, so nothing is retained |

There are no PR line comments or review objects on #828. The only prior public findings are the R757 and R758 round reports.

## Real limits

- **Not re-run:** the submodule-dependent docs-workflow steps (HDL reference, RV32 SDK, builder legs, code ratchets, NVM, CI events, act contract). The author's published receipts at this head are the source-head evidence for them.
- **Hosted runs:** at 06:35 UTC, `docs-gates-0` and `docs-gates-2` were still in progress at this head. `docs-gates-1`, `docs-check-no-git`, `wire-accountability`, `rtl-fast`, `elaborate`, `bdd-conformance` and `full-ci-gate` had succeeded. 22 contexts were skipped, consistent with a documentation-only delta (`receipts/hosted_checks.tsv`).
- **Standards:** the 802.1AS-2020 clause texts were applied as the page quotes them (B.1.1 100 ppm, B.1.2 40 ns, B.3 1 µs over seven hops). N5 rests on the design's own two-latch description, not on a different reading of the clauses.
- **Not used:** hardware, bench, act, a hosted re-run and the builder bank. Physical calibration was not run, and field skips are not hardware proof.
- **Manager bank:** no manager source bank ran at this head, and this round claims none.
- **Clone state:** the clone equals HEAD. The index tree is `f7c3f02d`, the mode, blob and path listings are identical, the worktree is clean, and the six gitlinks are unchanged. One ignored `scripts/__pycache__/`, created by this round's gate runs, was removed (`receipts/clone_integrity.txt`).

## Pending manager duties

- Accept the hosted `docs-check` at this head, once `docs-gates-0` and `docs-gates-2` complete with all three legs executed.
- Accept `verilator-suites` and `yosys-portability` as skipped contexts for a documentation-only head.
- Validate the current-dev merge candidate at the merge turn, with the builder and native banks. The source base is `e5b8405d`; live dev is `1f29f189`.
- Get owner approval of the requirement text, and of open decisions 1 to 3 in the area plan.
- Carry RR3 and RR4 to the residue checklist.

R757-3 FINISHED

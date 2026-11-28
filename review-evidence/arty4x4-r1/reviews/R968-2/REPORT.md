[R968] POSITIVE - exact head 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e

Round R968-2, external independent re-review of PR #1026 (draft, base `dev-soft-core`, stacked on PR #1004) against its task contract, issue #1027.
Tree `998ce7dd057cc9947b3db4bbdf3dd6f20acf75ef`. Narrow delta reviewed: `12ab4b189f54439cd126f677b906a19835d7f32a..47f2a3d7ffdf7ef701c69267a91ac92892a1c99e`, seven commits, 16 files, +349/-105. The whole PR is `c0b625d1792e61b8e99944daea65b842e6b9dcde..47f2a3d7`, 28 files, +940/-163.
Reconstructed from AGENTS.md, CONTRIBUTING.md, #1027 (its body; it has no comments), the delta and its history, and the author's packet at evidence commit `117bd43f1cb642326123e7d426cc8f34174043f6` (`review-evidence/arty4x4-r1/author-r5`). The two round-1 reports were read only after an independent pass over the delta and a first run of probes. The concurrent internal round's report at this head was read only after this verdict and ledger were written; its items are resolved or retained in their own section.

## Summary

Every finding of round 1, the external report's F1 to F5 and the internal report's F1 to F3, is closed at its stated outcome. No BLOCKER, MAJOR or MINOR is open at this head. Three wording items are recorded as RESIDUE and nine optional SUGGESTIONS are listed, and two residue items of the concurrent internal round are retained, so the author can take them all in one pass.

Checked by execution here, not taken from the author:
- The four self-tests pass at the head, and their output is byte-identical to the author's receipts (`egress_mii` 35 of 35, `record_classes` 26 controls and 26 Arty checks, `egress_ledger` 26 mutants, `egress_fixed` 3 mutants).
- The published census-4 extract regrades to 446.760 us and 527.042 us over 159 cases, and to 1655 ledger instances, PASS. The 159 grades equal the packet's full-log grades as a multiset: the packet's two grade files key a line by case name without its variant.
- The fixed-path bench, run as its usage line states with Verilator 5.050, reports 300.0 ns at 100000000 Hz (exit 0) and 312.5 ns at the default (PASS).
- 24 reviewer mutants were planted in disposable copies. All eight mutants the round-1 reports named are caught by an in-tree self-test. Seven mutants fail nothing; none of them is a defect at this head, and each is explained below.
- The packet's 827 files match its manifest, and 822 index rows and 218 archive-mapping rows resolve to files with their stated hashes.
- The 4x4 builder outputs are identical with and without the delta's configuration header edit, and the generated shape include equals the tracked one.

Not covered by this verdict: #1027's last acceptance item, the bench session, is NOT MET, and no source head can meet it. No hosted run exists for this head. See Limits and Pending manager duties.

## Prior findings, each at its cause

| Prior finding | Stated outcome | Result at `47f2a3d7` | Evidence |
|---|---|---|---|
| R968-1 F1 (Tests): the CRF output's frame in the 100 Mb/s stream load has no control | A control at a shape with a CRF output that fails when the frame is absent or has another length; M1 caught in-tree | CLOSED | `egress_mii.py:74-77,640-656` hold each point's sources to a hand-stated load and every frame of it on the wire. M1 (`crf = ()`), `return aaf`, a 27-octet and a zero-length AVTPDU each fail `--selftest` at `[arty-4x4]` (`receipts/mutants/M1-*.log`, `A1-*.log`, `A2-*.log`, `M1b-*.log`). The clean tree passes 35 of 35. |
| R968-1 F2 (Tests): the record-class gate's arty-4x4 branches have no control | A 4x4 leg off 100 MHz refused, the configuration named to its own point, its own cost read at (1,5,5); M8, M9, M10 caught | CLOSED | `record_classes.py:462-551`. M8 (B2), M9 (B6) and M10 (B1) each fail `--selftest`. So do the 4x4 dropped from `REBOOT_PATH_POINTS` (B3) and from `COMPLETE` (B4), and a 4x4 clock never checked (B8). |
| R968-1 F3 (Tests, Docs): the fixed-path bench does not run as its usage line states; SYS_HZ untested | The documented invocation runs; the SYS_HZ report path is exercised by a test | CLOSED | `python3 -I tb/verilator/ctrl_service_budget/egress_fixed.py DIR 100000000` exits 0 reporting 300.0 ns (`receipts/head-egress_fixed-100.log`). `--selftest` holds the argument, the period passed to the build and the report's verdict; a fixed build flag (D1) and a missing whole-ps check (D3) fail it. |
| R968-1 F4 (Docs, Conformance): scope and decisions not public | Scope, acceptance and the applied decisions published, with a link to the packet | CLOSED; one pointer carried as residue Q1 | #1027 states the scope, eight acceptance items and decisions 1 to 5. The PR body links it and says which decision each claim rests on, and section 15 cites them (`SPLIT_CONTROL_MEMORY.md:3634-3640,3684-3687`). The packet is public, but the PR body and #1027 do not link it (Q1). |
| R968-1 F5 (Docs): the packet omits the receipts its indexes name | The named receipts or regradeable extracts public; each index entry resolves; 446.76 us reproduced from a published receipt | CLOSED | The 123 compressed receipts are published as text: 218 mapping rows resolve (`receipts/packet-index-verify.txt`). Among them are 45 route and utilization reports (ExtraPostPlacementOpt: Slow WNS +0.049 / WHS +0.156, Fast +1.606 / +0.012 ns, 0 failing endpoints). The census-4 extract regrades here to 446.760 us (`receipts/extract-egress-regrade.log`). |
| R967-1 F1 (Conformance, Docs): no public task contract; rulings (a) to (f) | Each decision reachable by link from the PR body | CLOSED | (a) #1027 Task and Acceptance; (b) decision 1; (c) decision 2; (d) decision 3; (e) decision 4; (f) decision 5. |
| R967-1 F2 (Tests, Robustness): CRF term and 4x4 egress parameters unchecked; `--packet` pinned to the 1x1 | Both mutants caught; `--packet` and `--structural` take the point or refuse | CLOSED | `return aaf` and `CRF_AVTPDU = 0` are caught (A1, M1b). Both options take `--point` (`egress_mii.py:708-725`), and a named control refuses a log of the other point's queue in both directions. |
| R967-1 F3 (Docs, Tests): compressed receipts unpublished | Every receipt row resolves to a published file with its hash | CLOSED | As F5 above. |
| R968-1 R1 to R4, R967-1 R1 to R4 (residue) | Exact wording fixes | APPLIED | `egress_ledger.py:101-103` (no comment ID); `shape_costs.py:57-58`; `record_classes.py:99-100`; `selftest_share.py:170-171`; `test_builder.py:23900-23902`; `ENDSTATION_BUILDER.md:25,28`; `BUILDING.md:361`; the harness README's queue bullet; the PR body ("the stated 320 ns fixed path (300.0 ns measured at 100 MHz)"). |
| R968-1 S1, S2; R967-1 S1 to S4 (suggestions) | Optional | TAKEN | SYS_HZ is validated. Section 15 is "Arty split points", with its three inbound links updated. The clock mutants are caught. Section 15 tabulates the stated costs, all twelve equal to `ctrl_loop.h:416-427`, and names the two qualifying rows, which the published `author/round3/receipts/derive-merged234-969.json` confirms (125/5/1250 and 130/5/1000, the first installed). |
| R968-1 S3; R967-1 S5 | Optional | NOT TAKEN, and stated as such | The README still links no published 4x4 qualification (S9). #1022's body is unchanged; a comment there (issuecomment-7241723121) names the 4x4's owed records and the packet. |

## Findings at this head

No BLOCKER, MAJOR or MINOR.

### Residue

Wording only. Each changes no measurement, figure, verdict, test outcome, code path or clause claim.

- **Q1. RESIDUE. Docs.** Artifact: PR #1026 body; issue #1027.
  Evidence: AGENTS.md section 6, Docs ("enough evidence for another cold reviewer"); round 1's F4(d) and F5 asked for a link to the packet. Checked at 2026-11-28T16:32Z: the PR body and #1027 name `EXTRACT/*/` and "the census-4 extract" but link no evidence commit. The packet is public at `117bd43f` on branch `arty4x4-review-evidence`, and #1022's comment 7241723121, cross-referenced on #1027's timeline, names it.
  Impact: a reader starting from the PR body reaches the receipts only through another issue.
  Exact fix: add to the PR body, under "Regradeable evidence": `Evidence packet: https://github.com/kebag-logic/milan-fpga/tree/117bd43f1cb642326123e7d426cc8f34174043f6/review-evidence/arty4x4-r1/author-r5 (EXTRACT is receipts/census4-extract).`
  Verification: the link opens the packet, and `receipts/INDEX.md` is under it.
- **Q2. RESIDUE. Docs.** Artifact: PR #1026 body, "Stacked on #1004".
  Evidence: "this PR's own change is 28 files in 21 commits". `c0b625d1..47f2a3d7` is 28 files in 22 commits, 24 with its two merges of #1004's branch.
  Impact: none on any figure.
  Exact fix: `28 files in 22 commits (24 with its two merges of #1004's branch)`.
  Verification: `git rev-list --count --no-merges c0b625d1..47f2a3d7` prints 22.
- **Q3. RESIDUE. Tests, Docs.** Artifact: `tb/verilator/ctrl_service_budget/egress_mii.py:645` (a check label).
  Evidence: the label prints `[arty-1x1] arty-1x1: the stream load is its talkers' frames and its CRF output's, (90,)`. The 1x1 has no CRF output. The check itself is right at both points.
  Impact: a reader of the 1x1 line may take (90,) to include a CRF frame.
  Exact fix: `f"{point}: the stream load is its stated frames, its CRF output's among them where it has one, {STREAM_LOAD[point]}"`.
  Verification: `egress_mii.py --selftest` still reports 35 of 35.

### Suggestions

Optional. None affects coverage.

- **S1. SUGGESTION. Tests.** `tb/verilator/ctrl_service_budget/egress_fixed_main.cpp:25-28`, `egress_fixed.py:91-140`. The self-test replaces the simulator with a stub, so it holds the period the build is given, not the period the bench runs. With `kSysPs` fixed at 12500, the self-test passes and the documented 100 MHz run reports "312.5 ns, within", exit 0 (`receipts/mutants/D2-*.log`). At this head the bench does take the period: it measures 300.0 ns at 100 MHz against 312.5 ns at the default, both run here. The bench could print its sys period and the tool refuse a run at another.
- **S2. SUGGESTION. Tests, Robustness.** `egress_mii.py:708-725`. No control runs the `--point` dispatch itself.
  - With `--structural` reading the 1x1's queue whatever the point, the self-test passes and the tool prints the 1x1's 391.51 us under `# arty-4x4` (`receipts/mutants/A8-*.log`). FR_NFR 3.4.1 quotes that output.
  - With `--packet` doing the same, the self-test also passes (A9), but a 4x4 packet is then refused, never graded.
  - At this head the 4x4 figures are right: 431.12 us, 2420.78 us and 2711.42 us, as FR_NFR states.
  - Separately, an option in an unexpected position (`--structural --point` with no value, `--selftest --point P`) falls into BUILD mode and ends in a FileNotFoundError traceback, exit 1. The usage text and exit 2 would be clearer (`receipts/cli-probes.log`).
- **S3. SUGGESTION. Tests.** `egress_ledger.py:401,418`. The new control holds `CLOCK_KHZ` to each configuration's `sys_clk_hz`, and the plant reads that table on one line. A plant of 12.5 ns at every point passes the self-test (C3), because a longer overrun is still over. A check that the planted value is the figure plus `1 / config_khz(point)` would hold the plant itself.
- **S4. SUGGESTION. Robustness.** `egress_fixed.py:59`. `str.isdigit()` accepts characters that `int()` refuses. A SYS_HZ of U+00B2 ends in a ValueError traceback, exit 1, not the usage text and exit 2 the docstring states (`receipts/mutants/X1-*.log`). `text.isascii() and text.isdigit()` closes it. The failure is loud, and no figure can come of it.
- **S5. SUGGESTION. Docs.** `egress_fixed.py:104`. `import contextlib` is repeated inside `controls()`; the module imports it at line 22.
- **S6. SUGGESTION. Docs.** Packet, `receipts/census4-extract/FILES.json`. Eight rows, each variant's `build.json`, carry the size and sha256 of the file before its host paths were replaced. `INDEX.md` marks the eight "Redacted: yes" and carries the published hashes, and the regrade on the published bytes gives the same 159 grades (`receipts/extract-files-json-verify.txt`). Hashes taken after redaction, or a note in the index's description of `FILES.json`, would let it verify on its own.
- **S7. SUGGESTION. Docs.** Packet, `receipts/gates5/identity-head-digests.json`. 69 of 72 digests equal the base's: all 66 builder outputs and the three existing product ELFs. The three products' `size.json` differ, and the packet does not say in what. The images are the ELFs, so acceptance item 5 holds; one sentence on the sidecar would close the question.
- **S8. SUGGESTION. Docs.** Harness `README.md:268`. The `--structural` sentence gives the 1x1's figures only (391.5 us, 2.18 ms, 2.65 ms). FR_NFR gives both points'.
- **S9. SUGGESTION. Docs.** Carried from R968-1 S3: the README's 1x1 row links its published qualification, and the 4x4 row links none.

## Reviewer mutation probes

Each mutant is one exact edit in its own copy of the head tree. The command is the in-tree self-test unless stated (`scripts/mutants_r968_2.py`, `receipts/mutants/`). The four clean runs pass.

| ID | Planted defect | Result | Failing control, or why nothing fails |
|---|---|---|---|
| M1 | `crf = ()` in `sr_frames` (round 1's M1) | CAUGHT | `[arty-4x4]` the stream load is the stated one; every frame on the wire |
| A1 | `return aaf` | CAUGHT | the same two |
| A2 | `CRF_AVTPDU = 27` | CAUGHT | `[arty-4x4]` the stream load is the stated one |
| M1b | `CRF_AVTPDU = 0` | CAUGHT | the same |
| A4 | the 4x4 point reads the 1x1 product configuration | CAUGHT | the stream load; the other point's log refused |
| A5 | the grade's queue carries four of five SR frames | CAUGHT | every frame on the wire |
| B1 | `ARTY_CLOCKS['arty-4x4']` = 80 MHz (M10) | CAUGHT | the 4x4 fixture at 100 MHz |
| B2 | `point_name` maps the 4x4 configuration to `arty-1x1` (M8) | CAUGHT | the configuration named to its point |
| B3 | 4x4 not in `REBOOT_PATH_POINTS` | CAUGHT | a missing accepted REBOOT refused |
| B4 | 4x4 not in `COMPLETE` | CAUGHT | an AX pass does not supply 4x4 arm A |
| B6 | `poll_grade` reads (1,5,5) at the 1x1's record cost (M9) | CAUGHT | its own ACMP record cost, 210 us |
| B8 | a 4x4 leg's clock never checked | CAUGHT | an 80 MHz CPU and bus basis refused |
| C1 | `CLOCK_KHZ['arty-4x4']` = 80,000 | CAUGHT | the planted cycle is the configuration's `sys_clk_hz` |
| D1 | `build()` passes 12500 ps whatever it is given | CAUGHT | builds at a 10000 ps sys period |
| D3 | no whole-ps check on SYS_HZ | CAUGHT | SYS_HZ '3' refused |
| E1 | the published extract regraded with no CRF frame in the sources | CAUGHT | all 159 cases refused: the testbench ran five frames, the sources state four |
| E3 | the published extract regraded by a queue that states five frames and carries four | CAUGHT | all 159 cases depart from the printed departures; FAIL |
| E2 | the published extract regraded with the CRF frame one octet short | nothing fails | Equivalent mutant: 45 and 46 octets both pad to the 60-octet minimum frame, so no departure moves. The length is held by the stated-load control (A2). |
| A6 | the testbench's C++ queue (`egress_queue.hpp:86`) carries four of five frames | the self-test passes | The self-test writes its log with the Python model and never runs the C++ queue. That file is not in this PR's diff. A census run with such a queue fails the regrade, as E3 shows from the other side: the published 159 cases agree at 0 ps only with all five frames. |
| A8 | `--structural --point` reads the 1x1's queue | nothing fails | S2 |
| A9 | `--packet --point` reads the 1x1's queue | the self-test passes | S2; fail-safe, since the 4x4 packet is then refused |
| B5 | `LABELS['arty-4x4']` = `arty-1x1` | nothing fails | At `record_classes.py:604` the gate takes only group names from the labelled point. The same edit at the 1x1 (B5b) is equally unseen, so the 4x4's controls match the 1x1's, which is what F2 asked. |
| C3 | the ledger's plant uses 12.5 ns at every point | nothing fails | S3 |
| D2 | the bench ignores `EGRESS_FIXED_SYS_PS` | nothing fails | S1 |

## Clean lenses

```text
[R968] PASS Conformance - issue #1027 (Task, Acceptance, Decisions 1 to 5); configs/endstation_arty_split_4x4.yaml:63-64; tb/verilator/ctrl_service_budget/egress_mii.py:70-77,140-148; bind_save.py:57,61; egress_ledger.py:101-110; docs/reference/FR_NFR.md:299,522-524; receipts/extract-egress-regrade.log; receipts/extract-ledger-regrade.log; receipts/head-arty_grade-arty-4x4.log - acceptance items 1 to 7 against evidence (table below; item 8 is a bench duty, NOT MET, outside what a source head can show); decision 1: sys and CPU 100000000 Hz, datapath 50000000 Hz, and the published route reports meet the +0.030 ns floor at all four corners; decision 2: the seven ledger figures, 61.65 to 63.50 ms, cover the measured 61.56471 to 63.32736 ms, and the extract's 1655 instances are within them; decision 3: 550 ms and 4 saves at arty-4x4; decision 5: FR-CLK-05's pair recorded as owed under #1027; the stream load is 18 + 24 + 2 x 6 x 4 = 90 octets a talker and 18 + 28 = 46 for the CRF output, and the row is (446.76 + 54.88) x 1.05 + 0.32 = 527.04 us of 1000; the model gate reproduces load 0.46887, ACMP 28.52, txL 48.72 and last notice 117.68 ms, byte-identical to the author's receipt
[R968] PASS RTL - git diff --name-only 12ab4b18..47f2a3d7 (16 files: one configuration, five documents, nine harness scripts, sw/builder/test_builder.py); configs/endstation_arty_split_4x4.yaml:4; configs/generated/endstation_arty_split_4x4/gen/adp_shape_defaults.svh; sw/builder/endstation_builder.py:3718-3724; receipts/config-header-identity.txt - the delta holds no HDL, LiteX, firmware, mailbox or generated file; its one configuration edit is a header comment; the builder's eleven outputs for that configuration are identical with the file as at 12ab4b18 and at the head, and the generated include equals the tracked one (b23e1903...); the model id is hashed from the model shape, never from the file's bytes; nothing the round-1 RTL result examined has changed
[R968] PASS Robustness - tb/verilator/ctrl_service_budget/egress_fixed.py:57-76; egress_mii.py:440-448,640-656,708-715; egress_ledger.py:116-122; receipts/cli-probes.log; receipts/head-egress_fixed-selftest.log; receipts/mutants/E1-census-regrade-without-crf.log - a SYS_HZ of 0, a negative, a non-number, a fraction, a signed number or a non-whole-ps period, an extra argument, and an option in BUILD_DIR's place each exit 2 with the usage text; an unknown --point exits 2; a log of the other point's queue is refused at each point, and a census whose queue states another frame count is refused case by case; config_khz raises on a configuration that does not state sys_clk_hz exactly once (read, not run); S2 and S4 record two loud tracebacks on malformed command lines, neither able to produce a figure
[R968] PASS Tests - tb/verilator/ctrl_service_budget/egress_mii.py:565-670; record_classes.py:453-551; egress_ledger.py:110-122,401-418,486-490; egress_fixed.py:91-170; selftest_share.py:164-172; receipts/head-*-selftest.log; receipts/mutants/mutants.json and its two companions - each new control fails for the defect it names: 15 reviewer mutants fail an in-tree self-test, the eight round 1 named among them, and two more fail the regrade of the published census; the seven that fail nothing are an equivalent mutant, a file outside this PR, a label the gate does not read, and four reporting or fixture paths recorded as S1 to S3; the four self-tests' outputs are byte-identical to the author's receipts at this head; the service self-test's clock check now reads each Arty clock from arty_grade.CLOCKS against the configurations, and the author's receipt shows it passing within 323 of 323
[R968] PASS Docs - docs/design/SPLIT_CONTROL_MEMORY.md:28,3493,3632-3690; docs/reference/FR_NFR.md:299,522-524; tb/verilator/ctrl_service_budget/README.md:8,51,230,261,264-268; docs/ENDSTATION_BUILDER.md:15,25-39; docs/integration/BUILDING.md:361,375; sw/firmware/ctrl/loop/ctrl_loop.h:415-427; receipts/docs-check.log; receipts/head-structural-4x4.log; receipts/head-structural-1x1.log - the twelve stated costs equal the firmware's (1,5,5) row; the two qualifying rows and their order equal the published derivation; FR_NFR's 431.12 us, 2.42 ms, 2.71 ms and 35 records equal the tool's output and the regrade; the README's counts (eleven controls a point, thirteen plants, twenty-six ledger mutants, three fixed-path mutants) equal the self-tests' output; no link to the renamed section's old anchor remains; scripts/docs_check.py reports 0 findings over 226 markdown and 1985 text files; no U+2014 is on an added line and git diff --check is clean; no new source comment in the delta shows a lane label, review round, reviewer ID or issue-comment ID, and the one round 1 found is gone
```

## #1027's acceptance, item by item

| Acceptance item | Result at this head | Basis |
|---|---|---|
| 1. Route meets the #818 floor at every corner, best of three directives | Met, on the author's receipts | Published reports: ExtraPostPlacementOpt Slow WNS +0.049 / WHS +0.156, Fast WNS +1.606 / WHS +0.012 ns, 0 failing endpoints. Not re-routed here. Nothing the route reads changed in the delta. |
| 2. The rule's row meets every owner bound at 1if | Met | `arty_grade.py --point arty-4x4`, run here: load 0.4689 of 0.70, ACMP 28.52 of 30 ms, txL 48.72 of 49 ms, last notice 117.68 of 140 ms. THE SHARE, 1.733 of 2 ms, is the census receipt's. |
| 3. 100 Mb/s egress within 1000 us with the CRF output in the load | Met | Regraded here from the published extract: 527.042 us, load (90, 90, 90, 90, 46), 159 cases agreeing at 0 ps. E3 shows that agreement depends on the CRF frame. |
| 4. Every gate passes, or states why NOT RUN | Met, on the author's receipts | Gate 11 is NOT RUN with its reason printed (`gates5/test_builder.log:860-862`). The four renderer-bound documentation commands fail on the system interpreter and pass in the pinned environment; the packet says so. |
| 5. The 1x1 Arty and AX7101 images byte-identical to the base | Met, on the author's digests | 66 builder outputs and three product ELFs are equal. Not rebuilt here. The delta cannot move an image, because no source of one is in it. See S7. |
| 6. FR_NFR and SPLIT_CONTROL_MEMORY state the point | Met | The lines cited under Docs. |
| 7. Every change has a self-checking control with a planted defect | Met for every behaviour a gate or grade depends on | The mutation table. S1 and S2 name two reporting paths whose controls stop one step short. If the criterion is read as every code path, those two are what remains. |
| 8. Bench session with 4+4 streams and CRF at once, and the latency pair at 100 MHz | NOT MET | No bench session and no flash. The PR and the packet state it as owed. |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1027 body; `configs/endstation_arty_split_4x4.yaml:63-64`; `egress_mii.py:70-77,140-148`; `bind_save.py:57,61`; `egress_ledger.py:101-110`; `FR_NFR.md:299,522-524`; the extract regrades; the model gate at both Arty points | R968-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| RTL | CLEAN | the delta's file list; `configs/endstation_arty_split_4x4.yaml:4`; builder outputs with and without the header edit; the generated shape include; `endstation_builder.py:3718-3724` | R968-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Robustness | CLEAN | `egress_fixed.py:57-76`; `egress_mii.py:440-448,640-656,708-715`; `egress_ledger.py:116-122`; 15 command-line probes; E1 | R968-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Tests | CLEAN | `egress_mii.py:565-670`; `record_classes.py:453-551`; `egress_ledger.py:110-122,401-418,486-490`; `egress_fixed.py:91-170`; `selftest_share.py:164-172`; four self-tests; 24 mutants; the author's service self-test receipt | R968-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Docs | CLEAN | `SPLIT_CONTROL_MEMORY.md:28,3493,3632-3690`; `FR_NFR.md`; the harness `README.md`; `ENDSTATION_BUILDER.md`; `BUILDING.md`; `ctrl_loop.h:415-427`; the PR body; the packet manifest and indexes; `docs_check.py` | R968-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |

All five lenses are clean at this head in this round. Q1 to Q3 are residue and S1 to S9 are suggestions; neither class leaves a lens open.

## The concurrent internal round, R967-2

`[R967] POSITIVE` at this same head (issuecomment-7242154105) was published while this review ran. It was read after the verdict and ledger above were written. It reports no BLOCKER, MAJOR or MINOR. Each of its items, at this head:

| Its item | Result here | Basis |
|---|---|---|
| RES1 (residue): `SPLIT_CONTROL_MEMORY.md:3634-3635` says "the decisions below (its decisions 1 to 5)" | RETAINED, concurred | The 4x4 subsection cites decisions 1, 2 and 3 only (lines 3639, 3684, 3686); 4 and 5 are stated in `ENDSTATION_BUILDER.md` and `FR_NFR.md:299`. This review did not find it. Its exact fix stands. |
| RES2 (residue): "28 files in 21 commits" | RETAINED, the same as Q2 | 22 commits and two merges. |
| RES3 (residue): the packet is not linked from the PR body | RETAINED, the same as Q1 | Its published report now carries the link in a PR comment; the PR body and #1027 still do not. |
| RES4 (residue): harness `README.md:269`, "**At the Arty**" | RETAINED, concurred | The bullet's 426.47 us, 505.74 us and 19 records are the 1x1's; the bullet above it now covers both points. Its exact fix stands. |
| S1: repeated `import contextlib` | the same as S5 here | |
| S2: `g-full.txt` and `g-ext.txt` keyed without the variant | concurred | 152 distinct keys for 159 lines, confirmed here. The summary above says "as a multiset" for that reason. This review's own regrade prints `variant/case` and equals them once the variant is dropped. |
| S3: section 15's stated-cost tables held by no self-test | concurred, optional | The 4x4 table equals `ctrl_loop.h:416-427` today. |
| S4: `config_khz` reads `sys_clk_hz` by regex, `point_spec` by YAML | concurred, optional | A mismatch would fail loudly. |
| S5: `crf-frame-not-queued` at `arty-1x1` removes the AAF frame | concurred, optional | `sr_bytes[:-1]` of `(90,)` is empty there; the 4x4 catch is the real one. |
| S6: #1027 lacks some AGENTS.md section 4 fields | concurred | Listed under Pending manager duties. |
| S7: say why the products' `size.json` differ | the same as S7 here | |

Nothing in it is a BLOCKER, MAJOR or MINOR, so none changes a lens in the ledger above. Its RES1 and RES4 are wording in documents this delta touched and go to the residue checklist with Q1 to Q3.

## Receipts

Listed with hashes in `MANIFEST.sha256`. Host paths are replaced by `$CLONE`, `$PACKET`, `<TREE>`, `<EXTRACT>` and `<SCRATCH>`.

- `receipts/head-*-selftest.log` and `.rc`: the four self-tests at the head, rc 0, byte-identical to the author's.
- `receipts/head-egress_fixed-100.log`, `head-egress_fixed-default.log`: the fixed-path bench as documented, with Verilator 5.050.
- `receipts/head-structural-*.log`, `head-arty_grade-*.log`: the structural figures and the model gate at both Arty points.
- `receipts/extract-egress-regrade.log`, `extract-ledger-regrade.log`: the published census-4 extract regraded.
- `receipts/packet-manifest-verify.txt`, `packet-index-verify.txt`, `extract-files-json-verify.txt`: 827 manifest entries, 822 index rows and 218 mapping rows verified, and the eight pre-redaction rows of S6.
- `receipts/mutants/`: one log a mutant and three JSON summaries. `scripts/mutants_r968_2.py` plants and runs them.
- `receipts/cli-probes.log`: 15 malformed command lines.
- `receipts/config-header-identity.txt`: builder outputs across the configuration header edit.
- `receipts/docs-check.log`, `diff-check.log`, `em-dash.log`, `gen-toc-check.log`: the documentation gates that ran here, and the two that could not.
- `receipts/restore-verification.log`: the clone after the probes.

## Limits

- **Not reproduced:** the route (no Vivado run), the censuses, the firmware shards, the boot and region simulations, the builder suite, the service self-test (the author's 323 of 323 at this head was read, not rerun), and the byte-identity rebuilds. For these the evidence is the author's packet. Its hashes were verified, and its figures were cross-checked wherever a published receipt allows.
- **No manager source bank** ran at this head, and none is claimed. Source-head execution evidence is the author's gate receipts and the reruns listed above.
- **Hosted evidence:** this head has no check run, no workflow run and no commit status. Nothing was executed and nothing was skipped.
- **The self-tests are local gates.** No workflow runs the service-budget harness or its four standalone self-tests. That was so before this PR.
- **Two documentation gates did not run here.** `check_em_dash.py` and `gen_toc.py --check` need the pinned Markdown renderer, which this host lacks. The author's receipts show both passing in the pinned environment (0 findings over 2821 added lines; 161 pages). A direct scan of the delta's added lines found no U+2014.
- **The extract cannot authenticate omitted bytes.** It carries the lines the two grades read; the census traces stay with the author. Its regrade equals the packet's full-log grades.
- **No hardware.** The 4x4 image has not been flashed or booted in this review. The correction pair at 100 MHz is unmeasured. Physical calibration is NOT RUN, and simulation and skipped field checks are not hardware proof.
- **Thin margins, as the author states:** setup 0.019 ns over the floor on one directive of three, hold +0.012 ns, txL 0.28 ms, THE SHARE 0.267 ms.
- **Clause text:** Milan v1.2 5.4.2.7, 7.2.3 and 7.3.2 and IEEE 802.1Q 34.3.1 were not read from the standards. The arithmetic was recomputed. The clause readings are the tree's; 7.3.2 is cited for the CRF profile elsewhere in the tree.
- **PR #1004** is reviewed separately. Nothing below `c0b625d1` was reviewed here.
- **Clone state:** restored and verified. Head `47f2a3d7`, tree `998ce7dd`, 2,010 tracked blobs re-hashed with no byte or mode mismatch, the index hash equal to its value before the probes, six gitlinks unchanged, and no untracked or ignored file left. Three bytecode cache directories written by child processes of the gates were removed.

## Pending manager duties

- Link the evidence packet from the PR body or #1027 (Q1), and carry Q1 to Q3 and the internal round's RES1 and RES4 to the residue checklist.
- **#1027's item 8.** The bench session and the 100 MHz correction pair are owed. The PR body says `Closes #1027`, and the issue should stay open until the session is on record. The base, `dev-soft-core`, is not the default branch, so this merge will not close the issue by itself, but a later merge into `dev` may.
- #1027 shows Project status `Backlog` and no assignee while its PR is in review, and its body does not name the executor and reviewer. AGENTS.md sections 4 and 5 put an active task at `In progress` with both set.
- The review bar asks for two positive reviews at this exact head. The internal round published POSITIVE at this head (issuecomment-7242154105), and this report is the external one; the manager checks the pair against the bar.
- Obtain hosted or replica verdicts for the head; none exists.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, after PR #1004 lands, and link its receipts on the PR.
- #1022 owns the registration cost left out under #969's disposition at this point.
- Any later commit that touches a lens's scope un-covers that lens. This ledger stands for `47f2a3d7` only.

R968-2 FINISHED

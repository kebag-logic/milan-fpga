[R968] NEGATIVE - exact head 12ab4b189f54439cd126f677b906a19835d7f32a

Round R968-1, external independent review of PR #1026 (draft, base `dev-soft-core`, stacked on PR #1004), relating to issue #878.
Tree `1aa020a3f0e62cff459120209e5157a4e6689276`. Reviewed delta: `c0b625d1792e61b8e99944daea65b842e6b9dcde..12ab4b189f54439cd126f677b906a19835d7f32a`, 28 files, +619/-86.
Reconstructed from AGENTS.md, CONTRIBUTING.md, the issue and its manager rulings, the diff and history, and the author's packet at evidence commit `1994a795` (`review-evidence/arty4x4-r1/author`).

## Summary

The technical content of the delta holds wherever it could be checked at this head:
- the tree's model reproduces every stated figure (load 0.4689, ACMP 28.52 ms, txL 48.72 ms, last notice 117.68 ms);
- the installed statements equal the published census receipt term for term;
- the ledger figures are the rule applied to the published measurements;
- the generated shape include regenerates byte-identical;
- the fixed path measures 300.0 ns at 100 MHz;
- the firmware's (1,5,5) row compiles and its transmit-bound assertion fires at the boundary;
- the standalone self-tests, the service self-test (323 of 323 mutants), twelve focused builder gates and eleven documentation gates pass.

The verdict is NEGATIVE on five open MINOR findings. None reports a wrong figure in the tree.
- **Tests (F1, F2, F3):** three behaviours this delta adds have no control that fails without them. Four planted defects pass every standalone self-test and all 1,073 checks of the service self-test.
- **Docs and Conformance (F4, F5):** the decisions the change rests on are not on the public record, and the published packet omits the receipts for three load-bearing figures.

## Findings

### F1

```text
[R968] MINOR Tests — tb/verilator/ctrl_service_budget/egress_mii.py:132-140 — The CRF output's frame in the 100 Mb/s stream load has no control
Requirement/evidence: AGENTS.md section 5 (self-checking tests for changed behaviour) and section 6, Tests. Commit e7bc55f8a adds the CRF output's 46-octet frame to `sr_frames`; FR_NFR 3.4.1's 4x4 row (527.04 us) is graded with it. `egress_mii.py --selftest` builds its queue from `endstation_arty_current` only (`arty_spec`, line 634), a shape with no CRF output, and no other self-test reads `sr_frames`. Probe M1 replaces line 139 with `crf = ()`: the 4x4 load becomes (90, 90, 90, 90) and every check still passes (receipts/probes.log, receipts/probes-service-checklist.log). A census would not notice either: the testbench's queue and the grade's replay read the same function, and the EGRESSQ line they compare carries the frame count only.
Impact: the stream load of the one 100 Mb/s point with a CRF output can lose that frame silently, and the egress row would then be graded against a lighter queue than the image's.
Required change: a control at a shape with a CRF output that fails when the CRF frame is absent from the queue's stream load or has another length, with its planted defect.
Verification: M1 is caught by an in-tree self-test; `egress_mii.py --selftest` stays green at the head.
```

### F2

```text
[R968] MINOR Tests — tb/verilator/ctrl_service_budget/record_classes.py:101-108,143-150,255,453-502 — The record-class gate's arty-4x4 branches have no control
Requirement/evidence: AGENTS.md section 6, Tests. The delta adds `arty-4x4` to COMPLETE, LABELS, REBOOT_PATH_POINTS, ARTY_CLOCKS (100 MHz) and `point_name`; the qualification cites this gate ("record_classes over the legs, PASS"). `arty_checks()` (line 453) builds its fixture at `arty-1x1` only, where two controls plant a leg on the wrong clock; the 4x4 has none. Probes: M8 (`point_name` maps `endstation_arty_split_4x4` to `arty-1x1`), M10 (`ARTY_CLOCKS['arty-4x4']` = 80 MHz) and M9 (`poll_grade.py:195` takes arty-1x1's `record.acmp` at (1,5,5)) each pass `record_classes.py --selftest`, `arty_grade.py --point arty-4x4` and all 1,073 checks of the service self-test (receipts/probes.log, receipts/probes-service-checklist.log).
Impact: a 4x4 leg measured at the wrong clock, or graded at the 1x1's statements, is refused or accepted by code no test exercises. M8 and M10 would be refused loudly by a real 100 MHz census; M10 would accept a census run at 80 MHz.
Required change: controls at `arty-4x4` matching the 1x1's: a 4x4 leg off 100 MHz refused, the 4x4 configuration named to its own point, and its own stated costs read at (1,5,5).
Verification: M8, M9 and M10 are each caught by an in-tree self-test.
```

### F3

```text
[R968] MINOR Tests, Docs — tb/verilator/ctrl_service_budget/egress_fixed.py:11,20,53 — The fixed-path bench cannot be run as its usage line states, and its new clock option has no test
Requirement/evidence: AGENTS.md section 5 (reproducible evidence) and section 6, Tests and Docs. Commit 41166c346 rewrites the usage line to `python3 -I egress_fixed.py BUILD_DIR [SYS_HZ]` and adds the option that produced FR_NFR 3.4.1's "300.0 ns" at 100 MHz. Run that way, the tool stops at line 20 with `ModuleNotFoundError: No module named 'egress_mii'` (receipts/egress-fixed-isolated-usage.log): isolated mode leaves the script's directory off the import path, and unlike its neighbours this file does not add it. Without `-I` it measures 312.5 ns at 80 MHz and 300.0 ns at 100 MHz (receipts/egress-fixed-80.log, egress-fixed-100.log), so the figures themselves stand. No self-test, gate or workflow runs the tool. The same usage line failed at the base; this delta edited it and extended the tool behind it.
Impact: the command the tree gives for a figure FR_NFR quotes does not run, and nothing in the tree would show it.
Required change: the documented invocation runs; the SYS_HZ report path is exercised by a test or its absence is stated where the figure is quoted.
Verification: `python3 -I tb/verilator/ctrl_service_budget/egress_fixed.py DIR 100000000` exits 0 reporting 300.0 ns.
```

### F4

```text
[R968] MINOR Docs, Conformance — issue #878 and PR #1026 (public record) — The scope and the decisions this change rests on are not public
Requirement/evidence: AGENTS.md section 1 (all useful state public), section 2 (a cold reviewer reconstructs the task from GitHub and the repository; a conflict between Issue and implementation is published), section 4 (frozen acceptance, public task contract). Searched: all 20 comments of #878, the PR's comments and reviews, every repository comment since 2026-11-26, and issue bodies naming the 4x4.
(a) #878's frozen scope is "One Arty configuration ... at the 1x1 shape", and its one clock ruling (issuecomment-7097204685) sets the Arty's sys/CPU clock to "80,000,000 Hz exactly". No public comment scopes a second configuration at 4x4, moves its clock to 100 MHz, states its acceptance, or names its executor and reviewer. The only public mention is "4x4/1if target" in #1022's body.
(b) The seven arty-4x4 held-egress rows are new recorded misses of FR_NFR 3.4.1's 20 ms budget, up to 63.50 ms. Every other ledger point cites its own ruling. The author's round-3 report says "#878's held-egress ruling states a ledger for (1,1,2) only ... decision needed"; round 4 applies "the manager's five decisions", none of which is public. The tree cites PR #1020's ruling, which rules on the USB-network Arty.
(c) The bind bounds (550 ms, 4 saves) apply a rule whose public ruling (PR #1004, issuecomment-7221391389) names `arty-1x1`.
(d) Neither the PR nor the issue links the evidence packet.
Impact: the acceptance this PR is measured against, and the authority for seven new ledgered misses, cannot be reconstructed from public state.
Required change: the scope and acceptance of the 4x4/100 MHz qualification, the ledger-point decision, the bind-bound confirmation and the other applied decisions are published on the issue or the PR, with a link to the evidence packet. No source change is required by this finding.
Verification: a reviewer finds each decision by link from #878 or PR #1026.
```

### F5

```text
[R968] MINOR Docs — review-evidence/arty4x4-r1/author (evidence commit 1994a795) — The published packet omits the receipts its own indexes name for three load-bearing figures
Requirement/evidence: AGENTS.md section 6, Docs ("enough evidence for another cold reviewer"). The three receipt indexes name 251 files; 123 of them, every compressed one, are not in the published tree (receipts/crosscheck.log, last three lines). Among them:
- `egress_mii-census4.log.gz`: the only receipt for the 446.76 us wait behind FR_NFR 3.4.1's 527.04 us. The figure appears in no published machine receipt.
- the twelve signoff timing reports and three utilization reports of the final route. The published `routefinal-graded-images.json` carries their figures and hashes, not the reports.
- `ledger-census4.log.gz` (1,655 instances), `test_builder.log.gz` (gate 11's NOT RUN line), and the firmware, boot, region and memory logs, published as return codes only.
`egress_mii.py --packet` grades with the 1x1's queue (`arty_spec`, lines 663-669), so a 4x4 extract would be refused as "another queue": there is no public regrade path for this point.
Impact: the egress row's measured wait and the route's corner figures rest on the author's summary alone.
Required change: the named receipts, or compact extracts a published command regrades, are public at an evidence commit linked from the PR.
Verification: each index entry resolves to a file with its stated hash; the 446.76 us wait is reproduced from a published receipt.
```

### Residue

Wording only; each changes no figure, verdict, test or code path.

- **R1, `tb/verilator/ctrl_service_budget/egress_ledger.py:102`.** A new source comment carries an issue-comment ID ("#1020's ruling (comment 7234489667, item 3)"), against the comment rule of 2026-10-15. Fix: "as PR #1020's ledger ruling (item 3) makes the USB-network Arty's".
- **R2, `tb/verilator/ctrl_service_budget/shape_costs.py:57`.** "Arty's 80 MHz FPGA points" now covers (1,5,5), which runs at 100 MHz. Fix: "Arty's FPGA points state these additional measured costs and their own pace, each at its shape and clock: (1,1,2) at 80 MHz and (1,5,5) at 100 MHz (#878)". The check title at `selftest_share.py:169` ("Arty is exactly 80,000,000 Hz") has the same slip; fix: "arty-1x1 is exactly 80,000,000 Hz".
- **R3, PR body, "100 Mb/s egress".** "plus the 300 ns fixed path measured at 100 MHz, is 527.04 us": 527.04 uses the stated 320 ns, as FR_NFR and section 15 say; with 300 ns it is 527.02. Fix: "plus the stated 320 ns fixed path (300.0 ns measured at 100 MHz), is 527.04 us of 1 ms".
- **R4, `tb/verilator/ctrl_service_budget/README.md:264`.** The queue bullet still gives the stream load as "the shape's SR frames (90 bytes each 125 us)". Fix: add "and, where the shape has a CRF output, its 46-byte frame".

### Suggestions

- **S1, `egress_fixed.py:53`.** A SYS_HZ of 0 or a non-number ends in a traceback (rc 1) rather than the usage text (receipts/cli-robustness.log).
- **S2, `docs/design/SPLIT_CONTROL_MEMORY.md:3493`.** Section 15 is titled "Arty split at 80 MHz" and now holds the 100 MHz point; its contents line was updated, the heading was not.
- **S3, `tb/verilator/ctrl_service_budget/README.md`.** The 1x1 row links its published qualification; the 4x4 row has no such link.

## Clean lenses

```text
[R968] PASS RTL — configs/generated/endstation_arty_split_4x4/gen/adp_shape_defaults.svh; sw/litex/milan_soc.py:272-315; sw/firmware/ctrl/loop/ctrl_loop.h:415-427; sw/firmware/ctrl/loop/ctrl_loop.c:203; hdl/milan/milan_datapath.sv:8916,9846,10458 — no HDL, LiteX or mailbox file is in the delta; the include regenerates byte-identical (b23e1903...); the Arty PLL is pinned to an 800 MHz VCO with margin=0, so 100/50/25/200 MHz divide exactly by 8/16/32/4; the (1,5,5) row compiles on the host and its transmit-bound assertion passes at 49 ms and fails at 50; an unlisted (1,4,4) shape is refused; builder gates 23m (11 real elaborations), 23n, 23o and the clock-contract gates pass; open issue #800's narrow MAAP index sits in blocks the split placement does not build
[R968] PASS Robustness — tb/verilator/ctrl_service_budget/arty_grade.py:131-136; egress_ledger.py:104-122,383-440; record_classes.py:143-150; configs/endstation_arty_split_4x4.yaml:63,126-135 — bad and missing `--point` values exit 2 with usage; an unknown ledger point and a path with no instance are refused; a 4x4 leg at two interfaces is refused; each ledger row one 10 ns cycle over its figure fails at the 4x4 point; the owner gate refuses 0.01 ms over each bound and an unbounded row; the 4x4 at 80 MHz, a 10 ms pace, a 1000 us slice and a 28 ms transmit statement are each refused by the model gate (probes M2 to M5); formats outside the 100 Mb/s envelope are absent from the advertised set, and the CRF load is counted at sixteen times its rate
```

## The assigned checks

| Check | Result at this head |
|---|---|
| 4x4 configuration and per-point clocks | Holds. (1,5,5) shape, sys 100 MHz, datapath 50 MHz; every per-point table has its own arty-4x4 entry; the 1x1 stays at 80 MHz. Probe M2 (80 MHz) refused. |
| Route at the floor, every corner | Author receipt, consistent: ExtraPostPlacementOpt worst WNS +0.049, worst WHS +0.012 ns, 0 failing endpoints over four corners; the other two directives +0.002 ns, graded FAIL. Routed at `a64c88bd`; since then no gateware input changed but `CTRL_LOOP_TX_MS` 28 to 29, read only as (TX + 9) / 10. Reports not published (F5). Not re-routed. |
| Row and owner bounds | Reproduced from the tree: load 0.46887, ACMP 28.52, txL 48.72, last 117.68 ms. THE SHARE 173,322 cycles = 1.733 ms from the census receipt. 39 installed statements equal the receipt. |
| 100 Mb/s egress, CRF counted | Arithmetic reproduced: (446.76 + 54.88) x 1.05 + 0.32 = 527.04 us. Stream load (90, 90, 90, 90, 46). The 446.76 us wait has no published receipt (F5); the CRF term has no test (F1). |
| Held-egress ledger, 63.50 ms | Figures are the rule applied to the receipt's measurements (6,264,658 cycles = 62.64658 ms, and so on); section 15 equals the tool; the self-test catches 24 mutants. The deciding ruling is not public (F4). |
| Bind bounds | 2 x 253.671 = 507.3, stated 550 ms; floor(530 / 253.671) + 2 = 4 saves. Pinned by the service self-test (probe M7 caught). |
| FR_NFR 3.4.1 and section 15 | Every figure matches the tool or a receipt; documentation gates pass. |
| 1x1 and ALINX images byte-identical | Not rebuilt here. No existing configuration, HDL, LiteX or firmware source changes in the delta except the new `#elif` row and one assertion operand; `endstation_arty_split` regenerates its tracked include byte-identical. Author digests published. |
| Gate 11 NOT RUN | Its oracle path is absent on this host too; the gate skips by design when the report is not on disk. The stated reason is accurate. |
| 100 MHz latency pair owed | Recorded in FR_NFR (FR-CLK-05 note), the configuration header and the builder suite's comment; the image keeps 1409/100 ns. |
| Comment rule | One new instance (R1). |

## Reviewer-owned ledger

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F4) | #878 body and rulings 7096503672, 7097204685, 7097474930, 7153532537; PR #1020 ruling 7234489667; PR #1004 ruling 7221391389; #1022; `configs/endstation_arty_split_4x4.yaml`; `docs/reference/FR_NFR.md:299-305,519-522`; `arty_grade.py --point arty-4x4`; `tools/crosscheck.py` (50 of 50) | R968-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| RTL | CLEAN | generated shape include; `milan_soc.py:272-315`; `ctrl_loop.h:415-427`; `ctrl_loop.c:203`; `milan_datapath.sv` split generates; builder gates 23m/23n/23o; `routefinal-graded-images.json` | R968-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Robustness | CLEAN | `arty_grade.py`, `egress_ledger.py`, `record_classes.py` negative paths; probes M2 to M5, M12, M13, M15, M16; receipts/cli-robustness.log | R968-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Tests | UNCLEAN (F1, F2, F3) | `egress_mii.py`, `record_classes.py`, `poll_grade.py`, `egress_fixed.py`, `egress_ledger.py`, `selftest*.py`, `sw/builder/test_builder.py` (12 gates); 16 probes; service self-test 323 of 323 | R968-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Docs | UNCLEAN (F3, F4, F5) | `SPLIT_CONTROL_MEMORY.md:3632-3692`; `FR_NFR.md`; harness `README.md`; `ENDSTATION_BUILDER.md`; `BUILDING.md`; `AAF_LATENCY_TAPS.md`; PR body; evidence packet indexes; eleven documentation gates | R968-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |

No lens is banked by this round for the merge: two are clean at this head and three are open.

## Prior findings on this PR

None. When this report was written the PR carried two comments, both review-start notices, and no review. No other reviewer's report was read.

## Receipts

Listed with hashes in `MANIFEST.sha256`. Host paths are replaced by `$CLONE` and `$PACKET`.

- `receipts/arty_grade-4x4.log`, `arty_grade-1x1.log`, `arty_grade-selftest.log`: the model gate, rc 0.
- `receipts/standalone-*.log` and `.rc`: seven standalone self-tests, rc 0 (egress_ledger 24 mutants, rows_tiers 1033, load_grade 28, record_classes 26 and 9, shape_costs 25, egress_mii 17, kept_grade 32).
- `receipts/service-selftest.log`: 323 of 323 mutants caught over eight partitions.
- `receipts/probes.log`, `probes-service-checklist.log`, `tools/probe.py`: 16 planted defects, 9 caught, 7 not (M1, M8, M9, M10 are F1 and F2; M6 and M11 are a stated cost and a prose row that only a census or a reader holds, as at the 1x1; M14 removes a compile-time assertion, which no test can see).
- `receipts/crosscheck.log`, `tools/crosscheck.py`: 50 cross-checks of tree, rule and published receipts.
- `receipts/builder-regenerate.log`, `builder-focused-gates.log`: regeneration identity; 12 of 115 builder gates, rc 0.
- `receipts/egress-fixed-80.log`, `egress-fixed-100.log`, `egress-fixed-isolated-usage.log`: the fixed path, with the pinned Verilator 5.050.
- `receipts/ctrl-loop-shape-compile.log`, `cli-robustness.log`, `docs-gates.log`, `restore-verification.log`.

## Limits

- **Not reproduced:** the route (no Vivado run), the three censuses (hours of simulation each), the 100 Mb/s grade over census 4, the firmware shards, the boot, region and memory simulations, the full builder suite, the byte-identity rebuilds. For these the evidence is the author's packet, checked for internal consistency only.
- **Builder suite:** 12 of 115 gates were run, chosen for the tables the delta touches. That is not the suite's verdict.
- **Hosted evidence:** the head has no check run and no workflow run. Nothing was executed and nothing was skipped; there is no hosted verdict to read.
- **No hardware:** the 4x4 image has not been flashed or booted. The correction pair at 100 MHz is owed and unmeasured; simulation and skipped field checks are not hardware proof.
- **Thin margins, as the author states:** setup 0.019 ns over the floor on one directive of three, hold +0.012 ns, txL 0.28 ms, THE SHARE 0.267 ms. They meet their bounds; a later change to this image has little room.
- **Clause text:** Milan v1.2 Table 4.4, 5.4.2.7, 6.4 and 7.2.3 were not read from the standard. The bandwidth arithmetic was recomputed; the clause readings are the tree's.
- **PR #1004** is reviewed separately; its content below `c0b625d1` was not reviewed here.
- **Clone state:** restored and verified: tree `1aa020a3`, 2,010 tracked blobs re-hashed with no mismatch, modes and index equal to the head, six gitlinks unchanged, no untracked or ignored file left (receipts/restore-verification.log).

## Pending manager duties

- Publish the scope, acceptance and applied decisions of the 4x4/100 MHz qualification, and link the evidence packet (F4).
- Publish the omitted receipts or regradeable extracts (F5).
- Carry R1 to R4 to the residue checklist.
- Obtain hosted or replica verdicts for the head; none exists.
- Validate the current-dev merge candidate (builder and native banks) at the merge turn, after PR #1004 lands.
- The bench: boot and link of the 4x4 image, and the correction pair at 100 MHz.
- #1022 owns the registration cost left out under #969's disposition at this point; counted, the load is 0.82 and no last-notice row is finite.
- A re-review of the corrected head is required; this round's clean lenses stand only while nothing in their scope changes.

R968-1 FINISHED

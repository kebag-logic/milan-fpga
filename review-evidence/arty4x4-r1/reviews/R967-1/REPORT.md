[R967] NEGATIVE - exact head 12ab4b189f54439cd126f677b906a19835d7f32a

Round R967-1. This is the internal, independent review of kebag-logic/milan-fpga PR #1026, which relates to #878. The review was run in a cleared context.

- Head `12ab4b189f54439cd126f677b906a19835d7f32a`, tree `1aa020a3f0e62cff459120209e5157a4e6689276`.
- Reviewed delta: `c0b625d1792e61b8e99944daea65b842e6b9dcde..12ab4b189f54439cd126f677b906a19835d7f32a`. That is 28 files, 15 lane commits and two merges of #1004. #1004's own commits are reviewed separately.
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

The verdict is NEGATIVE for three MINOR findings:
- F1: the 4x4 lane has no public task contract or decision record.
- F2: the new CRF egress term and the `arty-4x4` egress parameters are checked by no self-test. Two mutants survive every gate.
- F3: the published evidence packet leaves out every indexed compressed receipt. Among them are the logs that carry the 527.04 us egress grade, the 1655-instance ledger grade, the signoff timing reports and the builder-suite log.

The measured content checked out wherever I could reproduce it:
- The cost statements recompute from the published census cycles.
- The ledger, bind and egress arithmetic holds.
- The service self-test passes at 323 of 323.
- The datapath elaborates cleanly at the split 4x4 shape.
- The existing points' tables are unchanged.
- The clone is restored byte for byte.

## Findings

### F1. MINOR. Conformance, Docs. The 4x4 lane has no public task contract, and its decisions have no public record

Artifact: issue #878 (body and comments to 2026-11-28), PR #1026 (body and comments), `configs/endstation_arty_split_4x4.yaml:4`, `tb/verilator/ctrl_service_budget/run.py:39` ("arty-4x4 #878's").

Requirement and evidence:
- AGENTS.md section 2 requires that a cold reviewer can reconstruct the task from GitHub and the repository alone. Conflicts must be published, not settled privately.
- AGENTS.md section 4 requires a public task contract, with acceptance criteria and no open decision, before work starts.
- #878's body limits the scope to "One Arty configuration ... at the 1x1 shape" and lists 8x8 as out of scope. Its frozen acceptance names no 4x4 point.
- #878's clock ruling (issuecomment-7097204685) says "The Arty's sys/CPU clock becomes 80,000,000 Hz exactly". This image runs at 100 MHz.
- The author's published packet records that decisions were taken:
  - `round1/HANDOFF-r1.md` lists five "Decisions needed".
  - `round4/HANDOFF-r4.md` says "The five decisions are applied".
  - `round4/REVIEW-READY.md` cites "manager decision 1".
- No owner or manager comment on #878 or #1026 records any of the following:
  - (a) the 4x4/1if point as #878 work, and its acceptance criteria;
  - (b) the 100 MHz sys/CPU clock for this image, which departs from 7097204685;
  - (c) `arty-4x4` as its own held-egress ledger point. The ruling cited, PR #1020 issuecomment-7234489667 item 3, rules the USB-network Arty, not this point;
  - (d) the bind bounds of 550 ms and 4 saves at `arty-4x4`. PR #1004's ruling covers `arty-1x1`;
  - (e) the Milan v1.2 5.4.2.7 policy of leaving unfit formats out of the advertised set;
  - (f) acceptance of the FR-CLK-05 correction pair as owed for this image.
- The only public references are the PR body's own statements and an analogy to #1020's ruling.

Impact:
- The qualification is judged against bounds and departures whose authority is private.
- No reviewer can confirm "every acceptance criterion is satisfied" (section 6, Conformance) for criteria that are not public.
- Source comments cite #878 as the authority for decisions that #878 does not contain.

Required change: the deciding party publishes the scope and acceptance criteria for the 4x4/1if point, and rulings (a) to (f). This can go on #878, on #1026, or on a new Issue that the PR links. Otherwise the PR body names the public record that carries each one.

Verification: each decision can be reached by link from the PR body, and a re-review checks the PR's claims against them.

### F2. MINOR. Tests, Robustness. The CRF output's egress term and the `arty-4x4` egress parameters are checked by no self-test

Artifact: `tb/verilator/ctrl_service_budget/egress_mii.py:69`, `:132-140` (`sr_frames`, `CRF_AVTPDU`), `:634-635` (`arty_spec`), `:663`, `:669`.

Requirement and evidence:
- AGENTS.md section 5 says to "add or update self-checking tests for changed behavior".
- Section 6 (Tests) says "Each new test can fail for the defect it claims to detect".
- Commit `e7bc55f8` adds the CRF output's 46-byte frame to the 100 Mb/s queue's SR load. That load is what the 527.04 us row of FR_NFR 3.4.1 was measured with.
- `--selftest`, `--structural` and `--packet` all take `params(arty_spec())`. `arty_spec()` is `endstation_arty_current`: one talker, no CRF output, 80 MHz. No self-test exercises the `arty-4x4` parameters, which are `(90, 90, 90, 90, 46)` bytes at 10 ns (`receipts/arith-check.log`).
- Two mutants survive every check:
  - `return aaf + crf` changed to `return aaf`;
  - `CRF_AVTPDU = 0`.
- The checks they survive are `egress_mii.py --selftest`, the six other standalone checks (`receipts/mutants.json`) and all of the service self-test's checks (`receipts/crf-mutant-service-checks.log`, rc 0; the 4x4 SR load drops to `(90, 90, 90, 90)`).
- `--packet` grades any packet at the 1x1's clock and SR load. It does not refuse a 4x4 packet.

Impact:
- The term the PR adds can be removed or zeroed with every gate green, which would quietly lighten the queue model for this point.
- A packet regrade of the 4x4 census's evidence would run at the wrong clock and load without any refusal.

Required change:
- Add a control that fails when a shape with a CRF output lacks the CRF frame, or carries it at the wrong size, in its SR load. Exercise it at the `arty-4x4` parameters.
- Make `--packet` and `--structural` either take the packet's point or refuse a packet whose point is not the 1x1's.

Verification: rerun both mutants. Each must be caught.

### F3. MINOR. Docs, Tests. The published evidence packet leaves out every indexed compressed receipt

Artifact: evidence commit `1994a795`, `review-evidence/arty4x4-r1/MANIFEST.json` (166 files, no `.gz`), `author/round3/receipts/INDEX.md`, `author/round4/receipts/INDEX.md`.

Requirement and evidence:
- AGENTS.md section 6 (Docs) requires that "The PR and Issue contain enough evidence for another cold reviewer".
- Round 4's index lists 40 compressed receipts, and none of them is published. Round 3's index lists more, also unpublished. The missing receipts include:
  - `egress_mii-census4.log.gz`, the only receipt of the 446.76 us wait and the 527.04 us row;
  - `ledger-census4.log.gz`, which holds the 1655 measured instances;
  - the 24 signoff timing and 6 utilisation reports behind the route summaries;
  - `test_builder.log.gz`, which would show gate 11's NOT RUN line. Only `test_builder.rc.txt` (0) is published;
  - the boot, region, firmware and host gate logs;
  - the service self-test partition logs.
- The census traces are kept only locally (`census4-traces-archive.sha256`).
- Several stated figures exist publicly only as prose in REPORT.md: 446.76 us, 1655 instances, 353.671 ms for the save-bind group, and the 80 MHz no-row figures.

Impact: the claims a merge rests on can be checked only as hashes and summaries. The ledger grade and the egress grade cannot be reproduced from public state.

Required change: publish the indexed compressed receipts, compressed or not, and list them in the manifest. Otherwise the packet states which receipts are withheld and why, and the PR names that limit.

Verification: every receipt row in both indexes resolves to a published file whose sha256 matches its row.

### R1. RESIDUE. Docs. Source-comment rule (owner, 2026-10-15)

Artifact: `tb/verilator/ctrl_service_budget/egress_ledger.py:102`.

The line reads `... as #1020's ruling (comment 7234489667, item 3)`. It shows an issue-comment ID in a source comment, and the instance is new in this delta.

Exact fix: replace `as #1020's ruling (comment 7234489667, item 3)` with `as #1020's ruling (item 3)`.

### R2. RESIDUE. Docs. Comments and a check label left at one Arty point and one clock

- `tb/verilator/ctrl_service_budget/shape_costs.py:57`. Replace `Arty's 80 MHz FPGA points state` with `Arty's FPGA points (the 1x1 at 80 MHz, the 4x4 at 100 MHz) state`.
- `tb/verilator/ctrl_service_budget/record_classes.py:100`. Replace `and #878's Arty point at its own 80 MHz costs.` with `and #878's two Arty points, each at its own clock's costs.`
- `tb/verilator/ctrl_service_budget/selftest_share.py:169`. This is a check label only. Replace `Arty is exactly 80,000,000 Hz` with `arty-1x1 is exactly 80,000,000 Hz`.
- `sw/builder/test_builder.py:23900-23901`. The tuple now holds four configurations. Replace `the two AX7101 shapes its bench gate qualified.` with `the two AX7101 shapes its bench gate qualified and the two Arty split images.`

### R3. RESIDUE. Docs. Unqualified Arty clock statements that the new 4x4 paragraphs now contradict

- `docs/ENDSTATION_BUILDER.md:25` and `:28`. Replace `The Arty sys/CPU clock is exactly 80,000,000 Hz.` with `The Arty 1x1 split's sys/CPU clock is exactly 80,000,000 Hz.` Replace `Their divisors are 10, 32, 16 and four respectively.` with `Their divisors are 10, 32, 16 and four respectively (the 4x4 divides sys by eight).`
- `docs/integration/BUILDING.md:361-362`. Replace `The clock ruling keeps` with `The 1x1's clock ruling keeps`.

### R4. RESIDUE. Docs. PR body and REVIEW-READY wording of the egress row

Artifact: the PR #1026 body ("100 Mb/s egress") and `round4/REVIEW-READY.md`.

The text says the 527.04 us row adds "the 300 ns fixed path measured at 100 MHz". The figure actually adds the stated 320 ns: (446.76 + 54.88) x 1.05 + 0.320 = 527.04. With 300 ns the result would be 527.02. FR_NFR 3.4.1 already words this correctly.

Exact fix: replace `plus the 300 ns fixed path measured at 100 MHz, is 527.04 us` with `plus the stated 320 ns fixed path (300.0 ns measured at 100 MHz), is 527.04 us`.

### SUGGESTIONS (optional, none affects coverage)

- S1. `record_classes.py:108`. A mutant setting `ARTY_CLOCKS['arty-4x4']` to 80 MHz survives `record_classes.py --selftest`. A 4x4 leg in the clock-refusal control would pin it.
- S2. `egress_ledger.py:110`. A mutant setting `CLOCK_KHZ['arty-4x4']` to 80,000 survives. The plant then becomes 12.5 ns rather than the 10 ns the README states. Hold the plant's cycle to the point's clock.
- S3. `docs/design/SPLIT_CONTROL_MEMORY.md`, the "Arty split 4x4/1if" subsection:
  - tabulate its stated costs, as the 1x1 subsection does;
  - say that two rows meet every rule and bound (125/5/1250 and 130/5/1000, `derive-merged234-969.json`);
  - say that the tie-break (pace, then queued bound, then slice) takes the first.
- S4. `selftest_share.py:167`. This line pins `arty-4x4` to `PRODUCT_CPU_HZ` rather than to its own clock (`arty_grade.CLOCKS`). Today the two agree.
- S5. #1022's acceptance says "4x4/1if target". It could name `arty-4x4` and its own owed records, which are 770 to 870 us here, against 495 us at the 1x1. Counted, those records leave load at 0.82 and no finite last-notice row (section 15).

## Per-lens results

### Conformance (UNCLEAN by F1)

Each of the following was checked and found clean:

- Envelope (Milan v1.2 Table 4.4 against 802.1Q 34.3.1's 75 %):
  - Egress is 4 x 7,360 + 5,632 = 35,072 kb/s.
  - Ingress is 4 x 16,576 + 5,632 = 71,936 kb/s, which is within 75,000 (`receipts/arith-check.log`).
- Entity shape, from the builder output regenerated at head (`receipts/b1-builder-4x4.log`, overlay inspected):
  - 5 STREAM_INPUT (4 AAF and CRF) and 5 STREAM_OUTPUT (4 AAF and the CRF output Milan v1.2 7.2.3 requires);
  - talker capabilities 0x4801;
  - 6 CLOCK_SOURCEs in #629's class order, with CRF at index 1 located on STREAM_INPUT 4;
  - AUDIO_UNIT [48000];
  - inputs carry the 48 kHz Base family, outputs only 2ch 48 kHz.
- Builder gates 29 and 36a on `arty_split_4x4` pass (`receipts/builder-subset.log`).
- #800 (narrow MAAP source index on 4x4) does not apply to this image: `milan_datapath.sv:388-396` builds no `KL_pp_maap_shim` or `KL_maap` at `CTRL_SPLIT_P = 1`.
- The FR-CLK-05 pair is disclosed as owed (`FR_NFR.md:299-305`, config header, `test_builder.py:29405-29410`). Its public acceptance is part of F1.

### RTL (CLEAN)

[R967] PASS RTL - `configs/generated/endstation_arty_split_4x4/gen/adp_shape_defaults.svh`, `hdl/milan/milan_datapath.sv`, `sw/firmware/ctrl/loop/ctrl_loop.h:415-427`, `ctrl_loop.c:203`, `sw/builder/endstation_builder.py:5165`, `sw/litex/milan_soc.py:292`, `receipts/lint-*.log`, `round3/receipts/routefinal-*.json` - I checked the new shape's elaboration, the scheduler row and the clock plumbing against the datapath's own shape guards and the THE SHAPES contract:
- The HDL delta is empty. The include regenerates byte-identical (`b1-builder-4x4-include-cmp.rc` 0).
- The datapath lint-elaborates with the harness's own sources and flags at N_STREAMS=4 and CTRL_SPLIT_P=1, with `-Werror-USERERROR -Werror-UNDRIVEN`: rc 0, the same 61 warnings as the all-fabric 4x4 and split 1x1 controls, and no new class.
- The CRG divides 800 MHz by 8 with `margin=0`. The builder omits `--sys-clk-freq` only at the 100 MHz default.
- `CTRL_LOOP_TX_MS` moving from 28 to 29 changes no firmware byte. Its only consumer, `srp_mbx.c:56`, rounds `(TX + 9) / 10` to 3 at both values.
- Since the routed head `a64c88bd`, the only gateware or firmware inputs that changed are that line and the gtest ratchet.
- The route receipts: ExtraPostPlacementOpt has Slow WNS +0.049 / WHS +0.156 and Fast WNS +1.606 / WHS +0.012 ns, with 0 failing endpoints, against the +0.030 floor. The other two directives reach +0.002.
- No hard-coded 80 MHz constant was found in the firmware, LiteX or HDL.

### Robustness (UNCLEAN by F2)

These were clean:
- `arty_grade.py --point` with an unknown point returns usage, rc 2 (`b1-arty-badpoint`).
- The new `egress_fixed.py SYS_HZ` option measures 312.5 ns at 80 MHz, 300.0 at 100 MHz and 285.0 at 125 MHz. A build directory reused at another clock rebuilds and does not give a stale figure (`b1-fixed-reuse-80then100.log`).
- `record_classes.point_name` refuses an Arty build with more than one interface.
- The mutants of the 4x4 row (slice, pace, queued bound, TX), its config clock and its grade clock are each refused (`receipts/mutants.json`).

F2's `--packet` pinning is the open item.

### Tests (UNCLEAN by F2 and F3)

These passed at head:
- the service self-test, 323 of 323 mutants caught with 0 failures (`receipts/st-*.log`);
- `egress_ledger --selftest`, 24 mutants including three new ones (`b1-ledger-selftest.log`);
- `arty_grade --selftest` and `--point arty-4x4` and `arty-1x1`;
- `shape_costs`, `load_grade`, `rows_tiers`, `record_classes` and `egress_mii`, both self-test and check.

Further checks:
- Of 14 lane mutants, 9 are caught. The 5 survivors are F2's two, S1, S2, and a stated cost under its measurement, which only a census can catch.
- 126 rule recomputations of the census costs, 42 merges and 38 head statements match (`receipts/costs-check.log`).
- The existing points' tables are unchanged base to head (`receipts/base-vs-head-tables.log`).

### Docs (UNCLEAN by F1 and F3)

These were clean:
- `scripts/docs_check.py`: 0 findings over 226 markdown and 1985 text files (`receipts/docs-check.log`).
- No U+2014 on added lines, and `git diff --check` is clean.
- Section 15's 4x4 tables match `egress_ledger.ARTY_4X4` and the rule.
- FR_NFR 3.4.1's 4x4 sentences match the arithmetic.

R1 to R4 are wording only.

## The focus list, item by item

| Item | Result | How |
|---|---|---|
| 4x4 configuration and per-point clocks | matches | config and include read. `arty_grade` CLOCKS and `record_classes` ARTY_CLOCKS are 100 MHz. Clock mutants are caught. |
| Route closes the floor at every corner | matches the receipts | `routefinal-graded-images.json`. The reports themselves are unpublished (F3). |
| Owner bounds: load 0.469, ACMP 28.52, txL 48.72, last 117.68, SHARE 1.733 | reproduced | `b1-arty-4x4.log`. SHARE is 173,322 cycles at 100 MHz. Costs recompute from the census cycles. |
| 100 Mb/s egress, 527.04 of 1000 us, CRF counted | arithmetic holds, CRF in the 4x4 load | The grade log is unpublished (F3). The CRF term is untested (F2). R4 covers the wording. |
| Ledger point at 63.50 ms by #878's rule | figures reproduced | The authority is not public (F1(c)). |
| Bind bounds 550 ms, 4 saves | arithmetic holds | The 353.671 ms appears only in prose (F3). The authority is not public (F1(d)). |
| FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY section 15 | consistent | See R3 and S3. |
| 1x1 and ALINX images byte-identical | consistent with the receipts | `identity-*-digests.json`: 72 entries, only `size.json` differs. Not rebuilt here (no LiteX). |
| Gate 11 NOT RUN, and why | confirmed | `test_resource_calibration` reads only `arty_current`'s v1-era place report, which is absent (`builder-subset.log`). |
| 100 MHz latency pair owed to the bench | disclosed | `FR_NFR.md:299-305`. Its acceptance is part of F1(f). |
| Comment rule | one new instance | R1. |

Prior public review findings on PR #1026: none exist. The PR carries only the two review-start comments and zero reviews, so nothing needs to be resolved or retained at this head.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN (F1) | #878 body, rulings 7096503672, 7097204685, 7097474930, 7153532537; PR #1020 7234489667; #969 7116192252; #1022; #800; config; regenerated overlay; builder gates 29 and 36a | R967-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| RTL | CLEAN | generated include; `milan_datapath.sv` split guards; lint elaboration at three shapes; `ctrl_loop.h`/`.c` row; CRG and builder clock plumbing; route receipts | R967-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Robustness | UNCLEAN (F2) | `arty_grade` and `egress_fixed` argument paths; build-dir reuse; `record_classes.point_name`; 14 mutants; `egress_mii` modes | R967-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Tests | UNCLEAN (F2, F3) | service self-test 323/323; 9 standalone self-tests and checks; 14 mutants; CRF mutant under the service checks; cost recomputation; base/head tables; builder subset (12 gates) | R967-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |
| Docs | UNCLEAN (F1, F3) | the 5 changed docs and harness README; `docs_check.py`; em dash and `diff --check`; section 15 tables against code; PR body; evidence packet manifest and indexes | R967-1 | 12ab4b189f54439cd126f677b906a19835d7f32a |

## Real limits

- Nothing was rebuilt that needs the LiteX/RV32 environment, which is not available here. That covers the product ELF identity, the 4x4 split boot simulation, native controls, the region self-test, the firmware shards and `test_ctrl_memory`. For those the author's rc receipts stand, and their logs are unpublished (F3).
- No census was rerun, and the census traces are not public. The 446.76 us wait, the 1655 ledger instances, the 353.671 ms save and the qualification's "statements equal the measured rule" are taken from summaries. The stated costs were recomputed from the published census cost receipts, not from the traces.
- No route was rerun (no Vivado run here). Timing comes from the graded JSON summaries. The reports are unpublished.
- Only a 12-gate subset of the builder suite ran, not the full suite. `test_nvm_firmware_shapes` could not run in a copy without git metadata (`receipts/nvm-selftest-copy.log`, an environment limit, not a finding).
- The builder CLI wrote `configs/generated/sweep_opts_arty.sh` into the clone. The bytes were identical, and the final fingerprint and per-blob hash check show the clone at exact head (`receipts/final-fingerprint.txt`, `receipts/blob-check.txt`).
- There was no hardware, no bench and no physical calibration. Field skips are not hardware proof.
- No hosted check run or workflow run exists for this exact head (`receipts/hosted-check-runs.txt`, `receipts/hosted-runs.json`).

## Pending manager duties

- Publish or record the decisions in F1, and the withheld receipts in F3.
- Supply the exact-head `rtl-fast` verdict and, once the PR is ready, the `verilator-suites` and `yosys-portability` evidence. None exists yet.
- Build and validate the current-dev merge candidate (source base `c0b625d1`, live dev `e275d795`) with the builder and native banks, and link those receipts. This round has no manager source bank to cite.
- The FR-CLK-05 pair at 100 MHz is owed to a board measurement.
- Carry R1 to R4 to the residue checklist.
- #1004 must land first. This branch carries it through round 11.

## Reproduction

Scripts are in `scripts/`. Set `PINNED_VERILATOR_DIR` to the directory holding the pinned 5.050 simulator, whose identity was checked as `Verilator 5.050 2026-07-01 rev v5.050`.

- `batch1.sh CLONE PACKET`
- `service_selftest.sh CLONE PACKET`
- `crf_selftest_probe.sh CLONE PACKET`
- `dp_lint.sh CLONE TREE PACKET`
- `python3 -I mutants.py CLONE WORKDIR OUT --jobs 6`
- `python3 -I costs_check.py ROUND3_RECEIPTS CLONE`
- `python3 -I arith_check.py CLONE`
- `python3 -I base_vs_head.py BASE_TREE CLONE`

In the receipts, host paths are redacted to `$PACKET`, `$CLONE`, `$HOME` and `$PINNED_VERILATOR_DIR`.

R967-1 FINISHED

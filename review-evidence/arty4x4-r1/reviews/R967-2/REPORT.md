[R967] POSITIVE - exact head 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e

Round R967-2. This is the internal, independent re-review of kebag-logic/milan-fpga PR #1026 against its task contract, issue #1027. It ran in a cleared context.

- Head `47f2a3d7ffdf7ef701c69267a91ac92892a1c99e`, tree `998ce7dd057cc9947b3db4bbdf3dd6f20acf75ef`.
- Reviewed delta: the seven commits `12ab4b189f..47f2a3d7ff` (16 files, +349/-105), judged against the previously reviewed head `12ab4b189f`. Code that this delta does not touch keeps its round-1 lens verdict, unless the delta changes something that code depends on.
- Full lane delta for context: `c0b625d1792e61b8e99944daea65b842e6b9dcde..47f2a3d7ff` (28 files, 22 lane commits, two merges of #1004).
- Evidence packet: `review-evidence/arty4x4-r1/author-r5` at evidence commit `117bd43f1cb642326123e7d426cc8f34174043f6`, https://github.com/kebag-logic/milan-fpga/tree/117bd43f1cb642326123e7d426cc8f34174043f6/review-evidence/arty4x4-r1
- Lenses applied: Conformance, RTL, Robustness, Tests, Docs.

**Verdict: POSITIVE.** No BLOCKER, MAJOR or MINOR finding is open at this head. Every prior finding was checked at its cause:
- this reviewer's round-1 F1 to F3;
- the external round-1 review's F1 to F5.

Each is closed at its stated outcome, and each new control was falsified with my own planted defects. The four RESIDUE items below are wording only. The SUGGESTIONS are optional.

## What was established

- **Task contract.** #1027's body holds the following, and the PR body, source comments and docs now cite #1027:
  - the scope: 4x4/1if with the CRF output on 100 Mb/s;
  - eight acceptance items;
  - decisions 1 to 5: 100 MHz clock, own ledger at 63.50 ms, bind bounds 550 ms / 4 saves, the formats policy under Milan v1.2 5.4.2.7, and the correction pair owed to the bench.
- **CRF frame in the 100 Mb/s stream load.**
  - `egress_mii.py --selftest` passes 35 of 35 (`receipts/egress_mii_selftest.log`). It runs eleven controls at each of `arty-1x1` and `arty-4x4` and catches all thirteen plants.
  - The four CRF plants are each caught by an `[arty-4x4]` control, not only at the 1x1.
  - My mutants, planted in source, are each caught with rc 1 (`receipts/mutants.json`):
    - M1 `return aaf`;
    - M2 `CRF_AVTPDU = 0`;
    - M3 `crf = ()`;
    - M4 a 68-octet AVTPDU (six timestamps a PDU);
    - M11 `STREAM_LOAD` restated without the 46.
  - The 28-octet AVTPDU matches the RTL and configuration: `hdl/ieee1722/crf/KL_crf_tx.sv:17`, `KL_crf_rx.sv:17-18` and `configs/endstation_arty_split_4x4.yaml:132-136`, which give one timestamp a PDU at interval 96 (Milan v1.2 7.3.2, Table 7.1).
- **Record-class gate at arty-4x4.**
  - `record_classes.py --selftest` passes: 26 of 26 controls and 26 of 26 Arty checks.
  - Each of these mutants is refused by its own named check (`receipts/mutants-record.json`):
    - M5: `point_name` maps the 4x4 configuration to `arty-1x1`. Escapes "endstation_arty_split_4x4 is named to arty-4x4".
    - M6: `ARTY_CLOCKS['arty-4x4']` is 80 MHz. Escapes "arty-4x4 record classes accept their complete 100 MHz fixture".
    - M7: `poll_grade.record_us` reads `arty-1x1`'s ACMP cost at (1,5,5). Escapes "...reads arty-4x4's ACMP record cost, 210 us".
  - The fixture arithmetic holds under `rule()`, which takes the time at the CPU clock, adds 5 % and rounds up to 5 us:
    - 22,500 cycles at 100 MHz gives 240 us, over the 225 us statement;
    - 20,000 cycles at 100 MHz gives 210 us, which fits;
    - 20,000 cycles at 80 MHz gives 265 us, which does not.
- **Ledger's planted cycle at each point's clock.**
  - `egress_ledger.py --selftest` refuses all 26 mutants. Both new clock mutants are caught by "one cycle over a figure is planted at the point's own bus cycle".
  - The same defect, planted in source as M8 (`CLOCK_KHZ['arty-4x4']` = 80,000), gives rc 1.
- **Fixed-path bench.** Run as its usage line states, under `python3 -I` with the pinned Verilator 5.050 (`Verilator 5.050 2026-07-01 rev v5.050`):
  - `BUILD_DIR` gives "PASS: the most is 312.5 ns, stated 320 ns", rc 0;
  - `BUILD_DIR 100000000` gives "the most is 300.0 ns, within the stated 320 ns", rc 0;
  - `BUILD_DIR 99999999` gives the usage text, rc 2.
  - `--selftest` passes 11 controls and catches 3 of 3 mutants. My M9 (whole-ps check removed) and M10 (`over()` never over) are each caught.
- **Regradeable census-4 evidence.**
  - Packet integrity: all 827 `author-r5` files match `MANIFEST.json`'s `published_sha256`, and no file is unlisted. All 822 `receipts.json` rows match on size and sha256 (`receipts/packet-verify.log`).
  - The census-4 extract is 334 data files plus `FILES.json`.
  - My regrade at this head reproduces "EGRESS100 wait 446.760 us + gPTP 54.88 us, x 1.05, + fixed 0.32 us = 527.042 us ... most records queued at once 35", with "RESULT: PASS cases=159".
  - My 159 per-case grades equal the published `checks/g-full.txt` and `checks/g-ext.txt` as multisets (`receipts/g-compare.log`).
  - `egress_ledger.py --point arty-4x4 EXTRACT/*/results` reads "1655 instance(s) ... (1655 measured)". Its result is PASS and is byte-identical to the published log.
- **Images.** The packet's `gates5/identity-head-digests.json` has 72 entries, against `identity-base-digests.json` at base `aa53840d9`:
  - every builder output and all three existing product `ctrl_app.elf` files are identical;
  - only the three products' `size.json` sidecars differ, and those carry the `.map` file's hash (see S7).
  - The only configuration change in the delta is the 4x4 YAML's header comment (`#878` to `#1027`).
- **Docs gates.**
  - I ran these at the head:
    - with the pinned Markdown venv, whose versions match `tools/markdown/requirements.txt`: `gen_toc.py --check`, `--verify-anchors` and `--selftest`, and `check_em_dash.py` against both `aa30d77f` and `12ab4b18`;
    - `docs_check.py`, `check_doc_style.py`, `check_doc_paths.py`, `check_py_idiom.py` and `git diff --check`.
  - All pass. The author's system-Python run shows four rc-2 lines, all four renderer-dependent. `REVIEW-READY.md` explains them, and they pass here (`receipts/docs-md.rc.txt`).
- **Comment rule.** No source line this delta adds carries a bench lane label, lane name, review round, reviewer ID or issue-comment ID.
- **Clone restored.** HEAD and `write-tree` both equal the stated head and tree. 2010 tracked blobs are byte-identical, the six gitlinks are unchanged, and no untracked or ignored file remains: the `__pycache__` directories my probes created were removed (`receipts/restore-check.log`).

## Prior findings at this head

| Prior finding | Stated outcome | At 47f2a3d7 | Evidence |
|---|---|---|---|
| Internal F1 (MINOR, Conformance/Docs): no public task contract or decisions | Scope, acceptance and rulings (a)-(f) public and reachable from the PR | CLOSED | #1027 body: (a) scope and acceptance; (b) decision 1; (c) decision 2; (d) decision 3; (e) decision 4; (f) decision 5. The PR body links #1027 and lists all five. `SPLIT_CONTROL_MEMORY.md:3634-3641,3684,3686`; `egress_ledger.py:101-103`; `run.py:39`; the YAML at line 1. |
| Internal F2 (MINOR, Tests/Robustness): CRF term and 4x4 egress parameters untested; `--packet` at 1x1 only | CRF control at 4x4; `--packet`/`--structural` take or refuse the point | CLOSED | M1, M2, M3 and M11 caught. `egress_mii.py:640-655` (`load_controls`) and `:706-725` (`--point`). An unknown point gives rc 2 (`receipts/cli-badpoint.log`). A log of the other point's queue is refused by its own control at each point. |
| Internal F3 (MINOR, Docs/Tests): indexed compressed receipts unpublished | Receipts published or withholding stated | CLOSED | `receipts/earlier/` (218 files) extracts every round-1, 3 and 4 `.gz`. `INDEX.md` maps each `.gz` to its content sha256. The census-4 extract regrades both figures. The traces themselves (0.4 to 0.5 GB per census) are withheld, and `INDEX.md` says so. |
| Internal R1 (RESIDUE) | Drop the comment ID | FIXED | `egress_ledger.py:101-103` |
| Internal R2 (RESIDUE) | Four comment and label fixes | FIXED | `shape_costs.py:57-58`, `record_classes.py:100`, `selftest_share.py:170-171`, `test_builder.py:23900-23901` |
| Internal R3 (RESIDUE) | Qualify the 1x1 clock statements | FIXED | `ENDSTATION_BUILDER.md:25,28`, `BUILDING.md:361` |
| Internal R4 (RESIDUE) | The PR body's 320 ns wording | FIXED | The PR body's "100 Mb/s egress" paragraph |
| Internal S1-S4 (SUGGESTION) | Optional | ADOPTED | S1 caught as M6; S2 caught as M8. S3: the table (`SPLIT_CONTROL_MEMORY.md:3657-3670`) equals `ctrl_loop.h:416-427`, and the two rows equal `derive-merged234-969.json` (`receipts/derive-two-rows.log`). S4: `selftest_share.py:168`. |
| Internal S5 (SUGGESTION, #1022 wording) | Optional, outside this PR | RETAINED, optional | n/a |
| External F1 (MINOR, Tests): CRF frame has no control | Control at a CRF shape with plant | CLOSED | As internal F2: M1 to M4 and M11 |
| External F2 (MINOR, Tests): record-class 4x4 branches have no control | Its M8, M9 and M10 each caught (my M5, M7 and M6) | CLOSED | `record_classes.py:453-549`. Each mutant escapes a distinct named check. |
| External F3 (MINOR, Tests/Docs): `egress_fixed.py` cannot run under `-I`; SYS_HZ untested | The documented invocation runs; the report path is tested | CLOSED | `egress_fixed.py:27-30` puts its own directory on the import path. `receipts/fixed_80.log` and `fixed_100.log` give rc 0. `--selftest` passes; M9 and M10 are caught. |
| External F4 (MINOR, Docs/Conformance): scope and decisions not public; (d) packet unlinked | Decisions public; packet linked | CLOSED (a)-(c); (d) wording carried as RES3 | #1027. Item (d) asks only for a PR-body link, recorded as RES3. |
| External F5 (MINOR, Docs): named receipts unpublished | Receipts or regradeable extracts public at a linked evidence commit | CLOSED (substance); link carried as RES3 | As internal F3. Regrade reproduced. |
| External R1-R4 (RESIDUE) | Wording fixes | FIXED | `egress_ledger.py:101-103`; `shape_costs.py:57-58` and `selftest_share.py:170-171`; the PR body's 320 ns wording; `README.md:264`, which now carries the CRF frame |
| External S1, S2 (SUGGESTION) | Optional | ADOPTED | SYS_HZ `0` gives the usage text and rc 2 (control). Section 15 is retitled "Arty split points", and all three anchors were updated (`gen_toc --verify-anchors` passes). |
| External S3 (SUGGESTION): link the 4x4 qualification in the README | Optional | RETAINED, optional | `README.md:232` links the 1x1's only |

## Findings at this head

No BLOCKER, MAJOR or MINOR.

### RES1. RESIDUE. Docs. `docs/design/SPLIT_CONTROL_MEMORY.md:3634-3635`: "the decisions below (its decisions 1 to 5)"

- Authority and evidence: section 15 states and cites only decisions 1, 2 and 3 (lines 3639, 3684 and 3686).
- Decision 4, the advertised formats, is stated in `ENDSTATION_BUILDER.md`, and decision 5, the owed correction pair, in FR_NFR FR-CLK-05 (`FR_NFR.md:299`). So "below" over-claims.
- Impact: a reader looks in section 15 for decisions 4 and 5 and does not find them.
- Exact fix: replace `its scope, its acceptance and the decisions below (its decisions 1 to 5), beside` with `its scope, its acceptance and its decisions 1 to 5 (1 to 3 below; 4, the advertised formats, in ENDSTATION_BUILDER.md; 5, the owed correction pair, in FR_NFR FR-CLK-05), beside`.
- Verification: rerun `gen_toc.py --check` and `check_em_dash.py`.

### RES2. RESIDUE. Docs. PR #1026 body, "Stacked on #1004": "28 files in 21 commits"

- Evidence: `git rev-list --count --no-merges c0b625d1..47f2a3d7` gives 22, which is 15 at round 1 plus 7 in this round. Both that count and `--first-parent` say 22, and there are two merges.
- Exact fix: replace `28 files in 21 commits` with `28 files in 22 commits and two merges of #1004`.

### RES3. RESIDUE. Docs. PR #1026 body: the round-5 evidence packet is not linked

- Evidence: the PR body's "Regradeable evidence" paragraph names `EXTRACT/*/`, but neither the PR body nor any PR or #1027 comment links the evidence commit `117bd43f` or `review-evidence/arty4x4-r1/author-r5`. External F4(d) and F5 asked for "an evidence commit linked from the PR".
- Impact: a cold reader cannot find the extract from the PR. The evidence itself is public and verified.
- Exact fix: add to the PR body: `Evidence packet: [review-evidence/arty4x4-r1/author-r5 at 117bd43f](https://github.com/kebag-logic/milan-fpga/tree/117bd43f1cb642326123e7d426cc8f34174043f6/review-evidence/arty4x4-r1/author-r5); the extract is receipts/census4-extract.`
- Publishing this report, which links the packet, also puts the link on the PR.

### RES4. RESIDUE. Docs. `tb/verilator/ctrl_service_budget/README.md:269`: "**At the Arty**"

- Evidence: with two Arty points, this bullet's figures (426.47 us, 505.74 us, 19 records) are the 1x1's alone. The bullet above it, `:268`, now describes both points.
- Exact fix:
  - Replace `**At the Arty**, over the 159-case link-rate census,` with ``**At the Arty 1x1** (`arty-1x1`), over the 159-case link-rate census,``.
  - Optionally append: `At arty-4x4 the largest wait is 446.76 us (answering-every-port/notice-every-1) and the row is 527.04 us; at most 35 records queue at once.` FR_NFR 3.4.1 already states these figures, and my regrade reproduces them.

### SUGGESTIONS (optional; none affects coverage)

- **S1. `egress_fixed.py:104`.** `import contextlib` is repeated inside `controls()`, although line 22 already imports it at module level. Drop the inner import.
- **S2. Packet `checks/g-full.txt` and `g-ext.txt`.** These are keyed by case stem without the variant: 152 distinct keys for 159 cases. So per-case identity is provable only as a multiset. Key each line by `variant/case`, as the grader prints it.
- **S3. Section 15's stated-cost tables.** Neither table is held by a self-test against `ctrl_loop.h` THE SHAPES: the 1x1's at `SPLIT_CONTROL_MEMORY.md:3555-3573`, nor the new 4x4 one at `:3657-3670`. Both are correct today. `arty_grade.py --selftest` could hold them, as `egress_ledger` holds its tables.
- **S4. `egress_ledger.py:116-122`.** `config_khz` reads `sys_clk_hz` with a regex, while `egress_mii.point_spec` reads it with YAML. A `100_000_000` spelling would be misread, though the check would fail loudly. Reading it with YAML keeps one parser.
- **S5. `egress_mii.py:568`.** At `arty-1x1`, `crf-frame-not-queued` (`sr_bytes[:-1]` of `(90,)`) removes the AAF frame, not a CRF frame, so its 1x1 catches test a different defect from the plant's name. The 4x4 catch is genuine. A plant that removes only the `SR_HEADER + CRF_AVTPDU` frame would match its name at both points.
- **S6. #1027 body.** It does not yet carry every AGENTS.md section 4 field: executor and reviewer, out-of-scope work, the exact validation method, and dependencies. The executor tag and the PR's review-start comments cover the roles publicly. This is a manager-owned field.
- **S7. Identity receipt.** Say why the three existing products' `size.json` sidecars differ from base while their ELFs are identical. The sidecar includes the `.map` file's sha256, and the map is probably path-dependent. That cause is unverified here, because the base sidecars are not published.

## Per-lens results

- **Conformance: CLEAN.** I checked:
  - #1027's acceptance and decisions against the PR body and the docs;
  - the 28-octet CRF AVTPDU against `KL_crf_tx.sv:17` and `KL_crf_rx.sv:17-18` and the YAML's Table 7.1 format (Milan v1.2 7.3.2, one timestamp a PDU);
  - `STREAM_LOAD` (`egress_mii.py:77`) against the 18 + 24 + 2 x 6 x 4 = 90-octet AAF frame;
  - the egress row, 527.04 us of 1000 us, reproduced from the published extract;
  - the ledger, 1655 instances, all within their figures, reproduced;
  - the two qualifying rows, reproduced from `derive-merged234-969.json`.
- **RTL: CLEAN.** This delta changes no HDL, LiteX, mailbox or firmware source:
  - `git diff --stat 12ab4b18..47f2a3d7` lists only the YAML header comment, docs and harness Python;
  - `ctrl_loop.h:415-427` is unchanged since round 1, where this lens was clean;
  - the ELF digests are identical to base, and the 4x4 ELF equals the routed image's (`gates5/identity-head-digests.json`).
- **Robustness: CLEAN.** I checked:
  - the `egress_fixed.sys_period` refusals (`:57-61`, `:73-75`) of `0`, `-1`, `abc`, `3` and `1e8` (control) and `99999999` (real run, rc 2);
  - `egress_mii --point nosuch`, which gives rc 2;
  - the refusal of the other point's queue log at each point (`load_controls`);
  - `config_khz`'s refusal of a configuration that does not state `sys_clk_hz` exactly once (`egress_ledger.py:119-121`).
- **Tests: CLEAN.** Each new control was shown to fail for its defect:
  - M1 to M11 are all caught (`receipts/mutants.json`, `receipts/mutants-record.json`), with an unmutated baseline at rc 0 for each self-test;
  - every focused self-test passes at the head: `egress_mii` 35/35, `egress_fixed` 11 controls and 3/3 mutants, `egress_ledger` 26 mutants, `record_classes` 26 and 26, `arty_grade` 6/6, `shape_costs --check` and `--selftest` 25/25.
  - The service self-test's new clock label passes in all eight author partitions (`gates5/service-selftest-*.log`).
- **Docs: CLEAN.** RES1 to RES4 are wording only and leave the lens clean. I checked:
  - `README.md:261,264,267-268`, `FR_NFR.md:299,520-521`, `SPLIT_CONTROL_MEMORY.md:28,3493,3634-3690`, `ENDSTATION_BUILDER.md:15,25,28,39` and `BUILDING.md:361,375` against the code and the receipts;
  - every figure: 431.12 us, 2.42 ms, 2.71 ms, 35 records, 312.5/300.0 ns, eleven controls, thirteen plants, 26 mutants;
  - the docs gates listed above, all passing.

## Reviewer-owned ledger

| Lens | Result | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #1027 body; PR body; `egress_mii.py:68-77,140-148`; `KL_crf_tx.sv:17`; `KL_crf_rx.sv:17-18`; YAML `:63,:132-136`; regrade of `census4-extract` (527.042 us, 1655 instances); `derive-merged234-969.json` | R967-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| RTL | CLEAN | delta file list (no HDL, LiteX, mailbox or firmware change); `ctrl_loop.h:415-427`; `gates5/identity-head-digests.json` against `identity-base-digests.json` | R967-2 (delta); R967-1 for the untouched RTL | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Robustness | CLEAN | `egress_fixed.py:57-61,73-75`; `egress_mii.py:706-725`; `egress_mii.py:651-654`; `egress_ledger.py:116-122`; `receipts/fixed_bad.log`, `cli-badpoint.log` | R967-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Tests | CLEAN | `egress_mii.py:565-672`; `record_classes.py:453-549`; `egress_ledger.py:410-418,486-490`; `egress_fixed.py:91-171`; `selftest_share.py:164-172`; mutants M1-M11 with baselines | R967-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |
| Docs | CLEAN (RES1-RES4 carried) | `README.md:5,48,227,258-269`; `FR_NFR.md:299,520-521`; `SPLIT_CONTROL_MEMORY.md:28,3493,3631-3690`; `ENDSTATION_BUILDER.md`; `BUILDING.md`; PR body; packet `INDEX.md` and `MANIFEST.json`; docs gates | R967-2 | 47f2a3d7ffdf7ef701c69267a91ac92892a1c99e |

## Real limits

- No manager source bank runs at this head, and none is claimed or inferred. The author's published gate receipts are the source-head execution evidence:
  - `gates5/harness5.rc.txt`, every entry rc 0;
  - `gates5/test_builder.log`, "ALL GATES PASS EXCEPT 1 NOT RUN", where gate 11's oracle report is not on disk;
  - the service self-test, 8 partitions at rc 0.
- I did not rerun the service self-test, the builder suite, the boot or region simulations, the firmware shards, or any route. Their verdicts rest on the author's receipts. The firmware shards, 1x1 boot, region self-test, `test_ctrl_memory`, host arms and coverage ratchet last ran at `12ab4b18`, as `REVIEW-READY.md` states. This delta changes no file they read, apart from the YAML comment.
- The census-4 extract is bound to its full logs only by `FILES.json` hashes. The full traces are withheld, so the extract-to-trace binding cannot be checked from public state. The regrade itself is independent.
- The evidence commit `117bd43f` is unsigned (`verification.reason: unsigned`). Its integrity was checked by content hashes against `MANIFEST.json` and `receipts.json`, not by a signature.
- No hosted check-run, status or workflow run exists for this exact head (`receipts/hosted-checks.txt`), and no hosted evidence is claimed.
- Physical calibration is NOT RUN. The correction pair at 100 MHz and the 4+4+CRF bench session are owed to the board (#1027, decision 5 and the last acceptance item), and no field skip is hardware proof.
- The route figures (+0.049/+0.156 ns, +1.606/+0.012 ns) come from the author's published reports. I did not reroute.

## Pending manager duties

- Carry RES1 to RES4 to the residue checklist. RES2 and RES3 are PR-body edits.
- At the merge turn, build and validate the current-dev merge candidate: source base `c0b625d1792e61b8e99944daea65b842e6b9dcde`, live dev `e275d7950ef3385753e6a15d2e191ba855b171ed`. Run the builder and native banks there, and link their receipts on the PR.
- Own hosted and act acceptance. The PR is draft, so the exact-head hosted gates start only when it is marked ready.
- #1027's two unticked bench items remain open: the 4+4+CRF session and the correction pair at 100 MHz. They need explicit disposition before #1027 closes.
- Merge only with explicit maintainer authorization, after #1004 lands and after the second independent positive review.

## Receipts

Every receipt is listed in `MANIFEST.sha256`. Host paths in the fixed-path logs are replaced by `$SCRATCH`, `$CLONE`, `$TOOLS` and `$VERILATOR_IMAGE`. `mutants.py` is the portable mutation driver:

```
python3 -I mutants.py CLONE WORK OUT.json [M1 ...]
```

It archives HEAD, copies the checked-out submodules, and plants each mutant in a hard-linked copy.

R967-2 FINISHED

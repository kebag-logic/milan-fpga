[R493] POSITIVE - exact head 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783

R493-2 is the external independent delta review of issue #640 / PR #698. All five lenses are CLEAN. No BLOCKER, MAJOR or MINOR remains. Two presentation-only RESIDUE items remain below.

Reviewed tree: `2f8dac43d7c0efd0350b328818d89dc1cbebca47`. Full comparison: `5603c353137e90c1fa95429f6d00ef7a2298d9ee..7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`. Focused delta: `c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970..7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783`. Only `docs/design/MARK_II_AREA_PLAN.md` and `docs/design/AREA_BUDGET.md` change. History includes the assigned merge and additive round-1c/1d commits. No implementation, resource-record or policy value changes.

This approves the stage-1 plan, not #640's eventual hardware acceptance. The [issue](https://github.com/kebag-logic/milan-fpga/issues/640), [stage assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5988586965), [round 1c ruling](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081534590), [memory decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081706413) and [round 1d assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081895732) establish that scope. No routed Mark II fit, target timing or physical acceptance is granted.

I reconstructed the contract, documentation index, issue decisions, requirements and interfaces before examining the diff and evidence. The [independent verdict and ledger](receipts/independent-pass.md) were written before reading either prior public review. Prior findings were then checked individually. No private author material or other review packet was used. Submitted and inline reviews were empty; prior findings appeared in the two public conversation comments.

**Requested focus**

| Item | Result and exact-head artifacts |
|---|---|
| M0s and D7 | [Plan:966][lanes], plan:983-1027 and [budget:336][budget-order] assign the manager's resource bench. Reviewed tooling precedes the partial F0-F4 route; the full route follows F5 integration. Both precede week 4 and the default flip. Week-3 integration and later qualification are distinguished. D7 uses M0s placement figures against the accepted record, with later deltas separately visible. Missing measurements cannot pass. |
| M8a basis | [Plan:573][m8] and budget:204 identify 823 + 873 pre-packing LUT cells and 3,231 anonymous cells. The remainder earns no credit. Explicit packing and replacement assumptions reprice M8a to 1,000 LUTs, range 400-1,500. Both ledgers agree. These remain estimates. |
| Alternative placements | [Plan:875][fallback] and budget:288 include M3/M10 in no-split pricing and price F5-unqualified placement. Retained AECP, notification, originator and NVM costs are explicit. Both bars, core-revert cases and the required further redesign/ruling are stated. F5 qualification removes overlapping M3/M10 credits. |
| Firmware memory | [Plan:697][memory] and budget:222 include 224 KB/about 50 tiles, both preflight sizes, base primitives, historical memory reuse, additions and reserve. Exact disjoint stores are named for conditional reclamation. Both M0s routes, the flip and M9 report actual allocations. Packing, extra buffers, partial placement and lost conversion savings remain explicit obligations. |
| Reproduction and M2 | [Plan:1136][recipe] supplies source digests, source selection, arguments and serialized execution instructions. Shell syntax and three Tcl traces pass without synthesis. [Plan:450][m2] names packet, MAC crossing and CSR AW/W/B/AR/R FIFOs; it excludes DDR3 and overlapping bridges and grants no credit for already-converted storage. |
| Prose and checks | Named linking fixes are present; history is qualified. All 16 focused checks pass. Sentence-length residue and one table separator remain. |

**Independent arithmetic**

[recompute_ledger.py](scripts/recompute_ledger.py) reads the committed records and both pages. It passed [138 comparisons](receipts/recompute.log): endpoint metrics/input digests, current inventory, disjoint scopes, M8a census/rounding, M3 weighting, cumulative figures, both copies of scenario rows, memory partition and reserve arithmetic. Baseline bytes equal the assigned base's record.

| Placement | Conservative LUT | Central LUT | Optimistic LUT | Central headroom to 38,040 / 37,659 |
|---|---:|---:|---:|---:|
| Complete split | 35,867 | 31,667 | 27,567 | +6,373 / +5,992 |
| No split, including M3/M10 | 44,967 | 41,867 | 38,467 | -3,827 / -4,208 |
| Partial split, F5 unqualified | 43,557 | 37,957 | 32,557 | +83 / -298 |

Full-split gross reference: 18,107 LUTs. Mailbox debit: 3,102, plus estimated integration/mapping costs. Partial removal basis: 8,012; central partial saving: 3,910. Remaining M lanes total 4,600 centrally. Retained-fabric M3/M10 add 3,800 only in alternative placements. Without M8b, conservative full split is 37,167; central partial is 39,657.

The baseline is the stored `a5ca6e51` measurement, not a new measurement at this head: 50,267 LUT, 54,413 FF, 74 RAMB36 and 27 RAMB18, or 87.5 tiles. Standalone records contain 23,179 and 30,135 LUTs. The +0.299 ns setup record implies +0.049 ns under the fall tolerance; the absolute floor stays +0.030 ns. The record leaves 71 slices and 34 tiles below the policy ceiling.

Memory arithmetic: `87.5 - 6.5 + 6 - 18.5 + 50 + 2 = 120.5` tiles. Historical CPU-memory reuse of 18.5 tiles needs confirmation. The disjoint eleven-tile wrapper release gives 109.5. A 56-tile firmware mapping gives 115.5 after release. Without reuse, totals become 139 and 128, exceeding 121.5. Partial placement with the same firmware hold reaches 126.5 before extra staging. The plan reports these failures and withholds full-split credits from partial placement.

The [F5 preflight](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081556432) reports 94,688 B shipping and 147,360 B for the largest two-interface fixture, before AECP. Listed sections and stack total 147,342 B; alignment accounts for 18 B. Static pools are already in BSS. These are sizing fixtures, not completed F5 or mapped-memory proof. The plan preserves the [checkpoint duties](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916).

**Prior finding dispositions**

Sources: [R492-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081481326) and [R493-1](https://github.com/kebag-logic/milan-fpga/pull/698#issuecomment-6081524243). Original finding lenses are preserved. Suggested-item lenses below describe this review's coverage.

| ID | Severity / lenses | Disposition at this head |
|---|---|---|
| R492-1-F1 | MINOR; Conformance, RTL, Robustness, Tests, Docs | RESOLVED: M0s table, sequence, tooling prerequisite and D7 comparison agree; plan:966,983-1027; budget:336-356. |
| R492-1-F2 | MINOR; Conformance, RTL, Docs | RESOLVED: correct units, anonymous remainder, repriced M8a and recomputed ledgers; plan:573-599; budget:204-217. |
| R492-1-F3 | MINOR; Conformance, RTL, Robustness, Docs | RESOLVED: inclusive no-split and partial scenarios, both bars and shortfall disposition; plan:875-951; budget:288-330. |
| R492-1-R1 | RESIDUE; Docs | RETAINED: many sentences shortened; changed memory prose still exceeds ten words. R493-2-R1 carries concrete fixes. |
| R492-1-R2 | RESIDUE; Docs | RESOLVED for identified issue/path references. Links are present; path/anchor checks pass. |
| R492-1-R3 | RESIDUE; Docs | RESOLVED: plan:153,173-174,1118-1121 qualify the older record and slice statements as history. |
| R492-1-R4 | RESIDUE; Docs | RESOLVED: redundant separator before the historical re-baseline paragraph removed. |
| R492-1-S1 | SUGGESTION; Docs, Tests | RESOLVED: plan:1136-1230 supplies exact reproduction. Checked syntax/arguments, not historical synthesis. |
| R492-1-S2 | SUGGESTION; RTL, Docs | RESOLVED: plan:450-481 names surviving FIFOs and exclusions; checked against SoC wiring. |
| R493-1-R1 | RESIDUE; Docs | RETAINED as a category: both requested replacements are present at plan:830-837 and budget:168-169. Remaining/new long prose becomes R493-2-R1. The new table has separator residue R493-2-R2. |
| R493-1-R2 | RESIDUE; Docs | RESOLVED for all identified examples: plan:3,9,418-419 and budget:143,152 link their authorities/files. |

**Current findings**

**R493-2-R1 | RESIDUE | Docs | plan:700,812; budget:265 | Long changed prose remains.**

Authority/evidence: `docs/README.md`, Documentation rules, requires sentences under eleven words. These changed sentences exceed that bound. The built-in style gate omits both pages. [Screening output](receipts/changed-sentence-audit.txt) supplies additional candidates; its line-based results need manual interpretation for multiline prose and links containing code.

Impact: readability only. No figure, measurement, acceptance condition, conformance claim or privacy rule changes.

Required outcome and exact fixes:

- Replace plan:700 with: `The [F5 ruling](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6081705916) sets the linked-image limit at 224 KB.` Then: `That includes AECP.`
- Replace plan:812 with: `The default flip requires firmware in block RAM.` Then: `The reserve must remain intact.`
- Replace budget:265 with: `Five RX pools, MRP strip and TX slots give way.` Then: ``So do timer, trace, RX validator and `ctl_fifo`.``
- Carry repeated long-prose observations from both prior reviews to the residue checklist. Split confirmed long sentences to ten words or fewer, preserving every number, link and qualification.

Verification: inspect rendered prose and counts; preserve ledger and qualification claims.

**R493-2-R2 | RESIDUE | Docs | plan:837-838 | Missing blank line absorbs prose into the M3 table.**

Authority/evidence: the [rendered fragment](receipts/m3-table-render.html) places “That displaces about 3,380 LUTs.” and following narrative in extra table rows. All arithmetic and conditions remain visible and unchanged.

Impact: presentation only; no numeric or behavioral defect.

Required outcome and exact fix: insert one blank line after `| AECP dispatch queue | 421 | 40 percent |`, before `That displaces about 3,380 LUTs.`

Verification: [prose_probe.py](scripts/prose_probe.py) reproduced the defect and verified that the separator restores paragraphs. The [corrected rendering](receipts/m3-table-fixed-render.html) retains every word and figure. No source edit or committed generated-artifact change occurred.

Both findings qualify as RESIDUE under the assigned owner rule. Neither leaves a lens unclean.

**Reviewer-owned completion ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | #640 acceptance/decisions; REQUIREMENTS.md:22; FR_NFR.md:464; plan:64,573,697,875,953; budget:156,336. Targets, ownership and qualification preserved. | R493-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| RTL | CLEAN | full.diff; milan_soc.py:805,1612,1672,2556; milan_datapath.sv:8003; plan:450,571,769; resource scopes. FIFO, ownership and memory claims checked; no RTL change. | R493-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Robustness | CLEAN | Plan:714,722,760,796,875,983; budget:222,288; recompute.log. Packing, failed reuse, partial qualification, core reversal, delayed F5, missing measurements and primitive-growth policy checked. | R493-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Tests | CLEAN | gates/results.json; resource self-test/mutation logs; recompute.log; recipe.log; readiness 6082152872; full.diff. Focused checks pass; physical obligations remain. | R493-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |
| Docs | CLEAN | Both pages; docs/README.md rules; #649 census:262-287; MAILBOX_SPLIT.md:934-948; linked decisions; gates and M3 rendering. R1/R2 are residue only. | R493-2 | 7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783 |

**Execution and reproduction**

[run_focused.py](scripts/run_focused.py) ran 16 checks with eight concurrent lightweight workers, waited for all children, and retained separate logs/return codes. [All returned zero](receipts/gates/results.json). Coverage includes documentation/privacy, no-Git fallback, style/controls, paths, feature status, archive integrity, contents/anchors/controls, added-line punctuation/controls, baseline policy and resource refusal controls. The resource self-test passed 260 arms and 500 generated cases. Its control passed and all 174 mutants failed as expected. This is a focused campaign, not a full implementation bank.

Set `REPO` to an exact-head clone and `PACKET` to this directory:

```sh
rtk proxy python3 -m venv "$PACKET/scratch/markdown-venv"
rtk proxy "$PACKET/scratch/markdown-venv/bin/python" -m pip install --require-hashes -r "$REPO/tools/markdown/requirements.txt"
rtk proxy python3 "$PACKET/scripts/run_focused.py" "$REPO" "$PACKET/receipts/gates" --python "$PACKET/scratch/markdown-venv/bin/python" --jobs 8
rtk proxy python3 "$PACKET/scripts/recompute_ledger.py" "$REPO"
rtk proxy python3 "$PACKET/scripts/check_recipe.py" "$REPO" "$PACKET/scratch/recipe"
rtk proxy "$PACKET/scratch/markdown-venv/bin/python" "$PACKET/scripts/prose_probe.py" "$REPO" "$PACKET/receipts"
rtk proxy python3 "$PACKET/scripts/verify_checkout.py" "$REPO"
```

The [author's exact-head receipt](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6082152872) reports 51/51 commands. The [specified evidence tree](https://github.com/kebag-logic/milan-fpga/tree/994453e98aa8cea39e06534115ebebb258136767/review-evidence/640-r1) holds the older round-1b receipt, whose published digest was checked. It does not hold the round-1d raw logs or arithmetic scripts. Those author outcomes are attributed, not independently rehashed or represented as this review's execution. This packet provides independent scripts and raw focused receipts. No manager source bank exists at this head, and none is inferred.

The [hosted snapshot](receipts/hosted-jobs.json) names this exact head. Some jobs executed successfully; documentation, elaboration, firmware and long simulation jobs were still running. The physical job was skipped. No completed aggregate verdict is claimed. Hosted and local-replica acceptance remain manager duties; this reviewer ran no replica and did not poll for acceptance.

**Limits and pending manager duties**

- This review establishes planning consistency and arithmetic against committed records. Historical logs/checkpoints and CPU netlists were not reproduced. Source-digest declarations and syntax checks do not prove historical synthesis figures.
- Physical calibration: NOT RUN. Field skips and skipped physical jobs are not hardware proof. No full parent, processor, time-processor, synthesis or builder bank ran.
- F5 integration, measured CPU-memory reuse, primitive packing, replacement buffers, target service bounds, bench qualification and final routed fit/timing remain implementation obligations. M0s is future work.
- The manager publishes this packet and carries R1/R2 to the residue checklist. The other independent review, exact-head hosted/local-replica acceptance and explicit merge authorization remain required.
- The manager validates the current-dev merge candidate with builder/native banks at the merge turn and links its receipts. Assigned source base and live dev were both `5603c353137e90c1fa95429f6d00ef7a2298d9ee`. No future candidate validation is claimed. Source receipts are distinct from that validation.
- Post-merge containment and workflow updates remain manager duties. This stage does not complete #640's eventual routed-image acceptance.

[verify_checkout.py](scripts/verify_checkout.py) verified tracked blob bytes, executable modes, complete index entries and required submodule gitlinks. The [receipt](receipts/checkout.log) covers 1,233 parent blobs, 562 protocol-processor blobs, 104 time-processor blobs and 214 stream-library blobs. Required pins match; unused external and lwSRP worktrees remain uninitialized. Final status and whitespace checks are clean. No source fixes, commits, pushes, GitHub writes, author contact, shared installs or hardware actions occurred. Publish only REPORT.md and files listed in MANIFEST.sha256; scratch is excluded.

[lanes]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L966
[budget-order]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/AREA_BUDGET.md#L336
[m8]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L573
[fallback]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L875
[memory]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L697
[recipe]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L1136
[m2]: https://github.com/kebag-logic/milan-fpga/blob/7387bb6f6ae98f3e1d2e4a1f62c2c66f094fe783/docs/design/MARK_II_AREA_PLAN.md#L450

R493-2 FINISHED

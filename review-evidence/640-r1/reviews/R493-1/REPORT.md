[R493] POSITIVE - exact head c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970

Round R493-1, external independent review of [PR #698](https://github.com/kebag-logic/milan-fpga/pull/698), stage 1 of [issue #640](https://github.com/kebag-logic/milan-fpga/issues/640).
Tree: `a95adb1ad43e09865509188697ec4a96f42d7a83`.
Comparison base: `5603c353137e90c1fa95429f6d00ef7a2298d9ee`.

No BLOCKER, MAJOR or MINOR finding remains. Two wording-only Docs findings are RESIDUE under the owner's 2026-10-02 rule. This approves the planning document, not implementation completion, a default flip, hardware qualification or merge.

**Scope and independence**

I reconstructed the contract from repository authorities, the issue body and public decisions before examining the diff. The [round-1b assignment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6080904058) narrows this review to planning documentation. The issue's final routed-image acceptance remains future work.

The [diff](source.diff) changes only the plan and area budget: 950 insertions, eight deletions. History contains the required two-parent merge `a959b7879ed05a24c89bf71424e02c3049042463`, followed by the round-1b documentation commits. No RTL, gate, record, interface or submodule pin changes occur. I wrote the [independent verdict and ledger](INDEPENDENT_VERDICT.md) before checking for prior findings. No other review report informed that assessment.

**Conformance and decisions**

The [decision table][decisions] faithfully incorporates every assigned ruling. The [public decision snapshot](scope-decisions.json) retains each authority and its URL.

- [D1/D3/D7/D8](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5990755268): PDU and port-transaction equivalence; reviewed retargeting of cycle checks; bounded internal latency; preserved normative margin, restart, fast connect and capture; intermediate ledger measurements; M9 re-record; at least 1% planning margin.
- [Owner decisions](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991591637): diagnostics retained; DDR3 replaced by on-chip memory; smaller cacheless core conditional on 8x8 capture <=24.5 ms and boot timing. M10 remains planned where fabric AECP remains. Its zero default credit follows from the subsequent F5 removal.
- The milestone-13 progression at comments 5991605450, 5991626132, 5991695093 and 5991737927 is explicit in [plan:794][decisions]. The initial separate milestone and CSR boundary are superseded. Packet rings, filtered ingress, ADP/GM events, 32-bit accesses, doorbell/interrupt, no DMA, bus adapters, portable firmware and one YAML contract are retained.
- [Default split](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5991745829) and [pre-release integration](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5993114362): F0-F5 replaces M3's ACMP/ADP part and M4. AECP and saved-state handling are included. The all-fabric option remains supported; hard-core porting remains milestone 13.
- [Default-flip decision](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6009576644) and [approved requirements](https://github.com/kebag-logic/milan-fpga/issues/664#issuecomment-6015500032): shipping stays all-fabric until F2-F5 suite and bench acceptance. Major 3 identifies an actual split image. The approved 10 ms project budget remains separate from normative wire deadlines.

The [lane table][lanes] gives M2, M3, M5, M6, M7, M8, M10 and M9 scope, dependencies, estimates, order, risk and required evidence. The adopted pin satisfies the earlier dependency. Week-4 remeasurement and the December 15 schedule are explicitly estimates. The [budget][budget] agrees on placement, every central cumulative figure, margin and D7 policy. [Issue #229's closure](https://github.com/kebag-logic/milan-fpga/issues/229#issuecomment-6009659123) supports calling its former allocation superseded.

**Independent numerical checks**

[verify_figures.py](verify_figures.py) passed 143 assertions. [figures.json](figures.json) records actual and expected values. It compares the tables with the base commit's resource JSON, proves that JSON unchanged at the reviewed head, checks every current inventory row across all three endpoints, and recomputes the disjoint removal and cumulative tables.

| Recorded endpoint | LUT | FF | RAMB36 / RAMB18 | BRAM tiles | DSP | WNS / WHS, ns |
|---|---:|---:|---:|---:|---:|---:|
| route-1x1 | 50,267 | 54,413 | 74 / 27 | 87.5 | 14 | +0.299 / +0.031 |
| ooc-1x1 | 23,179 | 19,779 | 16 / 3 | 17.5 | 8 | -3.562 / +0.159 |
| ooc-8x8 | 30,135 | 27,380 | 21 / 5 | 23.5 | 8 | -2.278 / +0.159 |

These are stored measurements of `a5ca6e5110d515bf5f894f87b94f9bf6f6836bbb`, carried by the assigned base. They are not new measurements of either the base or review head. The [source receipt][baseline] supplies the four signoff corners, recipe, input digests and route-log digest. The plan copies them correctly. The route leaves 71 slices, 47.5 physical BRAM tiles and 34 tiles below the policy ceiling. The current 0.25 ns fall tolerance implies WNS >=+0.049 ns, beyond the +0.030 ns absolute floor. Standalone timing is not integrated timing acceptance.

The split calculation uses non-overlapping source scopes. AECP includes its children once. The [mailbox source][mailbox] supports 3,102 LUTs, 2,946 FF, six BRAM tiles and +0.402 ns at 100 MHz. Integration and mapping allowances are labelled estimates.

| Calculation | Independently reproduced result |
|---|---:|
| Disjoint wrapper subtotal plus parent MAAP | 17,678 + 429 = 18,107 LUT |
| Central split: 18,107 - 3,102 - 1,000 | 14,005; rounded down to 14,000 |
| Conservative split: 18,107 - 3,102 - 2,000 - 1,500 | 11,505; rounded down to 11,500 |
| Optimistic split: 18,107 - 3,102 - 500 + 1,500 | 16,005; rounded down to 16,000 |
| Credited BRAM released, less replacement | 6.5 - 6 = 0.5 tiles |
| Other wrapper LUTs, uncredited | 23,179 - 17,678 = 5,501 |
| Remaining central savings: M2/M5/M6/M7/M8a/M8b | 200 + 600 + 600 + 500 + 1,600 + 1,700 = 5,200 |
| Final central / conservative / optimistic image | 31,067 / 35,067 / 27,067 LUT |
| Central / conservative headroom below 38,040 | 6,973 (18.33%) / 2,973 (7.82%) |
| Conservative image without conditional M8b | 36,367 LUT |
| Integer ceiling for at least 1% margin | 37,659 LUT |

M2 excludes processor, media and gPTP arrays. M5 optimizes the existing CSR face; L2 bears new split integration. M6 retains media ownership, M7 retains fabric gPTP, and M8 owns memory/core replacement costs. M3/M10 and old diagnostic, registry and SRP savings are not added again. The M3 weighted basis yields 3,380.3 LUT before overhead and residual width work, consistent with its approximate 2,600-LUT fabric-only estimate.

**Architecture and robustness**

I checked the plan against the [ownership contract][ownership], [SoC mailbox wiring][soc] and [unconditional processor instance][instance]. The current mailbox datapath is idle, so merely enabling it cannot remove processor area. The plan makes removal contingent on integration and qualification. Media admission, counter production, framing, timestamps, gPTP, physical audio and equivalent diagnostics remain fabric obligations.

The [risk and verification text][split] covers bounded ingress, ring backlog, flash interference, all recipients, delayed events, independent wire deadlines and memory capacity. The [invariants][invariants] preserve malformed-input, reset, ordering and backpressure tests, all-fabric counts, ATDECC authority, interface indices and the second-port seam. Partial flips cannot claim the full saving. M8b must be reverted if its bounds fail. The conservative scenario clears the planning margin without it.

The plan identifies the current recipe's missing split endpoint. It requires reviewed measurement support before M9, retaining independent all-fabric references. No BRAM-growth tolerance is waived. LUT arithmetic does not establish memory fit, routing or timing.

**Executable evidence**

The independent [documentation campaign](docs-gates/results.json) completed 41/41 commands with rc 0. It covered link/privacy checks and controls, added-line punctuation, style, feature consistency, traceability, diagrams, imported documentation references, source paths, TOC/anchors, bare-metal scope, wire accountability, resource-record validity and CI contracts. [run_docs.py](run_docs.py) retains the commands; each has a raw log and rc file. It waited for every child, with at most eight concurrent lightweight checks. No heavy bank or hardware run was performed.

The [author's published receipt](author-gate-receipts.txt), fetched from the [pinned evidence tree](https://github.com/kebag-logic/milan-fpga/tree/994453e98aa8cea39e06534115ebebb258136767/review-evidence/640-r1), binds the source head and hashes of the reported 48-command campaign. The [readiness comment](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-6081236580) supplies commands and reported outcomes. Those are author evidence. Their listed raw logs were not all published in that tree and were not independently rehashed here. No manager source bank exists or is inferred.

The [hosted snapshot](hosted-checks.json) names the reviewed head. It separates successful executed jobs, ongoing jobs and a skipped physical job. It does not establish final aggregate acceptance. Hosted and local-replica acceptance remain manager duties.

**Findings**

**R493-1-R1 | RESIDUE | Docs | [plan:655][long-plan], [budget:168][long-budget] | Long prose remains.**

Authority/evidence: the [documentation rules][doc-rules] require short sentences. The M3 basis is one 37-word sentence under the repository's tokenizer. The placement sentence also exceeds the limit. Neither changed page belongs to the built-in style gate's fixed population. The [prose observations](prose-observations.json) expose that limit; they are screening output, not a claim that every observation is a new defect.

Impact: readability only. Measurements, decisions and acceptance claims remain correct.

Required outcome and exact fixes: replace the M3 sentence at lines 655-658 with:

```markdown
Its basis uses these shares:

| Scope | LUT basis | Share |
|---|---:|---:|
| Notification | 2,125 | 60 percent |
| D3 and dynamic state | 1,703 + 134 | 70 percent |
| AECP own logic | 1,302 | 50 percent |
| AECP dispatch queue | 421 | 40 percent |
```

Replace the placement sentence at budget lines 168-169 with:

```markdown
The [owner's decision](https://github.com/kebag-logic/milan-fpga/issues/640#issuecomment-5993114362) assigns the bare-metal split to milestone 12.
Integration precedes P3.
```

Carry repeated long-prose observations to the residue checklist. Verification: inspect sentence lengths and rendered text; retain every existing figure and claim. A wording pass must not change the ledger or qualification conditions.

**R493-1-R2 | RESIDUE | Docs | [plan:3][plan], plan:414-415, [budget:143][budget] | References are not consistently linked.**

Authority/evidence: the review assignment requires every reference to be a link. Issue references and source filenames at these locations remain plain text. Link-health checks cannot validate a missing link.

Impact: navigation only. The intended authorities and source files are identifiable and were independently examined.

Required outcome and exact fixes: at plan line 3, wrap `#640` as `[#640](https://github.com/kebag-logic/milan-fpga/issues/640)` and `NFR-RES-01` as `[NFR-RES-01](../reference/FR_NFR.md#35-resource-reliability-and-the-rest)`. Apply the same links at budget line 143. At plan line 9 and budget line 152, wrap `#396` as `[#396](https://github.com/kebag-logic/milan-fpga/issues/396)`. At plan lines 414-415, use these exact source links:

```markdown
[`milan_soc.py`](../../sw/litex/milan_soc.py)
[`milan_datapath.sv`](../../hdl/milan/milan_datapath.sv)
```

Carry repeated bare references to the residue checklist, preserving their parent-versus-processor repository identity. Verification: inspect rendered navigation and rerun link/anchor checks. Only link markup changes are required.

Both findings are purely presentational. Neither changes a measurement, figure, verdict, test, generated artifact, clause claim, conformance claim or privacy rule. Neither makes a lens unclean under the assigned RESIDUE rule.

**Prior public findings**

After writing my independent verdict and ledger, I checked PR conversation comments, submitted reviews and inline comments. The [receipt](prior-findings.json) records two review-start notices, zero submitted reviews and zero inline comments. No prior public findings existed to resolve or retain at this head.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | [Decisions](scope-decisions.json); [requirements][ownership]; [plan decisions][decisions]; [lane table][lanes]; [figures](figures.json) | R493-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| RTL | CLEAN | [Two-file diff](source.diff); [split plan][split]; [architecture][architecture]; [SoC wiring][soc]; [processor instance][instance]. Architecture review; no changed RTL | R493-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Robustness | CLEAN | [Split risks][split]; [dependencies][lanes]; [invariants][invariants]; [budget and growth policy][budget]; [scenario checks](figures.json) | R493-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Tests | CLEAN | [41-command results](docs-gates/results.json); [143 assertions](figures.json); [author receipts](author-gate-receipts.txt); [byte verification](tree-after.json). No changed tests | R493-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |
| Docs | CLEAN | [Plan][plan]; [budget][budget]; [docs results](docs-gates/results.json); [prose observations](prose-observations.json); R1/R2 are RESIDUE only | R493-1 | c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970 |

**Limits and pending manager duties**

- This review proves document consistency and arithmetic against committed records. Historical full measurement logs/checkpoints and redesigned hardware were not reproduced. Estimates and allowances remain uncertain.
- Physical calibration: NOT RUN. Field skips and skipped physical contexts provide no hardware proof. F5 integration, target service timing, memory capacity, F2-F5 bench acceptance and final routed fit/timing remain implementation obligations.
- The manager must publish this packet, carry R1/R2 to the residue checklist, obtain the other independent review, settle hosted/local-replica acceptance and validate the current-dev merge candidate with the required builder/native banks. Source-head receipts are distinct from that future candidate validation.
- No merge authorization is supplied. The planning PR relates to the redesign issue; it does not complete final hardware acceptance. Required containment and workflow updates remain with the manager after an authorized merge.

[verify_tree.py](verify_tree.py) proves matching tracked bytes, file modes, complete index entries and required submodule gitlinks before and after all checks. The [final receipt](tree-after.json) equals the [initial receipt](tree-before.json): 1,233 parent blobs, 562 processor blobs, 104 time-processor blobs and 214 stream-library blobs. Working-tree status is empty. No source fixes, commits, pushes, GitHub writes, author contact or hardware actions occurred. Publish only REPORT.md and files listed in [MANIFEST.sha256](MANIFEST.sha256); scratch is excluded.

[plan]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L3
[decisions]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L776
[lanes]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L695
[split]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L401
[invariants]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L742
[budget]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/AREA_BUDGET.md#L143
[baseline]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/findings/234_PP_SHADOW_AREA_BASELINE.md#L30
[mailbox]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MAILBOX_SPLIT.md#L934
[ownership]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/REQUIREMENTS.md#L21
[architecture]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/ARCHITECTURE_HW_SW_SPLIT.md#L32
[soc]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/sw/litex/milan_soc.py#L2504
[instance]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/hdl/milan/milan_datapath.sv#L8003
[long-plan]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/MARK_II_AREA_PLAN.md#L655
[long-budget]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/design/AREA_BUDGET.md#L168
[doc-rules]: https://github.com/kebag-logic/milan-fpga/blob/c4b8b7d373c9233bc9e71c6ed32eae9ad2b3f970/docs/README.md#documentation-rules

R493-1 FINISHED

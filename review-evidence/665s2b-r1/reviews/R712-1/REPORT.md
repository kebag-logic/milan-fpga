[R712] NEGATIVE - exact head f884c7e9fb71cdb94c12e3228b1412801c34e1f4

External independent review R712-1, issue #665 / PR #810 into dev-soft-core. Tree `40ee92bf67435d4a2dd31ab2373ad05c9bdf24f5`; whole change against `f4c9ad4f`, including the S1 merge. All five lenses were applied. Two open MINOR findings prevent clean coverage: a mover boundary defect above the lengths current firmware submits, and an unsettled per-pass acceptance requirement. Neither alleges that the published unheld end-to-end rows exceed their family budget.

Authority: AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md, FR_NFR 3.4.1/3.4.2 and NFR-SCOUT-01/03; the issue's frozen acceptance and public scope decisions, particularly the [cache/mover amendment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6492443864), [20 ms decision](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6495692075), and [S1 merge assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6502579312). Public decisions are preserved in `public-scope.json`. The PR relates to #665; the owner explicitly left the egress-held work and area commissioning open.

## Findings

**R712-1-F1 — MINOR — Conformance, RTL, Robustness, Tests — `hdl/milan/mailbox/KL_mbx_dma.sv:174`; `tb/verilator/mbx/dma_main.cpp:417` — the three largest accepted lengths overflow the word count.**

- **Authority/evidence:** The component interface at `KL_mbx_dma.sv:59` accepts a 12-bit byte length, with zero a no-op. Lines 14–24 require at most sixteen beats inside one 64-byte line and byte-exact payload movement. The CSR contract in `sw/firmware/ctrl/plat/mbx_dma.h:15` exposes all twelve bits, without stating a smaller accepted range. The start path does not reject 4093–4095. At line 174, `11'((len_bytes_i + 12'd3) >> 2)` adds in twelve bits: those lengths produce zero words. This violates the mover interface, not an inferred larger Ethernet-frame requirement.
- **Reproduction:** `probe_dma_length.py` compiles unchanged submitted RTL against a disposable copy of its byte-oracle bench, with a 1024-word ring and lengths 4092–4095 in both directions. The 4092 control passes. Each other length fails receive completion and, on transmit, the sixteen-beat limit, 64-byte-line limit and byte comparison. `dma-length.log`: 9,255 checks, 12 failures, exit 1. No checkout source changed.
- **Impact:** Receive enters FILL with zero chunk/count, issues no request and remains BUSY, holding subsequent CPU mailbox accesses. Transmit presents underflowed ARLEN=255, emits an oversized read burst and moves incorrect data. ERR is not raised at acceptance. Current `mbx.c:423,494` rejects records above their channel maximum (global maximum 1514), so well-formed current firmware traffic cannot trigger this. That containment makes this MINOR rather than MAJOR.
- **Required outcome:** Every accepted length must obey the byte-movement and burst contract. If only a smaller range is intended, enforce a defined refusal/ERR outcome before acquiring the host port. No accepted boundary value may wedge it or emit an oversized burst.
- **Verification:** Check 4092–4095 in both directions, including subsequent CPU access and recovery transfer; test any defined refusal range. Retain the short/tail/alignment/stall/error/reset cases and all 17 plants. The current shape sweep covers 1–96 and 1512–1514; its passing plants do not exercise this arithmetic boundary.

**R712-1-F2 — MINOR — Conformance, Tests, Docs — `sw/firmware/ctrl/loop/ctrl_loop.h:55–63`; public `author/receipts/measure/{N10-A8,N10-B8}/table.md` — the separate per-pass acceptance remains unmet/unsettled.**

- **Authority/evidence:** The [public S2b assignment, items 3 and 6](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6414297191) requires a stated share derived from the one-hart rule and explicitly makes **every pass within the per-pass share** an acceptance condition. `ctrl_loop.h` derives nine passes, states the historical 10/9 ms cap, and now names SRP's 18 ms as the tightest shared bound. The later 20 ms decision changes T_svc/family grading but records no removal of this separate criterion. Earlier public acceptance reports distinguished fitting T_svc from meeting the share.
- **Measured counterexample:** On the unheld `backlog` group, N10-A8's longest pass is 228,766 cycles = **2.28766 ms**, and N10-B8's is 230,298 cycles = **2.30298 ms**, at the commissioned 100 MHz. Both exceed even a relaxed 20/9 = 2.22222 ms share. The comment's tightest-family derivation, 18/9 = 2 ms, also rejects D10-A8 (2.20017 ms) and D10-B8 (2.20440 ms). `rows-audit.log` independently checks these conversions. Changing a historical “10 ms” phrase to 20 ms would still leave failing passes.
- **Impact:** The evidence establishes measured end-to-end rows, but not the frozen per-pass fairness condition. The path grader does not turn these over-share passes into failing acceptance, and the final docs/evidence provide no resolved per-pass disposition. This is a requirement/gate gap, not proof of an additional failed wire deadline, and cannot be cleared as wording residue.
- **Required outcome:** Publicly settle per-pass acceptance against the approved budget and unchanged admission: meet and grade the derived cap, or obtain an explicit acceptance amendment with a justified replacement bound. Retain measured failures until validated. Do not silently equate row-budget success with pass-share acceptance.
- **Verification:** At both points, both arms, with and without drafts, report/assert the accepted per-pass bound independently of row verdicts. A planted pass above it must fail even if every end-to-end row fits. If the owner amends the criterion, link that decision and test the replacement claim.

## Independent lens results

**Conformance: UNCLEAN, F1 and F2.** Examined `docs/reference/FR_NFR.md:322–424`, the harness's `scenario.py`, `grade.py`, self-tests/plants, CPU options and mailbox interface against the decisions. T_svc is 20 ms, SRP/MRP min(20,18)=18 ms, ACMP/discovery 20 ms, ordinary AECP 20 of 24 ms, optional identification 15 ms when enabled. The S1 IN_PROGRESS path retains its separate 12 ms bound. The budget self-test kills SRP T_svc-only grading, the stale 10 ms pin and ceiling-only AECP grading. The response-margin arithmetic is sound conditionally: 178 ms ACMP, 218 ms AECP/MVU, 228 ms controller timeout, after the stated 1 ms ingress and egress allowances. These are design bounds, not measured wire proof; the text says so.

`audit_rows.py` independently checks all 392 instances in the eight published tables: 49 per leg, 43 fitting and six missing, with every miss egress-held. It checks cycle/time conversion and each minimum bound. The worst unheld SRP instance is 16.949 ms against 18; 8x8 AECP maxima round to 15.10/15.84 ms without drafts, 13.74/14.61 with them. No unserved or owed row disappears from the denominator. `rows-audit.log` records the result.

**RTL: UNCLEAN, F1.** Examined `KL_mbx_dma.sv:125–419`, `sw/litex/milan_soc.py`, `sw/litex/ctrl_memory.py`, harness `split_soc.py` and `plat/mbx_dma.h`. Checked start/register ordering, CPU request retention, acknowledgements, receive strobes, transmit tail masking, line splitting, backpressure, burst error draining and sticky ERR cleared by an accepted start. The focused submitted suite passes 360,473 checks; all 17 plants are caught. The additional full-width boundary probe exposes F1.

Split-only CPU options give RV32IM, 128 sets × two ways × 64-byte fetch lines, one refill, two-way LRU, and 128 × 64-byte coherent direct-mapped data cache. Mailbox/CSR/flash remain uncached; all-fabric CPU arguments remain unchanged. Examined the public out-of-context netlist options, constraints, timing and route reports: at 10 ns CPU WNS/WHS +0.659/+0.031 ns, bus +2.660/+0.072 ns, zero route errors. The separate mover route reports 395 LUT, 700 FF and no block RAM. These are out-of-context results, not whole-board timing acceptance.

**Robustness: UNCLEAN, F1.** Examined mover bench/plants, driver validation/error handling in `mbx/mbx.c`, `plat/ctrl_mem.c`, `test/test_ctrl_mem.cpp`, AECP retry/event/index changes and SRP reclamation. Checked zero/tail lengths, ring wrap, CPU access during moves, busy/misaligned starts, reset and both AXI error directions. For memory primitives, checked alignment, overlapping memmove in both directions, guard-page bounds, comparison sign and return values. Five focused memory tests pass; all six new bulk/remainder copy/fill plants are independently caught. No further behavioral finding was identified in the inspected protocol state changes.

**Tests: UNCLEAN, F1 and F2.** Examined actual failure assertions and mutation mechanisms, the public source receipts and profiling patch. Independently executed budget self-test (109 checks, 80 plants, zero failures), mailbox generation/check/crosscheck/self-test, mover positive suite/17 plants, five memory tests and six new copy/fill plants. Published exact-head coverage is 100% for all 33 measured files: for example `ctrl_mem.c` 167/167 lines and 80/80 branches; mailbox driver 324/324 and 158/158; AECP core 479/479 and 392/392; commands 472/472 and 398/398; face 172/172 and 152/152; SRP adapter 572/572 and 500/500. Branch coverage does not establish all operand boundaries, as F1 demonstrates.

Reviewed the published four-shard firmware campaign (553 plants, including 168 AECP plants and S1's 59), the 64-suite sweep at `51fa5f18` (2,552,440 checks, zero failures), and the subsequent documentation-only change. The eight legs use the labeled profiling variant at `db77201b`; the published final-head check reproduces N10-A1 backlog byte-for-byte. This is the author's source execution/equivalence evidence, not a fresh independent execution of all eight CPU simulations or a manager source bank.

**Docs: UNCLEAN, F2 — `docs/reference/FR_NFR.md:334`, `docs/design/SPLIT_CONTROL_MEMORY.md:837`, `docs/design/MAILBOX_SPLIT.md`, `docs/design/MARK_II_AREA_PLAN.md`, harness `README.md`, PR #810 and public evidence — checked normative budget, measured claims, open work and S1/S2b integration against source/receipts.** The owner-approved policy and per-family rule agree. The 124/121.5 block-RAM ledger is explicitly open; the 8x8 two-interface firmware allocation is 56.5, above normal 56 and within the ledgered exception. Egress-held misses remain open under tsn-c-stack #26. Calibration NOT RUN and field skips are not hardware proof. The added-source-comment scan found no new prohibited bench/review labels. F1 is an implementation violation of the stated interface; a wording-only change cannot resolve it.

For the eleven formerly conflicting files, checked history and the combined result: FR_NFR keeps IN_PROGRESS and minimum grading; AECP retains S1's face writer/acknowledged state with the index/event optimization; the face fixture rebuilds the index after key changes; plants/coverage include both sides; both SoCs retain face wiring and mover/cache setup; the hot list loses the replaced stream fixture. `gen_mailbox.py --check --crosscheck --selftest` passes. Contract/generator/generated files remain at S1's 2.3 without a separate S2b contract edit. Staged donor drafts are measurement variants, not parent pin updates.

## Reviewer-owned ledger

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: F1, F2 | FR_NFR 3.4.1/3.4.2; grade/scenario/self-tests; DMA interface; eight composed tables | R712-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| RTL | UNCLEAN: F1 | KL_mbx_dma; milan_soc; ctrl_memory; split_soc; netlist/route reports | R712-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Robustness | UNCLEAN: F1 | dma_main/plants; mbx.c; ctrl_mem/tests; AECP/SRP paths; boundary probe | R712-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Tests | UNCLEAN: F1, F2 | Focused executions; plants; public coverage, source gates, sweep/composed receipts | R712-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |
| Docs | UNCLEAN: F2 | FR_NFR; MAILBOX_SPLIT; SPLIT_CONTROL_MEMORY; area plan; harness README; task/PR | R712-1 | f884c7e9fb71cdb94c12e3228b1412801c34e1f4 |

## Execution evidence

Builds/probes stayed in this review's disposable scratch directory with bounded concurrency and no source changes. Reproduction scripts: `run_focused.py`, `run_memory.py`, `run_memory_mutants.py`, `probe_dma_length.py`, `audit_rows.py`. Raw logs and return-code files accompany the report. The boundary probe's nonzero exit is expected evidence of the finding; killed-mutant test logs also fail intentionally, while the mutation campaign returns zero.

The [public evidence revision](https://github.com/kebag-logic/milan-fpga/tree/b447e26340def7706919eff18d41f198c29ae5b9/review-evidence/665s2b-r1) includes author-r8, author-r9 and author receipts. `public-evidence-integrity.log` records 867 selected public executable artifacts checked against publication hashes. No private author material or another reviewer's report was used to form this verdict and ledger. Prior-public-finding reconciliation and final checkout integrity are recorded after this independent verdict/ledger was written.

## Limits and pending manager duties

- The composed rows are the explicitly commissioned **100 MHz CPU / 100 MHz bus** profiling variant. Checked-in 1x1/8x8 recipes still specify **50 MHz CPU / 100 MHz bus**; `milan_soc.py:3200` connects CPU to the Milan domain. The public no-clock-increase decision and later explicit 100 MHz experiment do not establish these rows at 50 MHz. No product clock changed here; this review accepts the explicitly requested 100 MHz experiment within that scope and infers neither proportional scaling nor acceptance at 50 MHz.
- Slow-firmware controls run on the cacheless core. The published split-cache spin is 17.3 ms, so it escapes the 20 ms threshold; it is not a demonstrated kill on the split cached CPU. No composed row exercises S1 IN_PROGRESS; its face behavior has source/host tests, not a measured 12 ms CPU row. Optional identification is disabled.
- Wire/network timing, ingress/egress taps and calibration remain open. The 60 ms egress-held cases remain with tsn-c-stack #26. Area overrun and donor draft review remain separately commissioned. Out-of-context timing and unexecuted field contexts do not prove board timing, fit or hardware operation.
- This reviewer ran no full source bank, hosted/act acceptance, builder bank, whole-parent/processor/gPTP bank or new route. The published builder's historical Arty route NOT RUN and CI command-table checker NOT RUN remain limits. Skipped contexts and executed gates are distinct.
- The manager owns hosted/act acceptance and the **current-dev merge candidate**, including builder/native banks and their published receipts. No manager source bank exists at this head. Source validation against `f4c9ad4f` does not validate incorporation of live dev `1e80128f0a467b58bf884b7d9bf62e013a2fb141` or a later tip. Resolve F1 and F2, re-review affected lenses at the corrected head, complete review/merge evidence and containment, and obtain explicit maintainer merge authorization. This review publishes nothing and authorizes no merge.

## Prior public findings and final integrity

After writing the independent verdict and ledger, inspected PR #810's combined public discussion, inline-comment and review-submission timeline. As retrieved on 2026-10-29 before 20:59 UTC, it contains the two manager review-start comments and no published review findings to resolve or retain. `pr-discussion.json` preserves that result. No other reviewer's report was read. A review still in flight is not a positive review or a completed merge condition.

`verify_checkout.py` and `checkout-integrity.log` confirm the exact head/tree, raw tracked blob bytes, executable/symlink modes, complete index and absence of masking index flags: 1,476 parent files and 1,188 files in the five required initialized submodules. Their gitlinks and checked-out heads are:

| Submodule | Exact gitlink |
|---|---|
| gptp-processor | 55680bff3b287b9a7b0c759f51471fa617c17335 |
| protocol-processor | ed2118035e4cec76fb1b59cfbf8a053aeacc8af8 |
| third_party/lwSRP | 08ee86e812a0eb5e1dc6cd61b494d8baf3491348 |
| third_party/tsn-c-stack | 70936b77dc41981e192438388cd0aced69954f18 |
| third_party/verilog-axis | 48ff7a7e2ef782cf778d47910cf85835c64b1bce |

The external gitlink remains `efeb541ae5fe1e078332d8462dca2fc2d9cb8db5`; its worktree was not required. Parent status is empty. Probe code/builds remain only under this packet's unpublished `scratch/`. `MANIFEST.sha256` enumerates the publishable files with relative paths. No source fixes, commits, pushes or GitHub writes were made.

R712-1 FINISHED

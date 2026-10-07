[R529] POSITIVE - exact head 938497af1dffd8a87edebf3ab93663914bf85e5e

R529-2 is complete. All five lenses are CLEAN at this head. The eight prior findings are resolved, and the optional suggestion is addressed. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION remains. This is a source-review verdict, not merge authorization or physical acceptance.

**Scope and independence**

Reviewed tree `b40dfc375f080a96eb4a927e023fa6b916cbe7c1`. The assigned comparison is `021b9c1fb966e9a1a4acef6b5233edd3518f32a0..938497af1dffd8a87edebf3ab93663914bf85e5e`: 38 files including inherited FC changes. F2 itself begins after `db9aa8c9b135b34ff3d070a979dee70440b37cc6`. Round 2 consists of `11e195bea` and `938497af1` after `1a5d70faba6a9b01aab6bb868c12e4c7023e0c70`, touching ten files. No F2-only change touches RTL, register definitions, shipping configuration, placement glue or submodule pins. [Identity and inventory](receipts/identity-scope.json).

Reconstructed the operating contract, contribution rules, documentation index, #665 frozen acceptance and public decisions, requirements and interfaces, diff/history, and public evidence. Authorities include IEEE Std 1722-2016 Annex B, Table B.7 and note a, Table B.8, B.3.4-.6 and B.4; NFR-SCOUT-02/03/08 and H-MAAP; the mailbox YAML; the register map; and #678. The parent is a differential subject, not the conformance oracle.

The [independent verdict and ledger](receipts/independent-pass.md) were written before reading either prior public review report. Only then were the [R529-1 findings and ledger](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6028867882) and [R528-1 findings](https://github.com/kebag-logic/milan-fpga/pull/687#issuecomment-6029234761) reconciled. No private author material, lane notes, or current-round reviewer report was used. No additional formal reviews or inline findings were present at the read checkpoint.

The R529-1 ledger marked every lens UNCLEAN. Consequently no old clean lens is banked here. Unchanged artifacts and prior execution scope are referenced by that ledger, while all five lenses were reapplied and cleared at the current head. [Artifact-specific static examination](receipts/static-review.md).

**Prior findings: disposition at this head**

The [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/665#issuecomment-6029239721) accepts these outcomes. Original severities and lens assignments are retained below.

| ID; original severity; lenses | Root verification and required outcome | Disposition |
|---|---|---|
| R529-1-F1; MAJOR; Conformance, RTL, Robustness, Tests | `sw/firmware/ctrl/app/ctrl_app.c:55-58` writes the MAAP RX bit with ADP/event bits. `test_maap_mbx.cpp:273` traverses `ctrl_app_start_maap`, idle `ctrl_loop_step`, the wait callback, IRQ and subsequent service. Each accepted record reaches the indexed core and produces a committed retry. The missing-bit production defect fails `MaapHost.AppWaitWakesForMaapWithinBudget` at one and two interfaces. | RESOLVED |
| R529-1-F2; MINOR; Conformance, Tests, Docs. R528-1-F2; MINOR; Tests, Docs | `test_maap_differential.cpp:39,133` records timer-driven software sends and parent completion cycles. Core intervals satisfy strict 500 < T < 600 ms; 1, 500 and 600 ms production defects fail `ProbeTimingAndParentDelta`. Parent phases reach 500/627 ms endpoints. Four immediate-start core PROBEs and three delayed parent PROBEs are asserted, and false parent-bound/count expectations fail. All eleven previous cases remain. README:166 lists the six deltas in #686 plus its count addition. | BOTH RESOLVED |
| R528-1-F1; MINOR; Conformance, Robustness, Tests | `maap.c:185,230` retains Begin's supplied range while down and reserves it at the next operational port; :105 consumes the preference. `MaapCore.BeginBeforePortOperationalRetainsRange` checks transmitted bytes, invalid Begin, subsequent conflict and a fresh unpreferred Begin. A production defect selecting a random range instead fails the named case. Authority: Table B.7 note a. | RESOLVED |
| R528-1-F3; MINOR; Tests | `test_maap.cpp:179,195` checks fixed-seed Restart moving the base and both priority directions with every deciding octet, including tied suffixes and the first octet. Reusing the old range, comparing only the last octet and dropping the first octet each fail the specified tests. The numeric-order control also fails. Authority: B.3.5.3, Table B.7, B.3.6.4. | RESOLVED |
| R528-1-F4; MINOR; Tests, Docs | `test_maap.cpp:368,423` makes listener DMAC writes read-only and checks all 18 destination-word writes precede either enable, with enables last. Verified against REGISTER_MAP:1541,1546 and `hdl/common/csr/milan_csr.sv:1834`. Clearing direction and enabling before programming each fail a named CSR case. | RESOLVED |
| R528-1-F5; MINOR; Tests | `test_maap_mbx.cpp:324` fills TX, stalls interface 1's DEFEND, resumes after 5 ms, and requires the indexed output to drain within the original H-MAAP allowance. The interface-0-only poll defect fails `InterfaceOneStallDrainsWithinBudget`. | RESOLVED |
| R528-1-F6; MINOR; RTL, Docs | README:101 and the PR description state that clearing MAAP_CTRL[0] disables KL_maap, leaving KL_pp_maap_shim unable to grant ALLOC_DA and talker_active unasserted. Checked against the shim and `milan_datapath.sv:1999,5326,7066`. They require firmware allocation to feed the processor face, or ACMP to move to the core through F3 before use, as a #664 decision 3 default-flip condition. | RESOLVED |
| R528-1-S1; SUGGESTION; Tests | `maap_mutants.py:63` adds generic production-predicate controls; all four are caught in this review. README:144 and the PR body expressly limit RV32 validation to release objects and distinguish the host debug assertion from target debug linkage. | ADDRESSED |

The README's probe-count attribution now agrees with [#686's public addition](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6029233665). The other listed deviations agree with the [issue body](https://github.com/kebag-logic/milan-fpga/issues/686). No defect has been cleared merely by moving it to another issue: #686 concerns the unchanged parent, which is deliberately compared against separate Annex B expectations.

**Fresh executable evidence**

| Execution | Result | Receipt |
|---|---|---|
| Focused positive core/CSR, mailbox and debug arms | 36 core/CSR; 12 mailbox at one interface; 13 at two; one debug case; zero failures | [one-interface/core](receipts/focused/positive-maap.log), [two-interface](receipts/focused/positive-maap_if2.log), [debug](receipts/focused/positive-maap_debug.log) |
| Unchanged surrounding model/port/unit arms | 22 model, 31 port, 23 seam and two MMIO cases; zero failures | [model](receipts/focused/positive-model.log), [port](receipts/focused/positive-port.log), [units](receipts/focused/positive-unit.log) |
| Reviewer-selected production defects | 18/18 caught by named failures after successful compilation, including both wake sizes, all required root defects, generic predicates and late-service controls | [campaign](receipts/focused-campaign.log); individual full logs and exits under `receipts/focused/` |
| Core/parent differential and complete self-test | 12 positive cases; 16/16 controls caught, including 1/500/600 ms and false parent bounds/count | [positive](receipts/differential-positive.log), [control summary](receipts/differential-summary.txt), [complete transcript](receipts/differential-campaign.log.gz), [exit](receipts/differential-campaign.rc) |
| Firmware coverage `--check --jobs 4` | All 17 files meet 100% line/branch ratchet after existing exclusions; no new exclusions. MAAP core 209/209 lines, 140/140 branches; CSR 39/39, 18/18; adapter 98/98, 60/60 | [coverage](receipts/coverage.log), [exit](receipts/coverage.rc) |
| Scoped exact-head mailbox RTL, both bus adapters | 316 Wishbone and 361 AXI-Lite checks; zero failures | [mailbox](receipts/mailbox.log), [exit](receipts/mailbox.rc) |
| Mailbox generator consistency and controls | Zero drift/crosscheck findings; all self-test controls pass | [generator](receipts/generator.log), [self-test](receipts/generator-selftest.log) |
| Final byte/mode/index/gitlink proof | PASS: 1,154 root blobs, 558 processor, 104 gPTP processor and 214 axis blobs match committed objects; required submodules are registered at their exact pins; status clean | [integrity](receipts/integrity.json) |

Wake elapsed time is 4,700 ns from original RX publication in every tested interface case. Interface 1's response takes 5,004,400 ns including its 5 ms stall. Both are under 10 ms with the stated 100 ns/access assumption. Original timer deadlines, backlog and stalls remain charged; planted late-send and late-state controls fail. This does not measure physical CPU or wire latency.

The current controller catalog has 192 defects and 197 named obligations; its four 48-entry partitions are complete and disjoint. [Catalog audit](receipts/catalog-audit.json). The full 192-defect campaign was supplied as public evidence and was not rerun in this delta review. The [public round-2 author packet](https://github.com/kebag-logic/milan-fpga/tree/d5338f877751683bf9e378d562ef8f892b442ec8/review-evidence/665f2-r1/author-r2) provides the final-head firmware results and the source-bank command/exit/hash tables. The handoff hash matches the public object. The underlying author logs are not all present in that archive, so their hashes were not independently verified. The results in the table above are fresh executions.

**Reviewer-owned completion ledger**

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | `maap.c:73,102,182,217,262,280`, Table B.7/B.8 and B.2-B.4; `FR_NFR.md:363,409`; timer/wire differential and preferred-range controls | R529-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| RTL | CLEAN | `KL_mbx_rx.sv:149,286` and generated masks versus YAML; `ctrl_app.c:55`; `maap_mbx.c:94,119`; `maap_csr.c:42`; `milan_csr.sv:1834`; shim/datapath consumers versus register contract; both bus-adapter receipts | R529-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Robustness | CLEAN | `test_maap.cpp:238,289,311,332,349`; `test_maap_mbx.cpp:170,273,324`; malformed, queue, link, tag, wrap, reentry, wait/wake, stall and late-service controls versus H-MAAP | R529-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Tests | CLEAN | `test_maap.cpp:179,195,368,423`; `test_maap_mbx.cpp:273,324`; `test_maap_differential.cpp:133`; named mutation receipts; coverage ratchet/exclusions; generator and mailbox checks | R529-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |
| Docs | CLEAN | MAAP README:29,101,144,166; #665 assignments; #686 body/addition; PR body; MAILBOX_SPLIT:420; public author packet versus executable observations and interface consumers | R529-2 | 938497af1dffd8a87edebf3ab93663914bf85e5e |

**Limits and pending manager duties**

Source validation is distinct from the final current-dev candidate. The deliberate dev merge deferral until #683 and #685 land is not a finding. At the merge turn, preserve the SDK object-build path and MAAP arms/partitions, construct the candidate against current dev, record both object IDs, and validate that candidate with the required full bar. The supplied live-dev reference is `79b086d44eb62d007d38e18f5618b98e8e2a33e6`; this report does not validate a merge into it.

Hosted acceptance and local workflow replication remain manager duties. The [single exact-head snapshot](receipts/hosted-contexts.json) includes successful executed lint, BDD, wire-accountability, no-Git docs, selector and four synthesis shards; firmware, docs, elaboration and simulation jobs were still running. Physical gPTP was **skipped**, which is not an execution. No hosted aggregate completion is inferred from partial child results, and no local workflow replica was run here.

Physical calibration was **NOT RUN**. Field/vendor skips are not hardware proof. Host mailbox co-simulation, ordered CSR programming and a host debug assertion establish neither target debug linkage nor target CPU/arbitration/NVM/egress margins, media quiescence, redundancy acceptance or all-stream bench/audio-soak acceptance. Resolve the allocation-to-ACMP dependency before this output is used and before any shipping-default flip. This review does not close the parent deviations in #686.

No full parent, processor, gPTP, synthesis or builder bank was run here. No source fix, commit, push, GitHub write, author contact, delegated review, container action, privilege or hardware operation occurred. Probes and builds stayed under packet scratch; the source worktree was not mutated. The final proof checks raw blob bytes and modes plus index records, rather than relying only on a clean status. The unused external submodule remains uninitialized with its gitlink unchanged.

The manager still owns publication, the independent review completion bar, required hosted/local acceptance, candidate validation, explicit merge authorization, post-merge containment and issue/project bookkeeping. A positive source verdict does not discharge those duties.

Portable reproduction: `python3 scripts/reproduce.py --source <exact-head-checkout> --packet <packet-directory> --verilator <pinned-simulator>`. It joins independent foreground subprocesses, confines disposable files to `scratch/`, passes the coverage job limit and uses `make -j16` with bounded child builds. Original run concurrency never exceeded sixteen compiler jobs. `scripts/focused_controls.py` and `scripts/integrity.py` also run independently. Publication copies normalize only local path prefixes; the [normalization receipt](receipts/path-normalization.json) records original and published hashes. The complete differential transcript is losslessly compressed. `MANIFEST.sha256` enumerates every publishable receipt and script; scratch is excluded.

R529-2 FINISHED

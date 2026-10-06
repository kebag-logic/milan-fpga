[R519] POSITIVE - exact head cd9825c947cf67b735d26cc1c42541ccd9d7f637

All five lenses are CLEAN for this source round. No BLOCKER, MAJOR or MINOR finding remains. One evidence-replay SUGGESTION is recorded below. This verdict covers tree `7234360164b13afa707faa552ebf72d4f10a44e7`, against base `86a7b0c57831c15e9cd8b42d64cc4a9843f4e726`. The upcoming main merge is a separate delta; issue #163 still needs its adoption timing sweep.

Scope was reconstructed from the repository instructions, documentation guide, [issue #163](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163), [assignment 6015580618](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/163#issuecomment-6015580618), interface and timing authorities, then all four commits and the complete 12-file diff. There is no tracked AGENTS.md or CONTRIBUTING.md in this processor tree. Relevant authorities are `hdl/README.md`, `docs/README.md`, architecture 02 §3/F02.4, 03 §8/F03.5, 06 §7, 08 §4 and 09. Public evidence was read after the independent diff pass. Scope snapshots and the exact diff are in `receipts/public/` and `receipts/exact.diff`.

The [public evidence at fc004672](https://github.com/kebag-logic/milan-fpga/tree/fc0046724b1416d5f87451c52eaac1a2668ae4ad/review-evidence/pp163-r1) was fetched by immutable revision. All 21 files match the published SHA-256 manifest and their repository blob identities. The measurement below is published source evidence; this review did not repeat synthesis or routing.

**Conformance and RTL.** `hdl/packet_engine/KL_pp_tx_arbiter.sv:161` replaces the serial minimum search with a unique minimum under `(age, class, lane index)`. The strict/non-strict comparisons preserve lowest-index ties. Qualification, pacing, aging, grants and the frame state machine are unchanged. `hdl/top/protocol_processor_top.sv:4382` resets and registers the withdrawal mask; its three consumers at lines 4407, 4427 and 4505 move together. Production module signatures, parameters and register maps are unchanged; the added ports are test observations only. The published sequential comparisons close 438/438 points at the integrated parameters and 386/386 at defaults, and their tie-fault control fails. Independent arbiter tests and planted faults support the same behavior.

**Cancellation and robustness.** The originator's response/cancel/acceptance priority, parked events, release merge, queue compaction and slot lifecycle were examined with the changed stage. A cancellation on the acceptance edge can send one complete probe. The retired exchange ignores its later grant, and the slot pool handles its release while streaming, then frees it at EOF. A cancellation on selection reaches the abort before the pool starts. The synchronous reset clears the new mask. No stale handle, double pop, truncated frame or lost response was observed. WD grades both adjacent edges, byte-exact output, both solicited answers, no retry/deregistration over its observation interval and complete slot/originator recovery. CX grades cancellation in the command's own clock and its absence for eight later clocks. The independent originator run includes simultaneous events and a seeded session of 3,757 events, peaking at eight live exchanges.

The [#653 ruling](https://github.com/kebag-logic/milan-fpga/issues/653#issuecomment-6009659836) retains response-before-notification. Its standing parent tests are `tb/verilator/milan_dp/README.md:666`, UNB U1–U4: both AAF and CRF inputs, both registered controllers, response-before-every-unlock-push, and the 1/1/0 counter invariant. The reversed-order control fails four U2 checks. The public consumer comparison includes that 421-check notify leg passing at both processor revisions. This review traced the unchanged ACMP/unsolicited ranking and serializer boundary; it relies on that published parent execution for UNB, rather than claiming a new parent run. See [the retained authority](receipts/public/parent-unb-authority.md).

**Cone coverage and resources.** The described survey visits each startpoint in the fan-in of every integrated arbiter sequential cell, taking the worst path for each start/end pair. The 187-cell inventory reconciles as FSM 3, slot 3, owner 3, start-sent 1, age 32, counters 128, grants 8, qualification 8 and pacing 1. Every family occurs in both public cone summaries. The standalone inventory has 188 cells: its additional `sof_pend_r` feeds only `tx_sof_o`, which the measured parent wrapper leaves open at `hdl/milan/KL_pp_shadow.sv:1182`. Its pruning explains the difference. This checks the target inventory; the unpublished traversal script itself remains the limit in S1. See [the inventory audit](receipts/cone-inventory-audit.json) and [reconciliation](receipts/cone-reconciliation.json).

| Published OOC 1x1 measurement | Base | Reviewed implementation |
|---|---:|---:|
| Deepest sampled arbiter path | 51 levels | 16 levels |
| Startpoints | 1,631 | 328 |
| Start/end pairs | 263,154 | 17,990 |
| Pairs above 20 levels | 146,535 | 0 |
| WNS | -3.562 ns | +3.337 ns |
| TNS / failing endpoints | -37.519 ns / 16 | 0.000 ns / 0 |
| Processor LUT / FF | 22,517 / 18,941 | 22,478 / 18,951 |
| Arbiter LUT / FF | 185 / 187 | 234 / 187 |

The processor delta is -39 LUT/+10 FF; arbiter growth is +49 LUT/0 FF; the two changed blocks' own logic totals -110 LUT/+6 FF. These stay inside the assignment's 60-LUT/120-FF stop limits. The five reported worst arbiter paths move to registered CA-release sources at 14–16 levels. The new mask's own input remains 28 levels with reported +7.229 ns slack. The measurement was made at `912ee6ef`; its HDL and synthesis inputs are unchanged at this head. The public summaries support an arbiter-cone improvement, not a claim that every processor cone is below 20 levels. Full measurement tables and worst-five endpoints are in [the public evidence excerpt](receipts/public/handoff-evidence-excerpt.md).

**Independent execution and Docs.** The scoped simulator's 5.050 identity was verified before use. Independent work ran concurrently in disposable trees, with bounded compilation and campaign concurrency, explicit job counts and all subprocesses joined. Peak unit memory was 5,100,855,296 bytes under the 12-GiB cap. No source checkout was modified by a probe.

| Review-owned check | Result | Receipt |
|---|---|---|
| Arbiter suite | 66/66 pass | [stdout](receipts/tx-arbiter.sim.log) |
| Originator suite | 107/107 pass | [stdout](receipts/originator.sim.log) |
| Notification clean control | 42 default + 4 identify; all pass | [stdout](receipts/withdraw-campaign/golden-aecp_notify-run.sim.log) |
| WD clean control | 3/3 pass; acceptance sends one probe, selection sends none | [stdout](receipts/withdraw-campaign/golden-pp_top-withdraw-only.sim.log) |
| Three new mutants | Unregistered mask: WD1/WD2; ignored abort: WD2/WD3; delayed cancel: IX3/CX1 | [results](receipts/withdraw-campaign/results.json) |
| Five arbiter faults | All detected; 13, 6, 23, 30 and 2 failures, matching the published current-shape records | [results](receipts/arbiter-mutants.json) |
| Every bench patch | 283/283 apply at base and head | [audit](receipts/patch-plants.json) |
| Exact-text controls | 296/296 plant at this head, including admission and retry tables | [audit](receipts/exact-text-plants.json) |
| `make -j16 check` | Pass: diagrams, freshness, links, figures, IDs, parameters and matrices | [log](receipts/docs-check.log) |

The changed architecture withdrawal row, WD/CX explanations, build routing, mutant names and current failure counts match the implementation and executed results. The old historical mutation counts are distinguished from the new rerun paragraph. The PR correctly says “Relates to #163” and assigns the parent sweep to adoption. Public broad-bank summaries report 1,028,239 processor checks, including pp_top 10,447 and aecp_notify 46, all campaigns passing, and all 17 consumers passing at parent dev `28f9666f` with the 148 and 22 patches. Those broad banks were not repeated here. The manager's source static/builder and native passes are also stated in the review assignment; they are source validation, separate from final current-dev composition.

**R519-1-S1 — SUGGESTION — Tests, Docs.** Artifact: the immutable public evidence inventory and its handoff §1/§9. Authority/evidence: #163 asks for all arbiter cones and endpoints; the public packet contains grouped summaries and hashes, but omits `scripts/arb_cone.tcl`, the complete integrated endpoint/pair TSVs and full timing reports. Impact: a public reader can reconcile every register family and the reported totals, but cannot independently inspect or replay the traversal from this packet alone. Requested outcome: publish the exact traversal script, sequential-cell/pin inventory and full before/after pair reports with their hashes alongside the evidence. Verification: reproduce the 187-cell coverage, listed endpoint pins, 263,154/17,990 pairs and 146,535/0 above-threshold totals with the same recipe. This is an evidence-replay improvement, with no identified incorrect measurement or blocking acceptance defect.

The reviewer-owned ledger is:

| Lens | Status | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Frozen issue/assignment; architecture interfaces/timing; #653 UNB authority; cone inventory and OOC tables | R519-1 | cd9825c947cf67b735d26cc1c42541ccd9d7f637 |
| RTL | CLEAN | Complete two-file RTL delta; originator, release merge, slot pool and prepend shim; public sequential comparison; arbiter suite | R519-1 | cd9825c947cf67b735d26cc1c42541ccd9d7f637 |
| Robustness | CLEAN | Reset, concurrent retirement/acceptance, pending events, queue removal/reuse, backpressure; originator session; WD and arbiter faults | R519-1 | cd9825c947cf67b735d26cc1c42541ccd9d7f637 |
| Tests | CLEAN | New bench/helper/driver changes; clean WD/CX; eight executed faults; 283 patch and 296 exact-text arms; public consumer comparison | R519-1 | cd9825c947cf67b735d26cc1c42541ccd9d7f637 |
| Docs | CLEAN | Documentation guide and authorities; withdrawal row; three READMEs; PR scope and measurement claims; documentation gates | R519-1 | cd9825c947cf67b735d26cc1c42541ccd9d7f637 |

Public prior FINDINGS were checked only after the independent diff pass and the reviewer's own verdict and ledger were written. No earlier FINDINGS existed on the inspected issue comments, PR comments, submitted reviews or inline-review surface. [The observation receipt](receipts/prior-findings-observation.json) records all four surfaces.

Limits and pending manager duties:

- Review the merge of processor main `2ad2f845` as a delta. Preserve DN and its nine controls plus WD/CX. Recheck both pp_top builds, affected campaigns and the assigned source/consumer banks; the stated 10,459-check main baseline plus WD's three is 10,462 if nothing else changes.
- Build and validate the final current-dev candidate at adoption. Source base `86a7b0c5` and live parent dev `6714181d0c8a16e2983f85b724f4d688f5111835` are distinct. Run the three placement directives on the merged pin and require each WNS to reach +0.03 ns. No adoption route was run in this review.
- Hosted observation at this exact head showed successful portability and documentation jobs, with suites still running. No observed job was skipped; a running context receives no pass credit. Hosted and local workflow acceptance remain manager-owned. [Receipt](receipts/hosted-observation.json).
- Physical calibration is NOT RUN. The published builder calibration omission and guarded/field skips provide no hardware proof. No hardware, field exercise, full-bank rerun or fresh normative-PDF audit was performed here. The unavailable complete cone traversal and broad raw bank logs bound independent replay as described above.

Final checkout verification matches all 562 tracked entries by raw blob bytes and executable/symlink mode, and matches every index entry to the assigned tree. Status is empty. This processor tree has no gitlinks; no parent checkout or parent submodule was mutated. [Integrity receipt](receipts/checkout-integrity.json). No source fix, commit, push, merge, external write or author contact occurred.

Portable review scripts are under `scripts/`; each source-dependent runner accepts `--repo` or `--compiler` as appropriate. Simulation receipts contain verbatim trace/failure/tally lines, with full-capture hashes in `receipts/simulation-receipt-provenance.json`. Disposable trees and full local build captures remain under `scratch/`, outside publication. `MANIFEST.sha256` lists every publishable file using packet-relative paths.

R519-1 FINISHED

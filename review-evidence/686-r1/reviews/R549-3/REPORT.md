[R549] NEGATIVE - exact head 9c601b5983acfd60fb269b9a88c27b48cab7cf65

Round R549-3, external independent delta review of issue #686 / PR #695. Tree: `d2337a496fb13813beb2f4a13aefcaca0e0a94db`. All five lenses were applied. The documentation correction is accurate, the receipt manifest is repaired, and the focused executable checks pass. No new source defect was found. The exact-source bank-publication portion of prior MAJOR R549-1-F4 remains open: the published broad banks validate an explicitly different merge-candidate commit.

This does not allege any failed source or candidate bank. No RESIDUE finding is added.

The public authorities are [issue #686](https://github.com/kebag-logic/milan-fpga/issues/686), [assignment 6043036997](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6043036997), fourth-PROBE addition 6029233665, and [round-2 scope decision](https://github.com/kebag-logic/milan-fpga/issues/686#issuecomment-6047563934). IEEE 1722-2016 Annex B was read directly, including B.2.1, Table B.7 and its notes, Table B.8, B.3.4, B.3.6.1 and B.3.6.4-6. Repository authorities examined include AGENTS.md, CONTRIBUTING.md, docs/README.md, REQUIREMENTS.md section 1, FR-MAAP-01, the MAAP port contract, CSR MAC defaults and resource recipe. The independent verdict and ledger were written before opening prior reviewer findings; reconciliation followed that pass. No private author material, other checkout or private management material was used.

**R549-1-F4, retained in part | MAJOR | Conformance, RTL, Tests, Docs | exact-source manager bank receipts remain unlocated.**

- Artifact: [archive 319f3567, manager-candidate](https://github.com/kebag-logic/milan-fpga/tree/319f3567ed693bc5dffd422164a768c142485a2d/review-evidence/686-r1/manager-candidate), specifically both banks' results, completion and initial-integrity records; [manager comment 6052017268](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6052017268). Audit receipts: `receipts/evidence-audit.json`, `receipts/public-inventory.json`.
- Authority/evidence: [R549-2](https://github.com/kebag-logic/milan-fpga/pull/695#issuecomment-6051015769) explicitly retained publication of the reported exact-source manager logs/statuses with commit/tree association. Both new banks instead name candidate `1351f398f9e0c246888b9ac5286db8370a3bc1f3`, tree `140c3b838ef3a1f72e2669744871a48b83911311`, base `b959830acd53a868febfe362974e33e144481aa7`. The manager identifies these as candidate validation, not source-head validation. The supplied archive's `author-r2/` contains HANDOFF.md, PR-BODY.md and resource receipts, but no broader source-bank logs. The full path inventory, issue/PR comments, and empty submitted-review/inline-comment populations supply no other location.
- Impact: candidate results are now inspectable, but do not establish the reported separate runs at source head `9c601b59` / tree `d2337a49`. Treating them as those source receipts conflates different validated populations. No incorrect RTL or invalid candidate result is alleged.
- Required outcome: publish or link the existing exact-source manager bank logs/statuses and their commit/tree association. This remains a publication duty; no source fix or new full-bank execution is requested.
- Verification: inspect their commands, completion statuses and integrity records against the source head/tree, retaining separate identification of candidate `1351f398` and physical skips. F4's resource portion is resolved; this remainder retains the original severity and all four lens labels.

The requested `e21c1ca0..9c601b59` comparison contains 95 paths, including earlier imported dev work. Comparing with imported dev tip `291710b1` isolates 20 lane paths; `48f12dc1..9c601b59` changes only `docs/design/MAAP_FABRIC.md`. There is no round-3 RTL, test, resource-record or gitlink change. `receipts/history.txt` and `receipts/round3.diff` record that distinction. This is a delta review using the round-2 code baseline, not an exhaustive new review of the imported firmware lane.

The seed correction matches the actual reset path:

| Exact-head artifact | Result |
|---|---|
| `hdl/ieee1722/maap/KL_maap.sv:147-149,286-292,315-316` | Reset samples folded `station_mac_i`, with zero replaced by `0xACE1`. After reset, only the recurrence updates the LFSR; later MAC writes do not reseed it. |
| `hdl/milan/milan_datapath.sv:2465-2466,7066-7071` | CSR and MAAP share `axis_clk` and active-low `axis_resetn`; MAAP receives the byte-reversed CSR MAC. |
| `hdl/common/csr/milan_csr.sv:1553-1556,1662-1663,2648` | Reset clears both MAC registers. Later writes program the output. Byte reversal preserves the zero reset value. |
| `docs/design/MAAP_FABRIC.md:90-103,134-141,175-176` | Separates the module input contract from shipping integration: shipping reset seeds `0xACE1`; seed timing joins the B.3.6.1 follow-up. |
| `scripts/seed_probe.cpp`, `receipts/focused/seed_probe.log` | Seven checks pass. Two zero-MAC reset instances seed identically; differing later MAC writes leave identical evolution over 65,535 cycles. Distinct reset-time MAC inputs change module seeds. The zero-fold fallback advances. Exhaustive one-step checks show zero is the only fixed point and no nonzero state enters it. |

The probe exercises module input timing; actual CSR wiring was checked statically. It is not a full datapath simulation or hardware reset measurement. The corrected text claims neither B.3.6.1 compliance nor station-specific shipping seed diversity. The generator limitation remains a frozen follow-up, not a defect newly deferred in this round.

| Executable evidence | Result and scope |
|---|---|
| `receipts/focused/clean.log` | 130 checks, zero failures: clause-based frames, timer bounds, four-PROBE sequence, conflict cells, empty/adjacent ranges, disable/re-enable and frame preservation. |
| `receipts/focused/results.json` and per-case logs/statuses | Clean control and all 26 named defect cases pass campaign criteria. Each defect builds and exits 1 at its required failing check. Including the seed probe, 28/28 rows pass. Build failure cannot count as a kill. |
| `receipts/em-dash.log`, `receipts/toc.log`, `receipts/diff-check.rc` | Documentation and whitespace checks pass. The round-3 wording check examines 17 added lines; all 339 controls pass. |
| `receipts/resource-checksums.log` | `sha256sum -c MANIFEST.sha256` at archive `16f2f7ea26ffdc67d314b9e4074cd794c7f9bcb3`: all 186 listed files pass, including the four orchestration scripts. |
| `receipts/evidence-fetch.log`, `receipts/evidence-downloads.json` | 252 selected public blobs verified against Git object IDs. All 186 resource-file provenance entries are preserved from `84add8ed`; the checksum manifest's own entry changes. The complete top-level manifest is not byte-identical because the archive gained files. |
| `receipts/evidence-audit.json` | All three published round-2 records equal the source head's baseline records. Rehashed 122 repository inputs for route-1x1 and 119 for each standalone endpoint. Resource inputs are unchanged. Full parser regeneration remains baseline evidence, not a new execution here. |
| `receipts/public-candidate/manager-builder/` | 48/48 zero command statuses and 48 numbered logs; results/completion/integrity agree on candidate commit/tree. |
| `receipts/public-candidate/full-native/` | 5/5 zero statuses, with logs for parent suites, portability, both processor banks and behavior tests. These are inspected manager executions, not reviewer reruns. |
| `receipts/hosted-checks.json`, `receipts/hosted-job-steps.json` | Exact-head association: 22 successful checks, one skipped Physical gPTP job. All five simulation shard execution steps and four portability shard execution steps succeeded; these were not skipped aggregates. Manager owns hosted/local-replica acceptance. |
| `receipts/checkout-final.json` | Exact head/tree, index, tracked bytes and modes pass for 1,187 root files and 880 files across all three required submodules. No source restoration was needed. |

The unchanged source route record is 50,391 LUT, 54,263 FF, 15,788 slices, WNS +0.241 ns, WHS +0.029 ns. Standalone records are 23,179/19,779 and 30,135/27,380 LUT/FF. Their negative OOC setup estimates are not routed timing closure. No new synthesis or implementation measurement was performed.

| Validated population | Commit / tree | Evidence boundary |
|---|---|---|
| Reviewed source | `9c601b5983acfd60fb269b9a88c27b48cab7cf65` / `d2337a496fb13813beb2f4a13aefcaca0e0a94db` | Focused checks, tracked-byte integrity, documentation delta and unchanged resource inputs verified here. The reported broad manager source runs remain the publication finding above. |
| Published candidate | `1351f398f9e0c246888b9ac5286db8370a3bc1f3` / `140c3b838ef3a1f72e2669744871a48b83911311` | Receipt association, 48/48 builder and 5/5 native statuses. Base `b959830acd53a868febfe362974e33e144481aa7` is publicly identified as #654's candidate on dev `99e4eb6c14462aafa84bb1ac597fd241abc1a240`. |
| Physical acceptance | No measurement | Builder gate 11 explicitly lacks its real calibration report; Physical gPTP is skipped; bench MAAP interoperability is NOT RUN. |

Candidate and parent objects were unavailable through the public commit API. Their association above is therefore a cross-check of published integrity/results/completion receipts and the public merge-train statement, not an independently reconstructed candidate tree. The final live-dev candidate and any resource re-baseline remain merge-turn duties. A successful process containing a calibration skip does not discharge that arm.

Prior public findings are resolved or retained as follows, preserving all attributed lenses:

| Finding | Disposition | Evidence at this head |
|---|---|---|
| R548-2-F1, MINOR, Conformance/Docs | RESOLVED | Corrected MAAP_FABRIC text; reset/CSR chain and seven-check probe above. |
| R549-2-F1, MINOR, Tests/Docs; R548-2-E1, MINOR, Docs | RESOLVED | 186/186 public checksums pass; original/published provenance mapping preserved; manager correction identifies path-redacted bytes. |
| R549-1-F4, MAJOR, Conformance/RTL/Tests/Docs | PARTIALLY RESOLVED; source-bank remainder RETAINED | Resource evidence is checkable. New candidate receipts validate their explicitly different commit/tree. |
| R549-1-F1 = R548-1-F3, all five lenses; former R548 R1 | RESOLVED | `KL_maap.sv:149,292`; fallback checks and both zero-seed defects caught. Manager's MAJOR severity ruling respected. |
| R548-1-F1, Tests/Robustness | RESOLVED | `sim_main.cpp:419-441`; named guard-removal defect fails the requested mid-frame byte check. |
| R548-1-F2, Conformance/Docs | RESOLVED | `MAAP_FABRIC.md:144-149`: repeated PROBEs distinguished from the fourth's immediate ANNOUNCE and compare_MAC consequence. |
| R549-1-F2 = R548-1-F4; former R548 R2, Docs | RESOLVED | `KL_maap.sv:222-228`, `MAAP_FABRIC.md:64-69`, PR body: source MAC/count remain live. |
| R549-1-F3 = R548-1-F5, Conformance/Docs | RESOLVED | `MAAP_FABRIC.md:50-53,151-153`, module page and `new_off_w`: clipped random ranges distinguished from unvalidated supplied offsets. |
| R548-1-S1 | RESOLVED | Own-empty-range check and killed supporting defect. |
| R548-1-S3 | RESOLVED | `mutants.py`: supporting item 0 cannot satisfy the required-item guard. |
| R548-1-S4 | RESOLVED | `milan_datapath.sv:267-286`: corrected area and four-PROBE comments. |

These optional suggestions remain and do not make a lens unclean. Their narrower mutation probes were not independently rerun here.

| ID / severity / lenses | Artifact and authority/evidence | Impact | Outcome and verification if adopted |
|---|---|---|---|
| R548-2-S1 / SUGGESTION / Tests, Robustness | `sim_main.cpp:419-441`; prior public finding identifies missing beat-zero and streaming windows | Current guard-removal check proves its mid-frame stall window only | Extend stimulus to both windows and kill the corresponding narrow guard defects; optional. |
| R548-2-S2 / SUGGESTION / Tests, Robustness | `sim_main.cpp:491-497`; own-empty-range stimulus is in PROBE | No separate ANNOUNCE-state proof for that predicate | Repeat with zero own count in ANNOUNCE, require unchanged defends and kill the state-specific defect; optional. |
| R548-1-S2 / SUGGESTION / Tests, Robustness | `KL_maap.sv:353`; prior finding and PR follow-up list | No comprehensive truncated-PDU gate proof | Add truncated-input cases and a gate-removal control in follow-up; optional, outside the frozen correction items. |

The reviewer-owned completion ledger is:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN: retained F4 publication duty | Issue scope and Annex B; `MAAP_FABRIC.md:90-103,134-149`; `KL_maap.sv:118-129,202-224,269-277,362-409`; source/candidate inventory. Seed-description correction passes. | R549-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| RTL | UNCLEAN: retained F4 publication duty | `KL_maap.sv:147-149,286-316`; `milan_datapath.sv:2465-2466,7066-7071`; `milan_csr.sv:1553-1556,2648`; resource-input and checkout integrity. No new RTL change or observed failure. | R549-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Robustness | CLEAN | `KL_maap.sv:202-224,269-277,374-409`; `sim_main.cpp:419-500,577-617`; zero-seed, reset timing, ranges, conflicts, disable and backpressure results in `receipts/focused/`. Optional suggestions retained. | R549-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Tests | UNCLEAN: retained F4 publication duty | MAAP harness/campaign; differential and crflic consumer changes; 130 clean checks, 26 named kills, seed probe; manifest and bank-scope audits. | R549-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |
| Docs | UNCLEAN: retained F4 publication duty | `MAAP_FABRIC.md:50-69,90-103,134-176`; module page; PR body; resource records and public inventories. Round-3 prose and checksum fixes pass. | R549-3 | 9c601b5983acfd60fb269b9a88c27b48cab7cf65 |

Limits: no full parent/processor banks, builder banks, synthesis, implementation, local workflow replication or hardware were run here. Unchanged differential and coverage measurements were not rerun. Scaled unit-clock timing is not bounded wire-timing proof under arbitrary stalls. Existing declared deviations remain outside the four correction items: B.3.6.1 generator/seeding, two compare_MAC cells, requested-field echo, PortOperational, busy-TX PROBE loss, tagged reception and supplied-seed validation.

The manager must publish/link the exact-source bank receipts and obtain re-review of retained F4; finish the final current-dev candidate and applicable resource re-baseline; own hosted/local-replica acceptance; and perform the assigned post-merge bench interoperability acceptance. Physical calibration is NOT RUN, and field skips are not hardware proof. Merge still requires the full review bar, no round in flight, explicit maintainer authorization and post-merge containment. This review made no source edits, commits, pushes, GitHub writes, merges or author contact.

Portable reproduction:

```sh
python3 scripts/run_focused.py --repo <checkout> --verilator <pinned-compiler>
python3 scripts/fetch_evidence.py
python3 scripts/audit_checkout.py <checkout>
python3 scripts/audit_evidence.py <checkout>
```

The evidence audit fetches its read-only API snapshots when absent; its published outputs preserve this round's evaluated associations and statuses. `MANIFEST.sha256` names every publishable receipt and script. Only listed files and this report are intended for publication. `scratch/` is excluded.

R549-3 FINISHED

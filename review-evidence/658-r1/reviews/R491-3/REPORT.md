[R491] POSITIVE - exact head 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57

Round R491-3, external independent review of issue #658 / PR #670. Tree: `09e56fc45c22d563612af8602d2e6ef67d954a49`. Source base: `e617275074e370cec342af99b929e2588fc8d43f`.

All five lenses are CLEAN. No new BLOCKER, MAJOR, MINOR or RESIDUE was found. Earlier resolved findings remain resolved; three suggestions remain optional. This verdict covers the published source head, not completion of the manager's merge and release duties.

Reconstruction followed AGENTS.md, CONTRIBUTING.md, docs/README.md, the public issue and scope decisions, requirements/interfaces, source diff/history, then public executable evidence. The source comparison was separated into upstream imports and the lane delta. `independent-verdict.md` records my verdict and ledger before prior reviewer reports were read. No private author material or pre-existing checkout outside this review was read.

The [stage-2 decision](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-5988843004) supersedes runtime adaptation-driven pruning: identity defaults and boot clipping are required, while Milan v1.2 5.4.2.7 retains BAD_ARGUMENTS when a format would orphan a mapping. The [round-3 assignment](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-6009196984) permits the dev merges and unchanged table extraction. Local authorities examined include REQUIREMENTS.md sections 1/3/8, `SAVED_STATE_MATERIALIZATION.md` sections 1/5.2/8.4, `ENDSTATION_BUILDER.md` D7/D8, `REGISTER_MAP.md` 0x900, and the pinned processor's `docs/architecture/07_memory_maps.md:570` and `02_interfaces.md:397`.

**Round-3 results**

- Both merges have the required two ordered parents. Recomputing their automatic merges succeeds without conflicts and reproduces their recorded trees: `c79c178e` gives `edb11ab6fce6f54a8c466bb242ab0e5490128645`; `0f3d37db` gives the reviewed tree. This proves merge preservation, not the final candidate's execution gates.
- The first merge's sole overlap with lane-changed paths is `scripts/measure_test_evidence.py`: it imports the upstream mailbox disposition. Existing lane entries, RTL and tests are preserved. The second merge touches no lane-changed path. Thus “no lane file changed” needs this qualification; neither merge rewrites a lane-owned hunk. Receipts: `structure.json` and the two `merge-*.patch` files.
- The extracted assignment is 135 lines, 9,843 bytes and 35 entries. Both SHA-256 values are `ad10ad7a7409b6808cc6658a619d9007c63d50fc68afd73df8962bde7eedc193`. Parsed item order is identical. Removing the moved assignment and new import leaves identical main-module syntax trees. The new module contains only documentation and the data assignment.
- The main module falls from 1,002 to 869 lines; the data module has 154. `scripts/py_idiom.budget` is byte-identical at the source base, previous positive head, extraction parent, extraction commit and final head: SHA-256 `d4268e92ca9ed205dbf22323e1666738c38d5952b8fcd354c4b6cf0be65ea846`. The old tree fails specifically with `long module 11 > ratchet 10`; the final tree passes at `10 <= 10`. Every other ratchet passes unchanged. The new module has zero findings under every rule.
- No registration is required. `ci_scope.py:107` classifies this path as relevant; its selftest passes. The quality population includes the tracked new module. `.github/workflows/docs.yml:313` and `:356` run the importing gate and quality gate. The separate no-git job checks documentation, not a curated helper inventory. `CODE_QUALITY.md:1761` names the actual table location.

**Executed evidence**

The real commands ran in registered disposable clones at `c79c178e` and `e8f7d247`, and in the reviewed clone at the final head. All three modes have identical stdout, stderr and exit-code bytes across all three revisions. Each exits 0; stderr is empty.

| Mode | SHA-256 of identical stdout |
|---|---|
| default | `29d2df9da1246aafd0d9e2e0ed855a9c97d6ed7a8d904454dbae468c31fda589` |
| `--check` | `4322b73a4b194c5aedc7a75ca57b7e20bbecce56a56032963eb515d2e1892a2a` |
| `--selftest` | `3c818777e9f41c6d64a15fa699cd238a94b030f0ce19981df099f855b97416ba` |

The measurement selftest passes 101/101; the idiom selftest passes 54/54. The measurement reports zero unexplained readers and no stale dispositions. Removing the lane's reader from the disposable table returns 1 and names it UNEXPLAINED. Adding a nonexistent reader returns 1 and names the stale disposition. These controls demonstrate that the imported table still controls the verdict. An absolute invocation from a different working directory also produces identical `--check` output.

Documentation hygiene passes with zero findings. All 925 cited paths resolve subject to the existing one-entry allowlist. `commands.json`, `additional-commands.json` and their named stdout/stderr/rc files preserve the results.

Portable reproduction, with SOURCE and PACKET supplied as arguments:

```sh
python3 review_checks.py SOURCE PACKET
python3 additional_checks.py SOURCE PACKET
python3 audit_integrity.py SOURCE PACKET/integrity.json
```

Foreground supervisors joined all children, with at most six concurrent lightweight checks. No native build or simulation ran in this round. Two setup attempts were non-evidence: an unsupported idiom-gate `--check` option returned 2, and unpersisted temporary submodule URLs made scratch scans refuse their population. The final reproducer uses the supported CLI and registered submodules. Diagnostic receipts remain in `idiom-invalid-cli.*` and `initial-unregistered-*`; they are not product failures or passes.

**Prior finding reconciliation**

Sources: [external round 1](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-5997138134), [internal round 1](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-5997255034), [external round 2](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-6008892870), [internal round 2](https://github.com/kebag-logic/milan-fpga/pull/670#issuecomment-6009191874). Submitted reviews and inline comments were empty. Reconciliation checked the current files and PR body; comparisons are in `prior-findings-checks.json`.

| ID | Severity; lenses | Disposition at this head |
|---|---|---|
| R490-1-F1 | MINOR; Tests | RESOLVED, retained. `sim_nxn.cpp:4334`, `:4436`, `:4472` stage CSR commits across CLOSED, rollback on the terminal, and an edit meeting the sweep. `dynmap_mutants.py:113` carries their removal controls. Those files, the probe configuration and Makefile are byte-identical to the round-2 positive head. The accepted shipping-shape RAM-site rationale remains in `milan_dp/README.md:800`. |
| R490-1-F2 | MINOR; Docs, Tests | RESOLVED, retained. The current PR body says the gPTP leg grades release/post-walk usability and does not grade refusal while the hold is up. `sim_ax1x1gptp.cpp:705` onward is unchanged. |
| R491-1-F1 | MINOR; Docs | RESOLVED, retained. `SAVED_STATE_MATERIALIZATION.md:1216` preserves the requested distinction: no clip-triggered persistence work, sticky live-map pending on controller edits, unmaterialized map records in stages 1/2, stage 3 owning their writer. |
| R490-1-R1 | RESIDUE; Docs | RESOLVED, retained. `CHANGELOG.md:55` retains the accepted two-sentence refusal and duration wording. |
| R490-1-R2 | RESIDUE; Docs | RESOLVED, retained. `REGISTER_MAP.md:2160` retains the exact per-dynamic-direction qualification after whitespace normalization. |

Retained suggestions, requiring no change for this PR:

- **R491-1-S1; SUGGESTION; RTL.** Artifact: `milan_datapath.sv:4358`, `:4550`. Authority/evidence: the existing shipping-shape specialization suggestion and unchanged wait/sweep implementation. Impact: possible area saving, still unmeasured. Required outcome: none; a later specialization must preserve arbitration wherever an edit can overlap the sweep. Verification: isolated synthesis comparison and queued/overlapping-edit plus larger-shape checks.
- **R490-1-S1 / R490-2-S2; SUGGESTION; Tests.** Artifact: `capture_coherence/sim_dp.cpp:257`, `milan_dp/sim_nxn.cpp:4181`. Authority/evidence: the unchanged talker check runs inside the boot window; the dynamic-map leg separately checks post-release capture RAM. Impact: a post-release talker run would make the end-to-end proof more direct. Required outcome: none; optionally add that run. Verification: decode slot-to-stream identity after a real restore terminal without a map command, with an empty-image control.
- **R490-2-S1; SUGGESTION; Tests.** Artifact: `milan_datapath.sv:6786`, `milan_dp/README.md:800`. Authority/evidence: the accepted shipping-shape equivalence rationale remains limited to that shape; the prior review identifies sparse physical render keys on the future-board configurations. Impact: the correct RAM-side guard lacks a dedicated regression on that future scope. Required outcome: none here; carry to #583 if that work resumes. Verification: a CSR render write across that shape's sweep must detect removal of the RAM-side guard.

**Reviewer-owned ledger**

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Decisions 5988843004/6009196984; `milan_datapath.sv:4396` identity/clip; processor memory-map contract; table byte/order and output comparisons in `structure.json` / `commands.json`. Protocol behavior is preserved. | R491-3 | 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57 |
| RTL | CLEAN | `milan_datapath.sv:4358`, `:4535`, `:4562`, `:4629`; parent-merge comparisons; unchanged lane RTL and pins in `prior-findings-checks.json` / `integrity.json`. No lane clock, reset, width, interface or arbitration change. | R491-3 | 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57 |
| Robustness | CLEAN | `measure_test_evidence.py:722`, `:748`, `:835`; missing/stale-reader refusal receipts; foreign-directory import; unchanged terminal/drain/CSR tests at `sim_nxn.cpp:4334`. | R491-3 | 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57 |
| Tests | CLEAN | Real CLI outputs at extraction parent, extraction commit and final head; 101/101 and 54/54 selftests; old ratchet failure; two named data controls; `ci_scope.py:107`; `.github/workflows/docs.yml:313`; retained mutation definitions. | R491-3 | 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57 |
| Docs | CLEAN | `CODE_QUALITY.md:1761`, new module documentation, `ENDSTATION_BUILDER.md:624`, `SAVED_STATE_MATERIALIZATION.md:1216`, `REGISTER_MAP.md:2160`, PR evidence limits; documentation/path gates and correction checks. | R491-3 | 0f3d37dbffc4ca3f0e0f69499de80fc256a7db57 |

**Real limits and manager duties**

Selected executable receipts from the [published packet](https://github.com/kebag-logic/milan-fpga/tree/d445cbd4d2dadfa01fbefc36bec82d9ffde5695f/review-evidence/658-r1) match its SHA-256 manifest. They are historical source evidence: that packet's dynamic-map campaign reports 9/9, not the later 16/16. Round-2 positive evidence stands for unchanged lane inputs. The [round-3 readiness comment](https://github.com/kebag-logic/milan-fpga/issues/658#issuecomment-6010201071) records 48/48 builder command exits and merged-feature banks. Those banks were not rerun here. Its nested builder gate 11 is explicitly NOT RUN for a missing place report; a successful aggregate does not turn that into a measurement.

`hosted-checks.json` is an exact-head snapshot, not hosted acceptance. Four synthesis shards, lint, behavior checks, wire accountability and the no-git documentation context had succeeded. Regular documentation, elaboration and five simulation shards were still running. The physical-named job was skipped. The manager owns final hosted and local-replica acceptance.

The manager must validate the final candidate against current dev, using the source base above and the stated live dev `423ac5d910d09ab189b3acc39ae3ae1d10d50b19`, or its newer successor at merge time. Source banks and clean parent merges do not discharge that duty. Subsequent changes reopen affected lenses. Complete the other independent review, close all rounds, meet resource/merge gates, obtain merge authorization, prove containment, and close the issue/project state. A later #645 merge must place its reader entries in the extracted module and revalidate overlapping datapath work.

Physical calibration was NOT RUN. Digital simulation and field skips are not hardware proof. The post-flash power-on map read and physical release obligations remain with the manager. Map persistence remains #70 scope.

`integrity.json` proves 1,109 superproject blobs, 558 processor blobs, 104 gPTP blobs and 214 interface-library blobs equal their pinned raw bytes and modes. Every index equals its HEAD tree, no hidden index flags remain, and status is empty. Required pins are `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`. The unused external gitlink is unchanged and uninitialized. Mutations stayed in scratch copies and were restored. No source fixes, commits, pushes, GitHub writes, author contact, merges, full banks, container runs or hardware operations occurred. Only MANIFEST.sha256-listed receipts and this report are publishable; scratch is excluded.

R491-3 FINISHED

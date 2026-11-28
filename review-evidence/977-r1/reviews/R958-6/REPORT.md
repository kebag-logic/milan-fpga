[R958] POSITIVE - exact head a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35

R958-6 applied all five lenses to `4461d77ca34ec1203321821a3313071ff1923984..a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35`, the round-5 findings at their causes, and published author-r14 evidence. Tree: `222e3e20fa0f6313632775aabf4f74a26c4417fc`. **F1 is closed, and the publication-wording residue is resolved. No new finding or suggestion. All five lenses are CLEAN within this narrow review and the preserved prior coverage.**

The [owner decision of 2026-11-28](https://github.com/kebag-logic/milan-fpga/issues/977#issuecomment-7235670586) authorizes **0.79 at 8x8/1if**, with every other bound unchanged. Both Markdown authorities link it; source comments name the dated decision and #977 without a comment ID. The unchanged measured load, **0.7821365**, fits that ceiling. The 1x1/1if load remains **0.5325402076023392**, below 0.70.

Reconstruction followed AGENTS.md/CONTRIBUTING.md, docs/README.md, the issue body and public scope decisions, REQUIREMENTS ownership/NFR-SCOUT-03, FR_NFR 3.4.1 and SPLIT_CONTROL_MEMORY section 13, then source-base inventory/history, the narrow diff, and executable evidence. The source base inspected is `dev-soft-core` at `0b5940237e8de8bd5912db87e5e036a78f59b5a6`. Unchanged implementation retains prior coverage unless a changed dependency affects it. The independent delta pass preceded reading prior external findings. This verdict and ledger were written before consulting another reviewer's report. No private author material or other checkout was accessed.

**Prior findings at their causes**

| Finding | Disposition at this head | Authority and verification |
|---|---|---|
| R958-4-F1, retained by R958-5; MAJOR, Conformance | CLOSED | Owner decision 7235670586 supplies the authorization required by manager decision 7229657853 item 4. `flip_grade.py:26,64,69,72` and `load_grade.py:134` name it; `FR_NFR.md:427` and `SPLIT_CONTROL_MEMORY.md:2548` link it. FLIP and RULED_FLIP hold 0.79. Independent load/edge checks pass. |
| R958-5-R1; RESIDUE, Docs | CLOSED | Live PR Contents/Status now says the historical index notes are published and links both. The r10/r11 `receipts/SUPERSESSION-NOTE.md` files exist at linked commit `63ebbbacee3d6c366274d0b756f86433a7588a30`; their bytes match the current packet. All twelve mapped published receipts match the manifest. |
| R958-4-F2; Conformance/RTL/Tests/Docs | Remains CLOSED by R958-5 | R958-5 verified 44 distinct record associations per point, exclusions, invalid-association controls and unchanged maxima. This delta changes no extractor, trace, cost, floor, rate or calculation. `load_grade.py:374-389` and `SPLIT_CONTROL_MEMORY.md:2548` retain that method and figures. No new extraction is claimed. |
| R958-4-R1; Docs | Remains CLOSED | The combined delta from `3256d1d2` replaces the source comment ID with the dated deferred-deliveries decision. Latest source-comment additions introduce no review identity, round, bench label, lane name or comment ID. |
| R958-4-R2; Docs | Remains CLOSED, including the summary residue above | Both supersession notes and mapped receipts verify; archived indexes keep their historical bytes. |

Earlier round-4 closures named in round 5 stand: baseline/floor authority, malformed-ceiling and unnamed-control adapters, neutral reviewer labels, cost-method wording/deliveries exception, and mutation-population wording. The delta changes none of their operative dependencies. Unrelated implementation, routing, S14, loss-turn and CDC/reset work is not reopened.

**Evidence and checks**

| Check | Result |
|---|---|
| Narrow delta | One commit; exactly four changed files, all comments/documentation: `flip_grade.py`, `load_grade.py`, FR_NFR and SPLIT_CONTROL_MEMORY. Executable ASTs match `4461d77c` after excluding docstrings. No firmware, RTL, build recipe or gitlink changes. |
| Combined later delta | `3256d1d2..a5b19f70` changes five files. The additional file is `load_deliveries.py`, whose docstring replaces a comment ID with the dated decision. All three Python executable ASTs match `3256d1d2`; final numeric ceilings and controls match it too. `delta-audit.json` records full commit identities and paths. |
| Loads | 8x8/1if **0.7821365**, displayed **0.78214**; without deliveries **0.7661365**. 1x1/1if **0.5325402076023392**, displayed **0.53254**. Delivery costs remain 160 and 200 us, respectively; rates remain V x 3 / 270 ms. `model-probe.json`. |
| Boundary/negative probes | FLIP = RULED_FLIP = `{8x8/2if: 0.70, 8x8/1if: 0.79}`; EDGE_1IF = `(0.790, 0.791)`. **0.790 passes; 0.791 fails.** The former 0.77 rejects the measured load. Lowering FLIP alone to 0.77 triggers both named controls; 155 us at 8x8 and 195 us at 1x1 fail the delivery floors. Mutations were in-process only. |
| Independent gates | Load check, load self-test **32/32**, delivery controls, both held-point flip checks, flip self-test **628/628**: all rc 0. Normal adapters report no failed checks. Whitespace checks against the source base and both review heads return 0. Commands/logs/rc files accompany `checks.json`. |
| Product identity | **80 unique paths per side, all 80 SHA-256 pairs equal to 25ff0632**: 72 harness and eight platform paths. The baseline also matches the separate round-10d receipt's 25ff0632 and measured e59cf6ea maps. This verifies published build/identity receipts, not a fresh build or direct rehash of unavailable binaries. `elf-identity-audit.json`. |
| Author source-head receipts | Published hashes verify. Harness aggregate: zero self-test failures; kept 33 checks; shape 25/25 and check PASS. Documentation receipt: 100 numbered steps, all rc 0. Its no-Git fixture explicitly skips inventory parity; the Git-backed step runs it. These are author receipts, **not a manager source bank**. |
| Integrity/signature | Current packet entries examined, both notes and mapped receipts match `MANIFEST.json` published hashes. Evidence commit `d963a0c0697795b4ad4f6247b7379bf5cddd81ad` has no signature header; public verification says `verified: false`, `reason: unsigned`. Hash integrity is established; a cryptographic packet signature is **not established**. This retains the prior limitation. |
| Checkout preservation | **1997 parent blobs and 1377 blobs across five required submodules** match committed bytes, modes and indexes. Required submodule HEADs match gitlinks; parent tree/status match the requested head and are clean. Optional external stays uninitialized with its gitlink preserved. `checkout-integrity.json`. |

**Reviewer-owned lens ledger**

[R958] PASS Conformance - `REQUIREMENTS.md:62`; `docs/reference/FR_NFR.md:427`; decision 7235670586; `flip_grade.py:69-73`; `model-probe.json` - ceiling authority is supplied and cited, the measured load fits, and other bounds remain unchanged.

[R958] PASS RTL - `previous-delta.patch`; `internal-delta.patch`; `delta-audit.json`; `elf-identity-audit.json`; `checkout-integrity.json` - no runtime, interface, placement, cost-calculation or pin change; R958-5's resource-cost and implementation coverage remains applicable.

[R958] PASS Robustness - `flip_grade.py:144-160,204-208`; `load_grade.py:374-389`; `model-probe.json` - exact-edge/over-edge behavior, lower-ceiling mutation and below-floor costs distinguish correctly. No reset, ordering, malformed-input or backpressure path changed.

[R958] PASS Tests - `flip_grade.py:69-75,180-214,460-467`; `checks.json`; focused gate logs; author-r14 harness receipts - controls and adapters still detect the stated defects, with 32/32 load and 628/628 flip controls refused. The accepted 0.79 now has public authority.

[R958] PASS Docs - `FR_NFR.md:427`; `SPLIT_CONTROL_MEMORY.md:2548`; `flip_grade.py:26-28,64-68`; `load_grade.py:134-135`; live PR summary and both supersession notes - limits, citations and publication wording agree with public state. No new wording residue in the requested delta.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Owner/manager decisions; FR_NFR:427; FLIP/RULED_FLIP; model probe | R958-6, closing retained F1 | a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35 |
| RTL | CLEAN | Delta/AST audit; 80-path identity receipts; tracked bytes/pins | R958-6, retaining unaffected R958-5 coverage | a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35 |
| Robustness | CLEAN | Ceiling-edge, lower-ceiling and lower-floor probes; unchanged executable paths | R958-6, retaining unaffected R958-5 coverage | a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35 |
| Tests | CLEAN | Focused gate logs/adapters; author-r14 receipts; unchanged extraction dependency | R958-6, retaining unaffected R958-5 coverage | a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35 |
| Docs | CLEAN | Dated authority citations; PR summary; both notes and mapped targets | R958-6, closing R958-5-R1 | a5b19f70a4ba63bf5a7bb4bd29b2056977a85e35 |

**Coverage after the internal positive**

**Yes: the entire later delta `3256d1d2..a5b19f70` is covered by R958-5 and R958-6 together.** R958-5 covered `3256d1d2..4461d77c`, closed the per-record measurement finding, and left the ceiling authorization plus publication wording. R958-6 covers the citation-only delta and closes both remaining items. The combined five-file delta is independently checked above. The [internal positive at 3256d1d2](https://github.com/kebag-logic/milan-fpga/pull/993#issuecomment-7230545660) remains evidence at its recorded head; it is not relabeled as an internal review at this head. This reviewer-owned ledger accounts for the later changes.

After the independent verdict and ledger were written, the internal positive's dispositions were checked. Its owner-answer condition is now satisfied. Its source-comment-ID residue R957-4-R1 is closed by the dated citations, and R957-3-R4/external round-3 R2 are closed by the published notes. The following existing optional items remain; they do not invalidate clean coverage or add implementation scope.

- **R957-4-R2 retained; RESIDUE; Docs; PR #993, Round 11 table, deliveries-term row.** Evidence: the live body still says "internal review F1, option (a)", without identifying the round. Impact: ambiguous historical attribution only; no numeric, test, behavior, clause or verdict changes. Exact fix: "the round-2 internal review's F1, option (a)". Verification: inspect that row in the published PR body. The manager carries this wording to the residue checklist.
- **R957-4-R3 retained; RESIDUE; Docs; `tb/verilator/ctrl_service_budget/load_grade.py:382`.** Evidence: the comment calls DELIVERY_MEASURED the floor, while the table holds raw cycles and `delivery_findings` applies `rule_us` to obtain the floor. The implementation and figures are correct and unchanged. Impact: wording only. Exact fix: "plus 5 %, rounded up to 5 us; DELIVERY_MEASURED holds the cycles, and their figure by the rule is the gate's floor: a cost stated under it is refused". Verification: compare the revised sentence with `delivery_findings` and the unchanged 160/200 us floor probes. The manager carries this wording to the residue checklist.
- **R957-4-S1 retained; SUGGESTION; Tests; `load_grade.py:963-965`, `selftest_mutants.py:539-541`.** Evidence: the load adapter's unnamed-escape branch is present, while the permanent unnamed-escape mutant targets the flip adapter. Impact: optional regression hardening. Suggested outcome: add a sibling control for an unnamed load escape. Verification: it fails when that load-only adapter branch is removed and passes at this head. No source change requested in this review session.
- **R957-4-S2 retained; SUGGESTION; Tests; `selftest_mutants.py:539`, `flip_grade.py:460-467`.** Evidence: the 0.71 plant is checked through the combined adapters, where an older load check can also catch it; the separate unnamed-escape mutant discriminates the repaired defect. Impact: optional control attribution. Suggested outcome: target `flip_checks()` alone or require the named ceilings-control failure. Verification: the targeted control distinguishes the repaired adapter from the pre-fix one. No new simulation or historical-tree execution is claimed here.

**Limits and pending manager duties**

ELF binaries and full CPU traces are absent from the public packet. No product rebuild, fresh simulation, raw-trace re-extraction, broad bank, scoped simulator, synthesis, hardware, source edit, commit, push, GitHub write or merge occurred. No other checkout or private management material was read. Physical calibration is **NOT RUN**; field skips are not hardware proof. Hosted jobs were not audited in this narrow pass; no skipped context counts as executed.

There is **no manager source bank at this exact head**. Source validation is the author's published receipts and the focused independent checks above. The manager owns hosted/local-replica acceptance and the final then-current-`dev` candidate, including builder/native banks and published receipts. Supplied live `dev` is `e275d7950ef3385753e6a15d2e191ba855b171ed`; this source review against `dev-soft-core` does not validate that future candidate. Final review-bar accounting, explicit merge authorization, containment, and issue/project completion remain manager duties.

Reproduce from the exact clone with `python3 -B <packet>/audit.py`, `python3 -B <packet>/model_probe.py`, `python3 -B <packet>/run_checks.py`, and `python3 -B <packet>/verify_checkout.py`. The first needs the public evidence commit and read-only repository API access. At most four lightweight checks run concurrently and wait in the foreground. Only REPORT.md and files in MANIFEST.sha256 are publication artifacts; scratch is excluded.

R958-6 FINISHED

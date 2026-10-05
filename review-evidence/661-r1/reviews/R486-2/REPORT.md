[R486] POSITIVE - exact head 3880c1eb6e2f927a07f98150d5b05a228f8f4efd

R486-2 is an internal independent source review of issue #661 / PR #663. Tree: `6bba0f2cf6c330ca1bd5cb012b571e69044b0dd7`. Source base: `506d91dbeeba585d72d2e80d92fca799c719f8ee`. The observed live dev tip is `fa450d301805881ad713b67521477bf042ddadfd`.

All five lenses are CLEAN for the assigned scope. No BLOCKER, MAJOR or MINOR remains open. R487-1 F1 and R486-1 F1/F2 are resolved. Two previously recorded wording residues and three optional suggestions remain below. This is source approval; final candidate validation, hosted/local-replica acceptance and release work remain the manager's duties.

The review reconstructed the repository contracts, documentation map, frozen acceptance and public decisions, linked authorities, full base-to-head diff and history, then public evidence. The independent verdict and ledger were written in `receipts/independent-assessment.md` before prior public findings were read. No private author material or other review packet was used. Unchanged round-1 coverage is retained under the assignment; changed artifacts were reviewed here.

**Authority and evidence.** The [original assignment](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5986065259) and [round-2 decision](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5991877761) authorize this adoption and its corrections. The P2 amendment agrees with the [deadline decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/15#issuecomment-5952386396); map ownership agrees with the [P1 decision](https://github.com/Mister-M-alt/protocol-processor-control-plane-avb-milan/issues/83#issuecomment-5967611704). All 20 files listed in the frozen [public manifest](https://github.com/kebag-logic/milan-fpga/tree/0010a410b0150c2c7043142fb64036a7d2655799/review-evidence/661-r1) match their published hashes. That packet describes round 1. The [round-2 validation statement](https://github.com/kebag-logic/milan-fpga/issues/661#issuecomment-5993741847) supplies the later results. These statements are distinguished from this review's own executions.

**Index rule.** `protocol-processor/hdl/adp/KL_adp_engine.sv:703` initializes zero, increments after ENTITY_AVAILABLE, and resets after ENTITY_DEPARTING, whose frame captures the pre-reset value. This matches the adopted IEEE 1722.1-2021 Section 6.2.2.15 rule and the processor's clause discussion at `tb/adp_engine/README.md:170`.

All five corrected locations agree: `docs/design/SAVED_STATE_MATERIALIZATION.md:1036`, `avdecc/gen_aemi_image.py:105`, `docs/reference/MILAN_COMPLIANCE_MATRIX.md:154`, `sw/builder/test_builder.py:26237`, and `tb/tools/avtp_wire_truth_checks.py:553`. The register-map correction at `docs/reference/REGISTER_MAP.md:1032` also agrees. The matrix no longer attributes a standards divergence to the adopted engine.

The exemption at `tb/tools/avtp_wire_truth_checks.py:588` requires both an immediately preceding DEPARTING and current index zero. The ordinary repeat check remains active. The committed four-arm test passes; the full wire self-test reports 25 tests, OK. Independently constructed wire bytes give:

| Sequence | Required and observed result |
|---|---|
| AVAILABLE 3, 4; DEPARTING 5; AVAILABLE 0, 1 | PASS |
| DEPARTING 0; AVAILABLE 0, 1 | PASS |
| DEPARTING 5; AVAILABLE 0, 0 | FAIL, one repeat |
| AVAILABLE 4; DEPARTING 5; AVAILABLE 5 | FAIL, one repeat |

Additional vectors cover an ordinary repeat, 32-bit wrap, repeated departure cycles and interleaved entity IDs. Three independently planted defects are each killed by the committed test: accepting any value after departure, accepting every zero, and accepting zero indefinitely after an earlier departure. Each mutant exits 1 with the intended assertion failure; the control exits 0. Receipts: `wire-probe.log`, `wire-selftest.log`, and `wire-*.log`/`.rc`.

**Merge and resource inputs.** The head has parents `ba57a3bc56dbc1883ba9f2230b45259b383e4ed6` and `fa450d301805881ad713b67521477bf042ddadfd`. A clean `git merge-tree --write-tree` produces the published tree exactly.

The only parent RTL delta since round 1 is `hdl/milan/KL_nvm_backend.sv:247`: a constant equal to 128 replaces the literal in the existing elaboration guard. No runtime datapath, state, clock, reset or interface logic changes. Gate 38 accepts 128 names, refuses 129 and 235 before writing, and catches nine planted defects. Its elaboration checks accept 128, refuse 129, and follow a planted capacity of 127. The processor top still has 212 ports with identical names; its parameter count changes 41 to 42 through the already reviewed `NVM_MEM_TMO_CYC_P` addition.

Source-list authorities, synthesis recipes, SoC source, firmware, configurations and required submodule pins are unchanged by round 2. Source-list checks pass, including 50/50 controls and the zero-record tops case. Fresh generation at `42f65447`, `ba57a3bc` and `3880c1eb` gives identical outputs for all five configurations: the reported 55-file scope plus ten packed-image metadata/layout files, 65 files per revision. `builder-equality.log` records every hash.

The resource baseline's tolerances, floors, ceilings, identities and kinds remain unchanged; `check-baseline` passes all three endpoints. The only changed first-party RTL input is the guard file, and generated image equality supports the source-input disposition. I did not independently reproduce the three original endpoint `inputs_sha256` values: the supplied public packet contains report/checkpoint digests, not those raw measurement directories. The public round-2 statement reports that restoring this file's measured bytes reproduces all three digests. No re-route was authorized or performed.

The retained route is 50,318 LUT / 54,214 FF / 15,789 slices, WNS/WHS +0.108/+0.036 ns at 50 MHz. The 60 percent LUT target remains unmet under #640. Capture validation passes with unchanged firmware, census and clocks; the retained 8x8 maximum is 13.86484 ms, below 24.5 ms. These are retained measurements, not new physical measurements at this head.

**gPTP and the retired exception.** The pacing change sends six samples per 3,072 modeled audio-clock edges, aligning the peer to the DUT's INTERNAL media clock. Payload, ordering, sequence, backpressure, loss and reset assertions remain.

R486-1 completed this suite on the clean merge of `42f65447` with the same dev tip: tree `57cc8b8afa04c315e99e5aa2f4bb84469f24df06`, physical 139/0 and accounting 6/0 + 20/0 + 14/0, make exit 0 ([public evidence](https://github.com/kebag-logic/milan-fpga/pull/663#issuecomment-5991604022)). I reconstructed that tree and proved its RTL, harnesses, recipes, firmware, configurations and pins identical to this head. The two Python dependencies changed only in comments, confirmed by equal parsed syntax trees; generated outputs were independently compared. Thus the completed prior result remains applicable. The public round-2 statement separately reports 139/0 + 40/0 at this exact head. The #656 exception is retired.

An additional independent rerun was started, then deliberately stopped after this equivalence was established. Its log ends with signal 15 and make exit 2; it is excluded from all passing counts. `gptp-inheritance.json` records the disposition, and `gptp.log`/`.rc` retain the incomplete run. This review does not claim a newly completed full simulation. The unchanged #657 exception remains the authorized 28 PASS / 4 FAIL render campaign, not a clean campaign claim.

**Prior findings.**

| Prior ID | Disposition at this head | Verification |
|---|---|---|
| R486-1 F1, MINOR, Docs | RESOLVED | Live body has placeholders, no host paths or named local account, and no privileged selector command. Corrected published copy at `8c01f837` uses placeholders. Both pass the privacy scrub. |
| R486-1 F2, MINOR, Docs | RESOLVED | Live body states 212 ports; census confirms 212 at both pins. Manager comment 5991634080 supersedes historical count prose. |
| R486-1 R1, RESIDUE, Docs | RESOLVED | Live body gives the published branch fetch and detached checkout. |
| R487-1 F1, MINOR, Conformance/Tests/Docs | RESOLVED | Five statements agree; four arms pass; three widened exemptions are killed. |
| R487-1 F2, MINOR, Docs | RESOLVED | Same privacy correction as R486-1 F1. |
| R486-1 R2/R3 | RETAINED, RESIDUE | Exact wording corrections below. |
| R486-1 S1; R487-1 S1/S2 | RETAINED, SUGGESTION | Optional work below; no present defect established. |

The frozen `0010a410` archive predates its privacy correction. I checked the later public copy named by the manager rather than treating the frozen copy as corrected. Its old count prose is historical; the live body explicitly supersedes it. Receipts: `pr-body.md`, `public-evidence-audit.json`, `structural.json`.

- **R486-1 R2 - RESIDUE - Docs - `docs/reference/SUBMODULES.md:148`.** Authority/evidence: the D3 header says name pending has not transferred; this summary uses an ambiguous present tense. Impact: wording can suggest completed adoption. Exact required wording: "Not yet adopted: a later parent lane (D3 section 18.3, lane 3) moves name pending to `d3_unflushed_o`; until then the sticky term stays." Verification: compare with the D3 header. Retained under the assigned wording-residue rule.
- **R486-1 R3 - RESIDUE - Docs - `docs/reference/PP_DESCRIPTOR_OWNERSHIP.md:333`.** Authority/evidence: the F5 conformance-waiver statement omits the explicit lint waiver in `configs/endstation_ax7101_8x8.yaml`. Impact: ambiguity between lint permission and conformance. Exact required addition: "The 8x8 configuration's `model_lint_waivers` entry (L1 `port-cluster-minimum`, STREAM_PORT_INPUT 0 to 7, #584) lets the default lint pack it; the packer refuses the waiver once any of those ports passes. The waiver is not a conformance claim." Verification: preserve both the existing conformance debt and lint behavior; no clause claim changes.
- **R486-1 S1 - SUGGESTION - Docs/RTL - `docs/findings/234_PP_SHADOW_AREA_BASELINE.md:38`.** Evidence: standalone 8x8 WNS falls from -1.947 to -4.095 ns; the page correctly separates this estimate from routed timing. Impact: possible future misreading. Optional outcome: identify the fall and the owner of an integrated 8x8 route. Verification: retain the standalone limitation without inventing an integrated fit claim.
- **R487-1 S1 - SUGGESTION - Tests - `tb/verilator/nvm_cosim/Makefile:50`.** Evidence: the producer chain excludes the D3 name writer; parent power-cycle name proof remains unclaimed. Impact: integration retains static compatibility evidence only. Optional outcome: test name write, restore and rollback with the real backend in lane 3/#637. Verification: cleared-state readback and fault-sensitive controls, without claiming hardware proof.
- **R487-1 S2 - SUGGESTION - Robustness/Tests - `protocol-processor/hdl/aecp/desc/model_rules.py:115`.** Evidence: lint literals 144 and 8 agree with the consumer, but the retired check derived its limits from that consumer. Impact: future drift could escape current agreement. Optional outcome: tie lint limits to the consumer's rate walk. Verification: a planted mismatch fails. No present mismatch was found.

**Reviewer-owned ledger.** CLEAN means no open BLOCKER, MAJOR or MINOR in this assigned scope; it does not discharge every product requirement or physical release obligation.

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #661 acceptance/decisions; REQUIREMENTS.md; `KL_adp_engine.sv:703`; register map and five corrected statements; wire vectors; retained capture/resource evidence | R486-2, retaining unaffected R486-1 coverage | 3880c1eb6e2f927a07f98150d5b05a228f8f4efd |
| RTL | CLEAN | Full diff/history; `KL_nvm_backend.sv:247`; port census; merge equality; source-list authorities; policy comparison; `delta.log` | R486-2, retaining unaffected R486-1 coverage | 3880c1eb6e2f927a07f98150d5b05a228f8f4efd |
| Robustness | CLEAN | `avtp_wire_truth_checks.py:588`; reset/repeat/wrap/entity vectors; name boundary and nine controls; allocation/resource-map refusals | R486-2, retaining unaffected R486-1 coverage | 3880c1eb6e2f927a07f98150d5b05a228f8f4efd |
| Tests | CLEAN | `avtp_wire_truth_selftest.py:347`; 25 tests and three killed mutations; builder gates 36b/38; source-list 50/50; gPTP pacing assertions and inherited input identity | R486-2, retaining unaffected R486-1 coverage | 3880c1eb6e2f927a07f98150d5b05a228f8f4efd |
| Docs | CLEAN | PR body/corrected copy; saved-state, register-map, compliance and ownership pages; submodule diagram; docs check; public manifest and prior dispositions | R486-2, retaining unaffected R486-1 coverage | 3880c1eb6e2f927a07f98150d5b05a228f8f4efd |

**Executed checks and limits.** All completed ordinary focused commands returned 0. Wire mutants returned the required 1; the intentionally stopped simulation returned 2 and is not a passing result. `scripts/focused_checks.py` records the command set: source lists/controls, capture, baseline policy, allocation controls, resource-map controls, submodule docs, ports, naming, evidence dispositions and builder gates 36b/38. The separate docs check reports zero findings across 189 Markdown and 987 text files, with 23/23 scrub controls and 4/4 routing arms. The boundary diagram checks all four gitlinks and its decoded raster.

Full parent, processor, gPTP-processor, synthesis, builder and hosted/local-replica banks were not run here. Full-bank claims rely on the assigned public evidence and the manager's supplied source-validation result, not these focused checks. The three original resource input digests were not re-derived from raw measurement directories. The external standards text was checked through its adopted clause record and interface authorities, not through a separately supplied standards document.

The exact-head hosted API snapshot marks `rtl-fast`, `wire-accountability` and `docs-check-no-git` successful, with other jobs still in progress. The physical-gPTP job is skipped. Status alone was not treated as proof that every underlying command executed; manager acceptance remains pending. `structural.json` preserves the timestamped job records.

Physical calibration: NOT RUN. Field-generator skips, historical calibration absence, simulation and timing reports are not hardware proof. No hardware, flash, soak, source fix, commit, push, GitHub write, Docker/local-replica execution, privilege operation or other-checkout edit was performed. Disposable builds and mutations remained under packet scratch storage. Independent checks ran concurrently with bounded parallelism; compilation used two workers. The original checkout is clean: all 1,011 parent tracked files and the tracked files of all three required submodules match their blobs, modes and indexes before and after. Required gitlinks are `ead8036035affd53ef4b29979190f2f4f67084c0`, `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d`, and `48ff7a7e2ef782cf778d47910cf85835c64b1bce`.

**Pending manager duties.** Publish this packet, obtain the external verdict and leave no review round in flight. Carry R2/R3 to the residue checklist and retain the optional suggestions. Record the disposition of the already publicly reported, unchanged FR-DISC-01 wording; this review does not amend that requirement. Accept exact-head hosted and local-replica evidence, distinguishing executed checks from skips and retaining the authorized #657 exception. At merge, validate the final candidate against then-current dev; this source review is not that gate. Merge only with explicit maintainer authorization, then check containment, flash, perform the required bench/soak work and complete issue/project closure.

`MANIFEST.sha256` lists every publishable receipt and portable script. Five receipt copies normalize host paths or a capture-product label; `receipts/redaction-summary.json` records raw and public hashes. Exit statuses, assertions and figures are unchanged. Raw originals and disposable trees stay under `scratch/`, excluded from publication.

R486-2 FINISHED

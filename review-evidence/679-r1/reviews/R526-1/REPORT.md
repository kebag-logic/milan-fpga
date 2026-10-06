[R526] NEGATIVE - exact head 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe

R526-1 independently applied Conformance, RTL, Robustness, Tests, and Docs. One MAJOR finding remains open: both runtime-dependency checks can accept an unresolved, unapproved external symbol. No production-firmware failure is claimed by this synthetic probe. There are no additional MINOR, RESIDUE, or SUGGESTION findings.

Reviewed tree: `dfc55c6343d0c4c943e0c127dee9912ea94357fa`. Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`. The diff contains one commit and 15 changed files. Production firmware sources, RTL, shipping-image construction, and submodule pins are unchanged.

Reconstruction followed the operating contract, contribution rules, documentation index, [issue #679](https://github.com/kebag-logic/milan-fpga/issues/679), [assignment](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923), [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702), product/firmware authorities, then the diff and history. The independent diff pass preceded public executable evidence. No private author material or other review report informed this verdict. After the independent verdict and ledger were written, the public review endpoints contained no earlier findings to resolve: no reviews, no inline comments, and only the two review-start comments. See `receipts/prior-public-findings.json`.

[R526] MAJOR Conformance, Robustness, Tests, Docs - `sw/firmware/ctrl/test/ctrl_arms.py:190`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:66` - R526-1-F1: local definitions hide unresolved runtime dependencies

- Authority/evidence: `sw/firmware/gtest/README.md:355` promises restricted undefined dependencies and rejection of unexpected double-underscore services. Both arms subtract every defined symbol name from the undefined set before applying their allowlists. Their definition collection includes local symbols. A private function cannot satisfy another translation unit's external reference.
- Reproducer: `scripts/runtime-binding-probe.py` appends a call to `__review_runtime_service` in a disposable firmware copy. Each real arm rejects that ordinary unresolved-symbol control. Adding a same-named, emitted static function in another source makes both arms report success. The static definition is marked `t`; the caller still has `U`. A relocatable partial link succeeds and still reports `U __review_runtime_service`. This demonstrates symbol-binding semantics without requiring the deferred linked firmware image.
- Actual result: ctrl reports `rc=0`, `RESULT: PASS`, and omits the dependency from its printed open-symbol list; the store returns an empty findings list. See `receipts/runtime-binding.log`, `receipts/runtime-binding-result.json`, and `receipts/runtime-binding-nm.log`.
- Impact: an object set can pass the advertised runtime boundary while retaining an unapproved external dependency. The new ordinary heap/unknown-service controls at `sw/firmware/gtest/fw_rv32_selftest.py:94` and `:111` do not cover this case. Conformance and Docs remain unclean because the stated dependency guarantee is false; Robustness and Tests remain unclean because the checks accept this adverse input.
- Required outcome: only definitions capable of satisfying an external reference may remove it from the unresolved set. Both real firmware arms must reject the same-name local-definition case. Preserve the valid object builds and existing allowed runtime interfaces; add controls for both arms.
- Verification: repeat this portable probe on the corrected head. Both masked cases must be rejected for the runtime dependency, while the unchanged firmware, existing 15 controls, both campaigns, and coverage ratchet remain green. Confirm the rejection is not merely a compile/setup failure.

The name-only resolution heuristic predates this PR. This finding concerns its retention in the runtime checks this PR strengthens and documents; it does not attribute the original defect to this commit. No source fix was made during review.

The intended SDK repair works on the unchanged firmware. A fresh scratch installation verified archive SHA-256 `d42680e926542595c4c87629d33f5f90aac1e9a964c8955089e0514caa01b78f`, release `riscv32-ilp32d--glibc--stable-2025.08-1`, and compiler version 14.3.0. The original ctrl header lookup reproduced the missing `gnu/stubs-ilp32.h` failure. The isolated headers produce RV32I/ILP32 objects with zero ABI flags and the required architecture attribute. The declarations provide no replacement runtime implementation.

Independent probes additionally confirmed rejection of RV32M in each real arm, a source-induced dynamic frame in each real arm, an explicitly absent required store compiler, wrong ELF endianness/machine/type/embedded ABI, and a missing frame file. The 15 committed controls also passed, including hostile hosted headers, RV64, hard-float, compressed ISA, heap calls, unknown services, and stack-protector dependencies. These successes do not resolve R526-1-F1.

Size and frame measurements agree with the PR. Ctrl totals are text/data/BSS `11520/0/170`, with a largest static frame of 112 bytes. All nine ctrl objects were byte-identical when comparing the old flags plus the necessary isolated headers against the new flags; passive frame reporting did not alter the object bytes. The literal old ctrl recipe cannot provide a successful pinned-SDK baseline because its headers fail, as reproduced above.

| Store shape | Before text | After text | Data, unchanged | BSS, unchanged | Largest static frame, unchanged |
|---|---:|---:|---:|---:|---:|
| endstation_arty_current | 12352 | 12112 | 24 | 3160 | 128 |
| endstation_ax7101_1x1_tdm8 | 12368 | 12128 | 24 | 4048 | 128 |
| endstation_arty_4x4 | 12360 | 12120 | 24 | 5452 | 128 |
| endstation_arty_8ch | 12360 | 12120 | 24 | 8012 | 128 |
| endstation_ax7101_8x8 | 12372 | 12132 | 24 | 14408 | 128 |

The store comparison used the base build routine and flags, adding passive stack reporting, against the current routine. Every static buffer/counter size also stayed unchanged. The 240-byte reduction per shape is acceptable for this scope: disabling SDK-injected stack protection changes validation objects, introduces no shipping-image change, and removes an unsupported runtime dependency. The PR description explicitly states the cause, and `sw/firmware/ctrl_nvm/README.md:337` states the instrumentation choice and updated figures. This acceptance is not approval to remove a required protection from a future integrated image.

The PR description and `sw/firmware/gtest/README.md:362` correctly limit these results to objects and individual frames. Per the public ruling, final linked-image size and whole-program stack bounds belong to integration. No nested-call, interrupt-stack, runtime-library compatibility, bootability, or board claim follows from the reported frame maxima.

| Executed check | Result | Receipt |
|---|---|---|
| ctrl suite, RV32 required, full campaign | PASS; all 76 mutants caught | `receipts/ctrl-campaign.log` |
| store suite, RV32 required, full campaign | PASS; five shapes, 434 tests, all 106 mutants caught | `receipts/nvm-reuse.log` |
| committed RV32 build controls | PASS; 15 checks | `receipts/rv32-controls.log` |
| independent sizes and boundary probes | PASS | `receipts/independent-rv32.log`, `receipts/object-size-comparison.json` |
| runtime binding probe | Two false acceptances confirmed | `receipts/runtime-binding.log` |
| coverage ratchet and its controls | PASS; 14 files, 100% adjusted lines/branches, unchanged exclusions | `receipts/coverage.log`, `receipts/coverage-selftest.log` |
| CI contract check and self-test | PASS; 1741 contract items, 2361 arms | `receipts/ci-events-check.log`, `receipts/ci-events-selftest.log` |
| scope classifier self-test | PASS | `receipts/ci-scope-selftest.log` |
| documentation, style, em-dash, contents | PASS after locked renderer setup | `receipts/docs-check.log`, `receipts/doc-style.log`, `receipts/em-dash-locked.log`, `receipts/toc-check.log` |

The original store campaign was deliberately stopped after 24 successful mutant rows because distinct physical build paths forced repeated compilation. Its interrupted receipt is retained and is not counted as a pass. The replacement calls the unchanged full driver and grading functions with one physical directory per worker. It preserves all mutant identities, source seams, generated inputs, flags, cache keys, expected failing tests, and completeness checks. Its 106 successful rows and zero exit status are the completed evidence. Campaigns and coverage ran concurrently, with explicit worker allocations below the 16-job cap. The initial em-dash setup refusal is likewise retained separately from its successful rerun with locked dependencies.

The exact-head hosted `firmware-unit` job [112422842862](https://github.com/kebag-logic/milan-fpga/actions/runs/37508325617/job/112422842862) executed successfully. Its log shows both `--require-rv32` commands, the 15 controls, ctrl RV32 output, all five store RV32 outputs, and the coverage verdict. Checkout used merge commit `57475e2e8dc5f4730e837b88cb8bdab2768189f6`; the public commit API confirms its parents are the source base and reviewed head, and its tree exactly equals the reviewed tree. See `receipts/hosted-firmware-excerpt.log` and `receipts/hosted-merge-tree.json`. The observed physical gPTP context was skipped, and several broader jobs were still running in the captured snapshot. Those are not completed hardware or full-bar evidence. Hosted and local workflow-replica acceptance remain manager-owned.

[R526] PASS RTL - `receipts/source.diff`, `REQUIREMENTS.md:4`, `docs/litex/LITEX_SOC.md:79`, `receipts/object-size-comparison.json` - verified the RV32I architecture boundary and unchanged production/RTL inputs; no clock, reset, CDC, wire-format, FSM, or production interface change appears in this diff.

Reviewer-owned coverage ledger:

| lens | CLEAN/UNCLEAN | examined artifacts | covering round | exact head |
|---|---|---|---|---|
| Conformance | UNCLEAN | #679 body/assignment/ruling; ctrl_arms.py:190; nvm_rv32.py:66; hosted firmware log; R526-1-F1 | none; R526-1 applied | 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe |
| RTL | CLEAN | source.diff; REQUIREMENTS.md:4; LITEX_SOC.md:79; object-size comparison; production-source and gitlink equality | R526-1 | 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe |
| Robustness | UNCLEAN | fw_rv32.py:45 and :62; independent boundary probes; runtime-binding probe; R526-1-F1 | none; R526-1 applied | 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe |
| Tests | UNCLEAN | fw_rv32_selftest.py:94 and :111; 76/106 campaigns; coverage and CI controls; R526-1-F1 | none; R526-1 applied | 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe |
| Docs | UNCLEAN | gtest/README.md:355; ctrl_nvm/README.md:337; CI_WORKFLOWS.md:42; PR description; R526-1-F1 | none; R526-1 applied | 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe |

Full parent, processor, gPTP, synthesis, and builder banks were not rerun under this assignment. The manager reports completed source banks; the retrieved public evidence snapshot still includes the author's earlier partial builder receipts, which this review does not promote to a completed bank. The manager must attach or identify the superseding source receipts, accept hosted/local-replica evidence, obtain the corrected-head re-review and independent external verdict, validate the final current-dev merge candidate, and perform post-merge containment and issue closure. Source validation and the final merge candidate remain distinct obligations even while dev equals the source base. Physical calibration was NOT RUN. Field skips, simulation, and object checks are not hardware proof. The optional private-dependency arm was not rerun; existing coverage exclusions remain unchanged.

Final integrity verification proved all 1144 parent tracked blobs, executable/symlink modes, and stage-zero index entries against HEAD. It also proved the three required registered submodules and all their tracked bytes/indexes: protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 files), gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104 files), and third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214 files). The optional uninitialized external gitlink is unchanged. The checkout is clean, and no probe altered its tracked source. See `receipts/tree-integrity-final.log`.

`MANIFEST.sha256` lists the publishable report, scripts, and receipts. Scratch trees, SDKs, environments, and unlisted metadata are excluded. Local output receipts preserve command results; only local paths and terminal color were normalized for publication, with original/published hashes in `receipts/scrub-receipt.json`. No source commits, pushes, GitHub writes, or merge actions were performed.

R526-1 FINISHED

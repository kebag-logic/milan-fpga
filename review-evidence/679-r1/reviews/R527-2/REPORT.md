[R527] POSITIVE - exact head 04e1435a218908d2b12b4053e5dab2c2dcac2ebf

R527-2, external independent review of issue #679 / PR #683.
Tree: `30980a43ee2b14afd59e25b16aafb18ea6e1df41`.
Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`.
Round-2 parent: `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe`.
This verdict covers the scoped source change, not merge authorization.

All five lenses are CLEAN. No new BLOCKER, MAJOR, MINOR, RESIDUE or SUGGESTION is raised. R526-1-F1 is resolved at this head. The earlier external verdict's unaffected conclusions stand; the changed dependency checks, controls and documentation were independently reassessed here.

The review followed the requested authority order: repository operating contract and contribution rules, documentation index, [frozen acceptance](https://github.com/kebag-logic/milan-fpga/issues/679), [assignment](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923), [scope ruling](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702), requirements and interface authorities, full base-to-head diff and history, then public executable evidence. The ruling explicitly accepts object sizes and individual static frames here; linked-image and complete stack bounds remain integration obligations. No private author material informed this review. The independent verdict and ledger were written before reading prior review reports. Public conversation, submitted-review and inline-comment endpoints were then reconciled; the latter two contained no findings.

R526-1-F1: MAJOR, RESOLVED. Attributable lenses: Conformance, Robustness, Tests, Docs. Artifacts: `sw/firmware/ctrl/test/ctrl_arms.py:161`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:65`, `sw/firmware/gtest/fw_rv32_selftest.py:100`, `sw/firmware/gtest/fw_rv32_selftest.py:127`, `sw/firmware/gtest/README.md:358`.

- Authority/evidence: the [prior finding](https://github.com/kebag-logic/milan-fpga/pull/683#issuecomment-6022774174) and [round-2 assignment](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022780134) require external references to be resolved only by global or weak definitions. Both definition queries now combine `--extern-only` with `--defined-only`.
- Previous impact: an emitted local definition could hide an unapproved external dependency from the check while leaving that dependency unresolved in the object set.
- Required outcome: both real arms reject that case for the runtime dependency, preserve valid builds and allowed interfaces, add effective controls, and describe the cross-object name check accurately. All are satisfied.
- Verification: the [original public probe](https://github.com/kebag-logic/milan-fpga/blob/b56eb2bea85d626e6ca398f6fd5496a99db66c7a/review-evidence/679-r1/reviews/R526-1/scripts/runtime-binding-probe.py) was rerun without changing its bytes. Both masked arms return 1 with `symbols outside the C library and libgcc: __review_runtime_service`. Every object compiles, both partial links return zero, and symbol inspection shows local `t` plus external `U`; the partial links retain the unresolved service. These are dependency rejections, not compile/setup failures. See [runtime-binding.log](receipts/runtime-binding.log), [results](receipts/runtime-binding-result.json), [symbol evidence](receipts/runtime-binding-nm.log), and [provenance](receipts/prior-probe-provenance.json).

[R527] PASS Conformance - `REQUIREMENTS.md:4`, `docs/ARCHITECTURE_HW_SW_SPLIT.md:62`, `.github/workflows/rtl-fast.yml:273`, `sw/firmware/ctrl/test/ctrl_arms.py:191`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:65` - both unchanged firmware populations build using the pinned SDK as RV32I/ILP32 freestanding objects. Required compiler selection and SDK-before-suite ordering remain enforced. Runtime allowlists are unchanged, and the binding restriction meets the round-2 decision. The exact-head hosted job executes both RV32 arms successfully.

[R527] PASS RTL - `receipts/source-scope.log`, `sw/firmware/ctrl/test/ctrl_arms.py:183`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:50`, `sw/firmware/gtest/fw_rv32.py:45`, `docs/design/MAILBOX_SPLIT.md:209` - the delta changes validation symbol collection and controls, not firmware behavior, production headers, RTL, clock/reset/CDC wiring, mailbox ownership, shipping-image construction, configurations or submodule pins. RV32I, ILP32 and the soft-float object contract remain intact. No new FSM, backpressure, reset or hardware timing behavior is introduced. Object-size and frame measurements remain consistent with the prior round and documented limits.

[R527] PASS Robustness - `sw/firmware/ctrl/test/ctrl_arms.py:161`, `sw/firmware/ctrl_nvm/test/nvm_rv32.py:65`, `sw/firmware/gtest/fw_rv32_selftest.py:83`, `scripts/binding_probe.py` - fourteen independent compiled cases cover both arms with an ordinary unresolved reference, local `t/d/b/r` definitions, global `T`, and weak `W`. Every local case remains unresolved and is rejected specifically by the runtime diagnostic. Global and weak positives pass and resolve in a partial link. All seventeen committed controls pass, retaining hostile-header, absent-compiler, ISA/ABI, malformed-object, dynamic-frame, heap, unknown-service and stack-protection controls. Full functional campaigns retain their existing adverse-input and failure-path coverage.

[R527] PASS Tests - `sw/firmware/gtest/fw_rv32_selftest.py:107`, `sw/firmware/gtest/fw_rv32_selftest.py:132`, `scripts/control_sensitivity.py`, `sw/firmware/ctrl/test/ctrl_mutants.py:381`, `sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:169`, `scripts/ci_events.py:7763` - removing either external-only filter independently makes its corresponding new static-definition assertion fail. Both complete required-RV32 campaigns pass; every mutant is caught by its named failure oracle. Coverage and its exclusions/ratchet are unchanged. CI controls still reject removal of either required-RV32 flag.

[R527] PASS Docs - `sw/firmware/gtest/README.md:345`, `sw/firmware/ctrl/README.md:110`, `sw/firmware/ctrl_nvm/README.md:334`, `docs/testing/CI_WORKFLOWS.md:42`, PR #683 body and scope ruling 6022358702 - the guarantee states cross-object name matching with global/weak definitions and expressly excludes local definitions. Documentation distinguishes runtime declarations from implementations, object checks from linked images, and individual static frames from complete stack bounds. Reported figures match this run. Documentation/privacy, style, added-line punctuation and generated contents checks pass.

| Executed validation | Result | Receipt |
|---|---|---|
| Fresh pinned SDK extraction, relocation and inventory verification | PASS; pinned archive digest and compiler 14.3.0 | [SDK installation](receipts/sdk-install.log) |
| Required RV32 build controls | 17/17 PASS | [Controls](receipts/rv32-controls.log) |
| Independent binding cases and filter-removal sensitivity | 14 compiled cases PASS; both new controls detect removal | [Binding](receipts/binding-probe.log), [sensitivity](receipts/control-sensitivity.log) |
| Original R526-1 binding probe | Both masked cases correctly rejected | [Probe](receipts/runtime-binding.log) |
| Ctrl suites and full campaign with `--require-rv32 --self-test` | PASS; 76/76 mutants caught | [Ctrl campaign](receipts/ctrl-campaign.log) |
| Store suites and full campaign with `--require-rv32 --self-test --jobs 4` | PASS; five shapes, 434 tests, 106/106 mutants caught | [Store campaign](receipts/nvm-campaign.log) |
| Coverage ratchet | PASS; 14 files, 100% adjusted lines and branches | [Coverage](receipts/coverage.log) |
| SDK, tally and coverage controls | PASS; 25 SDK cases, 18 tally cases, 18/18 listener mutants, 28/28 coverage cases | [SDK](receipts/sdk-controls.log), [tally](receipts/tally-controls.log), [coverage controls](receipts/coverage-controls.log) |
| CI contract and scope controls | PASS; 1741 contract items, 2361 mutation arms | [CI contract](receipts/ci-events-controls.log), [scope](receipts/ci-scope-controls.log) |
| Documentation and diff checks | PASS | `receipts/docs-check.log`, `doc-style.log`, `em-dash.log`, `toc.log`, `diff-check.log` |

The full store run uses the public evidence's bounded per-worker directory technique, reproduced in [nvm_campaign.py](scripts/nvm_campaign.py). It calls the original full driver and grading function. Only physical directories are reused; mutant identities, source seams, generated inputs, flags, preprocessed cache keys, completeness checks and killing assertions remain unchanged. No setup failure is credited as a caught mutant. Ctrl completed in 575.361 seconds, store in 416.130 seconds, and coverage in approximately 171.3 seconds. The supervisors awaited all children in the foreground. Worker allocations remained below sixteen; observed memory peak was 3,534,712,832 bytes against the 12,884,901,888-byte cap. Disposable SDKs, builds and probe copies stayed under `scratch/`.

Current object and frame measurements, in bytes:

| Subject | Text | Data | BSS | Largest static frame |
|---|---:|---:|---:|---:|
| ctrl | 11520 | 0 | 170 | 112 |
| store arty_current | 12112 | 24 | 3160 | 128 |
| store ax7101_1x1_tdm8 | 12128 | 24 | 4048 | 128 |
| store arty_4x4 | 12120 | 24 | 5452 | 128 |
| store arty_8ch | 12120 | 24 | 8012 | 128 |
| store ax7101_8x8 | 12132 | 24 | 14408 | 128 |

These agree with the public prior-round measurements. Round 2 changes neither compilation flags nor production sources; it adds no new size change. The earlier accepted 240-byte store-text reduction from disabling SDK stack protection in validation objects remains as described in the PR. This is not shipping-runtime or whole-stack evidence. The prior literal ctrl recipe's pinned-SDK header failure remains the original issue; no successful same-SDK baseline is implied. Five historical executable receipts were checked against their published manifest, as recorded in [public-evidence-verification.log](receipts/public-evidence-verification.log). They are historical evidence, not corrected-head verdicts.

The [hosted firmware-unit job 112439675542](https://github.com/kebag-logic/milan-fpga/actions/runs/37513227140/job/112439675542) completed successfully at the assigned head. Its executed log contains SDK verification, all seventeen controls, both required-RV32 suites, all five store builds and the coverage verdict, with no RV32 skip. Checkout used merge commit `8e846e586de567c15f890f2ab8b1cff39c142e02`; the public commit record proves ordered parents of source base and reviewed head, with a tree exactly equal to the reviewed tree. See [job metadata](receipts/hosted-firmware-unit.json), [executed steps](receipts/hosted-firmware-unit.log), and [tree proof](receipts/hosted-merge-tree.json). The broader [hosted snapshot](receipts/hosted-context-snapshot.json) still contains running jobs; the physical gPTP job is skipped. Neither state is a completed validation result.

The reviewer-owned completion ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #679 acceptance/rulings; REQUIREMENTS.md:4; .github/workflows/rtl-fast.yml:273; sw/firmware/ctrl/test/ctrl_arms.py:191; sw/firmware/ctrl_nvm/test/nvm_rv32.py:65; hosted-firmware-unit.log | R527-2 | `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| RTL | CLEAN | docs/ARCHITECTURE_HW_SW_SPLIT.md:62; docs/design/MAILBOX_SPLIT.md:209; sw/firmware/gtest/fw_rv32.py:45; source-scope.log; integrity-after.log; both campaign size outputs | R527-2 | `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| Robustness | CLEAN | sw/firmware/ctrl/test/ctrl_arms.py:161; sw/firmware/ctrl_nvm/test/nvm_rv32.py:65; sw/firmware/gtest/fw_rv32_selftest.py:83; binding-probe.log; runtime-binding.log; rv32-controls.log | R527-2 | `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| Tests | CLEAN | sw/firmware/gtest/fw_rv32_selftest.py:107,132; control-sensitivity.log; ctrl-campaign.log; nvm-campaign.log; coverage.log; ci-events-controls.log | R527-2 | `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |
| Docs | CLEAN | sw/firmware/gtest/README.md:345; sw/firmware/ctrl/README.md:110; sw/firmware/ctrl_nvm/README.md:334; docs/testing/CI_WORKFLOWS.md:42; PR #683 body; public scope and executable receipts | R527-2 | `04e1435a218908d2b12b4053e5dab2c2dcac2ebf` |

Receipt basenames in the ledger are under `receipts/`. Each result applies to the exact source head named and must be reconsidered if its scoped artifacts change.

Limits and pending manager duties:

- The manager reports passing full source static/builder and native banks. Those banks were not rerun under this assignment. The retrieved historical public packet contains partial earlier builder receipts; it is not promoted to a completed source or candidate bank. The manager must attach or identify the superseding receipts.
- The manager owns supported local workflow-replica acceptance and final hosted-context acceptance. This review confirms executed firmware-unit evidence only, not completion of every required aggregate.
- The manager must validate the final current-dev candidate at the merge turn, reconcile both independent corrected-head reviews, wait for all rounds to finish, obtain required merge authorization, and complete post-merge containment and issue closure. Source validation and final candidate validation remain distinct even when dev equals the source base.
- Linked runtime implementations, RV32 execution, bootability, whole-program/interrupt stack bounds and physical service timing remain unproved here. Physical calibration is NOT RUN. Skipped field jobs, simulation and object checks are not hardware proof. Optional private-dependency validation was not rerun; coverage remains adjusted by existing exclusions, including the recorded #678 premise.

Final integrity checks proved all 1144 superproject tracked blobs, executable/symlink modes and exact stage-zero index entries against the assigned head. They also proved the required submodules and their complete tracked populations: protocol-processor `ead8036035affd53ef4b29979190f2f4f67084c0` (558 files), gptp-processor `5dce647ab5a01a6ecff9a982b22e3a4a1d946d3d` (104 files), and third_party/verilog-axis `48ff7a7e2ef782cf778d47910cf85835c64b1bce` (214 files). Before/after receipts are byte-identical and checkout status is empty. The optional external gitlink remains unchanged and uninitialized. No probe altered tracked checkout bytes.

[REPRODUCE.md](REPRODUCE.md) and the portable scripts define the focused checks. [MANIFEST.sha256](MANIFEST.sha256) lists publishable report, scripts and receipts; scratch trees are excluded. Receipt normalization changes local path prefixes and terminal color only. No source fixes, commits, pushes, GitHub writes, author contact, sub-agents, shared installation, hardware access, local CI container execution or merge occurred.

R527-2 FINISHED

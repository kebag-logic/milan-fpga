[R527] POSITIVE - exact head 0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe

R527-1, external independent review of issue #679 / PR #683.
Tree: `dfc55c6343d0c4c943e0c127dee9912ea94357fa`.
Source base: `6714181d0c8a16e2983f85b724f4d688f5111835`.
This verdict covers the scoped source change. It is not merge authorization.

The scope was reconstructed from AGENTS.md, CONTRIBUTING.md, docs/README.md,
the [issue acceptance](https://github.com/kebag-logic/milan-fpga/issues/679),
[assignment 6021510923](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6021510923),
[ruling 6022358702](https://github.com/kebag-logic/milan-fpga/issues/679#issuecomment-6022358702),
linked requirements and interfaces, then the complete one-commit diff and public
[executable evidence](https://github.com/kebag-logic/milan-fpga/tree/4c5eb3ab1e9ceeb076a9e274fd1a4c8cf52f72d0/review-evidence/679-r1).
No other reviewer's report informed this independent verdict or ledger.

Findings: none. No BLOCKER, MAJOR, MINOR, RESIDUE, or SUGGESTION is raised.

[R527] PASS Conformance - `.github/workflows/rtl-fast.yml:265`,
`sw/firmware/gtest/fw_rv32.py:36`, issue #679 acceptance and ruling 6022358702 -
both actual RV32 arms compile with the unchanged pinned ILP32D SDK while
emitting RV32I/ILP32 objects. The original ctrl command reproduces the missing
`gnu/stubs-ilp32.h`; the candidate excludes hosted includes and succeeds.
The SDK is installed before either suite; both receive `--require-rv32`.
The hosted log confirms execution of both arms, with no RV32 skip.
The ruling expressly accepts object sizes and static frames for this PR.
No linked-image or whole-stack proof is claimed here.

[R527] PASS RTL - `docs/ARCHITECTURE_HW_SW_SPLIT.md:62`,
`sw/firmware/gtest/fw_rv32.py:45`, `sw/firmware/ctrl/test/ctrl_arms.py:175`,
`sw/firmware/ctrl_nvm/test/nvm_rv32.py:50`, `source-scope.json` - the checks
preserve the cacheless RV32I architecture, ILP32 types, little-endian ELF32
relocatable format and soft-float ABI. Extended ISA and hard-float objects
fail through both real arms. The new C11 headers only declare the existing
memory and bounded-formatting interfaces. Undefined runtime dependencies
are restricted to named interfaces and integer arithmetic helpers.
No RTL, clock/reset/CDC wiring, firmware behavior C/header, mailbox contract,
shipping configuration, SoC code, SDK pin, or shipping-image input changed.
Thus this diff introduces no FSM, CDC, reset, wire-format, or hardware timing change.

[R527] PASS Robustness - `sw/firmware/gtest/fw_rv32.py:29,45,62`,
`sw/firmware/gtest/fw_rv32_selftest.py:26,88`, `probe_rv32.py` - the fifteen
controls exercise hostile hosted headers, freestanding selection, RV64,
hard-float, compressed/multiply ISA, malformed ELF, dynamic frames, explicit
missing compiler, heap/unknown dependencies, and restored stack protection.
Independent probes additionally drive wrong ISA/ABI and real VLA-generated
dynamic frames through both production validation arms, require the store's
missing compiler to refuse, and verify a missing frame file cannot pass.
The unchanged functional campaigns retain malformed input, bounds, reset,
ordering, backpressure, timeout, persistence and configuration controls;
all 76 ctrl and 106 store mutants are caught at this head.

[R527] PASS Tests - `sw/firmware/gtest/fw_rv32_selftest.py:26`,
`scripts/ci_events.py:7763`, `sw/firmware/ctrl/test/ctrl_mutants.py:381`,
`sw/firmware/ctrl_nvm/test/test_ctrl_nvm.py:169,195`, `coverage.log` - both
positive suites run with RV32 required. The complete ctrl campaign catches
76/76 at the final head, closing the published evidence's earlier-checker
qualification. The store runs five shapes, 434 tests and 106/106 mutants.
The public directory-reuse wrapper calls the original full driver: only the
physical per-worker mutant directory changes; inventory, flags, firmware
recompilation, preprocessed cache keys and named killing assertions remain.
No tests, mutation oracles, coverage ratchet or exclusions changed.
All fourteen files retain 100 percent adjusted line and branch coverage;
raw counts match the published before/after evidence. This is adjusted
coverage with existing exclusions, including the recorded #678 premise.
The CI contract passes 1,741 items and 2,361 mutation arms, including removal
of either required-RV32 flag. Tally controls catch 18/18 listener mutants;
coverage controls pass 28/28 cases.

[R527] PASS Docs - `docs/testing/CI_WORKFLOWS.md:42`,
`sw/firmware/ctrl/README.md:110`, `sw/firmware/ctrl_nvm/README.md:335`,
`sw/firmware/gtest/README.md:345`, PR #683 body - the updated documents
correctly describe required RV32 compilation, isolated headers, runtime
allowlists, object sizes, static frames, and the absence of linked-image
or whole-program stack proof. The PR explicitly attributes the store's
240-byte text reduction to disabling SDK stack protection in validation
objects. The public ruling assigns linked size and stack bounds to integration.
Documentation/privacy, style, added-line punctuation and generated contents
checks pass. The renderer-dependent checks initially refused absent local
dependencies; passing reruns used the locked renderer installed only in scratch.
The initial refusal receipts remain recorded and are not counted as passes.

The measured size change is acceptable within this scope. It removes
SDK-injected `__stack_chk_fail` dependencies from validation objects,
preserves firmware behavior sources and shipping inputs, and is explicit
in the PR. It supplies no evidence about a future linked runtime's protection
or stack consumption. The original store build module and candidate were
both compiled with the pinned SDK for each shape; only observational
`-fstack-usage` was added to the baseline measurement.

| Subject | Text before | Text after | Data | BSS | Largest static frame |
|---|---:|---:|---:|---:|---:|
| ctrl | 11520 | 11520 | 0 | 170 | 112 |
| store arty_current | 12352 | 12112 | 24 | 3160 | 128 |
| store ax7101_1x1_tdm8 | 12368 | 12128 | 24 | 4048 | 128 |
| store arty_4x4 | 12360 | 12120 | 24 | 5452 | 128 |
| store arty_8ch | 12360 | 12120 | 24 | 8012 | 128 |
| store ax7101_8x8 | 12372 | 12132 | 24 | 14408 | 128 |

Units are bytes. Store data, BSS, static buffers and frames are identical
before/after in `independent-sizes.json`. Ctrl's candidate totals and frame
were reproduced; its before figure comes from the public matching-ABI SDK
receipt, because the baseline ctrl build fails on the pinned SDK.
It is not a same-SDK successful ctrl baseline comparison.

| Focused validation | Result | Receipt |
|---|---|---|
| Pinned SDK fresh installation and inventory verification | PASS | `sdk-install.log`, `.rc` |
| RV32 build controls, required compiler | 15 checks PASS | `rv32-controls.log`, `.rc` |
| Independent real-arm fault and size probes | PASS | `independent-rv32.log`, `.rc`, `independent-sizes.json` |
| Ctrl suites and full campaign, RV32 required | PASS; 76/76 caught | `ctrl-suite-mutants.log`, `.rc` |
| Store suites and full campaign, RV32 required | PASS; five shapes, 434 tests, 106/106 caught | `nvm-suite-mutants.log`, `.rc` |
| Coverage ratchet | PASS; 14 files | `coverage.log`, `.rc` |
| CI events check/self-test, CI scope self-test | PASS | `ci-events-*.log`, `ci-scope-selftest.log`, corresponding `.rc` |
| SDK, tally and coverage self-tests | PASS | `sdk-selftest.log`, `tally-selftest.log`, `coverage-selftest.log`, corresponding `.rc` |
| Documentation checks | PASS after isolated renderer setup | `docs-check.log`, `docs-style.log`, `em-dash-complete.log`, `toc-complete.log`, corresponding `.rc` |

`REPRODUCE.md`, the portable scripts and command JSON receipts define the
invocations. Independent commands ran concurrently under a foreground
supervisor. Ctrl completed in 559.880 seconds, store in 396.235 seconds,
and coverage in 135.719 seconds. No command timed out. Compiler concurrency
stayed within sixteen jobs; the unit peak was 3,932,549,120 bytes against
the 12,884,901,888-byte cap. Disposable sources, SDK and builds stayed in scratch.

The [hosted firmware-unit job](https://github.com/kebag-logic/milan-fpga/actions/runs/37508325617/job/112422842862)
completed successfully: SDK installation, all fifteen controls, both required
RV32 suites and coverage executed. `hosted-firmware-unit-excerpt.log` retains
the relevant log lines; `hosted-snapshot.json` retains step conclusions.
Its checkout was merge commit `57475e2e8dc5f4730e837b88cb8bdab2768189f6`,
with ordered parents base and reviewed head and tree exactly equal to this
reviewed tree (`hosted-checkout.json`). Cache-build steps marked skipped
are not executed builds. The physical gPTP job was skipped; it provides
no hardware evidence. Other required hosted aggregates were still running
in the recorded snapshot; this report does not claim their final success.

The reviewer-owned completion ledger is:

| Lens | CLEAN/UNCLEAN | Examined artifacts | Covering round | Exact head |
|---|---|---|---|---|
| Conformance | CLEAN | Issue #679 acceptance and ruling 6022358702; REQUIREMENTS.md:4,306; .github/workflows/rtl-fast.yml:265; fw_rv32.py:36; hosted-firmware-unit-excerpt.log | R527-1 | `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe` |
| RTL | CLEAN | docs/ARCHITECTURE_HW_SW_SPLIT.md:62,96; fw_rv32.py:45; ctrl_arms.py:175; nvm_rv32.py:50; source-scope.json; independent-sizes.json | R527-1 | `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe` |
| Robustness | CLEAN | fw_rv32.py:29,45,62; fw_rv32_selftest.py:26,88; probe_rv32.py; independent-rv32.log; both campaign logs | R527-1 | `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe` |
| Tests | CLEAN | fw_rv32_selftest.py:26; scripts/ci_events.py:7763; ctrl_mutants.py:381; test_ctrl_nvm.py:169,195; all focused receipts and coverage.ratchet | R527-1 | `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe` |
| Docs | CLEAN | docs/testing/CI_WORKFLOWS.md:42; sw/firmware/ctrl/README.md:110; sw/firmware/ctrl_nvm/README.md:335; sw/firmware/gtest/README.md:345; PR #683 body; public evidence manifest | R527-1 | `0a004a8cc2ad879e74d8e4168bd4a39a12d5dbbe` |


All ledger paths abbreviated above refer to the exact reviewed source tree;
packet receipt names refer to this directory. The complete relevant source
paths are spelled out in the per-lens results. Coverage is banked only
against this head and must be reassessed if an in-scope artifact changes.

Limits and pending manager duties:

- This review does not run the full parent, processor, gPTP, synthesis or
  builder banks. The assignment reports passing manager source banks;
  their source validation is distinct from final current-dev candidate validation.
- The manager owns hosted and supported local CI acceptance, publication
  of its complete evidence, and final required-context reconciliation.
  The available manager comments record the assignment and ruling, not
  a completed final candidate or local CI verdict.
- The manager must validate the final candidate against live dev at merge
  time, obtain the independent internal review and wait for every round
  to finish, then follow authorization, containment and issue closure rules.
- Update the PR's author-time pending-status text when final gate receipts
  are attached; keep the linked-image/whole-stack integration obligation explicit.
- These are compile and host-execution results. RV32 instruction execution,
  linked runtime resolution, nested/interrupt stack bounds, physical timing,
  calibration and field behavior are not proved. Physical calibration is
  NOT RUN. Skipped field jobs and desk tests are not hardware proof.
- Optional private-dependency validation is not run in this review.
- No source fixes, commits, pushes, GitHub writes, author contact, hardware
  access, shared installation or local CI container execution occurred.

`tree-before.json` and `tree-after.json` prove every root tracked blob and
mode, exact index records and the three required initialized submodule
pins/bytes/modes. Root has 1,144 tracked blobs; required submodules have
558, 104 and 214. The snapshots match; the detached checkout is clean.
The optional external gitlink is unchanged and uninitialized.

Prior public findings were checked after the independent verdict and ledger
were written. Paginated PR conversation, submitted-review and inline-comment
endpoints returned two review-start comments, zero submitted reviews and
zero inline comments. There are no prior findings to resolve or retain.
`prior-findings-reconciliation.json` records the snapshot;
`independent-verdict-written.json` binds the earlier independent report.

R527-1 FINISHED

[R214] POSITIVE - exact head 02c47cf0dbe7062ff762068875bf70b721dd6b37

Independent external round-four review. Applied lenses: RTL, Docs, Tests. No BLOCKER, MAJOR or MINOR remains under those assigned lenses. The reported later-write defect is refused at this head. This verdict does not approve a merge, closure of #408/#409, or another reviewer's coverage.

[R214] PASS RTL - tb/verilator/pp_shadow/Makefile:65, tb/verilator/pp_shadow/sim_main.cpp:1337, protocol-processor/hdl/adp/KL_adp_engine.sv:860 - traced the package-derived expected word and actual transmit bytes against docs/reference/REGISTER_MAP.md:938; pp_shadow passed 371 checks, and an independently wrong expected word failed at wire byte 37. The complete diff changes no HDL, constraints, firmware implementation or submodule pin.

[R214] PASS Docs - docs/integration/BAREMETAL_FIRMWARE.md:208, :1186, :1234; PR #498 public scope decision - the complete-loop claim, retained refusals, separate instrument acceptance table, compiler-dependent counts and explicit skips agree with the implementation and independent measurements. Fourteen focused documentation/static commands passed.

[R214] PASS Tests - sw/builder/test_builder.py:11584, :11694, :23312, :23358, :23676; review-evidence/publication-final.log, builder-rv32.log, builder-absent.log, acceptance-rv32.log, acceptance-absent.log - complete gates 1b and 35 ran in both principal compiler environments; independent controls reproduced the later-write defect on the previous checker and its refusal here, tested complete-loop boundaries, reconstructed every acceptance-table row, challenged both boot-word addresses and all five waits, and checked the capability oracle.

Scope was reconstructed from CONTRIBUTING.md, AGENTS.md, docs/README.md, REQUIREMENTS.md, issues [#465](https://github.com/kebag-logic/milan-fpga/issues/465), [#408](https://github.com/kebag-logic/milan-fpga/issues/408), [#409](https://github.com/kebag-logic/milan-fpga/issues/409), their linked #398/#153/#162 context, the architecture, register map, persistence timing contract and firmware page, the full PR diff/history, both [original R213](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263294055) and [original R214](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263294169) negative reviews, and the [public response](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5755811193). I also read the completed [round-three R213 report](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263484460), [round-three R214 report](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263585652), and [round-four correction response](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5756245830). No private handoff or transcript was consulted.

The [manager's public decision](https://github.com/kebag-logic/milan-fpga/pull/498#issuecomment-5754191153) and current PR body agree: every text refusal remains; compiler instruments are additions; only #465 is proposed for closure. #408/#409 retirement criteria remain open. This is consistent with the delivered code and does not treat a deferred reachable defect as resolved.

The clone was clean before testing. Candidate and live PR head matched the exact SHA above. Live dev matched the expected validation base `07294a76e833f1831d9fcbceb8123b8380c4ae76`; `git merge-base --is-ancestor BASE HEAD` exited 0. These refs were rechecked after testing and remained unchanged. Required initialized submodules were clean at these gitlinks:

| Submodule | Pin |
|---|---|
| protocol-processor | `424c688fa2205b934a7689a58f2aa766420f2326` |
| gptp-processor | `c1b617435824929a790739ea8585c3fe1a328cc0` |
| third_party/verilog-axis | `48ff7a7e2ef782cf778d47910cf85835c64b1bce` |

The external submodule is uninitialized and is not a required validation input. [Repository receipt](review-evidence/repository-state.json).

The original R214 findings were rechecked individually:

| Finding | Current disposition |
|---|---|
| B1, retirement and Docs | Resolved under the public changed contract. No retirement is claimed or implemented; every original text refusal still grades shipping firmware. |
| B1, Tests | Resolved. The accepted firmware count is 17 in both environments. The six proposed retirement edits are refused mutations. Separate instrument calls accept five and refuse the guarded boot printf. Independent constructions reproduced every row. |
| M1, reorder evidence and mismatched names | Resolved. Page and executable table name parse_u64()/seconds_to_ns(). Swapping them fails the ordered store set and passes the resolver alone. |
| m1, false forced-fallback diagnostic | Resolved. The forced arm is absent. The actual compiler-absent run registers its genuine stand-down. |
| m2, false equivalence of environments | Resolved. The page states the extra compiler coverage and the text-only gaps. Independent extra boot writes demonstrate that difference. |
| S1/S4, stale counts and ambiguous retirement row | Resolved. Current counts and the separate instrument table match execution. |
| S2, alternate compiler | Still a fail-closed limitation, reproduced below. It is not resolved by being recorded elsewhere. |

Against live dev, the splice, primitive-spelling, CSR-store closure, ordered cast/store and asm rules have identical executable ASTs after removing docstrings. The directory equality was moved into a renamed helper without changing its executable AST. The conditional rule retains the same six anchors, now shared. Calls remain unconditional before the additional compiler checks. [Comparison receipt](review-evidence/text-rule-comparison.json).

The current publication check requires exactly one `ast.For` with each expected iterator expression and compares its complete AST with the expected loop. This includes the target, every body statement and any `else` arm. The regexes now locate mutation sites only.

Independent variants were constructed from the actual publication loops, without using the gate's mutation constructors:

| Control, applied to both loops | Current result |
|---|---|
| Preserve the first call, append the reported `check_duplicate=False` override | Refused by the complete-loop checker and complete gate 35; the previous head's checker accepts these same variants |
| Add overriding write in a loop `else` arm | Refused |
| Add overriding write inside a nested conditional | Refused |
| Substitute the first value | Refused |
| Duplicate the matching loop | Refused |
| Remove the matching loop | Refused |
| Comments and multiline call formatting | Accepted by the AST comparison |
| Extra argument spacing | Accepted by the AST comparison |
| Pristine source | Accepted by the comparison and complete gate 35 |

This is 12 negative and five positive comparator controls. Both reported later writes were also refused through unmodified gate 35 using temporary source files. The permanent five wait/publication controls and four host-firmware controls passed. [Probe](review-evidence/publication_probe.py), [results](review-evidence/publication-final.log).

The mechanism pins these publication loops; it does not prove arbitrary Python execution or rule out arbitrary writes elsewhere. The formatting statement is also specifically about the AST comparison. A full-gate probe with extra argument spacing was refused by the existing text locator in `_planted_publication`, which is unchanged from the previous head. That result is retained in [the initial probe log](review-evidence/publication.log), not counted as a passing whole-gate formatting test. The final positive formatting controls test the comparator only.

The acceptance table was independently reconstructed with different helper names or insertion sites where practical:

| Edit | Whole contract, with and without RV32 | Instrument alone, with RV32 |
|---|---|---|
| Guarded debug printf inside milan_init | Refused by reach rule | Refused by preprocessed comparison |
| Token paste in UART handler | Refused by paste rule | Accepted |
| Extra cast storing into private static | Refused by cast set | Accepted |
| Extra helper pointer store into private static | Refused by store set | Accepted |
| Swap parse_u64 and seconds_to_ns | Refused by ordered store set | Accepted |
| README and notes.txt beside firmware | Refused by directory pin | Accepted |

Instrument-only probes were explicitly skipped without RV32. [Probe](review-evidence/acceptance_probe.py), [RV32 results](review-evidence/acceptance-results-rv32.json), [absent results](review-evidence/acceptance-results-absent.json).

Issue #465's acceptance items are satisfied within the explicitly declared compiler boundary:

1. Independent CRFT_CTRL and ADP_CAPS writes added to entity_advertise() were refused by the resolved boot-word census. Without RV32, both plants were accepted by the remaining text checks: that whole-firmware measurement is unavailable, not passed. Gate 35's host execution still covers configure_fabric() only.
2. Both original value substitutions and the reported subsequent overrides are refused by the corrected publication pin. The latter were the outstanding round-three defect.
3. Each of the five waits was independently increased by one; every variant failed the exact-value pin. The NVM writer host self-test passed five shapes and detected all four planted defects.
4. The harness takes its expected capability word from the package, no longer reads or provisions 0x614, and detects disagreement at the MAC boundary. Documentation and added-line em-dash checks passed.

RTL review followed the actual interface: REGISTER_MAP.md:938 defines 0x614 as scratch; milan_datapath.sv:2425 leaves that capability output unconnected; KL_adp_engine.sv:860 serializes ADP_ENTITY_CAPS_C into wire bytes 34-37; KL_pp_shadow.sv:1364 packs the bytes; milan_datapath.sv:6662 merges control egress. The changed harness compares those bytes against the package-derived word.

Fresh pp_shadow runs measured:

| Run | Result |
|---|---|
| Candidate sources and normal package-derived expectation 0xC588 | Exit 0; 371 checks, zero failures |
| Keep package 0xC588, force only expected word to 0xC589 | Expected make exit 2; 371 checks, one failure, first differing byte 37 |

The [prior public R214 report](https://github.com/kebag-logic/milan-fpga/pull/498#pullrequestreview-5263585652) additionally measured a changed package with a matching expectation and a disconnected engine with a mismatching wire word. Those experiments are banked evidence, not reruns claimed here. The recipe, harness, package, transmit path, pins, nvm_shape.py and pp_srcs.py are unchanged since `f8b8c0fe17466ed4c64aaeee81ff21e0411fda59`. Gate 1b and the wait checker are also AST-identical to that head. [Artifact comparison](review-evidence/banked-artifacts.json).

Thus RTL coverage from R214 round three at that ancestor can remain banked and is refreshed by this review. Docs and Tests required coverage at `02c47cf0dbe7062ff762068875bf70b721dd6b37`, because their artifacts changed. The PASS lines above cover those assigned lenses at this candidate. No combined five-lens ledger is accepted here.

Commands ran synchronously under CPU affinity 80-95, with `MAKEFLAGS=-j8`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=$REVIEW_TMP/tmp` and `CCACHE_DIR=$REVIEW_TMP/ccache`. `$REVIEW_TMP` denotes the assigned scratch directory; `$REVIEW_ROOT` denotes the clone. All builds and temporary files stayed under scratch. Receipts normalize local paths and typographic separators.

```sh
taskset -c 80-95 python3 -u -B review-evidence/focused_builder.py
HOME="$REVIEW_TMP/absent-home" PATH="$REVIEW_TMP/absent-bin" \
  taskset -c 80-95 python3 -u -B review-evidence/focused_builder.py
HOME="$REVIEW_TMP/elf-home" PATH="$REVIEW_TMP/elf-bin" \
  taskset -c 80-95 python3 -u -B review-evidence/focused_builder.py test_baremetal_profile_contract
taskset -c 80-95 python3 -u -B review-evidence/publication_probe.py
taskset -c 80-95 python3 -u -B review-evidence/acceptance_probe.py
HOME="$REVIEW_TMP/absent-home" PATH="$REVIEW_TMP/absent-bin" \
  taskset -c 80-95 python3 -u -B review-evidence/acceptance_probe.py
HOME="$REVIEW_TMP/elf-home" PATH="$REVIEW_TMP/elf-bin" \
  taskset -c 80-95 python3 -u -B review-evidence/acceptance_probe.py --base --baseline
taskset -c 80-95 python3 -u -B review-evidence/pp_run.py
taskset -c 80-95 python3 -u -B review-evidence/pp_run.py CAPS_RAW=0000C589
taskset -c 80-95 python3 -u -B review-evidence/docs_gates.py
taskset -c 80-95 python3 -B sw/firmware/nvm_hosttest/test_nvm_firmware.py --self-test
```

| Execution | Result |
|---|---|
| Complete gates 1b/35, Buildroot RV32 GCC 14.3.0 | Exit 0; 208/208 mutations refused; 17/17 firmware and 4/4 Makefile edits accepted; 5/6 instrument candidates accepted, one refused; 7/7 instrument-only hostile controls refused; no focused skip |
| Complete gates 1b/35, no RV32 candidates | Exit 0; 182/182 mutations refused; same accepted-edit counts; one registered gate-1b compiler arm NOT RUN; gate 35 passed |
| Gate 1b with riscv64-elf-gcc 15.2.0 | Exit 1; pristine firmware refused on __errno, not skipped or passed |
| Validation-base baseline with the alternate compiler | Exit 1; identical residual refusal |
| Final publication and acceptance probes | Exit 0; each expected observation asserted; individual refusal/acceptance and skip results preserved |
| Documentation/static runner | Exit 0; all fourteen commands passed, individually listed in review-evidence/docs-summary.log |
| NVM host self-test | Exit 0; five shapes and four negative controls |

The fourteen commands include docs_check, doc style/paths, TOC, em-dash against the expected base, feature status, solution docs, bare-metal check/selftest, derived processor sources check/selftest, C++/Python idiom checks, NVM record space and the module matrix. `git diff --check BASE HEAD` also passed.

The focused runner imports the candidate unchanged and redirects only its output directory. The acceptance probe exposes existing nested functions through an in-process AST return before the baseline call; it does not modify their checking logic. These helper observations are separate from complete focused runs. Compiler-absent and alternate-compiler environments use temporary executable symlinks and empty temporary homes; no installed compiler was renamed, removed or modified.

pp_shadow ran from disposable copied sources. The copied recipe changes only `--build -j 0` to `--build -j 8`. Its source list is derived by the real initialized clone's `make -s -C tb/verilator/milan_dp print-srcs` and passed to the staged recipe, preserving relative source paths. An initial staging attempt lacked Git metadata for source discovery and failed before compiling; it is not passing evidence. [Runner and exact command receipts](review-evidence/pp_run.py), [baseline](review-evidence/pp-shadow-final.log), [negative control](review-evidence/pp-shadow-wrong-cap.log).

[R214] SUGGESTION Robustness, Docs - sw/builder/test_builder.py:3667, :4685; review-evidence/builder-elf.log and base-elf.log - clarify the alternate compiler's C-library residual limitation.
Requirement/evidence: the listed alternate compiler passes the RV32 target probe, but emits __errno where the declared residual names __errno_location. Candidate and validation base refuse identically.
Impact: that compiler cannot complete pristine gate 1b. The refusal is conservative; the successful compiler-backed evidence here is specifically from Buildroot.
Required change: optional diagnostic/documentation clarification, or separately validated support for the additional residual spelling. This limitation is not declared fixed by deferral.
Verification: pristine firmware must complete on any newly supported compiler while unresolved-store negative controls remain effective.

Exact-head hosted checks were queried initially and finally with `gh api repos/kebag-logic/milan-fpga/commits/02c47cf0dbe7062ff762068875bf70b721dd6b37/check-runs`. Ten checks succeeded: rtl-fast, docs-check, docs-check-no-git, wire-accountability, elaborate, verilator-lint, yosys-elaboration, bdd-conformance, changes and full-ci-gate. Five were skipped: verilator-suites, yosys-portability, both shard entries and Physical gPTP. The PR remains draft. Skipped long jobs are not successful exhaustive evidence. [Exact-head check names and URLs](review-evidence/hosted-checks.json).

Not run here: builder main beyond gates 1b/35, the whole Verilator sweep, milan_dp simulation, Yosys portability, full processor suites, separate behavior suite, full SoC elaboration, Vivado or hardware. Gate 1b did run its own 46 RTL-mutant elaboration controls; that is not the exhaustive sweep. The manager's full-sweep evidence and prior-head experiments are not claimed as this review's execution. No Docker, act, installation, privilege, subagent, commit, push or public write was used.

Final tracked diffs, including all three required submodules, are empty. No tracked source needed restoration: mutations used in-memory text or disposable sources. Only REVIEW.md and review-evidence/ were added to the clone.

R214 FINISHED

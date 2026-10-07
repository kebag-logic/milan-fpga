[A566]

# Handoff

Status: Local validation complete; independent review pending.
Head: `d6b6ca899ae4c248a1342867bb89060e24febcd5`. Branch: `654-soc-option-refusals`.
Base: `e21c1ca024d37ea188ad15b5c8f9c2dae18628df`.
Origin was verified as the assigned HTTPS repository URL.
Author: [A566]. Internal reviewer: [R550]. External reviewer: [R551].

## Public contract

- Assignment: https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6045462105
- Resume ruling: https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6045774790
- First comment: https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6009639689
- Prior TAKEN: https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6045496540

The ruling supersedes the earlier STOP for this lane.
Acceptance covers the two AX7101 configurations only.
The retired Arty clock refusal belongs to #583 and is excluded.
No second TAKEN was posted. Existing public comments were preserved.
The issue body, first comment, assignment and ruling were read exactly.
REQUIREMENTS.md REQ-VER-03/04 and the build guide govern this change.

## Changes

| File:line | Change and purpose |
|---|---|
| `sw/litex/milan_soc.py:2573` | Shared validation rejects ignored FPU/L2 requests and invalid byte counts |
| `sw/litex/milan_soc.py:2612` | Constructor validates before CPU argument processing or generation |
| `sw/litex/milan_soc.py:3470` | CLI help explains unsupported FPU and the zero/omitted L2 contract |
| `sw/litex/milan_soc.py:3790` | CLI turns validation failures into reasoned exit 2 before platform construction |
| `sw/builder/test_soc_options.py:23` | Real recipe probe; only refusal probes replace setup with a sentinel |
| `sw/builder/test_soc_options.py:119` | Constructor boundary and invalid-option matrix at both register widths |
| `sw/builder/test_soc_options.py:143` | CLI refusal, product-profile and valid-zero/omission cases |
| `sw/builder/test_soc_options.py:158` | Six in-memory check-removal controls |
| `sw/builder/test_soc_options.py:202` | Actual NaxRiscv netlist comparisons and four lost-forwarding controls |
| `sw/builder/test_builder.py:28727` | Builder bank invokes the refusal bank through its required-interpreter ledger |
| `sw/builder/test_builder.py:29036` | Registers that test in the normal builder run |
| `docs/integration/BUILDING.md:136` | Documents both entry points, reasons, supported effects and validation commands |

Scope remains option validation, its tests, and the build guide.
No defaults, shipping configuration, CPU generator source, RTL, register map,
filter or mailbox was changed. No hardware, synthesis or implementation ran.
No push, PR operation, rebase or merge was performed.

## Measurements and decisions

All sixteen baseline constructor/export invocations returned 0.
Each CPU family was measured at RV32 and RV64 with one hart.
Options were omitted, FPU enabled, L2=8192, and explicit L2=0.
The baseline used the unchanged source at the assigned base.
CPU exports used the real constructor and Builder, with software compilation
and vendor execution disabled. Separate processes prevent class-state leakage.
CPU data and generated netlists live in scratch, outside the repository.

| CPU path, both widths | Measurement | Decision |
|---|---|---|
| VexiiRiscv FPU | Raw netlist bytes identical to omission | Refuse before setup; no floating-point hardware enabled |
| VexiiRiscv L2=8192 | Only generated name/comments change; normalized RTL identical | Refuse nonzero L2 for this cacheless recipe |
| VexiiRiscv L2=0 | Raw bytes identical to omission | Preserve zero and omitted requests |
| NaxRiscv FPU | Raw and normalized RTL both change | Preserve existing effect and test it |
| NaxRiscv L2=8192 | Raw and normalized RTL both change | Preserve positive-size effect and test it |
| NaxRiscv L2=0 | Raw bytes identical to omission; default L2 remains | Refuse explicit zero with its reason |

The L2 RTL delta includes cache-bank address widths and RAM geometry,
not just the module name. The FPU delta adds floating-point circuitry.
The product CLI still accepts only single-hart RV32 VexiiRiscv.
NaxRiscv remains a developer constructor path, not another CLI product.
The CLI's pre-existing profile refusals are preserved.
NaxRiscv data package: `20da269306bb3bfabd09de08d4c1be1fbc202474` (clean tracked files).
NaxRiscv source: `9f452d50560d02fb391bc8039f5453c54e0911af`.
Its SpinalHDL source: `c362657003fa178350d6955055867e9ab363c44a`.
VexiiRiscv source: `235753e24f2d960e49a0852205bae1400bf22c19`,
with the repository's existing patch series, checked by the builder gate.
Generator sources were frozen; none was patched for this lane.

`CPU-MEASUREMENTS.json` retains every raw size/digest and normalized RTL digest.
Normalization removes line comments and substitutes the generated module name;
it is used only to distinguish CPU hardware effects from naming changes.

| Baseline case | Bytes | Raw SHA-256 |
|---|---:|---|
| naxriscv-32-fpu | 6207896 | `94b79c574fb6e94c6aa46033d5263b3ea585b248e3ee0d0dd7ce34f164f04242` |
| naxriscv-32-l2 | 4853606 | `7afcade70d9688a10ea1fc84c0c3a343ede6ac4f1e5ea92f458abce40c195d91` |
| naxriscv-32-none | 4853653 | `89eb8f5ce7632bf5065f97fe408a6edf54924d0e4acfbccb8a979328d58be513` |
| naxriscv-32-zero | 4853653 | `89eb8f5ce7632bf5065f97fe408a6edf54924d0e4acfbccb8a979328d58be513` |
| naxriscv-64-fpu | 6303392 | `249e3e7bc3ec1c16fb7539219d0b323b1a5e73f6a6c39ccc4caee4df69a03f3d` |
| naxriscv-64-l2 | 4961618 | `b36e843975c09ffab96bcf1d2e19b5e226f9a595ba476a0f87454782b8df4ab8` |
| naxriscv-64-none | 4961665 | `e7f7af143c0ddb372f2cbeda21b4ba80e7f6aa603dcbb0910d8273dab575dba0` |
| naxriscv-64-zero | 4961665 | `e7f7af143c0ddb372f2cbeda21b4ba80e7f6aa603dcbb0910d8273dab575dba0` |
| vexiiriscv-32-fpu | 904947 | `c78bf94d062deea0bf456863348585ebaadd69fb1b56cf7c38ec6f8bc189a725` |
| vexiiriscv-32-l2 | 904947 | `fef96aa312b30a72bec08b291fb32f7619f88a7ea95f14c2b23f13db234aefe3` |
| vexiiriscv-32-none | 904947 | `c78bf94d062deea0bf456863348585ebaadd69fb1b56cf7c38ec6f8bc189a725` |
| vexiiriscv-32-zero | 904947 | `c78bf94d062deea0bf456863348585ebaadd69fb1b56cf7c38ec6f8bc189a725` |
| vexiiriscv-64-fpu | 976930 | `3cbf182bcb4858a522b1ecc8746afc7f1bb8ec91f9ec824d368b561903fb016e` |
| vexiiriscv-64-l2 | 976930 | `c42010fbf9c7fe4fe8d93f950b40fff702d73752303428058a979c9a514b4959` |
| vexiiriscv-64-none | 976930 | `3cbf182bcb4858a522b1ecc8746afc7f1bb8ec91f9ec824d368b561903fb016e` |
| vexiiriscv-64-zero | 976930 | `3cbf182bcb4858a522b1ecc8746afc7f1bb8ec91f9ec824d368b561903fb016e` |

## AX7101 byte identity

Each configuration was generated from base and candidate with the same argv,
paths, cached CPU, fixed wall-clock input, and deterministic diagnostic ordering.
`export_compare.py` is the portable reproduction harness alongside this handoff.
It loads the base recipe from its Git blob without changing the checkout.
Both versions retain the real recipe path for relative-source resolution.
It runs the configuration's emitted argv with `--no-compile-software`.
The absent `--build` keeps synthesis and implementation out of the export.

Generated banners otherwise contain wall-clock time. The hierarchy comment
sorts blackbox objects by their address representation. The harness fixes
`time.time()` to 1700000000 and gives `Instance.__repr__` its stable duid.
These equal diagnostic inputs apply to both exports before generation.
They do not modify any source file, CPU generation, or RTL lowering.
RTL lowering already sorts special instances by duid.
No generated artifact is normalized or rewritten for the comparison.
Every raw file is compared directly and separately hashed.

`litex.log` is a diagnostic log, excluded from the build-artifact population.
Its real start time and interleaved stdout/stderr differ across executions.
Its size and hash remain recorded with the other logs in `ARTIFACTS.json`.
The first uncontrolled comparisons failed on these metadata differences;
they are not presented as successful byte-identity evidence.
The original baseline manifests and logs remain preserved.

| Configuration | Generated files | Total bytes | Shared manifest SHA-256 |
|---|---:|---:|---|
| ax7101_8x8 | 32 | 2087704 | `5e691b10158760c80072f6b8eda42fb222d888281cee3f6a2498c612db64ff6a` |
| ax7101_1x1_tdm8 | 32 | 1997160 | `6f2ad2b855a96e3e746aeb85beaa2dcd2014c754935d1e70944674cd92c7869b` |

`EQUIVALENCE.json` records the complete path, size and digest population.
It includes top-level gateware, memory images, firmware headers, CSR export,
constraints, build scripts, AEM bytes, configuration metadata and flash manifest.
The shipping configuration is `ax7101_1x1_tdm8`.
These are gateware/software-input exports, not newly compiled bitstreams.

## Tests and planted defects

| Test | Concrete defect detected | Planted control / result |
|---|---|---|
| Vexii constructor, RV32/RV64 FPU | Silently accepted FPU without hardware | Remove FPU refusal; named-refusal assertion fails |
| Vexii constructor, RV32/RV64 L2 | Accepted nonzero cache size on cacheless recipe | Remove L2 refusal; setup is reached and test fails |
| NaxRiscv constructor, RV32/RV64 zero | Explicit zero retains the default cache | Remove zero refusal; setup is reached and test fails |
| Both CPUs, negative/fractional/NaN/infinite sizes | Truncated or invalid size reaches CPU setup | Remove byte validation; fractional-size test fails |
| Constructor call boundary | Validator exists but the constructor does not call it | Remove call; setup sentinel makes refusal test fail |
| CLI call boundary | Validator is bypassed and only generic profile errors remain | Remove CLI call; reason check fails |
| Both CPUs' accepted controls | New checks reject valid omission/zero/working NaxRiscv options | Real checks reach setup as required |
| NaxRiscv FPU effect, RV32/RV64 | FPU request loses hardware forwarding | Remove both FPU forwarding channels; netlist equals baseline and test fails |
| NaxRiscv L2 effect, RV32/RV64 | Requested positive size is dropped | Remove size forwarding; netlist equals baseline and test fails |
| Both AX7101 exports | A supposedly validation-only edit changes generated build inputs | Exact per-file byte comparison; no mutation claimed |
| Full builder bank | Recipe, generated artifact and firmware contracts regress | Existing planted controls run as part of the bank |
| LiteX simulation aggregate | Memory crossings, timestamps, freeze or bridge regress | Four existing self-checking simulations; no new mutation claim |
| Lint/docs/style gates | New structural, policy, link or style violations | Existing gate controls; no new mutation claim |

The focused bank reports 36 constructor cases, 11 CLI cases, and six killed
refusal controls. The effect run adds four netlist effects and four killed
forwarding controls. Probe/compilation failures raise RuntimeError and cannot
be mistaken for a killed assertion. Missing generator dependencies fail;
the optional `--netlists` mode is explicit and was run here.
The ordinary builder invocation includes the refusal bank.

## Acceptance coverage

| Contract item | Evidence | State |
|---|---|---|
| Measure every accepted CPU family at both widths | Sixteen baseline rows, all rc 0 | Met |
| Reasoned refusal before any build, or effect | CLI exit 2 and constructor ValueError before setup; four NaxRiscv effects | Met |
| Tests with planted controls | Six refusal and four forwarding controls killed | Met |
| Product configurations unchanged | Both AX7101 exports, 32 raw artifacts each, equal | Met |
| Builder, LiteX simulations, lint and docs gates | Exact command table below | Met |

## Gate table

All gate commands run directly, without piping their verdicts.
`<scratch>` in the command table is `$VALIDATION_STORAGE/654-a566`.
Each exact expanded invocation is preserved in its scratch `.command` file.
The environment selects the installed pinned interpreter and Verilator 5.050,
sets `VERILATOR_JOBS=2`, `MAKEFLAGS=-j8`, and uses disk-backed scratch.
Markdown gates use the hash-pinned `tools/markdown/requirements.txt` environment.
An initial missing-renderer refusal was resolved by installing those pinned
requirements into a scratch-only environment and rerunning the affected gates.

| Gate command | rc | Evidence log |
|---|---:|---|
| `python3 sw/builder/test_soc_options.py --netlists --nax-data-dir <scratch>/cpu/naxriscv` | 0 | `option-netlists.log` |
| `python3 export_compare.py baseline-fixed <AX-config>; python3 export_compare.py candidate-fixed <AX-config>` | 0 | `compare-ax.log` |
| `python3 -u sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | `builder.log` |
| `scripts/run_litex_sims.sh <scratch>/litex-sim-logs` | 0 | `litex-sims.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |
| `bash <scratch>/final-checks.sh` | 0 | `final-checks.log` |
| `python3 scripts/check_baremetal_only.py --check` | 0 | `docs-check_baremetal_only.log` |
| `python3 scripts/check_deploy_shape.py --self-test` | 0 | `docs-check_deploy_shape.log` |
| `python3 scripts/check_doc_paths.py` | 0 | `docs-check_doc_paths.log` |
| `python3 scripts/check_doc_style.py` | 0 | `docs-check_doc_style.log` |
| `python3 scripts/check_entity_shape.py --self-test` | 0 | `docs-check_entity_shape.log` |
| `python3 scripts/check_feature_status.py` | 0 | `docs-check_feature_status.log` |
| `python3 scripts/check_gptp_docs.py` | 0 | `docs-check_gptp_docs.log` |
| `python3 scripts/check_hygiene.py --check` | 0 | `docs-check_hygiene.log` |
| `python3 scripts/check_port_contracts.py` | 0 | `docs-check_port_contracts.log` |
| `python3 scripts/check_py_idiom.py` | 0 | `docs-check_py_idiom.log` |
| `python3 scripts/check_soc_sources.py` | 0 | `docs-check_soc_sources.log` |
| `python3 scripts/check_solution_docs.py` | 0 | `docs-check_solution_docs.log` |
| `python3 scripts/check_submodule_docs.py` | 0 | `docs-check_submodule_docs.log` |
| `python3 scripts/check_sweep_shape.py --self-test` | 0 | `docs-check_sweep_shape.log` |
| `python3 scripts/check_todo_ownership.py` | 0 | `docs-check_todo_ownership.log` |
| `python3 scripts/docs_check.py` | 0 | `docs-docs_check.log` |
| `python3 scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | `docs-em-dash.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `docs-matrix.log` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `docs-measure_fail_fast.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `docs-measure_naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `docs-measure_test_evidence.log` |
| `python3 scripts/gen_toc.py --check` | 0 | `docs-toc--check.log` |
| `python3 scripts/gen_toc.py --verify-anchors` | 0 | `docs-toc--verify-anchors.log` |

The builder returned 0 with one declared unavailable historical arm:
`gate 11`, the retired Arty mf48 utilization report is absent.
It reports `ALL GATES PASS EXCEPT 1 NOT RUN` and explicitly says that arm
is not covered. All required elaboration and RV32 compiler arms ran.
No missing-report acceptance claim is made; this lane's product comparison
covers only AX7101 under the manager ruling. No historical report was fabricated.

The AX comparison has per-phase/per-configuration logs and rc files.
All logs remain in scratch; the artifact index records size and SHA-256.
Long jobs run under detached process groups with foreground waits and their
own logs/rc files; no process is intentionally left behind at handoff.

## Independent review coverage

This is implementation evidence, not a review verdict.

| Lens | Covering round | Head |
|---|---|---|
| Conformance | Pending independent review | None |
| RTL | Pending independent review | None |
| Robustness | Pending independent review | None |
| Tests | Pending independent review | None |
| Docs | Pending independent review | None |

No hosted contexts, candidate-merge validation or post-merge containment are
claimed; this assignment prohibits push, PR operations and merge.

## Resource and artifact handling

Baseline measurements from the prior stop remain available.
The prior stop recorded a transient cache-memory overshoot in that earlier run;
the resumed service recorded a peak of 9,326,645,248 bytes (8.69 GiB).
That is below 9 GiB, but above 9 GB in decimal units. No OOM occurred.
Current usage after the builder run is about 1.4 GB.
Free disk space has remained above the 30 GB floor.
Generated test outputs were moved from the worktree into scratch.
The committed worktree and index are clean.
No environment, installed package, source export or generated netlist is stored
in this output directory. Every file here is below 200 KB.
`ARTIFACTS.json` records external logs and measurements by relative scratch path and hash.
The complete 1,299-entry manifest remains in scratch as `artifact-full.json`;
its size and SHA-256 are recorded in the compact output index.
`RESOURCE-USE.json` records the final counters and remaining disk space.
All owned background process groups have completed.
`PR-BODY.md` follows the repository template and is ready for the authorized
publisher to use after review. No publication or approval is implied.

## Public status

Posted `[A566] REVIEW READY` at the committed head:
https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6046393891
No further lane work is running.

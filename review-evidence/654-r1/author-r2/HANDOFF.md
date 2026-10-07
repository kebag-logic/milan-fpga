[A566]

# Handoff

Current work: see Round 2 below. The preceding evidence is round 1.

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

## Round 2

Status: Local validation complete at the final head; independent re-review pending.
Head: `853a7357ba86d758a0e38f65db89a6187fb547bc`. Parent under review: `d6b6ca899ae4c248a1342867bb89060e24febcd5`.
Assignment: https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6046709819
Reviews: PR #694 comments 6046673982 (external) and 6046704603 (internal).
Origin, branch, clean starting tree and the PR head were confirmed.
No second TAKEN was posted. The branch contains two new local commits:

- `cd3bd2d79385215df0690873d2412aae00d2f22a`: exact byte-count parsing, unknown CPU refusals and review documentation.
- `853a7357ba86d758a0e38f65db89a6187fb547bc`: wrap one mutation anchor to satisfy the Python line-length gate.

Both use the configured identity and one-line subjects without trailers.
Round 1 above remains historical evidence; this section governs the resumed head.

### Changes and review disposition

| File:line | Change | Review item |
|---|---|---|
| `sw/litex/milan_soc.py:38` | Imports exact decimal arithmetic for byte counts | R551-1-F1 |
| `sw/litex/milan_soc.py:2573` | Parses the original token without binary-float rounding; malformed tokens receive the whole-byte reason | R551-1-F1 |
| `sw/litex/milan_soc.py:2584` | Refuses unknown constructor CPU names before setup | R550-1 S2 |
| `sw/litex/milan_soc.py:2586` | Checks finiteness, sign and integrality against the preserved value | R551-1-F1 |
| `sw/litex/milan_soc.py:3495` | Routes the CLI byte-count argument through the exact parser | R551-1-F1 |
| `sw/builder/test_soc_options.py:140` | Unknown names, empty name and missing name at both widths, with omitted and explicit-zero L2 | R550-1 S2 |
| `sw/builder/test_soc_options.py:147` | Positive/negative underflow, precision beyond binary float, malformed tokens and genuine-zero controls | R551-1-F1 |
| `sw/builder/test_soc_options.py:179` | Updates the existing byte-validation mutation anchor without weakening its assertion | R551-1-F1 |
| `sw/builder/test_soc_options.py:183` | Plants removal of the unknown-CPU refusal | R550-1 S2 |
| `sw/builder/test_soc_options.py:201` | Restores float parsing separately for each underflow token; both controls are killed | R551-1-F1 |
| `sw/builder/test_soc_options.py:208` | Reports actual case/control counts | Test evidence |
| `docs/integration/BUILDING.md:133` | Restores the explicit section 2.1 reference | R550-1 RESIDUE |
| `docs/integration/BUILDING.md:148` | Documents fractional-token and unknown-CPU behavior | R551-1-F1, R550-1 S2 |
| `docs/integration/BUILDING.md:159` | Documents caching and `--nax-data-dir` isolation | R550-1 S1 |

These items are implemented, pending independent re-review.
The reviewer's lens labels remain unchanged. No new verdict is claimed.
Defaults, CPU forwarding, generator sources, configurations, RTL and gitlinks are unchanged.
No register-map, filter or mailbox change was needed.

### Tests and planted defects

| Test | Planted defect it catches | Evidence |
|---|---|---|
| CLI `1e-400` and `-1e-400` | Replace the exact parser with `float`, letting each nonzero fraction become zero | Both separately killed; exit 2 and whole-byte reason required before setup |
| CLI long fractional token | Binary-float rounding discards a fractional suffix | Refused with whole-byte reason; shared lossy-parser controls above |
| CLI malformed token | Numeric conversion escapes without a parser refusal | Exit 2 and named reason; no separate mutation claimed |
| CLI omission, `0`, `0.0`, `-0`, `0e-400` | Over-refusal of supported zero forms | All reach setup; no separate new mutation claimed |
| Constructor unknown CPU matrix | Remove the supported-name guard so `NaxRiscv` with zero falls through to NaxRiscv setup | Guard-removal control killed; 16 cases across RV32/RV64 |
| Existing constructor and CLI refusal bank | Remove FPU, cacheless L2, NaxRiscv zero, byte-validation or entry-point checks | Six existing controls remain killed |
| RV32/RV64 FPU and positive-L2 netlists | Remove FPU or L2 forwarding | Four effects retained; four forwarding controls killed |
| Unmodified reviewer underflow probe | Original float parser silently underflows | rc 1 before correction; rc 0 at final head; genuine zero still reaches setup |
| AX7101 raw export comparisons | Any change to generated product inputs | 32/32 files equal per configuration; no new mutation claimed |
| Builder, simulations, lint and docs | Existing recipe, generation, integration or policy defects | Existing banks and their controls; results below |

Final focused totals: 52 constructor cases, 18 CLI cases, nine killed refusal controls.
Netlist mode adds four hardware effects and four killed forwarding controls.
The reviewer probe was downloaded unchanged from public blob
`161fe7f3365579a0f89b918197dffe111b95f287` on `654-review-evidence`.
Both invalid underflow tokens exit 2 with the finite/non-negative/whole-number reason.
The probe's pre-fix failure is expected negative evidence, not a passing gate.

### Acceptance coverage

| Contract item | Current evidence | State |
|---|---|---|
| Validate byte-count tokens without fractional underflow | Focused bank and unchanged reviewer probe | Met |
| Keep omission and genuine zero semantics | Five accepted CLI forms, existing constructor matrix, AX exports | Met |
| Preserve existing refusals and constructor effects | Nine refusal controls; four netlist effects and four forwarding controls | Met |
| Refuse unknown constructor CPU values | 16 added constructor cases and guard-removal control | Met |
| Fix cross-reference and describe isolated generator data | BUILDING.md:133,159; docs gates | Met |
| Keep both AX7101 outputs byte-identical | ROUND2-EQUIVALENCE.json; raw snapshots in scratch | Met |
| Required fresh local validation | Every final command returns 0; historical Arty report arm remains NOT RUN | Met |

### Gate table

Commands execute directly; no gate verdict is piped.
The scratch runner records each expanded invocation in its `.command` file.
The existing pinned environment is retained. Every long gate runs under
`setsid nohup`, with its own log/rc files and short foreground waits.
`<scratch>` below denotes the assigned disk-backed scratch directory.
`<review-probe>` denotes the unchanged public review script described above.

| Command | rc | Round 2 receipt |
|---|---:|---|
| `python3 sw/builder/test_soc_options.py` | 0 | `final-refusals.log` |
| `python3 <review-probe>/byte_count_underflow.py <source-root>` | 0 | `final-underflow.log` |
| `python3 sw/builder/test_soc_options.py --netlists --nax-data-dir <scratch>/cpu/naxriscv` | 0 | `final-netlists.log` |
| `python3 export_compare.py baseline-fixed ax7101_8x8` | 0 | `ax-baseline-fixed-ax7101_8x8.log` |
| `python3 export_compare.py candidate-fixed ax7101_8x8` | 0 | `ax-candidate-fixed-ax7101_8x8.log` |
| `python3 export_compare.py baseline-fixed ax7101_1x1_tdm8` | 0 | `ax-baseline-fixed-ax7101_1x1_tdm8.log` |
| `python3 export_compare.py candidate-fixed ax7101_1x1_tdm8` | 0 | `ax-candidate-fixed-ax7101_1x1_tdm8.log` |
| `python3 -u sw/builder/test_builder.py --require-elaboration --require-rv32` | 0 | `builder.log` |
| `scripts/run_litex_sims.sh <scratch>/round2/sim-logs` | 0 | `sims.log` |
| `python3 scripts/lint_rtl.py --check` | 0 | `lint.log` |
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
| `<docs-python> scripts/check_em_dash.py --base e21c1ca024d37ea188ad15b5c8f9c2dae18628df` | 0 | `docs-em-dash.log` |
| `python3 docs/traceability/gen_module_matrix.py --check` | 0 | `docs-matrix.log` |
| `python3 scripts/measure_fail_fast.py --check` | 0 | `docs-measure_fail_fast.log` |
| `python3 scripts/measure_naming.py --check` | 0 | `docs-measure_naming.log` |
| `python3 scripts/measure_test_evidence.py --check` | 0 | `docs-measure_test_evidence.log` |
| `<docs-python> scripts/gen_toc.py --check` | 0 | `docs-toc--check.log` |
| `<docs-python> scripts/gen_toc.py --verify-anchors` | 0 | `docs-toc--verify-anchors.log` |

The builder returned 0 with `ALL GATES PASS EXCEPT 1 NOT RUN`.
Its one missing arm is the historical Arty mf48 utilization report (gate 11).
All required elaboration and RV32 compiler arms ran. This is the same declared
limitation as round 1; no evidence for that unavailable report is claimed.
The four simulations passed with zero failures, skips or timeouts.

The first docs run found one new overlong mutation-anchor line.
The follow-up commit wraps that source string; the same gate now returns 0.
The original failed receipt remains under `round2/initial-docs/`.
No budget, test assertion or acceptance condition was weakened.

Both AX comparisons reran from the original source base at the final head.
They use the round 1 harness and identical pre-generation diagnostic inputs.
No artifact bytes are normalized. Only diagnostic logs are excluded.
The raw artifact totals are 2,087,740 bytes (8x8) and 1,997,196 bytes (1x1 TDM8).
Absolute export paths account for the difference from round 1 totals/digests;
base and candidate are equal within each round. `path-provenance.json` proves
that each configuration differs from round 1 only in two output-path strings:
`alinx_ax7101.tcl` and `variables.mak`, each 18 bytes longer.
ROUND2-EQUIVALENCE.json records
all 64 path/size/digest rows. These remain exports, not physical-image evidence.

### Independent review coverage

The previous independent verdicts apply to `d6b6ca899ae4c248a1342867bb89060e24febcd5`.
The external reviewer left F1 open under Conformance, Robustness, Tests and Docs.
The internal reviewer recorded a positive verdict plus residue/suggestions.
The current head requires reviewer-owned reassessment; implementation evidence
below does not clear any reviewer ledger row.

| Lens | Current covering round | Head |
|---|---|---|
| Conformance | Pending independent re-review of F1 correction | None |
| RTL | Prior clean results exist; current applicability awaits reviewer confirmation | None |
| Robustness | Pending independent re-review of F1 and unknown-CPU change | None |
| Tests | Pending independent re-review of expanded cases and controls | None |
| Docs | Pending independent re-review of contract wording and evidence | None |

### Resource and publication status

Memory reclaim starts at 8,000,000,000 bytes, below the 9 GB ceiling.
The resource monitor samples service memory and free disk every five seconds.
Kernel peak memory was 8,231,006,208 bytes.
Minimum sampled free disk was 169,753,063,424 bytes.
No OOM event occurred. All owned background process groups have finished.
ROUND2-RESOURCE-USE.json records counters and disk measurements.
ROUND2-ARTIFACTS.json records receipt sizes and SHA-256 digests.
The complete 803-file manifest stays in scratch as `artifact-full.json`;
its size and digest are included in the output index.
All output files are below 200 KB; no packages or generated trees are stored there.
The 406 generated/ignored worktree files were moved to scratch after validation.
The index and working tree are clean, including ignored files.
Final source hashes match those recorded before the gates.
All three required submodules remain clean at their pins.
The final tree is `78af3f0b2ca316ad2b14440ff7bd4d64ca322bd2`.
`final-integrity.json` records the checks and final return codes.
No push, PR edit, merge, rebase, amend, hardware access or flashing was performed.
The manager retains publication, hosted/local-replica acceptance, independent
review completion, candidate-merge validation, merge authorization and containment.
Posted `[A566] REVIEW READY` at the final head:
https://github.com/kebag-logic/milan-fpga/issues/654#issuecomment-6047197977
No further lane work is running.
